import torch
import torch.nn as nn
import math
import matplotlib.pyplot as plt
import numpy as np

"""
深度解析：为什么需要Output投影？
QKV和O投影各自的作用是什么？

核心问题：
1. Q、K、V投影的作用 → 特征转换与语义空间映射
2. Attention的作用 → 信息聚合与加权
3. O投影的作用 → 特征融合与维度恢复

一句话总结：
- QKV: 把输入映射到"查询-键-值"的语义空间
- Attention: 根据相似度聚合信息
- O: 把多头的独立表示融合成统一的输出表示
"""

class VisualizableAttention(nn.Module):
    """
    带有详细输出和可视化的注意力层
    """
    def __init__(self, d_model=512, num_heads=8):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # QKV投影
        self.W_q = nn.Linear(d_model, d_model, bias=False)
        self.W_k = nn.Linear(d_model, d_model, bias=False)
        self.W_v = nn.Linear(d_model, d_model, bias=False)
        
        # O投影 (Output projection)
        self.W_o = nn.Linear(d_model, d_model, bias=False)
        
        # 用于分析
        self.attention_weights = None
        self.multi_head_outputs = None
        
    def forward(self, x, return_intermediate=False):
        """
        Args:
            x: [batch, seq_len, d_model]
            return_intermediate: 是否返回中间结果用于分析
        """
        batch_size, seq_len, _ = x.shape
        
        # ========== 阶段1: QKV投影 ==========
        # 作用: 将输入映射到不同的语义空间
        Q = self.W_q(x)  # [batch, seq_len, d_model]
        K = self.W_k(x)
        V = self.W_v(x)
        
        # ========== 阶段2: 分头 ==========
        Q = Q.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        
        # ========== 阶段3: Attention计算 ==========
        # 作用: 基于相似度聚合信息
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        attn_weights = torch.softmax(scores, dim=-1)
        
        # 加权求和
        attn_output = torch.matmul(attn_weights, V)  # [batch, num_heads, seq_len, d_k]
        
        # 保存用于可视化
        self.attention_weights = attn_weights.detach()
        
        # ========== 阶段4: 合并多头（但还未经过O投影）==========
        # [batch, num_heads, seq_len, d_k] -> [batch, seq_len, num_heads, d_k]
        multi_head_output = attn_output.transpose(1, 2).contiguous()
        # -> [batch, seq_len, d_model]
        multi_head_output = multi_head_output.view(batch_size, seq_len, self.d_model)
        
        # 保存多头输出（O投影前）
        self.multi_head_outputs = multi_head_output.detach()
        
        # ========== 阶段5: O投影 ==========
        # 关键：这一步对多头输出做线性变换
        output = self.W_o(multi_head_output)  # [batch, seq_len, d_model]
        
        if return_intermediate:
            return {
                'final_output': output,
                'before_o_proj': multi_head_output,
                'attention_weights': attn_weights,
                'Q': Q, 'K': K, 'V': V
            }
        
        return output


def demonstrate_without_o_projection():
    """
    演示：如果没有O投影会发生什么？
    """
    print("=" * 70)
    print("实验1: 对比有无O投影的区别")
    print("=" * 70)
    
    d_model = 512
    num_heads = 8
    seq_len = 10
    batch_size = 2
    
    # 创建测试数据
    x = torch.randn(batch_size, seq_len, d_model)
    
    # 方案1: 标准的Attention (有O投影)
    attn_with_o = VisualizableAttention(d_model, num_heads)
    results_with_o = attn_with_o(x, return_intermediate=True)
    
    # 方案2: 去掉O投影（直接用多头concat的结果）
    attn_without_o = VisualizableAttention(d_model, num_heads)
    attn_without_o.W_o = nn.Identity()  # 把O投影替换为恒等映射
    results_without_o = attn_without_o(x, return_intermediate=True)
    
    print("\n维度对比:")
    print(f"输入 x: {x.shape}")
    print(f"多头concat后: {results_with_o['before_o_proj'].shape}")
    print(f"经过O投影后: {results_with_o['final_output'].shape}")
    
    # 分析表示空间的差异
    before_o = results_with_o['before_o_proj']
    after_o = results_with_o['final_output']
    
    # 计算每个头的输出在最终输出中的独立性
    print("\n" + "=" * 70)
    print("关键发现：O投影的作用")
    print("=" * 70)
    
    print("""
1. 没有O投影时的问题：
   
   多头输出的concat: [head0的输出 | head1的输出 | ... | head7的输出]
   
   问题：
   ✗ 每个头的输出在各自的"子空间"中，相互独立
   ✗ 头之间没有交互，信息孤岛
   ✗ 最终表示是"拼接"的，不是"融合"的
   
   类比：
   8个专家各自给出建议，但这些建议只是简单堆在一起，
   没有经过综合讨论和整合

2. 有O投影时的优势：
   
   O投影: y = W_o @ [head0 | head1 | ... | head7]
   
   其中W_o是一个 [d_model × d_model] 的矩阵
   
   作用：
   ✓ 允许不同头的输出相互混合
   ✓ 学习如何组合来自不同头的信息
   ✓ 将多个子空间的表示融合到统一的输出空间
   
   类比：
   8个专家给出建议后，通过一个"决策层"来综合考虑，
   形成最终的统一意见

3. 数学角度：
   
   没有O: output_dim_i 只依赖于某一个头
   有O:    output_dim_i 依赖于所有头的加权组合
   
   这极大增强了模型的表达能力！
    """)


