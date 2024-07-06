# python

## 查看 python 安装

查看python版本：python --version

查看python安装路径：where python

pip install --force-reinstall pandas

pip install zstd xlwt xlrd numpy



## python 学习

### sys.argv

在Python中，`sys.argv`是一个列表，它包含了命令行参数。`sys.argv[0]` 是脚本的名称，而后面的元素是脚本后面跟随的命令行参数。

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

**使用场景**

1. **获取命令行参数**： `sys.argv`非常适用于需要从命令行获取输入参数的脚本。
2. **简单的命令行工具**： 使用`sys.argv`可以快速创建简单的命令行工具，处理不同的参数来执行不同的操作。

**注意事项**

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



### 负索引

在Python中，列表的负索引（例如 `[-1]`）是一种方便的方式，用于从列表的末尾开始访问元素。具体来说，`-1` 表示列表的最后一个元素，`-2` 表示倒数第二个元素，依此类推。下面是一些关于负索引的示例和用法：

**负索引的基本用法**

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

**负索引和切片**

负索引用于切片操作时也非常方便，可以从列表的末尾开始进行切片：

```
print(my_list[-3:])    # 输出: [30, 40, 50]  从倒数第三个元素到列表末尾
print(my_list[:-2])    # 输出: [10, 20, 30]  从列表开头到倒数第二个元素之前
print(my_list[-4:-1])  # 输出: [20, 30, 40]  从倒数第四个元素到倒数第一个元素之前
```

**修改列表元素**

负索引也可以用于修改列表中的元素：

```
my_list[-1] = 100
print(my_list)  # 输出: [10, 20, 30, 40, 100]

my_list[-3] = 60
print(my_list)  # 输出: [10, 20, 60, 40, 100]
```

**示例：循环遍历列表的倒数元素**

你可以使用负索引来循环遍历列表的倒数元素，例如：

```
for i in range(1, len(my_list) + 1):
    print(my_list[-i])
```

输出：

```
100
40
60
20
10
```

**注意事项**

1. **索引越界**： 使用负索引时，同样需要注意索引越界的问题。如果列表长度小于负索引的绝对值，将会抛出 `IndexError`。

   ```
   my_list = [1, 2, 3]
   print(my_list[-4])  # IndexError: list index out of range
   ```

2. **可读性**： 虽然负索引非常方便，但在使用时要确保代码的可读性。过多使用负索引可能会使代码难以理解。

负索引是Python中一个非常实用的特性，能够简化从列表末尾访问元素的操作，使代码更简洁。



### realpath

在Python中，`realpath` 函数用于获取文件或目录的绝对路径，并解析所有符号链接。这在处理文件路径时特别有用，因为它可以帮助你**确保你访问的是实际的文件位置**，而**不是符号链接指向的路径**。

`realpath` 是 `os.path` 模块中的一个函数，因此你需要先导入 `os` 模块，然后才能使用它。

以下是一些示例和用法：

**基本用法**

```python
import os

# 获取当前脚本的绝对路径
current_script_path = os.path.realpath(__file__)
print(current_script_path)
```

**示例：解析符号链接**

假设有一个符号链接指向某个文件或目录，可以使用 `realpath` 来获取实际路径：

```python
import os

# 假设 'symlink_path' 是一个符号链接的路径
symlink_path = '/path/to/symlink'
actual_path = os.path.realpath(symlink_path)
print(actual_path)
```

**示例：处理相对路径**

`realpath` 也可以用来将相对路径转换为绝对路径：

```python
import os

relative_path = './some/relative/path'
absolute_path = os.path.realpath(relative_path)
print(absolute_path)
```

**结合其他 `os.path` 函数**

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

**示例：跨平台使用**

**由于 `os.path` 是跨平台的**，在不同的操作系统上使用 `realpath` 可以确保路径处理的一致性：

```
python复制代码import os

# 在 Windows 上的示例
windows_path = 'C:\\path\\to\\file'
absolute_path_windows = os.path.realpath(windows_path)
print(absolute_path_windows)

# 在 Unix/Linux 上的示例
unix_path = '/path/to/file'
absolute_path_unix = os.path.realpath(unix_path)
print(absolute_path_unix)
```

**总结**

- **功能**：`realpath` 函数返回文件或目录的绝对路径，并解析所有符号链接。
- **用途**：适用于需要确定文件或目录的实际位置、解析符号链接、将相对路径转换为绝对路径等情况。
- **跨平台**：由于 `os.path` 是跨平台的，`realpath` 可以在不同操作系统上使用而无需担心兼容性问题。

