[toc]

# python 常用库\_4

## pathlib

官方文档: <https://docs.python.org/3/library/pathlib.html>

`pathlib` 是 Python 3.4 引入的标准库模块，用于 **面向对象地处理文件路径**。它是对 `os.path` 的现代替代方案，支持更清晰、跨平台、更强大的文件路径操作。

| 特点     | 说明                                              |
| -------- | ------------------------------------------------- |
| 面向对象 | 用路径对象表示路径，而不是字符串                  |
| 跨平台   | 自动处理不同操作系统的路径分隔符（如 `/` vs `\`） |
| 简洁     | 比 `os.path` 写法更直观                           |
| 强大     | 内建文件系统操作能力（读写、遍历、匹配等）        |

**常见应用场景与示例**

1. 导入和创建路径对象

   ```python
   from pathlib import Path

   # 当前目录
   p = Path('.')

   # 拼接路径（更推荐用 / 运算符）
   file_path = p / 'subdir' / 'file.txt'
   print(file_path)  # subdir/file.txt 或 subdir\file.txt（取决于系统）
   ```

2. **列出文件夹下的所有文件**

   ```python
   for f in Path('.').iterdir():
       print(f)
   ```

   过滤出文件：

   ```python
   files = [f for f in Path('.').iterdir() if f.is_file()]
   ```

3. **递归遍历目录树**

   ```python
   for path in Path('.').rglob('*.py'):
       print(path)
   ```

   > `rglob` 支持递归通配，比如找出所有 `.log` 文件等。

4. **路径拼接（代替 os.path.join）**

   ```python
   root = Path('/home/user')
   log_file = root / 'logs' / 'app.log'
   ```

5. **文件名/父目录提取**

   ```python
   p = Path('/home/user/data.csv')

   print(p.name)       # data.csv
   print(p.stem)       # data
   print(p.suffix)     # .csv
   print(p.parent)     # /home/user
   print(p.parent.name)     # user

   # 路径末尾是否是文件/目录都通用
   Path('/home/user/data.csv').parent.name   # user
   Path('/home/user/').parent.name           # home

   # 获取多级父目录
   p.parents[0].name  # 等价于 p.parent.name -> user
   p.parents[1].name  # home
   ```

6. **检测路径/文件存在与类型**

   ```python
   p = Path('test.txt')

   p.exists()      # 文件或目录是否存在
   p.is_file()     # 是不是文件
   p.is_dir()      # 是不是目录
   ```

7. **读取与写入文件（简洁！）**

   ```python
   # 写入
   Path('log.txt').write_text('hello world')

   # 读取
   text = Path('log.txt').read_text()
   ```

   > 也支持 `write_bytes()` 和 `read_bytes()`。

8. **创建文件夹 / 删除文件**

   ```python
   # 创建目录（如果不存在）
   Path('newdir').mkdir(exist_ok=True)

   # 删除文件
   Path('oldfile.txt').unlink()
   ```

9. **匹配文件名（非递归）**

   ```python
   for file in Path('.').glob('*.py'):
       print(file)
   ```

10. **获取绝对路径 / 规范化路径**

    ```python
    p = Path('some/../path/./file.txt')
    print(p.resolve())   # 返回规范化的绝对路径
    ```

11. **替换后缀**

    批量替换 `.txt` 为 `.log`

    ```python
    from pathlib import Path

    p = Path("example.txt")

    new_path = p.with_suffix(".log")
    print(new_path)  # 输出：example.log
    ```

    **注意事项**
    - `with_suffix()` **替换原有后缀**，包括点 `.`。若原路径没有后缀，`with_suffix()` 会直接添加新的后缀：

      ```python
      Path("file").with_suffix(".log")  # 得到 file.log
      ```

    - 保留原始文件名 + 添加额外后缀（非替换）

      如果你想保留 `.dump` 并变成 `.dump.log`，不能用 `with_suffix()`，应这样写：

      ```python
      new_name = file.with_name(file.name + ".log")
      ```

    - 若文件是**双重后缀**（如 `.tar.gz`），只替换最后一个：

      ```python
      Path("archive.tar.gz").with_suffix(".zip")  # archive.tar.zip
      ```

    - 如果你要真正**重命名文件**，加上 `.rename()` 即可：

      ```python
      p.rename(p.with_suffix(".log"))
      ```

12. **过滤文件**

    `pathlib.Path.glob()` 本身**一次只能匹配一个 pattern**，但你可以用多种方式匹配多个 pattern，例如：`*.log`、`*.txt`、`*.dump` 等。下面是推荐的做法：
    1. 用 `rglob()` 支持递归搜索多类型文件（推荐）

       ```python
       from pathlib import Path

       p = Path("your_directory")
       files = []

       for pat in ["*.log", "*.txt", "*.dump"]:
           files.extend(p.rglob(pat))  # 递归搜索

       for f in files:
           print(f)
       ```

    2. 用多个 `.glob()` 合并结果

       ```python
       from pathlib import Path

       p = Path("your_directory")

       files = []
       for pattern in ("*.log", "*.txt", "*.dump"):
           files.extend(p.glob(pattern))

       for f in files:
           print(f)
       ```

    3. 用 `rglob()` 匹配查找

       ```python
       from pathlib import Path

       p = Path("your_dir")

       keywords = ["_succ", "_failed"]

       files = [f for f in p.rglob("*") if f.is_file() and any(k in f.name for k in keywords)]

       for f in files:
           print(f)
       ```

    | 方式                | 是否支持递归 | 多模式优雅度 | 推荐度 |
    | ------------------- | ------------ | ------------ | ------ |
    | `.rglob()` + 多模式 | 是           | 高           | 推荐   |
    | 多次 `.glob()` 合并 | 否           | 中等         | 推荐   |

**总结常用 API（备忘表）**

| 功能       | 方法                                                     |
| ---------- | -------------------------------------------------------- |
| 路径拼接   | `p / 'subdir' / 'file.txt'`                              |
| 获取名字   | `.name`, `.stem`, `.suffix`, `.parent`                   |
| 判断存在   | `.exists()`, `.is_file()`, `.is_dir()`                   |
| 遍历目录   | `.iterdir()`, `.glob()`, `.rglob()`                      |
| 文件操作   | `.read_text()`, `.write_text()`, `.unlink()`, `.mkdir()` |
| 规范化路径 | `.resolve()`                                             |

**推荐使用场景**

| 场景                             | pathlib 优势                     |
| -------------------------------- | -------------------------------- |
| 编写跨平台工具脚本               | 自动处理分隔符                   |
| 数据路径管理                     | 对路径字段统一处理               |
| 日志、缓存、输出路径构建         | 更清晰地拼接路径                 |
| 替代 os/os.path 写法             | 更可读、更现代化                 |
| 与 `open()`, `with` 搭配读写文件 | 可直接用路径对象，无需字符串转换 |

## pathlib VS shutil

在 Python 的文件操作界，`pathlib` 和 `shutil` 就像是**瑞士军刀**与**重型重工**的区别。

- `pathlib` 侧重于路径的“对象化”和基础操作。
- `shutil` 则专为高层级的“文件管理”（如递归拷贝、压缩）而生。

**一、核心操作对比表**

下面是这两个模块在常见任务中的对比：

| **操作类型**   | **pathlib (面向对象)**      | **shutil (功能增强)**            |
| -------------- | --------------------------- | -------------------------------- |
| **创建文件**   | `path.touch()`              | -                                |
| **创建目录**   | `path.mkdir(parents=True)`  | -                                |
| **移动**       | `path.rename(target)`       | `shutil.move(src, dst)` (更安全) |
| **拷贝文件**   | - (需结合 `write_bytes`)    | `shutil.copy2(src, dst)`         |
| **拷贝文件夹** | -                           | `shutil.copytree(src, dst)`      |
| **删除文件**   | `path.unlink()`             | -                                |
| **删除文件夹** | `path.rmdir()` (仅限空目录) | `shutil.rmtree(path)` (递归删除) |

**二、具体代码实现**

1. **创建操作 (Creating)**

   `pathlib` 是创建文件和目录的首选，它的语法非常直观。

   Python

   ```python
   from pathlib import Path
   import shutil

   p = Path("test_folder/sub_dir/file.txt")

   # 创建目录 (parents=True 相当于 mkdir -p)
   p.parent.mkdir(parents=True, exist_ok=True)

   # 创建空文件
   p.touch()
   ```

2. **拷贝操作 (Copying)**

   `pathlib` 本身没有内置的 `copy` 方法，这时必须使用 `shutil`。

   ```python
   source = Path("file.txt")
   dest = Path("backup/file_v2.txt")

   # 拷贝单个文件 (保留元数据)
   shutil.copy2(source, dest)

   # 拷贝整个文件夹
   shutil.copytree("my_project", "my_project_backup")
   ```

3. **移动操作 (Moving)**

   虽然 `pathlib` 有 `rename` 方法，但跨磁盘分区移动时可能会失败。`shutil.move` 则会自动处理这些底层细节。

   ```python
   # pathlib 方式 (推荐用于同磁盘改名)
   Path("old_name.txt").rename("new_name.txt")

   # shutil 方式 (推荐用于移动到不同位置)
   shutil.move("data.csv", "archive/data.csv")
   ```

4. **删除操作 (Deleting)**

   如果你要删除一个非空的文件夹，`pathlib` 会报错，此时 `shutil` 是唯一选择。

   ```python
   # 删除单个文件
   Path("temp.log").unlink(missing_ok=True)

   # 删除空文件夹
   Path("empty_dir").rmdir()

   # 强力删除整个文件夹及其内容
   shutil.rmtree("old_logs")
   ```

**三、场景推荐**

虽然两者经常配合使用，但你可以根据以下逻辑进行选择：

1. 优先使用 `pathlib` 的场景：
   - **路径计算与拼接**：使用 `path / "subdir" / "file.txt"` 比 `os.path.join` 优雅得多。
   - **文件属性检查**：判断是否存在 (`.exists()`)、是否是文件 (`.is_file()`)、获取后缀 (`.suffix`)。
   - **读取/写入小文件**：`path.read_text()` 和 `path.write_text()` 极其方便。
   - **创建目录/空文件**。

2. 必须使用 `shutil` 的场景：
   - **拷贝操作**：无论是拷贝文件还是整个目录。
   - **递归删除**：删除内含文件的文件夹（`rmtree`）。
   - **归档压缩**：如创建或解压 `.zip`、`.tar` 文件（`shutil.make_archive`）。
   - **跨设备移动**：将文件从 C 盘移动到 D 盘。

3. 最佳实践

   **混合使用。** 在现代 Python 代码中，通常先用 `pathlib.Path` 定义和处理路径对象，当涉及到复杂的拷贝或递归删除任务时，再将 Path 对象传递给 `shutil` 函数（`shutil` 函数完全兼容 Path 对象）。

## typing 库

Python 的 `typing` 库是 **类型提示（Type Hints）** 的核心工具库，Python 3.5 以后引入，旨在给 Python 这种动态语言增加静态类型检查的能力，提高代码可读性和可靠性，同时可以配合 IDE 或类型检查工具（如 `mypy`、Pyright）发现潜在错误。

**一、基本概念**

Python 本身是动态类型语言，不要求声明变量类型：

```python
a = 10
a = "hello"  # Python 允许
```

使用 `typing` 可以写类型提示，让代码更易理解，也便于静态分析：

```python
from typing import List, Dict

