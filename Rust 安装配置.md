[toc]

# Rust 安装配置

## Cargo 包管理器

简单来说，**Cargo 是 Rust 编程语言的官方构建工具和包管理器**。

对于 Rust 开发者来说，Cargo 就相当于 Node.js 的 **npm**，Python 的 **pip**，或者 Java 的 **Maven/Gradle**。它极大地简化了 Rust 开发的流程，也是 Rust 语言生态系统中最受好评的工具之一。

以下是 Cargo 的主要核心功能：

1. 依赖管理 (Dependency Management)

   这是 Cargo 最强大的功能。在 C/C++ 等语言中，手动下载库、配置路径、解决版本冲突通常非常痛苦。Cargo 解决了这个问题：
   - **自动下载：** 你只需要在配置文件中写下你想要的库（在 Rust 中称为 **Crate**）的名字和版本，Cargo 会自动从官方仓库 [crates.io](https://crates.io/) 下载它们。
   - **依赖树解决：** 如果你用的库 A 依赖库 B，Cargo 会自动帮你把 B 也下载下来，并确保版本兼容。

2. 构建系统 (Build System)

   Cargo 负责调用 Rust 编译器 (`rustc`) 来编译你的代码。
   - 它知道如何按照正确的顺序编译你的项目和所有依赖项。
   - 它支持不同的构建模式，例如 **Debug 模式**（编译快但运行慢，方便调试）和 **Release 模式**（编译慢但运行极快，用于生产环境）。

3. 项目脚手架 (Project Scaffolding)

   当你开始一个新项目时，不需要手动创建文件夹结构。Cargo 提供了一键生成标准项目结构的命令，确保所有 Rust 项目都有统一的目录规范。

4. 测试与文档 (Testing & Documentation)
   - **测试：** Cargo 内置了测试运行器，你只需要运行 `cargo test`，它就会自动发现并运行你代码中的单元测试和集成测试。
   - **文档：** 运行 `cargo doc`，它会根据你的代码注释自动生成漂亮的 HTML 文档，甚至包括你引用的第三方库的文档。

### Cargo.toml 与 Cargo.lock

在 Cargo 项目中，有两个文件至关重要：

| **文件名**       | **作用**                                                                                                                   | **类比**                                 |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| **`Cargo.toml`** | **清单文件**。也就是“配方表”。你在这里定义项目名称、版本以及你需要用到哪些第三方库。                                       | `package.json` (Node) / `pom.xml` (Java) |
| **`Cargo.lock`** | **锁定文件**。Cargo 自动生成的文件，记录了当前项目使用的所有依赖库的**精确版本号**，确保在不同电脑上构建出的软件完全一致。 | `package-lock.json` (Node)               |

### 常用命令速查

如果你开始学习 Rust，这几个命令会伴随你的每一天：

- `cargo new [项目名]`：创建一个新的 Rust 项目。
- `cargo build`：编译你的项目（Debug 模式）。
- `cargo run`：编译并直接运行你的项目。
- `cargo check`：快速检查代码是否有语法错误（不进行编译，速度非常快，写代码时最常用）。
- `cargo test`：运行测试。
- `cargo build --release`：为正式发布进行优化编译。

### 总结

Cargo 的存在是 Rust 能够迅速流行的一个重要原因。它把“**创建项目 -> 引入库 -> 编写代码 -> 测试 -> 构建 -> 发布**”这一整套流程标准化并自动化了，让开发者可以专注于代码逻辑，而不是折腾环境配置。

## 管理全局工具（装软件）

Rust 生态中有很多好用的命令行工具（比如 `ripgrep` 搜索工具，`bat` 增强版 cat）。如果你想把它们装到电脑上当作日常软件用：

- **安装工具 (Install)**

  ```bash
  cargo install [包名]
  ```

  **示例：** `cargo install ripgrep`
  - **发生了什么：** Cargo 会下载源码，在你电脑上编译成可执行文件，并放到 `~/.cargo/bin` 目录下。
  - **注意：** 不要用这个命令来给你的项目添加依赖库！它只负责装“软件”。

- **卸载工具 (Uninstall)**

  ```bash
  cargo uninstall [包名]
  ```

  **示例：** `cargo uninstall ripgrep`

- **搜索 (Search)**

  ```bash
  cargo search [关键词]
  ```

  **示例：** `cargo search http`
  - **输出：** 会列出 crates.io 上相关的包、版本号和简单描述。

  > **:bulb:** 命令行搜索信息比较有限，通常建议直接去 **[crates.io](https://crates.io/)** 或 **[lib.rs](https://lib.rs/)** 网站搜索，那里有详细的文档、热度排名和使用示例。

# yazi

## yazi 安装

**二、下载预编译二进制文件**

如果你不想处理复杂的依赖报错，直接从 GitHub 下载官方编译好的运行文件即可：

1. 前往 [Yazi GitHub Releases](https://github.com/sxyazi/yazi/releases) 页面。

2. 找到最新版本（Latest），下载符合你架构的文件，例如：
   - `yazi-x86_64-unknown-linux-gnu.zip` (大多数 PC 使用这个)
   - `yazi-aarch64-unknown-linux-gnu.zip` (ARM 架构如树莓派使用)

   **如果有 GLIBC 依赖报错，可以使用静态链接版本 (Musl)** 。Yazi 官方通常会提供一个 `musl` 版本的二进制包。`musl` 版本将所有依赖库都打包进了二进制文件，**不依赖系统的 GLIBC 版本**，几乎可以在任何 Linux 发行版上运行。
   - `yazi-x86_64-unknown-linux-musl.zip`

3. 解压并将二进制文件移动到你的路径中：

   ```bash
   unzip yazi-x86_64-unknown-linux-gnu.zip
   cd yazi-x86_64-unknown-linux-gnu
   # 移动到 /usr/local/bin 即可在全局使用
   sudo cp yazi ya /usr/local/bin/
   ```

## Yazi 使用工作流

无论用哪种方式安装，Yazi 的核心体验依赖于一些外部工具。如果你的系统缺少这些，Yazi 运行起来可能“不好用”。建议顺手装上：

- **fd**: 用于快速搜索文件名。
- **ripgrep (rg)**: 用于搜索文件内容。
- **fzf**: 用于模糊找回。
- **zoxide**: 用于目录快速跳转。

```bash
# Ubuntu/Debian
sudo apt install fd-find ripgrep fzf zoxide
```

这套工具的核心逻辑是：**用 Yazi 作为中心枢纽，通过 fd/rg/zoxide 提供极速的搜索和跳转能力。**

1. Zoxide：瞬间移动 (The "Teleport")

   `zoxide` 是 `cd` 的增强版。它会学习你的习惯，你不需要输入完整路径，只需输入文件夹名字的一部分。
   - **工作流：** 1. 你在终端想去 `/home/user/projects/my-awesome-app`。 2. 只需输入 `z app`。 3. 它会自动匹配你访问频率最高且包含 "app" 的路径并跳转。
   - **与 Yazi 结合**：在 Yazi 中，按 **`z`** 键，会弹出一个交互式搜索框，你可以直接搜索并跳转到你常去的目录，无需逐层退出。

2. fd & ripgrep：定位目标 (The "Scouts")

   这两个工具是目前最快的搜索工具，Yazi 默认在后台使用它们。
   - **fd (找文件)**：
     - **工作流：** 比如你想找项目里所有的 `.json` 文件，终端输入 `fd json`。
     - **在 Yazi 中：** 按 **`C`** (大写) 可以进入筛选模式，Yazi 会实时调用 `fd` 帮你过滤当前目录下的文件。
   - **ripgrep (找内容)**：
     - **工作流：** 你想知道哪个文件写了 "TODO: fix bug"，终端输入 `rg "TODO"`。
     - **在 Yazi 中：** 按 **`s`** 键，可以直接在当前目录下进行全局内容搜索（grep），搜索结果会实时列出。

3. fzf：模糊选择 (The "Filter")

   `fzf` 像是一个过滤器，把杂乱的列表变得可以搜索。
   - **工作流：** 比如你在终端输入 `kill -9` 然后按 `Tab`，`fzf` 会列出所有进程让你搜索后关闭（取决于你的 Shell 配置）。
     - 或者输入 `CTRL-r`，模糊搜索你的历史命令。
   - **在 Yazi 中：** 很多插件（如 `yazi-fzf`）允许你按一个键，调起 `fzf` 搜索全盘文件，选中后 Yazi 会立即跳转过去。

4. 推荐的“丝滑”工作流示例

   想象你正在处理一个大型前端项目，你要修改 `UserCard.vue` 里的样式：
   1. **启动**：在终端输入 `z user` (zoxide) 瞬间跳到项目目录。
   2. **进入**：输入 `yazi` 或在 Neovim 里按 `<leader>-` 唤起 Yazi。
   3. **定位**：
      - 如果你知道文件名：在 Yazi 里按 <kbd>/</kbd> 输入 `User`，光标会自动锁定文件。
      - 如果你只记得里面有段代码叫 "border-red"：在 Yazi 里按 **`s`** 输入 `border-red` (ripgrep)，直接定位到那一行。
   4. **预览**：按 `l` 或 `右方向键` 预览文件内容。
   5. **操作**：按 `Enter`。由于你配置了 `yazi.nvim`，这个文件会**直接在你的 Neovim 编辑器里打开**。
   6. **跳转回目录**：按 `<leader>-` 再次唤起 Yazi，此时它会自动定位在 `UserCard.vue` 所在的文件夹，方便你寻找旁边的 `UserCard.test.js`。

5. 如何让它们在 Yazi 里更好用？

   Yazi 是高度可定制的。你可以通过修改 `~/.config/yazi/yazi.toml`（如果没有就创建一个）来强化它：

   > **提示：** Yazi 的默认快捷键非常直观：
   >
   > - `g` + `h`: 回家 (Home)
   > - `g` + `d`: 去下载 (Downloads)
   > - `g` + `p`: 去项目 (Projects - 需要自定)
   > - `f`: 调起 `fd` 搜索文件名

总结：你的“超级工具箱”配置图

| **工具**    | **角色** | **相当于**  | **在 Yazi 里的按键** |
| ----------- | -------- | ----------- | -------------------- |
| **zoxide**  | 导航员   | 智能 `cd`   | `z`                  |
| **fd**      | 侦查员   | 极速 `find` | `/` 或 `f`           |
| **ripgrep** | 搜索员   | 极速 `grep` | `s`                  |
| **fzf**     | 筛选员   | 模糊选择器  | 插件支持或 `CTRL-r`  |
