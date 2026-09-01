[toc]

# PyTorch 模块

## 随机数生成

1. **浮点型随机数 (Floating-point)**

   这些函数默认生成 `torch.float32` 类型的张量，通常用于权重初始化或噪声模拟。
   - **`torch.rand(*size)`**：生成 $[0, 1)$ 之间**均匀分布**的随机数。
   - **`torch.randn(*size)`**：生成均值为 0，方差为 1 的**标准正态分布**（高斯分布）随机数。
   - **`torch.rand_like(input)`**：根据输入张量的形状（shape）生成 $[0, 1)$ 的均匀分布随机数。

2. **整型随机数 (Integer)**

   如果你需要生成索引、类别标签或随机采样掩码，通常使用以下函数：
   - **`torch.randint(low=0, high, size)`**：生成在 $[low, high)$ 范围内的均匀分布**整数**。注意是不包含 `high` 的。
   - **`torch.randperm(n)`**：生成一个从 $0$ 到 $n-1$ 的**随机排列**（Random Permutation）。常用于打乱数据索引。

3. **特定概率分布 (Specific Distributions)**

   除了最常用的均匀分布和正态分布，PyTorch 还提供了一些进阶分布函数：
   - **`torch.normal(mean, std, *size)`**：生成指定均值 $\mu$ 和标准差 $\sigma$ 的正态分布。
   - **`torch.bernoulli(input)`**：生成**伯努利分布**（0 或 1）。输入是一个包含概率 $p$ 的张量，输出结果按该概率随机呈现 0 或 1。
   - **`torch.poisson(input)`**：根据输入张量中的速率参数（$\lambda$）生成**泊松分布**随机数。
   - **`torch.exponential(lambd=1.0)`**：生成**指数分布**随机数。

4. **随机种子：**
   为了保证实验的可复现性，建议在代码开头设置随机种子：

   ```python
   import torch
   torch.manual_seed(42) # 42 是宇宙的终极答案
   ```

快速查阅表

| **生成目标**       | **推荐函数**      | **示例**                                    |
| ------------------ | ----------------- | ------------------------------------------- |
| **0到1均匀分布**   | `torch.rand`      | `torch.rand(2, 3)`                          |
| **标准正态分布**   | `torch.randn`     | `torch.randn(2, 3)`                         |
| **指定范围整数**   | `torch.randint`   | `torch.randint(0, 10, (2, 2))`              |
| **打乱索引/排列**  | `torch.randperm`  | `torch.randperm(10)`                        |
| **自定义均值方差** | `torch.normal`    | `torch.normal(0, 0.1, (5,))`                |
| **0/1二项分布**    | `torch.bernoulli` | `torch.bernoulli(torch.tensor([0.5, 0.8]))` |

## 数据类型转换

在 PyTorch 中，数据类型转换（Dtype Casting）是一个非常高频的操作。你可以通过多种方式实现，最推荐的是使用 `.to()` 方法，因为它不仅能改类型，还能顺便移动设备（如从 CPU 到 GPU）。

1. **通用且推荐：`.to()` 方法**

   这是目前最标准的方法，语义清晰，且支持非阻塞操作。

   ```python
   import torch

   tensor = torch.randn(2, 2)  # 默认是 float32
   # 转换为 float16 (半精度)
   tensor_half = tensor.to(torch.float16)
   # 转换为 int32
   tensor_int = tensor.to(torch.int32)
   ```

2. **快捷简便：`.type()` 方法**

   如果你只需要改变类型，可以使用这个方法。如果不传参数，它会返回张量的类型字符串。

   ```python
   # 转换为双精度浮点型
   tensor_double = tensor.type(torch.float64)
   ```

3. **别名方法（最快语法糖）**

   PyTorch 为每种基本类型都提供了专门的转换函数，写起来最省事：
   - **`.float()`**: 转换为 `float32`
   - **`.double()`**: 转换为 `float64`
   - **`.half()`**: 转换为 `float16`
   - **`.int()`**: 转换为 `int32`
   - **`.long()`**: 转换为 `int64` (常用于索引和标签)
   - **`.bool()`**: 转换为布尔型

   ```python
   # 深度学习中最常用的：将标签转换为长整型
   labels = torch.tensor([1.0, 2.0]).long()
   ```

