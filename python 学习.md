[toc]

# python 内置功能

## sys.argv

在 Python 中，`sys.argv`是一个列表，它包含了命令行参数。`sys.argv[0]` 是脚本的名称，而后面的元素是脚本后面跟随的命令行参数。

下面是一个示例脚本`example.py`，它使用`sys.argv`来获取命令行参数并进行简单处理：

```python
import sys

def main():
    # 打印脚本名称
    print(f"Script name: {sys.argv[0]}")

    # 打印传递给脚本的参数
    for i in range(1, len(sys.argv)):
        print(f"Argument {i}: {sys.argv[i]}")

if __name__ == "__main__":
    main()
```

假设你通过以下命令运行脚本：

```shell
python example.py arg1 arg2 arg3
```

那么输出将是：

```yaml
Script name: example.py
Argument 1: arg1
Argument 2: arg2
Argument 3: arg3
```

**使用场景**：

1. **获取命令行参数**： `sys.argv`非常适用于需要从命令行获取输入参数的脚本。
2. **简单的命令行工具**： 使用`sys.argv`可以快速创建简单的命令行工具，处理不同的参数来执行不同的操作。

**注意事项**：

1. **参数类型**： `sys.argv`中的所有参数都是字符串类型。如果需要处理整数或浮点数，需要进行类型转换。
2. **参数个数**： 运行脚本时需要检查`sys.argv`的长度，以避免索引超出范围的错误。

以下是一个稍微复杂的示例，演示如何处理命令行参数并进行类型转换：

```python
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python example.py <param1> <param2>")
        sys.exit(1)

    param1 = sys.argv[1]
    param2 = int(sys.argv[2])  # 假设第二个参数需要是整数

    print(f"Parameter 1: {param1}")
    print(f"Parameter 2: {param2}")

if __name__ == "__main__":
    main()
```

运行示例命令：

```shell
python example.py hello 123
```

输出将是：

```sehll
Parameter 1: hello
Parameter 2: 123
```

如果参数不足或类型不正确，脚本将提示正确的用法并退出。

## 负索引

在 Python 中，列表的负索引（例如 `[-1]`）是一种方便的方式，用于从列表的末尾开始访问元素。具体来说，`-1` 表示列表的最后一个元素，`-2` 表示倒数第二个元素，依此类推。下面是一些关于负索引的示例和用法：

**负索引的基本用法**：

假设我们有一个列表：

```python
my_list = [10, 20, 30, 40, 50]
```

我们可以使用负索引来访问列表的元素：

```
print(my_list[-1])  # 输出: 50
print(my_list[-2])  # 输出: 40
print(my_list[-3])  # 输出: 30
print(my_list[-4])  # 输出: 20
print(my_list[-5])  # 输出: 10
```

**负索引和切片**：

负索引用于切片操作时也非常方便，可以从列表的末尾开始进行切片：

```
print(my_list[-3:])    # 输出: [30, 40, 50]  从倒数第三个元素到列表末尾
print(my_list[:-2])    # 输出: [10, 20, 30]  从列表开头到倒数第二个元素之前
print(my_list[-4:-1])  # 输出: [20, 30, 40]  从倒数第四个元素到倒数第一个元素之前
```

**修改列表元素**：

负索引也可以用于修改列表中的元素：

```
my_list[-1] = 100
print(my_list)  # 输出: [10, 20, 30, 40, 100]

my_list[-3] = 60
print(my_list)  # 输出: [10, 20, 60, 40, 100]
```

**示例：循环遍历列表的倒数元素**：

你可以使用负索引来循环遍历列表的倒数元素，例如：

```python
for i in range(1, len(my_list) + 1):
    print(my_list[-i])
```

输出：

```log
100
40
60
20
10
```

**注意事项**：

1. **索引越界**： 使用负索引时，同样需要注意索引越界的问题。如果列表长度小于负索引的绝对值，将会抛出 `IndexError`。

   ```python
   my_list = [1, 2, 3]
   print(my_list[-4])  # IndexError: list index out of range
   ```

2. **可读性**： 虽然负索引非常方便，但在使用时要确保代码的可读性。过多使用负索引可能会使代码难以理解。

负索引是 Python 中一个非常实用的特性，能够简化从列表末尾访问元素的操作，使代码更简洁。

## range[)

在 Python 中，范围和切片的定义通常是前闭后开（inclusive-exclusive）的，包括 `range` 函数、列表切片、字符串切片等。这种设计在编程中很常见，因为它简化了计算范围和索引的逻辑。

如：

1. `range(5)` 生成从 0 到 4 的数字，不包括 5。`np.arange()` 类似。
2. `list[1:4]` 选择从索引 1 到索引 3 的元素，不包括索引 4。数组索引从 0 开始。

## slice()

在 Python 和 NumPy 中，`slice` 是一个用于切片操作的内建对象，它提供了一种方便的方式来指定从序列（如列表、数组等）中提取部分元素的规则。`slice` 对象通常由 `start`、`stop` 和 `step` 三个参数构成，类似于 `start:stop:step` 这种切片表示法。

1. **基本语法**

   ```python
   slice(start, stop, step)
   ```

   - `start`: 切片开始的位置，默认值是 `None`（即从开始位置）。
   - `stop`: 切片结束的位置，默认值是 `None`（即直到序列的末尾）。
   - `step`: 切片的步长，默认值是 `1`。

   如 `s = slice(1, 5, 2)` 显示创建了一个 `slice` 类对象实例，表示从索引 1 开始到 5 结束（但不包括 5），步长为 2。

2. **常见的切片用法**

   1. **简单切片**

      ```python
      arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
      print(arr[2:7:2])  # 输出 [2 4 6]
      ```

      这表示从索引 `2` 开始，到 `7` 结束（不包括 7），步长为 `2`。

   2. **在多维数组中的切片**

      对于一个二维数组，你可以使用 `slice` 来选择某些行或列：

      ```python
      arr = np.random.rand(4, 5)  # 形状为 (4, 5) 的数组
      s = slice(1, 3)  # 选择第 1 行到第 2 行
      print(arr[s, :])  # 获取所有列
      ```

   3. **与切片对象一起使用**

      你还可以创建切片对象来处理多维数组的切片。举个例子：

      ```python
      arr = np.random.rand(4, 5, 6)
      s1 = slice(1, 3)
      s2 = slice(2, 4)
      s3 = slice(None)  # 表示所有元素
      idx = [s1, s2, s3]
      print(arr[tuple(idx)])  # 获取第 1 到第 2 行，第 2 到第 3 列，所有深度元素
      ```

      > 当你使用切片操作时，NumPy 期望的是一个 **元组** 来表示多个维度的索引。如果你传入一个列表，它可能不会被正确解析为多维切片索引，而是会将列表视为一个单一的索引。

3. **注意事项**

