import torch
import time
import numpy as np

"""
深度解析：为什么 transpose(1,2) 能实现并行计算

核心原理：
1. 矩阵乘法的批量计算（Batch Matrix Multiplication）
2. GPU的SIMD架构和内存访问模式
3. PyTorch的底层优化（cuBLAS库）
"""

def demonstrate_parallel_computation():
    """
    演示为什么transpose后能并行计算
    """
    print("=" * 70)
    print("场景对比：为什么要transpose？")
    print("=" * 70)
    
    batch_size = 2
    num_heads = 8
    seq_len = 100
    d_k = 64
    
    # 创建测试数据
    Q = torch.randn(batch_size, seq_len, num_heads, d_k).cuda()
    K = torch.randn(batch_size, seq_len, num_heads, d_k).cuda()
    
    print(f"\n原始形状:")
    print(f"Q: {Q.shape}  # [batch, seq_len, num_heads, d_k]")
    
    # ========== 方案1：不transpose，需要循环 ==========
    print("\n" + "=" * 70)
    print("方案1：不transpose - 必须用循环（串行）")
    print("=" * 70)
    
    def method_without_transpose(Q, K):
        """不使用transpose，必须循环处理每个头"""
        batch_size, seq_len, num_heads, d_k = Q.shape
        
        # 无法直接做矩阵乘法，必须遍历每个头
        scores_list = []
        for h in range(num_heads):
            # 取出第h个头
            Q_h = Q[:, :, h, :]  # [batch, seq_len, d_k]
            K_h = K[:, :, h, :]  # [batch, seq_len, d_k]
            
            # 对单个头做注意力计算
            scores_h = torch.matmul(Q_h, K_h.transpose(-2, -1))  # [batch, seq_len, seq_len]
            scores_list.append(scores_h)
        
        # 堆叠所有头的结果
        scores = torch.stack(scores_list, dim=2)  # [batch, seq_len, num_heads, seq_len]
        return scores
    
    start = time.time()
    scores1 = method_without_transpose(Q, K)
    time1 = time.time() - start
    
    print(f"输出形状: {scores1.shape}")
    print(f"执行方式: 循环8次，每次处理1个头")
    print(f"计算时间: {time1*1000:.3f} ms")
    print(f"问题: GPU无法并行，只能串行执行8次")
    
    # ========== 方案2：使用transpose，一次性并行 ==========
    print("\n" + "=" * 70)
    print("方案2：transpose后 - 批量矩阵乘法（并行）")
    print("=" * 70)
    
    def method_with_transpose(Q, K):
        """使用transpose，利用批量矩阵乘法"""
        batch_size, seq_len, num_heads, d_k = Q.shape
        
        # transpose将num_heads提到前面
        Q_t = Q.transpose(1, 2)  # [batch, num_heads, seq_len, d_k]
        K_t = K.transpose(1, 2)  # [batch, num_heads, seq_len, d_k]
        
        print(f"transpose后 Q: {Q_t.shape}")
        
        # 关键：torch.matmul自动识别批量维度
        # 它会并行计算 batch * num_heads 个独立的矩阵乘法
        scores = torch.matmul(Q_t, K_t.transpose(-2, -1))
        # [batch, num_heads, seq_len, seq_len]
        
        return scores
    
    # 预热GPU
    _ = method_with_transpose(Q, K)
    torch.cuda.synchronize()
    
    start = time.time()
    scores2 = method_with_transpose(Q, K)
    torch.cuda.synchronize()
    time2 = time.time() - start
    
    print(f"输出形状: {scores2.shape}")
    print(f"执行方式: 1次调用，GPU并行处理所有头")
    print(f"计算时间: {time2*1000:.3f} ms")
    print(f"加速比: {time1/time2:.2f}x")
    
    # 验证结果一致性
    # scores1: [batch, seq_len, num_heads, seq_len]
    # scores2: [batch, num_heads, seq_len, seq_len]
    # 需要将scores1转换为和scores2相同的形状
    print(f"\nscores1原始形状: {scores1.shape}")
    print(f"scores2形状: {scores2.shape}")
    
    # 正确的转换：先交换维度1和2（seq_len <-> num_heads）
    scores1_reorder = scores1.transpose(1, 2)  # [batch, num_heads, seq_len, seq_len]
    print(f"scores1转换后形状: {scores1_reorder.shape}")
    
    print(f"\n结果是否一致: {torch.allclose(scores1_reorder, scores2, atol=1e-5)}")


