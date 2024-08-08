# C++ 工具

# Doxygen

Doxygen 是一个强大的工具，用于从 C++ 代码中生成文档，并且可以生成类的调用关系图。下面是如何使用 Doxygen 的步骤：

### 1. 安装 Doxygen 和 Graphviz

首先，需要确保你已经安装了 Doxygen 和 Graphviz，因为 Doxygen 依赖 Graphviz 来生成类图。

- 在 Ubuntu 上:

  ```shell
  sudo apt-get install doxygen graphviz
  ```

- 在 macOS 上:

  ```shell
  brew install doxygen graphviz
  ```

- **在 Windows 上**: 可以从 [Doxygen 官方网站](https://www.doxygen.nl/) 和 [Graphviz 官方网站](https://graphviz.org/) 下载并安装。

### 2. 生成 Doxygen 配置文件

Doxygen 通过一个配置文件（通常称为 `Doxyfile`）来控制文档的生成。

```shell
doxygen -g
```

这个命令会在当前目录下生成一个默认的 `Doxyfile`。

### 3. 配置 `Doxyfile`

打开生成的 `Doxyfile` 并根据你的需求进行修改。以下是一些重要的配置选项：

- **PROJECT_NAME**: 设置项目名称。

  ```
  PROJECT_NAME = "Your Project Name"
  ```

- **INPUT**: 设置需要生成文档的源码目录或文件。

  ```
  INPUT = path/to/your/source
  ```

  > 注：oxygen 默认不直接支持使用 `~` 表示用户主目录路径。`~` 是 Unix/Linux shell 中的快捷方式，但在 Doxygen 配置文件中，它不会自动扩展为实际的路径。需要手动替换 `~` 为完整路径，或者使用环境变量。

- **OUTPUT_DIRCTORY**: 设置需要生成文档的保存目录。

  ```
  OUTPUT_DIRECTORY = path/to/your/out
  ```

- **RECURSIVE**: 如果要递归处理子目录，设置为 `YES`。

  ```
  RECURSIVE = YES
  ```

- **EXTRACT_ALL**: 如果你希望提取所有的注释，包括没有文档的符号，设置为 `YES`。

  ```
  EXTRACT_ALL = YES
  ```

- **GENERATE_LATEX** 和 **GENERATE_HTML**: 设置为 `YES`，以生成 PDF 或 HTML 文档。

  ```
  GENERATE_HTML = YES
  GENERATE_LATEX = YES
  ```

- **HAVE_DOT**: 设置为 `YES` 以生成类图。

  ```
  HAVE_DOT = YES
  ```

- **CALL_GRAPH 和 CALLER_GRAPH**: 设置为 `YES` 以生成调用图和调用者图。

  ```
  CALL_GRAPH = YES
  CALLER_GRAPH = YES
  ```

### 4. 生成文档

配置完成后，可以使用以下命令生成文档：

```shell
doxygen Doxyfile
```

这个命令会在指定的输出目录中生成 HTML 和/或 LaTeX 文档。类之间的调用关系图会自动包含在生成的 HTML 文档中。

### 5. 查看生成的文档

打开生成的 HTML 文件（通常在 `html/index.html`）以查看项目的文档和类的调用关系图。

### 6. 使用 Graphviz 生成图

如果你想单独生成类图，可以使用 Graphviz 将 Doxygen 生成的 `.dot` 文件转换为图形格式。例如：

```shell
dot -Tpng class_diagram.dot -o class_diagram.png
```

这样可以得到项目中类之间调用关系的图示。



# 名称解修饰

在C++中，函数名在编译过程中通常会被修改为一种称为“名称修饰”（name mangling）的形式，以便支持函数重载和其他语言特性。名称修饰后的符号（函数名）在编译后的二进制文件中可能看起来像一串杂乱无章的字符。为了反编译这些名称修饰后的符号并恢复成原来的函数名，可以使用一种叫做“名称解修饰”（name demangling）的过程。

常见的名称解修饰工具包括：

### 1. **`c++filt` 工具**

`c++filt` 是一个常用的工具，用于将名称修饰后的符号恢复为人类可读的C++函数名。

- 使用方式：

  - 在命令行中，你可以通过输入 `c++filt` 并跟上修饰后的名称来解修饰函数名。

  - **示例**：

    ```shell
    echo _Z3foo3int | c++filt
    foo(int)
    ```

    这里 `_Z3foo3int` 是一个经过修饰的函数名，通过 `c++filt` 解修饰后，得到 `foo(int)`，表示这是一个接受 `int` 参数的 `foo` 函数。

### 2. **`nm` 命令**

- `nm` 是一个用于列出二进制文件（如 `.o`、`.a`、`.so`、可执行文件）中符号表的工具，通常与 `c++filt` 配合使用。

- 使用方式：

  - 先用 `nm` 列出符号，然后通过管道将结果传给 `c++filt` 进行解修饰。

  - **示例**：

    ```shell
    nm myfile.o | c++filt
    ```

    这条命令会列出 `myfile.o` 中的所有符号，并解修饰所有名称修饰的符号。

### 3. **编译器支持的解修饰功能**

一些C++编译器（如GCC、Clang、MSVC）提供了内置的工具或选项来直接在调试信息中显示解修饰后的符号。调试器如 `gdb` 也可以自动解修饰符号。

### 4. **手动解修饰**

如果你有修饰规则的具体细节，也可以通过手动解修饰。然而，C++的名称修饰规则非常复杂，通常手动解修饰不是实际的选择。

### 名称修饰的规则

不同的编译器可能使用不同的名称修饰规则。比如，GCC、Clang 和 MSVC 的名称修饰规则就不尽相同。如果你需要手动处理名称修饰的符号，了解编译器的具体规则是必须的。

### 反编译和调试

名称解修饰有时被误解为反编译。需要注意的是，反编译通常指将编译后的二进制代码还原为源代码级别的表示，这比单纯的名称解修饰复杂得多，且不一定能恢复原始的C++代码。解修饰仅是将编译后的符号恢复成原始的函数名，而不涉及恢复完整的源代码。

### 小结

`c++filt` 工具或类似的工具可以用来解修饰经过C++编译器处理的符号（函数名等），将其转换回可读的C++函数名。这在调试和分析编译后的二进制文件时非常有用，但它并不是一个反编译器，而是一个解修饰工具。