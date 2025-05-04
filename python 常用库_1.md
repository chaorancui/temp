[toc]

# python 数据科学和机器学习库

## 参考链接

[1]. [数据科学和机器学习](https://mlhowto.readthedocs.io/en/latest/index.html)
[2]. [NumPy reference](https://numpy.org/doc/stable/reference/index.html#reference)

## numpy 模块

> [数据科学和机器学习](https://mlhowto.readthedocs.io/en/latest/index.html)

### NumPy 标准数据类型

NumPy 支持比 Python 更多种类的数值类型。 下表显示了 NumPy 中定义的不同标量数据类型。

| 数据类型   | 说明                                                             |
| :--------- | :--------------------------------------------------------------- |
| bool       | 布尔类型，True 或者 False。                                      |
| bool\_     | 布尔值（真、 True 或假、 False） ， 用一个字节存储               |
| int\_      | 默认整型（类似于 C 语言中的 long， 通常情况下是 int64 或 int32） |
| intc       | 与 C 语言的 int 类型一致，一般是 int32 或者 int64                |
| intp       | 用于索引的整数，与 C 预言中的 ssize_t 一致，int32 或者 int64     |
| int8       | 字节长度的整数，取值：[-128, 127]                                |
| int16      | 16 位长度的整数，取值：[-32768, 32767]                           |
| int32      | 32 位长度的整数，取值：[-2^31, 2^31-1]                           |
| int64      | 64 位长度的整数，取值：[-2^^63, 2^63-1]                          |
| uint8      | 8 位无符号整数，取值：[0, 255]                                   |
| uint16     | 16 位无符号整数，取值：[0, 65535]                                |
| uint32     | 32 位无符号整数，取值：[0, 2^32-1]                               |
| uint64     | 64 位无符号整数，取值：[0, 2^64-1]                               |
| float16    | 16 位半精度浮点数：1 位符号位，5 位指数，10 位尾数               |
| float32    | 32 位半精度浮点数：1 位符号位，8 位指数，23 位尾数               |
| float64    | 64 位半精度浮点数：1 位符号位，11 位指数，52 位尾数              |
| float      | float64 的简化形式                                               |
| float\_    | float64 的简化形式                                               |
| complex64  | 复数类型，实部和虚部都是 32 位浮点数                             |
| complex128 | 复数类型，实部和虚部都是 64 位浮点数                             |

浮点数：（符号）尾数\*10 指数；
复数：实部(.real)+虚部 i（.imag）；

NumPy 数字类型是`dtype`（数据类型）对象的实例，每个对象具有唯一的特征。 这些类型可以是`np.bool_`，`np.float32`等。

### NumPy 数组内存布局

[ndarray.flags](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.flags.html#numpy.ndarray.flags)

要打印 NumPy 数组的内存排布，可以使用数组对象的 `flags` 属性。`flags` 包含了有关数组内存布局的各种信息，包括是否是连续的内存布局（C-连续或 F-连续）、是否可写、是否拥有自己的数据等。

以下是如何读取 `.npy` 文件并查看其内存排布的示例：

```python
import numpy as np

# 读取 .npy 文件
array = np.load('文件路径.npy')

# 打印内存排布信息
print(array.flags)
```

输出

```shell
  C_CONTIGUOUS : True
  F_CONTIGUOUS : False
  OWNDATA : True
  WRITEABLE : True
  ALIGNED : True
  WRITEBACKIFCOPY : False
  UPDATEIFCOPY : False
```

**解释**：

- **C_CONTIGUOUS**：如果数组按 C 语言中的行优先顺序存储（即一行的元素连续存储），则为 `True`。
- **F_CONTIGUOUS**：如果数组按 Fortran 语言中的列优先顺序存储（即一列的元素连续存储），则为 `True`。
- **OWNDATA**：如果数组拥有自己的数据（而不是视图或切片），则为 `True`。
- **WRITEABLE**：如果数组是可写的，则为 `True`。
- **ALIGNED**：如果数组数据在内存中是按照要求对齐的，则为 `True`。
- **WRITEBACKIFCOPY** 和 **UPDATEIFCOPY**：用于管理写时复制的高级选项，通常情况下是 `False`。

通过 `flags`，你可以清楚地了解数组在内存中的排布情况。

:book: **扩展内容**：
通常情况下：

- **`C_CONTIGUOUS` 为 `True`** 表示数组是按照 C 语言的行优先顺序存储（行主序），即一行的数据在内存中是连续存储的。
- **`F_CONTIGUOUS` 为 `True`** 表示数组是按照 Fortran 的列优先顺序存储（列主序），即一列的数据在内存中是连续存储的。

然而，某些情况下，数组可能同时是 C 连续的和 Fortran 连续的，这通常发生在 **数组是一维数组** 或者 **数组的形状使得行和列的存储顺序一致时**。如：

1. **一维数组的特殊情况**：

   对于一维数组，内存中的存储是线性的，不存在行或列的概念。因此，无论是按行（C）还是按列（Fortran），其内存存储方式都是连续的。在这种情况下，`C_CONTIGUOUS` 和 `F_CONTIGUOUS` 都会返回 `True`。

   ```python
   import numpy as np
   arr = np.array([1, 2, 3, 4, 5])  # 一维数组
   print(arr.flags)
   ```

2. **二维数组的特殊情况**：

   如果一个二维数组的形状为 `(1, n)` 或者 `(n, 1)`（即单行或单列的情况），也会出现同时是 C 连续和 Fortran 连续的情况，因为内存中的数据也是线性的。

   ```python
   import numpy as np
   arr = np.array([[1, 2, 3, 4]])  # 只有一行
   print(arr.flags)
   ```

总结

当数组是 **一维** 或 **二维并且行或列长度为 1** 时，数组内存的存储顺序在行优先和列优先的情况下都是连续的，因此 `C_CONTIGUOUS` 和 `F_CONTIGUOUS` 都会同时为 `True`。这种现象是正常的。

### 数组转换为字符串

`numpy.array2string` 是一个非常灵活的函数，它可以将 NumPy 数组转换为字符串，并且提供了很多选项来控制输出格式。

```python
numpy.array2string(a, max_line_width=None, precision=None, suppress_small=None, separator=' ', prefix='', style=<no value>, formatter=None, threshold=None, edgeitems=None, sign=None, floatmode=None, suffix='', *, legacy=None)
```

**参数说明**：

- **a**: 输入的 NumPy 数组。
- **max_line_width**: 每行的最大字符宽度。如果超过这个宽度，数组会换行。
- **precision**: 浮点数的精度。
- **suppress_small**: 如果为 True，小的浮点数会打印为 0。
- **separator**: 元素之间的分隔符。
- **prefix**: 每行的前缀。
- **formatter**: 一个字典，用于指定不同类型元素的格式。
- **threshold**: 总元素个数的阈值，超过这个值时数组会使用省略号进行简化。
- **edgeitems**: 边缘元素的数量。
- **sign**: 控制符号的显示，可以是 `+` 或者 `-`。
- **floatmode**: 控制浮点数的显示模式，可以是 `maxprec`, `fixed`, `unique`, `maxprec_equal`。
- **suffix**: 每行的后缀。
- **legacy**: 控制旧版格式输出。

### numpy 实现 reinterpret cast

在 `numpy` 中，`astype` 方法用于转换数组的数据类型。`>i4` 是一种数据类型描述符，其中：

- `>` 表示大端字节序
- `i` 表示整数类型（signed integer）
- `4` 表示 4 字节（32 位）

除了 `i` 以外，还有很多其他类型描述符，可以用来表示不同的数据类型。以下是一些常用的数据类型描述符：

常用的数据类型描述符

#### 整数类型

- `i`：有符号整数（signed integer）
  - `i1`：1 字节（8 位）
  - `i2`：2 字节（16 位）
  - `i4`：4 字节（32 位）
  - `i8`：8 字节（64 位）
- `u`：无符号整数（unsigned integer）
  - `u1`：1 字节（8 位）
  - `u2`：2 字节（16 位）
  - `u4`：4 字节（32 位）
  - `u8`：8 字节（64 位）

#### 浮点类型

- `f`：浮点数（floating point）
  - `f2`：2 字节（16 位）半精度浮点数
  - `f4`：4 字节（32 位）单精度浮点数
  - `f8`：8 字节（64 位）双精度浮点数

#### 复数类型

- `c`：复数（complex number）
  - `c8`：8 字节（32 位实数和 32 位虚数）
  - `c16`：16 字节（64 位实数和 64 位虚数）

#### 字节序前缀

- `>`：大端字节序（big-endian）
- `<`：小端字节序（little-endian）
- `=`：原生字节序（native endian，依赖于主机系统）
- `|`：不考虑字节序（not applicable）

示例

```python
import numpy as np

# 创建一个示例数组
arr = np.array([1, 2, 3, 4])

# 转换为大端 32 位有符号整数
arr_big_endian_i4 = arr.astype('>i4')
print("Big-endian 32-bit signed integer:", arr_big_endian_i4.dtype)

# 转换为小端 16 位无符号整数
arr_little_endian_u2 = arr.astype('<u2')
print("Little-endian 16-bit unsigned integer:", arr_little_endian_u2.dtype)

# 转换为大端 64 位浮点数
arr_big_endian_f8 = arr.astype('>f8')
print("Big-endian 64-bit float:", arr_big_endian_f8.dtype)

# 转换为小端 32 位复数
arr_little_endian_c8 = arr.astype('<c8')
print("Little-endian 32-bit complex:", arr_little_endian_c8.dtype)
```

输出：

```python
Big-endian 32-bit signed integer: >i4
Little-endian 16-bit unsigned integer: <u2
Big-endian 64-bit float: >f8
Little-endian 32-bit complex: <c8
```

自己实现的转换函数：

```python
import numpy as np

def reinterpret_int64_to_float1632(input_arr, float_type):
    assert isinstance(input_arr, np.ndarray), f"input_arr({type(input_arr)}) only support numpy ndarray, please convert!"
    assert input_arr.dtype == "int64", f"the data type({input_arr.dtype}) of input_arr is not int64, please convert using .astype function!"
    assert float_type == "float16" or float_type == "float32", f"float_type({float_type}) only support float16 or float32, please check input param float_type!"
    byte_data = input_arr.tobytes()
    element_size = input_arr.itemsize

    # 计算字节流包含元素个数，numpy也可以用
    # num_elements = input_arr.size
    num_elements = len(byte_data) // element_size

    # 创建一个 NumPy 数组来存储结果
    result = np.array([]).astype(float_type)

    if float_type == "float32":
        float_element_size = 4
    else:
        float_element_size = 2
    # 遍历每个元素并【截取】前2或4个字节转换成float
    for i in range(num_elements):
        start_idx = i * element_size
        end_idx = start_idx + float_element_size
        result = np.append(result, np.frombuffer(byte_data[start_idx:end_idx], dtype=float_type))

    return result

arr = np.array([114, 114, 114, 114])
result = reinterpret_int64_to_float1632(arr, "float16")
print(f"原始数组：{arr}")
print(f"int 转 float16: {result}")


def reinterpret_float1632_to_int64(input_arr, int_type="int64"):
    assert isinstance(input_arr, np.ndarray), f"input_arr({type(input_arr)}) only support numpy ndarray, please convert!"
    assert input_arr.dtype == "float16" or input_arr.dtype == "float32", f"the data type({input_arr.dtype}) of input_arr only support float16 or float32, please check input param int_type!"
    assert int_type == "int64", f"int_type({int_type}) only support int64, please convert using .astype function!"
    byte_data = input_arr.tobytes()
    element_size = input_arr.itemsize

    # 计算字节流包含元素个数，numpy也可以用
    # num_elements = input_arr.size
    num_elements = len(byte_data) // element_size

    # 创建一个 NumPy 数组来存储结果
    result = np.array([]).astype(int_type)

    if input_arr.dtype == "float32":
        padding_length = 4
    else:
        padding_length = 6
    # 遍历每个元素并【填充】6个或4个字节转换成int64
    for i in range(num_elements):
        start_idx = i * element_size
        end_idx = (i + 1) * element_size
        byte_stream_tmp = byte_data[start_idx:end_idx] + b'\x00' * padding_length
        result = np.append(result, np.frombuffer(byte_stream_tmp, dtype=int_type))

    return result

arr1 = np.array([6.8e-06, 6.8e-06, 6.8e-06, 6.8e-06]).astype("float16")
result1 = reinterpret_float1632_to_int64(arr1)
print(f"原始数组：{arr1}")
print(f"float16 转 int64: {result1}")


# 将数字转换为为二进制表示
def print_binary_representation(input_arr):
    assert isinstance(input_arr, np.ndarray), f"input_arr({type(input_arr)}) only support numpy ndarray, please convert!"
    assert input_arr.dtype == "float16" or input_arr.dtype == "float32" or input_arr.dtype == "int64", \
        f"the data type({input_arr.dtype}) of input_arr only support float16 or float32 or int64, please check input param input_dtype!"

    if input_arr.dtype == "int64":
        byte_stream_flag = ">u8"
    elif input_arr.dtype == "float32":
        byte_stream_flag = ">f4"
    elif input_arr.dtype == "float16":
        byte_stream_flag = ">f2"

    byte_data = input_arr.astype(byte_stream_flag).tobytes()
    element_size = input_arr.itemsize

    # 计算字节流包含元素个数，numpy也可以用
    # num_elements = input_arr.size
    num_elements = len(byte_data) // element_size

    result = []

    for i in range(num_elements):
        start_idx = i * element_size
        end_idx = (i + 1) * element_size
        element_byte_stream = byte_data[start_idx:end_idx]
        binary_representation = "".join(f"{byte:08b}" for byte in element_byte_stream)
        result.append(binary_representation)

    return result

# 打印二进制表示
float_value = np.array([6.8e-06]).astype(np.float16)
binary_representation = print_binary_representation(float_value)
print(f"整数数 {float_value[0]:<10} 的二进制表示: {binary_representation},  长度：{[len(item) for item in binary_representation]}")


int_value = np.array([114]).astype(np.int64)
binary_representation = print_binary_representation(int_value)
print(f"整数数 {int_value[0]:<10} 的二进制表示: {binary_representation}, 长度：{[len(item) for item in binary_representation]}")
```

### 随机数生成

#### 基本随机数生成

- `numpy.random.rand(d0, d1, ..., dn)`
  生成指定形状的随机样本，样本值均在 0 到 1 的区间内（均匀分布）。

  ```python
  import numpy as np
  random_array = np.random.rand(3, 2)  # 生成3x2的二维数组，值在[0, 1)之间
  ```

- `numpy.random.randn(d0, d1, ..., dn)`
  生成指定形状的样本，样本值符合标准正态分布（均值为 0，标准差为 1）。

  ```python
  random_array = np.random.randn(3, 2)  # 生成3x2的二维数组，值符合标准正态分布
  ```

- `numpy.random.randint(low, high=None, size=None, dtype=int)`
  返回随机整数或随机整数数组，范围为[low, high)。如果只给出 low，则返回[0, low)的随机整数。

  ```python
  random_int = np.random.randint(1, 10, size=5)  # 生成5个1到9之间的随机整数
  ```

#### 特定分布的随机数生成

- `numpy.random.uniform(low=0.0, high=1.0, size=None)`
  从均匀分布[low, high)中生成随机数。

  ```python
  random_uniform = np.random.uniform(1, 10, size=(3, 2))  # 生成3x2的数组，值在[1, 10)之间
  ```

- `numpy.random.normal(loc=0.0, scale=1.0, size=None)`
  从正态分布（高斯分布）中生成随机数，loc 为均值，scale 为标准差。

  ```python
  random_normal = np.random.normal(0, 1, size=5)  # 生成5个均值为0，标准差为1的随机数
  ```

- `numpy.random.binomial(n, p, size=None)`
  从二项分布中生成随机数。n 是试验次数，p 是每次试验成功的概率。

  ```python
  random_binomial = np.random.binomial(10, 0.5, size=5)  # 生成5个二项分布样本，10次试验成功概率0.5
  ```

- `numpy.random.poisson(lam=1.0, size=None)`
  从泊松分布中生成随机数，lam 为事件的平均发生次数。

  ```python
  random_poisson = np.random.poisson(5, size=5)  # 生成5个泊松分布样本，平均事件发生次数为5
  ```

- `numpy.random.exponential(scale=1.0, size=None)`
  从指数分布中生成随机数，scale 为 $ \tfrac{1}{\lambda} $，即事件的平均发生间隔。

  ```python
  random_exponential = np.random.exponential(1, size=5)  # 生成5个指数分布样本，平均间隔为1
  ```

#### 其他随机数生成函数

- `numpy.random.choice(a, size=None, replace=True, p=None)`
  从一维数组 a 中随机抽取样本。replace 表示是否有放回地抽样，p 为每个元素被抽取的概率。

  ```python
  elements = ['a', 'b', 'c', 'd']
  random_choice = np.random.choice(elements, size=3, replace=False)  # 从elements中不放回抽取3个元素
  ```

- `numpy.random.shuffle(x)`
  对序列 x 进行就地随机打乱。

  ```python
  arr = np.array([1, 2, 3, 4, 5])
  np.random.shuffle(arr)  # 打乱数组arr
  ```

- `numpy.random.permutation(x)`
  返回序列 x 的随机排列，不会修改原序列。

  ```python
  arr = np.array([1, 2, 3, 4, 5])
  permuted_arr = np.random.permutation(arr)  # 生成arr的一个随机排列
  ```

#### 随机数生成器控制

- `numpy.random.seed(seed)`
  设置随机数生成器的种子，保证每次运行结果一致。

  ```python
  np.random.seed(42)  # 设置随机种子
  ```

这些函数使得 NumPy 在数据分析、机器学习等领域中非常方便地进行随机数生成和模拟实验。根据不同的需求，可以选择合适的分布和函数来生成随机数。

### `.npy` 文件

文件扩展名 `.npy` 是 NumPy 二进制文件格式的默认扩展，用于高效地存储 NumPy 数组，可以使用 `numpy.save` 和 `numpy.load` 来读写二进制文件。

与常见的文本文件（如 `.csv`）不同，`.npy` 是二进制文件，保存了数组的形状、数据类型以及实际的数据内容，因此比普通的文本格式更快、更节省空间。

下面是一个示例代码，演示如何读取和保存 `.npy` 文件：

#### 打开并读取 `.npy` 文件

```python
import numpy as np

# 读取 .npy 文件
array = np.load('文件路径.npy')

# 查看读取的数组
print(array)

# 输出数据的形状和数据类型
print("数据形状:", array.shape)
print("数据类型:", array.dtype)
print(f"name: {str('文件路径.npy')+',':<20} dtype: {str(array.dtype)+',':<10} shape: {str(array.shape)+',':<15} nbytes: {str(array.nbytes)+',':<15}")
# 打印内存排布信息
print(array.flags)
```

使用 NumPy 加载 `.npy` 文件时会**自动识别数据的形状和类型**，因此只需要指定文件路径即可。

#### 保存数组为 `.npy` 文件

```python
import numpy as np

# 创建一个 NumPy 数组
array = np.array([1, 2, 3, 4, 5])

# 保存为 .npy 文件
np.save('文件路径.npy', array)
```

### `.npz` 文件

`.npz` 文件是 NumPy 的一种用于存储多个数组的压缩文件格式。使用 `.npz` 文件可以将多个 NumPy 数组保存到一个文件中，方便数据的组织和管理。每个数组在 `.npz` 文件中都会以键值对的形式存储，可以单独读取其中的每个数组。

#### 保存多个数组到 `.npz` 文件

可以使用 `numpy.savez` 或 `numpy.savez_compressed` 保存多个数组。`savez_compressed` 会进行压缩，可以减小文件大小。

- **`numpy.savez`**：保存多个数组，不进行压缩。
- **`numpy.savez_compressed`**：保存多个数组，并进行压缩。

**示例**：

```python
import numpy as np

# 创建多个示例数组
array1 = np.array([1, 2, 3])
array2 = np.array([[4, 5, 6], [7, 8, 9]])

# 保存为 .npz 文件
np.savez("arrays.npz", arr1=array1, arr2=array2)

# 保存为压缩的 .npz 文件
np.savez_compressed("arrays_compressed.npz", arr1=array1, arr2=array2)
```

#### 从 `.npz` 文件读取数据

可以使用 `numpy.load` 函数加载 `.npz` 文件，并通过键名访问其中的每个数组。加载后的 `.npz` 文件是一个类似字典的对象，可以通过数组的键名访问。

**示例**：

```python
import numpy as np

# 加载 .npz 文件
data = np.load("arrays.npz")

# 访问其中的数组
array1 = data['arr1']
array2 = data['arr2']

print("array1:", array1)
print("array2:", array2)
```

#### `.npz` 文件的优点

1. **便捷**：可以将多个数组存储在一个文件中，便于组织。
2. **压缩**：可以选择压缩文件，减少磁盘空间使用。
3. **快速访问**：加载 `.npz` 文件不需要解压，可以快速访问其中的每个数组。

`.npz` 文件是保存和管理多个数组的好方法，尤其适合需要经常读取的大规模数据。

### `.bin` 文件

`.bin` 文件通常是指包含二进制数据的文件，未指定特定格式。与 `.npy` 或 `.npz` 文件不同，**`.bin` 文件不包含任何元数据（例如数组的形状、数据类型等），只包含原始的二进制数据**。因此，`.bin` 文件在读取和写入时，需要提前知道数据的格式（形状和数据类型），并手动指定这些信息。

#### 保存数组到 `.bin` 文件

可以使用 `numpy.ndarray.tofile` 方法将 NumPy 数组直接保存为 `.bin` 文件：

```python
import numpy as np

# 创建数组
array = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int32)

# 保存为 .bin 文件
array.tofile("array_data.bin")
```

**说明**：

- `tofile` 方法会将数组按顺序保存为二进制数据，不包含任何关于数组的形状、数据类型等元信息。
- 可以通过指定 `dtype`，来选择要保存的数据类型，例如 `np.int32`, `np.float64` 等。

#### 从 `.bin` 文件读取数据

使用 `numpy.fromfile` 方法从 `.bin` 文件中读取数据：

```python
import numpy as np

# 从 .bin 文件中读取数据，指定数据类型
loaded_array = np.fromfile("array_data.bin", dtype=np.int32)

# 如果需要，还可以手动指定形状
loaded_array = loaded_array.reshape((2, 3))

print("读取的数组：")
print(loaded_array)
```

**说明**：

- `fromfile` 函数加载二进制文件，需要手动指定数据类型（如 `np.int32`）。
- 如果文件中存储的是多维数组数据，加载后需用 `.reshape` 方法手动恢复原始形状。

#### `.bin` 文件的优缺点

- **优点**：
  - 文件简单，保存和读取效率高，适合保存大量的数据（如图像、音频信号等）。
  - 可以使用任意编程语言读取和写入（只要知道数据格式）。
- **缺点**：
  - 没有元数据，无法记录数据的形状、数据类型等信息。
  - 读取数据时需要事先知道数据格式（如数据类型、数组形状）。

`.bin` 文件适合简单、高效的数据存储应用，但由于缺少元信息，不适合复杂的数据结构保存。例如，需要保存多个数组或需要在数据中记录元信息时，`.npz` 文件更合适。

### `.txt` 输出原始数据

在 NumPy 中，可以使用 `numpy.savetxt` 函数将 `ndarray` 的值格式化输出到文本文件中。`savetxt` 允许我们指定文件名、分隔符以及数据格式，非常灵活。

1. **使用 `numpy.savetxt` 保存数组到文本文件**

   ```shell
   numpy.savetxt(fname, X, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None)
   ```

   `numpy.savetxt` 的主要参数如下：

   - `fname`：文件名，或者文件对象。
   - `X`：要保存的数组。
   - `fmt`：数据格式，默认是 `'%.18e'`，支持以下格式化控制。可以指定不同的格式化字符串，如 `'%.2f'`（保留两位小数）。
     Further explanation of the _fmt_ parameter (`%[flag]width[.precision]specifier`):

     - flags:

       `-` : left justify
       `+` : Forces to precede result with + or -.
       `0` : Left pad the number with zeros instead of space (see width).

     - width:

       Minimum number of characters to be printed. The value is not truncated if it has more characters.

     - precision:

       For integer specifiers (eg. `d,i,o,x`), the minimum number of digits.
       For `e, E` and `f` specifiers, the number of digits to print after the decimal point.
       For `g` and `G`, the maximum number of significant digits.
       For `s`, the maximum number of characters.

     - specifiers:

       `c` : character
       `d` or `i` : signed decimal integer
       `e` or `E` : scientific notation with `e` or `E`.
       `f` : decimal floating point
       `g,G` : use the shorter of `e,E` or `f`
       `o` : signed octal
       `s` : string of characters
       `u` : unsigned decimal integer
       `x,X` : unsigned hexadecimal integer

   - `delimiter`：分隔符，**默认是空格**，可以设定为逗号、制表符等。仅对于二维数组生效，一维数组需要 `reshape(1, -1)`。
   - `newline`：换行符，分隔行的字符串或字符。**默认是换行**。
   - `header`标题，将写入文件开头的字符串。。
   - `footer`：页脚，将被写入文件末尾的字符串。。
   - `comments`：评论，将被添加到 header 和 footer 字符串前面的字符串，以将它们标记为注释。**默认值：'#'**。
   - `encoding`：编码，用于对输出文件进行编码的编码。不适用于输出流。。
     **示例代码**：

   ```python
   import numpy as np

   # 创建一个数组
   array = np.array([[1.23456, 2.34567, 3.45678], [4.56789, 5.67890, 6.78901]])

   # 保存到文本文件，格式化为小数点后两位，逗号分隔
   np.savetxt("array_data.txt", array, fmt="%10.4f", delimiter=",")
   np.savetxt("array_data_1d.txt", array.reshape(1, -1), fmt="%f", delimiter=',', newline=' ') # delimiter 仅对二维数组有效，因此 reshape(1, -1)
   print(f"{'array:': <15} shape: {str(array.shape)+',': <20} nbytes: {str(array.nbytes)+',': <10} dtype: {str(array.dtype)+',': <10}")
   ```

   **大于 2 维的数组写入文件函数**：

   ```python
   def save_to_txt(input_array, file_name):
       dims = input_array.shape
       dim_num = len(dims)
       # 1、只支持 <= 4 维数据写入文件
       assert dim_num <= 4, f"input_array's shape({dim_num})is larger than 4, not supported!!"
       # 2、<= 2 维的数据直接写入
       if dim_num <= 2:
           with open(file_name, 'w') as f:
               f.write(f"dims: {dims}\n")
               np.savetxt(f, input_array, fmt="%-10.4f", delimiter=",")
           print(f"数组已保存至: {file_name}")
           return
       # 3、2 < dim_num <= 4 维的数据循环写入
       with open(file_name, 'w') as f:
           f.write(f"dims: {dims}\n")
           loop_arr = dims[0:-2] # 包含多少个二维数组
           ranges = [] # 生成循环索引
           for i in loop_arr:
               ranges.append(range(i))
           print(ranges)
           for indices in itertools.product(*ranges):
               idx = list(indices) # .extend([slice(None), slice(None)])
               idx.extend([slice(None), slice(None)])
               # print(input_array[tuple(idx)])
               np.savetxt(f, input_array[tuple(idx)], fmt="%-10.4f", delimiter=",")

   save_to_txt(arr_hw, "formatted_array.txt")
   ```

2. **使用 `numpy.array2string` 将数组格式化为字符串（不保存文件）**

   如果希望将 `ndarray` 转换为字符串格式，可以使用 `numpy.array2string`：

   > 注：跟直接 print 到屏幕一样，输出长内容会隐藏内容

   ```python
   import numpy as np

   # 创建一个数组
   array = np.array([[1.23456, 2.34567, 3.45678], [4.56789, 5.67890, 6.78901]])

   # 转换为字符串格式，保留两位小数
   array_str = np.array2string(array, precision=2, separator=",")
   print("格式化后的数组字符串：")
   print(array_str)
   ```

**总结**：

- **保存到文本文件**：使用 `numpy.savetxt`，可以指定格式和分隔符。
- **转换为字符串**：使用 `numpy.array2string`，灵活控制精度和分隔符。

## argparse 库

`argparse` 是 Python 中用于处理命令行参数的标准库，它允许你轻松地定义和解析程序运行时的命令行参数。通过它，你可以设置程序需要的输入参数、指定参数的类型、默认值等，并且自动生成帮助文档。

[argparse 官方 python 文档](https://docs.python.org/zh-cn/3.13/library/argparse.html)

**一、`argparse` 库使用格式**

1. **创建 ArgumentParser 对象**

   ```python复制编辑import argparse
   class argparse.ArgumentParser(prog=None, usage=None, description=None, epilog=None, parents=[], formatter_class=argparse.HelpFormatter, prefix_chars='-', fromfile_prefix_chars=None, argument_default=None, conflict_handler='error', add_help=True, allow_abbrev=True, exit_on_error=True)
   ```

   创建一个新的 [`ArgumentParser`](https://docs.python.org/zh-cn/3.13/library/argparse.html#argparse.ArgumentParser) 对象。所有的参数都应当作为关键字参数传入。每个参数在下面都有它更详细的描述，但简而言之，它们是：

   - [prog](https://docs.python.org/zh-cn/3.13/library/argparse.html#prog) - 程序的名称 (默认值: `os.path.basename(sys.argv[0])`)
   - [usage](https://docs.python.org/zh-cn/3.13/library/argparse.html#usage) - 描述程序用途的字符串（默认值：从添加到解析器的参数生成）
   - [description](https://docs.python.org/zh-cn/3.13/library/argparse.html#description) - 要在参数帮助信息之前显示的文本（默认：无文本）
   - [epilog](https://docs.python.org/zh-cn/3.13/library/argparse.html#epilog) - 要在参数帮助信息之后显示的文本（默认：无文本）
   - [parents](https://docs.python.org/zh-cn/3.13/library/argparse.html#parents) - 一个 [`ArgumentParser`](https://docs.python.org/zh-cn/3.13/library/argparse.html#argparse.ArgumentParser) 对象的列表，它们的参数也应包含在内
   - [formatter_class](https://docs.python.org/zh-cn/3.13/library/argparse.html#formatter-class) - 用于自定义帮助文档输出格式的类
   - [prefix_chars](https://docs.python.org/zh-cn/3.13/library/argparse.html#prefix-chars) - 可选参数的前缀字符集合（默认值： '-'）
   - [fromfile_prefix_chars](https://docs.python.org/zh-cn/3.13/library/argparse.html#fromfile-prefix-chars) - 当需要从文件中读取其他参数时，用于标识文件名的前缀字符集合（默认值： `None`）
   - [argument_default](https://docs.python.org/zh-cn/3.13/library/argparse.html#argument-default) - 参数的全局默认值（默认值： `None`）
   - [conflict_handler](https://docs.python.org/zh-cn/3.13/library/argparse.html#conflict-handler) - 解决冲突选项的策略（通常是不必要的）
   - [add_help](https://docs.python.org/zh-cn/3.13/library/argparse.html#add-help) - 为解析器添加一个 `-h/--help` 选项（默认值： `True`）
   - [allow_abbrev](https://docs.python.org/zh-cn/3.13/library/argparse.html#allow-abbrev) - 如果缩写是无歧义的，则允许缩写长选项 （默认值：`True`）
   - [exit_on_error](https://docs.python.org/zh-cn/3.13/library/argparse.html#exit-on-error) - 确定当出现错误时，`ArgumentParser` 是否退出并显示错误信息。（默认值:`True`）

2. **添加参数**

   ```python
   ArgumentParser.add_argument(name or flags..., *[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest][, deprecated])
   ```

   定义单个的命令行参数应当如何解析。每个形参都在下面有它自己更多的描述，长话短说有：

   - [name or flags](https://docs.python.org/zh-cn/3.13/library/argparse.html#name-or-flags) - 一个名称或是由选项字符串组成的列表，例如 `'foo'` 或 `'-f', '--foo'`。
   - [action](https://docs.python.org/zh-cn/3.13/library/argparse.html#action) - 当参数在命令行中出现时使用的动作基本类型。
   - [nargs](https://docs.python.org/zh-cn/3.13/library/argparse.html#nargs) - 命令行参数应当消耗的数目。
   - [const](https://docs.python.org/zh-cn/3.13/library/argparse.html#const) - 被一些 [action](https://docs.python.org/zh-cn/3.13/library/argparse.html#action) 和 [nargs](https://docs.python.org/zh-cn/3.13/library/argparse.html#nargs) 选择所需求的常数。
   - [default](https://docs.python.org/zh-cn/3.13/library/argparse.html#default) - 当参数未在命令行中出现并且也不存在于命名空间对象时所产生的值。
   - [type](https://docs.python.org/zh-cn/3.13/library/argparse.html#type) - 命令行参数应当被转换成的类型。
   - [choices](https://docs.python.org/zh-cn/3.13/library/argparse.html#choices) - 由允许作为参数的值组成的序列。
   - [required](https://docs.python.org/zh-cn/3.13/library/argparse.html#required) - 此命令行选项是否可省略 （仅选项可用）。
   - [help](https://docs.python.org/zh-cn/3.13/library/argparse.html#help) - 一个此选项作用的简单描述。
   - [metavar](https://docs.python.org/zh-cn/3.13/library/argparse.html#metavar) - 在使用方法消息中使用的参数值示例。
   - [dest](https://docs.python.org/zh-cn/3.13/library/argparse.html#dest) - 被添加到 [`parse_args()`](https://docs.python.org/zh-cn/3.13/library/argparse.html#argparse.ArgumentParser.parse_args) 所返回对象上的属性名。
   - [deprecated](https://docs.python.org/zh-cn/3.13/library/argparse.html#deprecated) - 参数的使用是否已被弃用。

3. **解析命令行参数**

   ```python
   ArgumentParser.parse_args(args=None, namespace=None)
   ```

   将参数字符串转换为对象并将其设为命名空间的属性。 返回带有成员的命名空间。

   之前对 [`add_argument()`](https://docs.python.org/zh-cn/3.13/library/argparse.html#argparse.ArgumentParser.add_argument) 的调用决定了哪些对象会被创建以及它们如何被赋值。 请参阅 `add_argument()` 的文档了解详情。

   - [args](https://docs.python.org/zh-cn/3.13/library/argparse.html#args) - 要解析的字符串列表。 默认值是从 [`sys.argv`](https://docs.python.org/zh-cn/3.13/library/sys.html#sys.argv) 获取。
   - [namespace](https://docs.python.org/zh-cn/3.13/library/argparse.html#namespace) - 用于获取属性的对象。 默认值是一个新的空 [`Namespace`](https://docs.python.org/zh-cn/3.13/library/argparse.html#argparse.Namespace) 对象。

**二、`add_argument` name/flags 参数**

1. **位置参数（Positional Arguments）**
   位置参数是命令行输入中位置固定的参数。它们是必填的。

   ```python
   parser.add_argument('filename', type=str, help='The name of the file')
   ```

2. **可选参数（Optional Arguments）**
   可选参数通常以 `--` 或 `-` 开头，允许用户指定值，通常有默认值。

   ```python
   parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
   ```

   这行代码的意思是，`--verbose` 是一个开关参数，如果在命令行中指定了 `--verbose`，它的值就会被设置为 `True`。

**三、`add_argument` 其他参数**

常见的参数类型包括：

1. **`type`**
   指定参数的类型，如 `int`、`float`、`str` 等。还可以用 `register()` 指定自定义类型。

   ```python
   parser.add_argument('--count', type=int, help='The number of items')
   ```

2. **`choices`**
   限制参数只能是某些特定值。

   ```python
   parser.add_argument('--mode', choices=['fast', 'slow'], help='Set the mode')
   ```

3. **`default`**
   设置参数的默认值。如果命令行没有提供该参数，则会使用默认值。

   ```python
   parser.add_argument('--output', type=str, default='result.txt', help='Output file name')
   ```

4. **`action`**
   控制如何处理参数的输入。常见的 `action` 值有：

   - `'store'`：保存参数值（默认行为）。
   - `'store_true'`：如果参数在命令行中出现，则将参数的值设置为 `True`。
   - `'store_false'`：如果参数在命令行中出现，则将参数的值设置为 `False`。
   - `'append'`：将多个输入值追加到列表中。
   - `'count'`：统计参数出现的次数。

   ```python
   parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
   ```

5. **`help`**
   提供关于参数的帮助信息。当用户在命令行中输入 `-h` 或 `--help` 时，这些信息会被自动显示。

   ```python
   parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
   ```

6. **`nargs`**
   设置命令行参数接受的值的数量。常见的 `nargs` 值包括：

   - `'?'`：参数是可选的，并且有默认值。
   - `'*'`：参数接受任意数量的值，结果是一个列表。
   - `'+'`：参数至少需要一个值。

   ```python
   parser.add_argument('input_files', nargs='+', help='List of input files')
   ```

7. **`dest`**
   用于指定命令行参数的目标变量名，默认情况下它会从参数的名字（去掉前缀）生成变量名。

   ```python
   parser.add_argument('--output', dest='output_file', help='Output file name')
   ```

8. **`metavar`**
   允许你自定义帮助信息中显示的参数名称。

   ```python
   parser.add_argument('filename', metavar='FILE', help='Input file name')
   ```

**四、示例代码**

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Example program")

    # 位置参数
    parser.add_argument('filename', type=str, help='The input file name')

    # 可选参数
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--count', type=int, default=5, help='The number of items')
    parser.add_argument('--mode', choices=['fast', 'slow'], help='Set the mode')

    # 解析命令行参数
    args = parser.parse_args()

    # 使用参数
    print(f"Filename: {args.filename}")
    print(f"Verbose: {args.verbose}")
    print(f"Count: {args.count}")
    print(f"Mode: {args.mode}")

if __name__ == "__main__":
    main()
```

## argcomplete 库

> 1. [Python 命令补全神器 argcomplete](https://vra.github.io/2023/05/28/python-autocomplete-with-argcomplete/)
> 2. [Python 的 4 个命令补全工具](https://blog.csdn.net/YouXiaoHuaAi/article/details/131569169)

**一、什么是 `argcomplete`**

`argcomplete` 是一个 Python 库，用于为基于 `argparse` 的命令行程序 **提供自动补全功能**。它可以在 Bash 或 Zsh 中自动补全选项、选项值、子命令等。

```bash
# 例：
./myscript.py --mo<Tab>
# 补全为：
./myscript.py --mode
```

**二、工作原理（简略版）**

`argcomplete` 会在 shell 的补全机制中“插入钩子”，当用户按下 `<Tab>` 时，bash 会调用这个钩子运行脚本的一部分代码，通过 `argcomplete` 返回可用补全项。

具体过程：

1. Shell 检测补全时运行补全函数
2. `argcomplete` 截获当前命令行状态（参数、光标位置等）
3. 运行你的 Python 脚本，并通过环境变量 `COMP_LINE`, `COMP_POINT` 传入命令状态
4. `argcomplete` 调用 `argparse` 解释器并返回匹配项
5. Shell 展示这些补全选项

**三、安装方法及启用补全的方式（两种）**

安装：

```bash
pip install argcomplete
```

启用补全：

1. 方式一：全局补全（推荐）

   ```bash
   activate-global-python-argcomplete --user
   source ~/.bashrc
   ```

   适合你有很多脚本的情况，只要这些脚本有：

   - `# PYTHON_ARGCOMPLETE_OK`
   - 调用了 `argcomplete.autocomplete(parser)`

   就能补全。

2. 方式二：注册特定脚本（适合测试/单个脚本）

   ```bash
   eval "$(register-python-argcomplete ./myscript.py)"
   ```

   > :warning: 每次打开新的终端都要重新执行，除非写入 `.bashrc`。

**四、基本使用方法**

```python
#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mode', choices=['fast', 'slow', 'auto'])

# 建议使用如下方式导入argcomplete并启用自动补全，而不是直接调用
try:
    import argcomplete
    argcomplete.autocomplete(parser)
except ImportError:
    pass
args = parser.parse_args()
```

让它可执行：

```bash
chmod +x myscript.py

# 例：
./myscript.py --mo<Tab>
# 补全为：
./myscript.py --mode
```

**五、补全类型支持**

| 类型       | 示例                                    |
| ---------- | --------------------------------------- |
| 选项名     | `--help`, `--mode`                      |
| 选项值     | `--mode <fast/slow/auto>`               |
| 位置参数   | `<input_file>`                          |
| 子命令     | `myscript.py train`, `myscript.py test` |
| 自定义补全 | 通过 `completer=` 自定义函数            |

**六、高级用法**

1. 自定义补全函数

   ```python
   def custom_completer(prefix, parsed_args, **kwargs):
       return ['apple', 'banana', 'cherry']

   parser.add_argument('--fruit').completer = custom_completer
   ```

2. 与子命令 (`add_subparsers`) 配合使用

   ```python
   subparsers = parser.add_subparsers(dest='command')

   train_parser = subparsers.add_parser('train')
   train_parser.add_argument('--epochs', type=int)
   ```

   `argcomplete` 能正确补全 `train`、`--epochs` 等子命令和参数。

**七、其他**

常见问题与排查：

| 问题                | 原因                              | 解决方法                                         |
| ------------------- | --------------------------------- | ------------------------------------------------ |
| 按 Tab 没反应       | 没启用补全                        | 运行 `activate-global-python-argcomplete --user` |
| 只能补全文件名      | Shell 没接管                      | 使用 bash/zsh，确认你用了 `./script.py`          |
| 无法补全子命令      | 没加 `argcomplete.autocomplete()` | 确认代码中包含该语句                             |
| 在 PyCharm 终端无效 | 它不是标准 bash/zsh               | 用系统终端测试                                   |
| Windows 下无法工作  | PowerShell/CMD 不支持             | 推荐使用 WSL 或 Git Bash                         |

工具命令速查：

| 命令                                        | 说明                     |
| ------------------------------------------- | ------------------------ |
| `activate-global-python-argcomplete --user` | 启用全局补全             |
| `register-python-argcomplete script.py`     | 注册脚本补全             |
| `complete -p`                               | 查看当前已注册补全的脚本 |
| `echo $SHELL`                               | 查看当前终端类型         |

**八、示例测试脚本模板**

```python
#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argparse

def main():
    parser = argparse.ArgumentParser(description="Demo CLI")
    parser.add_argument('--mode', choices=['debug', 'release', 'test'], help="Build mode")
    parser.add_argument('--target', help="Target platform")

    # 建议使用如下方式导入argcomplete并启用自动补全，而不是直接调用
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass
    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()
```

## Python CLI 项目模板带补全

好的，我将为你生成一个 **完整的 Python CLI 项目模板**，具备以下功能：

一、项目特性

- 使用 [`argparse`](https://docs.python.org/3/library/argparse.html) 和 [`argcomplete`](https://pypi.org/project/argcomplete/)
- 支持 **主命令 + 子命令结构**
- 支持 **多个脚本文件**，自动补全（全局补全机制兼容）
- 结构清晰，可扩展
- 自动补全支持 `--help`、自定义参数、子命令名等

二、项目结构示意

```bash
mycli/
├── cli/
│   ├── __init__.py
│   ├── main.py          # 主入口
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── build.py     # 子命令 build
│   │   └── deploy.py    # 子命令 deploy
├── mycli.py             # 执行入口（可补全）
└── README.md
```

三、文件内容一览：

1. `mycli.py`（主执行脚本）

   ```python
   #!/usr/bin/env python
   # PYTHON_ARGCOMPLETE_OK

   from cli.main import main
   main()
   ```

   > 🔧 可执行权限：`chmod +x mycli.py`

2. `cli/main.py`

   ```python
   import argparse
   import argcomplete
   from cli.commands import build, deploy

   def main():
       parser = argparse.ArgumentParser(prog="mycli", description="My CLI Tool")
       subparsers = parser.add_subparsers(dest="command", required=True)

       build.register_subcommand(subparsers)
       deploy.register_subcommand(subparsers)

       argcomplete.autocomplete(parser)
       args = parser.parse_args()
       args.func(args)  # Call the handler
   ```

3. `cli/commands/build.py`

   ```python
   def register_subcommand(subparsers):
       parser = subparsers.add_parser("build", help="Build project")
       parser.add_argument("--target", choices=["x86", "arm", "wasm"], help="Build target")
       parser.set_defaults(func=handle)

   def handle(args):
       print(f"Running build for target: {args.target}")
   ```

4. `cli/commands/deploy.py`

   ```python
   def register_subcommand(subparsers):
       parser = subparsers.add_parser("deploy", help="Deploy project")
       parser.add_argument("--env", choices=["dev", "prod"], help="Environment to deploy to")
       parser.set_defaults(func=handle)

   def handle(args):
       print(f"Deploying to environment: {args.env}")
   ```

5. `cli/__init__.py` 和 `cli/commands/__init__.py`

   空文件即可，用于标记为 Python 包。

6. `README.md`

   ````markdown
   # mycli

   A sample multi-script CLI tool with argcomplete support.

   ## Usage

   ```bash
   chmod +x mycli.py
   activate-global-python-argcomplete --user
   source ~/.bashrc

   ./mycli.py build --target x86
   ./mycli.py deploy --env prod
   ```
   ````

   这样就能体验到自动补全和多子命令结构的功能。

7. 使用方式

   1. 创建一个名为 `mycli` 的目录。
   2. 在该目录下，按上述结构创建文件并复制内容。
   3. 确保 `mycli.py` 文件可执行：

      ```bash
      chmod +x mycli.py
      ```

   4. 启用全局补全：

      ```bash
      activate-global-python-argcomplete --user # 全局启用一次
      source ~/.bashrc
      ```

   5. 运行以下命令测试补全：

      ```bash
      ./mycli.py <Tab>         # 自动补全子命令 build、deploy
      ./mycli.py build --<Tab> # 自动补全 --target
      ```

8. 可选：自动把 `mycli.py` 添加到 `$PATH` 中（例如放到 `~/bin`）

示例补全演示：

```bash
./mycli.py <Tab>
build   deploy

$ ./mycli.py build --<Tab>
--target  --help
```

---

是否需要我打包为 zip 或者通过文本形式输出所有文件内容方便你复制？
