[toc]

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

```log
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

```log
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

```python
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

```python
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

```log
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

```log
{'name': 'Alice', 'age': 30, 'city': 'Wonderland', 'job': 'Engineer', 'hobby': 'Reading'}
```

使用`vars()`函数将对象转换为字典后，我们可以将其与模板字符串结合使用，方便地进行字符串格式化。例如，结合前面提到的`string.Template` 和 Jinja2 模板引擎。

