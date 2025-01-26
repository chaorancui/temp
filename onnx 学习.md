# onnx 学习

参考链接：

1. [ONNX 学习笔记](https://zhuanlan.zhihu.com/p/346511883)
2. [Google 开源协议 Protobuf 的简介及其序列化原理](https://blog.csdn.net/chengzi_comm/article/details/53199278)

## 什么是 ONNX

简单描述一下官方介绍，开放神经网络交换（Open Neural Network Exchange）简称 ONNX 是微软和 Facebook 提出用来表示深度学习模型的开放格式。所谓开放就是 ONNX 定义了一组和环境，平台均无关的标准格式，来增强各种 AI 模型的可交互性。

换句话说，无论你使用何种训练框架训练模型（比如 TensorFlow/Pytorch/OneFlow/Paddle），在训练完毕后你都可以将这些框架的模型统一转换为 ONNX 这种统一的格式进行存储。注意 ONNX 文件不仅仅存储了神经网络模型的权重，同时也存储了模型的结构信息以及网络中每一层的输入输出和一些其它的辅助信息。我们直接从 onnx 的官方模型仓库拉一个 yolov3-tiny 的 onnx 模型（地址为：<https://github.com/onnx/models/tree/master/vision/object_detection_segmentation/tiny-yolov3/model>）用 Netron 可视化一下看看 ONNX 模型长什么样子。

![yolov3-tiny onnx的可视化结果](https://picx.zhimg.com/v2-d21635b818ed67dfdb4c834324fa1555_1440w.jpg)

但在实际使用 ONNX 的过程中，大多数人对 ONNX 了解得并不多，仅仅认为它只是一个完成模型转换和部署工具人而已，我们可以利用它完成模型转换和部署。正是因为对 ONNX 的不了解，在模型转换过程中出现的各种不兼容或者不支持让很多人浪费了大量时间。

## ProtoBuf 简介

ONNX 作为一个文件格式，我们自然需要一定的规则去读取我们想要的信息或者是写入我们需要保存信息。**ONNX 使用的是 Protobuf 这个序列化数据结构去存储神经网络的权重信息**。熟悉 Caffe 或者 Caffe2 的同学应该知道，它们的模型存储数据结构协议也是 Protobuf。

Protobuf 是一种轻便高效的结构化数据存储格式，可以用于结构化数据串行化，或者说序列化。**它很适合做数据存储或数据交换格式。可用于通讯协议、数据存储等领域的语言无关、平台无关、可扩展的序列化结构数据格式**。目前提供了 C++、Java、Python 三种语言的 API（摘自官方介绍）。

Protobuf 协议是一个以 `*.proto` 后缀文件为基础的，这个文件描述了用户自定义的数据结构。如果需要了解更多细节请参考链接 2，这里只是想表达 ONNX 是基于 Protobuf 来做数据存储和传输，那么自然 onnx.proto 就是 ONNX 格式文件了，接下来我们就分析一下 ONNX 格式。

## ONNX 格式分析

这一节我们来分析一下 ONNX 的组织格式，上面提到 ONNX 中最核心的部分就是 onnx.proto（<https://github.com/onnx/onnx/blob/master/onnx/onnx.proto>）这个文件了，它定义了 ONNX 这个数据协议的规则和一些其它信息。这个文件里的核心部分是以 message 关键字开头的对象，也是我们需要关心的。我们列一下最核心的几个对象并解释一下它们之间的关系。

- ModelProto
- GraphProto
- NodeProto
- ValueInfoProto
- TensorProto
- AttributeProto

当我们加载了一个 ONNX 之后，我们获得的就是一个 `ModelProto`，它包含了一些版本信息，生产者信息和一个 `GraphProto`。在 `GraphProto` 里面又包含了四个 `repeated` 数组，它们分别是：

- **node (NodeProto 类型)**：存放了模型中所有的计算节点
- **input (ValueInfoProto 类型)**：存放了模型的输入节点
- **output(ValueInfoProto 类型)**：存放了模型中所有的输出节点
- **initializer(TensorProto 类型)**：存放了模型的所有权重参数。

**Q**：我们知道要完整的表达一个神经网络，不仅仅要知道网络的各个节点信息，还要知道它们的拓扑关系。这个拓扑关系在 ONNX 中是如何表示的呢？
**A**：ONNX 的每个计算节点都会有 input 和 output 两个数组，这两个数组是 string 类型，通过 input 和 output 的指向关系，我们就可以利用上述信息快速构建出一个深度学习模型的拓扑图。这里要注意一下，GraphProto 中的 input 数组不仅包含我们一般理解中的图片输入的那个节点，还包含了模型中所有的权重。例如，Conv 层里面的 W 权重实体是保存在 initializer 中的，那么相应的会有一个同名的输入在 input 中，其背后的逻辑应该是把权重也看成模型的输入，并通过 initializer 中的权重实体来对这个输入做初始化，即一个赋值的过程。

最后，每个计算节点中还包含了一个 AttributeProto 数组，用来描述该节点的属性，比如 Conv 节点或者说卷积层的属性包含 group，pad，strides 等等，每一个计算节点的属性，输入输出信息都详细记录在 <https://github.com/onnx/onnx/blob/master/docs/Operators.md>。

## ONNX 的基本操作

`onnx` 库提供了一些常用的函数来操作和处理 ONNX 模型。下面是一些常用的函数，以及如何对图（`Graph`）和节点（`Node`）进行操作的常见方法。

### 常用函数

#### 加载和保存模型

- **`onnx.load()`**：加载 ONNX 模型。
- **`onnx.save()`**：保存修改后的 ONNX 模型。

```python
import onnx

# 加载模型
model = onnx.load('model.onnx')

# 保存模型
onnx.save(model, 'saved_model.onnx')
```

#### 验证模型

- **`onnx.checker.check_model()`**：验证模型的合法性。

```python
# 验证模型
onnx.checker.check_model(model)
```

#### 打印图的信息

- **`onnx.helper.printable_graph()`**：打印图的详细信息。

```python
# 打印图的信息
print(onnx.helper.printable_graph(model.graph))
```

### 图操作（Graph）常用函数

`Graph` 是 ONNX 模型的核心部分，包含了节点、输入、输出和常量张量等信息。

#### 获取图的基本信息

- **`model.graph.node`**：获取图中的所有节点。
- **`model.graph.input`**：获取图的输入节点。
- **`model.graph.output`**：获取图的输出节点。
- **`model.graph.initializer`**：获取图中的常量张量（initializer）。
- **`model.graph.value_info`**：存储的是图中间层的张量信息（即那些不是输入或输出的张量）。

```python
# 获取图中的所有节点
nodes = model.graph.node

# 获取图的输入和输出
inputs = model.graph.input
outputs = model.graph.output

# 获取图的常量张量（initializer）
initializers = model.graph.initializer
```

#### 查找特定节点

- 查找特定类型的节点（例如查找所有 `Gemm` 节点）：

```python
# 查找特定类型的节点
op_type = 'Gemm'
matching_nodes = [node for node in model.graph.node if node.op_type == op_type]
```

#### 修改图中的节点

通过修改图中的节点属性，可以更新模型。

```python
# 修改所有 Gemm 节点的 alpha 属性
for node in model.graph.node:
    if node.op_type == 'Gemm':
        for attr in node.attribute:
            if attr.name == 'alpha':
                attr.f = 1.5  # 修改 alpha 属性
```

### 节点操作（Node）常用函数

每个节点是 `onnx.NodeProto` 对象，包含了操作类型（`op_type`）、输入、输出和属性等信息。

#### 获取节点的输入和输出

- **`node.input`**：获取节点的输入。
- **`node.output`**：获取节点的输出。

```python
# 获取节点的输入和输出
for node in model.graph.node:
    print(f"Node {node.name} inputs: {node.input}")
    print(f"Node {node.name} outputs: {node.output}")
```

#### 获取和修改节点的属性

- **`node.attribute`**：获取节点的属性列表，可以通过修改属性来调整节点的行为。

```python
# 获取节点的属性
for node in model.graph.node:
    if node.op_type == 'Gemm':
        for attr in node.attribute:
            print(f"Attribute {attr.name} value: {attr}")

# 修改节点的属性（例如修改 alpha）
for node in model.graph.node:
    if node.op_type == 'Gemm':
        for attr in node.attribute:
            if attr.name == 'alpha':
                attr.f = 2.0  # 修改 alpha 属性值
```

#### 添加新节点

可以向模型中添加新的节点。

```python
from onnx import helper

# 创建一个新的 Add 节点
add_node = helper.make_node(
    'Add',  # 操作类型
    inputs=['input1', 'input2'],  # 输入张量名称
    outputs=['output'],  # 输出张量名称
    name='add_node'  # 节点名称
)

# 将新节点添加到图中
model.graph.node.append(add_node)

# 保存修改后的模型
onnx.save(model, 'modified_model.onnx')
```

#### 删除节点

可以从图中删除特定节点。

```python
# 删除所有 Gemm 节点
model.graph.node[:] = [node for node in model.graph.node if node.op_type != 'Gemm']

# 保存修改后的模型
onnx.save(model, 'modified_model_without_gemm.onnx')
```

#### 获取节点的输入和输出的形状

通过 `graph.value_info` 或 `graph.initializer` 获取节点输入输出的形状。

```python
# 获取每个节点的输入形状
for node in model.graph.node:
    print(f"Node {node.name} inputs:")
    for input_name in node.input:
        for value_info in model.graph.value_info:
            if value_info.name == input_name:
                shape = value_info.type.tensor_type.shape
                shape_values = [dim.dim_value for dim in shape.dim]
                print(f"  - {input_name}: Shape: {shape_values}")
```

### 常用的 `onnx.helper` 函数

`onnx.helper` 提供了方便的工具函数来创建节点、张量等。

#### 创建常量张量（Tensor）

使用 `onnx.helper.make_tensor()` 创建常量张量，并将其添加到模型中。

```python
from onnx import helper, numpy_helper
import numpy as np

# 创建一个常量张量
tensor = helper.make_tensor(
    name='my_tensor',
    data_type=onnx.TensorProto.FLOAT,
    dims=[2, 3],
    vals=np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=np.float32).tobytes()
)

# 将张量添加到模型的 initializer 中
model.graph.initializer.append(tensor)

# 保存修改后的模型
onnx.save(model, 'modified_model_with_initializer.onnx')
```

#### 创建节点（Node）

使用 `onnx.helper.make_node()` 创建节点。

```python
# 创建一个加法节点
add_node = helper.make_node(
    'Add',
    inputs=['input1', 'input2'],
    outputs=['output'],
    name='add_node'
)
```

#### 创建图（Graph）

使用 `onnx.helper.make_graph()` 创建图。

```python
# 创建一个图
graph = helper.make_graph(
    nodes=[add_node],  # 图中的节点
    name='my_graph',  # 图名称
    inputs=[helper.make_tensor_value_info('input1', onnx.TensorProto.FLOAT, [1])],
    outputs=[helper.make_tensor_value_info('output', onnx.TensorProto.FLOAT, [1])]
)

# 创建一个模型
model = helper.make_model(graph)
```

### 总结

| 功能                 | 函数 / 方法                               | 示例                                                                         |
| -------------------- | ----------------------------------------- | ---------------------------------------------------------------------------- |
| **加载模型**         | `onnx.load()`                             | `model = onnx.load('model.onnx')`                                            |
| **保存模型**         | `onnx.save()`                             | `onnx.save(model, 'saved.onnx')`                                             |
| **验证模型**         | `onnx.checker.check_model()`              | `onnx.checker.check_model(model)`                                            |
| **获取节点**         | `model.graph.node`                        | `gemm_nodes = [node for node in model.graph.node if node.op_type == 'Gemm']` |
| **获取输入输出**     | `node.input`, `node.output`               | `inputs = node.input`                                                        |
| **获取和修改属性**   | `node.attribute`                          | `for attr in node.attribute:`                                                |
| **创建节点**         | `onnx.helper.make_node()`                 | `helper.make_node('Add', ...)`                                               |
| **创建常量张量**     | `onnx.helper.make_tensor()`               | `helper.make_tensor(...)`                                                    |
| **获取图的基本信息** | `model.graph.input`, `model.graph.output` | `inputs = model.graph.input`                                                 |
| **获取常量张量**     | `model.graph.initializer`                 | `initializers = model.graph.initializer`                                     |
| **删除节点**         | `model.graph.node[:]`                     | `model.graph.node = ...`                                                     |
| **修改节点属性**     | `node.attribute`                          | `attr.f = ...`                                                               |
| **打印图的信息**     | `onnx.helper.printable_graph()`           | `print(onnx.helper.printable_graph(model.graph))`                            |