4. **常用数据类型对照表**

   为了方便你选择，这里列出了最常用的几种类型：

   | **目标类型**  | **PyTorch 对应关键字**            | **常用场景**             |
   | ------------- | --------------------------------- | ------------------------ |
   | **32位浮点**  | `torch.float32` 或 `torch.float`  | 网络权重、输入数据       |
   | **64位浮点**  | `torch.float64` 或 `torch.double` | 高精度科学计算           |
   | **16位浮点**  | `torch.float16` 或 `torch.half`   | 混合精度训练（省显存）   |
   | **64位整数**  | `torch.int64` 或 `torch.long`     | 类别标签、Embedding 索引 |
   | **32位整数**  | `torch.int32` 或 `torch.int`      | 一般计数                 |
   | **8位无符号** | `torch.uint8`                     | 图像掩码（Mask）         |

**⚠️ 两个关键注意事项**

1. **就地转换（In-place）**：

   上述所有转换方法（`.to()`, `.float()` 等）**都不会改变原张量**，而是返回一个新的张量。

   ```python
   x = torch.ones(2, dtype=torch.float32)
   x.int()       # 这行代码执行了，但 x 依然是 float32
   x = x.int()   # 必须重新赋值才能生效
   ```

2. **设备兼容性**：

   如果你在进行类型转换的同时需要移动设备（比如从 CPU 移到 GPU），一次性使用 `.to()` 是效率最高的方案：

   ```python
   device = "cuda" if torch.cuda.is_available() else "cpu"
   tensor = tensor.to(device, dtype=torch.float16)
   ```

## 导入/导出数据

1. 官方标准方法：`torch.save()` 与 `torch.load()`

   这是 PyTorch 最核心的存储方式。它不仅保存数据，还保存了 Tensor 的 **元数据**（如 `dtype`、`device`、`shape` 等）。适用于在 PyTorch 环境内部保存中间结果、模型权重。

   ```python
   import torch
   x = torch.randn(3, 3)

   # 保存
   torch.save(x, 'data.pt')
   # 读取
   x_loaded = torch.load('data.pt')
   ```

   **注意**：如果你在 GPU 上保存了 Tensor，默认读取时也会尝试加载到 GPU。如果目标机器没 GPU，需指定：`torch.load('data.pt', map_location='cpu')`。

2. 类似 NumPy 的文本/二进制存储

   PyTorch 本身没有内置 `savetxt`/`tofile`，但由于 Tensor 和 NumPy 数组共享底层内存，转换极其简单。

   存储为可读文本 (类似 `savetxt`)

   ```python
   import numpy as np

   # 必须先转到 CPU，再转为 numpy
   x_np = x.cpu().numpy()
   np.savetxt('data.txt', x_np, delimiter=',', fmt='%.4f')
   ```

   存储为原始二进制 (类似 `tofile`)

   ```python
   # 写入
   x.cpu().numpy().tofile('data.bin')

   # 读取时必须手动指定 dtype 和 shape
   original_data = np.fromfile('data.bin', dtype=np.float32).reshape(3, 3)
   ```

3. 安全且高效的新标准：`Safetensors`

   这是由 Hugging Face 开发的一种新格式，正逐渐取代 `.pt` 成为行业标准。
   **优点**：**安全性极高**（防止 Pickle 反序列化攻击）、**速度极快**（支持零拷贝加载）。
   **安装**：`pip install safetensors`

   ```python
   from safetensors.torch import save_file, load_file

   tensors = {"my_tensor": x}
   # 保存 (必须以字典形式存储)
   save_file(tensors, "model.safetensors")

   # 读取
   loaded = load_file("model.safetensors")
   x_loaded = loaded["my_tensor"]
   ```

# 常用函数记录

## torch.Tensor

### Tensor.expand

```python
tensor.expand(*sizes)
```

- `*sizes`：你期望的目标形状（可变参数或列表/元组）。你可以在目标形状中使用 **`-1`**，表示该维度保持原始大小不变。

`expand` 遵循严格的广播逻辑，必须满足以下条件（与 `expand_as` 一致）：

1. **维度数量**：`len(sizes)` **必须大于或等于** 原始张量的维度数。如果更多，多出来的维度会被放在**前面**（相当于自动在原始张量前面补了 1）。
2. **维度对齐**：对于原始张量的每个维度：
   - 如果目标维度大于原始维度，那么原始该维度的**大小必须为 1**（此时才能扩展）。
   - 如果目标维度等于原始维度，大小必须完全相同（或者用 `-1` 保持原样）。
   - （注意：如果目标维度小于原始维度，会直接报错，除非通过补 `-1` 在前面对齐）。

