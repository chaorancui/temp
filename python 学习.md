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

## 可变参数

在 Python 中，可变参数（variadic arguments）允许你编写能够接受可变数量参数的函数。这在编写需要处理不定数量输入的函数时特别有用。Python 提供了**两种**主要的可变参数：`*args` 和 `**kwargs`。使 Python 函数具有很高的灵活性和可扩展性。

- `*args` 用于传递不定数量的**非关键字参数**（以元组形式传递）。
- `**kwargs` 用于传递不定数量的**关键字参数**（以字典形式传递）。
- 可以在函数定义中同时使用 `*args` 和 `**kwargs` 来处理**所有类型**的输入参数。**使用时 `*args` 必须出现在 `**kwargs` 之前\*\*。
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

# python 模板

## Python 模板引擎

在 Python 中，模板引擎用于生成基于模板的动态内容。模板引擎常用于网页生成、文档生成、配置文件生成等场景。以下是一些常用的 Python 模板引擎及其示例。

### 常用的 Python 模板引擎

1. **Jinja2**：一个功能强大的模板引擎，常用于 Web 框架如 Flask。
2. **Mako**：一个快速的模板引擎，支持嵌入式 Python 表达式。
3. **Django Templates**：Django 框架自带的模板引擎。

### Jinja2 示例

#### 安装 Jinja2

```bash
pip install Jinja2
```

#### 使用 Jinja2 渲染模板

```python
from jinja2 import Template

# 模板内容
template_content = """
Hello, {{ name }}!
You have {{ notifications }} new notifications.
"""

# 创建模板对象
template = Template(template_content)

# 渲染模板
output = template.render(name="Alice", notifications=5)

print(output)
```

输出：

```log
Hello, Alice!
You have 5 new notifications.
```

#### 复杂示例：循环和条件语句

```python
from jinja2 import Template

# 模板内容
template_content = """
{% if items %}
<ul>
    {% for item in items %}
    <li>{{ item }}</li>
    {% endfor %}
</ul>
{% else %}
<p>No items found.</p>
{% endif %}
"""

# 创建模板对象
template = Template(template_content)

# 渲染模板
output = template.render(items=["apple", "banana", "cherry"])

print(output)
```

输出：

```log
<ul>
    <li>apple</li>
    <li>banana</li>
    <li>cherry</li>
</ul>
```

### Mako 示例

#### 安装 Mako

```bash
pip install Mako
```

#### 使用 Mako 渲染模板

```python
from mako.template import Template

# 模板内容
template_content = """
Hello, ${name}!
You have ${notifications} new notifications.
"""

# 创建模板对象
template = Template(template_content)

# 渲染模板
output = template.render(name="Bob", notifications=10)

print(output)
```

输出：

```plaintext
Hello, Bob!
You have 10 new notifications.
```

#### 复杂示例：循环和条件语句

```python
from mako.template import Template

# 模板内容
template_content = """
<%!
    def format_item(item):
        return item.capitalize()
%>
% if items:
<ul>
    % for item in items:
    <li>${format_item(item)}</li>
    % endfor
</ul>
% else:
<p>No items found.</p>
% endif
"""

# 创建模板对象
template = Template(template_content)

# 渲染模板
output = template.render(items=["apple", "banana", "cherry"])

print(output)
```

输出：

```log
<ul>
    <li>Apple</li>
    <li>Banana</li>
    <li>Cherry</li>
</ul>
```

### Django Templates 示例

#### 安装 Django

```bash
pip install Django
```

#### 使用 Django 模板渲染

```python
from django.template import Template, Context

# 模板内容
template_content = """
Hello, {{ name }}!
You have {{ notifications }} new notifications.
"""

# 创建模板对象
template = Template(template_content)

# 创建上下文对象
context = Context({"name": "Charlie", "notifications": 3})

# 渲染模板
output = template.render(context)

print(output)
```

输出：

```plaintext
Hello, Charlie!
You have 3 new notifications.
```

#### 复杂示例：循环和条件语句

```python
from django.template import Template, Context

# 模板内容
template_content = """
{% if items %}
<ul>
    {% for item in items %}
    <li>{{ item }}</li>
    {% endfor %}
</ul>
{% else %}
<p>No items found.</p>
{% endif %}
"""

# 创建模板对象
template = Template(template_content)

# 创建上下文对象
context = Context({"items": ["apple", "banana", "cherry"]})

# 渲染模板
output = template.render(context)

print(output)
```

