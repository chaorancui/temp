[toc]

# 主流 AI 算子

1. Matmul : matrix multiply 的缩写，是专门用于矩阵乘法的函数。
2. Conv2d : 二维卷积运算，常用于二维图像。相对应的还有一维卷积方法 Conv1d，常用于文本数据的处理。
3. Relu : 整流线性单位函数（Rectified Linear Unit, ReLU），又称修正线性单元，是一种人工神经网络中常用的激活函数，通常指代以斜坡函数及其变种为代表的非线性函数。
   线性整流被认为有一定的生物学原理，并且由于在实践中通常有着比其他常用激活函数（如 sigmiod/tanh）更好的效果。

4. Softmax : 一种激活函数，它可以将一个数值向量归一化为一个概率分布向量，且各个概率之和为 1。Softmax 可以用来作为神经网络的最后一层，用于多分类问题的输出。
5. Pooling : 卷积神经网络中常见的一种操作，Pooling 层是模仿人的视觉系统对数据进行降维，其本质是降维。减小网络的模型参数量和计算成本，也在一定程度上降低过拟合的风险
6. Img2Col : 是一种实现卷积操作的加速计算策略。它能将卷积操作转化为 GEMM（通用矩阵乘 General Matrix Multiply)，从而最大化地缩短卷积计算的时间。

## MM 和 GEMM

MM 和 GEMM 都是大模型中常用的矩阵运算，但它们在数学上有一些重要的区别:

1. **MM (Matrix Multiplication)**:
   <!-- prettier-ignore -->
   MM 指的是标准的矩阵乘法。对于两个矩阵 $ A_{m \times p} $ 和 $ B_{p \times n} $，它们的乘积 $ C_{m \times n} = AB $ 是一个 $ m \times n $ 的矩阵。
   数学表达式:
   $$ C_{(i, j)} = \Sigma_{k=1}^n A_{(i, k)} \times B_{(k, j)} $$

2. **GEMM (General Matrix Multiplication)**:

   GEMM 是一种更通用的矩阵运算,全称为"General Matrix Multiply"。它的形式是:

   $$ C = \alpha AB + \beta C $$

   其中 $ \alpha, \beta $ 是标量，$ A, B, C $ 是矩阵。

3. **主要区别**:

   1. 操作复杂度:
      - MM 只进行矩阵乘法
      - GEMM 除了矩阵乘法外，还包含缩放($ \alpha $)和累加($ \beta $)操作
   2. 灵活性:
      - MM 是 GEMM 的一个特例(当 $ \alpha = 1, \beta = 0 $ 时)
      - GEMM 允许更灵活的矩阵运算组合
   3. 性能优化:
      - GEMM 通常有更优化的实现，因为它可以一次性完成多个操作,减少内存访问
   4. 应用场景:
      - MM 在简单的矩阵乘法中使用
      - GEMM 在需要频繁进行矩阵乘加操作的场景中更有优势，如深度学习中的全连接层或卷积层
   5. 数值稳定性:
      - GEMM 由于其缩放和累加操作，在某些情况下可能提供更好的数值稳定性

   在大模型中，GEMM 通常更受欢迎，因为它能提供更高的计算效率和更大的灵活性。但具体使用哪种方法还要根据实际需求和硬件支持情况来决定。

4. **SGEMM 和 DGEMM**：
   GEMM 分成双精度（DGEMM）和单精度（SGEMM）两个版本，这两个版本的参数是一致的，只不过在一些参数类型上是 double 和 float 的区别。

   1. **SGEMM (Single precision General Matrix Multiply)**:

      SGEMM 是用于单精度浮点数(32 位浮点数，也称为 float)的 GEMM 操作。特点:

      - 使用 32 位浮点数进行计算
      - occupies less memory
      - 计算速度通常比 DGEMM 快
      - 精度相对较低，适用于对精度要求不是特别高的场景

   2. **DGEMM (Double precision General Matrix Multiply)**:

      DGEMM 是用于双精度浮点数(64 位浮点数，也称为 double)的 GEMM 操作。特点:

      - 使用 64 位浮点数进行计算
      - 占用更多内存
      - 计算速度通常比 SGEMM 慢
      - 精度更高,适用于需要高精度计算的场景

   3. **主要区别**:

      1. 精度:
         - SGEMM: 约 7 位十进制精度
         - DGEMM: 约 15-17 位十进制精度
      2. 内存使用:
         - SGEMM 使用的内存大约是 DGEMM 的一半
      3. 计算速度:
         - 在相同硬件上，SGEMM 通常比 DGEMM 快 1.5-2 倍
      4. 适用场景:
         - SGEMM: 深度学习训练和推理、图形处理等对速度要求高但对精度要求相对较低的场景
         - DGEMM: 科学计算、金融模型等需要高精度的场景
      5. 硬件支持:
         - 现代 GPU 通常对 SGEMM 有更好的优化
         - 一些专门的 AI 加速器可能只支持或主要优化 SGEMM

   4. **在大模型中的应用**:

      1. 训练阶段:
         - 通常使用 SGEMM，因为它能提供足够的精度，同时具有更快的速度和更低的内存占用
      2. 推理阶段:
         - 大多数情况下使用 SGEMM
         - 在一些需要高精度的特殊应用中可能使用 DGEMM
      3. 混合精度训练:
         - 有时会结合使用 SGEMM 和 DGEMM，以平衡精度和性能

      选择使用 SGEMM 还是 DGEMM 通常需要在精度、速度和内存使用之间做权衡。在大多数深度学习应用中，SGEMM 已经能提供足够的精度，同时带来显著的性能提升。