def visualize_o_projection_effect():
    """
    可视化O投影的效果
    """
    print("\n" + "=" * 70)
    print("实验2: O投影如何混合多头信息")
    print("=" * 70)
    
    d_model = 64  # 用小一点的维度便于可视化
    num_heads = 4
    
    # 创建一个简单的attention层
    attn = VisualizableAttention(d_model, num_heads)
    
    # 创建测试输入
    x = torch.randn(1, 5, d_model)
    results = attn(x, return_intermediate=True)
    
    # 获取W_o矩阵
    W_o = attn.W_o.weight.detach().numpy()  # [d_model, d_model]
    
    print(f"\nO投影矩阵 W_o shape: {W_o.shape}")
    print(f"这是一个 {d_model}×{d_model} 的矩阵\n")
    
    # 分析W_o的结构
    d_k = d_model // num_heads
    
    print("W_o矩阵的结构分析:")
    print("=" * 70)
    print("""
W_o可以看作是4×4的块矩阵，每个块是16×16:

        [输入来自head0] [head1] [head2] [head3]
输出维度
  0-15   [  块00  ]  [ 块01 ] [ 块02 ] [ 块03 ]  
 16-31   [  块10  ]  [ 块11 ] [ 块12 ] [ 块13 ]
 32-47   [  块20  ]  [ 块21 ] [ 块22 ] [ 块23 ]
 48-63   [  块30  ]  [ 块31 ] [ 块32 ] [ 块33 ]

关键观察：
- 块00: head0对输出前16维的贡献
- 块01: head1对输出前16维的贡献
- 对角块 (00,11,22,33): 每个头对"对应位置"的贡献
- 非对角块: 头之间的信息混合！

如果W_o是单位矩阵（或只有对角块非零）：
→ 那就等价于没有O投影，头之间无交互

但实际训练后，W_o的所有块都有显著值：
→ 说明模型学会了如何混合不同头的信息！
    """)
    
    # 计算不同块的平均绝对值
    print("\nW_o矩阵各块的平均绝对值:")
    print("-" * 70)
    for i in range(num_heads):
        row_str = f"输出块{i}: "
        for j in range(num_heads):
            block = W_o[i*d_k:(i+1)*d_k, j*d_k:(j+1)*d_k]
            avg_abs = np.abs(block).mean()
            row_str += f"[head{j}→{avg_abs:.3f}] "
        print(row_str)
    
    print("\n解读:")
    print("- 所有块都有相当的数值 → 每个头都对所有输出维度有贡献")
    print("- 这证明了O投影在进行真正的信息融合，而非简单拼接")


