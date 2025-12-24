import torch
import torch.nn as nn
import math

class MultiHeadAttention(nn.Module):
    """
    多头注意力机制的完整实现，包含详细的维度变化注释
    
    关键概念：
    - d_model: 模型维度 (如512)
    - num_heads: 注意力头数 (如8)
    - d_k = d_model // num_heads: 每个头的维度 (如64)
    """
    def __init__(self, d_model=512, num_heads=8, dropout=0.1):
        super().__init__()
        assert d_model % num_heads == 0, "d_model必须能被num_heads整除"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads  # 每个头的维度
        
        # QKV投影层：将输入映射到Q、K、V
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        
        # 输出投影层
        self.W_o = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, query, key, value, mask=None, use_cache=False, past_kv=None):
        """
        Args:
            query: [batch_size, seq_len_q, d_model]
            key: [batch_size, seq_len_k, d_model]
            value: [batch_size, seq_len_v, d_model]
            mask: [batch_size, 1, seq_len_q, seq_len_k] 或 None
            use_cache: 是否使用KV缓存（推理时）
            past_kv: 历史KV缓存 (past_key, past_value)
            
        Returns:
            output: [batch_size, seq_len_q, d_model]
            new_kv: 新的KV缓存 (用于下一步)
        """
        batch_size = query.size(0)
        seq_len_q = query.size(1)
        
        # ========== 步骤1: 线性投影 QKV ==========
        # Q: [batch, seq_len_q, d_model] -> [batch, seq_len_q, d_model]
        # K: [batch, seq_len_k, d_model] -> [batch, seq_len_k, d_model]
        # V: [batch, seq_len_v, d_model] -> [batch, seq_len_v, d_model]
        Q = self.W_q(query)
        K = self.W_k(key)
        V = self.W_v(value)
        
        print(f"投影后 Q shape: {Q.shape}")  # [batch, seq_len_q, d_model]
        print(f"投影后 K shape: {K.shape}")  # [batch, seq_len_k, d_model]
        
        # ========== 步骤2: 分割多头 ==========
        # 关键操作：reshape + transpose
        # [batch, seq_len, d_model] -> [batch, seq_len, num_heads, d_k]
        Q = Q.view(batch_size, seq_len_q, self.num_heads, self.d_k)
        K = K.view(batch_size, -1, self.num_heads, self.d_k)
        V = V.view(batch_size, -1, self.num_heads, self.d_k)
        
        print(f"view后 Q shape: {Q.shape}")  # [batch, seq_len_q, num_heads, d_k]
        
        # transpose将num_heads维度提前，便于并行计算
        # [batch, seq_len, num_heads, d_k] -> [batch, num_heads, seq_len, d_k]
        Q = Q.transpose(1, 2)
        K = K.transpose(1, 2)
        V = V.transpose(1, 2)
        
        print(f"transpose后 Q shape: {Q.shape}")  # [batch, num_heads, seq_len_q, d_k]
        print(f"transpose后 K shape: {K.shape}")  # [batch, num_heads, seq_len_k, d_k]
        
        # ========== 步骤3: KV Cache处理（推理优化）==========
        if use_cache and past_kv is not None:
            # 推理时，只计算新token的K和V
            # past_kv包含之前所有token的K和V
            past_key, past_value = past_kv
            
            print(f"past_key shape: {past_key.shape}")
            print(f"当前K shape: {K.shape}")
            
            # 沿序列维度拼接：将新的K、V追加到历史缓存后面
            # [batch, num_heads, past_seq_len, d_k] + [batch, num_heads, 1, d_k]
            # -> [batch, num_heads, past_seq_len+1, d_k]
            K = torch.cat([past_key, K], dim=2)
            V = torch.cat([past_value, V], dim=2)
            
            print(f"拼接后K shape: {K.shape}")
        
        # 保存当前的KV用于下一次推理
        new_kv = (K, V) if use_cache else None
        
        # ========== 步骤4: 计算注意力分数 ==========
        # Q @ K^T: [batch, num_heads, seq_len_q, d_k] @ [batch, num_heads, d_k, seq_len_k]
        # -> [batch, num_heads, seq_len_q, seq_len_k]
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        print(f"注意力分数 scores shape: {scores.shape}")
        
        # ========== 步骤5: 应用mask（可选）==========
        if mask is not None:
            # mask中为True的位置会被设置为-inf，softmax后变为0
            scores = scores.masked_fill(mask == 0, -1e9)
        
        # ========== 步骤6: Softmax归一化 ==========
        # 对最后一个维度（seq_len_k）做softmax
        attn_weights = torch.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        
        print(f"注意力权重 attn_weights shape: {attn_weights.shape}")
        
        # ========== 步骤7: 加权求和 ==========
        # [batch, num_heads, seq_len_q, seq_len_k] @ [batch, num_heads, seq_len_k, d_k]
        # -> [batch, num_heads, seq_len_q, d_k]
        output = torch.matmul(attn_weights, V)
        
        print(f"加权求和后 output shape: {output.shape}")
        
        # ========== 步骤8: 合并多头 ==========
        # transpose回来: [batch, num_heads, seq_len_q, d_k] 
        # -> [batch, seq_len_q, num_heads, d_k]
        output = output.transpose(1, 2).contiguous()
        
        print(f"transpose回来 output shape: {output.shape}")
        
        # reshape合并: [batch, seq_len_q, num_heads, d_k] 
        # -> [batch, seq_len_q, d_model]
        output = output.view(batch_size, seq_len_q, self.d_model)
        
        print(f"合并多头后 output shape: {output.shape}")
        
        # ========== 步骤9: 输出投影 ==========
        output = self.W_o(output)
        
        print(f"最终输出 shape: {output.shape}\n")
        
        return output, new_kv