## 各种 Matmul

在深度学习和线性代数中，**矩阵乘法**（Matrix Multiplication，简称`matmul`）是一个核心的操作，通常用于神经网络的前向传播、权重计算和激活计算。矩阵乘法有不同类型的实现方式，适应不同的应用场景和张量形状。

- **Linear Matmul**：常规矩阵乘法，广泛用于线性变换。
- **Batch Matmul**：批量矩阵乘法，适用于处理多维张量。
- **Element-wise Matmul**（Hadamard Product）：逐元素乘法，要求矩阵形状相同。
- **Strassen’s Matmul**：一种快速矩阵乘法算法，减少了乘法次数。
- **Sparse Matmul**：稀疏矩阵乘法，专门处理稀疏矩阵。
- **Block Matmul**：将矩阵分块处理，适合并行计算。

每种 `matmul` 操作都有其特定的应用场景，选择合适的矩阵乘法能够提升算法性能。

1. **Linear Matmul**

   **Linear Matmul**，通常指的是常规的矩阵乘法（即二维矩阵相乘），它用于线性变换。对于两个矩阵 $ A $ 和 $ B $，它们的乘积满足以下条件：

   - $ A $ 的列数与 $ B $ 的行数必须相等。
   - 矩阵乘法的结果是一个新的矩阵，行数为 $ A $ 的行数，列数为 $ B $ 的列数。

   公式如下：

   $$ C = A \times B $$

   其中，

   - $ A \in \mathbb{R}^{m \times n} $
   - $ B \in \mathbb{R}^{n \times p} $
   - 结果矩阵 $ C \in \mathbb{R}^{m \times p} $

   示例：

   假设 $ A $ 是一个 $ 2 \times 3 $ 的矩阵，$ B $ 是一个 $ 3 \times 2 $ 的矩阵：

   $$ A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{pmatrix}, \quad B = \begin{pmatrix} 7 & 8 \\ 9 & 10 \\ 11 & 12 \end{pmatrix} $$

   矩阵乘积 $ C = A \times B $ 结果为：

   $$ C = \begin{pmatrix} 58 & 64 \\ 139 & 154 \end{pmatrix} $$

2. **Batch Matmul**

   **Batch Matmul** 是一种矩阵乘法的扩展，适用于批量的多维张量乘法。在深度学习中，输入通常是三维或更高维的张量，因此需要对批次数据进行矩阵乘法。

   在 Batch Matmul 中，每个批次中的矩阵独立执行矩阵乘法，结果也是批次级别的。例如，给定两个形状为 $ (batch_size, m, n) $ 和 $ (batch_size, n, p) $ 的张量，结果将是形状 $ (batch_size, m, p) $ 的张量。

   示例：

   如果有两个张量，分别是形状 $ (2, 2, 3)$ 和 $ (2, 3, 2) $，它们的每个“子矩阵”会进行独立的矩阵乘法，最终生成一个 $ (2, 2, 2) $ 的输出。

3. **Element-wise Matmul**

   **Element-wise Matmul**，也叫 **Hadamard Product**，指的是两个矩阵在元素级别逐元素相乘，要求两个矩阵具有相同的形状。与常规矩阵乘法不同，元素相乘不会进行矩阵的行列组合，而是直接对对应位置的元素做乘法。

   公式如下：

   $$ C[i, j] = A[i, j] \times B[i, j] $$

   示例：

   $$ A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}, \quad B = \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix} $$

   Hadamard 乘积为：

   $$ C = \begin{pmatrix} 1 \times 5 & 2 \times 6 \\ 3 \times 7 & 4 \times 8 \end{pmatrix} = \begin{pmatrix} 5 & 12 \\ 21 & 32 \end{pmatrix} $$

4. **Strassen’s Matmul**

   **Strassen 算法**（快速矩阵乘法）是一种减少矩阵乘法中运算次数的快速算法。普通的矩阵乘法复杂度是 $ O(n^3) $ ，而 Strassen 算法通过减少一些乘法运算，实现了 $ O(n^{2.81}) $ 的复杂度。这种算法在大型矩阵乘法中能提供一定的效率提升。

   虽然 Strassen 算法在理论上减少了计算复杂度，但其递归实现方式带来了额外的内存开销，因此在某些场景下并不总是最优选择。

5. **Sparse Matmul**

   **Sparse Matmul** 用于处理稀疏矩阵的乘法。稀疏矩阵是指包含大量零元素的矩阵，直接使用普通矩阵乘法效率较低。Sparse Matmul 利用稀疏矩阵的特性，只计算非零元素的乘法，显著减少了计算时间和内存占用。

   稀疏矩阵乘法在图神经网络、科学计算和大规模数据处理中的应用非常广泛。

6. **Block Matmul**

   **Block Matmul** 是矩阵分块计算的一种方式，将大矩阵划分为多个小块，分别进行计算，然后再合并结果。这个方法能够提高矩阵乘法在并行计算中的效率，尤其是在处理非常大的矩阵时。

## GEMM GEMV GEMD

在高性能计算和深度学习领域，**GEMM**、**GEMV** 和 **GEMD** 是指 **通用矩阵运算** 的三种主要类型，分别代表矩阵乘法和矩阵-向量操作的不同变体。

