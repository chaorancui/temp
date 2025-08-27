[toc]

# python 学习

## Python 中调用 Python

在 Python 中调用另一个 Python 脚本文件可以通过几种方式实现：

### 使用 `import` 语句

你可以通过 `import` 语句导入其他脚本中的函数、类或者变量。

假设你有一个脚本 `script1.py` 和一个脚本 `script2.py`，你想在 `script2.py` 中调用 `script1.py` 中的内容。

- `script1.py`：

  ```python
    def greet(name):
      print(f"Hello, {name}!")
  ```

- `script2.py`：

  ```python
  import script1

  script1.greet("Alice")
  ```

在这种方法下，`script2.py` 中调用了 `script1.py` 中定义的 `greet` 函数。

### 使用 `from ... import ...`

你也可以只导入某个特定的函数、类或变量，而不是整个脚本文件。

- `script1.py`：

  ```python
  def greet(name):
      print(f"Hello, {name}!")
  ```

- `script2.py`：

  ```python
  from script1 import greet

  greet("Bob")
  ```

### 使用 `exec()` 函数

如果你希望动态执行其他 Python 脚本的代码，可以使用 `exec()` 函数。这个方法适用于你需要在运行时执行代码文件。

```python
with open('script1.py', 'r') as file:
    exec(file.read())
```

### 使用 `subprocess` 模块

如果你想在 Python 中运行外部脚本作为一个独立的进程，可以使用 `subprocess` 模块。这样不仅能执行 Python 脚本，还能获取其输出。

```python
import subprocess

# 调用外部 Python 脚本
subprocess.run(["python", "script1.py"])
```

### 使用 `runpy` 模块

`runpy` 模块提供了一些函数来运行模块。你可以使用 `runpy.run_path()` 来运行一个 Python 脚本。

```python
import runpy

runpy.run_path('script1.py')
```

### 总结

- 如果只是希望调用脚本中的函数或类，使用 `import` 或 `from ... import ...` 是最常见和推荐的方法。
- 如果需要运行脚本文件作为独立的程序，可以使用 `subprocess` 或 `exec()`。
- `runpy` 也是一个有用的选择，尤其是在动态执行脚本时。

选择合适的方法取决于你的需求。

## Shell 中调用 Python

除了直接以 `python xxx.py` 的方式运行 py 文件，对于简单的 python 代码，还可以使用 `python -c`。
`python -c` 是 Python 提供的一个命令行参数，意思是 **直接在命令行执行一段 Python 代码字符串**。

### 一、基本语法

```python
python -c "代码"
```

比如：

```python
python -c "print('Hello, world!')"
# 输出：
# Hello, world!
```

### 二、典型使用场景

1. **快速执行一小段 Python 代码**

   例如测试表达式、计算结果：

   ```python
   python -c "print(2**10)"
   # 输出：
   # 1024
   ```

2. **当作脚本替代品**

   有时候我们不想写一个 `.py` 文件，就可以用 `python -c`。

   比如 **文件行数统计**：

   ```python
   python -c "import sys; print(sum(1 for _ in open(sys.argv[1])))" filename.txt
   ```

3. **结合 Shell 脚本处理数据**

   比如从 JSON 提取字段（不依赖 `jq`）：

   ```python
   echo '{"name": "Alice", "age": 25}' | python -c "import sys, json; print(json.load(sys.stdin)['name'])"
   # 输出：
   # Alice
   ```

4. **读取/修改 YAML 或 JSON 配置文件**

   用 `python -c` + `PyYAML/json` 解析配置，然后在 shell 里取值。

   ```python
   python -c "import yaml;print(yaml.safe_load(open('config.yaml'))['output']['file'])"
   ```

5. **调用 Python 库做简单计算**

   有些任务用 Shell 工具不好算，可以直接调用 Python：

   ```python
   python -c "import math; print(math.sin(math.pi/2))"
   # 输出：
   # 1.0
   ```