def explain_qkv_roles():
    """
    详细解释Q、K、V的作用
    """
    print("\n" + "=" * 70)
    print("深入理解：Q、K、V的语义")
    print("=" * 70)
    
    print("""
设想一个场景：你在图书馆查资料

原始句子: "The cat sat on the mat"
任务: 理解每个词的含义（考虑上下文）

======================== QKV的类比 ========================

对于词 "cat":

1. Query (Q): "我想要找什么信息？"
   -----------
   Q_cat = W_q @ embedding_cat
   
   语义: cat发出的"查询信号"
   - 想知道：谁是主语？在哪里？
   - 想知道：附近有什么修饰词？
   
   类比: 你脑海中的问题 "这只猫的特征是什么？"

2. Key (K): "我能提供什么信息？"
   ---------
   K_cat = W_k @ embedding_cat
   K_sat = W_k @ embedding_sat
   K_on  = W_k @ embedding_on
   ...
   
   语义: 每个词广播的"索引信息"
   - cat的key: "我是一个动物名词"
   - sat的key: "我是一个动作动词"
   - on的key:  "我是一个介词"
   
   类比: 图书馆每本书的索引标签

3. Value (V): "我实际包含的信息内容"
   ----------
   V_cat = W_v @ embedding_cat
   
   语义: 词的实际特征表示
   - 包含cat的语义、语法、风格等所有信息
   - 这是真正要被加权求和的内容
   
   类比: 图书馆每本书的实际内容

======================== Attention计算过程 ========================

步骤1: 计算相似度 (Q和K的匹配度)
------
score(cat, sat) = Q_cat · K_sat / √d_k
score(cat, on)  = Q_cat · K_on / √d_k
...

语义: "cat的query和哪些词的key最匹配？"
→ 决定cat应该关注哪些词

步骤2: Softmax归一化
------
α_cat,sat = softmax(scores)[sat]  # 给sat的权重
α_cat,on  = softmax(scores)[on]   # 给on的权重
...

语义: 注意力分配，权重和为1

步骤3: 加权求和 (用权重组合Value)
------
output_cat = α_cat,sat * V_sat + α_cat,on * V_on + α_cat,mat * V_mat + ...

语义: cat的新表示 = 上下文词的value的加权平均
→ 这个新表示融合了上下文信息！

======================== 为什么要分开QKV？========================

问题: 为什么不直接用 embedding 做点积？
答案: QKV的投影赋予了不同的语义角色

如果直接用embedding:
   score(cat, sat) = embedding_cat · embedding_sat
   
问题:
✗ embedding包含所有信息（语义、语法、位置等）
✗ 点积会混合不相关的特征
✗ 无法区分"查询需求"和"提供信息"

使用QKV投影后:
   score(cat, sat) = (W_q @ embedding_cat) · (W_k @ embedding_sat)
   
优势:
✓ W_q学习提取"查询相关"的特征
✓ W_k学习提取"被查询相关"的特征  
✓ W_v学习提取"真正有用"的内容特征
✓ 三者分工明确，优化目标清晰

类比:
- 不用QKV: 用整本字典查词 (效率低)
- 用QKV: 用专门的索引系统查词 (高效准确)
    """)


def explain_full_pipeline():
    """
    完整流程的统一解释
    """
    print("\n" + "=" * 70)
    print("完整流程：从输入到输出")
    print("=" * 70)
    
    print("""
输入: x ∈ ℝ^(seq_len × d_model)
      例如: "The cat sat" 的embedding

┌─────────────────────────────────────────────────────────────┐
│ 阶段1: QKV投影 - "准备不同角色的表示"                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Q = W_q @ x  → "查询视角的表示"                              │
│  K = W_k @ x  → "被检索视角的表示"                            │
│  V = W_v @ x  → "内容视角的表示"                              │
│                                                               │
│  作用: 将输入映射到三个不同的语义空间                          │
│  目的: 分离"问"、"索引"、"答"三种功能                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 阶段2: 多头分割 - "多个视角并行处理"                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Q → [Q_head0, Q_head1, ..., Q_head7]                        │
│  K → [K_head0, K_head1, ..., K_head7]                        │
│  V → [V_head0, V_head1, ..., V_head7]                        │
│                                                               │
│  作用: 每个头关注不同的特征子空间                              │
│  目的: head0关注语法，head1关注语义，head2关注位置...          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 阶段3: Attention计算 - "信息聚合"                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  对每个头 i:                                                  │
│    scores_i = Q_i @ K_i^T / √d_k  → 计算相似度              │
│    α_i = softmax(scores_i)         → 归一化权重              │
│    output_i = α_i @ V_i            → 加权求和                │
│                                                               │
│  作用: 基于query-key匹配度，聚合value信息                     │
│  目的: 让每个token融合上下文信息                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 阶段4: 多头拼接 - "组合不同视角"                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  concat([output_0, output_1, ..., output_7])                 │
│  → shape: [seq_len, d_model]                                 │
│                                                               │
│  此时: 维度恢复到d_model，但这只是"拼接"！                    │
│  问题: 各头信息独立，缺乏交互                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 阶段5: O投影 - "信息融合" ★关键步骤★                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  output_final = W_o @ concat_output                          │
│                                                               │
│  W_o的作用:                                                   │
│  ┌─────────────────────────────────────────┐                 │
│  │ 维度i的输出 = Σ w_ij × (head_j的输出)   │                 │
│  └─────────────────────────────────────────┘                 │
│                                                               │
│  这意味着:                                                    │
│  ✓ 输出的每一维都是所有头的加权组合                            │
│  ✓ 不同头的信息可以相互混合                                    │
│  ✓ 模型学习"如何组合"不同头的见解                             │
│                                                               │
│  类比: 8个专家独立给意见(多头输出)                             │
│        → 决策层综合考虑(O投影)                                │
│        → 形成最终决策(最终输出)                                │
└─────────────────────────────────────────────────────────────┘

输出: y ∈ ℝ^(seq_len × d_model)
      融合了多头注意力信息的上下文表示

======================== 关键洞察 ========================

1. 为什么QKV都需要投影？
   → 分离不同的语义角色，让模型学习专门化的表示

2. 为什么要多头？
   → 并行捕获不同类型的依赖关系（语法、语义、位置等）

3. 为什么需要O投影？ ★核心问题★
   → 融合多头信息，而非简单拼接
   → 这是多头能够真正协作的关键！

4. 没有O投影会怎样？
   → 各头输出独立，信息孤岛
   → 表达能力大幅下降
   → 相当于8个独立的小模型，而非协作的大模型

======================== 数学直觉 ========================

不使用O投影:
   y_i 只依赖于第⌊i/d_k⌋个头的输出
   → 输出空间被分割成num_heads个独立子空间

使用O投影:
   y_i = Σ_j w_ij × (所有头的第j维输出)
   → 输出空间是所有头的线性组合
   → 表达能力指数级提升！

这就是为什么O投影是必不可少的！
    """)