def explain_batch_matmul():
    """
    详细解释批量矩阵乘法的工作原理
    """
    print("\n" + "=" * 70)
    print("核心原理：批量矩阵乘法 (Batch Matrix Multiplication)")
    print("=" * 70)
    
    print("""
torch.matmul 的智能识别规则：
    
当输入维度 >= 3 时，前面的维度被视为"批量维度"，最后两个维度做矩阵乘法

示例：
    A: [batch, num_heads, seq_len, d_k]
    B: [batch, num_heads, d_k, seq_len]
    
    torch.matmul(A, B) 会：
    1. 识别 [batch, num_heads] 为批量维度
    2. 对每个 (batch_i, head_j) 执行独立的矩阵乘法
    3. 总共执行 batch × num_heads 次矩阵乘法
    4. GPU并行处理这些独立计算
    
    输出: [batch, num_heads, seq_len, seq_len]
    """)
    
    # 具体示例
    batch, heads, seq, d_k = 2, 4, 10, 8
    
    A = torch.randn(batch, heads, seq, d_k)
    B = torch.randn(batch, heads, d_k, seq)
    
    print(f"\n示例：")
    print(f"A shape: {A.shape}  # [batch=2, heads=4, seq=10, d_k=8]")
    print(f"B shape: {B.shape}  # [batch=2, heads=4, d_k=8, seq=10]")
    
    C = torch.matmul(A, B)
    print(f"C shape: {C.shape}  # [batch=2, heads=4, seq=10, seq=10]")
    print(f"\nGPU实际执行：2×4=8个独立的 [10×8] @ [8×10] 矩阵乘法")
    print(f"这8个计算在不同的GPU核心上同时进行！")


def explain_memory_layout():
    """
    解释内存布局对并行计算的影响
    """
    print("\n" + "=" * 70)
    print("内存布局与并行计算的关系")
    print("=" * 70)
    
    print("""
1. GPU内存访问模式（Coalesced Memory Access）：
   
   形状: [batch, num_heads, seq_len, d_k]
   
   内存布局（行优先）：
   [b0,h0,s0,: ] [b0,h0,s1,: ] ... [b0,h1,s0,: ] ... [b1,h0,s0,: ] ...
   
   当num_heads在前面时：
   - 同一个head的所有seq_len数据在内存中连续
   - GPU的warp（32个线程）可以高效地连续读取
   - 减少内存事务次数，提高带宽利用率

2. GPU的SIMD架构（Single Instruction Multiple Data）：
   
   现代GPU有数千个核心，可以同时执行相同的操作
   
   [batch, num_heads, seq_len, d_k] 形状：
   ├─ batch × num_heads 个独立的矩阵乘法任务
   ├─ 每个任务分配给不同的GPU核心
   └─ 所有核心同时执行 matmul 指令
   
   这就是"并行"的本质！

3. cuBLAS库的优化：
   
   PyTorch底层调用NVIDIA的cuBLAS库
   cuBLAS专门针对批量矩阵乘法优化：
   - 识别连续的批量维度
   - 使用Tensor Core（在Volta及以上GPU）
   - 自动选择最优的分块策略
    """)


def demonstrate_actual_speedup():
    """
    实际测速：对比不同方案的性能
    """
    print("\n" + "=" * 70)
    print("实际性能对比（大规模场景）")
    print("=" * 70)
    
    batch_size = 16
    num_heads = 32
    seq_len = 512
    d_k = 128
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"使用设备: {device}")
    
    if device == 'cuda':
        Q = torch.randn(batch_size, num_heads, seq_len, d_k).cuda()
        K = torch.randn(batch_size, num_heads, seq_len, d_k).cuda()
        
        # 预热
        for _ in range(10):
            _ = torch.matmul(Q, K.transpose(-2, -1))
        torch.cuda.synchronize()
        
        # 测速
        num_runs = 100
        start = time.time()
        for _ in range(num_runs):
            scores = torch.matmul(Q, K.transpose(-2, -1))
        torch.cuda.synchronize()
        elapsed = time.time() - start
        
        print(f"\n配置:")
        print(f"  Batch size: {batch_size}")
        print(f"  Num heads: {num_heads}")
        print(f"  Seq length: {seq_len}")
        print(f"  d_k: {d_k}")
        print(f"\n总计算量: {batch_size * num_heads} 个矩阵乘法")
        print(f"单次耗时: {elapsed/num_runs*1000:.3f} ms")
        print(f"吞吐量: {batch_size*num_heads*num_runs/elapsed:.0f} 个矩阵乘法/秒")
        
        # 计算理论FLOPS
        flops_per_matmul = 2 * seq_len * seq_len * d_k  # 2 for multiply-add
        total_flops = batch_size * num_heads * flops_per_matmul * num_runs
        tflops = total_flops / elapsed / 1e12
        
        print(f"实际算力: {tflops:.2f} TFLOPS")


