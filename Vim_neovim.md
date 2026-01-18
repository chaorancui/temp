
# neovim

[2024 年 vim 的 C/C++ 配置](https://martins3.github.io/My-Linux-Config/docs/nvim.html) ---- 介绍了很多 vim 和 neovim 的基础和演进

[简单理解 Nvim 的 cmp 与 lsp](https://vatery.com/2023/09/02/%E7%AE%80%E5%8D%95%E7%90%86%E8%A7%A3Nvim%E7%9A%84cmp%E4%B8%8Elsp/) ---- 简单介绍 lsp 和 cmp

- LSP 管理器: `nvim-lspconfig`。nvim-lspconfig 它简化了 LSP 集成，支持多种编程语言的高级功能，如智能代码补全、实时错误检测等。
- cmp 代码补全引擎插件: `nvim-cmp`
- language server 管理器: `mason.nvim`

[在 Vim 和/或 Neovim](https://juejin.cn/post/7090094882588459045)

# windows 下使用 neovim

> [Neovim Github 仓库](https://github.com/neovim/neovim/tree/master) > [安装指南](https://github.com/neovim/neovim/blob/master/INSTALL.md)

## 安装与使用

Windows 下，安装与运行 Neovim 有 2 种方式：

1. 在终端中使用 nvim 命令启动 Neovim
2. 直接使用 Neovim 的 GUI 客户端

在终端命令行使用 Neovim，Neovim 的很多快捷键会和 windows 终端本身冲突，体验不佳。（可以寻找 windows 下配合 Neovim 好用的 terminal，暂时放弃）
而使用 Neovim 的 GUI 客户端，可以避免很多小问题，能在 Windows 上获得较好的 Neovim 使用体验。

### 终端命令使用 Neovim

1. 安装
   从 [Neovim](https://github.com/neovim/neovim) 的 [GitHub releases](https://github.com/neovim/neovim/releases) 页面下载适用于 Windows 的 Neovim 安装包，并安装到电脑上。如：nvim-win64.msi
2. 配置环境变量
   在 windows 左下角搜索框中输入“编辑系统环境变量”，在弹出的窗口中点击“环境变量”，找到“系统变量”中的“Path”变量，点击“编辑”，然后添加 Neovim 的 bin 目录路径。
   例如 bin 路径可能是：`C:\Program Files\Neovim\bin`，添加后便可以从命令行直接调用 nvim 命令启动 Neovim。
3. 启动 Noevim
   在 windows 终端中输入 nvim (不是 neovim)来启动 Neovim，终端可以使用 powershell 或者其他自己安装的终端，看个人喜好。

> windows 下也可以使用包管理工具 Chocolatey 或者 Scoop 安装 Neovim，需要首先在 windows 下安装这些包管理工具，然后再使用包管理工具安装 Neovim。后面一步可以参考官方文档 [INSTALL.md](https://github.com/neovim/neovim/blob/master/INSTALL.md)。

### neovim GUI 客户端

Neovim 为很多平台都提供了 GUI，可以参见 [GUIs](https://github.com/neovim/neovim/wiki/Related-projects#gui)。
Windows 系统下一些不错的 GUI 客户端有 [Neovim Qt](https://github.com/equalsraf/neovim-qt) 和 [FVim](https://github.com/yatli/fvim)（这两个都是跨平台 GUI）。

> 对比：
>
> - nvim-qt:
>   由 Neovim 官方团队维护，目标是提供一个简单且与 Neovim 终端版类似的 GUI 前端。
>   主要关注点在于尽量保持与 Neovim CLI 的一致性，同时提供基本的 GUI 功能（如字体渲染、剪贴板集成）。
>
> - fvim:
>   由社区开发者维护，目标是通过利用现代渲染技术提供更高性能和更好的视觉效果。
>   关注点在于提供更高性能的渲染、更流畅的界面交互以及丰富的视觉效果（如抗锯齿、透明度支持）。

1. 安装
   从 [Neovim Qt](https://github.com/equalsraf/neovim-qt) 或 [FVim](https://github.com/yatli/fvim) 的 GitHub releases 页面下载适用于 Windows 的 GUI 安装包，并安装到电脑上（或直接解压到安装目录）。如：neovim-qt-installer.msi 或 fvim-win-x64-v0.3.548+g2e4087d-2-gee4316c.zip
2. 创建桌面快捷方式
   便于打开 GUI 窗口。
3. 配置环境变量（可选）
   添加后可在终端中启动 GUI 窗口，避免每次都要在桌面打开。
   在 windows 左下角搜索框中输入“编辑系统环境变量”，在弹出的窗口中点击“环境变量”，找到“系统变量”中的“Path”变量，点击“编辑”，然后添加 GUI 可执行文件的目录路径。
   例如 bin 路径可能是：`C:\Program Files\neovim-qt 0.2.18\bin` 或 `D:\Program Files\fvim-win-x64-v0.3.548`。

## 配置

不同 vim 的默认配置文件：

- Linux 下的 vim：`~/.vimrc`
- Windows 下的 Neovim：`~/AppData/Local/nvim/init.vim`
  > 方法 1：打开 Neovim，输入 `:h init.vim` 查看 Neovim 的配置文件位置
  > 方法 2：打开 Neovim，输入 `:echo stdpath('config')` 查看
- Windows 下的 Neovim Qt、Fvim：`~/AppData/Local/nvim/ginit.vim`
- Windows 下的 Fvim 专用配置文件：`~/AppData/Local/fvim/fvim.vim`

> - Powershell 中查看环境变量 `$env:<ENV_Name>`，如查看 path 环境变量的值 `$env:path`
> - %LOCALAPPDATA% 为 ~/AppData/Local 文件夹。

### Neovim 使用系统剪切板

尽管 Neovim 的 Windows 版本通常已经包含对剪贴板的直接支持，但安装 win32yank 作为备选方案可以增加稳定性。**（可选）**

- 正常情况下，**Neovim 将使用 `+` 和 `*` 寄存器来访问系统剪贴板**。
- 设置 `clipboard=unnamedplus` 后，**普通的 y 和 p 命令也会自动使用系统剪贴板**。**<font color=red>（推荐）</font>**

> neovim 和系统剪贴板的交互方式和 vim 的机制是不同的，所以不要先入为主的用 vim 的方式使用 neovim。
> neovim 需要外部的程序与系统剪贴板进行交互，参考 `:help clipboard`
> 参考：[和系统剪贴板进行交互](https://wdd.js.org/vim/clipboard/)

1. 确保已安装支持剪贴板的 Neovim 版本
   首先，确保你安装的是支持剪贴板功能的 Neovim 版本。Windows 上的 Neovim 二进制文件通常已经内置了对剪贴板的支持。

   ```shell
   # 方式 1：打开Neovim，然后在命令模式下输入：
   :echo has('clipboard')
   # 如果返回 1，表示支持剪切板；如果返回 0，表示不支持。

   # 方式 2：PowerShell 中输入
   nvim --version
   # 输出若有 +clipboard 表示Neovim支持系统剪切板。-clipboard 表示不支持。
   ```

   > 方式 2 亲测不好用

2. 安装依赖：win32yank（可选）
   `win32yank` 是一个用来在 Windows 上与剪贴板交互的外部工具。尽管 Neovim 的 Windows 版本通常已经包含对剪贴板的直接支持，但**安装 win32yank 作为备选方案可以增加稳定性**。
   从 win32yank 的 [GitHub releases](https://github.com/equalsraf/win32yank/releases) 页面下载 win32yank.exe。
   将 win32yank.exe 复制到一个在 PATH 环境变量中的目录，例如 C:\Windows\System32。

3. 配置并使用 Neovim 系统剪贴板（推荐）
   打开或创建你的 Neovim 配置文件 `init.vim`，通常位于：`~/AppData/Local/nvim/init.vim`，在配置文件中添加以下设置：

   > 或者 `init.lua` 如果使用的是 Lua 配置。
   > 或者 `~/AppData/Local/nvim/ginit.vim` 如果使用的是 GUI。

   ```sql
   set clipboard=unnamedplus " 使用系统剪贴板
   ```

   Neovim 默认使用 `+` 和 `*` 寄存器来访问系统剪贴板。设置 `clipboard=unnamedplus` 后，**普通的 y 和 p 命令也会自动使用系统剪贴板（方便）**：

   - `"+y` 或 `y`：将 Neovim 选中文本复制到系统剪贴板。
   - `"+p` 或 `p`：从系统剪贴板粘贴文本到 Neovim。

4. 使用 win32yank 测试
   在 Neovim 中用如下命令测试 win32yank 是否正常工作：

   ```bash
   :echo system('echo hello | win32yank.exe -i')
   ```

   这会将字符串 hello 复制到剪贴板。如果成功，表示 win32yank 正常工作。

5. 常见问题与解决
   剪贴板不工作：确保你在 nvim --version 输出中看到了 +clipboard。如果没有，尝试更新 Neovim 或重新安装以获得最新的功能支持。
   win32yank 错误：确保 win32yank.exe 位于系统路径中（如 C:\Windows\System32），并且没有被防病毒软件拦截或删除。

## reference

【neovimBeginCpp | 看起来还行】：<https://github.com/jiaxinaoliao/neovimBeginCpp>
