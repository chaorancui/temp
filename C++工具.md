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

  ```ini
  PROJECT_NAME = "Your Project Name"
  ```

- **INPUT**: 设置需要生成文档的源码目录或文件。

  ```ini
  INPUT = path/to/your/source
  ```

  > 注：oxygen 默认不直接支持使用 `~` 表示用户主目录路径。`~` 是 Unix/Linux shell 中的快捷方式，但在 Doxygen 配置文件中，它不会自动扩展为实际的路径。需要手动替换 `~` 为完整路径，或者使用环境变量。

- **OUTPUT_DIRCTORY**: 设置需要生成文档的保存目录。

  ```ini
  OUTPUT_DIRECTORY = path/to/your/out
  ```

- **RECURSIVE**: 如果要递归处理子目录，设置为 `YES`。

  ```ini
  RECURSIVE = YES
  ```

- **EXTRACT_ALL**: 如果你希望提取所有的注释，包括没有文档的符号，设置为 `YES`。

  ```ini
  EXTRACT_ALL = YES
  ```

- **GENERATE_LATEX** 和 **GENERATE_HTML**: 设置为 `YES`，以生成 PDF 或 HTML 文档。

  ```ini
  GENERATE_HTML = YES
  GENERATE_LATEX = YES
  ```

- **HAVE_DOT**: 设置为 `YES` 以生成类图。

  ```ini
  HAVE_DOT = YES
  ```

- **CALL_GRAPH 和 CALLER_GRAPH**: 设置为 `YES` 以生成调用图和调用者图。

  ```ini
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

> 参考：
> [1]. [绘制函数调用图（call graph）：doxygen + graphviz](https://www.cnblogs.com/lidabo/p/15855564.html)

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

# 命令行参数解析库

`gflags` 是一个用于**解析命令行参数的库**，最初由 Google 开发，支持 C++ 和 Python。它允许开发者轻松定义命令行标志（flags），并提供了一种灵活、结构化的方式来解析和使用这些命令行参数。

### `gflags` 的主要功能和特点

1. **命令行标志定义**： `gflags` 允许开发者为程序定义多种类型的命令行标志，包括布尔类型、整型、浮点型和字符串类型。这些标志可以通过命令行传递，直接影响程序的行为。
2. **自动解析命令行参数**： `gflags` 可以自动解析程序启动时传递的命令行参数，并将其映射到预定义的标志变量中，供程序使用。
3. **默认值和帮助信息**： 在定义标志时，可以指定明标志的默认值和详细的帮助说。用户可以通过 `--help` 选项查看程序可用的命令行标志及其说明，帮助用户更好地理解程序的参数使用方式。
4. **支持布尔标志的简写形式**： 对于布尔标志，`gflags` 提供了简写形式，例如 `--flag` 可以表示 `--flag=true`，而 `--noflag` 则表示 `--flag=false`。
5. **灵活的标志命名和命名空间**： 标志可以使用任何合理的命名，且通过命名空间划分，可以避免标志命名冲突。此外，`gflags` 允许标志的重定义，以适应不同模块或组件的需求。
6. **自动生成帮助文档**： 当用户使用 `--help` 选项运行程序时，`gflags` 会自动生成并展示所有命令行标志的帮助信息、类型和默认值。

### 安装 `gflags`

- **C++ 版本安装**： 如果你使用的是 Linux 或 macOS，可以通过包管理器安装：

  ```bash
  sudo apt-get install libgflags-dev  # Ubuntu / Debian
  brew install gflags  # macOS
  ```

  你也可以通过源码安装：

  ```bash
  git clone https://github.com/gflags/gflags.git
  cd gflags
  mkdir build && cd build
  cmake ..
  make
  sudo make install
  ```

- **Python 版本安装**： 在 Python 中，可以通过 `pip` 进行安装：

  ```bash  
  pip install gflags
  ```

### 基本使用示例（C++）

#### 1. 定义命令行标志

使用 `gflags`，可以通过宏来定义标志：

- **布尔标志**：`DEFINE_bool`，用于表示是否启用某个功能。
- **整型标志**：`DEFINE_int32` 和 `DEFINE_int64`，用于定义整型参数。
- **浮点型标志**：`DEFINE_double`，用于定义浮点型参数。
- **字符串标志**：`DEFINE_string`，用于定义字符串参数。

#### 示例代码

```cpp
#include <iostream>
#include <gflags/gflags.h>