def visualize_concept():
    """
    可视化概念：为什么transpose能并行
    """
    print("\n" + "=" * 70)
    print("可视化理解")
    print("=" * 70)
    
    print("""
不使用transpose: [batch, seq_len, num_heads, d_k]
    
    batch 0                      batch 1
    ┌─────────────────┐         ┌─────────────────┐
    │ seq 0           │         │ seq 0           │
    │  [h0][h1][h2]...│         │  [h0][h1][h2]...│
    │ seq 1           │         │ seq 1           │
    │  [h0][h1][h2]...│         │  [h0][h1][h2]...│
    │ ...             │         │ ...             │
    └─────────────────┘         └─────────────────┘
    
    问题：要计算h0的注意力，需要从每个seq位置提取h0
         → 内存不连续，需要跳跃访问
         → 无法批量处理


使用transpose后: [batch, num_heads, seq_len, d_k]
    
    batch 0                      batch 1
    ┌─────────────────┐         ┌─────────────────┐
    │ head 0          │         │ head 0          │
    │  [seq0][seq1]...│         │  [seq0][seq1]...│
    │ head 1          │         │ head 1          │
    │  [seq0][seq1]...│         │  [seq0][seq1]...│
    │ ...             │         │ ...             │
    └─────────────────┘         └─────────────────┘
    
    优势：每个head的数据连续存储
         → GPU可以一次读取完整的head数据
         → batch × num_heads 个独立任务并行执行
         → 充分利用GPU的并行能力

    
GPU并行执行示意：
    
    GPU核心 0:  batch0_head0 的 matmul  ┐
    GPU核心 1:  batch0_head1 的 matmul  │
    GPU核心 2:  batch0_head2 的 matmul  ├─ 同时执行！
    GPU核心 3:  batch0_head3 的 matmul  │
    ...                                 │
    GPU核心 31: batch1_head15 的 matmul ┘
    """)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Transpose与并行计算：完整解析")
    print("=" * 70)
    
    # 1. 基础演示
    if torch.cuda.is_available():
        demonstrate_parallel_computation()
    else:
        print("\n[注意] 需要GPU才能看到明显的并行加速效果")
    
    # 2. 原理解释
    explain_batch_matmul()
    explain_memory_layout()
    
    # 3. 性能测试
    if torch.cuda.is_available():
        demonstrate_actual_speedup()
    
    # 4. 可视化
    visualize_concept()
    
    # 总结
    print("\n" + "=" * 70)
    print("核心要点总结")
    print("=" * 70)
    print("""
1. 数学层面：
   ✓ torch.matmul识别批量维度，自动并行化
   ✓ [batch, num_heads, ...] 被视为 batch×num_heads 个独立任务
   
2. 硬件层面：
   ✓ GPU有数千个并行核心
   ✓ 每个核心处理一个独立的矩阵乘法
   ✓ 内存连续访问提高带宽利用率
   
3. 软件层面：
   ✓ cuBLAS库针对批量矩阵乘法深度优化
   ✓ Tensor Core加速（A100/H100等新GPU）
   ✓ 自动选择最优计算策略
   
4. 实际效果：
   ✓ 相比循环：5-10倍加速（小规模）
   ✓ 大规模场景：可达数十倍加速
   ✓ 吞吐量：数十TFLOPS（高端GPU）

结论：transpose不是为了"方便"，而是为了"性能"！
      它让GPU能够充分发挥并行计算能力。
    """)