# ==================== 测试代码 ====================
def test_attention():
    print("=" * 60)
    print("测试1: 自注意力（训练场景）")
    print("=" * 60)
    
    batch_size = 2
    seq_len = 10
    d_model = 512
    num_heads = 8
    
    # 创建模型
    attn = MultiHeadAttention(d_model=d_model, num_heads=num_heads)
    
    # 创建输入
    x = torch.randn(batch_size, seq_len, d_model)
    
    # 自注意力：Q=K=V
    output, _ = attn(x, x, x)
    
    print("\n" + "=" * 60)
    print("测试2: KV Cache推理场景")
    print("=" * 60)
    
    # 第一步：处理完整序列（prefill阶段）
    print("\n--- Prefill阶段：处理完整prompt ---")
    prompt_len = 5
    prompt = torch.randn(batch_size, prompt_len, d_model)
    
    output1, kv_cache = attn(prompt, prompt, prompt, use_cache=True)
    
    # 第二步：生成新token（decode阶段）
    print("\n--- Decode阶段：生成第1个新token ---")
    new_token = torch.randn(batch_size, 1, d_model)
    
    # 使用缓存，只需要计算新token的Q，而K和V会复用
    output2, kv_cache = attn(new_token, new_token, new_token, 
                             use_cache=True, past_kv=kv_cache)
    
    # 第三步：继续生成
    print("\n--- Decode阶段：生成第2个新token ---")
    new_token2 = torch.randn(batch_size, 1, d_model)
    output3, kv_cache = attn(new_token2, new_token2, new_token2,
                             use_cache=True, past_kv=kv_cache)
    
    print("\n" + "=" * 60)
    print("测试3: 交叉注意力（Encoder-Decoder）")
    print("=" * 60)
    
    # Decoder的query和Encoder的key-value
    decoder_input = torch.randn(batch_size, 3, d_model)  # decoder序列
    encoder_output = torch.randn(batch_size, 10, d_model)  # encoder输出
    
    # 交叉注意力：Q来自decoder，K和V来自encoder
    output4, _ = attn(decoder_input, encoder_output, encoder_output)


def analyze_kv_cache_efficiency():
    """分析KV Cache的效率提升"""
    print("\n" + "=" * 60)
    print("KV Cache效率分析")
    print("=" * 60)
    
    seq_len = 1000
    d_model = 4096
    num_heads = 32
    
    # 不使用cache：每次都要计算所有token的K和V
    # 计算量：O(seq_len * d_model^2)
    
    # 使用cache：只计算新token的K和V，历史的直接复用
    # 计算量：O(1 * d_model^2)
    
    print(f"\n生成100个新token的计算对比：")
    print(f"不使用KV Cache: 需要 {100 * seq_len} 次 K/V 投影")
    print(f"使用KV Cache: 只需要 {100} 次 K/V 投影")
    print(f"速度提升: {100 * seq_len / 100:.1f}x")
    
    # 内存占用分析
    kv_cache_size = 2 * num_heads * seq_len * (d_model // num_heads) * 2  # 2字节(fp16)
    print(f"\nKV Cache内存占用（单个样本）:")
    print(f"  {kv_cache_size / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    # 运行测试
    test_attention()
    analyze_kv_cache_efficiency()
    
    print("\n" + "=" * 60)
    print("关键要点总结")
    print("=" * 60)
    print("""
    1. 多头注意力的transpose操作：
       - view: 将d_model分割为num_heads个d_k维度
       - transpose(1,2): 将num_heads维度提到seq_len前面
       - 目的：让每个头独立并行计算
    
    2. KV Cache存储方式：
       - 存储格式: (K, V), 每个形状为 [batch, num_heads, seq_len, d_k]
       - 更新方式: 沿着seq_len维度concat新的K、V
       - 优势: 避免重复计算历史token的K和V
    
    3. 推理优化效果：
       - 训练时: 使用并行计算，不需要cache
       - 推理时: 使用KV cache，速度提升seq_len倍
       - 典型场景: 长文本生成时节省大量计算
    
    4. 注意力机制的三种模式：
       - 自注意力: Q=K=V (Encoder、Decoder)
       - 交叉注意力: Q≠K=V (Decoder attending to Encoder)
       - 因果注意力: 自注意力+下三角mask (GPT等)
    """)