1. **GEMM (General Matrix Multiply)**：

   **GEMM** 表示 **矩阵-矩阵乘法**，是通用矩阵计算中的核心操作。

   **定义**：

   - 计算公式为：

     $$ C = \alpha \cdot A \cdot B + \beta \cdot C $$

     其中：

     - $ A $ 是 $ M \times K $ 的矩阵；
     - $ B $ 是 $ K \times N $ 的矩阵；
     - $ C $ 是 $ M \times N $ 的矩阵；
     - $ \alpha $ 和 $ \beta $ 是标量系数（常用于缩放结果或累加到已有矩阵上）。

   **应用场景**：

   - 深度学习的全连接层（矩阵乘法）。
   - 图像处理中的卷积计算（通过矩阵展开）。
   - 科学计算和数值模拟中大规模矩阵运算。

2. **GEMV (General Matrix-Vector Multiply)**：

   **GEMV** 表示 **矩阵-向量乘法**，是 GEMM 的一个特例。

   **定义**：

   - 计算公式为：

     $$ y = \alpha \cdot A \cdot x + \beta \cdot y $$

     其中：

     - $ A $ 是 $ M \times N $ 的矩阵；
     - $ x $ 是长度为 $ N $ 的向量；
     - $ y $ 是长度为 $ M $ 的向量；
     - $ \alpha $ 和 $ \beta $ 是标量系数。

   **应用场景**：

   - 神经网络中前向传播的向量操作。
   - 数据处理中的线性变换（如 PCA 中的降维操作）。
   - 系统线性方程组求解中的部分计算。

   **区别于 GEMM**：

   - GEMV 是 GEMM 的特殊形式（当 $ B $ 是一个列向量时，GEMM 退化为 GEMV）。
   - GEMV 对计算资源的要求更低，但在大规模数据中仍然占用重要地位。

3. **GEMD (General Matrix-Dimension Multiply)**：

   **GEMD** 是更广义的 **多维矩阵运算（张量运算）** 的一种通用表示，通常表示矩阵乘法扩展到高维的操作。

   **定义**：

   - 将 **GEMM** 扩展到更高维度，支持多张量间的批量矩阵运算。例如： $ C[i] = \alpha \cdot A[i] \cdot B[i] + \beta \cdot C[i] $ 其中 $ i $ 是批量（batch）的索引。

   **应用场景**：

   - 深度学习中批量数据处理（例如 Transformer 中的多头注意力）。
   - 视频分析中的时间序列矩阵操作。
   - 高维张量分解与数值仿真。

   **区别于 GEMM 和 GEMV**：

   - GEMD 是 GEMM 的扩展，用于批量和多维度矩阵运算。
   - GEMD 可以处理多个矩阵的并行计算，适合高性能 GPU 加速场景。

**总结对比**：

| 特性         | GEMM                             | GEMV                    | GEMD                                   |
| ------------ | -------------------------------- | ----------------------- | -------------------------------------- |
| 操作对象     | 矩阵-矩阵                        | 矩阵-向量               | 批量矩阵-矩阵                          |
| 输入维度     | $ M \times K $ 和 $ K \times N $ | $ M \times N $ 和 $ N $ | 批量张量（如 $ B \times M \times K $） |
| 输出结果维度 | $ M \times N $                   | $ M $                   | 批量输出（如 $ B \times M \times N $） |
| 应用场景     | 全连接层，科学计算，仿真         | 向量变换，降维处理      | 批量矩阵操作，深度学习模型             |

## Gather 算子

在深度学习中，**Gather 算子**（`Gather` operation）用于从张量中提取特定的元素或切片，**根据给定的索引**从输入张量中"聚集"（gather）数据。这在处理动态数据访问或选择特定位置的数据时非常有用。

1. **Gather 算子的功能**

   Gather 操作通常用于以下场景：

   - **根据索引选择特定元素**：Gather 可以按照给定的索引列表从张量的某一维度选择数据。
   - **根据索引动态选择**：与静态切片不同，Gather 可以根据输入的索引动态地选取数据。

2. **Gather 的主要参数**

   `Gather`算子通常有两个主要参数：

   - **输入张量（input tensor）**：从这个张量中根据索引提取数据。
   - **索引张量（index tensor）**：指定要从输入张量中提取的元素位置。

   此外，Gather 操作还支持指定沿哪个维度（axis）进行索引，默认沿着第 0 维度进行。

3. **Gather 的工作原理**

   假设有一个输入张量 `input`，形状为 `(5, 4)`，索引张量 `indices` 为 `[0, 2, 3]`，`Gather`操作会根据`indices`中的值从 `input` 的第 0 维中选择相应的数据行。

   示例：

   ```python
   import tensorflow as tf

   # 定义输入张量
   input_tensor = tf.constant([[1, 2, 3, 4],
                               [5, 6, 7, 8],
                               [9, 10, 11, 12],
                               [13, 14, 15, 16],
                               [17, 18, 19, 20]])

   # 定义索引张量
   indices = tf.constant([0, 2, 3])

   # 使用Gather算子
   gathered = tf.gather(input_tensor, indices)

   # 输出结果
   print(gathered)
   ```

   输出：

   ```log
   [[ 1  2  3  4]
    [ 9 10 11 12]
    [13 14 15 16]]
   ```

   在这个例子中，`Gather` 根据索引 `[0, 2, 3]` 从输入张量中选择了第 0 行、第 2 行和第 3 行的数据。

4. **Gather 的应用场景**

   1. **序列处理**：在自然语言处理任务中，`Gather` 可用于根据动态索引从序列或嵌入矩阵中选取数据。
   2. **图神经网络**：在图神经网络中，`Gather` 可以用于根据节点索引选择邻居节点的特征。
   3. **稀疏数据处理**：在需要根据特定的索引选择稀疏数据时，`Gather` 算子非常适用。

