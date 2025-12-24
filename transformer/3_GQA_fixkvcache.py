import torch
import torch.nn as nn
import math

"""
Grouped-Query Attention (GQA) with Fixed-Length KV Cache

GQA是MHA和MQA的折中方案：
- MHA (Multi-Head Attention): 每个Q头对应独立的K、V头
- MQA (Multi-Query Attention): 所有Q头共享同一组K、V
- GQA: Q头分组，每组共享同一组K、V

示例：32个Q头，4个KV头
- Q头分成4组，每组8个Q头
- 每组共享1个K头和1个V头
- 内存节省: 32个KV头 → 4个KV头 (8x节省)
"""

class GroupedQueryAttention(nn.Module):
    """
    GQA实现，使用固定长度的KV Cache
    
    典型配置（Llama 2 70B）：
    - d_model: 8192
    - num_q_heads: 64
    - num_kv_heads: 8  (每8个Q头共享1个KV头)
    - kv_cache_max_len: 4096
    """
    def __init__(
        self, 
        d_model=4096,
        num_q_heads=32,
        num_kv_heads=4,  # GQA的关键参数
        kv_cache_max_len=2048,
        dropout=0.1
    ):
        super().__init__()
        
        assert num_q_heads % num_kv_heads == 0, \
            "num_q_heads必须能被num_kv_heads整除"
        
        self.d_model = d_model
        self.num_q_heads = num_q_heads
        self.num_kv_heads = num_kv_heads
        self.num_groups = num_q_heads // num_kv_heads  # 每组有多少个Q头
        self.d_k = d_model // num_q_heads
        self.kv_cache_max_len = kv_cache_max_len
        
        # Q投影：输出维度 = num_q_heads * d_k
        self.W_q = nn.Linear(d_model, num_q_heads * self.d_k, bias=False)
        
        # K、V投影：输出维度 = num_kv_heads * d_k (注意：更少的头)
        self.W_k = nn.Linear(d_model, num_kv_heads * self.d_k, bias=False)
        self.W_v = nn.Linear(d_model, num_kv_heads * self.d_k, bias=False)
        
        self.W_o = nn.Linear(num_q_heads * self.d_k, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)
        
        print(f"GQA配置:")
        print(f"  Q heads: {num_q_heads}")
        print(f"  KV heads: {num_kv_heads}")
        print(f"  Groups: {self.num_groups} (每{self.num_groups}个Q头共享1个KV头)")
        print(f"  d_k: {self.d_k}")
        print(f"  KV Cache最大长度: {kv_cache_max_len}\n")
    
    def init_kv_cache(self, batch_size, dtype=torch.float16, device='cuda'):
        """
        初始化固定长度的KV Cache
        
        关键设计：预分配固定大小的缓冲区
        - 避免推理时动态申请内存（慢）
        - 避免频繁的concat操作
        - 使用索引更新，速度快
        
        Returns:
            kv_cache: dict包含
                - k_cache: [batch, num_kv_heads, max_len, d_k]
                - v_cache: [batch, num_kv_heads, max_len, d_k]
                - cache_position: 当前已使用的长度
        """
        k_cache = torch.zeros(
            batch_size, 
            self.num_kv_heads, 
            self.kv_cache_max_len, 
            self.d_k,
            dtype=dtype,
            device=device
        )
        
        v_cache = torch.zeros(
            batch_size,
            self.num_kv_heads,
            self.kv_cache_max_len,
            self.d_k,
            dtype=dtype,
            device=device
        )
        
        cache_position = torch.zeros(batch_size, dtype=torch.long, device=device)
        
        print(f"初始化KV Cache:")
        print(f"  K Cache shape: {k_cache.shape}")
        print(f"  V Cache shape: {v_cache.shape}")
        print(f"  内存占用: {k_cache.element_size() * k_cache.numel() * 2 / 1024**2:.2f} MB")
        
        return {
            'k_cache': k_cache,
            'v_cache': v_cache,
            'cache_position': cache_position
        }
    
    def update_kv_cache(self, kv_cache, new_k, new_v, seq_len):
        """
        更新KV Cache：使用索引赋值而非concat
        
        Args:
            kv_cache: 当前的cache字典
            new_k: [batch, num_kv_heads, seq_len, d_k] 新的K
            new_v: [batch, num_kv_heads, seq_len, d_k] 新的V
            seq_len: 本次新增的序列长度
            
        核心思想：
            cache[start:end] = new_data
            而不是 cache = concat(cache, new_data)
        """
        batch_size = new_k.size(0)
        start_pos = kv_cache['cache_position'][0].item()  # 假设batch内位置相同
        end_pos = start_pos + seq_len
        
        if end_pos > self.kv_cache_max_len:
            raise RuntimeError(
                f"KV Cache溢出: 需要{end_pos}个位置, 但最大长度为{self.kv_cache_max_len}"
            )
        
        # 使用索引赋值更新cache (in-place操作，不申请新内存)
        kv_cache['k_cache'][:, :, start_pos:end_pos, :] = new_k
        kv_cache['v_cache'][:, :, start_pos:end_pos, :] = new_v
        
        # 更新位置指针
        kv_cache['cache_position'][:] = end_pos
        
        print(f"更新KV Cache: [{start_pos}:{end_pos}], 当前已用长度: {end_pos}")
        
        return kv_cache
    
    def repeat_kv(self, kv, num_groups):
        """
        GQA的核心操作：将KV头复制扩展以匹配Q头数量
        
        例如：
            输入: [batch, 4_kv_heads, seq, d_k]
            num_groups: 8 (每个KV头要服务8个Q头)
            输出: [batch, 32_q_heads, seq, d_k]
        
        实现方式：
            [b, kv_h, s, d] 
            -> [b, kv_h, 1, s, d]      # 插入新维度
            -> [b, kv_h, groups, s, d] # 在新维度上repeat
            -> [b, kv_h*groups, s, d]  # reshape合并
        """
        if num_groups == 1:
            return kv
        
        batch, num_kv_heads, seq_len, d_k = kv.shape
        
        # 方法1：使用repeat_interleave (推荐，更清晰)
        # [b, kv_h, s, d] -> [b, kv_h*groups, s, d]
        kv_expanded = kv.repeat_interleave(num_groups, dim=1)
        
        return kv_expanded
    
    def forward(self, x, kv_cache=None, use_cache=False):
        """
        Args:
            x: [batch, seq_len, d_model] 输入
            kv_cache: KV缓存字典 (推理时使用)
            use_cache: 是否更新并返回cache
            
        Returns:
            output: [batch, seq_len, d_model]
            kv_cache: 更新后的cache (if use_cache)
        """
        batch_size, seq_len, _ = x.shape
        
        # ========== 步骤1: QKV投影 ==========
        Q = self.W_q(x)  # [batch, seq_len, num_q_heads * d_k]
        K = self.W_k(x)  # [batch, seq_len, num_kv_heads * d_k]
        V = self.W_v(x)  # [batch, seq_len, num_kv_heads * d_k]
        
        # ========== 步骤2: Reshape分头 ==========
        Q = Q.view(batch_size, seq_len, self.num_q_heads, self.d_k)
        K = K.view(batch_size, seq_len, self.num_kv_heads, self.d_k)
        V = V.view(batch_size, seq_len, self.num_kv_heads, self.d_k)
        
        # Transpose: [batch, num_heads, seq_len, d_k]
        Q = Q.transpose(1, 2)
        K = K.transpose(1, 2)
        V = V.transpose(1, 2)
        
        print(f"\n投影后形状:")
        print(f"  Q: {Q.shape}  # {self.num_q_heads}个Q头")
        print(f"  K: {K.shape}  # {self.num_kv_heads}个KV头")
        print(f"  V: {V.shape}")
        
        # ========== 步骤3: KV Cache处理 ==========
        if use_cache:
            if kv_cache is None:
                # 首次调用：初始化cache
                kv_cache = self.init_kv_cache(
                    batch_size, 
                    dtype=K.dtype, 
                    device=K.device
                )
            
            # 更新cache (in-place操作)
            kv_cache = self.update_kv_cache(kv_cache, K, V, seq_len)
            
            # 从cache中取出有效部分
            cache_len = kv_cache['cache_position'][0].item()
            K = kv_cache['k_cache'][:, :, :cache_len, :]  # [b, kv_h, cache_len, d_k]
            V = kv_cache['v_cache'][:, :, :cache_len, :]
            
            print(f"使用Cache: 有效长度 {cache_len}")
        
        # ========== 步骤4: GQA的关键 - 扩展KV头 ==========
        # K, V: [batch, num_kv_heads, seq, d_k]
        # 需要扩展为: [batch, num_q_heads, seq, d_k]
        K = self.repeat_kv(K, self.num_groups)
        V = self.repeat_kv(V, self.num_groups)
        
        print(f"\nGQA扩展后:")
        print(f"  K: {K.shape}  # 扩展到{self.num_q_heads}个头")
        print(f"  V: {V.shape}")
        
        # ========== 步骤5: 计算注意力 ==========
        # Q: [batch, num_q_heads, seq_q, d_k]
        # K: [batch, num_q_heads, seq_k, d_k] (已扩展)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        # Causal mask (自回归)
        if seq_len > 1:  # 训练或prefill阶段
            mask = torch.triu(
                torch.ones(seq_len, scores.size(-1), device=scores.device),
                diagonal=scores.size(-1) - seq_len + 1
            )
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        attn_weights = torch.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        
        # 加权求和
        output = torch.matmul(attn_weights, V)  # [batch, num_q_heads, seq_q, d_k]
        
        # ========== 步骤6: 合并多头 ==========
        output = output.transpose(1, 2).contiguous()
        output = output.view(batch_size, seq_len, self.num_q_heads * self.d_k)
        
        # 输出投影
        output = self.W_o(output)
        
        if use_cache:
            return output, kv_cache
        return output, None


