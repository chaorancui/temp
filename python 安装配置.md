# python 安装配置

## 查看 python 版本

查看 python 版本：python --version

windows 查看安装 python 版本：py -0

查看 python 安装路径：where python

## 代码格式化插件

### yapf

`yapf` (Yet Another Python Formatter) 是 Google 开发的 Python 代码格式化工具，支持 `pep8`、`google`、`facebook` 和 `chromium` **4 种内置预设风格（built-in styles）**，还可自定义风格，调整自定义缩进、换行、括号样式、对齐方式等。

**一、内置风格（built-in styles）**（共 4 个）

你可以通过参数 `--style=<style_name>` 或在配置文件中指定 `based_on_style = <style_name>` 来使用它们。

下面是这 4 种风格的核心区别总结：

1. `pep8`（Python 官方风格）

   - **基准：** [PEP 8](https://peps.python.org/pep-0008/)
   - **缩进宽度：** 4 空格
   - **换行控制：** 比较宽松（更早换行）
   - **函数参数换行：** 尽量放在多行，尤其当参数较多时
   - **推荐用途：** 想遵循 Python 官方规范的人

   ```python
   def foo(a, b, c,
           d, e, f):
       pass
   ```

2. `google`

   - **基准：** Google Python Style Guide
   - **缩进宽度：** 4 空格
   - **函数参数：** 尽可能保持在一行，除非超长
   - **字典、列表等结构体：** 尽量紧凑
   - **推荐用途：** 喜欢 Google 风格、简洁写法的人

   ```python
   def foo(a, b, c, d, e, f):
       pass
   ```

3. `chromium`

   - **基准：** Chromium 项目中的 Python 风格
   - **缩进宽度：** 2 空格（与其他风格不同）
   - **格式更紧凑：** 倾向少换行，节省垂直空间
   - **推荐用途：** Chromium、Google 工程代码一致性需求

   ```python
   def foo(a, b, c, d, e, f):  # 使用 2 空格缩进
     pass
   ```

4. `facebook`

   - **Facebook 风格（不公开文档）**
   - **缩进宽度：** 4 空格
   - **长行换行：** 更激进的分行
   - **字典和函数参数：** 倾向多行，尤其在超过列宽限制时
   - **推荐用途：** 喜欢更加规整、清晰结构风格的人

   ```python
   def foo(
       a, b, c,
       d, e, f,
   ):
       pass
   ```

小结：

| 特性              | pep8     | google   | chromium   | facebook   |
| ----------------- | -------- | -------- | ---------- | ---------- |
| 缩进              | 4 空格   | 4 空格   | **2 空格** | 4 空格     |
| 参数换行倾向      | 较早换行 | 尽量一行 | 尽量一行   | 较激进换行 |
| 风格紧凑度        | 中等     | 紧凑     | 紧凑       | 宽松       |
| 多行列表/字典格式 | 较宽松   | 紧凑     | 紧凑       | 更倾向多行 |

**二、自定义风格（custom styles）**

你可以基于上述任意一个内置风格**自定义参数**，创建你自己的配置文件。`yapf` 配置文件可以放在多个位置，会按照一定的顺序查找这些配置文件。以下是可以放置 `yapf` 配置支持格式和优先级顺序：

1. `yapf` 支持的配置文件格式包括：

   - `setup.cfg`
   - `tox.ini`
   - `.style.yapf`
   - `pyproject.toml`（支持较新版本）

2. `yapf` 配置文件的查找优先级（从高到低）：

   1. 显式指定配置路径（最高优先级）

      - 使用 `--style=/path/to/your/configfile` 指定的配置文件。

   2. 当前目录及其父目录中查找配置文件

      按以下顺序查找，并向上递归查找，直到文件系统根或用户主目录：

      - `.style.yapf`
      - `setup.cfg` （含 `[yapf]` section）
      - `tox.ini` （含 `[yapf]` section）
      - `pyproject.toml`（含 `[tool.yapf]` section，v0.32.0+ 支持）

   3. 用户主目录中的 `.style.yapf`（如果存在）

      - 路径通常是 `~/.style.yapf` 或 `%USERPROFILE%\.style.yapf`
      - 属于“全局配置”，如果项目中没有配置文件，会使用它。

   4. 默认内置风格

      - 如果没有找到任何配置文件，使用 `pep8` 风格作为默认。
      - 除非显式指定了 `--style=google`、`chromium`、`facebook` 等。

   | 优先级 | 来源                                             | 示例说明                         |
   | ------ | ------------------------------------------------ | -------------------------------- |
   | 1      | 显式指定 `--style=path`                          | `yapf --style=mycfg.cfg code.py` |
   | 2      | 当前目录及向上查找 `.style.yapf`、`setup.cfg` 等 | 项目级配置                       |
   | 3      | 用户主目录 `~/.style.yapf`                       | 全局配置                         |
   | 4      | 默认风格 `pep8`                                  | 无配置文件时的兜底风格           |

3. 配置内容

   方式 1：`.style.yapf`

   ```ini
   [style]
   based_on_style = pep8
   indent_width = 4
   column_limit = 100
   ```

   方式 2：`setup.cfg`

   ```ini
   [yapf]
   based_on_style = pep8
   indent_width = 2
   ```

   方式 3：`pyproject.toml`（v0.32.0+ 支持）

   ```toml
   [tool.yapf]
   based_on_style = "pep8"
   indent_width = 4
   column_limit = 120
   ```

   建议

   - 如果是单个项目，推荐将 `.style.yapf` 或 `setup.cfg` 放在项目根目录。
   - 如果多个项目共用一套规则，可以放到用户目录下 `~/.style.yapf`（但不是所有版本都支持）。
   - 使用 `--style=...` 显式指定配置文件，可以避免查找混乱。

4. 可配置项

   可以在官方文档或运行以下命令查看所有可用项 `yapf --style-help`。

   1. 基本缩进设置

      - `indent_width=4`：缩进宽度为 4 个空格。
      - `continuation_indent_width=4`：续行缩进宽度为 4 个空格。
      - `use_tabs=False`：不使用制表符，仅用空格。
      - `indent_blank_lines=False`：不缩进空行。

   2. 括号与缩进处理

      - `align_closing_bracket_with_visual_indent=True`：闭合括号与视觉缩进对齐。
      - `coalesce_brackets=False`：不合并连续括号。
      - `dedent_closing_brackets=False`：闭合括号不单独一行并取消缩进。
      - `indent_closing_brackets=False`：闭合括号不单独一行并缩进。
      - `space_inside_brackets=False`：括号/方括号/花括号内部不加空格。
      - `space_between_ending_comma_and_closing_bracket=True`：结束逗号与闭合括号间加空格。

   3. 字典与集合格式

      - `allow_multiline_dictionary_keys=False`：禁止字典键跨多行。
      - `each_dict_entry_on_separate_line=True`：每个字典条目单独一行。
      - `force_multiline_dict=False`：不强制多行字典格式。
      - `indent_dictionary_value=False`：字典值不缩进。
      - `allow_split_before_dict_value=True`：允许在字典值前换行。
      - `spaces_around_dict_delimiters=False`：字典分隔符周围不加空格。

   4. 列表与元组格式

      - `spaces_around_list_delimiters=False`：列表分隔符周围不加空格。
      - `spaces_around_tuple_delimiters=False`：元组分隔符周围不加空格。
      - `disable_split_list_with_comment=False`：允许在含注释的列表中换行。
      - `disable_ending_comma_heuristic=False`：不禁用以逗号结尾的列表换行规则。

   5. 运算符与表达式格式

      - `arithmetic_precedence_indication=False`：不用空格表示运算符优先级。
      - `no_spaces_around_selected_binary_operators=`：未指定禁止空格的二元运算符。
      - `spaces_around_power_operator=False`：幂运算符周围不加空格。
      - `spaces_around_subscript_colon=False`：切片运算符周围不加空格。
      - `split_before_arithmetic_operator=False`：不在算术运算符前换行。
      - `split_before_bitwise_operator=True`：在位运算符前换行。
      - `split_before_logical_operator=True`：在逻辑运算符前换行。

   6. 函数与参数格式

      - `allow_split_before_default_or_named_assigns=True`：允许在默认值/命名赋值前换行。
      - `split_before_named_assigns=False`：不在命名赋值前换行。
      - `split_arguments_when_comma_terminated=False`：逗号结尾时不换行参数列表。
      - `split_before_first_argument=False`：不在第一个参数前换行。
      - `split_before_expression_after_opening_paren=False`：不在开括号后表达式前换行。

   7. 换行与拆分规则

      - `join_multiple_lines=True`：合并短行为一行。
      - `split_all_comma_separated_values=False`：不拆分所有逗号分隔值。
      - `split_all_top_level_comma_separated_values=False`：不拆分顶级逗号分隔值。
      - `split_before_closing_bracket=False`：不在闭合括号前换行。
      - `split_before_dict_set_generator=True`：在字典/集合生成器前换行。
      - `split_before_dot=False`：不在点号前换行。
      - `split_complex_comprehension=False`：不拆分复杂推导式。

   8. 注释与文档字符串

      - `spaces_before_comment=2`：行尾注释前保留 2 空格。
      - `blank_line_before_class_docstring=False`：类文档字符串前不插空行。
      - `blank_line_before_module_docstring=False`：模块文档字符串前不插空行。
      - `i18n_comment=`：未设置国际化注释正则。
      - `i18n_function_call=`：未设置国际化函数调用名。

   9. 空行与间距

      - `blank_lines_around_top_level_definition=2`：顶级定义周围保留 2 空行。
      - `blank_lines_between_top_level_imports_and_variables=1`：顶级导入与变量间保留 1 空行。
      - `blank_line_before_nested_class_or_def=True`：嵌套类/函数前插空行。
      - `spaces_around_default_or_named_assign=False`：默认值/命名赋值周围不加空格。

   10. Lambda 与推导式

       - `allow_multiline_lambdas=False`：禁止多行 Lambda 表达式。
       - `split_complex_comprehension=False`：不拆分复杂推导式。
       - `split_penalty_comprehension=80`：推导式换行惩罚值为 80。

   11. 换行惩罚值（Split Penalties）

       - `split_penalty_after_opening_bracket=30`：开括号后换行惩罚值。
       - `split_penalty_after_unary_operator=10000`：一元运算符后换行惩罚值。
       - `split_penalty_arithmetic_operator=300`：算术运算符换行惩罚值。
       - `split_penalty_bitwise_operator=300`：位运算符换行惩罚值。
       - `split_penalty_logical_operator=300`：逻辑运算符换行惩罚值。
       - `split_penalty_before_if_expr=0`：if 表达式前换行惩罚值。
       - `split_penalty_excess_character=7000`：超列限制惩罚值。
       - `split_penalty_for_added_line_split=10`：新增换行惩罚值。
       - `split_penalty_import_names=0`：导入名称拆分惩罚值。

   12. 其他杂项

       - `column_limit=120`：列限制为 120 字符。
       - `continuation_align_style=SPACE`：续行对齐使用空格。
       - `split_before_dict_set_generator=True`：字典/集合生成器前换行。
       - `split_before_semicolon = True`：分号前会自动换行

**三、vscode 配置**

1. pip 安装 ypaf，vscode 安装插件
2. 把 formatter 设置为 ypaf
3. 项目中直接建立配置文件，或者通过 vscode 指定配置文件

或者直接在 `settings.json` 中直接添加：

```json
    "[python]": {
        "editor.defaultFormatter": "eeyore.yapf"
    },
    "yapf.args": [
        "--style=xxx/.style.yapf"
    ]
```

参考：`.style.yapf`

```ini
[style]
based_on_style = pep8

# 每行字符限制
column_limit = 120

# 是否第一个参数前换行
split_before_first_argument = False
# 是否闭合括号前换行
split_before_closing_bracket = False
# 是否在含注释的列表中换行
disable_split_list_with_comment = False
# 是否命名赋值前换行
split_before_named_assigns = False
# 是否列表每个元素强制换行
each_dict_entry_on_separate_line = False
# 是否分号前会自动换行
split_before_semicolon = False
```

# pip 命令

pip 是 Python 包管理工具，该工具提供了对 Python 包的查找、下载、安装、卸载的功能。

```shell
pip --version	# 显示版本和路径，也可判断是否已经安装pip
pip --help		# 获取帮助
pip list		# 列出已安装的包
pip list -o		# 查看可升级的包
pip install -U pip	# 升级 pip
# 安装包
pip install SomePackage              # 最新版本
pip install SomePackage==1.0.4       # 指定版本
pip install 'SomePackage>=1.0.4'     # 最小版本

# 显示安装包信息
pip show xxx

# 升级包
pip install --upgrade xxx

# 删除包
pip uninstall xxx

# 搜索包
pip search xxx

# 软件源安装某个包（临时使用）
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple xxx		# 清华源
```

# python 虚拟环境

Python 版本更新比较快速，主要原因有：活跃的开发社区、适应技术变化、改进性能、修复安全漏洞等。尽管版本更新频繁，但主要版本（如 Python 2 到 Python 3）之间通常会有较长的过渡期。因此不同的机器上安装的 python 版本和依赖库版本不同。

考虑这种情况：你正在开发应用程序 A，使用你的系统安装的 Python 和你 pip install 安装的 packageX 的 1.0 版本到全局 Python 库。然后你切换到本地机器上的项目 B，并安装了相同的 packageX，但版本为 2.0，在 1.0 和 2.0 之间有一些突破性的变化。当你回去运行你的项目 A 时，你遇到了各种各样的错误，而且你的项目不能运行。这是你在用 Python 构建软件时可能遇到的情况。而为了解决这个问题，我们可以使用虚拟环境。

使用虚拟环境时可能会遇到`virtualenv`、`venv`、`pipenv`等名词，下面是他们的区别：

## virtualenv 虚拟环境

`virtualenv` 是目前最流行的 Python 虚拟环境配置工具。它不仅同时支持 Python2 和 Python3，而且可以为每个虚拟环境指定 Python 解释器，并选择不继承基础版本的包。

```shell
# 安装 virtualenv
pip install virtualenv

# 创建虚拟环境
virtualenv [虚拟环境名称]
# –no-site-packeages参数，意义在于不复制已经安装到系统Python环境中的所有第三方包从而得到一个“纯净”的运行环境。
virtualenv --no-site-packages [虚拟环境名称]

# 激活环境
cd venv
source ./bin/activate	# Linux
.\Scripts\activate.bat	# Windows

# 退出环境
deactivate					# Linux
.\Scripts\deactivate.bat	# Windows

# 删除环境
# 直接删除venv文件夹来删除环境

# 使用环境
# 进入环境后，一切操作和正常使用python一样 安装包使用pip install 包。
```

## venv

Python 从 3.3 版本开始，自带了一个虚拟环境 venv，在 PEP-405 中可以看到它的详细介绍。它实际是 virtualenv 的一个子集被整合到标准库的 venv 模块下，因此很多操作都和 virtualenv 类似，但是两者运行机制不同。因为是从 3.3 版本开始自带的，这个工具也仅仅支持 python 3.3 和以后版本。所以，要在 python2 上使用虚拟环境，依然要利用 virtualenv。

## pipenv

**pipenv 是 Python 官方推荐的包管理工具。** pipenv 是 Pipfile 主要倡导者、requests 作者 Kenneth Reitz 写的一个命令行工具，主要包含了 Pipfile、pip、click、requests 和 virtualenv，能够有效管理 Python 多个环境，各种第三方包及模块。

```shell
# 安装 pipenv
pip install pipenv

# 创建虚拟环境
# pipenv以是基于项目的，首先新建项目文件夹
cd myproject
pipenv install  # 使用本地默认版本的python
pipenv --two  # 使用当前系统中的Python2 创建环境
pipenv --three  # 使用当前系统中的Python3 创建环境
pipenv --python 3.6  # 指定使用Python3.6创建环境


# 激活环境
pipenv shell

# 退出环境
exit

# 删除环境
pipenv --rm

# 使用环境
# 不要使用pip安装库，而要使用pipenv install命令
pipenv install xxx
pipenv install requests  # 或者直接安装库
```

## conda

conda 可以直接创建不同 python 版本的虚拟环境。前面讲的 virtualenv 只是指定创建不同 python 版本的虚拟环境，前提是你的电脑上已经安装了不同版本的 python，与 conda 相比没有 conda 灵活。
