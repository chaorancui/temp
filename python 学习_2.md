[toc]

# python 学习

## Python 中调用 Python

在 Python 中调用另一个 Python 脚本文件可以通过几种方式实现：

**一、使用 `import` 语句**

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

**二、使用 `from ... import ...`**

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

**三、使用 `exec()` 函数**

如果你希望动态执行其他 Python 脚本的代码，可以使用 `exec()` 函数。这个方法适用于你需要在运行时执行代码文件。

```python
with open('script1.py', 'r') as file:
    exec(file.read())
```

**四、使用 `subprocess` 模块**

如果你想在 Python 中运行外部脚本作为一个独立的进程，可以使用 `subprocess` 模块。这样不仅能执行 Python 脚本，还能获取其输出。

```python
import subprocess

# 调用外部 Python 脚本
subprocess.run(["python", "script1.py"])
```

**五、使用 `runpy` 模块**

`runpy` 模块提供了一些函数来运行模块。你可以使用 `runpy.run_path()` 来运行一个 Python 脚本。

```python
import runpy

runpy.run_path('script1.py')
```

**总结**

- 如果只是希望调用脚本中的函数或类，使用 `import` 或 `from ... import ...` 是最常见和推荐的方法。
- 如果需要运行脚本文件作为独立的程序，可以使用 `subprocess` 或 `exec()`。
- `runpy` 也是一个有用的选择，尤其是在动态执行脚本时。

选择合适的方法取决于你的需求。

## Shell 中调用 Python

除了直接以 `python xxx.py` 的方式运行 py 文件，对于简单的 python 代码，还可以使用 `python -c`。
`python -c` 是 Python 提供的一个命令行参数，意思是 **直接在命令行执行一段 Python 代码字符串**。

**一、基本语法**

```python
python -c "代码"
```

比如：

```python
python -c "print('Hello, world!')"
# 输出：
# Hello, world!
```

**二、典型使用场景**

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

5. `str.strip([chars])`

   移除字符串两端的空白字符（包括空格、换行符等）。

   ```python
   s = "  hello  "
   print(s.strip())  # 输出: "hello"
   ```

6. `str.lstrip([chars])` 和 `str.rstrip([chars])`

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

### rstrip / lstrip / strip

这三个方法都是 Python 字符串的内置方法，用于去掉 **首尾的字符**，常用于清理空格、换行符、标点等。

**基本语法**

```python
s.strip([chars])
s.lstrip([chars])
s.rstrip([chars])
```

- **参数 `chars`**：
  - 可选，字符串形式。
  - 不是“子串”，而是一个 **字符集合**。
  - 表示要删除的字符集合中 **任意字符**。
  - 如果省略，默认去掉 **空白字符**（空格、`\t`、`\n`、`\r` 等）。

1. `strip([chars])`

   去掉 **字符串首尾** 出现的指定字符集合。

   ```python
   s = "   hello world   \n"
   print(s.strip())          # "hello world"

   s = "---hello---"
   print(s.strip("-"))       # "hello"
   ```

2. `lstrip([chars])` 和 `rstrip([chars])`

   去掉 **字符串左边（开头）** 的指定字符集合。去掉 **字符串右边（末尾）** 的指定字符集合。

   ```python
   s = "   hello   "
   print(s.lstrip())         # "hello   "
   print(s.rstrip())         # "   hello"

   s = "xxxyhelloxxx"
   print(s.lstrip("xy"))     # "helloxxx"
   print(s.rstrip("xy"))     # "xxxyhello"
   ```

解释：`"xy"` 是一个字符集合，左边的 `x` 和 `y` 都会被去掉，直到遇到不在集合里的字符为止。

**注意点：**

1. `chars` 是 **字符集合**，而不是“子串”。

   ```python
   s = "foobar"
   print(s.strip("fo"))   # "bar"
   ```

   解释：去掉所有 `f` 或 `o`，直到遇到其他字符。不是去掉字符串 `"fo"`。