// 定义命令行标志
DEFINE_bool(verbose, false, "Display verbose output");
DEFINE_int32(port, 8080, "Port to listen on");
DEFINE_string(host, "localhost", "Host to connect to");

int main(int argc, char* argv[]) {
    // 解析命令行参数
    gflags::ParseCommandLineFlags(&argc, &argv, true);

    // 输出解析后的标志值
    std::cout << "Host: " << FLAGS_host << std::endl;
    std::cout << "Port: " << FLAGS_port << std::endl;

    if (FLAGS_verbose) {
        std::cout << "Verbose mode enabled" << std::endl;
    } else {
        std::cout << "Verbose mode disabled" << std::endl;
    }

    // 释放命令行标志解析相关的资源
    gflags::ShutDownCommandLineFlags();
    return 0;
}
```

#### 编译

```bash
g++ -o example example.cpp -lgflags
```

#### 运行程序

```bash
./example --host=127.0.0.1 --port=9000 --verbose
```

输出结果：

```bash
Host: 127.0.0.1
Port: 9000
Verbose mode enabled
```

#### 帮助信息

`gflags` 可以自动生成帮助信息，当用户输入 `--help` 时：

```bash
./example --help
```

输出示例：

```bash
Usage: ./example [--host=string] [--port=int32] [--verbose]
  --host: Host to connect to
    (default: "localhost")
  --port: Port to listen on
    (default: 8080)
  --verbose: Display verbose output
    (default: false)
```

### 常见命令行标志类型

- **布尔标志**：定义布尔值标志，用于开关某些功能。

  ```cpp
  DEFINE_bool(verbose, false, "Enable verbose mode");
  ```

  使用时：

  ```bash
  --verbose
  --noverbose
  ```

- **整型标志**：定义整型标志。

  ```cpp
  DEFINE_int32(port, 8080, "Port number");
  ```

  使用时：

  ```bash
  --port=9000
  ```

- **字符串标志**：定义字符串标志。

  ```cpp
  DEFINE_string(host, "localhost", "Host address");
  ```

  使用时：

  ```bash
  --host=127.0.0.1
  ```

- **浮点型标志**：定义浮点型标志。

  ```cpp
  DEFINE_double(rate, 0.5, "Rate value");
  ```

  使用时：

  ```bash
  --rate=0.8
  ```

### gflags 的优点

- **自动解析命令行参数**：简化了开发者处理命令行参数的工作。
- **自动生成帮助信息**：为用户提供清晰的帮助文档，无需手动编写。
- **灵活的标志定义**：支持多种类型的标志，适合多种应用场景。
- **命名空间隔离**：通过命名空间可以防止命令行标志的冲突。
- **适应性强**：可用于小型脚本工具到大型复杂系统。

### gflags 的应用场景

- **命令行工具**：许多命令行工具需要处理大量的参数和选项，`gflags` 可以帮助定义和解析这些参数。
- **服务程序**：对于服务器或守护进程，`gflags` 可以用来定义端口、日志级别、主机等运行时参数。
- **实验性应用**：在机器学习、数据分析等领域，经常需要快速调整参数，`gflags` 可以为这种需求提供便利。

### 总结

`gflags` 是一个强大且易于使用的命令行参数解析库，适用于需要灵活处理命令行选项的项目。它通过简洁的 API 和自动生成的帮助信息，帮助开发者快速定义、解析和使用命令行标志，使得命令行工具和应用程序的开发变得更加简单高效。
