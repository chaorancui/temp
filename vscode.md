[toc]

# VSCode

## vscode 软件

### 安装版

- 安装过程可以添加右键菜单
- 插件安装目录默认，需要额外修改

### 便携版

- 插件安装位置在便携解压目录
- 需要自己添加右键菜单

官方文档在 Portable Mode 部分已经说明了，你只需要在解压后的 VSCode 目录里新建一个名为 data 的文件夹，那么以后所有的数据文件（包括用户配置、插件等）都会安装到这个 data 文件夹里。

以前网上流传的加启动选项--extensions-dir [path] 的方法，在部分情景下有不少缺点，这里提到的方法应该是最完美的，百闻不如一试，赶快动手吧~

最后，附上一段把 VSCode 添加到右键菜单的[bat 代码](https://www.zhihu.com/search?q=bat代码&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1139906712})，保存到一个.bat 文件里并放到 VSCode 目录中，双击运行：

```bat
@ECHO OFF
PUSHD %~DP0
TITLE VSCode
Md "%WinDir%\System32\test_permissions" 2>NUL||(Echo 请使用右键管理员身份运行&&Pause >NUL&&Exit)
Rd "%WinDir%\System32\test_permissions" 2>NUL
SetLocal EnableDelayedExpansion
SET /P ST=输入a添加右键菜单，输入d删除右键菜单：
if /I "%ST%"=="a" goto Add
if /I "%ST%"=="d" goto Remove
:Add
reg add "HKEY_CLASSES_ROOT\*\shell\VSCode"         /t REG_SZ /v "" /d "&VSCode"   /f
reg add "HKEY_CLASSES_ROOT\*\shell\VSCode"         /t REG_EXPAND_SZ /v "Icon" /d "%~dp0Code.exe" /f
reg add "HKEY_CLASSES_ROOT\*\shell\VSCode\command" /t REG_SZ /v "" /d "%~dp0Code.exe \"%%1\"" /f

exit
:Remove
reg delete "HKEY_CLASSES_ROOT\*\shell\VSCode" /f
exit
```

## vscode-server

当你使用 Visual Studio Code (VS Code) 的 Remote-SSH 扩展连接到远程服务器时，VS Code 会自动在远程服务器上安装一个名为 "VS Code Server" 的组件，以便在远程环境中运行代码编辑功能。首次 SSH 到远程服务器时下载，所以首次可能会比较慢。

> VSCode Server 的版本要和 VSCode 的版本对应，当 VSCode 更新时，下次 SSH 登陆远程服务器，VSCode Server 会重新下载安装更新后的版本。二者对应用的是<commit_id>，可以在 【VSCode 菜单栏】-->【Help】->【About】下查看【Commit】的值 。

### 自动安装

1. **安装 Remote-SSH 扩展**：
   - 在 VS Code 中，打开扩展市场（快捷键：`Ctrl+Shift+X`）。
   - 搜索并安装 `Remote - SSH` 扩展。
2. **配置 SSH 连接**：
   - 打开命令面板（快捷键：`Ctrl+Shift+P`）。
   - 输入并选择 `Remote-SSH: Connect to Host...`。
   - 如果这是你第一次设置连接，你需要配置 SSH 主机。在弹出的对话框中，输入远程主机的 SSH 地址（如 `user@hostname`）。
   - 如果 SSH 主机已经配置好，选择你要连接的主机。
3. **连接到远程主机**：
   - 选择要连接的远程主机后，VS Code 将使用配置的 SSH 密钥或密码进行连接。
   - 连接成功后，VS Code 会自动在远程主机上安装所需的 VS Code Server。这通常包括下载并解压必要的文件。
4. **安装过程**：
   - 在连接的过程中，你可能会看到 VS Code 的输出窗口显示安装进度。
   - 一旦安装完成，你将在 VS Code 的左下角看到一个绿色的远程连接图标，表示你已经连接到远程主机。

**自动安装失败检查**：
在某些情况下，自动安装可能失败（网络不稳定）。这种情况下，你可以先进行下述检查后再次尝试：

1. **查看日志**：
   - 打开输出窗口（`View` -> `Output`）。
   - 从下拉菜单中选择 `Remote - SSH` 查看连接和安装过程的日志。
2. **检查权限**：
   - 确保你的用户对安装目录有写权限。
   - 如果需要，尝试使用 `sudo` 权限进行安装（注意安全性和权限管理）。

### 手动下载和安装

当远程服务器无法访问外网或网络不稳定一直安装失败时，就需要手动安装。

1. **下载 VS Code Server**：

   - 使用 `wget` 或 `curl`

     从能联网的机器上运行下述命令下载 VS Code Server。例如：

     ```shell
     wget https://update.code.visualstudio.com/commit:<commit_id>/server/<platform>/<architecture>/stable -O vscode-server.tar.gz
     # 这个 URL 包含了具体的 `commit_id`、`platform` 和 `architecture` 信息。

     # 例子：
     wget https://update.code.visualstudio.com/commit:f1e16e1e6214d7c44d078b1f0607b2388f29d729/server-linux-x64/stable -O vscode-server.tar.gz
     ```

     下载完成之后，把软件包拷贝到不能联网的远程服务器。可以使用 scp 命令或者 winscp 等 ftp 工具。

2. **解压下载的文件**：

   - 解压下载的 tar 文件：

     ```shell
     tar -xzf vscode-server.tar.gz -C ~/.vscode-server/bin/<commit_id>
     ```

   - 创建解压目录（如果它不存在的话）：

     ```shell
     mkdir -p ~/.vscode-server/bin/<commit_id>
     ```

3. **设置权限**：

   - 确保文件和目录具有正确的权限，以便 VS Code 可以运行：

     ```shell
     chmod -R 755 ~/.vscode-server/bin/<commit_id>
     ```

4. **重启 VS Code 并重新连接**：

   - 断开远程连接，然后重新连接。VS Code 应该检测到 VS Code Server 已经安装，并直接使用它。

## 插件

### C++ 插件

- **C/C++ Extension Pack**: 此扩展包包含一组用于 Visual Studio Code 中 C++ 开发的流行扩展。**安装这 1 个，会自动安装下面 4 个**。

  - [C/C++](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)
  - [C/C++ 主题](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools-themes)
  - [CMake](https://marketplace.visualstudio.com/items?itemName=twxs.cmake)
  - [CMake 工具](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cmake-tools)

- **C/C++**: 此扩展为 Visual Studio Code 添加了对 C/C++ 的语言支持，包括[编辑（IntelliSense）](https://code.visualstudio.com/docs/cpp/cpp-ide)和[调试](https://code.visualstudio.com/docs/cpp/cpp-debug)功能。

  > 插件市场链接：[C/C++](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)，介绍信息挺有用的。
  > C/C++ 扩展**不包含** C++ **编译器**或**调试器**。您需要安装这些工具或使用计算机上已安装的工具。如 Windows 上可以用 MinGW。

- **C/C++ Themes**：语义着色，提供的较少，且不如直接换主题自由。**觉得意义不大**。

- **CMake**：此扩展为 Visual Studio Code 中的[CMake](http://www.cmake.org/)提供支持。提供特性：着色，补全，注释，代码片段，函数快速帮助。

- **CMake Tools**：CMake Tools 为原生开发人员提供了针对 Visual Studio Code 中基于 CMake 的**项目**的功能齐全、便捷且强大的工作流程。可直接查看/配置项目。

### 反汇编插件

- x86 and x86_64 Assembly：

### python 插件

- **Python**：提供对 IntelliSense（Pylance）、调试（Python 调试器）、格式化、linting、代码导航、重构、变量资源管理器、测试资源管理器等的支持！

  > Python 扩展将默认自动安装以下扩展，以在 VS Code 中提供最佳的 Python 开发体验：
  >
  > - [Pylance——](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)提供高性能 Python 语言支持
  > - [Python 调试器](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)- 使用 debugpy 提供无缝调试体验

- **autoDocstring - Python Docstring Generator**：快速生成 Python 函数的文档字符串。

- **Jinja**：提供对 Jinja 模板语言的语言着色支持。

### shell 插件

编写 shell 脚本，有以下插件可以选择：

1. shellman - Remisa
   智能提示和自动补全，shellman 全部搞定

2. shellcheck - Timon Wong
      语法错误检查

3. shell-format - foxundermoon
   快捷键：Ctrl + Shift + I

到这里，刀就已经磨好了，去劈柴吧少年~

> 本文转载自：[VScode 打造 shell 脚本 IDE](https://zhuanlan.zhihu.com/p/199187317)

### 代码编辑插件

- **Vim**: VSCodeVim 是 Visual Studio Code 的 Vim 模拟器。
- **VSCode Neovim**：Neovim 是 Vim 的一个分支，可实现更高的可扩展性和集成性。此扩展使用完全嵌入的 Neovim 实例，不再是半成品 Vim 模拟！VSCode 的本机功能用于插入模式和编辑器命令，从而充分利用这两个编辑器。

### icon 图标插件

- **vscode-icons**：目录树图标主题，风格硬朗。
- **Material Icon Theme**：与 vscode-icons 差不多，风格卡通一点。**推荐**。

### 主题插件

- **One Dark Pro**：偏灰色的主题，用着不错
- **Atom One Dark Theme**：也还行，感觉字体颜色没有上面的多
- **Dracula Theme Official**：吸血鬼主题配色，写代码颜色区分清晰，**推荐**。
- **Material Theme — Free**：偏灰绿，有多种可选。

### markdown 插件

- **Markdown Preview Enhanced**：超级强大的 Markdown 插件，预览滑动同步、Pandoc、自定义预览 css、TOC、Latex、渲染代码运行结果（配置复杂）。
- **Markdown All in One**：Markdown 所需的一切（键盘快捷键、目录、自动预览、数学公式、列表编辑、自动补全等）。
- **PlantUML**：提供 UML 支持。如要在 markdown 中渲染，需配置 Markdown Preview Enhanced。
- **Markdown Table Prettifier**：编辑/格式化表格，将 csv 文本转化为表格。

### 代码风格规范插件

- **Prettier - Code formatter**：主要支持前端语言，JavaScript、[JSX](https://facebook.github.io/jsx/)、[Angular](https://angular.io/)、[Vue](https://vuejs.org/)、[Flow](https://flow.org/)、[TypeScript](https://www.typescriptlang.org/)、CSS, [Less](http://lesscss.org/), and [SCSS](https://sass-lang.com/)、[HTML](https://en.wikipedia.org/wiki/HTML)、[Ember/Handlebars](https://handlebarsjs.com/)、[JSON](https://json.org/)、[GraphQL](https://graphql.org/)、[Markdown](https://commonmark.org/), including [GFM](https://github.github.com/gfm/) and [MDX v1](https://mdxjs.com/)、[YAML](https://yaml.org/)
- **Better Align**：无论是否选择**任何语言**，任何字符或单词都可以实现更好的**垂直对齐**。
- **indent-rainbow**：用颜色填充缩进，非常直观，如果有缩进错误还会变成红色。**对写 `Python` 用处极大**。

### 其他插件

- LeetCode: Solve LeetCode problems in VS Code
- LeetCode with labuladong: 帮助 labuladong 的读者高效刷题

> 参考网址：
>
> - vs-code“实用插件”：<https://hailangya.com/articles/2021/03/15/vs-code-plugins/>
> - 10 款 VS Code 插件神器，第 7 款超级实用！：<https://cloud.tencent.com/developer/article/1889258>

## 插件配置

### prettier 插件

由于笔者不写前端语言，此插件的主要用途是用来格式化 markdown。

#### prettier 配置

使用此扩展配置 Prettier 有多种方式。您可以使用[VS Code 设置](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode#prettier-settings)、[Prettier 配置文件](https://prettier.io/docs/en/configuration.html)或`.editorconfig`文件。VS Code 设置旨在用作后备，通常仅用于非项目文件。**建议您始终在项目中包含一个 Prettier 配置文件，指定项目的所有设置**。这将确保无论您如何运行 Prettier（从此扩展、从 CLI 或从另一个带有 Prettier 的 IDE），都将应用相同的设置。

建议使用[Prettier 配置文件](https://prettier.io/docs/en/configuration.html)来设置格式化选项。选项从正在格式化的文件开始递归搜索，因此如果您想将 Prettier 设置应用于整个项目，只需在根目录中设置配置即可。配置选项参考：[Options](https://prettier.io/docs/en/options.html)。

在项目目录下新增文件 `.prettierrc.json`，或者在 vscode 配置文件 `settings.json` 中，**直接添加**下述内容：

```json
{
  "//参考网址": "https://prettier.io/docs/en/options",
  "//printWidth": "默认 80",
  "printWidth": 120,
  "//tabWidth": "默认 2",
  "tabWidth": 2,
  "//useTabs": "默认 false",
  "useTabs": false,
  "//semi": "默认 false",
  "semi": false,
  "//singleQuote": "默认 false",
  "singleQuote": false,
  "//quoteProps": "默认 as-needed",
  "quoteProps": "as-needed",
  "//trailingComma": "默认 all",
  "trailingComma": "es5",
  "//bracketSpacing": "默认 true",
  "bracketSpacing": true,
  "//bracketSameLine": "默认 true",
  "bracketSameLine": false,
  "//arrowParens": "默认 always",
  "arrowParens": "always",
  "//proseWrap": "默认 preserve",
  "proseWrap": "preserve",
  "//endOfLine": "默认 lf",
  "endOfLine": "lf",
  "//embeddedLanguageFormatting": "默认 auto",
  "embeddedLanguageFormatting": "auto"
}
```

#### prettier 插件问题

> :warning: 在格式化 markdown 的时候，针对 **markdown 中的数学公式** $ $，会把 `_` 换成 `*`，原因可能是 pretteir 默认使用 `*` 进行斜体的格式化，当公式中出现多个 `_` 时，可能被语法树分析成斜体从而被改成 `*`。

**问题**：
`$$ \mu_B = \frac{1}{m} \sum_{i=1}^{m} x_i $$` 格式化成
`$$ \mu*B = \frac{1}{m} \sum*{i=1}^{m} x*i $$`

**解决方案**：

要让 Prettier 在格式化 Markdown 文件时忽略数学公式（尤其是用 `$$` 包围的块级 LaTeX 数学公式），你可以通过以下几种方法实现：

1. 使用 Prettier 的 `prettier-ignore` 注释

   Prettier 支持在文件中添加 `prettier-ignore` 注释，来忽略特定部分的格式化。你可以在公式的上方加上 `<!-- prettier-ignore -->` 注释，让 Prettier 跳过格式化该公式。
   Prettier 只会忽略**紧随注释的多行代码块或段落**（即**遇到空行结束**，可以包含空格或换行），其他部分仍会遵循默认的格式化规则。

   示例：

   ```markdown
   <!-- prettier-ignore -->
   添加 `prettier-ignore` 注释，下面的两行都不会被格式化。直至遇见空行。
   对于两个矩阵 $ A_{m \times p} $ 和 $ B_{p \times n} $，它们的乘积 $ C_{m \times n} = AB $ 是一个 $ m \times n $ 的矩阵。
   $$ C_{(i, j)} = \Sigma_{k=1}^n A_{(i, k)} \times B_{(k, j)} $$

   上面有空行，这里以及下面的代码会被格式化。
   $$ C*{(i, j)} = \Sigma*{k=1}^n A*{(i, k)} \times B*{(k, j)} $$
   ```

   当 Prettier 遇到这个注释时，它会跳过对这个公式的格式化。

2. 使用 `remark-math` 插件与 Prettier 配合（**复杂未尝试**）

   目前，Prettier 并没有内置的选项来自动跳过 Markdown 中的数学公式。不过，可以通过结合 `remark` 插件来实现更细粒度的控制。
   你可以自己编写或使用现有的 `remark` 插件，来处理 Markdown 中的数学公式部分，并跳过对它们的格式化。
   `remark-math` 是一个 `remark` 插件，它能够识别并处理 Markdown 中的数学公式。你可以使用它配合 Prettier 一起工作。

   **步骤**：

   1. 安装 `remark-math` 和 `remark-html-katex`（用于将数学公式转换成可视化效果）：

      ```bash
      npm install remark-math remark-html-katex
      ```

   2. 在 Prettier 的配置文件中添加自定义的 `remark` 配置，以识别数学公式并跳过它们的格式化：

      ```javascript
      const remarkMath = require("remark-math");
      const remarkHtmlKatex = require("remark-html-katex");

      module.exports = {
        plugins: [
          // 使用 remark-math 插件来处理数学公式
          {
            name: "markdown",
            parse: "markdown",
            plugins: [remarkMath, remarkHtmlKatex],
          },
        ],
      };
      ```

   3. 将公式用 `$$` 或 `$` 包围，Prettier 将能够识别出这些公式，并通过插件处理它们，而不会对公式内容进行重新格式化。

      示例：

      ```markdown
      Here is an inline formula: $E = mc^2$

      Here is a block formula:

      $$
      a^2 + b^2 = c^2
      $$
      ```

      通过 `remark-math` 插件，Prettier 不会对这些数学公式的内容进行重新排版和格式化，而是保持公式原有的样式。

3. 使用 `.prettierignore` 文件（全局忽略）

   如果你想完全避免 Prettier 格式化某些 Markdown 文件（或特定类型的文件），你可以使用 `.prettierignore` 文件来忽略这些文件的格式化。这对于包含大量数学公式的文件可能是一个简单的解决方案。

   示例：

   在项目根目录下创建一个 `.prettierignore` 文件，并添加你要忽略的 Markdown 文件路径：

   ```bash
   # .prettierignore
   docs/math-heavy-file.md
   ```

   这种方法适用于需要跳过特定文件的情况，而不是局部忽略公式的格式化。

4. 总结

   - **局部忽略**：使用 `<!-- prettier-ignore -->` 注释跳过某个数学公式的格式化。
   - **插件方式**：使用 `remark-math` 插件结合 Prettier，让 Prettier 识别数学公式并跳过其格式化。
   - **全局忽略**：通过 `.prettierignore` 文件，忽略某些特定的 Markdown 文件的格式化。

### PlantUML && MPE

在 VSCode 中使用 Markdown 编写 UML 图，通常使用的是 `PlantUML` 插件。以下是配置环境和书写代码的步骤：

1. 安装 VSCode 插件

   首先需要在 VSCode 中安装相关插件：

   - `PlantUML`：这是一个可以让你在 Markdown 中使用 PlantUML 语法绘制 UML 图的插件。需要安装 java。
   - `Markdown All in One`：支持 Markdown(键盘快捷键、目录、自动预览等)。
   - `Markdown Preview Enhanced`：可以对 Markdown 做增强预览, 比如支持各种绘图等。

2. 下载 plantuml jar 包

   从 **[PlantUML](https://plantuml.com/zh/download)** 直接下载集成 Graphviz 的 jar 包。
   LGPL 协议的 jar 包不集成 Graphviz。

3. 安装 Java

   PlantUML 依赖 Java 运行环境。如果你没有安装 Java，需要安装一个。你可以从 **[Oracle 官方](https://www.oracle.com/java/technologies/javase-downloads.html)** 或者 **[OpenJDK](https://openjdk.java.net/)** 安装最新版本的 JDK。

   确保 Java 安装成功后，你可以通过命令行执行以下命令来验证：

   ```bash
   java -version
   ```

4. 安装 Graphviz

   PlantUML 需要 Graphviz 来生成图表。你可以从 **[Graphviz 官网](https://graphviz.org/)** 下载并安装。

   安装成功后，也可以通过命令行验证安装：

   ```bash
   dot -version
   ```

5. 配置 VSCode 设置

   如果是**在 Markdown 文件中嵌入 UML 代码**，预览时需要配置 `markdown-preview-enhanced` 插件，下面配置一个就可以。

   - 方法一：使用 PlantUML 官网提供的 `plantuml.jar` 包（需要本地安装 JDK 并配置 java 系统环境变量）
   - 方法二：直接使用 plantumlServer。只有联网才能用。

   ```json
   "markdown-preview-enhanced.plantumlJarPath": "D:\\Program Files\\plantuml-lgpl-1.2024.7.jar",
   "markdown-preview-enhanced.plantumlServer": "https://kroki.io/plantuml/svg/",
   ```

   如果不配置，则报错如下：

   ```log
   Error: plantuml.jar file not found: ""

   Please download plantuml.jar from https://plantuml.com/download.

   If you are using VSCode or coc.nvim, then please set the setting "markdown-preview-enhanced.plantumlJarPath" to the absolute path of plantuml.jar file.

   If you don't want to use plantuml.jar, then you can use the online plantuml server
   by setting the setting "markdown-preview-enhanced.plantumlServer" to the URL of the online plantuml server, for example: https://kroki.io/plantuml/svg/
   ```

   如果是**直接新建 plantuml 文件编写代码**，则需要对 `PlantUML` 插件进行配置：

   - 实测配置了 java 和 Graphviz 的系统环境变量后，不进行下述配置也可以。如果不行请再配置。

   ```json
   "plantuml.java": "C:/path/to/java",  // Java 路径
   "plantuml.jar": "C:/path/to/plantuml.jar",  // PlantUML 的 jar 包路径
   "plantuml.exportFormat": "png",  // 导出格式，常用的有 png, svg
   ```

6. 编写 UML 代码

   你可以在 Markdown 文件中嵌入 UML 代码，用于生成图表。PlantUML 支持各种 UML 图，例如类图、时序图、用例图等。
   `@startuml` 和 `@enduml` 之间的内容是你的 UML 代码：

   ```plantuml
   @startuml
   Alice -> Bob: Hello
   Bob --> Alice: Hi
   @enduml
   ```

   或者新建 plantuml 文件，支持格式 `*.wsd`, `*.pu`, `*.puml`, `*.plantuml`, `*.iuml`，然后把上面的代码拷贝到文件中（注意不能含头尾```）。

7. 预览 UML 图
   在 VSCode 中，右键点击包含 UML 代码的 Markdown 文件，可以选择 "Preview" 选项来查看生成的图形。`PlantUML` 插件会自动渲染图表。

   你也可以通过 `Ctrl+P` 打开命令面板，搜索 `PlantUML: Preview` 来预览。

8. 导出图表
   使用 `PlantUML` 插件，你可以右键 UML 代码块，选择“Export Current Diagram”来导出图片格式，如 PNG、SVG 或 PDF。

9. 总结

   1. 安装 PlantUML 插件。
   2. 安装并配置 Java 和 Graphviz。
   3. 在 Markdown 中使用 `plantuml` 代码块编写 UML 代码。
   4. 预览和导出图表。

## 软件配置

首先输入：`command + p`，然后输入：`Settings`，接下来，选择：`Preferences: Open Settings (UI)`，就进入了快捷键文件 `settings.json` 编辑页面。

路径：C:\Users\c00619335\AppData\Roaming\Code\User\settings.json

### 基础配置参考

```json
{
    // leetcode
    "leetcode.endpoint": "leetcode-cn",
    "leetcode.defaultLanguage": "cpp",
    "leetcode.showDescription": "Both",
    "leetcode.showLocked": true,
    
    // 信任区域
    "security.workspace.trust.banner": "never",
    "security.workspace.trust.untrustedFiles": "open",
    
    // markdown 插件
    "markdown-preview-enhanced.codeBlockTheme": "solarized-dark.css",
    "markdown-preview-enhanced.previewTheme": "solarized-dark.css",
    
    // editor
    "editor.minimap.enabled": false,
    "editor.lineNumbers": "relative",
    "workbench.iconTheme": "vscode-icons",
    "C_Cpp.clang_format_fallbackStyle": " { BasedOnStyle: Visual Studio,  ColumnLimit: 120 }",
    // "editor.fontFamily": "Fira Code, Consolas, 'Courier New', monospace",
    // "editor.fontLigatures": true,
    "editor.fontFamily": "Operator Mono",
    "editor.fontLigatures": true, // 这个控制是否启用字体连字，true启用，false不启用，这里选择启用
    "editor.tokenColorCustomizations": {
        "textMateRules": [
            {
                "name": "italic font",
                "scope": [
                    "comment",
                    "keyword",
                    "storage",
                    "keyword.control.import",
                    "keyword.control.default",
                    "keyword.control.from",
                    "keyword.operator.new",
                    "keyword.control.export",
                    "keyword.control.flow",
                    "storage.type.class",
                    "storage.type.function",
                    "storage.type",
                    "storage.type.class",
                    "variable.language",
                    "variable.language.super",
                    "variable.language.this",
                    "meta.class",
                    "meta.var.expr",
                    "constant.language.null",
                    "support.type.primitive",
                    "entity.name.method.js",
                    "entity.other.attribute-name",
                    "punctuation.definition.comment",
                    "text.html.basic entity.other.attribute-name.html",
                    "text.html.basic entity.other.attribute-name",
                    "tag.decorator.js entity.name.tag.js",
                    "tag.decorator.js punctuation.definition.tag.js",
                    "source.js constant.other.object.key.js string.unquoted.label.js",
                ],
                "settings": {
                    "fontStyle": "italic",
                }
            },
        ]
    },
    "editor.fontSize": 16,
    "terminal.integrated.cursorStyle": "line",
    "terminal.integrated.defaultProfile.windows": "Git Bash",
    "[cpp]": {
        "editor.defaultFormatter": "NextCode.nextcode-check"
    },
    "vim.insertModeKeyBindings": [
        {
            "before": [
              "j",
              "j"
            ],
            "after": [
              "<Esc>"
            ]
        },
      ],
    "vim.vimrc.enable": true
}
```

### 按键映射

> [Visual Studio Code 的按键绑定](https://code.visualstudio.com/docs/getstarted/keybindings#_keyboard-shortcuts-reference)

首先输入：`command + p`，然后输入：`keyboard`，接下来，选择：`Preferences: Open Keyboard shortcurs(JSON)`，就进入了快捷键文件 keybindings.json 编辑页面。

路径：C:\Users\c00619335\AppData\Roaming\Code\User\keybindings.json

```json
// 将键绑定放在此文件中以覆盖默认值
[
    {
        "key": "ctrl+f",
        "command": "cursorRight",
        "when": "editorTextFocus && vim.active && vim.use<C-f> && !inDebugRepl && vim.mode == 'Insert'"
    },
    {
        "key": "ctrl+b",
        "command": "cursorLeft",
        "when": "editorTextFocus && vim.active && vim.use<C-b> && !inDebugRepl && vim.mode == 'Insert'"
    },
    {
        "key": "ctrl+p",
        "command": "cursorUp",
        "when": "editorTextFocus && vim.active && vim.use<C-p> && !inDebugRepl && vim.mode == 'Insert'"
    },
    {
        "key": "ctrl+n",
        "command": "cursorDown",
        "when": "editorTextFocus && vim.active && vim.use<C-n> && !inDebugRepl && vim.mode == 'Insert'"
    },
]
```

其他可参考：

> [VSCode Terminal 快捷键设置](https://zgljl2012.com/vscode-terminal-kuai-jie-jian-she-zhi/)

```json
// Place your key bindings in this file to override the defaults
[
    { "key": "ctrl+1",                "command": "workbench.action.terminal.focusAtIndex1", "when": "terminalFocus" },
    { "key": "ctrl+2",                "command": "workbench.action.terminal.focusAtIndex2", "when": "terminalFocus" },
    { "key": "ctrl+3",                "command": "workbench.action.terminal.focusAtIndex3", "when": "terminalFocus" },
    { "key": "ctrl+4",                "command": "workbench.action.terminal.focusAtIndex4", "when": "terminalFocus" },
    { "key": "ctrl+5",                "command": "workbench.action.terminal.focusAtIndex5", "when": "terminalFocus" },
    { "key": "ctrl+6",                "command": "workbench.action.terminal.focusAtIndex6", "when": "terminalFocus" },
    { "key": "ctrl+7",                "command": "workbench.action.terminal.focusAtIndex7", "when": "terminalFocus" },
    { "key": "ctrl+8",                "command": "workbench.action.terminal.focusAtIndex8", "when": "terminalFocus" },
    { "key": "ctrl+9",                "command": "workbench.action.terminal.focusAtIndex9", "when": "terminalFocus" },
    { "key": "ctrl+t",                "command": "workbench.action.terminal.new", "when": "terminalFocus" },
    { "key": "ctrl+p",                "command": "cursorup", "when": "terminalFocus" },
    { "key": "ctrl+n",                "command": "cursordown", "when": "terminalFocus" }

]
// 这就设置好了基础的配置。ctrl+1-9 用于切换终端， ctrl+t 用于创建新终端。
```

### vscode 标签页高亮

在系统的 `settings.json` 里添加

```json
    "workbench.colorCustomizations": {
        "tab.activeBackground": "#d9ff009d",
        "editor.lineHighlightBackground": "#ffd00033"
    },
```

### 文件标签栏多行显示

**方法一**：
打开 vscode 设置，搜索 `wrapTabs`，会出现 `workbench.editor.wrapTabs` 选项：

- 勾选该设置，多行显示。
- 取消勾选，单行显示。

**方法二**：

在系统的 `settings.json` 里添加

```json
    "workbench.editor.wrapTabs": true,
```

`true`：多行显示。`false`：单行显示。

### 显示错误和告警

1. 使用内置的 "Problems" 面板：

   VS Code 默认会在 "Problems" 面板中显示错误和警告。虽然这不是直接显示在代码末尾，但它提供了一个集中的错误查看位置。

2. 安装 **Error Lens** 扩展：

   - 在扩展市场中搜索 `Error Lens` 并安装。

   - `Error Lens` 扩展能够将错误和警告信息直接显示在相应的代码行末。

   - 安装后，可以**根据需要**进行配置。打开设置文件（`settings.json`），添加或修改以下配置项：

     ```json
     "errorLens.enabled": true,
     "errorLens.fontWeight": "normal",
     "errorLens.fontStyle": "normal",
     "errorLens.italic": false,
     "errorLens.fontSize": "12px",
     "errorLens.messageBackgroundMode": "message",
     "errorLens.messageBackgroundColor": "rgba(255,255,255,0.1)",
     "errorLens.errorForeground": "#ff0000",
     "errorLens.warningForeground": "#ffa500",
     "errorLens.infoForeground": "#0000ff",
     "errorLens.hintForeground": "#008000",
     ```

## 使用技巧

### 查找匹配行，存至文件

1. 在 vscode 中，可以使用如下**正则搜索**包含特性字符串的行：

   ```shell
   # 行之间没有空行
   ^.*特定字符串.*$
   # 如果要每行下面都有一个空行，需要把 $ 替换成换行符 \n。经尝试，linux 和 windows 下都用\n
   ^.*特定字符串.*\n
   ```

2. 按 `Alt + Enter`，即可选中所有已经匹配到的文字。

3. 按 `Ctrl + C` 复制，再 `Ctrl + N` 新建文件，再 `Ctrl + V` 粘贴，在 `Ctrl + S` 保存文件即可。

### 搜索编辑器

1. 在 vscode 中侧边栏中，找到 search 项，在 SEARCH 栏中点击 `Open New Seach Editor`(中间的图标)。

2. 输入要搜索的内容，即可像文件一样展示搜索结果。

## 调试

> 官方文档：
>
> [python](https://vscode.js.cn/docs/python/debugging)
>
> [C++](https://vscode.js.cn/docs/cpp/launch-json-reference)

### 调试添加运行参数

`launch.json` 中添加 `args` 项，每个运行参数是一个字符串，如：

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "args": [
                "./xxx/xxx.yaml",
                "--xxx=xxx"
            ]
        }
    ]
}
```

### 调试添加环境变量

`launch.json` 中添加 `envs` 项：

1. **python/bash 用 `env`**

   ```json
   "env": {
       "PYTHONPATH": "/usr/local/xxx/xxx/python:${env:PYTHONPATH}",
       "PATH": "~/xxx/xxx:${env:PATH}",
       "LD_LIBRARY_PATH": "~/xxx/lib64:${env:LD_LIBRARY_PATH}"
   }
   ```

2. **C/C++ 用 `environment`**

   ```json
   "environment":[
   {
     "name":"squid",
     "value":"clam"
   }
   ]
   ```

> :warning: **注意**：
> 在 VSCode 的 `launch.json` 中，**同一个环境变量不能配置多次**。如果你在多个地方配置同一个环境变量（如 `PATH`），后面的配置会覆盖前面的配置。
>
> 追加环境变量，要使用 `${env:xxx}`，而不能用 `$xxx`。
>
> `${env:PATH}` 是 VSCode 的变量替换语法，用于引用当前系统环境中的 `PATH` 变量。在 `launch.json` 中使用 `${env:PATH}` 可以获取到当前用户或系统定义的 `PATH` 环境变量的值。这确保了在调试过程中，新的环境变量配置能够基于现有的 `PATH`，而不是覆盖它。
>
> **平台差异**
>
> 需要注意的是，`PATH` 环境变量的路径分隔符在不同操作系统中是不同的：
>
> - Windows：使用分号 `;` 作为路径分隔符。例子：`C:\Program Files;C:\Windows\System32`。
> - Unix/Linux/macOS：使用冒号 `:` 作为路径分隔符。例子：`/usr/local/bin:/usr/bin:/bin`。
>
> 因此，在配置 `launch.json` 时，确保使用正确的路径分隔符。例如，在 Unix 系统上，应该使用 `:`，而在 Windows 上使用 `;`。
>
> **路径格式**：
>
> - **Windows**：使用反斜杠 `\`，需要转义为双反斜杠 `\\`，例如 `C:\\my\\new\\path`。
> - **Unix/Linux/macOS**：使用正斜杠 `/`，例如 `/my/new/path`。

### 调试设置当前工作路径

`launch.json` 中添加 `cwd` 项：

Specifies the current working directory for the debugger, which is the base folder for any relative paths used in code. If omitted, defaults to `${workspaceFolder}` (the folder open in VS Code).

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "cwd": "xxx/xxx"
        }
    ]
}
```

### 查看反汇编代码

运行程序后，在监视变量中添加：

```bash
-exec disassemble /m main
# 或
-exec disassemble /m
```

然后在**<font color=red>调试控制台</font>**就可以看到汇编代码了。

## c++ intellisense 排除某些文件

在 Visual Studio Code (VS Code) 中配置 C++ IntelliSense 时，有时你可能需要排除某些文件或目录，以避免它们影响 IntelliSense 功能。以下是如何在 `c_cpp_properties.json` 文件中配置排除文件或目录的详细步骤。

### 使用 `c_cpp_properties.json` 配置排除路径

`c_cpp_properties.json` 文件主要用于配置 IntelliSense 的包含路径、编译器路径等。然而，它本身不支持直接排除文件。你可以通过以下几种间接方法来实现：

通过修改 `includePath`

虽然 `c_cpp_properties.json` 没有提供直接的排除选项，但你可以控制 `includePath` 的设置，间接影响哪些文件被包含在 IntelliSense 中。

1. 打开或创建 `c_cpp_properties.json` 文件：

   - 按 `Ctrl` + `Shift` + `P` 打开命令面板。
   - 输入 `C/C++: Edit Configurations (UI)` 或 `C/C++: Edit Configurations (JSON)` 并选择。

2. 配置 `includePath`，仅包括你需要的路径。例如，如果你有某些目录不想包含在 IntelliSense 中，不将这些目录添加到 `includePath` 中：

   ```json
   {
       "configurations": [
           {
               "name": "Win32",
               "includePath": [
                   "${workspaceFolder}/src",   // 仅包含 src 目录
                   "${workspaceFolder}/include" // 仅包含 include 目录
               ],
               "defines": [],
               "compilerPath": "C:/path/to/your/compiler",
               "cStandard": "c11",
               "cppStandard": "c++17",
               "intelliSenseMode": "gcc-x64"
           }
       ],
       "version": 4
   }
   ```

   通过仅包括你需要的路径，实际上排除了其他目录的影响。

### 使用 `.vscode/settings.json` 排除文件和目录

另一个方法是通过 VS Code 的**工作区配置**设置排除文件或目录，这样可以影响到 IntelliSense 的显示效果。

1. 打开 `.vscode/settings.json` 文件：

   - 进入工作区文件夹，找到 `.vscode` 文件夹。
   - 创建或编辑 `settings.json` 文件。

2. 配置 `files.exclude` 和 `search.exclude`，排除特定的文件或目录。例如：

   ```json
   {
       "files.exclude": {
           "**/test/**": true,        // 排除所有 test 目录
           "**/*.tmp": true           // 排除所有 .tmp 文件
       },
       "search.exclude": {
           "**/test/**": true,        // 在搜索时排除 test 目录
           "**/*.tmp": true           // 在搜索时排除 .tmp 文件
       }
   }
   ```

   这些设置**主要影响文件浏览器和搜索功能**，但也会间接影响 IntelliSense，因为这些文件不会被索引。

3. 使用 `C_Cpp.files.exclude` 设置

   这个设置专门用于 C/C++ 扩展，可以控制哪些文件和目录被排除在 IntelliSense 引擎的处理之外，从而影响代码跳转、自动完成等功能。

   打开 `.vscode/settings.json` 文件，添加或修改 `C_Cpp.files.exclude` 设置

   ```json
   {
       "C_Cpp.files.exclude": {
           "**/build/**": true,
           "**/third_party/**": true,
           "**/test/**": true,
           "**/CMakeFiles/**": true
       }
   }
   ```

   这个配置会排除：

   - `build` 目录及其所有子目录
   - `third_party` 目录及其所有子目录
   - `test` 目录及其所有子目录
   - `CMakeFiles` 目录及其所有子目录

   > 与 `files.exclude` 的区别：
   > `C_Cpp.files.exclude` **只影响 C/C++ 扩展**的行为，不会影响文件在 VS Code 文件浏览器中的可见性。

### 过滤符号

如果某些符号或文件仍然被 IntelliSense 识别，可以考虑使用 `c_cpp_properties.json` 中的 `browse` 配置来进一步限制哪些文件被解析：

1. 打开 `c_cpp_properties.json` 文件。

2. 添加 `browse.path` 配置项，用于指定符号解析的路径：

   ```json
   {
       "configurations": [
           {
               "name": "Win32",
               "includePath": [
                   "${workspaceFolder}/src",
                   "${workspaceFolder}/include"
               ],
               "browse": {
                   "path": [
                       "${workspaceFolder}/src",
                       "${workspaceFolder}/include"
                   ],
                   "limitSymbolsToIncludedHeaders": true
               },
               "defines": [],
               "compilerPath": "C:/path/to/your/compiler",
               "cStandard": "c11",
               "cppStandard": "c++17",
               "intelliSenseMode": "gcc-x64"
           }
       ],
       "version": 4
   }
   ```

   在 `browse.path` 中指定你希望被解析的路径，并设置 `limitSymbolsToIncludedHeaders` 为 `true`，将**符号解析限制在 `includePath` 和 `browse.path` 中指定的文件和路径中**。

## c_cpp_properties.json

1. 官方文档：
   您应该查阅的主要文档是 VS Code 官方网站上的 C/C++ 扩展文档：
   <https://code.visualstudio.com/docs/cpp/c-cpp-properties-schema-reference>
2. 主要属性：
   `c_cpp_properties.json` 文件中可以设置的一些重要属性包括：
   - `configurations`: 一个数组，包含不同的配置选项。
   - `name`: 配置的名称。
   - `includePath`: 指定额外的包含目录。
   - `defines`: 预处理器定义。
   - `compilerPath`: 编译器的路径。
   - `cStandard`: C 语言标准。
   - `cppStandard`: C++ 语言标准。
   - `intelliSenseMode`: IntelliSense 模式。
   - `browse`: 配置符号数据库。
     - `path`: 浏览路径。
     - `limitSymbolsToIncludedHeaders`: 是否限制符号到包含的头文件。
     - `databaseFilename`: 数据库文件名。
   - `compileCommands`: compile_commands.json 文件的路径。
   - `forcedInclude`: 强制包含的文件。
   - `configurationProvider`: 配置提供者。
3. JSON 模式：
   VS Code 使用 JSON 模式来验证 `c_cpp_properties.json` 文件。您可以在以下链接中查看完整的模式定义：
   <https://github.com/microsoft/vscode-cpptools/blob/main/Extension/c_cpp_properties.schema.json>
4. 配置示例：
   文档中通常会提供一些配置示例，这些可以作为很好的起点：
   <https://code.visualstudio.com/docs/cpp/config-linux>
   <https://code.visualstudio.com/docs/cpp/config-msvc>
   <https://code.visualstudio.com/docs/cpp/config-clang-mac>
5. 扩展命令：
   在 VS Code 中，您可以使用 "C/C++: Edit Configurations (UI)" 命令来通过图形界面编辑这些设置，这可能会更直观一些。
6. 更新和变化：
   C/C++ 扩展经常更新，所以建议定期查看最新的文档，了解新的功能和变化。
7. 特定设置：
   对于一些特定的设置，如排除文件和目录，实际上是在 VS Code 的 `settings.json` 文件中配置的，而不是在 `c_cpp_properties.json` 中。这些包括：
   - `files.exclude`
   - `files.watcherExclude`
   - `C_Cpp.files.exclude`

通过仔细阅读这些文档和资源，您应该能够全面了解 `c_cpp_properties.json` 文件的配置选项，以及如何根据您的项目需求进行最佳设置。如果您在配置过程中遇到任何具体问题，欢迎随时询问。

# CLion （Windows）

> 参考：[IntelliJ IDEA 中最被低估的快捷键](https://blog.jetbrains.com/zh-hans/idea/2022/11/intellij-idea-3/)

## clion 快捷键

- `Ctrl+Shift+f7`：高亮所有选中文本，按 ESC 取消高亮
- `Tab/Shift+Tab`：缩进，反缩进
- `Ctrl+Shift+j`：连接行
- `Ctrl+x`：剪切当前行，或选定块到剪贴板
- `Ctrl+d`：复制当前行，或选定块
- `Alt+Shift+↑/↓`：移动行
- `Alt+Shift+鼠标左键`：多个光标
- `Alt+Shift+Insert`：切换为块模式，然后鼠标框选
- ``Ctrl+Shift+Alt+鼠标框选`：标选则多行文本
- `Alt+j`：选择多次出现的内容

# Nodejs

```shell
registry=https://registry.npm.taobao.org/
strict-ssl=false
proxy=http://user:password@proxy.huawei.com:8080/
https-proxy=http://user:password@proxy.huawei.com:8080/
```

> **密码中特殊字符的处理**
> 如果密码中有@等特殊字符，会出错，此时要对其中的特殊符号进行处理，使用百分比编码(Percent-encoding)对特殊字符进行转换，转换列表如下：
> ! --> %21 # --> %23 $ --> %24 & --> %26 ' --> %27
> ( --> %28 ) --> %29 \* --> %2A + --> %2B , --> %2C
> / --> %2F : --> %3A ; --> %3B = --> %3D ? --> %3F
> @ --> %40 [ --> %5B ] --> %5D
>
> 例如：密码是 12#，转义之后就是 12%23

## 离线安装

1. 下载 linux 版本的 node.js

   下载网址：<https://nodejs.org/zh-cn/download/package-manager>

   Linux 选择【预构建二进制文件】-->【Linux】-->【x64】-->【v20.16.0(LTS)】-->下载，会得到如 `node-v20.16.0-linux-x64.tar.xz` 的文件。