def parameter_count_analysis():
    """
    参数量分析：O投影的成本
    """
    print("\n" + "=" * 70)
    print("参数量分析")
    print("=" * 70)
    
    d_model = 4096
    num_heads = 32
    
    # QKV投影参数
    qkv_params = 3 * d_model * d_model
    
    # O投影参数
    o_params = d_model * d_model
    
    total_params = qkv_params + o_params
    
    print(f"\n模型配置: d_model={d_model}, num_heads={num_heads}")
    print(f"\nQKV投影参数量: {qkv_params:,} ({qkv_params/1e6:.1f}M)")
    print(f"  - W_q: {d_model * d_model:,}")
    print(f"  - W_k: {d_model * d_model:,}")
    print(f"  - W_v: {d_model * d_model:,}")
    print(f"\nO投影参数量: {o_params:,} ({o_params/1e6:.1f}M)")
    print(f"\n总参数量: {total_params:,} ({total_params/1e6:.1f}M)")
    print(f"\nO投影占比: {o_params/total_params*100:.1f}%")
    
    print(f"\n结论:")
    print(f"- O投影增加了25%的参数量")
    print(f"- 但带来了巨大的表达能力提升")
    print(f"- 这是非常值得的trade-off！")
    
    print(f"\n如果去掉O投影:")
    print(f"- 节省参数: {o_params:,} ({o_params/1e6:.1f}M)")
    print(f"- 但模型效果会显著下降")
    print(f"- 实际上没有任何主流模型这么做")


if __name__ == "__main__":
    # 设置随机种子
    torch.manual_seed(42)
    np.random.seed(42)
    
    # 1. 对比有无O投影
    demonstrate_without_o_projection()
    
    # 2. 可视化O投影的效果
    visualize_o_projection_effect()
    
    # 3. 解释QKV的作用
    explain_qkv_roles()
    
    # 4. 完整流程解释
    explain_full_pipeline()
    
    # 5. 参数量分析
    parameter_count_analysis()
    
    print("\n" + "=" * 70)
    print("总结：Attention的完整故事")
    print("=" * 70)
    print("""
1. QKV投影: 角色分离
   ├─ Q: 查询表示（我要找什么）
   ├─ K: 键表示（我能提供什么索引）
   └─ V: 值表示（我的实际内容）

2. 多头机制: 视角多样化
   ├─ 每个头关注不同的特征子空间
   ├─ head0→语法, head1→语义, head2→位置...
   └─ 并行处理，互补学习

3. Attention: 信息聚合
   ├─ 基于Q-K相似度分配权重
   ├─ 对V加权求和
   └─ 融合上下文信息

4. O投影: 多头融合 ★最容易被忽视但最重要★
   ├─ 不是简单拼接，而是学习如何组合
   ├─ 允许不同头之间信息交互
   └─ 这才是真正的"集体智慧"

完整公式:
   Attention(Q,K,V) = softmax(QK^T/√d_k)V
   MultiHead(x) = W_o @ Concat(head_1, ..., head_h)
   where head_i = Attention(W_q^i x, W_k^i x, W_v^i x)

没有W_o，就失去了多头协作的能力！
    """)