def greet(names: List[str]) -> None:
    for name in names:
        print(f"Hello, {name}")
```

- `names: List[str]` 表示 `names` 是一个字符串列表
- `-> None` 表示函数没有返回值

> **注意：Python 解释器不会强制检查类型**，它只是提示和静态分析工具用的。

**二、常用类型**

1. **基本集合类型**

   ```python
   from typing import List, Tuple, Set, Dict

   names: List[str] = ["Alice", "Bob"]
   point: Tuple[int, int] = (10, 20)
   unique_ids: Set[int] = {1, 2, 3}
   mapping: Dict[str, int] = {"Alice": 1, "Bob": 2}
   ```

2. **可选类型**

   ```python
   from typing import Optional

   def get_name(id: int) -> Optional[str]:
       if id == 1:
           return "Alice"
       return None
   ```

   - `Optional[str]` 等价于 `Union[str, None]`，表示可能是 `str` 或 `None`。

3. **多类型联合**

   ```python
   from typing import Union

   def parse(value: Union[str, int]) -> str:
       return str(value)
   ```

   - `Union` 表示可能是多种类型之一

4. **可调用对象**

   ```python
   from typing import Callable

   def apply(func: Callable[[int, int], int], x: int, y: int) -> int:
       return func(x, y)
   ```

   - `Callable[[arg1_type, arg2_type], return_type]` 表示函数签名

5. **Any**

   ```python
   from typing import Any

   def process(value: Any):
       print(value)
   ```

   - 表示可以是任意类型

6. **Literal（Python 3.8+）**

   ```python
   from typing import Literal

   def move(direction: Literal["up", "down", "left", "right"]):
       print(f"Moving {direction}")
   ```

   - 限定某个参数只能是几个固定值

7. **Generic / TypeVar（泛型）**

   ```python
   from typing import TypeVar, List

   T = TypeVar("T")

   def first_element(lst: List[T]) -> T:
       return lst[0]
   ```

   - 用于编写泛型函数或类

**三、高级类型提示**

1. **TypedDict（Python 3.8+）**
   - 给字典定义“结构化”字段类型

   ```python
   from typing import TypedDict

   class User(TypedDict):
       id: int
       name: str
       active: bool

   user: User = {"id": 1, "name": "Alice", "active": True}
   ```

2. **Protocol / Structural Subtyping**
   - 类似接口/结构类型

   ```python
   from typing import Protocol

   class SupportsClose(Protocol):
       def close(self) -> None: ...

   def cleanup(resource: SupportsClose):
       resource.close()
   ```

3. **Annotated（Python 3.9+）**
   - 附加元信息，比如用于验证或框架提示：

   ```python
   from typing import Annotated

   Age = Annotated[int, "must be positive"]
   def set_age(age: Age):
       print(age)
   ```

**四、使用场景**

1. **提高可读性**
   - 团队开发中，函数参数和返回值类型一目了然
   - 类似于文档注释，但更规范
2. **静态类型检查**
   - 配合工具（`mypy`, `Pyright`）提前发现类型错误
   - 避免运行时才报错
3. **IDE 智能提示**
   - PyCharm、VSCode 可以提供自动补全和类型提示
   - 方便调用函数和访问对象属性
4. **数据结构约束**
   - 用 `TypedDict`, `Literal` 限制字典字段、枚举值
   - 用 `Generic` 写泛型数据结构
5. **大型项目和 API 设计**
   - 明确输入输出类型，方便多人协作
   - 配合 docstring，自动生成 API 文档

**五、`typing` 常用类型一览图**
把 `List/Dict/Tuple/Union/Optional/Any/Literal/TypedDict/Callable` 的关系和使用场景都可视化如下

```plantuml
@startuml
title Python typing 常用类型一览（含使用场景）