```python
import torch

# 1. 基本扩展：将 (3, 1) 扩展为 (3, 4)
a = torch.tensor([[1], [2], [3]])  # shape: (3, 1)
b = a.expand(3, 4)
print(b)
# 输出：
# tensor([[1, 1, 1, 1],
#         [2, 2, 2, 2],
#         [3, 3, 3, 3]])

# 2. 使用 -1 保持维度不变
c = torch.tensor([[1], [2], [3]])
d = c.expand(-1, 4)  # 第一维保持 3，第二维扩展到 4
print(d.shape)  # 输出: torch.Size([3, 4])

# 3. 增加新的维度（在前面补维度）
e = torch.tensor([1, 2, 3])  # shape: (3,)
# 注意：原维度是 1 维，现在目标是 3 维 (1, 3, 4)
# 新增的靠前维度 dim0=1，可以扩展到 1；dim1 对应原 dim0=3 保持不变；dim2 新增扩展为 4
f = e.expand(1, 3, 4)
print(f.shape)  # 输出: torch.Size([1, 3, 4])
print(f)
# 输出：
# tensor([[[1, 1, 1, 1],
#          [2, 2, 2, 2],
#          [3, 3, 3, 3]]])

# 4. 错误示例（会报错）
g = torch.tensor([[1, 2], [3, 4]])  # shape: (2, 2)
# g.expand(2, 4)  # 报错！因为第二维是 2（不是 1），无法扩展到 4
```

**注意事项（陷阱）**

1. **共享内存（视图特性）**：因为返回的是视图，修改 `expand` 后的张量会影响原始数据！

   ```python
   x = torch.tensor([[1], [2]])
   y = x.expand(2, 3)
   y[0, 0] = 999
   print(x)  # 输出: tensor([[999], [2]]) —— 原始数据被修改了！
   ```

   如果你需要独立的数据副本，请务必在最后加上 `.clone()`，例如：`new_tensor = x.expand(2, 3).clone()`。

2. **与 `repeat` 的区别**：`repeat` 会**实际复制数据**并分配新内存（类似拷贝），而 `expand` 只是改变步长的视图。如果数据量巨大，优先使用 `expand` 来节省内存和计算时间。

3. **维度只能扩展为 1 的维度**：这是硬性规定，如果某个维度不是 1 且目标尺寸不相等，一定会抛出运行时错误。

### Tensor.expand_as

`expand_as` 是 PyTorch 中一个用于**广播**张量的方法，它可以将一个张量**在不复制数据**的情况下，扩展成与另一个张量相同的形状。

`expand_as` 的目标是让一个张量（我们称为 `A`）的形状变得与另一个张量（称为 `B`）完全相同。其用法非常简洁：

```python
A_expanded = A.expand_as(B)
```

这行代码的作用，**完全等同于** `A.expand(B.size())`。它返回的是原始张量 `A` 的一个**新视图（View）**。

**注意：**

- `expand_as` **不会复制原始数据**，而是创建一个新的张量视图。这个视图在底层通过设置步长（stride）为0来实现数据的“虚拟”扩展。
  - 由于是视图，对新张量的修改会**直接影响**原始张量。这个设计使得 `expand_as` 非常高效，尤其适合处理大张量。
- `expand_as` 的有效性取决于**广播规则**，核心限制是：**只能扩展原始张量中维度大小为 1 的维度**。非1的维度必须与目标张量的对应维度完全相等。
  - **可行示例**：形状为 `(3, 1)` 的张量可以成功扩展为 `(3, 4)`。
  - **不可行示例**：形状为 `(3, 2)` 的张量**无法**扩展为 `(4, 3)`，因为其第一维是3而非1，与目标的4不匹配。

**典型应用场景**

`expand_as` 在需要对不同形状的张量进行**逐元素操作**（如加法、乘法）前尤其有用。最常见的场景是在需要**广播**时，确保两个张量形状一致。

例如，我们有一个形状为 `(3, 1)` 的偏置向量，想将它加到形状为 `(3, 4)` 的特征矩阵上：

```python
import torch

# 特征矩阵 (3x4)
features = torch.randn(3, 4)
# 偏置向量 (3x1)
bias = torch.randn(3, 1)

# 将 bias 扩展成 (3x4)，然后与 features 相加
result = features + bias.expand_as(features)
print(result.shape)  # 输出: torch.Size([3, 4])
```

