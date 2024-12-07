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

**1. GEMM (General Matrix Multiply)**：

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



**2. GEMV (General Matrix-Vector Multiply)**：

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

**3. GEMD (General Matrix-Dimension Multiply)**：

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

| 特性         | GEMM                             | GEMV                    | GEMD                                 |
|------------|----------------------------------|-------------------------|--------------------------------------|
| 操作对象     | 矩阵-矩阵                        | 矩阵-向量               | 批量矩阵-矩阵                        |
| 输入维度     | $ M \times K $ 和 $ K \times N $ | $ M \times N $ 和 $ N $ | 批量张量（如 $ B \times M \times K $） |
| 输出结果维度 | $ M \times N $                   | $ M $                   | 批量输出（如 $ B \times M \times N $） |
| 应用场景     | 全连接层，科学计算，仿真           | 向量变换，降维处理       | 批量矩阵操作，深度学习模型            |

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

## Scatter算子

`scatter`算子在深度学习中是一种常用的操作，用于**将数据按特定的索引写入到目标张量的特定位置**。它主要通过指定索引（indices）和数据（updates），在目标张量（tensor）中以原地方式进行更新。

**Scatter算子的作用**：

1. **数据写入与更新**：
   - 将输入数据（`updates`）按照索引（`indices`）写入到目标张量的指定位置（`tensor`）。
   - 支持不同的更新方式（如替换、加法等）。
2. **张量的稀疏更新**：
   - 用于对某些特定位置进行更新，而无需重新生成整个张量，适合稀疏数据操作。
3. **索引操作的反向操作**：
   - 类似于`gather`算子的反向操作，它通过索引将数据写回目标张量。

**常用场景**：

1. **深度学习模型的梯度更新**：
   - 在一些分布式计算或稀疏梯度场景下，用`scatter`算子对特定权重的梯度进行更新。
2. **数据增强与处理**：
   - 根据特定规则对数据或特征进行置换或填充。
3. **图神经网络（Graph Neural Networks, GNN）**：
   - 计算节点特征聚合时，用于将消息分发到节点或边上。
   - 在实现Message Passing机制时，`scatter`算子通常用于归约和消息更新。
4. **自然语言处理（NLP）**：
   - 在Transformer等模型中，用于按位置更新词嵌入或处理mask操作。
5. **稀疏数据处理**：
   - 对于稀疏数据，按需更新非零位置，而不需要操作整个张量。

**示例代码**：

以PyTorch的`scatter`为例：

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

- dim=0：按行更新，即沿着第0维（行）进行操作。每一行独立地被处理，indices 的每一行中索引的值，更新到 input 的每一行。
- dim=1：按列更新，即沿着第1维（列）进行操作。每一列独立地被处理，indices 的每一列中索引的值，更新到 input 的每一列。
- 更高维度：对于高维张量，dim 指定了更新的哪个轴。

**结果解释**：

- 在 `dim=1`（列方向）更新，每一行独立地被处理，indices 的每一行中的值更新到 input 的每一行：

  - 第1行，第`indices[0][0]=0`位置赋值为`updates[0][0]=5`。
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

dim=2 指定了更新操作发生在第3个轴（最后一个维度）。

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