package "集合类型" {
    class List {
        - 存放同类型元素
        - List[int], List[str]
        - 场景: 函数参数/返回值列表，处理同类数据集合
    }
    class Dict {
        - 键值对
        - Dict[str, int]
        - 场景: 配置、映射关系、JSON 数据
    }
    class Tuple {
        - 固定长度、可不同类型
        - Tuple[int, str]
        - 场景: 坐标、固定结构返回值
    }
    class Set {
        - 唯一元素集合
        - Set[int]
        - 场景: 去重、集合运算
    }
}

package "组合类型" {
    class Union {
        - 多种类型之一
        - Union[int, str]
        - 场景: 接受多种输入类型
    }
    class Optional {
        - Union[X, None]
        - 可选值
        - 场景: 参数可缺省或返回可能为空
    }
    class Any {
        - 任意类型
        - 场景: 灵活接口或暂不确定类型
    }
    class Literal {
        - 限定值集合
        - Literal['up','down']
        - 场景: 限定固定选项，例如枚举参数
    }
}

package "高级类型" {
    class Callable {
        - 函数类型
        - Callable[[int,str],bool]
        - 场景: 高阶函数参数，回调函数
    }
    class TypedDict {
        - 字典结构化类型
        - TypedDict('User', {'id':int, 'name':str})
        - 场景: JSON/配置文件数据结构约束
    }
    class Generic {
        - 泛型
        - TypeVar
        - 场景: 泛型函数/类，保持类型一致性
    }
    class Protocol {
        - 结构化子类型接口
        - duck typing
        - 场景: 类型约束，接口定义
    }
}

