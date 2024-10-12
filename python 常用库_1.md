[toc]

# python 常用库

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

### 数组转换为字符串

`numpy.array2string` 是一个非常灵活的函数，它可以将 NumPy 数组转换为字符串，并且提供了很多选项来控制输出格式。

```python
numpy.array2string(a, max_line_width=None, precision=None, suppress_small=None, separator=' ', prefix='', style=<no value>, formatter=None, threshold=None, edgeitems=None, sign=None, floatmode=None, suffix='', *, legacy=None)
```

**参数说明**

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

