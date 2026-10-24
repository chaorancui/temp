[TOC]

# python 常用库\_7

## 装饰器实现工厂注册

Python 中的**装饰器实现工厂注册**（Decorator-based Registry Pattern）是一种非常优雅且解耦的设计模式。

它的核心思想是：**“声明即注册”**。
通过在目标类或函数上贴一个装饰器，在其定义被 Python 解释器加载时，自动将其映射关系（如名称 $\to$ 类/函数）存入一个中央注册表（如字典）。
使用时，通过名称直接向工厂请求对应的实例，从而彻底解耦了“类的定义/注册”与“类的实例化/使用”。

**核心工作原理**

1. **注册表（Registry）**：通常是一个全局字典（`dict`），存储字符串标识符与类/函数的映射。
2. **装饰器（Decorator）**：在类或函数被加载时（Import 时或解析定义时）触发执行，将类/函数本身及对应的键名写入注册表，并原样返回该类/函数（不改变其原有逻辑）。
3. **工厂（Factory）**：暴露获取或创建实例的统一接口，根据传入的标识符检索注册表，实例化并返回对应对象。

**典型用法示例**

下面以一个典型的 **“多格式文档导出器（Exporter）”** 为例，演示完整实现。

```python
from typing import Dict, Type, Any


class ExporterRegistry:
    """导出器注册表与工厂"""
    _registry: Dict[str, Type['BaseExporter']] = {}

    @classmethod
    def register(cls, name: str):
        """注册装饰器：支持通过参数指定名称"""
        def decorator(subclass: Type['BaseExporter']):
            if name in cls._registry:
                raise ValueError(f"导出器 '{name}' 已经被注册过！")
            cls._registry[name] = subclass
            return subclass  # 原样返回，不破坏原始类的结构
        return decorator

    @classmethod
    def create(cls, name: str, *args, **kwargs) -> 'BaseExporter':
        """工厂方法：根据名称实例化对象"""
        if name not in cls._registry:
            raise KeyError(f"未找到名为 '{name}' 的导出器，可用导出器: {list(cls._registry.keys())}")
        exporter_cls = cls._registry[name]
        return exporter_cls(*args, **kwargs)


# 1. 定义基类
class BaseExporter:
    def export(self, data: dict) -> str:
        raise NotImplementedError


# 2. 通过装饰器优雅地注册不同实现
@ExporterRegistry.register("json")
class JSONExporter(BaseExporter):
    def export(self, data: dict) -> str:
        import json
        return json.dumps(data)


@ExporterRegistry.register("csv")
class CSVExporter(BaseExporter):
    def export(self, data: dict) -> str:
        items = [f"{k},{v}" for k, v in data.items()]
        return "key,value\n" + "\n".join(items)


@ExporterRegistry.register("xml")
class XMLExporter(BaseExporter):
    def export(self, data: dict) -> str:
        xml_items = "".join([f"<{k}>{v}</{k}>" for k, v in data.items()])
        return f"<root>{xml_items}</root>"


# 3. 使用工厂（调用方无需关心具体类名，也不需要依赖 JSONExporter/CSVExporter）
def main():
    data = {"name": "Alice", "age": 30}

    # 根据配置或用户输入动态生成对象
    fmt = "json"
    exporter = ExporterRegistry.create(fmt)
    print(f"[{fmt.upper()} 导出]:\n{exporter.export(data)}\n")

    fmt = "xml"
    exporter = ExporterRegistry.create(fmt)
    print(f"[{fmt.upper()} 导出]:\n{exporter.export(data)}")


if __name__ == "__main__":
    main()
```

**模式优势与使用场景**

1. 优势
   - **符合开闭原则（OCP）**：增加新功能（如添加 `PDFExporter`）时，只需写一个新的类并加上 `@ExporterRegistry.register("pdf")`，**零修改** 原有的工厂逻辑或 `if/elif` 条件判断。
   - **高内聚解耦**：类的注册声明紧贴类的定义本身，代码可读性好，且客户端代码仅依赖接口与字符串 Token。
   - **避免长 `if-elif-else` 结构**：用字典查表替换条件分支，时间复杂度由 $O(N)$ 降低为 $O(1)$。

2. 经典实际应用场景
   1. **Web 框架中的路由/插件（如 Flask, Pytest）**：
      - Flask 的 `@app.route('/path')` 就是典型的注册装饰器，将 URL 路径与视图函数建立映射。
   2. **深度学习与 AI 框架（如 PyTorch / MMCV / OpenMMLab / Detectron2）**：
      - 在配置文件中声明 `model_name: "ResNet50"`，主程序通过注册表动态构建对应的神经网络 Backbone 或 Loss 函数。
   3. **数据处理与任务调度**：
      - 各种 CLI 工具或 ETL 管道中，根据命令行参数执行不同的 Task / Action。