' 关系箭头
Optional --> Union : Optional[X] = Union[X,None]
List --> Generic
Dict --> Generic
Tuple --> Generic
Set --> Generic

@enduml
```

## typing.Mapping

**一、`typing.Mapping` 是什么**

`Mapping[K, V]` 是 **typing 模块中对“映射类型”的抽象类型注解**，表示：

> **任何“键 → 值”的只读映射接口**

它并不要求具体实现是 `dict`，只要对象**符合映射协议**即可。

```python
from typing import Mapping

def f(cfg: Mapping[str, int]) -> None:
    ...
```

这里的含义是：

- `cfg` 是一个“映射”
- key 类型是 `str`
- value 类型是 `int`
- **不承诺它是可变的**

**二、 `Mapping` 的位置（类型体系）**

在 typing 中，映射类型是一个**层级结构**：

```python
object
 └── collections.abc.Mapping
       ├── typing.Mapping[K, V]     （抽象、只读）
       └── typing.MutableMapping[K, V]
             └── dict
```

关键点：

- `Mapping` ≈ **只读 dict 接口**
- `MutableMapping` ≈ **可修改 dict 接口**
- `dict` 是 `MutableMapping` 的具体实现

**三、 `Mapping` vs `Dict` 的核心区别**

| 对比点            | `Dict[K, V]` | `Mapping[K, V]` |
| ----------------- | ------------ | --------------- |
| 是否限定为 `dict` | 是           | 否              |
| 是否允许修改      | 是           | 否（语义上）    |
| 抽象程度          | 具体         | 抽象            |
| API 约束          | 强           | 弱              |
| 推荐使用场景      | 构造、修改   | 只读访问        |

示例对比

```python
from typing import Dict, Mapping

def bad(cfg: Dict[str, int]) -> None:
    cfg["x"] = 1    # 合法，调用者必须接受修改

def good(cfg: Mapping[str, int]) -> None:
    cfg["x"] = 1    # ❌ 类型检查器会报错
```

**工程含义**：

- `Mapping` 明确告诉调用者：**我不会改你的数据**
- 这是“接口契约”的一部分

**四、 为什么工程中更推荐 `Mapping`**

1. 接口更稳定（面向接口编程）

   ```python
   def parse_cfg(cfg: Mapping[str, str]) -> None:
       ...
   ```

   调用方可以传入：
   - `dict`
   - `defaultdict`
   - `ChainMap`
   - `MappingProxyType`
   - 任何自定义映射类型

   而不破坏接口。

2. 防止“意外修改”配置

   **这是 `Mapping` 最常见的工程用途**

   ```python
   def load_compare_cfg(cfg: Mapping[str, object]) -> CompareCfg:
       ...
   ```

   语义非常明确：
   - `cfg` 是输入配置
   - 函数只读取，不负责修改

   这对**配置解析、YAML/JSON 反序列化、dataclass.from_dict** 尤其重要。

3. 类型系统层面的“只读语义”

   Python 运行时不会阻止你改：

   ```python
   cfg["x"] = 1  # 运行时仍然能改
   ```

   但：
   - mypy / pyright / pylance 会直接报错
   - IDE 会提示不合法

   这是**静态约束**，不是运行时约束。

**五、`Mapping` 支持的最小接口**

`Mapping` 要求对象至少实现：

```python
__getitem__(key)
__iter__()
__len__()
```

因此可以安全使用：

```python
def f(cfg: Mapping[str, int]) -> None:
    v = cfg["a"]
    for k in cfg:
        ...
    if "x" in cfg:
        ...
    cfg.get("y", 0)
```

但**不能假设**以下方法存在：

```python
cfg.pop(...)
cfg.update(...)
cfg.clear()
```

**六、与 dataclass / from_dict 的结合（强烈推荐）**

❌ 不推荐

```python
@staticmethod
def from_dict(data: dict) -> CompareCfg:
    ...
```

问题：

- 强制调用方只能传 `dict`
- 暗示函数可能修改入参

✅ 推荐

```python
from typing import Mapping, Any

@staticmethod
def from_dict(data: Mapping[str, Any]) -> CompareCfg:
    ...
```

好处：

- 表达“只读配置”
- 可接收任意映射类型
- API 语义更清晰

**七、`Mapping` vs `TypedDict`**

这是一个常见疑问。

| 对比         | `Mapping[str, Any]` | `TypedDict`        |
| ------------ | ------------------- | ------------------ |
| 键是否固定   | 否                  | 是                 |
| 是否声明结构 | 否                  | 是                 |
| 灵活性       | 高                  | 中                 |
| 严格性       | 低                  | 高                 |
| 典型场景     | 通用配置            | 协议 / JSON Schema |

示例

```python
class CompareCfgDict(TypedDict, total=False):
    expect_shape: list[int]
    real_shape: list[int]
    expect_dtype: str
```

工程实践中常见组合：

```python
def from_dict(data: Mapping[str, Any]) -> CompareCfg:
    ...
# 或
def from_dict(data: CompareCfgDict) -> CompareCfg:
    ...
```

**八、何时“必须”用 `Mapping`**

**强烈推荐用 `Mapping` 的场景**：

- 配置解析（YAML / JSON / CLI）
- from_dict / parse_xxx
- 工具函数只读访问 dict
- 库对外暴露的接口参数

**可以用 `Dict` 的场景**：

- 构造数据
- 明确要修改入参
- 内部实现细节（非公共 API）

**一句话总结**

> **`Mapping` 是“只读字典接口”的类型注解，是 Python 中“面向接口编程”的最佳实践之一。**

```plantuml
@startuml
title Python typing Collection / Mapping / Sequence 分层继承关系图