5. 注意事项

   - Gather 操作不会改变张量的维度结构，而是返回具有索引选择维度的子集。
   - Gather 的索引必须在张量的有效范围内，否则会抛出越界错误。

   Gather 算子在 TensorFlow、PyTorch 等深度学习框架中都有实现，并且常用于高效的数据索引和提取操作。

## Scatter 算子

`scatter`算子在深度学习中是一种常用的操作，用于**将数据按特定的索引写入到目标张量的特定位置**。它主要通过指定索引（indices）和数据（updates），在目标张量（tensor）中以原地方式进行更新。

1. **Scatter 算子的作用**：

   1. **数据写入与更新**：
      - 将输入数据（`updates`）按照索引（`indices`）写入到目标张量的指定位置（`tensor`）。
      - 支持不同的更新方式（如替换、加法等）。
   2. **张量的稀疏更新**：
      - 用于对某些特定位置进行更新，而无需重新生成整个张量，适合稀疏数据操作。
   3. **索引操作的反向操作**：
      - 类似于`gather`算子的反向操作，它通过索引将数据写回目标张量。

2. **常用场景**：

   1. **深度学习模型的梯度更新**：
      - 在一些分布式计算或稀疏梯度场景下，用`scatter`算子对特定权重的梯度进行更新。
   2. **数据增强与处理**：
      - 根据特定规则对数据或特征进行置换或填充。
   3. **图神经网络（Graph Neural Networks, GNN）**：
      - 计算节点特征聚合时，用于将消息分发到节点或边上。
      - 在实现 Message Passing 机制时，`scatter`算子通常用于归约和消息更新。
   4. **自然语言处理（NLP）**：
      - 在 Transformer 等模型中，用于按位置更新词嵌入或处理 mask 操作。
   5. **稀疏数据处理**：
      - 对于稀疏数据，按需更新非零位置，而不需要操作整个张量。

**示例代码**：

以 PyTorch 的`scatter`为例：

```python
import torch

# 初始化目标张量，设置 dtype 为 int64 以匹配 updates 的数据类型
tensor = torch.zeros(3, 5, dtype=torch.int64)

# 索引位置
indices = torch.tensor([[0, 1, 2], [3, 4, 0]])

# 更新值
updates = torch.tensor([[5, 6, 7], [8, 9, 10]], dtype=torch.int64)

# 按索引进行更新
tensor.scatter_(dim=1, index=indices, src=updates)

print(tensor)
'''输出：
tensor([[ 5,  6,  7,  0,  0],
        [10,  0,  0,  8,  9],
        [ 0,  0,  0,  0,  0]])
'''
```

dim 参数的作用：

- dim=0：按行更新，即沿着第 0 维（行）进行操作。每一行独立地被处理，indices 的每一行中索引的值，更新到 input 的每一行。
- dim=1：按列更新，即沿着第 1 维（列）进行操作。每一列独立地被处理，indices 的每一列中索引的值，更新到 input 的每一列。
- 更高维度：对于高维张量，dim 指定了更新的哪个轴。

**结果解释**：

- 在 `dim=1`（列方向）更新，每一行独立地被处理，indices 的每一行中的值更新到 input 的每一行：

  - 第 1 行，第`indices[0][0]=0`位置赋值为`updates[0][0]=5`。
  - 依次更新其它位置。

```python
import torch
tensor = torch.zeros(5, 3, dtype=torch.int64)
indices = torch.tensor([[0, 1, 2], [3, 4, 0]])
updates = torch.tensor([[5, 6, 7], [8, 9, 10]])

# 按行（dim=0）进行更新
tensor.scatter_(dim=0, index=indices, src=updates)
print(tensor)
'''output:
tensor([[ 5,  0, 10],
        [ 0,  6,  0],
        [ 0,  0,  7],
        [ 8,  0,  0],
        [ 0,  9,  0]])
'''

tensor = torch.zeros(2, 3, 4)
indices = torch.tensor([[[1, 2, 0], [0, 1, 2]], [[1, 0, 2], [2, 1, 0]]])
updates = torch.ones(2, 2, 3)

# 按 dim=2 更新
tensor.scatter_(dim=2, index=indices, src=updates)
print(tensor)
'''output:
tensor([[[1., 1., 1., 0.],
         [1., 1., 1., 0.],
         [0., 0., 0., 0.]],

        [[1., 1., 1., 0.],
         [1., 1., 1., 0.],
         [0., 0., 0., 0.]]])
'''
```

**结果解释**：

dim=0 表示按行操作，每一列独立地被处理。
第一列：

- `indices[0][0]=0`，因此第 0 行被赋值为 `updates[0][0]=5`。
- `indices[1][0]=3`，因此第 3 行被赋值为 `updates[1][0]=8`。
- 其他列以此类推。

dim=2 指定了更新操作发生在第 3 个轴（最后一个维度）。

## RoPe 算子

RoPE（Rotary Position Embedding，旋转位置编码）是一种用于大模型中的位置编码方法，最早由论文《RoFormer: Enhanced Transformer with Rotary Position Embedding》中提出。**RoPE 通过对自注意力机制中的输入向量应用旋转变换来嵌入位置信息**，主要目的是克服传统位置编码方式的局限性，使得模型能够**更好地处理长序列问题**。

RoPE 的核心思想是在注意力计算时，将输入向量的不同维度按照特定的方式进行旋转，这种旋转与输入的位置相关联。具体来说，对于输入向量中的每一对相邻维度（偶数维和奇数维），根据其在序列中的位置进行不同角度的旋转操作。通过这种方式，RoPE 能够实现位置编码的周期性，同时允许模型在一定程度上推广到比训练时更长的序列。