**`expand` vs. `expand_as` 对比**

| 特性         | `expand`                  | `expand_as`                                       |
| :----------- | :------------------------ | :------------------------------------------------ |
| **形状指定** | 手动传入目标尺寸 `*sizes` | 传入另一个张量 `other`，形状自动取 `other.size()` |
| **使用场景** | 明确知道想要变多大时      | 需要匹配某个现有张量的形状时                      |
| **本质关系** | 基础方法                  | 语法糖，等价于 `expand(other.size())`             |

## transpose

在 PyTorch 中，进行维度转置（Transpose）有多种方法。虽然它们都能改变数据的维度顺序，但在语义和适用场景上有所区别。

1. `torch.transpose(input, dim0, dim1)`

   这是最基础的转置函数。它**只能交换两个特定的维度**。
   - **语法**：`tensor.transpose(dim0, dim1)`
   - **适用场景**：经典的矩阵转置（行变列，列变行）。

   ```python
   import torch

   x = torch.randn(2, 3)  # 形状 (2, 3)
   y = x.transpose(0, 1)  # 形状 (3, 2)
   ```

2. `torch.permute(*dims)`

   这是在深度学习中最常用的函数。它可以**一次性重新排列所有维度**，比 `transpose` 更强大、更直观。
   - **语法**：`tensor.permute(dim0, dim1, dim2, ...)`
   - **适用场景**：改变图像张量的布局（例如从 `[通道, 高, 宽]` 转换为 `[高, 宽, 通度]`）。

   ```python
   # 假设有一个图像张量 (C, H, W)
   img = torch.randn(3, 224, 224)

   # 转换为 (H, W, C)，常用于绘图
   img_permuted = img.permute(1, 2, 0)
   ```

3. `tensor.T` (快捷属性)

   这是模仿 NumPy 的简洁写法。
   - **1D 张量**：返回自身。
   - **2D 张量**：等同于 `transpose(0, 1)`。
   - **高维张量**：在最新版本的 PyTorch 中，`.T` 会报错或警告（建议改用 `.mT` 处理最后两维，或用 `permute` 显式指定）。

   ```python
   x = torch.randn(2, 3)
   print(x.T.shape)  # torch.Size([3, 2])
   ```

4. 关键点：连续性 (Contiguous)

   转置操作**不会改变内存中数据的实际存储顺序**，它只是改变了“看数据的方式”（即步长 Stride）。

   这就引出了一个常见的坑：如果你在转置后紧接着使用 `view()`，程序会报错。

   > **解决方法**：在转置后调用 `.contiguous()`。

   ```python
   x = torch.randn(2, 3)
   y = x.transpose(0, 1).contiguous().view(-1) # 只有先 contiguous 才能 view
   ```

**核心方法对比表**

| 方法                  | 功能描述         | 优点                                |
| --------------------- | ---------------- | ----------------------------------- |
| `transpose(a, b)`     | 交换两个维度     | 简单，符合数学直觉                  |
| `permute(a, b, c...)` | 重新排列所有维度 | 灵活，处理高维数据必备              |
| `.T`                  | 2D 矩阵快速转置  | 书写极简                            |
| `.mT`                 | 批量矩阵转置     | 专门处理形如 `(Batch, N, M)` 的数据 |

## torch.argsort

`torch.argsort` 是 PyTorch 中非常实用的一个函数，它的核心作用是：**返回张量（Tensor）排序后的索引（Indices），而不是排序后的数值本身。**

当你需要知道"最小的元素在哪个位置"、"最大的元素在哪个位置"，或者需要根据某一个张量的顺序去调整另一个张量时，这个函数就派上用场了。

**核心参数介绍**

```python
torch.argsort(input, dim=-1, descending=False)
```

- **`input`** (Tensor)：输入的张量。
- **`dim`** (int, 可选)：沿着哪一个维度进行排序。默认是 `-1`（即最后一个维度）。
- **`descending`** (bool, 可选)：排序顺序。默认是 `False`（升序）；如果设置为 `True`，则按降序（从大到小）排序。

> 💡 **补充小知识**：`torch.argsort(x)` 实际上等价于 `torch.sort(x).indices`。

**示例：一维张量（1D Tensor）**