**注意事项**

- **模块加载问题（Import Side-Effects）**：装饰器代码只有在包含该类的文件被 `import` 解释器执行时才会生效。如果把实现类放在独立文件（如 `plugins/pdf.py`）且未被显式导入，注册表里将找不到该类。常见解决策略是在工厂初始化时批量自动导入目录（如 `pkgutil.walk_packages`）。

**`ExporterRegistry` 里类方法拆解**

1. 注册装饰器：`register(cls, name: str)`

   ```python
   @classmethod
   def register(cls, name: str):
       """注册装饰器：支持通过参数指定名称"""
       def decorator(subclass: Type['BaseExporter']):
           if name in cls._registry:
               raise ValueError(f"导出器 '{name}' 已经被注册过！")
           cls._registry[name] = subclass
           return subclass  # 原样返回，不破坏原始类的结构
       return decorator
   ```

   **为什么有“两层函数嵌套”:**

   因为我们用的是**带参数的装饰器** `@ExporterRegistry.register("json")`。在 Python 中，它的语法等价于两步操作：
   1. **第一步：调用外层函数** `ExporterRegistry.register("json")`，它接收参数 `"json"`，并**返回**内层函数 `decorator`。
   2. **第二步：用返回的内层函数去装饰目标类** `@decorator`。

   **详细拆解执行流程：**

   假设 Python 执行到了这一行代码：

   ```python
   @ExporterRegistry.register("json")
   class JSONExporter(BaseExporter):
       ...
   ```

   1. **进入外层函数 `register(cls, name="json")`**：
      - 这里的 `cls` 指向 `ExporterRegistry` 类本身（因为是 `@classmethod`）。
      - 参数 `name` 接收到了 `"json"`。
      - 外层函数定义了内层函数 `decorator`，并把它**返回**出去。
   2. **进入内层函数 `decorator(subclass)`**：
      - 当 Python 解析完 `JSONExporter` 类的定义后，会自动把 `JSONExporter` 这个**类对象本身**作为参数传给 `subclass`。
      - **查重检查**：看 `"json"` 是不是已经在字典 `cls._registry` 里了，如果在就报错（防止同名覆盖）。
      - **写入字典（核心步骤）**：执行 `cls._registry["json"] = JSONExporter`。此时全局字典里就建立了一对映射：`"json" -> <class JSONExporter>`。
      - **原样返回**：执行 `return subclass`。必须把接收到的类原封不动地返回，这样后续代码才能正常使用 `JSONExporter` 这个类名。

   > **重点理解**：这个注册动作是在 **代码被 import 或加载解析时** 自动完成的，**不需要你手动去调用任何注册函数**。

2. 工厂创建方法：`create(cls, name: str, *args, **kwargs)`

   ```python
   @classmethod
   def create(cls, name: str, *args, **kwargs) -> 'BaseExporter':
       """工厂方法：根据名称实例化对象"""
       if name not in cls._registry:
           raise KeyError(f"未找到名为 '{name}' 的导出器，可用导出器: {list(cls._registry.keys())}")
       exporter_cls = cls._registry[name]
       return exporter_cls(*args, **kwargs)
   ```

   **参数解释：**
   - `cls`：`ExporterRegistry` 类本身。
   - `name`：你想创建的导出器名称，比如 `"json"` 或 `"csv"`。
   - `*args, **kwargs`：可变参数，用于把创建实例时需要的其他初始化参数（比如文件路径、编码格式等）透传给具体的类。

   **详细拆解执行流程：**

   当你在业务代码里调用这一行时：

   ```python
   exporter = ExporterRegistry.create("json")
   ```

   1. **检查合法性**：判断 `"json"` 是否在 `cls._registry` 字典的 key 里面。如果传了个未注册的 `"pdf"`，会立刻抛出明确的 `KeyError` 提示。
   2. **取出类对象**：从字典里拿到对应注册的类：
      - `exporter_cls = cls._registry["json"]`
      - 此时 `exporter_cls` 的值就是 `JSONExporter` 这个类。
   3. **实例化并返回**：
      - `exporter_cls(*args, **kwargs)` 等价于调用了 `JSONExporter(*args, **kwargs)`。
      - 它会创建出一个 `JSONExporter` 的**具体实例**并返回给调用者。