- 切片操作不会创建数组的副本，而是返回原数组的一个视图。如果你修改切片返回的数组，原数组也会受到影响。为了避免这种情况，可以使用 `copy()` 方法来创建切片的副本。
- `slice(None)` 等价于 `:`，用于选择整个维度。

**总结**：

`slice` 是 Python 中处理序列切片的工具，可以通过它来指定切片的开始、结束和步长。它尤其在 NumPy 中非常有用，用于灵活地处理多维数组的高级切片操作。

## realpath

在 Python 中，`realpath` 函数用于获取文件或目录的绝对路径，并解析所有符号链接。这在处理文件路径时特别有用，因为它可以帮助你**确保你访问的是实际的文件位置**，而**不是符号链接指向的路径**。

`realpath` 是 `os.path` 模块中的一个函数，因此你需要先导入 `os` 模块，然后才能使用它。

以下是一些示例和用法：

**基本用法**：

```python
import os

# 获取当前脚本的绝对路径
current_script_path = os.path.realpath(__file__)
print(current_script_path)
```

**示例：解析符号链接**：

假设有一个符号链接指向某个文件或目录，可以使用 `realpath` 来获取实际路径：

```python
import os

# 假设 'symlink_path' 是一个符号链接的路径
symlink_path = '/path/to/symlink'
actual_path = os.path.realpath(symlink_path)
print(actual_path)
```

**示例：处理相对路径**：

`realpath` 也可以用来将相对路径转换为绝对路径：

```python
import os

relative_path = './some/relative/path'
absolute_path = os.path.realpath(relative_path)
print(absolute_path)
```

**结合其他 `os.path` 函数**：

可以结合其他 `os.path` 函数使用，以便更好地处理文件路径。例如，**可以使用 `join` 来组合路径**，然后使用 `realpath` 获取绝对路径：

```python
import os

base_path = '/base/directory'
relative_path = 'subdir/file.txt'

# 组合路径
combined_path = os.path.join(base_path, relative_path)

# 获取绝对路径
absolute_path = os.path.realpath(combined_path)
print(absolute_path)
```

**示例：跨平台使用**：

**由于 `os.path` 是跨平台的**，在不同的操作系统上使用 `realpath` 可以确保路径处理的一致性：

```python
import os

# 在 Windows 上的示例
windows_path = 'C:\\path\\to\\file'
absolute_path_windows = os.path.realpath(windows_path)
print(absolute_path_windows)

# 在 Unix/Linux 上的示例
unix_path = '/path/to/file'
absolute_path_unix = os.path.realpath(unix_path)
print(absolute_path_unix)
```

**总结**：

- **功能**：`realpath` 函数返回文件或目录的绝对路径，并解析所有符号链接。
- **用途**：适用于需要确定文件或目录的实际位置、解析符号链接、将相对路径转换为绝对路径等情况。
- **跨平台**：由于 `os.path` 是跨平台的，`realpath` 可以在不同操作系统上使用而无需担心兼容性问题。

通过使用 `realpath`，你可以更可靠地处理文件路径，确保你的代码处理的是实际的文件位置而不是符号链接指向的路径。

## f-string

在 Python 中，`f""` 是一种字符串格式化方法，称为 **f-string**（格式化字符串字面量），引入于 Python 3.6。f-string 提供了一种简洁且直观的方式来嵌入表达式和变量到字符串中。

**基本用法**：

要使用 f-string，只需在字符串前面加上字母 `f` 或 `F`，然后在字符串中用花括号 `{}` 包含表达式或变量名。

```python
name = "Alice"
age = 30
a = 5

# 使用 f-string 进行字符串格式化
greeting = f"Hello, {name}. You are {age + a} years old."
print(greeting)  # 输出："Hello, Alice. You are 35 years old."
```

**调用函数和方法**：

你也可以在 f-string 中调用函数或方法：

```python
def greet(name):
    return f"Hello, {name}!"

name = "Bob"
greeting = f"{greet(name)} How are you today?"
print(greeting)  # 输出: "Hello, Bob! How are you today?"
```

**格式化数字**：

你可以在 f-string 中在表达式后面加上 `:` 和格式说明符，来控制数字的显示格式。例如，浮动小数点数字的精度、填充宽度、对齐方式等。

- `:.2f` 表示保留两位小数。
- `:05` 表示总宽度为 5，空位填充 0。
- `:,` 会自动为数字添加千位分隔符。
- `<` 表示左对齐。
- `>` 表示右对齐。
- `^` 表示居中对齐。
- `10` 表示宽度为 10，空白部分根据对齐规则填充。

```python
pi = 3.14159265358979
print(f"Value of Pi to 2 decimal places: {pi:.2f}")  # 输出: "Value of Pi to 2 decimal places: 3.14"

number = 42
print(f"Number padded with leading zeros: {number:05}")  # 输出: "Number padded with leading zeros: 00042"

number = 1000000
print(f"Formatted number: {number:,}")  # 输出: "Formatted number: 1,000,000"

name = "Alice"
print(f"{name:<10}")  # 输出: "Alice     "  (左对齐)
print(f"{name:>10}")  # 输出: "     Alice"  (右对齐)
print(f"{name:^10}")  # 输出: "  Alice   "  (居中对齐)
```

**日期和时间格式化**：

你可以在 f-string 中使用 `strftime()` 格式化日期和时间。

```python
from datetime import datetime

now = datetime.now()
print(f"Current date and time: {now:%Y-%m-%d %H:%M:%S}")
# 输出: "Current date and time: 2024-11-13 12:34:56"
```

- `%Y-%m-%d %H:%M:%S` 是日期和时间的格式化字符串。

**多行 f-string**：

你可以使用三引号（`'''` 或 `"""`）创建多行 f-string：

```python
name = "Alice"
age = 30
address = "Wonderland"

# 多行 f-string
info = f"""
Name: {name}
Age: {age}
Address: {address}
"""
print(info)
```

输出：

```log
Name: Alice
Age: 30
Address: Wonderland
```

**嵌套引号**：

在 f-string 中使用引号时，你需要注意嵌套的引号类型。如果 f-string 使用双引号（`"`），那么在花括号内的字符串最好使用单引号（`'`），反之亦然：

```python
name = "Alice"
quote = f'He said, "Hello, {name}!"'
print(quote) # 输出: He said, "Hello, Alice!"
```

**字符和变量格式化**：

```python
print(f"{'mean:': <15} shape: {str(mean.shape)+',': <20} nbytes: {str(mean.nbytes)+',': <10} dtype: {str(mean.dtype)+',': <10}")
```

**使用字典和列表**：

f-string 也可以用来格式化字典和列表中的值：

```python
person = {"name": "Alice", "age": 30}
numbers = [1, 2, 3, 4, 5]

info = f"{person['name']} is {person['age']} years old."
number_list = f"The first number is {numbers[0]}."
print(info) # 输出: Alice is 30 years old.
print(number_list) # 输出: The first number is 1.
```

**使用对象的属性**：