2. 不会影响中间的字符，只处理首尾。

   ```python
   s = "  hello  world  "
   print(s.strip())       # "hello  world"
   ```

3. 默认去掉的是 **空白符**（含空格、制表符 `\t`、换行 `\n` 等）。

**常见应用场景**

- **去掉换行符**（常见于 `readlines` 之后）：

  ```python
  line = "hello\n"
  print(line.strip())   # "hello"
  ```

- **去掉路径末尾的 `/`**：

  ```python
  path = "dir///"
  print(path.rstrip("/"))  # "dir"
  ```

- **去掉前导 0**（比如格式化数字）：

  ```python
  num = "00012300"
  print(num.lstrip("0"))   # "12300"
  ```

- **去掉标点符号**：

  ```python
  s = "...hello!!!"
  print(s.strip(".!"))     # "hello"
  ```

**总结对比表**

| 方法       | 作用范围     | 示例                    | 结果     |
| ---------- | ------------ | ----------------------- | -------- |
| `strip()`  | 去掉首尾     | `"  hi  ".strip()`      | `"hi"`   |
| `lstrip()` | 去掉左边     | `"  hi  ".lstrip()`     | `"hi  "` |
| `rstrip()` | 去掉右边     | `"  hi  ".rstrip()`     | `"  hi"` |
| 指定 chars | 去掉首尾集合 | `"xxhiixx".strip("xi")` | `"h"`    |

## 原始字符串（raw string）