输出：

```plaintext
<ul>
    <li>apple</li>
    <li>banana</li>
    <li>cherry</li>
</ul>
```

### 总结

- **Jinja2**：强大且广泛使用，支持复杂的逻辑、过滤器和扩展。
- **Mako**：速度快，支持嵌入式 Python 代码，适合高性能需求的应用。
- **Django Templates**：简单易用，适合使用 Django 框架的项目。

选择合适的模板引擎取决于具体的需求和使用场景。在 Web 开发中，Jinja2 是一个很好的选择，而对于需要高性能的应用，Mako 是一个不错的选择。如果你在使用 Django 框架，Django Templates 是默认且集成良好的选择。

## python 模板过滤器

Python 中的模板引擎（如 Jinja2 和 Django 模板）提供了丰富的过滤器（filters），用于对模板中的变量进行各种格式化、转换和处理操作。以下是常见的模板引擎过滤器及其用法总结：

### 常见过滤器

1. **字符串处理**

   - `upper`: 将字符串转换为大写。
   - `lower`: 将字符串转换为小写。
   - `capitalize`: 将字符串的首字母转换为大写，其他字母转换为小写。
   - `title`: 将字符串中每个单词的首字母转换为大写。

   ```django
   {{ variable | upper }}
   {{ variable | lower }}
   {{ variable | capitalize }}
   {{ variable | title }}
   ```

2. **默认值处理**

   - `default`: 如果变量不存在或为空，则使用指定的默认值。

   ```django
   {{ variable | default:"Default Value" }}
   ```

3. **列表和字典操作**

   - `length`: 返回列表、字符串等的长度。
   - `join`: 将列表按指定分隔符连接成字符串。
   - `dictsort`: 对字典按键或值进行排序。

   ```django
   {{ list_var | length }}
   {{ list_var | join:", " }}
   {{ dict_var | dictsort }}
   ```

4. **日期和时间格式化**

   - `date`: 格式化日期和时间。

   ```django
   {{ date_var | date:"Y-m-d H:i:s" }}
   ```

5. **数值处理**

   - `floatformat`: 格式化浮点数。
   - `intcomma`: 给整数添加千位分隔符。

   ```django
   {{ float_var | floatformat:"2" }}
   {{ int_var | intcomma }}
   ```

### 示例

1. 使用 Jinja2 模板引擎示例

   ```python
   from jinja2 import Template

   # 模板内容
   template_content = """
   Original: {{ variable }}
   Upper case: {{ variable | upper }}
   Lower case: {{ variable | lower }}
   Capitalized: {{ variable | capitalize }}
   Default: {{ missing_variable | default:"Default Value" }}
   Length: {{ list_var | length }}
   Join: {{ list_var | join:", " }}
   Date: {{ date_var | date:"Y-m-d" }}
   """

   # 创建模板对象
   template = Template(template_content)

   # 渲染模板，传入上下文数据
   context = {
       'variable': 'Hello World',
       'list_var': ['apple', 'banana', 'cherry'],
       'date_var': datetime.date(2023, 1, 25)
   }

   output = template.render(context)

   print(output)
   ```

2. 使用 Django 模板引擎示例

   ```python
   from django.template import Template, Context
   from datetime import datetime

   # 模板内容
   template_content = """
   Original: {{ variable }}
   Upper case: {{ variable | upper }}
   Lower case: {{ variable | lower }}
   Capitalized: {{ variable | capitalize }}
   Default: {{ missing_variable | default:"Default Value" }}
   Length: {{ list_var | length }}
   Join: {{ list_var | join:", " }}
   Date: {{ date_var | date:"Y-m-d" }}
   """

   # 创建模板对象
   template = Template(template_content)

   # 创建上下文对象
   context = {
       'variable': 'Hello World',
       'list_var': ['apple', 'banana', 'cherry'],
       'date_var': datetime.now()
   }

   # 渲染模板
   output = template.render(Context(context))

   print(output)
   ```

### 总结

- 模板引擎过滤器允许在模板中对变量进行各种格式化、转换和处理操作，使模板更加灵活和强大。
- 不同的模板引擎可能支持不同的过滤器语法和过滤器集合，具体使用时需要参考相应的模板引擎文档。
- 过滤器的使用可以大大简化模板中对输出内容的处理和格式化操作，提高代码的可读性和维护性。

## python 模板变量展开