1. **RoPE 的优点**

   1. **无需额外参数**：RoPE 不需要引入额外的可学习参数，这与传统的可学习位置编码不同，因此它具有更好的通用性和扩展性。
   2. **周期性**：由于位置编码是通过旋转操作实现的，它具有自然的周期性，非常适合处理循环结构的数据。
   3. **长序列处理能力**：RoPE 在处理长序列时的表现优于传统的绝对位置编码方式。它允许模型推广到比训练时更长的序列，这在大模型和长文档处理任务中尤为重要。
   4. **与自注意力机制无缝集成**：RoPE 的设计可以直接与 Transformer 架构中的自注意力机制结合使用，提升模型在序列数据上的表现。

2. **RoPE 的具体实现**

   <!--prettier-ignore-->
   RoPE 的旋转操作通常可以使用复数或者实数域上的旋转矩阵来实现。给定输入向量 $ \mathbf{x}_i $ 的偶数维度 $ x_{2k} $ 和奇数维度 $ x_{2k+1} $，其经过 RoPE 变换后的新坐标可以表示为：
   $$ \begin{aligned} x_{2k}' &= x_{2k} \cos(\theta_i) - x_{2k+1} \sin(\theta_i) \\ x_{2k+1}' &= x_{2k} \sin(\theta_i) + x_{2k+1} \cos(\theta_i) \end{aligned} $$

   其中，$ \theta_i $ 是根据位置 $ i $ 生成的角度，通常设定为与位置 $ i $ 和维度 $ k $ 相关的固定函数，例如：$ \theta_i = i / 10000^{2k/d} $，其中 $ d $ 是输入向量的维度。

   通过这种方式，RoPE 能够在注意力计算时嵌入序列位置信息，且不会显著增加计算复杂度。

## Concat 算子

在大模型的推理和训练过程中，**`concat`算子**（拼接算子）是一个常用的操作，尤其在处理多模态数据或需要将不同特征融合的场景下。`concat`算子的作用是**将两个或多个张量（tensor）沿某个维度进行拼接，生成一个新的张量**。

1. **功能和定义**

   - **`concat`**（拼接）算子将输入的多个张量沿指定的轴（维度）合并为一个张量。
   - 可以拼接二维、三维甚至更高维的张量。比如，对于二维张量，`concat`算子可以将它们沿行或列拼接，具体取决于指定的维度。

2. **应用场景**

   - **多模态数据融合**：在处理图像、文本、音频等不同类型的数据时，`concat`可以用来将它们的特征拼接在一起，形成一个统一的输入。
   - **特征融合**：在神经网络中，`concat`算子常用于将不同网络层的输出特征合并，用于后续的处理或决策。例如，卷积神经网络（CNN）中，特征图可以在某些层进行拼接以增强表达能力。
   - **数据预处理和增广**：当处理不同尺度、不同形式的数据时，拼接可以作为数据预处理的一部分，用于统一不同输入数据的形状。

3. **常见的操作细节**

   - 拼接轴（axis）：拼接时需要指定沿着哪个维度拼接。例如：

     - 沿第一个维度（通常是批次维度）拼接：`axis=0`。
     - 沿第二个维度（通常是特征维度）拼接：`axis=1`。

   - **输入张量的维度匹配**：拼接操作要求除了拼接维度外，其他维度的大小必须相同。如果要拼接的张量在非拼接维度上的大小不同，则会报错。

4. **代码示例**

   假设有两个二维张量：

   ```python
   import tensorflow as tf

   # 创建两个二维张量
   tensor1 = tf.constant([[1, 2], [3, 4]], dtype=tf.float32)
   tensor2 = tf.constant([[5, 6], [7, 8]], dtype=tf.float32)

   # 沿着第0维（行）拼接（垂直拼接）
   concat_axis0 = tf.concat([tensor1, tensor2], axis=0)
   print("沿着第0维拼接结果:\n", concat_axis0)
   # 输出：
   '''
   沿着第0维拼接结果:
    tf.Tensor(
   [[1. 2.]
    [3. 4.]
    [5. 6.]
    [7. 8.]], shape=(4, 2), dtype=float32)
   '''

   # 沿着第1维（列）拼接（水平拼接）
   concat_axis1 = tf.concat([tensor1, tensor2], axis=1)
   print("沿着第1维拼接结果:\n", concat_axis1)
   # 输出：
   '''
   沿着第1维拼接结果:
    tf.Tensor(
   [[1. 2. 5. 6.]
    [3. 4. 7. 8.]], shape=(2, 4), dtype=float32)
   '''
   ```

5. **总结**

   `concat`算子是一个非常有用的工具，用于将不同张量拼接成一个新的张量，广泛应用于多模态学习、特征融合以及神经网络架构中。拼接时需要注意拼接的轴和维度匹配问题，确保操作的合法性。

## split 算子

在大模型推理中，**`split`** 算子（分割算子）是另一个常用的操作。它的作用是**将一个张量沿指定的维度分割成多个子张量**。这一操作在许多深度学习任务中非常有用，尤其是当需要将数据分成不同的部分进行处理时。

1. **功能和定义**

   - **`split`** 算子将一个大的张量沿某个维度分割成多个较小的张量，通常是等分或按照特定大小分割。
   - 你可以指定每个子张量的大小，或者指定分割的次数，系统会根据这些信息自动进行分割。