在 Python 中，**原始字符串**（raw string）是一种特殊的字符串类型，可以通过在字符串前添加小写字母 `r` 或 `R` 来定义。
使用原始字符串时，Python 会**忽略字符串中的转义字符**，即使是反斜杠 `\` 也会被视为普通字符，而不会作为转义符来处理。

**一、带转义字符串**

通常，在字符串中使用反斜杠（`\`）时，Python 会将其视为转义字符。例如：

```python
s = "Hello\nWorld"
print(s)
# 输出:
# Hello
# World
```

上面的例子中，`\n` 被解释为换行符。如果你希望在字符串中使用反斜杠而不进行转义（例如路径分隔符），就可以使用原始字符串。

**二、原始字符串**

通过在字符串前添加 `r` 或 `R`，可以定义一个原始字符串。

```python
s = r"Hello\nWorld"
print(s)
# 输出：
# Hello\nWorld
```

**三、原始字符串的规则**

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

**四、常见用途**

1. **文件路径**：

   - 在 Windows 中，文件路径通常包含反斜杠（`\`）。如果不使用原始字符串，就需要使用双反斜杠（`\\`）来避免转义：

     - 普通字符串需要写成 `"C:\\Users\\Documents\\file.txt"`.
     - 使用原始字符串时，可以直接写成 `r"C:\Users\Documents\file.txt"`。

   - 路径中有空格

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

2. **正则表达式**：
   在正则表达式中，很多特殊字符（如 `\d`, `\n` 等）都以反斜杠开头。如果不使用原始字符串，你需要双写反斜杠，比如 `\\d` 来匹配数字，而原始字符串就不需要这样做。

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

3. **HTML/XML 字符串**：

   如果你正在处理包含大量反斜杠的 HTML 或 XML 字符串，原始字符串会使代码更易读。

   ```python
   html = r"<div class=\"container\">Content</div>"
   print(html)  # 输出: <div class="container">Content</div>
   ```

**总结**

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

## sorted()

**`sorted` 是 Python 内置函数**。

**一、基本介绍**

- **作用**：返回一个排序后的新列表，不会修改原始数据。
- **语法**：

```python
sorted(iterable, *, key=None, reverse=False)
```

- **参数说明**：
  - `iterable`：任何可迭代对象（list、tuple、str、dict、set、生成器等）。
  - `key`：函数，用于从元素中提取比较值。默认是元素自身。
  - `reverse`：是否倒序，默认为 `False`（升序）。
- **返回值**：一个新的 `list`。

**二、基本用法**

1. 对数字排序

   ```python
   nums = [5, 2, 9, 1]
   print(sorted(nums))         # [1, 2, 5, 9]
   print(sorted(nums, reverse=True))  # [9, 5, 2, 1]
   ```

2. 对字符串排序

   ```python
   s = "python"
   print(sorted(s))  # ['h', 'n', 'o', 'p', 't', 'y']  按字符 ASCII 排序
   ```

3. 对元组 / 列表的列表排序

   ```python
   pairs = [(2, 'b'), (1, 'c'), (2, 'a')]
   print(sorted(pairs))
   # [(1, 'c'), (2, 'a'), (2, 'b')]  先按第一个元素，再按第二个元素
   ```

4. 按 key 排序

   - 按字符串长度

     ```python
     words = ["python", "is", "great"]
     print(sorted(words, key=len))
     # ['is', 'great', 'python']
     ```

   - 忽略大小写

     ```python
     words = ["banana", "Apple", "cherry"]
     print(sorted(words, key=str.lower))
     # ['Apple', 'banana', 'cherry']
     ```

   - 文件名排序

     ```python
     files = sorted(Path('./').rglob('*.md'), key=lambda p: p.name)
     for file in files:
         print(f"find file: {file}")
     ```

5. 对字典排序

   默认字典迭代的是 **键**：

   ```python
   d = {"b": 2, "c": 3, "a": 1}
   print(sorted(d))            # ['a', 'b', 'c'] (按 key 排序)
   print(sorted(d.items()))    # [('a', 1), ('b', 2), ('c', 3)]
   print(sorted(d.items(), key=lambda x: x[1]))
   # [('a', 1), ('b', 2), ('c', 3)] 按 value 排序
   ```

6. 自定义排序函数

   ```python
   nums = [5, -2, 9, -1]
   print(sorted(nums, key=abs))
   # [-1, -2, 5, 9] 按绝对值排序
   ```

7. 排序生成器 / 集合

   ```python
   print(sorted({3, 1, 2}))       # [1, 2, 3]
   print(sorted(x*x for x in [3, -1, 2]))  # [1, 4, 9]
   ```

8. 多级排序

   比如：先按分数排，再按姓名

   ```python
   students = [("Alice", 88), ("Bob", 75), ("Charlie", 88), ("David", 92)]
   print(sorted(students, key=lambda x: (-x[1], x[0])))
   # [('David', 92), ('Alice', 88), ('Charlie', 88), ('Bob', 75)]
   ```

9. 稳定排序

   Python 的排序是 **稳定的**，即当两个元素的 key 相同时，保持原有顺序。

   ```python
   data = [('a', 2), ('b', 1), ('c', 2)]
   print(sorted(data, key=lambda x: x[1]))
   # [('b', 1), ('a', 2), ('c', 2)]  保留了 a 和 c 的原顺序
   ```

Python `sorted` 用法速查表

| 场景                                     | 示例代码                                                                                                       | 输出结果                                                   |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **数字排序（升序/降序）**                | `sorted([5, 2, 9, 1])` `sorted([5, 2, 9, 1], reverse=True)`                                                    | `[1, 2, 5, 9]` `[9, 5, 2, 1]`                              |
| **字符串排序**                           | `sorted("python")`                                                                                             | `['h', 'n', 'o', 'p', 't', 'y']`                           |
| **元组排序（按第一个元素，再按第二个）** | `sorted([(2,'b'), (1,'c'), (2,'a')])`                                                                          | `[(1, 'c'), (2, 'a'), (2, 'b')]`                           |
| **按字符串长度排序**                     | `sorted(["python","is","great"], key=len)`                                                                     | `['is', 'great', 'python']`                                |
| **忽略大小写排序**                       | `sorted(["banana","Apple","cherry"], key=str.lower)`                                                           | `['Apple', 'banana', 'cherry']`                            |
| **字典按键排序**                         | `sorted({"b":2, "c":3, "a":1})`                                                                                | `['a', 'b', 'c']`                                          |
| **字典按值排序**                         | `sorted({"b":2,"c":3,"a":1}.items(), key=lambda x:x[1])`                                                       | `[('a', 1), ('b', 2), ('c', 3)]`                           |
| **按绝对值排序**                         | `sorted([5, -2, 9, -1], key=abs)`                                                                              | `[-1, -2, 5, 9]`                                           |
| **排序生成器/集合**                      | `sorted({3, 1, 2})` `sorted(x*x for x in [3, -1, 2])`                                                          | `[1, 2, 3]` `[1, 4, 9]`                                    |
| **多级排序（先分数，再姓名）**           | `students=[("Alice",88),("Bob",75),("Charlie",88),("David",92)]` `sorted(students, key=lambda x:(-x[1],x[0]))` | `[('David',92), ('Alice',88), ('Charlie',88), ('Bob',75)]` |
| **稳定排序（保持相对顺序）**             | `sorted([('a',2), ('b',1), ('c',2)], key=lambda x:x[1])`                                                       | `[('b', 1), ('a', 2), ('c', 2)]`                           |

**小结**

- **`sorted`** 总是返回 **新列表**，不改变原 iterable。
- 常见用法：
  - 数值、字符串排序
  - 按 key 排序（长度、大小写、绝对值、自定义规则）
  - 对字典的 key 或 value 排序
  - 多级排序（结合 tuple）
  - 稳定排序可保证相等 key 时顺序不乱

## map()

**Python 内置的 `map()` 函数**。

**一、基本介绍**

- `map()` 用于**把一个函数作用到可迭代对象的每个元素上**，返回一个新的迭代器。
- 常用于**批量处理数据**，比如对列表里的所有元素平方、取绝对值、转换类型等。

```python
map(function, iterable, ...)
```

- **function**：要应用的函数（可以是 `def` 定义的函数，或 `lambda` 匿名函数）。
- **iterable**：一个或多个可迭代对象（list、tuple、str 等）。
- **返回值**：一个 **迭代器 (map object)**，通常需要用 `list()`、`tuple()`、`set()` 等转换。

**二、基本用法**

1. 基本示例

   ```python
   # 把列表中每个元素平方
   nums = [1, 2, 3, 4]
   squares = map(lambda x: x**2, nums)
   print(list(squares))
   # 输出: [1, 4, 9, 16]
   ```

2. 使用多个 iterable

   如果传入多个可迭代对象，`map` 会并行取它们的元素，作为参数传给函数：

   ```python
   a = [1, 2, 3]
   b = [4, 5, 6]

   sums = map(lambda x, y: x + y, a, b)
   print(list(sums))
   # 输出: [5, 7, 9]
   ```

   > :pushpin: 注意：**取最短的 iterable 长度**，多余部分会被忽略。

3. 结合内置函数

   ```python
   # 转换数据类型
   nums = ["1", "2", "3"]
   ints = map(int, nums)
   print(list(ints))
   # 输出: [1, 2, 3]
   # 把字符串全部大写
   words = ["hello", "world"]
   uppercased = map(str.upper, words)
   print(list(uppercased))
   # 输出: ['HELLO', 'WORLD']
   ```

4. 注意点

- `map` 返回的是一个 **惰性迭代器**，只会在你 `list()` 或遍历时才真正计算。

- 如果你只需要结果，通常写成列表推导式更直观：

  ```python
  nums = [1, 2, 3]
  print([x*2 for x in nums])   # 更清晰
  ```

- `map` 的优势在于 **和现成函数/多个 iterable 搭配** 时更简洁。

## lambda 表达式

**一、基本介绍**

- **定义**：`lambda` 用于创建 **匿名函数**（没有名字的函数）。

- **语法**：

  ```python
  lambda 参数列表: 表达式
  ```

- 返回值：是一个 **函数对象**，可以赋值给变量，或者直接传给其他函数。

相当于：

```python
lambda x: x + 1
# 等价于：
def f(x):
    return x + 1