f-string 也可以直接访问对象的属性：

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("John", 25)
message = f"Name: {person.name}, Age: {person.age}"
print(message)  # 输出: "Name: John, Age: 25"
```

**总结**：

f-string 提供了一种简洁且高效的字符串格式化方式。它们不仅可以嵌入变量，还可以嵌入复杂的表达式，并支持各种格式化选项。通过使用 f-string，可以使代码更易读、更直观。

## with...as

在 Python 中，`with ... as ...` 语句用于上下文管理（context management）。它提供了一种简洁的方式来**处理资源的分配和释放**，比如**文件操作、锁、网络连接**等。

**基本用法**：

最常见的用法之一是文件操作。在使用文件时，`with` 语句确保文件会被正确地关闭，即使在操作过程中发生异常。

```python
# 使用 with 语句打开文件
with open('example.txt', 'r') as file:
    content = file.read()
    print(content)
# 文件在此处自动关闭
```

在上面的示例中，`open('example.txt', 'r')` 返回一个文件对象，并且 `as file` 将该对象赋值给变量 `file`。`with` 语句的作用范围结束时，文件会自动关闭。

**错误处理**：

如果 `with ... as ...` 语句失败（例如文件不存在、权限不足等），你应该通过异常处理机制来捕获错误，并进行相应的处理。

常用的错误处理方式是使用 `try...except` 来捕获异常。如果 `with ... as ...` 操作失败，Python 会引发相应的异常（如 `FileNotFoundError`、`PermissionError` 等），你可以在 `except` 块中捕获并处理这些错误。

1. **示例：文件打开失败的错误处理**

   假设我们尝试打开一个文件进行读取，如果文件不存在或者没有权限，程序应该捕获异常并打印错误信息。

   ```python
   try:
       with open('file.txt', 'r') as f:
           content = f.read()
           print(content)
   except FileNotFoundError:
       print("错误：文件未找到！")
   except PermissionError:
       print("错误：没有权限读取文件！")
   except Exception as e:
       # 捕获其他未预料到的异常
       print(f"发生错误：{e}")
   ```

   解释：

   1. **`FileNotFoundError`**：当文件不存在时会抛出此异常。
   2. **`PermissionError`**：当程序没有权限读取文件时会抛出此异常。
   3. **`Exception`**：这是一个通用异常捕获，表示其他所有类型的异常。它将捕获任何未在前面列出的异常，并打印异常消息。

2. **更复杂的示例：文件写入失败的错误处理**

   如果你尝试写入文件，也可能遇到权限问题或磁盘空间不足等问题，可以按如下方式进行处理：

   ```python
   try:
       with open('output.txt', 'w') as f:
           f.write("这是写入文件的内容")
   except PermissionError:
       print("错误：没有权限写入文件！")
   except IOError as e:
       print(f"输入/输出错误：{e}")
   except Exception as e:
       print(f"发生错误：{e}")
   ```

3. **其他资源管理中的 `with` 示例**

   `with` 不仅用于文件操作，还广泛应用于其他需要资源管理的场景，比如数据库连接、网络连接等。无论是打开数据库连接、使用网络套接字、获取锁等，都是使用 `with` 语句来管理资源并保证资源释放。

   ```python
   import sqlite3

   try:
       with sqlite3.connect('example.db') as conn:
           cursor = conn.cursor()
           cursor.execute("SELECT * FROM users")
           rows = cursor.fetchall()
           print(rows)
   except sqlite3.Error as e:
       print(f"数据库错误：{e}")
   except Exception as e:
       print(f"发生错误：{e}")
   ```

**总结**：

- `with ... as ...` 本身可以保证在块结束时自动释放资源（即使发生异常），但如果操作失败，你需要使用 `try...except` 捕获并处理异常。
- 通过捕获具体的异常类型（如 `FileNotFoundError` 或 `PermissionError`），你可以提供更明确的错误信息。
- 使用通用的 `Exception` 捕获未预料的错误，并确保程序能继续运行或给出提示。

## 上下文管理器

要实现自定义的上下文管理器，可以定义一个类并实现 `__enter__` 和 `__exit__` 方法。

示例：自定义上下文管理器

```python
class MyContextManager:
    def __enter__(self):
        print("Entering the context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting the context")

    def do_something(self):
        print("Doing something")

# 使用自定义的上下文管理器
with MyContextManager() as manager:
    manager.do_something()