通过使用 `realpath`，你可以更可靠地处理文件路径，确保你的代码处理的是实际的文件位置而不是符号链接指向的路径。



### f-string

在Python中，`f""` 是一种字符串格式化方法，称为 **f-string**（格式化字符串字面量），引入于Python 3.6。f-string 提供了一种简洁且直观的方式来嵌入表达式和变量到字符串中。

**基本用法**

要使用 f-string，只需在字符串前面加上字母 `f` 或 `F`，然后在字符串中用花括号 `{}` 包含表达式或变量名。

```python
name = "Alice"
age = 30

# 使用 f-string 进行字符串格式化
greeting = f"Hello, {name}. You are {age} years old."
print(greeting)
```

输出：

```
Hello, Alice. You are 30 years old.
```

**表达式嵌入**

f-string 还允许在花括号中嵌入任意的Python表达式：

```python
a = 5
b = 10

# 在 f-string 中嵌入表达式
result = f"The sum of {a} and {b} is {a + b}."
print(result)
```

输出：

```
The sum of 5 and 10 is 15.
```

**调用函数和方法**

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

**格式化选项**

f-string 支持格式化选项，与 `str.format()` 方法类似。你可以在表达式后面加上 `:` 和格式说明符：

```python
value = 3.14159

# 保留两位小数
formatted_value = f"Pi is approximately {value:.2f}."
print(formatted_value)
```

输出：

```
Pi is approximately 3.14.
```

**多行 f-string**

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

```
Name: Alice
Age: 30
Address: Wonderland
```

**嵌套引号**

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

**使用字典和列表**

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

```
Alice is 30 years old.
The first number is 1.
```

**总结**

f-string 提供了一种简洁且高效的字符串格式化方式。它们不仅可以嵌入变量，还可以嵌入复杂的表达式，并支持各种格式化选项。通过使用 f-string，可以使代码更易读、更直观。



###  with...as...

在Python中，`with ... as ...` 语句用于上下文管理（context management）。它提供了一种简洁的方式来**处理资源的分配和释放**，比如**文件操作、锁、网络连接**等。

**基本用法**

最常见的用法之一是文件操作。在使用文件时，`with` 语句确保文件会被正确地关闭，即使在操作过程中发生异常。

```python
# 使用 with 语句打开文件
with open('example.txt', 'r') as file:
    content = file.read()
    print(content)
# 文件在此处自动关闭
```

在上面的示例中，`open('example.txt', 'r')` 返回一个文件对象，并且 `as file` 将该对象赋值给变量 `file`。`with` 语句的作用范围结束时，文件会自动关闭。

**上下文管理器**

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

```
复制代码Entering the context
Doing something
Exiting the context
```

在上面的示例中：

- `__enter__` 方法在进入上下文时被调用，并且其返回值被赋给 `as` 后的变量（这里是 `manager`）。
- `__exit__` 方法在离开上下文时被调用，它接受三个参数（`exc_type`, `exc_value`, 和 `traceback`），用于处理可能发生的异常。

**处理异常**

`with` 语句在处理异常时也非常有用。`__exit__` 方法可以捕获并处理在上下文块中发生的异常。

示例：处理异常的上下文管理器

```
python复制代码class MyContextManager:
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

```
scss复制代码Entering the context
Inside the context
An exception occurred: Something went wrong!
Exiting the context
```

在上面的示例中，异常 `ValueError` 被抛出，`__exit__` 方法捕获了该异常并进行了处理。通过返回 `True`，`__exit__` 方法告诉解释器异常已被处理，不需要再次抛出。

使用上下文管理器的内置模块

Python 的标准库中有许多内置的上下文管理器，如 `threading.Lock` 和 `decimal.localcontext`。

示例：使用锁进行线程同步

```
python复制代码import threading

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

**总结**

`with ... as ...` 语句是Python中强大的特性，用于确保资源的正确管理和释放。通过实现 `__enter__` 和 `__exit__` 方法，你可以创建自定义的上下文管理器，从而更好地控制资源的生命周期。标准库中也提供了许多内置的上下文管理器，便于在各种场景中使用。











## OS 库常见使用函数