在 Python 中，可以在模板中传入一个结构体（通常指**字典**或自定义对象），然后在模板中展开其属性或键值对。这种操作通常用于**动态生成文本或格式化输出**，其中模板可以根据传入的数据动态地填充值。

### 使用字典展开

如果传入的结构体是一个字典，可以使用字典展开的方式将其属性或键值对传递给模板。

```python
from string import Template

data = {
    "name": "Alice",
    "age": 30,
    "city": "Wonderland",
    "job": "Engineer"
}

template_str = "Hello, my name is $name. I am $age years old. I live in $city and work as a $job."
template = Template(template_str)
result = template.substitute(data)
print(result)
```

输出：

```log
Hello, my name is Alice. I am 30 years old. I live in Wonderland and work as a Engineer.
```

在这个示例中，`data` 是一个字典，包含了名为 `name`、`age`、`city` 和 `job` 的键值对。模板字符串中的 `$name`、`$age`、`$city` 和 `$job` 被模板引擎替换为字典中相应的值。

### 使用对象展开

如果传入的结构体是一个自定义对象，你可以通过对象的属性来填充模板。

```python
from string import Template

class Person:
    def __init__(self, name, age, city, job):
        self.name = name
        self.age = age
        self.city = city
        self.job = job

data = Person("Alice", 30, "Wonderland", "Engineer")

template_str = "Hello, my name is $name. I am $age years old. I live in $city and work as a $job."
template = Template(template_str)
result = template.substitute(vars(data))  # 使用 vars() 函数将对象属性转换为字典
print(result)
```

输出：

```log
Hello, my name is Alice. I am 30 years old. I live in Wonderland and work as a Engineer.
```

在这个示例中，`data` 是一个 `Person` 对象，它具有 `name`、`age`、`city` 和 `job` 属性。**使用 `vars(data)` 将对象的属性转换为字典**，然后传递给模板。

> **使用`vars()`函数时的注意事项：**
>
> 1. **仅适用于具有`__dict__`属性的对象**：`vars()`函数仅适用于那些有`__dict__`属性的对象（通常是用户定义的对象）。对于内置对象（如整数、字符串等），调用`vars()`会引发`TypeError`。
> 2. **只包含实例变量**：返回的字典**只包含对象的实例变量**，不包括类变量或方法。
> 3. **动态属性**：如果对象在**运行时动态添加了新的属性**，这些属性也会包含在`vars()`返回的字典中。

### 使用 Jinja2 + 对象展开

在使用 Jinja2 渲染模板时，可以通过 `template.render` 方法**将多个对象（变量）传递给模板**。你可以在 `render` 方法中**直接传递关键字参数**，也可以**传递一个包含多个变量的字典**。

```python
from jinja2 import Template

class Person:
    def __init__(self, name, age, city, job):
        self.name = name
        self.age = age
        self.city = city
        self.job = job

data = Person("Alice", 30, "Wonderland", "Engineer")

template_str = "Hello, my name is {{ person.name }}. I am {{ person.age }} years old. I live in {{ person.city }} and work as a {{ person.job }}."
template = Template(template_str)
result = template.render(person=data)
print(result)
```

输出：

```log
Hello, my name is Alice. I am 30 years old. I live in Wonderland and work as a Engineer.
```

在这个示例中，使用了 Jinja2 的 `Template` 类和 `render` 方法，将 `Person` 对象 `data` 传递给模板，然后使用 `{{ person.name }}`、`{{ person.age }}` 等表达式展开模板。

**传递多个对象**：

```python
from jinja2 import Environment, FileSystemLoader

# 创建一个 Jinja2 环境，加载模板文件
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

# 加载模板
template = env.get_template('template.html')

# 定义模板中使用的多个变量
title = 'My Web Page'
header = 'Welcome to My Web Page'
content = 'This is a simple web page rendered with Jinja2.'
items = ['Item 1', 'Item 2', 'Item 3']
user = {
    'name': 'John Doe',
    'age': 30,
    'email': 'john.doe@example.com'
}

# 渲染模板并传递多个对象
output = template.render(
    title=title,
    header=header,
    content=content,
    items=items,
    user=user
)

# 打印渲染结果
print(output)
```

# python 面向对象

## 类方法和类函数

在 Python 中，类方法（classmethod）和普通的类函数（class function）有一些区别，主要体现在它们的装饰器和第一个参数上。

### 类方法（classmethod）

