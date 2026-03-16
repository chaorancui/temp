[toc]

# python 常用库\_5

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
import os, sys, shutil, re
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
    sys.exit(main())
```

五、argparse 库使用惯例

**一、个人写法推荐**

argparse 写在：

- **main 函数里（推荐做法）**
- **全局作用域**

1. **写在 `main()` 函数里（推荐做法）**

   ```python
   import argparse

   def main():
       parser = argparse.ArgumentParser(description="Example program")
       parser.add_argument('--verbose', action='store_true')
       args = parser.parse_args()

       if args.verbose:
           print("Verbose mode on")

   if __name__ == "__main__":
       main()
   ```

   **优点：**
   - 遵循 Python 程序的入口惯例（`if __name__ == "__main__":`）。
   - 方便封装逻辑，后续可以复用 `main()` 或在单元测试时绕过参数解析。
   - 避免全局作用域在 import 时就执行 `argparse.parse_args()`（会导致导入时报错）。

   这是 Python 官方文档和大多数项目推荐的方式。

2. **写在全局作用域**

   ```python
   import argparse

   parser = argparse.ArgumentParser(description="Example program")
   parser.add_argument('--verbose', action='store_true')
   args = parser.parse_args()   # ⚠️ 在导入时就会执行
   ```

   **缺点：**
   - 如果这个文件被其他模块 import，会立刻尝试解析命令行参数，通常会报错（因为没有传递参数）。
   - 不利于测试和扩展，几乎没有大型项目这样写。

   适用场景：
   - 小脚本（one-off scripts），只在命令行运行，且不会被 import。
   - 临时工具，个人使用。

**二、Python 官方库/工具的写法**
Python **标准库**和**官方工具**的源码，普遍写法是：

1. **argparse 写在 main 函数内，parse_args 在 main 中调用**

   **`venv` 标准库**（Python 的虚拟环境工具）就是这样：

   ```python
   def main(args=None):
       import argparse
       parser = argparse.ArgumentParser(...)
       parser.add_argument(...)
       options = parser.parse_args(args)
       ...

   if __name__ == '__main__':
       sys.exit(main())
   ```

2. **函数参数传递 args（便于单元测试）**

   很多官方库不会直接 `parse_args()`，而是允许 `main(args)` 接收一个参数：
   - **`pydoc` 源码** 和 **`unittest` CLI** 都是这样写的。
   - 这样测试时可以直接传一个 `list` 作为参数，而不是依赖命令行。

   ```python
   def main(argv=None):
       parser = argparse.ArgumentParser()
       parser.add_argument('--foo')
       args = parser.parse_args(argv)
       print(args.foo)

   if __name__ == "__main__":
       import sys
       main(sys.argv[1:])
   ```

**总结（最佳实践）**

1. **推荐写在 `main()` 函数里**，并在 `if __name__ == "__main__":` 里调用。
2. 如果要做测试/复用，建议 `main(argv=None)` 并把 `parse_args(argv)` 放里面。
3. 全局作用域里写 argparse 只适合一次性的小脚本。

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

## Pydantic 库

**一、Pydantic 简介**

Pydantic 是一个基于 Python 类型提示的数据验证和设置管理库。它利用 Python 3.6+ 的类型注解来定义数据模型，并在运行时自动验证传入的数据，将其转换为正确的类型，同时提供友好的错误信息。

**核心功能**：

- **数据验证**：根据模型定义自动检查字段类型、范围、约束等。
- **类型转换**：尝试将输入转换为声明的类型（如字符串 `"123"` 转为整数 123）。
- **序列化/反序列化**：轻松将模型实例转换为字典、JSON 或其他格式。
- **解析复杂结构**：支持嵌套模型、列表、联合类型等。
- **集成友好**：与 FastAPI、Flask、Django 等 Web 框架无缝集成。

**二、核心概念与基本用法**

1. 定义模型

   继承 `pydantic.BaseModel`，使用类型注解声明字段。

   ```python
   from pydantic import BaseModel

   class User(BaseModel):
       id: int
       name: str
       age: int = 0          # 默认值
       email: str | None = None   # 可选字段，默认为 None
   ```

2. 实例化与验证

   创建实例时自动进行验证和类型转换。

   ```python
   user = User(id="123", name="Alice", age="25")  # 字符串自动转为 int
   print(user)  # id=123 name='Alice' age=25 email=None
   ```

   如果数据不合法，抛出 `pydantic.ValidationError`：

   ```python
   try:
       User(id="abc", name="Bob")  # id 无法转为 int
   except ValidationError as e:
       print(e)
   ```

3. 字段类型与约束

   支持多种内置类型及自定义类型：
   - 基本类型：`int`, `float`, `str`, `bool`, `bytes`
   - 容器类型：`List`, `Dict`, `Set`, `Tuple`
   - 特殊类型：`Optional`, `Union`, `Literal`, `Any`
   - 约束类型：`conint`, `constr`, `EmailStr`, `UrlStr` 等（需导入）

   ```python
   from pydantic import constr, conint, EmailStr

   class Product(BaseModel):
       name: constr(min_length=1, max_length=100)  # 字符串长度限制
       price: conint(gt=0, le=10000)                # 整数范围
       email: EmailStr                               # 邮箱格式
   ```

4. 自定义验证器

   使用 `@field_validator`（Pydantic v2）或 `@validator`（v1）为字段添加自定义验证逻辑。

   ```python
   from pydantic import field_validator

   class Order(BaseModel):
       quantity: int
       price: float

       @field_validator('quantity')
       def check_positive(cls, v):
           if v <= 0:
               raise ValueError('quantity must be positive')
           return v
   ```

   Pydantic v2 引入了 `@model_validator` 用于跨字段验证：

   ```python
   from pydantic import model_validator

   class Booking(BaseModel):
       start: int
       end: int

       @model_validator(mode='after')
       def check_start_before_end(self):
           if self.start >= self.end:
               raise ValueError('start must be before end')
           return self
   ```

5. 嵌套模型

   模型可以嵌套其他模型，形成复杂结构。

   ```python
   class Address(BaseModel):
       city: str
       street: str

   class Person(BaseModel):
       name: str
       address: Address

   data = {'name': 'Alice', 'address': {'city': 'Beijing', 'street': 'Main St'}}
   person = Person(**data)
   print(person.address.city)  # Beijing
   ```

6. 配置（Config）

   通过内部类 `Config` 或 `model_config` 设置模型行为，如允许额外字段、字段别名、严格模式等。

   Pydantic v2 使用 `model_config` 字典：

   ```python
   from pydantic import BaseModel, ConfigDict

   class MyModel(BaseModel):
       model_config = ConfigDict(extra='forbid')  # 禁止额外字段
       name: str
   ```

7. 解析与导出
   - **从字典/JSON 创建**：`Model(**data)` 或 `Model.model_validate(data)`（v2）。
   - **导出为字典**：`model.model_dump()`。
   - **导出为 JSON**：`model.model_dump_json()`。

   ```python
   user = User(id=1, name="Alice")
   user_dict = user.model_dump()          # {'id': 1, 'name': 'Alice', 'age': 0}
   user_json = user.model_dump_json()     # '{"id":1,"name":"Alice","age":0}'
   ```

8. 错误处理

   验证失败时捕获 `ValidationError`，可通过 `e.errors()` 获取详细错误列表。

**三、典型使用场景**

1. 配置管理

   将配置文件（YAML/JSON）加载为 Pydantic 模型，确保配置项类型正确、字段完整，并自动完成类型转换。例如之前的 `TestCaseConfig`：

   ```python
   from pydantic import BaseModel
   from typing import Optional

   class VerificationConfig(BaseModel):
       golden_path: str = ""
       output_path: str = ""

   class TestCaseConfig(BaseModel):
       test_config_path: str
       verification_config: VerificationConfig

   # 从 YAML 加载后验证
   raw = yaml.safe_load(open("case.yaml"))
   case = TestCaseConfig.model_validate(raw)
   ```

   优势：配置结构清晰，错误在启动时暴露，避免运行时因配置错误导致崩溃。

2. 数据清洗与解析

   处理外部数据（如 CSV、第三方 API 响应），将其转换为结构化模型。

   ```python
   import csv
   from pydantic import BaseModel, ValidationError

   class Stock(BaseModel):
       symbol: str
       price: float

   stocks = []
   with open('stocks.csv') as f:
       reader = csv.DictReader(f)
       for row in reader:
           try:
               stocks.append(Stock(**row))
           except ValidationError as e:
               print(f"Invalid row: {row}, error: {e}")
   ```

3. 环境变量解析

   使用 `pydantic-settings` 将环境变量映射为配置对象。

   ```python
   from pydantic_settings import BaseSettings

   class Settings(BaseSettings):
       database_url: str
       debug: bool = False

       class Config:
           env_prefix = "MYAPP_"   # 环境变量前缀

   settings = Settings()  # 自动从 os.environ 读取
   ```

4. API 请求/响应验证

   与 FastAPI 深度集成，自动验证请求体和响应。

   ```python
   from fastapi import FastAPI
   from pydantic import BaseModel

   app = FastAPI()

   class Item(BaseModel):
       name: str
       price: float

   @app.post("/items/")
   async def create_item(item: Item):   # FastAPI 自动验证并注入 item
       return item
   ```

**四、Pydantic v1 与 v2 主要区别**

| 特性        | v1                         | v2                                             |
| :---------- | :------------------------- | :--------------------------------------------- |
| 验证器      | `@validator`               | `@field_validator`                             |
| 模型验证器  | -                          | `@model_validator`                             |
| 配置        | 内部类 `Config`            | `model_config = ConfigDict(...)`               |
| 解析方法    | `obj.dict()`, `obj.json()` | `obj.model_dump()`, `obj.model_dump_json()`    |
| 从 ORM 创建 | `from_orm`                 | `model_validate` (with `from_attributes=True`) |

**五、在你的项目中使用 Pydantic 的收益**

- **强类型保障**：避免配置中字段类型错误（例如将布尔值写成字符串）。
- **自动路径拼接**：通过自定义验证器或字段处理，可统一处理相对路径。
- **清晰的错误定位**：当 YAML 缺少字段或类型错误时，Pydantic 会明确指出是哪个用例的哪个字段有问题。
- **易于扩展**：新增字段只需在模型类中添加类型注解，其余逻辑自动生效。

**六、总结**

Pydantic 是现代 Python 数据验证的事实标准，它通过类型提示实现了声明式的数据模型，让数据验证、清洗和序列化变得简单而可靠。无论是配置管理、API 开发还是数据解析，Pydantic 都能显著提升代码的健壮性和可维护性。