[OS库](https://blog.csdn.net/qsx123432/article/details/120335885#:~:text=python%E4%B8%AD%20os%20%E5%BA%93%E5%B8%B8%E8%A7%81%E7%9A%84%E4%BD%BF%E7%94%A8%E5%87%BD%E6%95%B0%201%20os.name%20%28%29%20%E8%8E%B7%E5%BE%97%20%E5%BD%93%E5%89%8D%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F,7%20os.removedirs%20%28%E6%96%87%E4%BB%B6%E5%A4%B9%E5%90%8D%29%20%E7%A7%BB%E9%99%A4%E7%A9%BA%E6%96%87%E4%BB%B6%E5%A4%B9%208%20os.remove%20%28%E6%96%87%E4%BB%B6%E5%A4%B9%E5%90%8D%29%20%E7%A7%BB%E9%99%A4%E7%A9%BA%E6%96%87%E4%BB%B6%E5%A4%B9) 



## xlrd 和 xlwt

**xlrd**

xlrd是一个从Excel文件读取数据和格式化信息的库，支持.xls以及.xlsx文件。

http://xlrd.readthedocs.io/en/latest/

- xlrd支持.xls，.xlsx文件的读.
- 通过设置on_demand变量使open_workbook()函数只加载那些需要的sheet，从而节省时间和内存(该方法对.xlsx文件无效)。
- xlrd.Book对象有一个unload_sheet方法，它将从内存中卸载工作表，由工作表索引或工作表名称指定(该方法对.xlsx文件无效)

**xlwt**

xlwt是一个用于将数据和格式化信息写入旧Excel文件的库(如.xls)。

https://xlwt.readthedocs.io/en/latest/

- xlwt支持.xls文件写。







## XML

读取xml：

     root = ElementTree.parse(r"/Users/..../Documents/111.xml")
     root = ElementTree.fromstring(text)

遍历：

for node in root.iter():
    print type(node)
元素标签名 node.tag
元素标签属性名称、属性值node.attrib
获取元素属性对应的值node.attrib.get('id','NULL') # 不存在则取默认值NULL，不指定默认值不存在时报错
元素属性二元组node.attrib.items()
元素属性列表 node.attrib.keys()
该结点的所有子节点中选择符合元素名称的第一个子节点node.find('xxx')
该结点的所有子节点中选择符合元素名称的所有子节点node.findall('xxx')
所有子节点以列表形式给出node.getchildren()
遍历所有子树 node.iter()



[`xml.etree.ElementTree`](https://docs.python.org/3.6/library/xml.etree.elementtree.html#module-xml.etree.ElementTree)— 元素树 XML API

python ElementTree：https://blog.csdn.net/weixin_43956958/article/details/121986040?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-1-121986040-blog-79852724.pc_relevant_recovery_v2&spm=1001.2101.3001.4242.2&utm_relevant_index=2

























# PyQt5

## [PyQt5 关于Qt Designer的初步应用和打包过程详解](http://www.codebaoku.com/it-python/it-python-223940.html)

​    在PyQt中编写UI界面可以直接通过代码来实现，也可以通过Qt Designer来完成。Qt Designer的设计符合MVC的架构，其实现了视图和逻辑的分离，从而实现了开发的便捷。Qt Designer中的操作方式十分灵活，其通过拖拽的方式放置控件可以随时查看控件效果。Qt Designer生成的.ui文件（实质上是XML格式的文件）也可以通过pyuic5工具转换成.py文件。 Qt Designer随PyQt5-tools包一起安装，其安装路径在 “Python安装路径\Lib\site-packages\pyqt5-tools”下。若要启动Qt Designer可以直接到上述目录下，双击designer.exe打开Qt Designer；或将上述路径加入环境变量，在命令行输入designer打开；或在PyCharm中将其配置为外部工具打开。下面以PyCharm为例，讲述PyCharm中Qt Designer的配置方法。





# vscode 调试

## vscode 调试添加运行参数

`launch.json` 中添加 `args` 项，每个运行参数是一个字符串，如：

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "args": [
                "./xxx/xxx.yaml",
                "--xxx=xxx"
            ]
        }
    ]
}
```



## vscode 调试添加环境变量

`launch.json` 中添加 `envs` 项：

> python 用 `env`
>
> C/C++ 用 `environment`
>
> ```json
> "environment":[
>     {
>         "name":"squid",
>         "value":"clam"
>     }
> ]
> ```

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {
                "PYTHONPATH": "/usr/local/xxx/xxx/python:$PYTHONPATH",
                "PATH": "~/xxx/xxx:$PATH",
                "LD_LIBRARY_PATH": "~/xxx/lib64:$LD_LIBRARY_PATH"
            }
        }
    ]
}
```



### vscode 设置调试器当前工作路径

`launch.json` 中添加 `cwd` 项：

Specifies the current working directory for the debugger, which is the base folder for any relative paths used in code. If omitted, defaults to `${workspaceFolder}` (the folder open in VS Code).

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "cwd": "xxx/xxx"
        }
    ]
}
```







c++报错error: expected namespace name