类方法**使用 `@classmethod` 装饰器标识**，并且**第一个参数通常被命名为 `cls`**，表示调用该方法的类本身。类方法可以**通过类名或实例来调用**，但通常建议使用类名调用类方法。

**示例**：

```python
class MyClass:
    class_attr = 10

    @classmethod
    def class_method(cls):
        print(f"Class method called with class attribute: {cls.class_attr}")

# 调用类方法
MyClass.class_method()  # 输出: Class method called with class attribute: 10
```

在这个示例中，`class_method` 是一个类方法，通过 `@classmethod` 装饰器标识。`cls` 参数表示调用该方法的类本身，可以用来访问类的属性和方法。

### 类函数（普通的类方法）

普通的类方法是指在类中定义的普通方法，**没有使用 `@classmethod` 装饰器标识**。这些方法**可以通过实例访问**，并且**第一个参数通常是 `self`**，表示调用该方法的实例本身。

**示例**：

```python
class MyClass:
    def __init__(self, x):
        self.x = x

    def instance_method(self):
        print(f"Instance method called with instance attribute: {self.x}")

# 创建实例并调用实例方法
obj = MyClass(5)
obj.instance_method()  # 输出: Instance method called with instance attribute: 5
```

在这个示例中，`instance_method` 是一个普通的类方法，可以通过实例 `obj` 来调用，`self` 参数表示调用该方法的实例本身，可以访问实例的属性和方法。

### 区别总结

- **类方法**：
  - 使用 `@classmethod` 装饰器标识。
  - 第一个参数通常命名为 `cls`，表示调用该方法的类本身。
  - 可以通过类名或实例调用，但通常建议使用类名调用。
  - 用于在类级别上操作或管理类的属性和方法。
- **普通的类方法（类函数）**：
  - 没有使用 `@classmethod` 装饰器标识。
  - 第一个参数通常命名为 `self`，表示调用该方法的实例本身。
  - 只能通过实例调用。
  - 用于操作或访问实例的属性和方法。

**选择使用类方法还是普通的类方法**：

- 使用 **类方法**：
  - 当方法需要访问和操作类的属性或者需要在**类级别上进行操作时，应使用类方法**。
  - 类方法适用于实现工厂方法或者管理类级别的状态。
- 使用 **普通的类方法（类函数）**：
  - 当方法需要访问和**操作实例的属性时，应使用普通的类方法**。
  - 普通的类方法适用于实现与特定实例相关的逻辑和操作。

## 获取类的变量

在 Python 中，获取类的变量（包括**类变量**和**实例变量**）可以通过内置函数和标准库模块来实现。主要的方法有两种：使用 **`__dict__` 属性**和 **`inspect` 模块**。

> 在继承场景下，当使用`__dict__`在子类实例上时，它不会显示父类的成员。这是因为`__dict__`只包含对象的直接属性，而不包含继承自父类的属性。这种情况若要获得父类的变量，需要自己实现函数。

### 获取类变量

类变量是在**类定义中直接定义的变量，不依赖于实例**。可以直接访问类的 `__dict__` 属性来获取类变量。

示例

```python
class MyClass:
    class_variable = "I am a class variable"

    def __init__(self, name):
        self.name = name

# 获取类的类变量
class_variables = {k: v for k, v in MyClass.__dict__.items() if not k.startswith('__') and not callable(v)}
print(class_variables)
```

输出：

```log
{'class_variable': 'I am a class variable'}
```

### 获取实例变量

实例变量是在类的 `__init__` 方法中定义的，**依赖于实例**。可以通过实例的 `__dict__` 属性来获取实例变量。

**示例**：

```python
class MyClass:
    class_variable = "I am a class variable"

    def __init__(self, name, age):
        self.name = name
        self.age = age
    # 可封装成函数
    def gen_param_dict(self):
        return self.__dict__

# 创建实例
instance = MyClass("Alice", 30)

# 获取实例的实例变量
instance_variables = instance.__dict__
print(instance_variables)
print(instance.gen_param_dict()) # 调用函数
```

输出：

```log
{'age': 30, 'name': 'Alice'}
{'age': 30, 'name': 'Alice'}
```

### 使用 `inspect` 模块

`inspect` 模块提供了更多关于对象信息的函数，可以用来获取类的变量。

#### 获取类变量

```python
import inspect

class MyClass:
    class_variable = "I am a class variable"

    def __init__(self, name, age):
        self.name = name
        self.age = age

# 获取类的类变量
class_variables = {k: v for k, v in inspect.getmembers(MyClass) if not k.startswith('__') and not callable(v)}
print(class_variables)
```