```python
import torch

# 创建一个无序的一维张量
x = torch.tensor([30, 10, 20, 50, 40])

# 进行升序 argsort
indices = torch.argsort(x)

print("原始张量 x:", x)
print("排序后的索引:", indices)
```

输出结果：

```log
原始张量 x: tensor([30, 10, 20, 50, 40])
排序后的索引: tensor([1, 2, 0, 4, 3])
```

**示例：二维张量与维度（2D Tensor & dim）**

在处理矩阵（二维张量）时，我们可以指定是"按行排序"还是"按列排序"。

```python
# 创建一个 2x3 的二维张量
y = torch.tensor([[5, 1, 3],
                  [9, 2, 6]])

# 1. 默认情况：dim=-1（在二维里等同于 dim=1，即每一行内部进行排序）
indices_row = torch.argsort(y, dim=1)

# 2. 降序排序：descending=True
indices_desc = torch.argsort(y, dim=1, descending=True)

# 3. 按列排序：dim=0（每一列内部进行纵向排序）
indices_col = torch.argsort(y, dim=0)

print("按行升序索引:\n", indices_row)
print("按行降序索引:\n", indices_desc)
print("按列升序索引:\n", indices_col)
```

输出结果：

```log
按行升序索引:
 tensor([[1, 2, 0],
        [1, 2, 0]])

按行降序索引:
 tensor([[0, 2, 1],
        [0, 2, 1]])

按列升序索引:
 tensor([[0, 0, 0],
        [1, 1, 1]])
```

二维结果解析：

- **按行升序 (`dim=1`)**：
  - 第一行 `[5, 1, 3]` 排序后是 `[1, 3, 5]`，它们原来的索引分别是 `[1, 2, 0]`。
  - 第二行 `[9, 2, 6]` 排序后是 `[2, 6, 9]`，它们原来的索引分别是 `[1, 2, 0]`。

- **按列升序 (`dim=0`)**：
  - 对比第一列 `[5, 9]`，5 比 9 小，所以索引顺序是 `[0, 1]`。
  - 对比第二列 `[1, 2]`，1 比 2 小，所以索引顺序是 `[0, 1]`。
  - 第三列同理。

**常见应用场景：根据索引重排张量**

`torch.argsort` 最强大的地方在于，你可以用它返回的索引去重新排列**另一个**相关的张量（通常配合 `torch.gather` 或直接切片使用）。

例如，你有同学的名字和他们的成绩，你想让名字按照成绩从高到低排列：

```python
names = ["Alice", "Bob", "Charlie", "David"]
scores = torch.tensor([85, 92, 78, 99])

# 获取成绩降序排列的索引
sort_indices = torch.argsort(scores, descending=True)
# sort_indices 结果为: tensor([3, 1, 0, 2])

# 根据索引重新排列名字（将 tensor 转为列表索引）
sorted_names = [names[i] for i in sort_indices]

print("成绩从高到低的名单:", sorted_names)
# 输出: ['David', 'Bob', 'Alice', 'Charlie']
```

## torch.where

`torch.where(condition, input, other, *, out=None) → Tensor`

Return a tensor of elements selected from either `input` or `other`, depending on `condition`.

The operation is defined as:

$$
\mathrm{out}_i=
\begin{cases}
\mathrm{input}_i        &
\text{if condition}_i   \\
\mathrm{other}_i        &
\mathrm{otherwise}      &
\end{cases}
$$