```

**二、基本用法**

1. 最简单的例子

   ```python
   f = lambda x: x + 1
   print(f(5))  # 6
   ```

2. 多个参数

   ```python
   add = lambda a, b: a + b
   print(add(3, 7))  # 10
   ```

3. 结合 `sorted` 使用（常见）

   按第二个元素排序：

   ```python
   pairs = [(1, 'c'), (2, 'a'), (2, 'b')]
   print(sorted(pairs, key=lambda x: x[1]))
   # [(2, 'a'), (2, 'b'), (1, 'c')]
   ```

4. 结合 `map`

   ```python
   nums = [1, 2, 3]
   print(list(map(lambda x: x**2, nums)))
   # [1, 4, 9]
   ```

5. 结合 `filter`

   ```python
   nums = [1, 2, 3, 4, 5]
   print(list(filter(lambda x: x % 2 == 0, nums)))
   # [2, 4]
   ```

6. 结合 `reduce`

   ```python
   from functools import reduce
   nums = [1, 2, 3, 4]
   print(reduce(lambda a, b: a * b, nums))
   # 24 (阶乘)
   ```

**三、特点和限制**

1. **只能写单个表达式**

   ```python
   f = lambda x: x + 1  # 合法
   f = lambda x: print(x); x+1  # 不允许多条语句
   ```

2. **没有 `return`**
   表达式的结果会自动返回。

3. **常用场景**：适合写小的、一次性的函数，比如：

   - 排序的 `key`
   - `map` / `filter` / `reduce`
   - GUI 回调、并行任务参数

Python `lambda` vs `def` 对比表

| 特性         | `lambda` 表达式                                                               | `def` 函数定义                                               |
| ------------ | ----------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **语法**     | `lambda 参数: 表达式` 例如：`lambda x: x+1`                                   | `def 函数名(参数):` `    return 结果`                        |
| **返回值**   | 自动返回表达式的值（不能写 `return`）                                         | 必须显式用 `return` 返回值（否则返回 `None`）                |
| **代码块**   | **只能写单个表达式**，不能有多行语句                                          | 可以写多行逻辑，包含控制流、循环等                           |
| **可读性**   | 简洁但复杂时难懂                                                              | 结构清晰，可读性更好                                         |
| **命名**     | 匿名函数（通常赋给变量）                                                      | 有函数名，利于调试与文档化                                   |
| **调试**     | 名称显示为 `<lambda>`，不易追踪                                               | 有明确函数名，调试堆栈更直观                                 |
| **适用场景** | - 需要临时函数时 - 作为参数传递给 `map`、`sorted`、`filter` 等 - 一次性小逻辑 | - 逻辑复杂、多处调用时 - 需要文档化或单元测试 - 需要高可读性 |
| **示例**     | `sorted(data, key=lambda x: x[1])`                                            | `python\ndef add(x, y):\n    return x+y\n`                   |

**一句话口诀：**

- **简单、小型、一次性** ➝ 用 `lambda`
- **复杂、复用、可维护** ➝ 用 `def`

# pdb

官方文档：<https://docs.python.org/3/library/pdb.html>

`pdb` 是 Python 内置的调试器模块，全称是 **Python Debugger**。它允许你在程序运行中以交互方式查看变量、单步执行、设置断点等，是调试 Python 代码的一个非常有用的工具。

## 基本用法

你可以在代码中插入：

```python
import pdb; pdb.set_trace()
```

程序运行到这里会暂停，进入调试模式，你可以交互式地执行命令来观察和控制程序。

## 调试器命令汇总

**基本说明**

- 命令可简写，如 `help` → `h`，`next` → `n`
- 空行表示重复上一个命令（`list` 除外）
- 非法命令默认按 Python 表达式执行，也可用 `!` 前缀强制执行语句

### 帮助与堆栈

| 命令                   | 说明                                       |
| ---------------------- | ------------------------------------------ |
| `help [command]` / `h` | 查看命令帮助。支持 `help pdb` 查看完整文档 |
| `where` / `w`          | 打印堆栈跟踪（当前帧底部用 `>` 指示）      |
| `up [n]` / `u`         | 向上移动堆栈 n 层（默认 1 层）             |
| `down [n]` / `d`       | 向下移动堆栈 n 层（默认 1 层）             |

### 断点控制

| 命令                                           | 说明                                       |
| ---------------------------------------------- | ------------------------------------------ |
| `break [file:line\|function][, condition]`/`b` | 设置断点，也可查看断点                     |
| `tbreak`                                       | 临时断点，命中后自动删除                   |
| `clear [file:line\| bpnum]`/`cl`               | 清除断点，不带参数则清除所有断点           |
| `disable bpnum`                                | 禁用指定断点                               |
| `enable bpnum`                                 | 启用指定断点                               |
| `ignore bpnum [count]`                         | 命中 `count` 次后才生效                    |
| `condition bpnum [condition]`                  | 设置断点触发条件                           |
| `commands [bpnum]`                             | 为断点设置命令序列，结束于 `end`           |
| `silent`                                       | 不显示断点命中信息（配合 `commands` 使用） |

> `ipdb` 中无法保存/加载断点：
>
> - 因为 `pdb.Pdb` 类里实现了 `do_save()`、`do_restore()` 等命令。
> - `ipdb` 是对 `pdb` 的一层包装（基于 IPython 的交互增强），它默认 **没有注册 `save` / `restore` 命令**。

### 执行控制

| 命令                     | 说明                                 |
| ------------------------ | ------------------------------------ |
| `step` / `s`             | 执行当前行，进入函数内部             |
| `next` / `n`             | 执行当前行，不进入函数内部           |
| `until [lineno]` / `unt` | 执行到当前函数中**下一行**，或指定行 |
| `return` / `r`           | 执行到当前函数返回                   |
| `continue` / `c`         | 继续执行，直到下一个断点             |
| `jump lineno` / `j`      | 跳转到某一行，仅限当前帧的代码块内部 |
| `run [args]`             | 重启调试程序（保留状态）             |
| `restart`                | 等同于 `run`                         |
| `quit` / `q`             | 退出调试器                           |

### 查看变量

| 命令          | 说明                               |
| ------------- | ---------------------------------- |
| `args` / `a`  | 查看当前函数的参数和对应值         |
| `p expr`      | 打印表达式结果                     |
| `pp expr`     | 使用 `pprint` 格式化打印表达式结果 |
| `whatis expr` | 查看表达式类型                     |
| `source expr` | 尝试获取对象源代码（如函数）       |

1. 查看当前函数的所有局部变量
   `p locals()` 会返回一个字典，key 是变量名，value 是当前值.
   或 `pp locals()`，（pretty print）让结果更易读。
2. 查看全局变量
   `p globals()` 或 `pp globals()`。

### 显示表达式值

| 命令               | 说明                                     |
| ------------------ | ---------------------------------------- |
| `display expr`     | 每次暂停时自动显示表达式结果（若值改变） |
| `undisplay [expr]` | 移除 `display` 表达式                    |

示例：`display lst[:]` 可捕捉列表内容变化

### 交互与别名

| 命令                 | 说明                             |
| -------------------- | -------------------------------- |
| `interact`           | 启动交互式解释器（新的命名空间） |
| `alias name command` | 创建别名，支持 `%1` 参数传递     |
| `unalias name`       | 删除别名                         |
| `! statement`        | 在当前上下文执行 Python 语句     |

示例：`!x=42`，或 `global x; x=42` 设置全局变量

### 程序控制和会话恢复

| 命令                                           | 说明                             |
| ---------------------------------------------- | -------------------------------- |
| `.pdbrc` 文件                                  | 初始化命令文件（支持别名、断点） |
| 支持 `$var` 形式的临时变量（程序恢复后会清空） |                                  |
| 预设变量：`$_frame`, `$_retval`, `$_exception` |                                  |

### 异常处理

| 命令               | 说明                 |
| ------------------ | -------------------- |
| `exceptions`       | 列出所有链式异常     |
| `exceptions <num>` | 跳转到指定编号的异常 |

示例：可用于分析 `raise ... from e` 中的多个异常链

## ipdb

`pdb` 和 `ipdb` 都是 Python 中用于调试程序的工具，但它们之间有一些关键区别，主要体现在用户体验、功能扩展和依赖方面。

| 调试器 | 全称             | 所属项目      | 依赖                |
| ------ | ---------------- | ------------- | ------------------- |
| `pdb`  | Python Debugger  | Python 标准库 | 无（内置模块）      |
| `ipdb` | IPython Debugger | IPython 项目  | `ipython`（需安装） |

1. `pdb`

   - Python 官方标准库提供的命令行调试器。
   - 提供基本的调试功能：断点、单步执行、查看变量、堆栈跟踪等。
   - 轻量、无依赖，可在任何 Python 环境中使用。
   - 使用：

     ```python
     import pdb
     pdb.set_trace()  # 程序将在此暂停进入调试模式
     ```

2. `ipdb`

   - `pdb` 的一个增强版本，基于 IPython。
   - 提供更强的交互式调试体验。
   - 使用 IPython 的特性（如自动补全、语法高亮、历史记录、魔法命令等）。
   - 安装：

     ```python
     pip install ipdb
     ```

   - 使用：

     ```python
     import ipdb
     ipdb.set_trace()
     ```

**核心区别对比**

| 功能                    | `pdb`                    | `ipdb`                                           |
| ----------------------- | ------------------------ | ------------------------------------------------ |
| 自动补全（tab 补全）    | ❌                       | ✅                                               |
| 语法高亮                | ❌                       | ✅                                               |
| 多行编辑                | ❌                       | ✅ （依赖 IPython shell）                        |
| 支持 IPython 魔法命令   | ❌                       | ✅                                               |
| 异常调试（post-mortem） | ✅                       | ✅                                               |
| 依赖 IPython            | ❌                       | ✅                                               |
| 默认交互体验            | 命令行原始交互           | IPython shell 风格（类似 Jupyter Notebook）      |
| 适用场景                | 所有环境，特别是轻量环境 | 更复杂、更丰富的调试体验，适合开发机或交互式开发 |

**总结**

- `pdb` 是 Python 内置的调试器，简单、无依赖、可随时用。
- `ipdb` 提供更好的用户体验，尤其在需要频繁交互、使用历史记录、补全等功能时非常强大。
- 两者接口一致，`set_trace()` 等使用方式几乎相同，方便替换。

## 注意事项

1. `ipdb` 无法进行交互
   原因是是**运行它的终端环境没有启用 readline 或没有走交互式终端输入模式**，所以上下左右箭头的按键转义序列（`^[[A`、`^[[B` 等）没有被解析成历史记录或光标移动。

   **常见原因**

   1. **ipdb 运行在非交互终端（stdin 不是 tty）**
      比如你是通过 `python script.py 2>&1 | tee log.txt` 运行，或在 `tmux` / `screen` 的非交互模式里运行，
      这时标准输入输出被管道重定向，`ipdb` 以为自己没有终端控制能力。

   2. **没有安装 `readline` 或 `prompt_toolkit`**
      `ipdb` 默认依赖 Python 的 `readline` 模块（Linux/macOS 内置，Windows 需要 `pyreadline`）。
      如果缺失，按键就会原样显示 `^[[A`。

   3. **远程环境缺少正确的 TERM 设置**
      如果 `$TERM` 变量没设置（或设置成 `dumb`），终端控制符就不会被识别。

   4. **使用了 minimal shell 或容器里缺少终端库（如 ncurses）**
      有些精简镜像里 `libncurses` 不全，`readline` 功能就失效。