skinparam linetype ortho
skinparam ranksep 80
skinparam nodesep 60

' 强制从上到下布局
top to bottom direction

' ===========================
' 第一层：基础抽象类
' ===========================
package "Layer 1: Base ABC" <<Rectangle>> {
    interface "Iterable" as ITER
    interface "Sized" as SIZED
    interface "Container" as CONTAINER
}

ITER -[hidden]right- SIZED
SIZED -[hidden]right- CONTAINER

' ===========================
' 第二层：抽象子类
' ===========================
package "Layer 2: Abstract Collections" <<Rectangle>> {
    interface "Collection" as COLLECTION
    interface "Sequence" as SEQ
    interface "MutableSequence" as MSEQ
    interface "Mapping" as MAP
    interface "MutableMapping" as MMAP
}

COLLECTION -[hidden]right- SEQ
SEQ -[hidden]right- MSEQ
MAP -[hidden]right- MMAP

' ===========================
' 第三层：typing 泛型
' ===========================
package "Layer 3: Generic Types" <<Rectangle>> {
    interface "Iterable[T]" as ITER_T
    interface "Collection[T]" as COLLECTION_T
    interface "Sequence[T]" as SEQ_T
    interface "MutableSequence[T]" as MSEQ_T
    interface "Mapping[K,V]" as MAP_T
    interface "MutableMapping[K,V]" as MMAP_T
}

ITER_T -[hidden]right- COLLECTION_T
COLLECTION_T -[hidden]right- SEQ_T
SEQ_T -[hidden]right- MSEQ_T
MAP_T -[hidden]right- MMAP_T

' ===========================
' 第四层：具体类型
' ===========================
package "Layer 4: Concrete Types" <<Rectangle>> {
    interface "List[T]" as LIST_T
    interface "Dict[K,V]" as DICT_T
    interface "Tuple[T,...]" as TUPLE_T
}

LIST_T -[hidden]right- DICT_T
DICT_T -[hidden]right- TUPLE_T

' ===========================
' 继承关系
' ===========================

' 第一层到第二层
ITER --> COLLECTION
SIZED --> COLLECTION
CONTAINER --> COLLECTION

COLLECTION --> SEQ
COLLECTION --> MAP
SEQ --> MSEQ
MAP --> MMAP

' 第二层到第三层
ITER --> ITER_T
COLLECTION --> COLLECTION_T
SEQ --> SEQ_T
MSEQ --> MSEQ_T
MAP --> MAP_T
MMAP --> MMAP_T

' 第三层到第四层
SEQ_T --> LIST_T
MSEQ_T --> LIST_T
SEQ_T --> TUPLE_T
MAP_T --> DICT_T
MMAP_T --> DICT_T

@enduml
```

## dataclasses

**一、`dataclasses` 简介**

`dataclasses` 是 Python 3.7 引入的一个标准库模块（3.6 可以用 backport 包 `dataclasses` 安装），
它的主要目的是简化“**数据容器类**”的定义，减少样板代码（boilerplate），尤其是 `__init__`、`__repr__`、`__eq__` 等方法的重复编写。

传统写法：

```python
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
```

使用 `@dataclass`：

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```

**自动生成** `__init__`、`__repr__`、`__eq__` 等方法，减少手写代码。

**二、核心功能**

| 功能               | 描述                                                                    |
| ------------------ | ----------------------------------------------------------------------- |
| **自动生成方法**   | `__init__`、`__repr__`、`__eq__`、`__hash__`、`__lt__` 等               |
| **类型标注支持**   | 用类型注解定义字段（推荐，但不是强制）                                  |
| **可配置字段行为** | 通过 `field()` 控制字段的默认值、是否参与比较、是否出现在 `__repr__` 等 |
| **不可变对象**     | 通过 `frozen=True` 创建不可变数据类                                     |
| **排序支持**       | 通过 `order=True` 生成比较运算符                                        |
| **辅助函数**       | `asdict()`、`astuple()`、`replace()`、`fields()` 等                     |

**三、装饰器 `@dataclass` 常用参数**

```python
@dataclass(init=True, repr=True, eq=True, order=False, frozen=False)
class MyClass:
    ...
```

| 参数            | 默认值  | 含义                                                  |
| --------------- | ------- | ----------------------------------------------------- |
| `init`          | `True`  | 自动生成 `__init__` 方法                              |
| `repr`          | `True`  | 自动生成 `__repr__` 方法(可读的字符串，主要用于调试)  |
| `eq`            | `True`  | 自动生成 `__eq__` 方法                                |
| `order`         | `False` | 自动生成排序比较方法（需要 `eq=True`）                |
| `frozen`        | `False` | 生成不可变对象（字段赋值会报错）                      |
| `unsafe_hash`   | `False` | 自动生成 `__hash__`，即使 `eq=True` 且 `frozen=False` |
| `slots` (3.10+) | `False` | 使用 `__slots__` 节省内存                             |

注意事项：

- `@dataclass` 里的字段必须有类型注解（除非你用 `field()` 明确声明）。
- 如果字段有**可变默认值**（`list`, `dict` 等），一定要用 `field(default_factory=...)`，否则会出现共享引用的坑。

**四、`field()` 的作用**

`field()` 用于为单个字段设置细粒度控制。

常用参数：

```python
from dataclasses import field

@dataclass
class Person:
    name: str
    age: int = 18
    id: int = field(default_factory=lambda: random.randint(1000, 9999))
    temp_data: list = field(default_factory=list, repr=False, compare=False)  # 每个对象独立的列表
```