3. 总结对比

| **函数**               | **触发时机**                           | **核心作用**                                   | **字典里的变化**                              |
| ---------------------- | -------------------------------------- | ---------------------------------------------- | --------------------------------------------- |
| **`register("json")`** | Python 加载文件/类定义时（程序刚启动） | 存映射关系：把字符串与类绑定起来               | `_registry` 增加一项 `{"json": JSONExporter}` |
| **`create("json")`**   | 业务代码运行需要使用对象时             | 查表并实例化：根据字符串找到类，并 `()` 实例化 | 不改变字典，只是从字典里**取类**并**实例化**  |

## 模块导出接口

在 Python 文件中，`__all__` 是一个用于定义**模块导出接口**的特殊变量（列表或元组）。

**一、作用与解决的问题**

1. 控制 `from module import *` 的导入行为
   - **问题：** 当外部代码使用 `from my_module import *` 通配符导入时，默认情况下，Python 会导入该模块中**所有不以单下划线 `_` 开头的名称**（包括该模块导入的其他第三方库或辅助变量）。这容易导致**命名空间污染**（Namespace Pollution）或不小心覆盖外部变量。
   - **解决：** 定义 `__all__ = ['SimRouter']` 后，`from my_module import *` **只**会导入 `SimRouter`，忽略其他所有未 listed 在 `__all__` 中的类、函数或变量。

2. 明确定义模块的公共 API（Public API）
   - **问题：** 在一个复杂的 Python 文件中，外部使用者很难快速分辨哪些是内部工具类/辅助函数，哪些是设计给外部调用的核心类。
   - **解决：** `__all__` 显式声明了该模块的公共接口。看到 `__all__ = ['SimRouter']`，其他开发者能瞬间明白：**这个文件对外提供的核心能力就是 `SimRouter`**。

3. 优化文档生成与代码补全
   - 自动文档生成工具（如 Sphinx、pydoc）以及 IDE（如 PyCharm、VS Code）会优先读取 `__all__`，从而在生成 API 文档或提供自动补全提示时更准确。

**二、典型用法**

1. 单文件/模块的显式导出

   假设有一个文件 `router.py`：

   ```python
   # router.py

   # 定义导出列表
   __all__ = ['SimRouter']

   # 导入的第三方库或辅助模块（不希望被 from router import * 导出去）
   import os
   import sys

   # 内部辅助函数（不需要暴露给外部）
   def _helper_func():
       pass

   # 核心公共类
   class SimRouter:
       def __init__(self):
           print("SimRouter initialized")

   # 内部使用的全局变量
   TEMP_CONFIG = {"debug": True}
   ```

   **外部使用方式对比：**

   ```python
   # 使用通配符导入
   from router import *

   r = SimRouter()      #  正常使用
   _helper_func()       #  NameError: name '_helper_func' is not defined
   print(TEMP_CONFIG)   #  NameError: name 'TEMP_CONFIG' is not defined
   print(os)            #  NameError: name 'os' is not defined
   ```

   _(注意：如果是精确导入如 `from router import TEMP_CONFIG`，`__all__` 不会阻止导入，它仅对 `import *` 生效。)_

2. 包的 `__init__.py` 封装与暴露

   在编写 Python 包时，经常会在顶层的 `__init__.py` 中使用 `__all__`，将子模块的核心类暴露到包根路径：

   ```log
   my_package/
   ├── __init__.py
   └── router.py
   ```

   在 `my_package/__init__.py` 中：

   ```python
   from .router import SimRouter

   __all__ = ['SimRouter']
   ```

   这样外部使用者就可以直接干净地导入：

   ```python
   from my_package import SimRouter
   # 或者
   from my_package import * # 只拿到 SimRouter
   ```

3. 总结
   - **作用：** 限制并规范 `import *` 导入的名称，声明模块的公共 API。
   - **解决的问题：** 命名空间污染、内部实现细节泄漏、API 界限模糊。
   - **推荐做法：** 即使团队规范中倡导“不使用 `import *`”，在库/框架的开发中编写 `__all__` 依然是极其良好的 Pythonic 实践。

**三、备注**

1. `__all__` 位置

   `__all__` 放在 `.py` 文件的开头、中间还是结尾，在 Python 语法层面和功能实现上是没有区别的，只要它是一个在**模块作用域（全局）中**被赋值的列表或元组即可。
   但是，在代码规范、最佳实践以及实际执行顺序上，**强烈建议放在文件开头（紧随模块文档字符串和 `import` 语句之后）**。