# ==================== 对比测试 ====================
def compare_mha_gqa_mqa():
    """
    对比三种注意力机制的内存占用和计算量
    """
    print("=" * 70)
    print("MHA vs GQA vs MQA 对比分析")
    print("=" * 70)
    
    d_model = 4096
    num_q_heads = 32
    seq_len = 2048
    d_k = d_model // num_q_heads  # 128
    
    # 计算KV Cache的内存占用 (fp16 = 2 bytes)
    bytes_per_element = 2
    
    configs = {
        'MHA': {'kv_heads': 32, 'description': '每个Q头有独立的KV头'},
        'GQA': {'kv_heads': 8, 'description': '4个Q头共享1个KV头'},
        'MQA': {'kv_heads': 1, 'description': '所有Q头共享1个KV头'}
    }
    
    print(f"\n配置:")
    print(f"  模型维度: {d_model}")
    print(f"  Q头数: {num_q_heads}")
    print(f"  序列长度: {seq_len}")
    print(f"  d_k: {d_k}")
    print(f"\n" + "-" * 70)
    
    for name, config in configs.items():
        kv_heads = config['kv_heads']
        
        # KV Cache大小: 2 (K和V) × batch × kv_heads × seq_len × d_k × bytes
        kv_cache_size = 2 * kv_heads * seq_len * d_k * bytes_per_element
        kv_cache_mb = kv_cache_size / (1024 ** 2)
        
        # 相对MHA的内存节省
        ratio = 32 / kv_heads
        
        print(f"\n{name}:")
        print(f"  {config['description']}")
        print(f"  KV头数: {kv_heads}")
        print(f"  KV Cache (单样本): {kv_cache_mb:.2f} MB")
        print(f"  相对MHA: {ratio:.1f}x 内存节省")


