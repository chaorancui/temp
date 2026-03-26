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

## transpose 函数

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