输出：

```log
{'class_variable': 'I am a class variable'}
```

#### 获取实例变量

```python
import inspect

class MyClass:
    class_variable = "I am a class variable"

    def __init__(self, name, age):
        self.name = name
        self.age = age

# 创建实例
instance = MyClass("Alice", 30)

# 获取实例的实例变量
instance_variables = {k: v for k, v in inspect.getmembers(instance) if not k.startswith('__') and not callable(v)}
print(instance_variables)
```

输出：

```log
{'age': 30, 'name': 'Alice'}
```

**总结**：

- **获取类变量**：可以通过类的 `__dict__` 属性或 `inspect.getmembers` 来获取。
- **获取实例变量**：可以通过实例的 `__dict__` 属性或 `inspect.getmembers` 来获取。

### 示例代码

以下是一个完整的示例代码，展示如何获取类变量和实例变量：

```python
import inspect

class MyClass:
    class_variable = "I am a class variable"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def instance_method(self):
        pass

    @classmethod
    def class_method(cls):
        pass

    @staticmethod
    def static_method():
        pass

# 获取类的类变量
class_variables = {k: v for k, v in MyClass.__dict__.items() if not k.startswith('__') and not callable(v)}
print("Class Variables:", class_variables)

# 创建实例
instance = MyClass("Alice", 30)

# 获取实例的实例变量
instance_variables = instance.__dict__
print("Instance Variables:", instance_variables)
```

运行结果：

```log
Class Variables: {'class_variable': 'I am a class variable'}
Instance Variables: {'name': 'Alice', 'age': 30}
```

## vars() 函数

在 Python 中，`vars()`函数可以用于**将对象的属性转换为字典**。这个函数**返回对象的`__dict__`属性**，该属性是一个字典，包含了对象的可变属性（即实例变量）。

**使用`vars()`函数时的注意事项：**

1. **仅适用于具有`__dict__`属性的对象**：`vars()`函数仅适用于那些有`__dict__`属性的对象（通常是用户定义的对象）。对于内置对象（如整数、字符串等），调用`vars()`会引发`TypeError`。
2. **只包含实例变量**：返回的字典**只包含对象的实例变量**，不包括类变量或方法。
3. **动态属性**：如果对象在**运行时动态添加了新的属性**，这些属性也会包含在`vars()`返回的字典中。
4. **嵌套的类对象**：无法嵌套展开

以下是一个示例，演示了如何处理动态属性：

```python
class Person:
    def __init__(self, name, age, city, job):
        self.name = name
        self.age = age
        self.city = city
        self.job = job

# 创建一个 Person 对象
person = Person("Alice", 30, "Wonderland", "Engineer")

# 动态添加属性
person.hobby = "Reading"

# 将 Person 对象转换为字典，使用`vars()`函数
person_dict = vars(person)
print(person_dict)
```

输出：

```log
{'name': 'Alice', 'age': 30, 'city': 'Wonderland', 'job': 'Engineer', 'hobby': 'Reading'}
```

使用`vars()`函数将对象转换为字典后，我们可以将其与模板字符串结合使用，方便地进行字符串格式化。例如，结合前面提到的`string.Template` 和 Jinja2 模板引擎。

# PyQt5

## [PyQt5 关于 Qt Designer 的初步应用和打包过程详解](http://www.codebaoku.com/it-python/it-python-223940.html)

在 PyQt 中编写 UI 界面可以直接通过代码来实现，也可以通过 Qt Designer 来完成。Qt Designer 的设计符合 MVC 的架构，其实现了视图和逻辑的分离，从而实现了开发的便捷。Qt Designer 中的操作方式十分灵活，其通过拖拽的方式放置控件可以随时查看控件效果。Qt Designer 生成的.ui 文件（实质上是 XML 格式的文件）也可以通过 pyuic5 工具转换成.py 文件。 Qt Designer 随 PyQt5-tools 包一起安装，其安装路径在 “Python 安装路径\Lib\site-packages\pyqt5-tools”下。若要启动 Qt Designer 可以直接到上述目录下，双击 designer.exe 打开 Qt Designer；或将上述路径加入环境变量，在命令行输入 designer 打开；或在 PyCharm 中将其配置为外部工具打开。下面以 PyCharm 为例，讲述 PyCharm 中 Qt Designer 的配置方法。