def test_gqa_inference():
    """
    测试GQA推理流程：Prefill + Decode
    """
    print("\n" + "=" * 70)
    print("GQA推理流程测试")
    print("=" * 70)
    
    batch_size = 1
    d_model = 4096
    num_q_heads = 32
    num_kv_heads = 8
    max_len = 2048
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # 创建模型
    gqa = GroupedQueryAttention(
        d_model=d_model,
        num_q_heads=num_q_heads,
        num_kv_heads=num_kv_heads,
        kv_cache_max_len=max_len
    ).to(device)
    
    # ===== 阶段1: Prefill - 处理输入prompt =====
    print("\n" + "-" * 70)
    print("阶段1: Prefill (处理prompt)")
    print("-" * 70)
    
    prompt_len = 128
    prompt = torch.randn(batch_size, prompt_len, d_model).to(device)
    
    output, kv_cache = gqa(prompt, kv_cache=None, use_cache=True)
    
    # ===== 阶段2: Decode - 逐token生成 =====
    print("\n" + "-" * 70)
    print("阶段2: Decode (逐token生成)")
    print("-" * 70)
    
    num_new_tokens = 5
    
    for i in range(num_new_tokens):
        print(f"\n--- 生成第{i+1}个token ---")
        
        # 每次只输入1个新token
        new_token = torch.randn(batch_size, 1, d_model).to(device)
        
        # 使用之前的cache
        output, kv_cache = gqa(new_token, kv_cache=kv_cache, use_cache=True)
    
    print("\n" + "=" * 70)
    print("推理完成!")
    print(f"总token数: {prompt_len + num_new_tokens}")
    print(f"Cache使用率: {(prompt_len + num_new_tokens) / max_len * 100:.1f}%")