| 参数              | 作用                               |
| ----------------- | ---------------------------------- |
| `default`         | 字段默认值                         |
| `default_factory` | 默认值工厂（避免可变默认值陷阱）   |
| `init`            | 是否出现在 `__init__` 参数中       |
| `repr`            | 是否出现在 `__repr__` 输出中       |
| `compare`         | 是否参与比较运算（`__eq__`、排序） |
| `metadata`        | 存放自定义元数据字典               |

注意事项：

- 如果字段是可变类型（`list`, `dict`, `set`），**不要用 `default=[]`**，要用 `default_factory=list`，否则多个实例会共享一个列表。

**五、常用辅助函数**

```python
from dataclasses import asdict, astuple, replace, fields, is_dataclass

p = Person(name="Alice")

asdict(p)       # {'name': 'Alice', 'age': 18, 'id': 1234, 'temp_data': []}
astuple(p)      # ('Alice', 18, 1234, [])
replace(p, age=20)  # 创建一个新对象，修改部分字段
fields(p)       # 获取字段元信息
is_dataclass(p) # True
```

| 函数                                | 用途                               |
| ----------------------------------- | ---------------------------------- |
| `asdict(obj)`                       | 递归转 `dict`                      |
| `astuple(obj)`                      | 转 `tuple`                         |
| `replace(obj, **kwargs)`            | 创建修改版对象                     |
| `fields(obj)`                       | 获取字段元信息（`Field` 对象列表） |
| `is_dataclass(obj)`                 | 检查是否为数据类                   |
| `make_dataclass(name, fields, ...)` | 动态创建数据类                     |

**六、`__post_init__()` 生命周期钩子**

`__post_init__()` 会在自动生成的 `__init__` 执行后调用，可用于**二次初始化**或验证字段。

```python
@dataclass
class User:
    name: str
    age: int

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("年龄不能为负数")
```

**七、典型应用场景**

- 配置对象（如解析 YAML/JSON 配置后映射成类）
- 简单数据结构（点、向量、树节点）
- 数据传输对象（DTO）
- 单元测试数据模型
- 与 `from_dict()` / `to_dict()` 配合，进行序列化和反序列化

**八、总结**

| 方法 / 装饰器      | 作用                                                                     | 常见参数                                                                                                                                 | 使用示例                                                           | 使用场景                                 |
| ------------------ | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------- |
| `@dataclass`       | 将一个普通类转为数据类，自动生成 `__init__`、`__repr__`、`__eq__` 等方法 | `init=True` / `False`（是否生成 `__init__`） `repr=True`（是否生成 `__repr__`） `frozen=True`（不可变对象） `order=True`（生成比较方法） | `@dataclass(frozen=True, order=True) class Point: x: int; y: int ` | 定义只存储数据、不需要手写方法的类       |
| `field()`          | 为某个字段自定义默认值、默认工厂、是否出现在 `__init__` 等               | `default=...`（默认值） `default_factory=...`（工厂函数） `init=False`（不在构造函数出现） `repr=False`（不显示在 `repr`）               | `scores: list = field(default_factory=list) `                      | 列表、字典等可变类型默认值；控制字段行为 |
| `asdict()`         | 将数据类实例转为 `dict`（递归转换）                                      | /                                                                                                                                        | `asdict(obj) `                                                     | 序列化到 JSON、日志输出                  |
| `astuple()`        | 将数据类实例转为元组                                                     | /                                                                                                                                        | `astuple(obj) `                                                    | 快速打包成元组，便于比较                 |
| `replace()`        | 创建对象副本，并修改部分字段                                             | /                                                                                                                                        | `new_obj = replace(obj, x=10) `                                    | 不可变对象的更新                         |
| `fields()`         | 获取数据类字段的元数据                                                   | /                                                                                                                                        | `for f in fields(Point): print(f.name, f.type) `                   | 反射、动态生成表单                       |
| `is_dataclass()`   | 判断对象或类是否为数据类                                                 | /                                                                                                                                        | `is_dataclass(Point) `                                             | 类型检查                                 |
| `make_dataclass()` | 动态创建数据类                                                           | /                                                                                                                                        | `Point = make_dataclass("Point", [("x", int), ("y", int)]) `       | 动态生成类结构                           |
| `__post_init__()`  | 构造完成后自动调用，用于额外初始化                                       | /                                                                                                                                        | `def __post_init__(self): self.z = self.x + self.y `               | 复杂初始化逻辑                           |

使用建议

- **可变类型**（list/dict/set）要用 `field(default_factory=...)`，避免共享引用。
- 需要 JSON 序列化时，可以配合 `asdict()`。
- 如果需要不可变数据类（比如键值缓存），使用 `@dataclass(frozen=True)`。
- `replace()` 非常适合更新不可变对象。
- `__post_init__()` 在需要额外验证或计算派生字段时很好用。

```plantuml
@startuml
title dataclasses 常用 API 关系图

package "dataclasses 核心" {
    class "@dataclass" as DC {
        + 自动生成 __init__, __repr__, __eq__
        + 支持 frozen, order, init, repr 等参数
    }
    class "field()" as FIELD {
        + default
        + default_factory
        + init
        + repr
    }
}

package "实例操作" {
    class "asdict()" as ASDICT {
        + 实例 → dict (递归)
    }
    class "astuple()" as ASTUPLE {
        + 实例 → tuple
    }
    class "replace()" as REPLACE {
        + 创建副本并修改部分字段
    }
}

package "类/反射工具" {
    class "fields()" as FIELDS {
        + 获取字段元数据
    }
    class "is_dataclass()" as ISDC {
        + 判断是否为数据类
    }
    class "make_dataclass()" as MKDC {
        + 动态创建数据类
    }
}

package "特殊方法" {
    class "__post_init__()" as POST {
        + 构造后自动执行
        + 可进行额外初始化
    }
}

DC --> FIELD : 定义字段
DC --> POST : 构造后调用
DC --> ASDICT : 实例转换
DC --> ASTUPLE : 实例转换
DC --> REPLACE : 实例复制更新

ISDC --> DC : 类型检查
FIELDS --> DC : 获取元信息
MKDC --> DC : 动态生成

ASDICT ..> FIELDS : 递归获取字段
ASTUPLE ..> FIELDS : 按字段顺序生成元组

@enduml
```