Note: The tensors `condition`, `input`, `other` must be [broadcastable](https://docs.pytorch.org/docs/2.13/notes/broadcasting.html#broadcasting-semantics).

## torch.lerp

`torch.lerp` 是 PyTorch 中用于执行**线性插值（Linear Interpolation）**的函数。它的核心作用是在两个张量之间，根据一个权重值进行逐元素的混合。

**数学定义**

对于每个位置的元素，`torch.lerp` 执行的计算公式如下：

$$ output=start+weight×(end−start) $$

或者等价地写作：

$$ output=(1−weight)×start+weight×end $$

- 当 `weight = 0` 时，输出完全等于 `start`。
- 当 `weight = 1` 时，输出完全等于 `end`。
- 当 `weight = 0.5` 时，输出是 `start` 和 `end` 的中点（平均值）。

**函数签名与参数**

```python
torch.lerp(input, end, weight, *, out=None)
```

| 参数     | 说明                                                                                                                   |
| :------- | :--------------------------------------------------------------------------------------------------------------------- |
| `input`  | 起始张量（起点）。                                                                                                     |
| `end`    | 结束张量（终点）。                                                                                                     |
| `weight` | 插值权重。可以是一个**标量**（`float`），也可以是一个与 `input`/`end` **形状相同**的张量（允许逐元素设置不同的权重）。 |
| `out`    | （可选）用于指定输出张量。                                                                                             |

1. **逐元素计算**：`input` 和 `end` 必须满足**广播规则**（Broadcastable）。如果形状不一致，PyTorch 会自动尝试广播。
2. **支持逐元素权重**：`weight` 也可以是一个张量，这允许你对张量中不同的位置施加不同的插值进度（例如，对图像的上半部分用 0.2，下半部分用 0.8）。
3. **数据类型**：要求 `input` 和 `end` 为浮点数（Float）或复数类型。整数类型（如 `int`）会报错，因为插值结果往往是小数。
4. **原地操作**：有对应的原地操作版本 **`torch.lerp_()`**，会直接修改 `input` 张量，节省内存。

**代码示例**

1. 基础使用（标量权重）

   将两个向量按 30% 和 70% 的比例混合：

   ```python
   import torch

   start = torch.tensor([1.0, 2.0, 3.0])
   end = torch.tensor([4.0, 5.0, 6.0])

   # 权重 0.3：结果 = start * 0.7 + end * 0.3
   result = torch.lerp(start, end, 0.3)
   print(result)  # 输出: tensor([1.9000, 2.9000, 3.9000])
   # 计算验证: 1.0 + 0.3*(4.0-1.0) = 1.9
   ```

2. 广播机制

   起始值是单行，结束值是多行，PyTorch 会自动广播起始行：

   ```python
   start = torch.tensor([[1.0, 2.0]])  # shape: (1, 2)
   end = torch.tensor([[3.0, 4.0], [5.0, 6.0]])  # shape: (2, 2)

   result = torch.lerp(start, end, 0.5)
   print(result)
   # 输出:
   # tensor([[2.0000, 3.0000],   # (1+3)/2, (2+4)/2
   #         [3.0000, 4.0000]])  # (1+5)/2, (2+6)/2
   ```

3. 张量作为权重（逐元素不同权重）

   这在需要对不同像素或通道区别对待时非常有用：

   ```python
   start = torch.tensor([1.0, 2.0, 3.0])
   end = torch.tensor([4.0, 5.0, 6.0])
   weights = torch.tensor([0.1, 0.5, 0.9])

   result = torch.lerp(start, end, weights)
   print(result)  # 输出: tensor([1.3000, 3.5000, 5.7000])
   ```

**常见应用场景（非常实用）**

1. **深度学习中的模型指数移动平均（EMA）**
   在训练时更新影子权重（Shadow Weights）：

   ```python
   # shadow = shadow * decay + param * (1 - decay)
   # 等价于 lerp 从 param 插值到 shadow，权重为 decay
   shadow_weights = torch.lerp(param, shadow_weights, decay)
   ```

2. **图像混合（Cross-fading / Alpha Blending）**
   将两张图片按透明度 `alpha` 混合：

   ```python
   blended = torch.lerp(image1, image2, alpha)
   ```

3. **渲染中的射线步进（Ray Marching）**
   在两点之间平滑移动物体或摄像机位置。

4. **数据增强（MixUp）**
   在训练分类模型时，将两张图片和它们的标签按比例混合。

**注意事项（踩坑提醒）**

- **整数报错**：如果 `start` 是 `torch.tensor([1, 2, 3])`（整型），会直接报错。**务必先转换为 `.float()`**。
- **`weight` 超出 [0, 1] 范围**：`torch.lerp` **不会**钳制（Clamp）权重！如果 `weight=2.0`，结果会外推（Extrapolate）到 `end` 范围之外（即 `2*end - start`）。如果你需要严格限制在 0~1 之间，请先执行 `weight = weight.clamp(0, 1)`。
- **内存与视图**：`torch.lerp` 会**分配新内存**。如果你在循环中反复调用（例如 EMA 更新），建议使用 **`torch.lerp_()`**（原地操作）来避免内存暴涨，提升性能。

总结：`torch.lerp` 是一个极其干净、高效的张量混合工具，掌握它可以让你在各种数值计算和模型训练技巧中事半功倍。如果你还想了解它与 `torch.nn.functional.interpolate`（用于缩放图像）的区别，随时可以问我！😄
