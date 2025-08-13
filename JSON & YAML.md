[toc]

# JSON & YAML

# JSON

## 使用注释：

> 参考链接：
>
> [1]. [在 JSON 文件中注释](https://www.freecodecamp.org/chinese/news/comments-in-json/)
>
> [2]. []

JSON（JavaScript Object Notation，JavaScript 对象表示法）因其简单灵活而成为 web 开发和移动应用程序中常用的数据交换格式。

但 JSON 文件本身并不支持注释。这使得为数据提供额外的上下文或解释具有挑战性。

### 为什么 JSON 不支持注释

根据 JSON 规范，JSON 文档只应包含数组和对象等数据结构，而不应包含注释。这是因为 JSON 是一种简单的、易于解析的数据格式，可以快速有效地进行处理。

注释虽然有助于为人类读者提供额外的上下文或解释，但会**增加解析过程的复杂性**。这会降低性能并增加出错的风险。

JSON 不支持注释的主要原因是，其创建者道格拉斯·克罗克福特（Douglas Crockford）特意从格式中删除了注释，以防止误用并使其保持为纯数据格式。

克罗克福特观察到有些人使用注释来存储解析指令，这可能会**破坏不同系统之间的兼容性**。因此，他决定删除注释，以**保持格式在各种编程语言和环境中的简洁性和一致性**。

因此，在 JSON 文件中添加注释的唯一选择就是使用变通方法，例如使用自定义元素来存储注释。

### 如何在 JSON 中添加注释

当你以常用编程语言中使用的 `//`、`#` 或 `/* */` 的形式添加注释时，你会发现 “JSON 中不允许添加注释 ”的**错误**。

唯一的办法就是在 JSON 文件中**将注释作为数据对加入**。这种做法并不常用，也不值得推荐，**但严格来说，这是添加注释到 JSON 文件的最佳方法**。

在 JSON 对象中创建一个自定义元素（如 “//comment”），以便将注释与其他数据区分开来。

> **注意：**并非必须使用两个斜线。你可以决定使用井号，如 “#comment” 或任何其他允许的字符。**这样做的目的是为了明确这是一个注释。**

### 其他方法

- 使用约定俗成的 key 作为注释字段

  如以"//"作为注释的 key. 但是如果有多个以"//"为 key 的属性，是否符合协议的？答案是：**协议理论上不允许**。**实现上(几乎?)所有的 JS 环境都允许**，解析之后，**只保留最后一项**。常用的类似 key 还有： "\_comment", "#####"("#"个数自定)等。

- 使用 JSON5 规范

  JSON5 规范允许在 JSON 文件中加入注释：单行注释，多行注释均可

  可以使用 npm 的 json5 库，用法与 JSON 库类似。JSON5 规范见：https://json5.org/

# YAML

YAML（**YAML Ain't Markup Language**）是一种人类可读的**数据序列化格式**，常用于配置文件，替代 JSON 或 XML。它语法简洁，适合表达结构化数据。

## YAML 基础语法规则

- **缩进表示层级关系**（使用空格，通常为 2 或 4 个空格，不可使用 Tab）
- **键值对格式**：`key: value`
- **大小写敏感**
- **支持注释**：使用 `#` 开头

## YAML 文件结构和数据类型

1. **标量（Scalar）值**

   - 字符串、整数、浮点数、布尔值、null

   ```yaml
   name: Alice
   age: 25
   height: 1.70
   married: false
   nickname: null # 或 ~
   ```

2. **字符串（String）**

   - 普通字符串无需引号
   - 含空格或特殊字符的字符串可用 `' '` 或 `" "`

   ```yaml
   greeting: Hello
   quote1: "He said: Hello"
   quote2: 'She said: "Hi"'
   ```

3. **多行字符串**

   - **文字块（保留换行）**：`|`
   - **折叠块（自动合并换行）**：`>`

   ```yaml
   text_block: |
     This is line 1
     This is line 2

   text_folded: >
     This is line 1
     This is line 2
   ```

4. **布尔、Null、数字**

   ```yaml
   enabled: true
   disabled: false
   nothing: null
   count: 10
   pi: 3.14
   ```

5. **数组（序列 / 列表）**

   块格式（常用）：

   ```yaml
   fruits:
     - apple
     - banana
     - orange
   ```

   行内格式：

   ```yaml
   numbers: [1, 2, 3, 4, 5]
   ```

6. **字典（映射 / 对象）**

   块格式：

   ```yaml
   person:
     name: Alice
     age: 25
     email: alice@example.com
   ```

   行内格式：

   ```yaml
   person: { name: Alice, age: 25 }
   ```

7. **嵌套结构**

   组合字典与列表等结构很常见：

   ```yaml
   employees:
     - name: Tom
       age: 30
       skills:
         - Python
         - YAML
     - name: Jane
       age: 28
       skills:
         - Java
         - Spring

   company:
     name: Tech Corp
     location:
       city: Shanghai
       zip: 200000
   ```

8. **引用（Anchor `&`，别名 `\*`）**

   重复结构复用

   ```yaml
   default: &defaults
     retries: 3
     timeout: 30

   service1:
     <<: *defaults
     timeout: 60 # override

   service2:
     <<: *defaults
   ```

## 常见用途

- Kubernetes 配置（如 `deployment.yaml`）
- CI/CD 工具配置（GitHub Actions: `.github/workflows/*.yml`）
- 应用配置文件（如 Python 中的 `PyYAML` 加载）

## YAML vs JSON 对比

| 特性       | YAML             | JSON    |
| ---------- | ---------------- | ------- |
| 可读性     | 非常好           | 一般    |
| 注释支持   | 支持 `#` 注释    | 不支持  |
| 数据结构   | 一致             | 一致    |
| 文件扩展名 | `.yaml` / `.yml` | `.json` |

# TOML

TOML（Tom’s Obvious, Minimal Language）是一种简洁、可读性强的配置文件格式，广泛用于项目配置（如 `pyproject.toml`、`Cargo.toml`）。

## 基本语法规则

- **编码**：必须使用 UTF-8
- **键值对**：`key = value`，`=` 前后必须有至少一个空格
- **注释**：`#` 开头直到行尾
- **空行**：允许，用于分隔逻辑块
- **键名**：
  - 普通键：`my_key`
  - 含空格或特殊字符：`"my key"` 或 `'my key'`

```toml
# 这是注释
title = "My Project"
"app name" = "My App"
```

## 数据类型

1. **字符串**

   ```toml
   # 基本字符串
   str1 = "Hello"
   str2 = 'World'

   # 多行字符串
   multiline = """
   This is
   a multi-line
   string.
   """

   # 单引号多行（不转义）
   multiline_raw = '''
   Path: C:\Users\Name
   '''
   ```

2. **整数与浮点数**

   ```toml
   int_val = 42
   neg_int = -10
   float_val = 3.14
   sci_val = 1e6
   ```

3. **布尔值**

   ```toml
   bool_true = true
   bool_false = false
   ```

4. **日期与时间（RFC 3339 格式）**

   ```toml
   # UTC 日期时间
   utc_time = 1979-05-27T07:32:00Z

   # 带时区偏移
   offset_time = 1979-05-27T00:32:00-07:00

   # 本地日期时间
   local_dt = 1979-05-27T07:32:00

   # 本地日期
   local_date = 1979-05-27

   # 本地时间
   local_time = 07:32:00
   ```

## 数据结构

1. **表（Table）**

   - 表类似 Python 的字典，用 `[表名]` 声明。

   ```toml
   [owner]
   name = "Tom"
   dob = 1979-05-27T07:32:00Z
   ```

   等价 Python：

   ```python
   {
       "owner": {
           "name": "Tom",
           "dob": datetime(...)
       }
   }
   ```

2. **嵌套表**

   ```toml
   [database]
   server = "192.168.1.1"

   [database.settings]
   max_connections = 100
   ```

   等价 Python：

   ```python
   {
       "database": {
           "server": "192.168.1.1",
           "settings": {"max_connections": 100}
       }
   }
   ```

3. **内联表（Inline Table）**

   - 适合一行表示的小对象

   ```toml
   point = { x = 1, y = 2 }
   ```

4. **数组（Array）**

   ```toml
   fruits = ["apple", "banana", "pear"]
   numbers = [1, 2, 3, 4]
   mixed = [1, "two", 3.0] # 允许混合类型，但不推荐
   ```

5. **表数组（Array of Tables）**

   表示多个对象：

   ```toml
   [[products]]
   name = "Hammer"
   price = 10.0

   [[products]]
   name = "Nail"
   price = 0.1
   ```

   等价 Python：

   ```python
   {
       "products": [
           {"name": "Hammer", "price": 10.0},
           {"name": "Nail", "price": 0.1}
       ]
   }
   ```

6. **内联表数组**

   表数组可一行表示：

   ```toml
   products = [
       { name = "Hammer", price = 10.0 },
       { name = "Nail", price = 0.1 }
   ]
   ```

## 小结速查表

| 类型/结构    | TOML 写法示例                 | Python 等价类型 |
| ------------ | ----------------------------- | --------------- |
| 字符串       | `str = "abc"`                 | `str`           |
| 多行字符串   | `"""..."""`                   | `str`           |
| 整数         | `num = 42`                    | `int`           |
| 浮点数       | `pi = 3.14`                   | `float`         |
| 布尔值       | `yes = true`                  | `bool`          |
| 日期时间 UTC | `time = 1979-05-27T07:32:00Z` | `datetime`      |
| 数组         | `arr = [1, 2, 3]`             | `list`          |
| 表（Table）  | `[server]`                    | `dict`          |
| 嵌套表       | `[a.b]`                       | 嵌套 `dict`     |
| 内联表       | `{ x = 1 }`                   | `dict`          |
| 表数组       | `[[items]]`                   | `list[dict]`    |

如果你要的话，我可以帮你再画一张 **TOML 数据结构 → Python 数据类型映射图**，这样你直接就能对照用。
你要我帮你画那张图吗？