## pprint 库

`pprint` 是 Python 标准库里的 **Pretty Print** 工具，专门用于 **美观、易读地打印复杂数据结构**。它在调试和日志记录时尤其常用。

**一、`pprint` 基础用法**

```python
import pprint

data = {
    "user": "alice",
    "roles": ["admin", "editor", "viewer"],
    "config": {
        "theme": "dark",
        "notifications": {"email": True, "sms": False}
    }
}

pprint.pprint(data)
```

输出效果比普通 `print(data)` 更清晰：

```python
{'config': {'notifications': {'email': True, 'sms': False}, 'theme': 'dark'},
 'roles': ['admin', 'editor', 'viewer'],
 'user': 'alice'}
```

相比 `print()`，`pprint` 会：

- 自动缩进和换行
- 控制行宽（避免一行太长）
- 保持键排序一致（默认按字典 key 排序）
- 让嵌套结构更容易读

**二、常用 API**

1. **`pprint.pprint(object, stream=None, indent=1, width=80, depth=None, compact=False, sort_dicts=True)`**
   - `object`：要打印的对象
   - `stream`：输出目标（默认是 `sys.stdout`）
   - `indent`：缩进级别（默认 1）
   - `width`：行宽（默认 80 字符，超过会换行）
   - `depth`：限制打印深度，超过层级会用 `...` 代替
   - `compact`：是否尽量紧凑打印列表/元组
   - `sort_dicts`：是否对字典 key 排序（Python 3.8+ 默认 True）

   ```python
   pprint.pprint(data, indent=4, width=60, depth=2, compact=True)
   ```

2. **`pprint.pformat(object, ...)`**
   - 和 `pprint()` 类似，但返回的是 **字符串**，而不是直接打印。
   - 适合写入日志或文件。

   ```python
   s = pprint.pformat(data, indent=2)
   print("Formatted data:\n", s)
   ```

3. **`pprint.isreadable(object)`**
   - 判断对象是否能被 `eval(repr(obj))` 正确还原。

4. **`pprint.isrecursive(object)`**
   - 判断对象是否包含自引用（比如一个 list 包含自己）。

**三、典型使用场景**

1. **调试复杂数据结构**
   - 打印嵌套的字典、列表、JSON 数据时，让输出更清晰。

   ```python
   import json
   data = json.loads('{"a":1,"b":{"x":[1,2,3],"y":true}}')
   pprint.pprint(data)
   ```

2. **日志记录**
   - 在日志中输出结构化数据时，用 `pprint.pformat` 生成更可读的字符串。

   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   logging.info("Args: %s", pprint.pformat(vars(args)))
   ```

3. **配置文件或参数展示**
   - 在程序启动时，把命令行参数或配置项以漂亮的方式打印出来，便于检查。

   ```python
   args_dict = vars(args)
   print("Current configuration:")
   pprint.pprint(args_dict)
   ```

4. **交互式调试（REPL、Jupyter Notebook）**
   - 直接 `pprint` 大数据结构，避免一行滚屏。

5. **输出可控层级**
   - 数据很深时，可以限制 `depth` 只看一部分，避免信息爆炸。

   ```python
   pprint.pprint(data, depth=1)
   ```

**四、和 `json.dumps(..., indent=4)` 的区别**

- `pprint` 更通用（适用于任意 Python 对象，比如类实例、集合等）。
- `json.dumps` 只能处理 JSON 兼容对象（字典、列表、字符串、数值、布尔、None）。
- `pprint` 打印的是 **合法 Python 表达式**，而不是 JSON。

**总结**：
`pprint` 的典型使用场景是 **调试、日志记录、参数打印、复杂数据可视化**。核心 API 是 `pprint()`（直接打印）和 `pformat()`（返回字符串）。

## vars()、locals()、globals()

vars()、locals()、globals() 都是 Python 里很“轻量级”的内置函数。

**一、基本定义**

| 函数          | 作用                                             | 返回值                | 典型用途                     |
| ------------- | ------------------------------------------------ | --------------------- | ---------------------------- |
| `vars([obj])` | 返回对象的 `__dict__`（无参时等价于 `locals()`） | 字典（属性/局部变量） | 对象转字典、调试、`argparse` |
| `locals()`    | 返回当前作用域的**局部变量字典**（只读快照）     | 字典                  | 调试/查看函数内部变量        |
| `globals()`   | 返回**当前模块的全局变量字典**                   | 字典                  | 运行时修改/访问全局变量      |

**二、对比示例**

1. `globals()`

   ```python
   x = 1

   def foo():
       print(globals().keys())  # 全局变量表

   foo()
   ```

   可能输出：

   ```python
   dict_keys(['__name__', '__doc__', '__package__', ..., 'x', 'foo'])
   ```

2. `locals()`

   ```python
   def foo(a, b):
       c = a + b
       print(locals())

   foo(2, 3)
   ```

   输出：

   ```python
   {'a': 2, 'b': 3, 'c': 5}
   ```

   > :warning: 注意：在函数中，`locals()` 返回的是局部变量的字典快照。**直接修改 locals() 不一定会反映到实际局部变量上**。

   结论（记忆规则）：
   - **全局作用域下**：`locals()` 可写（等价于 `globals()`），修改一定生效。
   - **函数局部作用域下**：`locals()` 是 **只读快照**，修改不保证生效；只有在 `exec` 这样的场景下，解释器可能会同步。
   - **对象上用 `vars(obj)`**：直接操作 `obj.__dict__`，修改一定生效。

3. `vars()`
   - **无参时 = `locals()`**

   ```python
   a = 10
   print(vars())   # 和 locals() 一样
   ```

   - **有对象参数时 → 对象的 `__dict__`**

   ```python
   class Person:
       def __init__(self, name):
           self.name = name

   p = Person("Alice")
   print(vars(p))   # {'name': 'Alice'}
   ```

   > :warning: 注意：
   >
   > 1. **仅适用于具有`__dict__`属性的对象**：`vars()`函数仅适用于那些有`__dict__`属性的对象（通常是用户定义的对象）。对于内置对象（如整数、字符串等），调用`vars()`会引发`TypeError`。
   > 2. **只包含实例变量**：返回的字典**只包含对象的实例变量**，不包括类变量或方法。
   > 3. **动态属性**：如果对象在**运行时动态添加了新的属性**，这些属性也会包含在`vars()`返回的字典中。

**三、修改行为对比**

```python
x = 1
globals()['x'] = 100
print(x)   # 100 ✅ 修改生效
def foo():
    y = 10
    locals()['y'] = 20
    print(y)  # 10 ⚠️ 修改不一定生效