6. **管道处理**

   接收前一个命令的输出，再用 Python 处理：

   ```python
   ls | python -c "import sys; print('\n'.join(sorted(sys.stdin.read().split())))"
   ```

   （相当于 `ls | sort`）

注意事项

- 代码一般用 **双引号** `"..."` 包裹，如果里面也要用引号，需要转义。
- 多行语句可以用 `;` 分隔。
- 如果逻辑太复杂，不建议用 `-c`，而是写到 `.py` 脚本里。

### Python -c One-liner 速查表

1. **数学计算**

   ```python
   # 幂运算
   python -c "print(2**10)"             # 1024

   # 开平方
   python -c "import math;print(math.sqrt(49))"   # 7.0

   # 三角函数
   python -c "import math;print(math.sin(math.pi/2))"  # 1.0

   # 随机数
   python -c "import random;print(random.randint(1,100))"
   ```

2. 文件处理

   ```python
   # 统计文件行数
   python -c "import sys;print(sum(1 for _ in open(sys.argv[1])))" file.txt

   # 打印文件前 5 行
   python -c "import sys;[print(next(open(sys.argv[1])).rstrip()) for _ in range(5)]" file.txt

   # 去重并排序文件行
   python -c "import sys;print('\n'.join(sorted(set(open(sys.argv[1])))))" file.txt
   ```

3. 文本/管道处理

   ```python
   # 反转字符串
   echo hello | python -c "import sys;print(sys.stdin.read()[::-1])"

   # 统计单词频率
   echo 'a b a c b a' | python -c "import sys,collections;print(collections.Counter(sys.stdin.read().split()))"
   ```

4. JSON 处理（替代 jq）

   ```python
   # 提取字段
   echo '{"name":"Alice","age":25}' | python -c "import sys,json;print(json.load(sys.stdin)['name'])"

   # 格式化 JSON
   echo '{"name":"Alice","age":25}' | python -c "import sys,json;print(json.dumps(json.load(sys.stdin), indent=2))"
   ```

5. YAML 处理（需要 PyYAML）

   ```python
   # 读取字段
   python -c "import yaml;print(yaml.safe_load(open('config.yaml'))['output']['file'])"

   # 打印整个 YAML
   python -c "import yaml;print(yaml.safe_load(open('config.yaml')))"
   ```

6. 时间与日期

   ```python
   # 当前时间戳
   python -c "import time;print(int(time.time()))"

   # 格式化时间
   python -c "import datetime;print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))"

   # N 天前日期
   python -c "import datetime;print((datetime.datetime.now()-datetime.timedelta(days=7)).strftime('%Y-%m-%d'))"
   ```

7. 系统/工具

   ```python
   # Python 版本
   python -c "import sys;print(sys.version)"

   # 获取环境变量
   python -c "import os;print(os.getenv('HOME'))"

   # 获取命令行参数
   python -c "import sys;print(sys.argv)" foo bar
   ```

8. 实用示例

   ```python
   # 计算平均值
   echo "1 2 3 4 5" | python -c "import sys;nums=list(map(int,sys.stdin.read().split()));print(sum(nums)/len(nums))"

   # 生成 10 个随机密码（每个 8 位）
   python -c "import random,string;[print(''.join(random.choices(string.ascii_letters+string.digits,k=8))) for _ in range(10)]"
   ```

总结：

- **数据计算** → math/random
- **文件处理** → sys/open
- **JSON/YAML** → json/yaml
- **时间** → datetime
- **管道** → sys.stdin

## 原始字符串（raw string）