2. **应用场景**

   - **特征拆分**：在某些模型架构中（比如卷积神经网络或变压器），你可能需要将特征图或特征矩阵拆分成多个部分进行独立处理，或者将它们传递给不同的子模型进行并行处理。
   - **多任务学习**：在多任务学习中，你可能会将输入数据分割成不同部分，分别用于不同的任务。
   - **模型并行**：当模型太大，无法在单个设备上运行时，可以通过拆分输入或模型的一部分，在多个设备上并行计算。

3. **常见的操作细节**

   - **分割维度（axis）**：`split`操作通常需要指定沿哪个维度进行分割。
   - **分割大小**：你可以指定每个子张量的大小，或者指定分割成多少个子张量。如果没有指定大小，系统会尽量平分。

4. **代码示例**

   假设有一个二维张量，大小为 `(4, 8)`，我们可以将其沿不同的维度进行分割。

   ```python
   import tensorflow as tf

   # 创建一个二维张量
   tensor = tf.constant([[1, 2, 3, 4, 5, 6, 7, 8],
                         [9, 10, 11, 12, 13, 14, 15, 16],
                         [17, 18, 19, 20, 21, 22, 23, 24],
                         [25, 26, 27, 28, 29, 30, 31, 32]], dtype=tf.float32)

   # 沿着第1维分割成2个张量
   split_tensors = tf.split(tensor, num_or_size_splits=2, axis=1)
   for i, t in enumerate(split_tensors):
       print(f"分割后的张量 {i}:\n", t)
   # 输出：
   '''
   分割后的张量 0:
    tf.Tensor(
   [[1. 2. 3. 4.]
    [9. 10. 11. 12.]
    [17. 18. 19. 20.]
    [25. 26. 27. 28.]], shape=(4, 4), dtype=float32)
   分割后的张量 1:
    tf.Tensor(
   [[5. 6. 7. 8.]
    [13. 14. 15. 16.]
    [21. 22. 23. 24.]
    [29. 30. 31. 32.]], shape=(4, 4), dtype=float32)
   '''

   # 沿着第0维分割成2个张量
   split_tensors = tf.split(tensor, num_or_size_splits=2, axis=0)
   for i, t in enumerate(split_tensors):
       print(f"分割后的张量 {i}:\n", t)
   # 输出：
   '''
   分割后的张量 0:
    tf.Tensor(
   [[ 1.  2.  3.  4.  5.  6.  7.  8.]]
   [[ 9. 10. 11. 12. 13. 14. 15. 16.]]
   shape=(1, 8), dtype=float32)

   分割后的张量 1:
    tf.Tensor(
   [[17. 18. 19. 20. 21. 22. 23. 24.]]
   [[25. 26. 27. 28. 29. 30. 31. 32.]]
   shape=(1, 8), dtype=float32)
   '''
   ```

5. **总结**

- `split`算子主要用于将一个张量沿着指定的维度分割成多个子张量。
- 在 TensorFlow 中，`tf.split()` 函数允许你指定分割的数量或大小。
- 在 PyTorch 中，`torch.split()` 可以指定每个子张量的大小（`split_size_or_sections`）或者分割的数量（`sections`）。
- 这个操作在模型并行、特征拆分、数据并行等方面非常有用，尤其是在处理大型数据集和模型时。

## slice 算子

在大模型（如深度学习模型）中，`slice` 算子**通常用于提取张量（tensor）的一部分**。它根据指定的索引和维度，截取输入张量的一部分，并返回一个新的张量。这个操作在数据预处理、模型构建、以及在不同层之间传递数据时非常常见。

1. **功能**
   具体来说，`slice` 算子的作用是从输入张量中按照指定的起始位置、终止位置和步长来提取子张量。通常有以下几种常见形式的参数：

   1. **起始索引**：指定从哪个位置开始截取。
   2. **结束索引**：指定截取的结束位置。
   3. **步长**：指定每个维度上切片的步长，常用于跳跃式切片。

2. **使用场景**

   - **子集选择**：在神经网络中，你可能希望根据不同的层或不同的输入特征选择子集。
   - **数据预处理**：在进行数据增强或特征选择时，可能需要通过 `slice` 从原始数据中提取部分信息。
   - **批处理**：在处理大规模数据时，通过 `slice` 对数据进行切片，以便分批处理。

3. **注意事项**

   - `slice` 操作并不创建输入张量的副本（除非在某些框架中明确指定）。它只是返回对原始数据的视图。
   - 根据使用的深度学习框架（如 TensorFlow、PyTorch 等），`slice` 的具体实现和语法可能有所不同，但其基本功能是类似的。

4. **代码示例**

   ```python
   import torch

   tensor = torch.tensor([[1, 2, 3, 4],
                          [5, 6, 7, 8],
                          [9, 10, 11, 12],
                          [13, 14, 15, 16]])

   # 从第1行到第2行，选择所有列
   sliced_tensor = tensor[1:3, :]
   print(sliced_tensor)
   # 输出：
   '''
   [[ 5,  6,  7,  8],
    [ 9, 10, 11, 12]]
   '''
   ```

这些操作在实际开发中非常常见，尤其是在处理高维数据（如图像、序列数据等）时，`slice` 算子能够有效地减少不必要的计算，提取出有用的信息。

## 激活函数