foo()
class Config:
    def __init__(self):
        self.lr = 0.1

cfg = Config()
vars(cfg)['lr'] = 0.01
print(cfg.lr)   # 0.01 ✅ 修改生效
```

**四、总结区别**

速查表：`locals()` / `globals()` / `vars()`

| 函数/作用域          | **全局作用域**                                    | **函数局部作用域**                                                                 | **类作用域**                                  | **对象实例**                         |
| -------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------ |
| **globals()**        | ✅ 返回全局符号表，修改一定生效                   | ✅ 依然指向模块的全局符号表，修改一定生效                                          | ✅ 依然指向模块的全局符号表，修改一定生效     | ❌ 不适用                            |
| **locals()**         | ✅ 返回全局符号表（等价于 `globals()`），修改生效 | ⚠️ 返回局部符号表副本，**通常不可写**（修改不保证生效） 仅 `exec()` 等情况可能同步 | ⚠️ 返回类定义体执行时的局部符号表，不保证可写 | ❌ 不适用                            |
| **vars()**（无参数） | ✅ 等价于 `locals()`，可写可生效                  | ⚠️ 等价于 `locals()`，修改不保证生效                                               | ⚠️ 等价于 `locals()`，修改不保证生效          | ❌ 不适用                            |
| **vars(obj)**        | ❌ 不适用                                         | ❌ 不适用                                                                          | ❌ 不适用                                     | ✅ 返回 `obj.__dict__`，修改一定生效 |

**关键总结：**

1. **全局作用域**
   - `locals() == globals()`，修改生效。
   - `globals()` 修改全局变量字典，生效。
   - `vars()` 等价于 `locals()`。
2. **函数局部作用域**
   - `locals()` 返回的是一个 **快照**，修改通常不生效。
   - 特例：`exec()`/`eval()` 可能会修改真实局部变量表。
   - `globals()` 始终指向模块级字典，不受影响。
3. **类作用域**
   - `locals()` 只在类体执行时使用，修改也不保证生效。
4. **对象实例**
   - `vars(obj)` 是访问 `obj.__dict__` 的推荐方式，修改一定生效。

**典型应用：**

- `globals()`：动态导入模块、运行时修改全局变量。
- `locals()`：调试时查看函数内部状态。
- `vars()`：对象转字典（配置保存、日志打印），是调试/序列化最常用的。

**globals() / locals() / vars() 的作用范围关系图:**

```plantuml
@startuml
title Python 中 globals() / locals() / vars() 作用范围关系图

package "Python 运行环境" {

  frame "全局作用域 (module)" {
    class globals {
      +返回全局变量字典
      +可修改并影响实际全局变量
    }
  }

  frame "局部作用域 (function)" {
    class locals {
      +返回局部变量字典
      +只读快照 (修改不保证生效)
    }
  }

  frame "对象作用域 (object)" {
    class vars {
      +无参时 = locals()
      +有对象参数时返回 __dict__
      +可修改并影响对象属性
    }
  }
}

' 关系连线
globals --> "全局变量" : 操作
locals --> "局部变量" : 操作
vars --> "对象.__dict__" : 操作

note right of vars
无参数：等价 locals()
有参数：返回对象.__dict__
end note

@enduml
```

## 是否包含中文字符及标点

`[\u4e00-\u9fff]` 是中日韩统一汉字的主要范围。
中文标点不在，需要扩展范围：

```python
import re

def has_chinese_or_punc(s: str) -> bool:
    pattern = r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]'
    return re.search(pattern, s) is not None

str=""""
"。，你好！"
"""
print(has_chinese_or_punc(str))
print(has_chinese_or_punc("hello"))        # False
```

## Matplotlib 库

链接：

- [fantastic-matplotlib](https://datawhalechina.github.io/fantastic-matplotlib/)
- [教程— Matplotlib 3.10.3 文档](https://matplotlib.org.cn/stable/tutorials/index)