def visualize_gqa_structure():
    """
    可视化GQA的结构
    """
    print("\n" + "=" * 70)
    print("GQA结构可视化")
    print("=" * 70)
    
    print("""
示例：32个Q头，8个KV头，分成4组

Q头分组 (每组8个Q头):
┌─────────────────────────────────────────────────┐
│ Group 0: Q0  Q1  Q2  Q3  Q4  Q5  Q6  Q7         │ ←→ K0, V0
│ Group 1: Q8  Q9  Q10 Q11 Q12 Q13 Q14 Q15        │ ←→ K1, V1
│ Group 2: Q16 Q17 Q18 Q19 Q20 Q21 Q22 Q23        │ ←→ K2, V2
│ Group 3: Q24 Q25 Q26 Q27 Q28 Q29 Q30 Q31        │ ←→ K3, V3
└─────────────────────────────────────────────────┘

KV Cache存储 (固定长度数组):
┌─────────────────────────────────────────────────┐
│ K0: [已用][已用][已用]......................[空]│
│ K1: [已用][已用][已用]......................[空]│
│ K2: [已用][已用][已用]......................[空]│
│ K3: [已用][已用][已用]......................[空]│
├─────────────────────────────────────────────────┤
│ V0: [已用][已用][已用]......................[空]│
│ V1: [已用][已用][已用]......................[空]│
│ V2: [已用][已用][已用]......................[空]│
│ V3: [已用][已用][已用]......................[空]│
└─────────────────────────────────────────────────┘
      ↑
   cache_position: 当前已使用的位置

更新方式 (索引赋值):
    cache[:, :, position:position+new_len, :] = new_kv
    
优势:
    ✓ 不需要动态申请内存
    ✓ 不需要concat操作
    ✓ 内存地址固定，访问快
    ✓ 支持batch推理时的动态长度
    """)


def analyze_fixed_cache_benefits():
    """
    分析固定长度cache的优势
    """
    print("\n" + "=" * 70)
    print("固定长度 vs 动态增长 KV Cache对比")
    print("=" * 70)
    
    print("""
方案1: 动态增长 (concat方式)
    初始: cache = []
    step1: cache = concat(cache, new_kv)  # 申请新内存，拷贝旧数据
    step2: cache = concat(cache, new_kv)  # 再次申请，再次拷贝
    ...
    
    问题:
    ✗ 每次都要申请新内存
    ✗ 要拷贝历史数据 (O(n)复杂度)
    ✗ 内存碎片化
    ✗ 延迟不稳定
    
方案2: 固定长度 (索引赋值)
    初始: cache = zeros(max_len)  # 预分配
    step1: cache[0:1] = new_kv     # 直接写入，无拷贝
    step2: cache[1:2] = new_kv     # 直接写入，无拷贝
    ...
    
    优势:
    ✓ 内存一次性分配
    ✓ 更新是O(1)操作
    ✓ 无内存碎片
    ✓ 延迟稳定
    ✓ 支持in-place更新

实际性能影响:
    生成1000个token:
    - 动态增长: 1000次内存申请 + 拷贝 → 几百ms额外开销
    - 固定长度: 0次额外申请 → 接近0开销
    
    这就是为什么生产环境都用固定长度cache！
    """)


if __name__ == "__main__":
    # 1. 对比三种注意力机制
    compare_mha_gqa_mqa()
    
    # 2. GQA结构可视化
    visualize_gqa_structure()
    
    # 3. 测试推理流程
    if torch.cuda.is_available():
        test_gqa_inference()
    
    # 4. 分析固定cache的优势
    analyze_fixed_cache_benefits()
    
    print("\n" + "=" * 70)
    print("核心要点总结")
    print("=" * 70)
    print("""
1. GQA的设计动机:
   • MHA内存占用大 (每个Q头独立KV)
   • MQA质量下降 (所有Q头共享1个KV)
   • GQA是最优平衡 (分组共享KV)
   
2. 固定长度KV Cache的实现:
   • 预分配: zeros(batch, kv_heads, max_len, d_k)
   • 更新: cache[:, :, pos:pos+len] = new_kv (索引赋值)
   • 追踪: cache_position记录当前使用长度
   
3. GQA的核心操作:
   • repeat_kv: 将KV头扩展以匹配Q头数量
   • 保持计算的正确性，同时节省内存
   
4. 为什么用固定长度:
   • 避免动态内存申请
   • 避免concat拷贝开销
   • 延迟稳定可预测
   • 这是生产环境的标准做法
   
5. 实际应用:
   • Llama 2: GQA with 8 KV heads
   • Mistral: GQA with 8 KV heads  
   • GPT-4: 推测使用GQA
   • 成为大模型的标准配置
    """)