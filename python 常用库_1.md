[toc]

# python 数据科学和机器学习库

## 参考链接

[1]. [数据科学和机器学习](https://mlhowto.readthedocs.io/en/latest/index.html)
[2]. [NumPy reference](https://numpy.org/doc/stable/reference/index.html#reference)

## numpy 模块

> [数据科学和机器学习](https://mlhowto.readthedocs.io/en/latest/index.html)

### NumPy 标准数据类型

> | 数据类型   | 描述                                                                     |
> | ---------- | ------------------------------------------------------------------------ |
> | bool       | 布尔值 bool\_ 别名                                                       |
> | bool\_     | 布尔值（真、 True 或假、 False） ， 用一个字节存储                       |
> | int        | int\_ 别名                                                               |
> | int\_      | 默认整型（类似于 C 语言中的 long， 通常情况下是 int64 或 int32）         |
> | intc       | 同 C 语言的 int 相同（通常是 int32 或 int64）                            |
> | intp       | 用作索引的整型（和 C 语言的 ssize_t 相同， 通常情况下是 int32 或 int64） |
> | int8       | 字节（byte， 范围从–128 到 127）                                         |
> | int16      | 整型（范围从–32768 到 32767）                                            |
> | int32      | 整型（范围从–2147483648 到 2147483647）                                  |
> | int64      | 整型（范围从–9223372036854775808 到 9223372036854775807）                |
> | uint8      | 无符号整型（范围从 0 到 255）uint16 无符号整型（范围从 0 到 65535）      |
> | uint32     | 无符号整型（范围从 0 到 4294967295）                                     |
> | uint64     | 无符号整型（范围从 0 到 18446744073709551615）                           |
> | float      | float64 的简化形式                                                       |
> | float\_    | float64 的简化形式                                                       |
> | float16    | 半精度浮点型：1 符号位，5 比特位指数(exponent)，10 比特位尾数(mantissa)  |
> | float32    | 单精度浮点型：1 符号位，8 比特位指数，23 比特位尾数                      |
> | float64    | 双精度浮点型：1 符号位，11 比特位指数，52 比特位尾数                     |
> | complex\_  | complex128 的简化形式                                                    |
> | complex64  | 复数， 由两个 32 位浮点数表示                                            |
> | complex128 | 复数， 由两个 64 位浮点数表示                                            |

### NumPy 数组内存布局

[ndarray.flags](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.flags.html#numpy.ndarray.flags)

要打印 NumPy 数组的内存排布，可以使用数组对象的 `flags` 属性。`flags` 包含了有关数组内存布局的各种信息，包括是否是连续的内存布局（C-连续或F-连续）、是否可写、是否拥有自己的数据等。

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
     Further explanation of the *fmt* parameter (`%[flag]width[.precision]specifier`):

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
   - `delimiter`：分隔符，默认是空格，可以设定为逗号、制表符等。仅对于二维数组生效，一维数组需要 `reshape(1, -1)`。

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

   **大于2维的数组写入文件函数**：

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

   > 注：跟直接print到屏幕一样，输出长内容会隐藏内容

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