[激活函数](https://github.com/wdndev/ai_interview_note/blob/main/docs/dl/1.%E6%BF%80%E6%B4%BB%E5%87%BD%E6%95%B0.md)
[深度学习领域最常用的 10 个激活函数，一文详解数学原理及优缺点](https://www.jiqizhixin.com/articles/2021-02-24-7)

在大模型（如深度神经网络）中，激活函数是决定神经元是否激活的数学函数，它在每个神经元的输出中起到**非线性转换**的作用。不同的激活函数对模型的性能和训练过程有着重要影响。
下面是一些常见的激活函数及其特点：

1. **Sigmoid（S 形函数）**

   - 公式：
     $$ \sigma(x) = \frac{1}{1 + e^{-x}} $$
   - 输出范围：$ [0, 1] $
   - 特点：将输入值压缩到 0 和 1 之间，常用于二分类任务的输出层。
   - 缺点：容易出现梯度消失问题，特别是在深层网络中。执行指数运算，计算机运行得较慢。
   <div style="text-align: center">
   <img src="https://image.jiqizhixin.com/uploads/editor/eeab4bb3-4d22-46fa-9428-142d15c1fc8a/640.png" style="width: 30%">
   </div>

2. **Tanh（双曲正切函数）**

   - 公式：
     $$ \text{tanh}(x) = \frac{2}{1 + e^{-2x}} - 1 $$
   - 输出范围：$ [-1, 1] $
   - 特点：比 Sigmoid 有更广的输出范围，输出中心对称，适用于隐藏层。
   - 缺点：同样容易出现梯度消失问题，尤其是对于非常大的输入。
   <div style="text-align: center">
   <img src="https://image.jiqizhixin.com/uploads/editor/a25ffd1e-786d-4f69-ae86-4b176009e2bf/640.png" style="width: 30%">
   </div>

3. **ReLU（Rectified Linear Unit）**

   - 公式：
     $$ \text{ReLU}(x) = \max(0, x) $$
   - 输出范围：$ [0, +\infty) $
   - 特点：计算简单，能够加速收敛。它有效避免了梯度消失问题，广泛应用于隐藏层。
   - 缺点：对于负输入，ReLU 的梯度为 0，可能导致"死神经元"问题。
   <div style="text-align: center">
   <img src="https://image.jiqizhixin.com/uploads/editor/aad549e6-ee38-464c-990c-5992279cc5e0/640.png" style="width: 30%">
   </div>

4. **Leaky ReLU**

   - 公式：
     $$ \text{Leaky ReLU}(x) = \begin{cases} x, & x \geq 0 \\ \alpha x, & x < 0 \end{cases} $$
   - 输出范围：$ [-\infty, +\infty) $
   - 特点：对负数输入值进行轻微“泄漏”，避免 ReLU 的死神经元问题。
   - 缺点：需要设定合适的参数 $ \alpha $，通常为 0.01，否则可能无法有效避免问题。
   <div style="text-align: center">
   <img src="https://image.jiqizhixin.com/uploads/editor/91a214e0-d773-4ede-be3b-3f046ae5e1d4/640.png" style="width: 30%">
   </div>

5. **PReLU（Parametric ReLU）**

   - 公式：
     $$ \text{PReLU}(x) = \begin{cases} x, & x \geq 0 \\ \alpha x, & x < 0 \end{cases} $$
   - 输出范围：$ [-\infty, +\infty) $
   - 特点：
     - PReLU 是 ReLU 的扩展，允许对负值部分的斜率 $ \alpha $ 进行训练，而不是固定为 0。
     - 这种“参数化”使得模型能动态地调整负半轴的“泄漏”量，从而增强了灵活性。
   - 优点：
     - 可以通过学习负半轴的斜率来避免 ReLU 的死神经元问题（即那些始终输出为 0 的神经元）。
     - 在一些任务中，PReLU 的表现优于 ReLU，尤其是对于那些训练数据分布比较复杂的情况。
     <div style="text-align: center">
     <img src="https://image.jiqizhixin.com/uploads/editor/daba35ae-e366-4233-b3ab-294d9a20d5e7/640.png" style="width: 30%">
     </div>

6. **ELU（Exponential Linear Unit）**

   - 公式：
     $$ \text{ELU}(x) = \begin{cases} x, & x > 0 \\ \alpha(e^x - 1), & x \leq 0 \end{cases} $$
   - 输出范围：$ (-\alpha, +\infty) $
   - 特点：对负值有指数性处理，能够更好地逼近零均值输出，且减少梯度消失问题。
   - 缺点：相比 ReLU 计算上更复杂，且需要选择合适的 $ \alpha $ 值。
   <div style="text-align: center">
   <img src="https://pic2.zhimg.com/v2-fa5b4490dc4a7f698543f9d37e28b6b1_1440w.jpg" style="width: 30%">
   </div>

7. **GLU（Gated Linear Unit）**

   - 公式：
     $$ \text{GLU}(x)=x \odot \sigma(g(x)) $$
     g(x) 表示的是向量 $x$ 经过一层 MLP 或者卷积，$ \odot $表示两个向量逐元素相乘，$ \sigma $ 表示 sigmoid 函数。
   - 输出范围：$ (-\infty, +\infty) $
   - 特点：
     - 当$\sigma(g(x))$趋近于 0 时表示对$x$进行阻断，当$\sigma(g(x))$趋近于 1 时表示允许$x$通过，以此实现门控激活函数的效果。
   - 优点：
     - 信息选择性：GLU 通过门控机制，使得模型能够选择性地通过信息，从而提高模型的表达能力。
     - 非线性增强：GLU 结合了线性变换和非线性激活，从而增强了模型的非线性特性。
     - 提高模型性能：GLU 在许多任务中表现出色，特别是在自然语言处理（NLP）和序列建模任务中。

8. **Swish / SiLU（Sigmoid Linear Unit）**

   - 公式：
     $$ \text{Swish}(x) = x \cdot \sigma(\beta x) $$
   - 输出范围：$ (-\infty, +\infty) $
   - 特点：
     - $\beta = 1 $ 时也称为 SiLU，是 Sigmoid 和线性函数的组合。
     - 与 ReLU 相比，它在负数区域进行平滑处理，避免了死神经元问题。
     - 它的名字“SiLU”源自其形式上的类似于 Sigmoid 与线性（Linear）函数的结合。
   - 优点：
     - SiLU 具有连续的梯度，不容易造成梯度消失问题，适用于较深的网络。
     - 经过一些实验，SiLU 相比 ReLU 和其他传统激活函数能在某些深度神经网络上提升性能。
     <div style="text-align: center">
     <img src="https://image.jiqizhixin.com/uploads/editor/81698e3e-b92a-4695-a06c-aae3d0d11c68/640.png" style="width: 30%">
     </div>

9. **SwiGLU（Switched Gated Linear Unit）**

   - 公式：
     $$ \text{SwiGLU}(x) = (xV + b1) \odot swish(xW + b2) $$
     $W, V$ 表示学习的权重矩阵，$b1, b2$ 是偏置，swish 表示 $ swish(x) = x ⋅ sigmoid(βx) $，$ \odot $ 表示两个向量逐元素相乘。
   - 输出范围：$ (-\infty, +\infty) $
   - 特点：
     - SwiGLU 是 GLU 的一个变体，用 Swish 函数替代了原始 GLU 中的 sigmoid 门控。相比原始 GLU，SwiGLU 在某些任务上表现更好，在 PaLM、GPT-4 等大型语言模型中得到应用。
     - 是一种复合激活函数，旨在结合两种激活函数的优点：非线性和可控性。
   - 优点：
     - 它结合了 ReLU 的稀疏性和 Sigmoid 的平滑性，能够提高网络的表现，尤其是在大型 Transformer 网络中表现优异。
     - 比较适用于需要对激活进行复杂控制的模型，像自然语言处理任务中的 GPT、BERT 等模型中曾被使用。

10. **GELU（Gaussian Error Linear Unit）**
    [GELU 激活函数介绍和笔记](https://blog.csdn.net/kkxi123456/article/details/122694916)

    - 公式：
      $$ \text{GELU}(x) = x \ast \phi(x) $$
      $ \phi(x) $ 是高斯分布（正态分布）的累积分布函数（CDF），该函数的具体表达为：

      <!--prettier-ignore-->
      $$ x \ast P(X \leq x) = x \int_{- \infty}^{x} \frac{e^{- \frac{(X - \mu)^2}{2 \sigma^2}}}{\sqrt{2 \pi} \sigma} dX $$
      其中 $ \mu $ 和 $ \sigma $ 分别代表正太分布的均值和标准差。由于上面这个函数是无法直接计算的，研究者在研究过程中发现 GELU 函数可以被近似地表示为

      $$ \text{GELU}(x) = 0.5x \left( 1 + \tanh\left( \sqrt{\frac{2}{\pi}}(x + 0.044715x^3) \right) \right) $$
      或者
      $$ \text{GELU}(x) = x \ast \sigma(1.702x) $$

    - 输出范围：$ (-\infty, +\infty) $
    - 特点：
      - GELU 是基于高斯误差函数的激活函数，能够让负值在接近零时逐渐逼近零（而不是像 ReLU 一样直接截断）。这种“平滑”特性有助于网络的训练和优化。
      - 比 ReLU 更加平滑且没有死神经元问题，在大规模预训练模型（如 BERT、GPT 系列）中有很好的表现。
    - 优点：
      - 相比 ReLU，GELU 对输入的负部分处理更平滑，有助于避免梯度消失或爆炸的问题。
      - GELU 相比 Swish 在某些任务上表现得更好，尤其是在 NLP 和 Transformer 模型中。
      <div style="text-align: center">
      <img src="https://i-blog.csdnimg.cn/blog_migrate/2fe1e7bbb7f876e92f78b992a7a3ef54.png" style="width: 30%">
      </div>

11. **Softmax**

    - 公式：
      $$ \text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}} $$
    - 输出范围：$ [0, 1] $，且所有输出加起来为 1
    - 特点：常用于多分类问题的输出层，能够将网络的输出转换为概率分布。
    - 缺点：当类别数较多时，计算量较大。
       <div style="text-align: center">
       <img src="https://image.jiqizhixin.com/uploads/editor/1c43f7b7-f414-44ca-82f4-d87016ad190a/640.png" style="width: 30%">
       </div>

12. **总结**

这些激活函数有各自的优势，适用于不同的场景：

- **Sigmoid**和**Tanh**：适用于小范围输出，但容易导致梯度消失。
- **ReLU**及其变体（如 Leaky ReLU、ELU、PReLU）：更常用于隐藏层，避免了梯度消失的问题，并且计算上非常高效。
- **SiLU（Swish）**：作为较新的激活函数，常在深度神经网络中取得较好的效果，尤其在大模型中表现较好。
- **GELU**：在大规模预训练模型（如 Transformer、BERT 等）中表现突出，因为它的平滑特性能有效地避免梯度消失问题，且有助于模型收敛。
- **SwiGLU**：SwiGLU 是 GLU 的一个变体，用 Swish 函数替代了原始 GLU 中的 sigmoid 门控。相比原始 GLU，SwiGLU 在某些任务上表现更好，在 PaLM、GPT-4 等大型语言模型中得到应用。
- **Softmax**：主要用于分类问题的输出层。

不同任务和网络结构对激活函数的选择有不同的需求。实际应用中，ReLU 及其变体在许多任务中都表现得较为优秀。
