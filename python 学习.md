[toc]

# python 学习

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

## 范围[)

在 Python 中，范围和切片的定义通常是前闭后开（inclusive-exclusive）的，包括 `range` 函数、列表切片、字符串切片等。这种设计在编程中很常见，因为它简化了计算范围和索引的逻辑。

如：

1. `range(5)` 生成从 0 到 4 的数字，不包括 5。`np.arange()` 类似。
2. `lst[1:4]` 选择从索引 1 到索引 3 的元素，不包括索引 4。数组索引从 0 开始。

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

# 使用 f-string 进行字符串格式化
greeting = f"Hello, {name}. You are {age} years old."
print(greeting)
```

输出：

```log
Hello, Alice. You are 30 years old.
```

**表达式嵌入**：

f-string 还允许在花括号中嵌入任意的 Python 表达式：

```python
a = 5
b = 10

# 在 f-string 中嵌入表达式
result = f"The sum of {a} and {b} is {a + b}."
print(result)
```

输出：

```log
The sum of 5 and 10 is 15.
```

**调用函数和方法**：

你也可以在 f-string 中调用函数或方法：

```python
def greet(name):
    return f"Hello, {name}!"

name = "Bob"
greeting = f"{greet(name)} How are you today?"
print(greeting)
```

输出：

```
Hello, Bob! How are you today?
```

**格式化选项**：

f-string 支持格式化选项，与 `str.format()` 方法类似。你可以在表达式后面加上 `:` 和格式说明符：

```python
value = 3.14159

# 保留两位小数
formatted_value = f"Pi is approximately {value:.2f}."
print(formatted_value)
```

输出：

```log
Pi is approximately 3.14.
```

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
print(quote)
```

输出：

```
He said, "Hello, Alice!"
```

**使用字典和列表**：

f-string 也可以用来格式化字典和列表中的值：

```python
person = {"name": "Alice", "age": 30}
numbers = [1, 2, 3, 4, 5]

info = f"{person['name']} is {person['age']} years old."
number_list = f"The first number is {numbers[0]}."
print(info)
print(number_list)
```

输出：

```log
Alice is 30 years old.
The first number is 1.
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

**上下文管理器**：

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

```
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

```
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

```
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

```
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

```
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

```
{'name': 'Alice', 'age': 30, 'city': 'Wonderland', 'job': 'Engineer', 'hobby': 'Reading'}
```

使用`vars()`函数将对象转换为字典后，我们可以将其与模板字符串结合使用，方便地进行字符串格式化。例如，结合前面提到的`string.Template` 和 Jinja2 模板引擎。

# PyQt5

## [PyQt5 关于 Qt Designer 的初步应用和打包过程详解](http://www.codebaoku.com/it-python/it-python-223940.html)

​ 在 PyQt 中编写 UI 界面可以直接通过代码来实现，也可以通过 Qt Designer 来完成。Qt Designer 的设计符合 MVC 的架构，其实现了视图和逻辑的分离，从而实现了开发的便捷。Qt Designer 中的操作方式十分灵活，其通过拖拽的方式放置控件可以随时查看控件效果。Qt Designer 生成的.ui 文件（实质上是 XML 格式的文件）也可以通过 pyuic5 工具转换成.py 文件。 Qt Designer 随 PyQt5-tools 包一起安装，其安装路径在 “Python 安装路径\Lib\site-packages\pyqt5-tools”下。若要启动 Qt Designer 可以直接到上述目录下，双击 designer.exe 打开 Qt Designer；或将上述路径加入环境变量，在命令行输入 designer 打开；或在 PyCharm 中将其配置为外部工具打开。下面以 PyCharm 为例，讲述 PyCharm 中 Qt Designer 的配置方法。
