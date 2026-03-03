[toc]

# python 数据科学和机器学习库

## 参考链接

[1]. [数据科学和机器学习](https://mlhowto.readthedocs.io/en/latest/index.html)
[2]. [NumPy reference](https://numpy.org/doc/stable/reference/index.html#reference)

## numpy 模块

> [数据科学和机器学习](https://mlhowto.readthedocs.io/en/latest/index.html)

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

### NumPy 指定数据类型

> [Data type objects (dtype)](https://numpy.org/doc/stable/reference/arrays.dtypes.html#)

在 NumPy 中，`dtype='<f2'` 是一种指定数据类型的方式，表示**小端字节序（little-endian）的 2 字节浮点数（float16）**。NumPy 提供了多种方式来指定数据类型（`dtype`），包括**基本数据类型**、**字节序前缀**、**结构化数据类型**和**扩展数据类型**等。以下是全面的介绍：

**一、基本数据类型（Type Codes）**

NumPy 使用简短的字符代码表示基本数据类型：

| 数据类型       | 字符代码               | 说明                                                    |
| :------------- | :--------------------- | :------------------------------------------------------ |
| 有符号整数     | `i1`, `i2`, `i4`, `i8` | `int8`, `int16`, `int32`, `int64`                       |
| 无符号整数     | `u1`, `u2`, `u4`, `u8` | `uint8`, `uint16`, `uint32`, `uint64`                   |
| 浮点数         | `f2`, `f4`, `f8`       | `float16`, `float32`, `float64`                         |
| 复数浮点数     | `c8`, `c16`            | `complex64`（`2×float32`）, `complex128`（`2×float64`） |
| 布尔型         | `?`                    | `bool`                                                  |
| 字符串         | `S10`                  | 10 字节的 ASCII 字符串                                  |
| Unicode 字符串 | `U10`                  | 10 字符的 Unicode 字符串                                |
| 时间差         | `m8[ns]`               | `timedelta64`                                           |
| 时间戳         | `M8[ns]`               | `datetime64`                                            |

**示例**：

```python
np.array([1, 2, 3], dtype='i4')  # 32 位整数
np.array([1.0, 2.0], dtype='f8')  # 64 位浮点数
```

**二、字节序前缀（Byte Order）**

> [numpy.dtype.byteorder](https://numpy.org/doc/stable/reference/generated/numpy.dtype.byteorder.html#numpy.dtype.byteorder)

NumPy 允许显式指定字节序（适用于多字节数据类型）：

- `>`：大端字节序（big-endian），示例：`'>i4'`（大端 int32）
- `<`：小端字节序（little-endian），示例：`'<f2'`（小端 float16）
- `=`：原生字节序（native endian，依赖于主机系统），示例：`'=f8'`（默认 float64）
- `|`：不考虑字节序（not applicable），示例：`'|b1'`（无字节序 bool）

> 所有内置数据类型对象的字节顺序都是 `=` 或 `|`。

**示例**：

```python
np.frombuffer(b'\x00\x3C', dtype='<f2')  # 小端 float16
np.frombuffer(b'\x3C\x00', dtype='>f2')  # 大端 float16
# 注：'<f2' 等价于 np.float16 的小端版本（如果系统默认是小端，则 np.float16 和 '<f2' 是相同的）。
```

**三、结构化数据类型（Structured `dtype`）**

结构化数据类型允许定义复合类型（类似 C 结构体）：

(1) 元组列表形式

```python
dtype = np.dtype([
    ('name', 'U10'),  # 字段名 'name'，Unicode 字符串（长度 10）
    ('age', 'i4'),    # 字段名 'age'，32 位整数
    ('height', 'f8')  # 字段名 'height'，64 位浮点数
])
```

(2) 字典形式

```python
dtype = np.dtype({
    'names': ['name', 'age', 'height'],
    'formats': ['U10', 'i4', 'f8']
})
```

(3) 字符串快捷形式

```python
dtype = np.dtype('U10, i4, f8')  # 字段名默认为 'f0', 'f1', 'f2'
```

(4) 对齐的结构化类型（内存对齐）

```python
dtype = np.dtype([
    ('a', 'i4'),
    ('b', 'f8')
], align=True)  # 按编译器对齐规则填充字节
```

**四、扩展数据类型（Extended `dtype`）**

(1) 子数组（Subarrays）

```python
dtype = np.dtype(('i4', (3,)))  # 每个元素是 3 个 int32 的数组
arr = np.array([(1, 2, 3), (4, 5, 6)], dtype=dtype)
```

(2) 自定义数据类型

```python
# 定义一个 4 字节的数据类型，前 2 字节是 int16，后 2 字节是 uint16
dtype = np.dtype([
    ('a', 'i2'),
    ('b', 'u2')
])
```

**五、其他特殊类型**

(1) 时间类型

```python
np.array(['2023-01-01'], dtype='M8[D]')  # 日期类型（天）
np.array([100], dtype='m8[ns]')          # 时间差（纳秒）
```

(2) 对象类型

```python
np.array([1, 'hello'], dtype='O')  # Python 对象类型
```

**六、`numpy` 类型对象直接指定**

可以直接使用 NumPy 的类型对象（推荐，可读性更好）：

```python
np.float16    # 等价于 'f2'
np.int32      # 等价于 'i4'
np.complex128 # 等价于 'c16'
```

**示例**：

```python
np.array([1.0, 2.0], dtype=np.float32)  # 显式指定 float32
```

**七、总结**

| 指定方式          | 示例                     | 说明               |
| :---------------- | :----------------------- | :----------------- |
| 字符代码          | `'i4'`, `'f8'`           | 基本数据类型       |
| 字节序 + 字符代码 | `'<f2'`, `'>i8'`         | 显式指定字节序     |
| 结构化 `dtype`    | `[('name', 'U10')]`      | 类似 C 结构体      |
| NumPy 类型对象    | `np.float16`, `np.int64` | 推荐方式，可读性高 |
| 时间类型          | `'M8[ns]'`, `'m8[D]'`    | 日期时间或时间差   |

选择哪种方式取决于场景：

- **简单类型**：直接用 `np.float32` 或 `'f4'`。
- **二进制数据解析**：用 `'<f2'` 或 `'>i4'` 显式控制字节序。
- **结构化数据**：用 `dtype=[('field', 'type')]`。
- **时间数据**：用 `'M8[ns]'` 或 `np.datetime64`。

### numpy 中 view()

在 **NumPy** 里要实现 **“把 N×K 的 uint8 数据重新解释成 N×(K/2) 的 uint16 数据”**，相当于 C++ 中的 `reinterpret_cast`，可以直接使用 **`view()`** 来做到 **零拷贝 reinterpret**。

**一、使用 `view(np.uint16)`（推荐）**

**前提:**

- 原数组 dtype = `uint8`
- 每一行长度 K 必须是 **偶数**（否则没法两字节组成一个 uint16）

```python
import numpy as np

N, K = 3, 6
a = np.arange(N*K, dtype=np.uint8).reshape(N, K)

# reinterpret_cast: u8 → u16
b = a.view(np.uint16).reshape(N, K // 2)

print(b)
```

解释：

- `view(np.uint16)` 会将底层 buffer 按 **两个字节** 组成一个 `uint16`
- 不发生复制（zero-copy），和 C++ `reinterpret_cast` 几乎一致
- 最终 reshape 成尺寸 `N × (K/2)`

**:warning: <font color=blue>注意点（必须读）</font>**

1. **字节序（endianness）**
   - NumPy 默认使用 **本机字节序（little-endian）**
   - 如果你的数据是 big-endian，则需指定：

   ```python
   b = a.view('>u2').reshape(N, K // 2)  # big-endian uint16
   ```

2. **数据必须连续（C-contiguous）**
   - 如果你的原数组不是 C 连续的，例如经过**切片**或**转置**：

   ```python
   a = a[:, ::2]  # 这种可能不连续
   a = a.transpose()  # 这种可能不连续
   # 使用前需要：
   a = np.ascontiguousarray(a)
   ```

3. **K 必须是偶数**
   否则：

   ```python
   ValueError: When changing to a larger dtype, its size must be a divisor ...
   ```

**二、使用 `np.frombuffer`（不推荐但参考）**

如果你已经有原始 uint8 buffer：

```python
b = np.frombuffer(a.tobytes(), dtype=np.uint16).reshape(N, K//2)
```

但这里会复制 buffer，因此不如 `view()` 好。

### numpy 转换数据类型

> `astype` 不能实现类似 c++ 的 reinterpret cast。

在 `numpy` 中，`astype` 方法用于转换数组的数据类型。`>i4` 是一种数据类型描述符，其中：

- `>` 表示大端字节序
- `i` 表示整数类型（signed integer）
- `4` 表示 4 字节（32 位）

除了 `i` 以外，还有很多其他类型描述符，可以用来表示不同的数据类型。以下是一些常用的数据类型描述符：

常用的数据类型描述符

**一、整数类型**

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

**二、浮点类型**

- `f`：浮点数（floating point）
  - `f2`：2 字节（16 位）半精度浮点数
  - `f4`：4 字节（32 位）单精度浮点数
  - `f8`：8 字节（64 位）双精度浮点数

**三、复数类型**

- `c`：复数（complex number）
  - `c8`：8 字节（32 位实数和 32 位虚数）
  - `c16`：16 字节（64 位实数和 64 位虚数）

**四、字节序前缀**

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

**一、基本随机数生成**

- `random.random(size=None)` or `random.random_sample(size=None)`
  生成指定形状的随机样本，样本值均在半开区间 $[0.0, 1.0)$ 内“连续均匀”分布的随机浮点数。
  若要生成 $[a, b)$ 区间的随机数：$(b - a) * random\_sample() + a$

  ```python
  import numpy as np
  random_array = np.random.random((3, 2))  # 生成3x2的二维数组，值在[0, 1)之间
  ```

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

**二、特定分布的随机数生成**

- `numpy.random.uniform(low=0.0, high=1.0, size=None)`
  从均匀分布 $[low, high)$ 中生成随机数。

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

**三、其他随机数生成函数**

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

**四、随机数生成器控制**

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

**一、打开并读取 `.npy` 文件**

```python
import numpy as np

# 读取 .npy 文件
array = np.load('文件路径.npy')

# 查看读取的数组
print(array)

# 输出数据的形状和数据类型
print("数据形状:", array.shape)
print("数据类型:", array.dtype)
print(f"name: {str('array')+',':<20} shape: {str(array.shape)+',':<15} size: {str(array.nbytes)+',':<15} nbytes: {str(array.nbytes)+',':<15} dtype: {str(array.dtype):<10}")
# 打印内存排布信息
print(array.flags)
```

使用 NumPy 加载 `.npy` 文件时会**自动识别数据的形状和类型**，因此只需要指定文件路径即可。

**二、保存数组为 `.npy` 文件**

```python
import numpy as np

# 创建一个 NumPy 数组
array = np.array([1, 2, 3, 4, 5])

# 保存为 .npy 文件
np.save('文件路径.npy', array)
```

### `.npz` 文件

`.npz` 文件是 NumPy 的一种用于存储多个数组的压缩文件格式。使用 `.npz` 文件可以将多个 NumPy 数组保存到一个文件中，方便数据的组织和管理。每个数组在 `.npz` 文件中都会以键值对的形式存储，可以单独读取其中的每个数组。

**一、保存多个数组到 `.npz` 文件**

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

**二、从 `.npz` 文件读取数据**

可以使用 `numpy.load` 函数加载 `.npz` 文件，并通过键名访问其中的每个数组。加载后的 `.npz` 文件是一个类似字典的对象，可以通过数组的键名访问。

**示例**：

```python
import os, sys, logging, pprint
import numpy as np

# 加载 .npz 文件
data = np.load("arrays.npz")

print(data.files) # 查看有哪些 key，或
pprint.pprint(data.files, compact=False, sort_dicts=False) # 查看有哪些 key
# 访问其中的数组
array1 = data['arr1']
array2 = data['arr2']

print("array1:", array1)
print("array2:", array2)

def print_npz_info(npz_file):
    # 加载 .npz 文件
    data = np.load(npz_file)
    pprint.pprint(data.files, compact=False, sort_dicts=False) # 查看有哪些 key
    # 遍历其中的所有数组
    for key in data.files:   # data.files 是所有的 key 列表
        arr = data[key]
        print(f"{key}: shape={arr.shape}, dtype={arr.dtype}")
```

**三、`.npz` 文件的优点**

1. **便捷**：可以将多个数组存储在一个文件中，便于组织。
2. **压缩**：可以选择压缩文件，减少磁盘空间使用。
3. **快速访问**：加载 `.npz` 文件不需要解压，可以快速访问其中的每个数组。

`.npz` 文件是保存和管理多个数组的好方法，尤其适合需要经常读取的大规模数据。

### `.bin` 文件

`.bin` 文件通常是指包含二进制数据的文件，未指定特定格式。与 `.npy` 或 `.npz` 文件不同，**`.bin` 文件不包含任何元数据（例如数组的形状、数据类型等），只包含原始的二进制数据**。因此，`.bin` 文件在读取和写入时，需要提前知道数据的格式（形状和数据类型），并手动指定这些信息。

**一、保存数组到 `.bin` 文件**

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

**二、从 `.bin` 文件读取数据**

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

**`.bin` 文件的优缺点**

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
   print(f"name: {str('array')+',':<20} shape: {str(array.shape)+',':<15} size: {str(array.size)+',':<15} nbytes: {str(array.nbytes)+',':<15} dtype: {str(array.dtype):<10}")
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

### 数组转字符串 array2string

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

### np.isclose

`np.isclose` 是 NumPy 用来判断两个数组（或数值）在**数值上是否足够接近**的函数，常用于浮点数比较，避免直接用 `==` 造成精度问题。

1. **基本语法**

   ```python
   numpy.isclose(a, b, rtol=1e-05, atol=1e-08, equal_nan=False)
   ```

   **参数说明：**
   - **`a`, `b`**
     可以是标量（单个数）、列表、NumPy 数组，形状需要能广播到相同形状。
   - **`rtol`**（Relative tolerance，相对误差容忍度，默认 `1e-5`）
     控制相对误差阈值。
   - **`atol`**（Absolute tolerance，绝对误差容忍度，默认 `1e-8`）
     控制绝对误差阈值。
   - **`equal_nan`**（默认 `False`）
     如果设为 `True`，那么 `NaN` 和 `NaN` 会被视为相等。

2. **判断标准**

   `np.isclose(a, b)` 的判断依据是：

   $$|a - b| \le (\text{atol} + \text{rtol} \times |b|)$$

   也就是说：
   - **`atol`** 控制的是数值特别小的情况（绝对误差）
   - **`rtol`** 控制的是数值特别大的情况（相对误差）

3. **示例**
   1. **浮点数比较**

      ```python
      import numpy as np

      a = np.array([1.0, 2.0, 3.0])
      b = np.array([1.0, 2.0000001, 3.1])

      print(np.isclose(a, b))
      # 输出: [ True  True False ]
      ```

      前两个元素的误差在容忍范围内，所以返回 `True`，最后一个差 0.1 超过了默认容忍度，返回 `False`。

   2. **NaN 处理**

      ```python
      a = np.array([np.nan, 1.0])
      b = np.array([np.nan, 1.00000001])

      print(np.isclose(a, b))  # [False  True]
      print(np.isclose(a, b, equal_nan=True))  # [ True  True ]
      ```

4. **常见搭配**

   如果需要判断**整个数组是否接近**，可以配合 `np.all` 使用：

   ```python
   if np.all(np.isclose(arr1, arr2)):
       print("两个数组几乎相等")
   ```

### np.all

`np.all` 是 NumPy 里一个非常实用的逻辑判断函数，用来检查**数组里的所有元素**是否全部满足某个条件。

1. **基本语法**

   ```python
   numpy.all(a, axis=None, out=None, keepdims=False, *, where=True)
   ```

   参数说明：
   - **`a`**
     要检查的输入数组，可以是布尔数组，也可以是数值（会自动转换为布尔值，0/False 视为假，其它为真）。
   - **`axis`**（默认 `None`）
     - `None`：检查整个数组是否全为 True
     - 指定整数或元组：按指定维度检查。
   - **`out`**
     可选，用于存放结果的输出数组（一般用不到）。
   - **`keepdims`**（默认 `False`）
     是否保持原有维度，方便广播。
   - **`where`**
     只对满足条件的位置计算（NumPy 1.20+ 新增）。

2. **工作原理**
   - 输入如果是布尔数组，`np.all` 直接检查是否全为 `True`。
   - 输入如果是数值数组，会先转成布尔值（`0` → False，非零 → True）。
   - 返回单个布尔值（或按 `axis` 返回布尔数组）。

3. **示例**
   1. **布尔数组**

      ```python
      import numpy as np

      arr = np.array([True, True, True])
      print(np.all(arr))  # True

      arr = np.array([True, False, True])
      print(np.all(arr))  # False
      ```

   2. **数值数组**

      ```python
      arr = np.array([1, 2, 3])
      print(np.all(arr))  # True（所有数都非零）

      arr = np.array([1, 0, 3])
      print(np.all(arr))  # False（有 0）
      ```

   3. **按维度检查**

      ```python
      arr = np.array([[True, True], [True, False]])

      # axis=0 → 按列检查
      print(np.all(arr, axis=0))  # [ True False ]

      # axis=1 → 按行检查
      print(np.all(arr, axis=1))  # [ True False ]
      ```

   4. **配合条件判断**

      ```python
      a = np.array([1.0, 1.000001, 1.000002])
      b = np.array([1.0, 1.0, 1.0])

      # 判断两个数组是否全部接近
      print(np.all(np.isclose(a, b, atol=1e-5)))  # True
      ```

4. **总结**：
   - `np.all` = **全都为真** 的判断器
   - 常用在数据比较、验证条件、过滤等场景
   - 搭配 `np.isclose`、`np.isnan`、`arr > 0` 等布尔条件特别好用

### tobytes() 二进制一致

numpy 数组最精确的二进制一致性对比方法：

```python
print(a.tobytes() == b.tobytes())  # True
```

特点：

- 直接按字节比较，dtype、endianness、NaN bit pattern 都会影响结果。
- 如果需要绝对的 bit-level 一致，这个方法最好。

### 数组堆叠和拼接

堆叠和拼接操作会复制原数组元素。

**一、任意轴拼接**

`concatenate(tuple)` 将相同轴数的数组元组进行拼接。结果数组不改变轴数。之所以首先介绍该函数，在于下面的 stack 系列函数最终都是通过它实现的（`np.c_` 和 `np.r_` 最终也通过它实现，实际上它是 C 语言的接口函数）。

拼接二维数组可以指定要拼接的轴，默认 axis = 0。

```python
A = np.array([[1, 2, 3]])
B = np.array([[4, 5, 6]])
C = np.concatenate((A, B), axis=0) # 增加行数
print(C)
D = np.concatenate((A, B), axis=1) # 增加列数
print(D)

>>>
[[1 2 3]
 [4 5 6]]
[[1 2 3 4 5 6]]

# 高维数组拼接
import numpy as np

a = np.ones((2, 3, 4, 5))
b = np.zeros((2, 3, 4, 5))

print(np.concatenate((a, b), axis=0).shape)  # (4, 3, 4, 5)
print(np.concatenate((a, b), axis=1).shape)  # (2, 6, 4, 5)
print(np.concatenate((a, b), axis=2).shape)  # (2, 3, 8, 5)
print(np.concatenate((a, b), axis=3).shape)  # (2, 3, 4, 10)

# for 循环数组拼接
data_list = []
for file in work_path.rglob('*.bin'):
    print(f"find file: {file}")
    data = np.fromfile(file, dtype=np.float32)
    print(f"data shape: {data.shape}, dtype: {data.dtype}")
    data_list.append(data)
data = np.concatenate(data_list, axis=0)
```

与聚合操作比较，可以发现聚合操作默认会减少轴数，而拼接操作不会改变轴数。concatenate 要求所有数组除了拼接的轴上的 shape 值无需相同，其他的轴上的 shape 值必须相同，否则无法拼接。

**二、垂直堆叠**

vstack(tuple) 接受一个由数组组成的元组，每个数组在列上的元素个数必须相同。
等价于 `concatenate(map(atleast_2d,tup), axis=0)`，显然要进行垂直堆叠操作，数组至少是 2D 的，转换后在行上堆叠：

- 在 2D 时：把行堆叠起来。
- 在 3D / 4D 时：也就是在 第 0 维 上拼接。
- vstack 在 1D 上堆叠会返回 2D 数组。

```python
A = np.array([1, 2, 3])
B = np.array([[4, 5, 6], [7, 8, 9]])
print(np.vstack((A, B, A)))

>>>
[[1 2 3]
 [4 5 6]
 [7 8 9]
 [1 2 3]]

# 高维数组拼接
import numpy as np

a = np.ones((2, 3, 4, 5))
b = np.zeros((2, 3, 4, 5))

print(np.vstack((a, b)).shape)  # (4, 3, 4, 5)
```

vstack 垂直堆叠示意图：
[![borders](https://mlhowto.readthedocs.io/en/latest/_images/vstack.png)](https://mlhowto.readthedocs.io/en/latest/_images/vstack.png)

**三、水平堆叠**

hstack(tuple) 与 vstack(tuple) 类似，按第二个轴依次取数据，数组行数必须相同。
等价于 `concatenate(map(atleast_2d,tup), axis=1)`，水平堆叠只需要保证数组有 1D 即可，但有细节：

- 如果数组是一维：会在最后一个维度拼接。
- 如果是 2D 以上：固定在 第 1 维 拼接。

```python
A = np.array([0, 1, 2])
B = np.array([30,40])
print(np.hstack((A, B, A)))

>>>
[0, 1, 2, 30, 40, 0, 1, 2]

# 高维数组拼接
import numpy as np

a = np.ones((2, 3, 4, 5))
b = np.zeros((2, 3, 4, 5))

print(np.hstack((a, b)).shape)  # (2, 6, 4, 5)
```

hstack 水平堆叠示意图：
[![borders](https://mlhowto.readthedocs.io/en/latest/_images/hstack.png)](https://mlhowto.readthedocs.io/en/latest/_images/hstack.png)

## 字节流

> 1. [Binary Sequence Types — bytes, bytearray, memoryview](https://docs.python.org/3/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview)
> 2. [`bytes.fromhex()` - Python docs](https://docs.python.org/3/library/stdtypes.html#bytes.fromhex)
> 3. [`bytes.hex()` — Python Docs](https://docs.python.org/3/library/stdtypes.html#bytes.hex)

- `bytes.fromhex()`：将十六进制字符串（hex string）转换为 `bytes` 对象
- `bytes.hex()`：将一个 `bytes` 对象转换成纯十六进制表示的字符串

### bytes.fromhex

`bytes.fromhex()` 是 Python 内置的一个非常实用的方法，用于将**十六进制字符串（hex string）转换为 bytes 对象**，常用于处理底层数据通信、文件解析、加密等场景。

**函数定义**

```python
bytes.fromhex(string)
```

**参数说明**

- `string`：一个表示十六进制的字符串，可以包含空格，必须是偶数字符数（每两个字符代表一个字节）

**返回值**

- 返回一个新的 `bytes` 对象，其中每个字节由 `string` 中的两个十六进制字符组成。

**示例**

1. 十六进制字符串

   ```python
   b = bytes.fromhex('48656c6c6f20576f726c64')
   print(b)         # 输出: b'Hello World'
   print(b.decode())  # 输出: Hello World
   ```

   `'48'` 是 `H`，`65` 是 `e`，依此类推。

2. 带空格的字符串

   ```python
   b = bytes.fromhex('48 65 6c 6c 6f')
   print(b)  # 输出: b'Hello'
   ```

   空格是允许的，它会被自动忽略。

3. 错误示例（字符串长度不是偶数）

   ```python
   bytes.fromhex('123')  # ValueError: non-hexadecimal number found in fromhex() arg at position 3
   ```

   你必须提供偶数长度的字符串，因为两个 hex 字符才能组成一个完整的字节。

**常见应用场景**

1. **从十六进制字符串还原二进制数据**
   - 如：网络数据包、十六进制编辑器导出的字符串
2. **配合 `struct.unpack` 使用**
   - 可以将十六进制转为 `bytes` 后按格式解析
3. **加密通信、哈希值处理**
   - 如将 SHA256 的 hex digest 转成 bytes 继续操作

### bytes.hex()

`bytes.hex()` 是 Python 中 `bytes` 类型的一个方法，用于将一个 `bytes` 对象转换成**纯十六进制表示的字符串**。它是 `bytes.fromhex()` 的逆操作，常用于**调试、日志输出、数据传输、加密摘要处理等**场景。

**函数定义**

```python
bytes.hex(sep=None, bytes_per_sep=1)
```

**参数说明（Python 3.8+ 支持）**

| 参数            | 类型  | 说明                                                           |
| --------------- | ----- | -------------------------------------------------------------- |
| `sep`           | `str` | 可选，插入在每个字节之间的分隔符，例如 `' '`（空格）、`':'` 等 |
| `bytes_per_sep` | `int` | 每多少个字节插入一个 `sep`，默认为 1                           |

> 早期版本（Python < 3.8）不支持 `sep` 和 `bytes_per_sep` 参数。

**返回值**

一个只包含十六进制字符的字符串，每个字节转为两个十六进制字符（小写）。

**示例**

1. 基本示例

   ```python
   data = b'ABC'
   hex_str = data.hex()
   print(hex_str)  # 输出: '414243'
   ```

   说明：
   - `'A'` → `0x41`
   - `'B'` → `0x42`
   - `'C'` → `0x43`

2. 使用 `sep` 和 `bytes_per_sep`

   ```python
   data = b'\x12\x34\x56\x78'
   print(data.hex(sep=':'))  # 输出: '12:34:56:78'

   print(data.hex(sep='-', bytes_per_sep=2))  # 输出: '1234-5678'
   ```

   这在调试或输出类似 MAC 地址、十六进制分组等格式时非常有用。

**应用场景**

| 场景         | 说明                                    |
| ------------ | --------------------------------------- |
| 数据调试     | 将 `bytes` 数据打印成可读的十六进制     |
| 数据传输     | 某些协议用 hex 字符串传输二进制数据     |
| 加密摘要处理 | 哈希值如 SHA256 通常转为 hex 字符串显示 |
| 数据序列化   | 可将 bytes 用 hex 保存为文本格式        |

### 字节流和数值互转

**一、将缓冲区解释为一维数组。**

```python
numpy.frombuffer(buffer, dtype=float, count=-1, offset=0, *, like=None)
```

**参数：**

- **buffer**: buffer_like

  buffer 区接口的对象

- **dtype**: data-type, **optional**

  返回数组的数据类型；**默认值：浮点数**。

- **count**: int, **optional**

  要读取的项目数。`-1`表示缓冲区中的所有数据；**默认值：-1**。

- **offset**: int, **optional**

  从该偏移量开始读取缓冲区（以字节为单位）；**默认值：0**。

- **like**: array_like, **optional**

  引用对象，用于创建非 NumPy 数组。如果传入的类数组`like`支持该`__array_function__`协议，则结果将由该协议定义。在这种情况下，它确保创建的数组对象与通过此参数传入的数组对象兼容。

**注意：**

如果缓冲区包含的数据不是按机器字节顺序排列的，则应将其指定为数据类型的一部分，例如：

```python
dt = np.dtype(int)
dt = dt.newbyteorder('>')
np.frombuffer(buf, dtype=dt)
```

结果数组的数据不会被字节交换，但会被正确解释。

此函数创建原始对象的视图。这通常是安全的，但当原始对象可变或不受信任时，复制结果可能是有意义的。

**二、从数组中的原始数据字节构造 Python 字节**

```python
ndarray.tobytes(order='C')
```

构造 Python 字节，显示数据内存原始内容的副本。字节对象默认以 C 语言顺序生成。此行为由`order`参数控制。

- 参数：

  **order**：{‘C’, ‘F’, ‘A’}, optional

  控制字节对象的内存布局。 ‘C’ 表示 C-order, ‘F’ 表示 F-order, ‘A’ (short for _Any_) 表示 ‘F’ if _a_ is Fortran contiguous, ‘C’ otherwise. 默认值为 ‘C’.

- 返回：

  **s**：bytes

  数组的原始数据副本的字节。

```python
import numpy as np
x = np.array([[0, 1], [2, 3]], dtype='<u2')
x.tobytes()
b'\x00\x00\x01\x00\x02\x00\x03\x00'
x.tobytes('C') == x.tobytes()
True
x.tobytes('F')
b'\x00\x00\x02\x00\x01\x00\x03\x00'
```

## round 舍入模式

**Python 内置** 、**NumPy** 、**PyTorch** 中的默认 round（舍入）模式都是 IEEE 754 的 **round to nearest, ties to even（银行家舍入）**。

### NumPy 的 round 行为

1. 默认 round 模式（ties-to-even）：

   ```python
   import numpy as np

   np.round([1.5, 2.5, 3.5, 4.5])
   # array([2., 2., 4., 4.])
   ```

2. NumPy 中其他舍入模式指定方法：

   | 目标      | 函数          |
   | --------- | ------------- |
   | 向 0      | `np.trunc(x)` |
   | 向下 (−∞) | `np.floor(x)` |
   | 向上 (+∞) | `np.ceil(x)`  |
   | 最近偶数  | `np.round(x)` |

   ```python
   x = np.array([1.5, -1.5])

   np.trunc(x)   # [ 1. -1.]
   np.floor(x)   # [ 1. -2.]
   np.ceil(x)    # [ 2. -1.]
   np.round(x)   # [ 2. -2.]
   ```

### PyTorch 的 round 行为

1. 默认 round 模式（ties-to-even）：

   ```python
   import torch

   x = torch.tensor([1.5, 2.5, 3.5, 4.5])
   torch.round(x)
   # tensor([2., 2., 4., 4.])
   ```

   ✔ 与 NumPy 完全一致
   ✔ CPU / CUDA 都遵循 IEEE 754 最近偶数

2. PyTorch 中其他舍入模式指定方法：

   | 舍入策略  | 函数            |
   | --------- | --------------- |
   | 向 0      | `torch.trunc()` |
   | 向下 (−∞) | `torch.floor()` |
   | 向上 (+∞) | `torch.ceil()`  |
   | 最近偶数  | `torch.round()` |

   ```python
   x = torch.tensor([1.5, -1.5])

   torch.trunc(x)   # tensor([ 1., -1.])
   torch.floor(x)   # tensor([ 1., -2.])
   torch.ceil(x)    # tensor([ 2., -1.])
   torch.round(x)   # tensor([ 2., -2.])
   ```

### 注意

1. 实现 ties away from zero

   需要手写逻辑：

   ```python
   # NumPy 版
   def round_half_away_from_zero(x):
       return np.sign(x) * np.floor(np.abs(x) + 0.5)

   # Torch 版：
   def round_half_away_from_zero_torch(x):
       return torch.sign(x) * torch.floor(torch.abs(x) + 0.5)
   ```

2. 量化 / int 转换要特别小心

   很多坑就在这里：

   ```python
   x = torch.tensor([2.5])
   x.int()     # tensor([2], dtype=torch.int32)
   ```

   👉 float → int 是 toward zero，不是 round！

   如果你在做：
   - int8 量化
   - scale + round
   - softmax / layernorm 定点化

   必须**显式 round 再 cast**

3. 工程常见问题

   NumPy / PyTorch 默认 round 是“最近偶数”，但很多芯片量化规范要求的是 “round half away from zero” 或 “round down”。

   这会导致：
   - Python 仿真 vs NPU / DSP 结果 **对不上**
   - 边界值（±0.5）误差集中爆发