在 Python 中，**原始字符串**（raw string）是一种特殊的字符串类型，可以通过在字符串前添加小写字母 `r` 或 `R` 来定义。
使用原始字符串时，Python 会**忽略字符串中的转义字符**，即使是反斜杠 `\` 也会被视为普通字符，而不会作为转义符来处理。

### 带转义字符串

通常，在字符串中使用反斜杠（`\`）时，Python 会将其视为转义字符。例如：

```python
s = "Hello\nWorld"
print(s)
# 输出:
# Hello
# World
```

上面的例子中，`\n` 被解释为换行符。如果你希望在字符串中使用反斜杠而不进行转义（例如路径分隔符），就可以使用原始字符串。

### 原始字符串

通过在字符串前添加 `r` 或 `R`，可以定义一个原始字符串。

```python
s = r"Hello\nWorld"
print(s)
# 输出：
# Hello\nWorld
```

### 原始字符串的规则

- **不能以单个反斜杠结尾**：如果原始字符串以单个反斜杠结尾，Python 会报错，因为反斜杠本身会被认为是转义字符的开始，并且没有后续字符来配对它。例如，`r"abc\"` 会引发语法错误。

  正确写法：

  ```python
  r"abc\\"
  ```

- **适用于所有字符串类型**：原始字符串不仅适用于双引号括起来的字符串，也适用于单引号括起来的字符串。

  ```python
  s = r'Hello\nWorld'
  print(s)  # 输出: Hello\nWorld
  ```

### 常见用途

1. **文件路径**：在 Windows 中，文件路径通常包含反斜杠（`\`）。如果不使用原始字符串，就需要使用双反斜杠（`\\`）来避免转义：
   - 普通字符串需要写成 `"C:\\Users\\Documents\\file.txt"`.
   - 使用原始字符串时，可以直接写成 `r"C:\Users\Documents\file.txt"`。
2. **正则表达式**：在正则表达式中，很多特殊字符（如 `\d`, `\n` 等）都以反斜杠开头。如果不使用原始字符串，你需要双写反斜杠，比如 `\\d` 来匹配数字，而原始字符串就不需要这样做。

   ```python
   # 正则表达式示例
   import re

   pattern = r"\d+"  # 匹配一个或多个数字
   text = "123 abc 456"
   matches = re.findall(pattern, text)
   print(matches)
   # 输出：
   # ['123', '456']
   ```

### 使用场景示例

#### Windows 文件路径

Windows 路径通常包含反斜杠。使用原始字符串时，可以避免使用双反斜杠进行转义。

```python
path = r"C:\Users\Name\Documents\File.txt"
print(path)  # 输出: C:\Users\Name\Documents\File.txt
```

#### 路径中有空格

在命令行（包括 Python 中使用 `subprocess` 等工具执行命令时），路径中包含空格时，通常会导致路径被**错误地解析为多个不同的参数**。例如，如果路径是 `C:\Program Files\MyApp`，命令行会把它解析为两个独立的部分：`C:\Program` 和 `Files\MyApp`，这显然不是你想要的。为了解决这个问题，使用**原始字符串 r"..." 或者直接使用引号（`"` 或 `'`）来保证路径被正确解析**，告诉命令行整个路径应当视为一个单独的参数。

如当我们通过 `subprocess.run()` 等方法执行命令时，如果路径中有空格，也需要将路径用引号括起来，确保整个路径作为一个参数传递。

```python
import subprocess

# 使用带有空格的路径
command = [
    "python",
    r"C:\Program Files\MyApp\my_script.py",  # 使用原始字符串避免反斜杠转义问题
    r"C:\Users\My User\Documents\input.txt"
]

# 执行命令
subprocess.run(command)
```

#### 正则表达式

在正则表达式中，反斜杠有特殊的含义（如 `\d` 表示数字）。如果不用原始字符串，需要双写反斜杠：

```python
# 使用普通字符串
pattern = "\\d+"
# 使用原始字符串
pattern = r"\d+"
```

#### HTML/XML 字符串

如果你正在处理包含大量反斜杠的 HTML 或 XML 字符串，原始字符串会使代码更易读。

```python
html = r"<div class=\"container\">Content</div>"
print(html)  # 输出: <div class="container">Content</div>
```