```

输出：

```log
Entering the context
Doing something
Exiting the context
```

在上面的示例中：

- `__enter__` 方法在进入上下文时被调用，并且其返回值被赋给 `as` 后的变量（这里是 `manager`）。
- `__exit__` 方法在离开上下文时被调用，它接受三个参数（`exc_type`, `exc_value`, 和 `traceback`），用于处理可能发生的异常。

**处理异常**：

`with` 语句在处理异常时也非常有用。`__exit__` 方法可以捕获并处理在上下文块中发生的异常。

示例：处理异常的上下文管理器

```python
class MyContextManager:
    def __enter__(self):
        print("Entering the context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"An exception occurred: {exc_value}")
        print("Exiting the context")
        return True  # 表示异常已经被处理

# 使用自定义的上下文管理器
with MyContextManager() as manager:
    print("Inside the context")
    raise ValueError("Something went wrong!")
```

输出：

```log
Entering the context
Inside the context
An exception occurred: Something went wrong!
Exiting the context
```

在上面的示例中，异常 `ValueError` 被抛出，`__exit__` 方法捕获了该异常并进行了处理。通过返回 `True`，`__exit__` 方法告诉解释器异常已被处理，不需要再次抛出。

**使用上下文管理器的内置模块**：

Python 的标准库中有许多内置的上下文管理器，如 `threading.Lock` 和 `decimal.localcontext`。

示例：使用锁进行线程同步

```python
import threading

lock = threading.Lock()

def thread_safe_function():
    with lock:
        # 线程安全的代码块
        print("Thread-safe operation")

# 创建多个线程来测试
threads = [threading.Thread(target=thread_safe_function) for _ in range(5)]

for t in threads:
    t.start()

for t in threads:
    t.join()
```

在这个示例中，`with lock` 确保了在多线程环境中对共享资源的访问是线程安全的。

**总结**：

`with ... as ...` 语句是 Python 中强大的特性，用于确保资源的正确管理和释放。通过实现 `__enter__` 和 `__exit__` 方法，你可以创建自定义的上下文管理器，从而更好地控制资源的生命周期。标准库中也提供了许多内置的上下文管理器，便于在各种场景中使用。

## try 和 except

在 Python 中，`try` 和 `except` 语句用于处理异常（错误）。异常处理机制使你可以捕获并处理在程序运行过程中可能发生的错误，从而提高程序的健壮性和可靠性。以下是对 `try` 和 `except` 语句的详细解释和使用示例。

### 基本用法

**捕获并处理异常**：

```python
try:
    # 可能引发异常的代码
    result = 10 / 0
except ZeroDivisionError:
    # 处理异常的代码
    print("You cannot divide by zero!")
```

在这个示例中：

- `try` 块中的代码尝试执行 `10 / 0`，这将引发 `ZeroDivisionError` 异常。
- `except` 块捕获并处理该异常，打印错误消息。

**捕获特定异常**：

你可以捕获并处理特定类型的异常：

```python
try:
    result = int("abc")
except ValueError:
    print("Cannot convert string to integer!")
```

在这个示例中：

- `int("abc")` 会引发 `ValueError` 异常。
- `except ValueError` 捕获并处理该异常。

**捕获多个异常**：

你可以捕获多个不同类型的异常，并对每种异常进行不同的处理：

```python
try:
    result = int("abc")
except ValueError:
    print("ValueError: Cannot convert string to integer!")
except TypeError:
    print("TypeError: Invalid operation!")
```

在这个示例中：

- 如果发生 `ValueError` 异常，将会被第一个 `except` 块捕获并处理。
- 如果发生 `TypeError` 异常，将会被第二个 `except` 块捕获并处理。

**捕获所有异常**：

你可以使用 `except Exception as e` 捕获所有类型的异常。虽然这种方式可以确保捕获所有异常，但不推荐在生产环境中使用，因为它会掩盖所有异常，包括你可能不希望捕获的异常。

```python
try:
    result = 10 / 0
except Exception as e:
    print(f"An error occurred: {e}")
```

在这个示例中：

- `10 / 0` 会引发 `ZeroDivisionError` 异常。
- `except Exception as e` 会捕获所有类型的异常，因此这个异常也会被捕获，并打印错误信息。

**使用 `else` 和 `finally`**

- `else` 块在 `try` 块没有引发异常时执行。
- `finally` 块无论是否引发异常都会执行。

```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("You cannot divide by zero!")
else:
    print(f"Result is: {result}")
finally:
    print("This will always be executed.")
```

在这个示例中：

- `10 / 2` 不会引发异常，因此会执行 `else` 块中的代码，打印结果。
- 无论是否发生异常，`finally` 块中的代码都会执行。

### 终止与继续执行

**如果在 `except` 块中没有调用 `exit()` 或其他显式的终止程序的语句，程序会继续执行后续的代码**。异常捕获后，程序会继续运行 `except` 块之后的代码，除非发生了无法恢复的错误，或者你显式调用了 `exit()`、`sys.exit()` 或者 `raise` 来终止程序。

**具体情况**：

1. **捕获并处理异常后，继续执行剩余代码**
   如果你在 `except` 块中处理了异常，程序会继续执行 `except` 块之后的代码，而不会停止。
   <font color=red><b>可以显式调用 `exit()`、`sys.exit()` 或者 `raise` 来终止程序</b></font>。

   ```python
   def caught_example():
       print("开始执行")
       try:
           result = 10 / 0  # 这里会产生除零错误
           print("这行不会执行")
       except ZeroDivisionError:
           print("捕获到除零错误")

   print("程序继续执行")  # 这行会执行，因为异常被捕获了
   caught_example()

   # 运行结果:
   # 开始执行
   # 捕获到除零错误
   # 程序继续执行
   ```

   在这个例子中，尽管发生除 0 错误，但程序通过 `except` 捕获了 `ZeroDivisionError` 异常，因此可以继续执行后续的代码（打印 `程序继续执行`）。

2. **捕获并处理异常后，显示终止程序**
   如果你在 `except` 块中处理了异常，程序会继续，<font color=red><b>可以显式调用 `exit()`、`sys.exit()` 或者 `raise` 来终止程序</b></font>。

   ```python
   def caught_example():
       print("开始执行")
       try:
           result = 10 / 0  # 这里会产生除零错误
           print("这行不会执行")
       except ZeroDivisionError:
           print("捕获到除零错误")
           sys.exit(1)

   print("程序继续执行")  # 这行不会执行，因为程序被显示终止
   caught_example()

   # 运行结果:
   # 开始执行
   # 捕获到除零错误
   ```

3. **未捕获异常会终止程序**
   如果你没有捕获异常，程序会被中断。

   ```python
   def uncaught_example():
       print("开始执行")
       # 这里会产生除零错误
       result = 10 / 0
       print("这行不会执行")  # 这行代码不会执行，因为上面的异常未被捕获

   print("程序继续")  # 这行也不会执行
   uncaught_example()

   # 运行结果:
   # 开始执行
   # ZeroDivisionError: division by zero
   ```

### 实际使用示例

文件操作中的异常处理

```python
try:
    with open('example.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("File not found!")
except IOError:
    print("IO error!")
else:
    print(f"File content:\n{content}")
finally:
    print("Finished attempting to read the file.")
```

在这个示例中：

- `open('example.txt', 'r')` 可能引发 `FileNotFoundError` 或 `IOError` 异常。
- 如果文件不存在，将会捕获 `FileNotFoundError` 异常并处理。
- 如果发生其他 I/O 错误，将会捕获 `IOError` 异常并处理。
- 如果没有异常发生，将会执行 `else` 块并打印文件内容。
- 无论是否发生异常，`finally` 块中的代码都会执行。

### 捕获和处理自定义异常

你可以定义和捕获自定义异常，以处理特定的错误情况。

```python
class MyCustomError(Exception):
    pass

try:
    raise MyCustomError("Something went wrong!")
except MyCustomError as e:
    print(f"Caught custom error: {e}")
```

在这个示例中：

- 定义了一个自定义异常 `MyCustomError`。
- 使用 `raise` 语句引发该异常。
- `except MyCustomError as e` 捕获并处理该自定义异常。

### 总结

- `try` 和 `except` 语句用于捕获和处理可能引发的异常。
- 可以捕获特定类型的异常，并进行不同的处理。
- 使用 `else` 块可以在没有异常时执行代码，使用 `finally` 块可以确保代码总是执行。
- 谨慎使用 `except Exception as e`，因为它会捕获所有类型的异常。
- 可以定义和捕获自定义异常，以处理特定的错误情况。

## Python 异常

### 内置异常

在 Python 中，内置了多种异常类型，每种异常类型对应不同的错误情况。以下是一些常见的内置异常类型及其用途：

1. **`Exception`**
   - 所有异常的基类，可以捕获所有类型的异常。
2. **`AssertionError`**
   - `assert` 语句失败时引发，通常用于调试和自检。
3. **`AttributeError`**
   - 尝试访问未定义的对象属性时引发。
4. **`EOFError`**
   - `input()` 函数在输入结束（文件末尾）时引发。
5. **`FloatingPointError`**
   - 浮点数运算错误，如除以零。
6. **`GeneratorExit`**
   - 生成器（generator）关闭时引发。
7. **`ImportError`**
   - 导入模块失败时引发。
8. **`IndexError`**
   - 序列中的索引超出范围时引发。
9. **`KeyError`**
   - 在字典中使用不存在的键时引发。
10. **`KeyboardInterrupt`**
    - 用户中断执行（例如按下 `Ctrl+C`）时引发。
11. **`MemoryError`**
    - 操作系统无法分配内存时引发。
12. **`NameError`**
    - 访问未声明的变量或函数时引发。
13. **`NotImplementedError`**
    - 抽象方法在子类中没有实现时引发。
14. **`OSError`**
    - 操作系统相关的错误，如文件操作失败。
15. **`OverflowError`**
    - 数值运算结果过大无法表示时引发。
16. **`RecursionError`**
    - 递归调用超过最大递归深度时引发。
17. **`ReferenceError`**
    - 弱引用（weak reference）试图访问已经被垃圾回收的对象时引发。
18. **`RuntimeError`**
    - 语法正确但执行时出现问题时引发。
19. **`StopIteration`**
    - 迭代器（iterator）没有更多的值时引发。
20. **`SyntaxError`**
    - Python 语法错误时引发。
21. **`IndentationError`**
    - 缩进错误，通常是因为代码格式不正确引起的。
22. **`TabError`**
    - 使用制表符和空格混合缩进时引发。
23. **`SystemError`**
    - Python 解释器遇到内部问题时引发。
24. **`TypeError`**
    - 操作或函数参数类型不正确时引发。
25. **`UnboundLocalError`**
    - 访问局部变量但该变量未初始化时引发。
26. **`UnicodeError`**
    - Unicode 相关的编码和解码问题时引发。
27. **`ValueError`**
    - 函数接收到的参数类型正确但值不合适时引发。
28. **`ZeroDivisionError`**
    - 除数为零时引发。

这些异常类型提供了处理各种错误情况的方法。在编写代码时，可以根据具体的需求选择捕获和处理适当的异常，从而提高程序的健壮性和可靠性。

**示例**：

**捕获 `IndexError`**

```python
my_list = [1, 2, 3]
try:
    print(my_list[5])
except IndexError as e:
    print(f"IndexError: {e}")
```

**捕获 `KeyError`**

```python
my_dict = {'a': 1, 'b': 2}
try:
    print(my_dict['c'])
except KeyError as e:
    print(f"KeyError: {e}")
```

**捕获 `ValueError`**

```python
try:
    number = int("not_a_number")
except ValueError as e:
    print(f"ValueError: {e}")
```

**捕获 `TypeError`**

```python
try:
    result = "2" + 2
except TypeError as e:
    print(f"TypeError: {e}")
```

**捕获 `FileNotFoundError`**

```python
try:
    with open('non_existent_file.txt', 'r') as file:
        content = file.read()
except FileNotFoundError as e:
    print(f"FileNotFoundError: {e}")
```

### subprocess 异常

在 Python 的 `subprocess` 模块中，有几种常见的异常类型，它们通常在使用子进程执行命令时发生。以下是一些可能会遇到的 `subprocess` 异常及其含义：

1. **`subprocess.CalledProcessError`**
   - 当子进程以非零退出状态（即执行失败）结束时引发。该异常包含返回码和命令输出信息。
2. **`subprocess.TimeoutExpired`**
   - 在设置了超时参数并且超时时间到期后，引发此异常。可以捕获超时情况并进行相应处理。
3. **`OSError`**
   - 在创建子进程时可能会引发 `OSError`，例如找不到指定的可执行文件或者无法执行文件等操作系统级错误。

示例

下面是使用 `subprocess` 模块时可能遇到的异常情况及如何捕获和处理它们的示例：

**捕获 `CalledProcessError`**

```python
import subprocess

try:
    result = subprocess.run(['ls', '/non_existent_directory'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except subprocess.CalledProcessError as e:
    print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}. Output: {e.stdout.decode()} Error: {e.stderr.decode()}")
```

在这个例子中，`subprocess.run` 函数尝试执行 `ls /non_existent_directory` 命令。由于目录不存在，它会抛出 `subprocess.CalledProcessError` 异常，并显示相应的命令、退出状态码以及标准输出和标准错误信息。

**捕获 `TimeoutExpired`**

```python
import subprocess

try:
    result = subprocess.run(['sleep', '10'], timeout=5, check=True)
except subprocess.TimeoutExpired as e:
    print(f"Command '{e.cmd}' timed out after {e.timeout} seconds.")
```

在这个示例中，`subprocess.run` 尝试执行 `sleep 10` 命令，并设置了 5 秒的超时时间。由于超过了设定的超时时间，它会抛出 `subprocess.TimeoutExpired` 异常，并显示相应的命令和超时时间信息。

**捕获 `OSError`**

```python
import subprocess

try:
    result = subprocess.run(['non_existent_command'], check=True)
except OSError as e:
    print(f"OS error: {e}")
```

在这个例子中，`subprocess.run` 尝试执行一个不存在的命令 `non_existent_command`，这会导致 `OSError` 异常被抛出，并显示相应的操作系统错误信息。

## 函数入参类型

在 Python 中，函数参数的行为取决于传入的对象类型。具体来说，**不可变类型**（如 `int`, `float`, `str`, `tuple` 等）会在函数内部传递副本，而**可变类型**（如 `list`, `dict`, `set`, 自定义对象等）会传递对对象的引用。因此，修改函数内的参数是否会影响外部变量，取决于你传入的是哪种类型。

1. **对于不可变类型（如 `str`, `int`, `tuple` 等）**

   如果你在函数内部修改一个不可变类型的参数，实际上是创建了一个新的对象，并将其绑定到局部变量，因此**函数内修改不会直接影响原始的外部变量**。

   如果你希望函数修改外部的不可变类型，你可以将不可变类型**包装成可变类型**（如 `list` 或 `dict`），或者**返回修改后的值**，并在调用时将返回值赋给外部变量。

2. **对于可变类型（如 `list`, `dict` 等）**

   如果你在函数内部修改一个可变类型的参数（比如修改列表的元素或字典的键值对），**这些修改会直接影响外部变量**，因为传入的是对原始对象的引用。

## 可变参数

在 Python 中，可变参数（variadic arguments）允许你编写能够接受可变数量参数的函数。这在编写需要处理不定数量输入的函数时特别有用。Python 提供了**两种**主要的可变参数：`*args` 和 `**kwargs`。使 Python 函数具有很高的灵活性和可扩展性。

- `*args` 用于传递不定数量的**非关键字参数**（以元组形式传递）。
- `**kwargs` 用于传递不定数量的**关键字参数**（以字典形式传递）。
- 可以在函数定义中同时使用 `*args` 和 `**kwargs` 来处理**所有类型**的输入参数。<b>使用时 `*args` 必须出现在 `**kwargs` 之前</b>。
- 在调用函数时，可以使用 `*` 和 `**` 来解包序列和字典，分别作为非关键字和关键字参数传递。

> :bulb:注意：
>
> `*args` 和 `**kwargs` 只是惯用的命名方式，实际上，`*` 或 `**` 后面的名字可以是任何有效的变量名。

### 使用 `*args` 处理任意数量的非关键字参数

- `*args` 用于接收不定数量的非关键字参数，并将它们作为元组传递给函数。
- 当你在定义函数时使用`*args`，可以传入任意数量的参数。

**示例：**

```python
def my_function(*args):
    for arg in args:
        print(arg)

# 调用函数并传入不同数量的参数
my_function(1, 2, 3)
# 输出:
# 1
# 2
# 3
```

**解释：**

- `*args` 收集所有传入的非关键字参数，并将它们放入一个名为 `args` 的元组中。
- 在函数内部，你可以**像访问普通元组**那样访问这些参数。

### 使用 `**kwargs` 处理任意数量的关键字参数

- `**kwargs` 用于接收不定数量的关键字参数，并将它们作为字典传递给函数。
- 当你在定义函数时使用 `**kwargs`，可以传入任意数量的键值对。

**示例：**

```python
def my_function(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} = {value}")

# 调用函数并传入不同数量的关键字参数
my_function(name="Alice", age=30, city="New York")
# 输出:
# name = Alice
# age = 30
# city = New York
```

**解释：**

- `**kwargs` 收集所有传入的关键字参数，并将它们放入一个名为 `kwargs` 的字典中。
- 在函数内部，你可以**像访问普通字典**那样访问这些参数。

### 同时使用 `*args` 和 `**kwargs`

你可以在同一个函数中同时使用 `*args` 和 `**kwargs`。这使得该函数能够接受任意数量的非关键字参数和关键字参数。

**示例：**

```python
def my_function(*args, **kwargs):
    print("Non-keyword arguments:", args)
    print("Keyword arguments:", kwargs)

# 调用函数并传入非关键字参数和关键字参数
my_function(1, 2, 3, name="Alice", age=30)
# 输出:
# Non-keyword arguments: (1, 2, 3)
# Keyword arguments: {'name': 'Alice', 'age': 30}
```

**解释：**

- `*args` 收集所有的非关键字参数并将其作为元组传递。
- `**kwargs` 收集所有的关键字参数并将其作为字典传递。
- **在同一个函数中使用这两种参数时，`*args` 必须出现在 `**kwargs` 之前\*\*。

### 使用 `*args` 和 `**kwargs` 在函数调用时解包参数

在调用函数时，你可以使用 `*` 和 `**` 来解包列表、元组或字典中的参数。

**示例：**

```python
def my_function(a, b, c):
    print(a, b, c)

# 使用元组解包
args = (1, 2, 3)
my_function(*args)  # 输出: 1 2 3

# 使用字典解包
kwargs = {'a': 10, 'b': 20, 'c': 30}
my_function(**kwargs)  # 输出: 10 20 30
```

## 内置字符串

Python 的字符串（`str` 类型）提供了许多内置方法，用于处理文本数据。以下是一些常用的字符串方法及其功能。

1. `str.capitalize()`

   将字符串的第一个字符转为大写，其余字符转为小写。

   ```python
   s = "hello"
   print(s.capitalize())  # 输出: "Hello"
   ```

2. `str.lower()`

   将字符串中的所有字符转换为小写。

   ```python
   s = "HELLO"
   print(s.lower())  # 输出: "hello"
   ```

3. `str.upper()`

   将字符串中的所有字符转换为大写。

   ```python
   s = "hello"
   print(s.upper())  # 输出: "HELLO"
   ```

4. `str.title()`

   将字符串中的每个单词的首字母转为大写，其他字母转为小写。

   ```python
   s = "hello world"
   print(s.title())  # 输出: "Hello World"
   ```

5. `str.strip()`

   移除字符串两端的空白字符（包括空格、换行符等）。

   ```python
   s = "  hello  "
   print(s.strip())  # 输出: "hello"
   ```

6. `str.lstrip()` 和 `str.rstrip()`

   - `str.lstrip()` 移除字符串左边的空白字符。
   - `str.rstrip()` 移除字符串右边的空白字符。

   ```python
   s = "  hello  "
   print(s.lstrip())  # 输出: "hello  "
   print(s.rstrip())  # 输出: "  hello"
   ```

7. `str.replace(old, new, count)`

   替换字符串中的指定子字符串。如果提供了 `count`，则只替换前 `count` 次出现的子字符串。

   ```python
   s = "hello world"
   print(s.replace("world", "Python"))  # 输出: "hello Python"
   ```

8. `str.split(sep, maxsplit)`

   将字符串根据指定的分隔符 `sep` 切割成多个子字符串。如果指定了 `maxsplit`，则最多切割 `maxsplit` 次。

   ```python
   s = "apple,banana,orange"
   print(s.split(","))  # 输出: ['apple', 'banana', 'orange']
   print(s.split(",", 1))  # 输出: ['apple', 'banana,orange']
   ```

9. `str.join(iterable)`

   将可迭代对象（如列表或元组）中的元素连接成一个新的字符串，并使用字符串作为分隔符。

   ```python
   words = ["hello", "world"]
   print(" ".join(words))  # 输出: "hello world"
   ```

10. `str.find(sub)`

    返回子字符串 `sub` 在字符串中第一次出现的位置，如果未找到返回 `-1`。

    ```python
    s = "hello world"
    print(s.find("world"))  # 输出: 6
    print(s.find("Python"))  # 输出: -1
    ```

11. `str.index(sub)`

    与 `find` 类似，但如果未找到子字符串，`index` 会抛出 `ValueError` 异常。

    ```python
    s = "hello world"
    print(s.index("world"))  # 输出: 6
    # print(s.index("Python"))  # 会抛出 ValueError
    ```

12. `str.count(sub)`

    返回子字符串 `sub` 在字符串中出现的次数。

    ```python
    s = "hello hello world"
    print(s.count("hello"))  # 输出: 2
    ```

13. `str.startswith(prefix)`

    判断字符串是否以 `prefix` 开头，返回布尔值。

    ```python
    s = "hello world"
    print(s.startswith("hello"))  # 输出: True
    print(s.startswith("world"))  # 输出: False
    ```

14. `str.endswith(suffix)`

    判断字符串是否以 `suffix` 结尾，返回布尔值。

    ```python
    s = "hello world"
    print(s.endswith("world"))  # 输出: True
    print(s.endswith("hello"))  # 输出: False
    ```

15. `str.isdigit()`

    判断字符串是否只包含数字字符，如果是，返回 `True`，否则返回 `False`。

    ```python
    s = "12345"
    print(s.isdigit())  # 输出: True
    print("hello".isdigit())  # 输出: False
    ```

16. `str.isalpha()`

    判断字符串是否只包含字母字符。

    ```python
    s = "hello"
    print(s.isalpha())  # 输出: True
    print("hello123".isalpha())  # 输出: False
    ```

17. `str.isalnum()`

    判断字符串是否只包含字母或数字字符。

    ```python
    s = "hello123"
    print(s.isalnum())  # 输出: True
    print("hello!".isalnum())  # 输出: False
    ```

18. `str.islower()` 和 `str.isupper()`

    - `str.islower()` 判断字符串是否全部为小写字母。
    - `str.isupper()` 判断字符串是否全部为大写字母。

    ```python
    s = "hello"
    print(s.islower())  # 输出: True
    print(s.isupper())  # 输出: False
    ```

19. `str.isnumeric()`

    判断字符串是否只包含数字字符。

    ```python
    s = "123"
    print(s.isnumeric())  # 输出: True
    ```

20. `str.zfill(width)`

    将字符串填充到指定的宽度 `width`，并在左侧填充零。如果字符串长度大于或等于 `width`，则返回原字符串。

    ```python
    s = "42"
    print(s.zfill(5))  # 输出: "00042"
    ```

21. `str.rjust(width, fillchar)` 和 `str.ljust(width, fillchar)`

    - `str.rjust(width, fillchar)` 将字符串右对齐，左侧填充 `fillchar`，直到达到指定宽度。
    - `str.ljust(width, fillchar)` 将字符串左对齐，右侧填充 `fillchar`，直到达到指定宽度。

    ```python
    s = "42"
    print(s.rjust(5, "0"))  # 输出: "00042"
    print(s.ljust(5, "0"))  # 输出: "42000"
    ```

22. `str.partition(sep)`

    将字符串按照分隔符 `sep` 分为三部分：分隔符前的部分、分隔符本身和分隔符后的部分，返回一个元组。如果找不到分隔符，返回原字符串和两个空字符串。

    ```python
    s = "apple,banana,orange"
    print(s.partition(","))  # 输出: ('apple', ',', 'banana,orange')
    ```

## itertools

`itertools.product` 是 Python 中 `itertools` 模块的一个函数，它用于生成多个输入可迭代对象的笛卡尔积（Cartesian product），即所有可能的元素组合。可以把它看作是多重嵌套的 `for` 循环的简洁实现。返回的是一个迭代器，而不是一个列表

1. **基本用法**

   `itertools.product` 接受多个可迭代对象作为输入（比如列表、元组、字符串等），并返回所有输入序列的笛卡尔积。返回的结果是一个生成器，产生所有的组合。

   示例：

   ```python
   import itertools

   # 三个列表的笛卡尔积
   a = [1, 2]
   b = ['x', 'y']
   c = ['a', 'b']
   result = itertools.product(a, b, c)

   for item in result:
       print(item)
   ```

   输出：

   ```log
   (1, 'x', 'a')
   (1, 'x', 'b')
   (1, 'y', 'a')
   (1, 'y', 'b')
   (2, 'x', 'a')
   (2, 'x', 'b')
   (2, 'y', 'a')
   (2, 'y', 'b')
   ```

   解释：

   - `itertools.product(a, b, c)` 返回的是 `a` 和 `b` 和 `c` 的所有可能组合。
   - 它等同于：

     ```python
     for i in a:
         for j in b:
            for k in c:
                print((i, j, k))
     ```

2. **重复的笛卡尔积**

   `itertools.product` 还支持重复的输入序列，即你可以指定一个可迭代对象重复多次。

   示例：

   ```python
   import itertools

   # 重复3次的笛卡尔积
   a = [1, 2]
   result = itertools.product(a, repeat=3)

   for item in result:
       print(item)
   ```

   **输出：**

   ```log
   (1, 1, 1)
   (1, 1, 2)
   (1, 2, 1)
   (1, 2, 2)
   (2, 1, 1)
   (2, 1, 2)
   (2, 2, 1)
   (2, 2, 2)
   ```

   解释：

   - `repeat=3` 表示生成 `a` 的三重笛卡尔积，相当于对 `a` 进行三次重复。

3. **处理空的可迭代对象**

   如果传入空的可迭代对象，`itertools.product` 返回的是一个空的迭代器。

   示例：

   ```python
   import itertools

   # 空的可迭代对象
   result = itertools.product([], [1, 2])

   for item in result:
       print(item)
   ```

   输出：

   ```bash
   # 输出为空，没有任何结果
   ```

4. **常见应用**

`itertools.product` 通常用于以下场景：

- **生成所有可能的排列组合**：比如在密码学、排列组合问题、测试用例生成等领域。
- **多维度的搜索**：比如遍历多维的空间（如网格搜索、模拟等）。

**总结**：

- `itertools.product(*iterables, repeat=1)` 用来生成多个可迭代对象的笛卡尔积，返回一个生成器。
- 可以通过 `repeat` 参数指定重复生成某个可迭代对象的笛卡尔积。
- 适合用于需要生成多层循环或所有组合的场景。

## exit() 和 sys.exit()

`exit()` 和 `sys.exit()` 都是用于终止程序的函数，但它们之间有一些细微的区别。具体来说，`exit()` 是一个内置函数，而 `sys.exit()` 来自于 `sys` 模块。它们的主要区别在于：

1. **`exit()`**

   - `exit()` 是一个内置函数，通常用于交互式命令行会话中，或者用来在脚本的最后退出。
   - 它会引发一个 `SystemExit` 异常，程序可以捕获这个异常。如果没有捕获，它会终止程序并返回退出码 0（表示正常退出）。
   - 如果你想要在 exit() 中自定义退出状态码，可以传递一个参数，**这个参数会被作为退出码传递给操作系统**。
   - 它通常是在 Python 解释器交互模式下使用，或者在脚本中用来优雅地退出。

   示例：

   ```python
   # 直接在交互式 Python 环境中使用 exit()
   exit()  # 正常退出

   # 在脚本中使用 exit()
   print("程序即将退出...")
   exit()  # 正常退出，结束程序
   exit(1) # 使用非零退出码
   ```

2. **`sys.exit()`**

   - `sys.exit()` 来自于 `sys` 模块，它更常用于脚本编程中。它和 `exit()` 功能相同，也会引发一个 `SystemExit` 异常，但它在 `sys` 模块中。
   - `sys.exit()` 更常用于编写非交互式的程序，它也接受一个可选的退出码参数（可以是整数或字符串），表示程序的退出状态。退出码 `0` 通常表示成功，非零值表示错误。
   - `sys.exit()` 更常用于需要根据某些条件退出程序时，尤其是在较复杂的应用中，比如在处理命令行参数时，或者在脚本中的异常处理。

   示例：

   ```python
   import sys

   print("程序即将退出...")
   sys.exit()  # 正常退出，结束程序

   # 使用非零退出码
   sys.exit(1)  # 表示程序由于错误退出，退出码为 1
   ```

3. **关键区别总结**

   | 特性         | `exit()`                       | `sys.exit()`                   |
   | ------------ | ------------------------------ | ------------------------------ |
   | 所在模块     | 内置函数                       | `sys` 模块                     |
   | 常用场景     | 交互式 Python 环境，简单脚本   | 脚本编程，异常处理，复杂的应用 |
   | 退出状态码   | 默认为 0（正常退出），可自定义 | 可以自定义退出状态码           |
   | 是否可以捕获 | 可以被捕获（因为它是异常）     | 也可以被捕获（因为它是异常）   |
   | 常见使用场景 | 在交互模式中简单退出           | 用于复杂程序，处理错误状态退出 |

4. **捕获 `SystemExit` 异常**

   无论是 `exit()` 还是 `sys.exit()`，它们都会抛出 `SystemExit` 异常，通常在脚本中不需要捕获这个异常，但如果需要，你可以捕获它来处理退出逻辑。

   示例：

   ```python
   import sys

   try:
       print("程序即将退出...")
       sys.exit(1)
   except SystemExit as e:
       print(f"捕获到退出异常，退出码为：{e.code}")

   # 输出：
   # 复制编辑程序即将退出...
   # 捕获到退出异常，退出码为：1
   ```

**总结**：

- 如果你在交互式 Python 环境中，或者你只是想简单地退出，可以使用 `exit()`。
- 对于更复杂的脚本或程序，尤其是需要在脚本中明确指定退出码或者与其他模块进行交互时，`sys.exit()` 更加常用。

## 字典

假定变量 test_cases 是一个字典，则：

```python
for k in test_cases:
    main(**test_cases[k])
```

等价于：

```python
for k, v in test_cases.items():
    main(**v)
```

- `test_cases` 是一个字典，遍历它时，默认遍历**键**。

- `test_cases[k]` 获取的是对应的值（也是一个字典）。

- `**test_cases[k]` **字典解包**：

  - `**` 操作符用于将字典的键值对作为**关键字参数**传递给函数 `main()`。

  - 例如：

    ```python
    main(a=3, b=False, c=16, d=128, e=False)
    ```

  - 这样 `main()` 就能直接接收这些参数，而不需要手动写出 `main(a=3, b=False, ...)`。

## 枚举

Python 提供了 enum 模块，可以使用 Enum 类定义枚举：

此模块定义了四个枚举类，它们可被用来定义名称和值的不重复集合: Enum, IntEnum, Flag 和 IntFlag。 此外还定义了一个装饰器 unique() 和一个辅助类 auto。

- `class enum.Enum`：用于创建枚举型常数的基类。 请参阅 Functional API 小节了解另一种替代性的构建语法。

- `class enum.IntEnum`：用于创建同时也是 int 的子类的枚举型常数的基类。

- `class enum.IntFlag`：此基类用于创建可使用按位运算符进行组合而不会丢失其 IntFlag 成员资格的枚举常量。 IntFlag 成员同样也是 int 的子类。

- `class enum.Flag`：此基类用于创建枚举常量 可使用按位运算符进行组合而不会丢失其 Flag 成员资格的枚举常量。

- `enum.unique()`：此 Enum 类装饰器可确保只将一个名称绑定到任意一个值。

- `class enum.auto`：实例会被替换为一个可作为 Enum 成员的适当的值。 初始值从 1 开始。

- 3.6 新版功能: Flag, IntFlag, auto

**示例：**

```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print(Color.RED)       # Color.RED
print(Color.RED.value) # 1
print(Color.RED.name)  # 'RED'
```

特点：

- `Enum` 成员是 **唯一的**，即相同的值不会指向不同的枚举项。
- 不能修改枚举值（不可变）。
- 可以通过 `Color(1)` 反向查找枚举项。

**使用 `Enum` 并使用 `is` 进行判等**

```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

def check_color(color: Color):
    if color is Color.RED:  # 推荐使用 `is` 进行判等
        print("Color is RED")
    elif color is Color.GREEN:
        print("Color is GREEN")
    elif color is Color.BLUE:
        print("Color is BLUE")
    else:
        print("Unknown color")

check_color(Color.RED)  # 输出: Color is RED
```

为什么用 `is` 而不是 `==`？

- `is` **保证是同一个对象**，不会因为 `Enum` 继承类的特殊性导致错误。
- `==` 也可以使用，但 `is` 更推荐用于 `Enum` 的判等。

## eval()

`eval()` 是 Python 内置函数，用于执行字符串形式的 Python 表达式，并返回表达式的计算结果。它的基本语法是：

```python
eval(expression, globals=None, locals=None)
```

- **expression**: 必须是一个字符串，表示要执行的 Python 表达式。
- **globals** (可选): 一个字典，表示全局命名空间。默认为 `None`，即使用当前的全局命名空间。
- **locals** (可选): 一个字典，表示局部命名空间。默认为 `None`，即使用当前的局部命名空间。

**用法示例：**

```python
x = 10
expression = "x * 2"
result = eval(expression)  # 结果是 20
print(result)
```

**高级用法：**

你可以通过 `globals` 和 `locals` 参数控制作用域。例如：

```python
x = 5
globals_dict = {"x": 10}
locals_dict = {}
expression = "x + 2"

# 使用自定义的全局作用域
result = eval(expression, globals_dict, locals_dict)  # 结果是 12
print(result)
```

**安全性注意：**

`eval()` 是一个非常强大的功能，但由于它会执行传入的任意代码，因此它有潜在的安全风险。如果用户输入恶意代码，可能会执行不安全的操作。因此，尽量避免使用 `eval()`，尤其是在处理不可信的输入时。如果需要执行字符串中的数学表达式，考虑使用 `ast.literal_eval()`，它更安全，只允许解析常见的字面量数据（如字符串、数字、列表、字典等）。

**总结：**

`eval()` 主要用于动态执行字符串形式的 Python 表达式，但需要谨慎使用，特别是在涉及不受信任的数据时。

# PyQt5

## [PyQt5 关于 Qt Designer 的初步应用和打包过程详解](http://www.codebaoku.com/it-python/it-python-223940.html)

在 PyQt 中编写 UI 界面可以直接通过代码来实现，也可以通过 Qt Designer 来完成。Qt Designer 的设计符合 MVC 的架构，其实现了视图和逻辑的分离，从而实现了开发的便捷。Qt Designer 中的操作方式十分灵活，其通过拖拽的方式放置控件可以随时查看控件效果。Qt Designer 生成的.ui 文件（实质上是 XML 格式的文件）也可以通过 pyuic5 工具转换成.py 文件。 Qt Designer 随 PyQt5-tools 包一起安装，其安装路径在 “Python 安装路径\Lib\site-packages\pyqt5-tools”下。若要启动 Qt Designer 可以直接到上述目录下，双击 designer.exe 打开 Qt Designer；或将上述路径加入环境变量，在命令行输入 designer 打开；或在 PyCharm 中将其配置为外部工具打开。下面以 PyCharm 为例，讲述 PyCharm 中 Qt Designer 的配置方法。