### 总结

原始字符串（`r"..."`）是一种非常有用的工具，可以让你避免在字符串中频繁使用反斜杠进行转义。它尤其适用于处理文件路径、正则表达式以及任何包含特殊字符的字符串。

## 组织数据 - 仿 struct

在 Python 里，其实没有像 C/C++ 那样的原生 `struct` 类型，但可以用好几种方式实现“结构体”效果，具体取决于你是想 **像 C 那样操作内存** 还是 **只是想用结构化的字段访问数据**。

- 如果是为了**Python 和 C 共享数据**（比如调用 `dll`、`so`），建议用 `ctypes.Structure`。
- 如果是为了**组织数据方便读写**，建议用 `dataclass` 或 `namedtuple`。

1. **如果只是想有“字段”的结构**

   最简单的方法是用 **`dataclass`** 或 **`namedtuple`**

   1. **`dataclass` 示例**

      ```python
      from dataclasses import dataclass

      @dataclass
      class Point:
          x: int
          y: int

      def get_point():
          return Point(1, 2)

      p = get_point()
      print(p.x, p.y)  # 1 2
      ```

      - 可变，更像普通 Python 类
      - 代码简洁，自动生成 `__init__`、`__repr__`

   2. **`namedtuple` 示例**

      ```python
      from collections import namedtuple

      Point = namedtuple("Point", ["x", "y"])
      def get_point():
         return Point(1, 2)

      p = get_point()
      print(p.x, p.y)  # 1 2
      ```

      - 不可变（类似 C struct 常量）
      - 可以用字段名访问

2. **如果要 C 风格内存对齐**

   可以用 **`struct` 模块** 或 **`ctypes.Structure`**

   1. **`struct` 模块（用于打包/解包二进制）**

      ```python
      import struct

      def get_struct():
          return struct.pack("if", 1, 3.14)  # int + float

      data = get_struct()
      print(data)               # b'\x01\x00\x00\x00\xc3\xf5H@'
      print(struct.unpack("if", data))  # (1, 3.140000104904175)
      ```

      - 常用于文件/网络二进制传输
      - 不直接返回“字段对象”，而是打包的字节串

   2. **`ctypes.Structure`（真正的 C 结构体）**

      ```python
      from ctypes import Structure, c_int, c_float

      class Point(Structure):
          _fields_ = [("x", c_int),
                      ("y", c_float)]

      def get_point():
          return Point(1, 3.14)

      p = get_point()
      print(p.x, p.y)  # 1 3.14
      ```

      - 完全对应 C 结构体内存布局
      - 可用于 Python 与 C 库交互（`ctypes`）

## 时间戳

1. 生成字符串形式

   ```python
   from datetime import datetime

   now = datetime.now()
   timestamp_str = now.strftime("%Y%m%d%H%M%S")
   print(timestamp_str)  # 例如: '20250822113345'
   ```

   - `%Y` → 4 位年份
   - `%m` → 月（01-12）
   - `%d` → 日（01-31）
   - `%H` → 时（00-23）
   - `%M` → 分（00-59）
   - `%S` → 秒（00-59）

2. 转成整数形式

   ```python
   timestamp_int = int(timestamp_str)
   print(timestamp_int)  # 例如: 20250822113345
   ```

   这样可以直接用于 **文件名、日志记录、唯一标识**。

3. 封装成函数

   ```python
   from datetime import datetime

   def current_ymdhms(timestamp_type="str"):
       now = datetime.now()
       s = now.strftime("%Y%m%d_%H%M%S")
       return s if timestamp_type == "str" else int(s)

   print(current_ymdhms("str"))  # '20250822_113345'
   print(current_ymdhms("int"))  # 20250822113345
   ```

**总结**

- `strftime("%Y%m%d%H%M%S")` 可以直接得到年月日时分秒
- 需要整数可用 `int()` 转换
- 常用于文件名、日志、批处理标识
