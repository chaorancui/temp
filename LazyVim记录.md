[toc]

# LazyVim 介绍

## 插件管理机制

LazyVim 的插件管理机制虽然初看复杂，但其核心逻辑其实非常优雅。它主要基于一个叫 **`lazy.nvim`** 的插件管理器。

我们可以把这个机制拆解为：**扫描 -> 匹配 -> 合并** 三个步骤。

1. 自动扫描机制 (Scanning)

   在你的 `~/.config/nvim/lua/config/lazy.lua` 文件中，通常有这样一段代码：

   ```Lua
   require("lazy").setup({
     spec = {
       { "LazyVim/LazyVim", import = "lazyvim.plugins" }, -- 加载官方默认插件
       { import = "plugins" }, -- 加载你本地 lua/plugins 目录下的插件
     },
     -- ... 其他配置
   })
   ```

   - **`import = "plugins"`**：这就是“魔法”所在。它告诉 `lazy.nvim` 去扫描 `lua/plugins/` 目录下的所有 `.lua` 文件。
   - **不分文件名**：无论你起名叫 `treesitter.lua` 还是 `my_stuff.lua`，只要它在 `plugins` 文件夹里并返回一个表（table），它就会被加载。

2. 插件对应与识别 (Matching)

   插件与配置是如何对应起来的？关键在于你 `return` 的那个 **Table 的第一行**。

   当你写下：

   ```Lua
   return {
     {
       "nvim-treesitter/nvim-treesitter", -- 插件的 GitHub 仓库地址（这就是 ID）
       opts = { ... },                   -- 针对这个插件的配置
     },
   }
   ```

   `lazy.nvim` 会通过 **仓库短名 (`nvim-treesitter`)** 来识别这个配置属于哪个插件。

   - **官方已有的插件**：如果 LazyVim 官方已经定义了 `nvim-treesitter`，而你在自己的 `treesitter.lua` 里也写了 `nvim-treesitter`，`lazy.nvim` 会识别出这是**同一个插件**。
   - **新插件**：如果你写了一个官方没包含的地址（如 `"someone/my-new-plugin"`），它就会去下载并安装这个新插件。

3. 配置合并机制 (Merging)

   这是 LazyVim 最强大的地方。当你（用户）和 LazyVim（官方）同时配置同一个插件时，会发生**合并**：

   1. **加载官方配置**：LazyVim 预设了一套 `opts`（例如默认的高亮设置）。
   2. **查找用户覆盖**：它发现你在 `lua/plugins/treesitter.lua` 里也写了 `opts`。
   3. **合并/覆盖**：
      - 如果你在本地写了新的键值对，它会添加到官方配置中。
      - 如果你写了同名的键，你的配置会**覆盖**官方的配置。

4. 核心参数的含义

   在你的 `lua/plugins/*.lua` 文件中，常用的几个字段定义了配置的行为：

   | **字段**            | **作用**   | **对应关系**                                                               |
   | ------------------- | ---------- | -------------------------------------------------------------------------- |
   | **`"author/repo"`** | 插件 ID    | 决定了这个配置块“送给”哪个插件。                                           |
   | **`opts`**          | 传参       | 这是最常用的。它会将表里的内容传给插件的 `setup()` 函数。                  |
   | **`config`**        | 自定义逻辑 | 如果 `opts` 满足不了你（比如需要执行一段复杂的 Lua 代码），就用 `config`。 |
   | **`dependencies`**  | 依赖关系   | 告诉 LazyVim 在加载本插件前先加载哪些插件。                                |
   | **`keys`**          | 快捷键     | 只有当你按下这些键时，插件才会被激活（懒加载）。                           |

**Treesitter 为例：**

1. **LazyVim 官方说**：我们要安装 `nvim-treesitter`，并且 `ensure_installed` 默认有 `lua`。
2. **你在 `treesitter.lua` 里说**：我们要安装 `nvim-treesitter`，并且我要 `prefer_git = true`，还要增加 `cpp`。
3. **最终结果**：`lazy.nvim` 合并两者。它知道这是同一个插件（因为名字一样），最后生成的配置既包含了官方的 `lua`，也包含了你的 `cpp`，并且下载方式改成了 `git`。

**准则总结：**

- **想改已有插件**：新建一个 `.lua` 文件，在 `return` 的表里写上该插件的名字，然后通过 `opts` 修改它。
- **想加新插件**：新建一个 `.lua` 文件，写上新插件的 GitHub 地址。
- **想彻底禁用官方某个插件**：在你的配置里写上 `enabled = false`。

这样设计的好处是，你**永远不需要去修改 LazyVim 的核心源代码**，所有的个性化都在你自己的 `lua/plugins/` 目录下完成。

**管理准则：**

你可以根据**功能领域**来划分文件：

| **文件名**       | **存放内容**                                            |
| ---------------- | ------------------------------------------------------- |
| `treesitter.lua` | 语法高亮、解析器安装、代码缩进相关的配置。              |
| `lsp.lua`        | 语言服务器（Clangd, Pyright）、格式化、补全相关的配置。 |
| `ui.lua`         | 主题（Colorscheme）、状态栏、看板等外观配置。           |
| `editor.lua`     | 类似 `flash.nvim`、`telescope`、文件树等通用工具。      |

# LazyVim 技巧

## 快速上下移动整行代码

在 **LazyVim（Neovim）** 中，**快速上下移动整行代码** 是一个**高频且已经默认配置好的能力**。

**一、LazyVim 默认快捷键（最推荐）**

1. 普通模式（Normal Mode）

   ```bash
   Alt + j   → 当前行向下移动
   Alt + k   → 当前行向上移动
   ```

   - 不需要选中
   - 光标会跟着行一起移动
   - 相当于 VS Code 的 `Alt + ↑ / ↓`

   > 终端里通常是：
   >
   > - `Alt` = `Meta`
   > - 有些终端需要用 `Esc` 再按 `j / k`

2. 可视模式（Visual Mode，多行）

   ```bash
   选中多行 → Alt + j / Alt + k
   ```

   - 整块上下移动
   - 保持缩进
   - 非常适合调整代码块顺序

**二、如果 Alt 键在服务器终端不好用（很常见）**

很多服务器终端（尤其是 tmux / 某些 ssh 客户端）会**吞掉 Alt 键**。

1. 使用 Vim 原生方案（100% 可用）

   单行

   ```bash
   :move +1    " 下移一行
   :move -2    " 上移一行
   ```

   记忆规则：

   - `+1`：移动到“下一行后面”
   - `-2`：移动到“上一行前面”

   可视模式（多行，强烈推荐）

   ```bash
   选中 → :move '>+1
   选中 → :move '<-2
   ```

2. 剪切粘贴

   ```bash
   dd       " 剪切单行
   p        " 粘贴
   ```

**三、背后的实现原理（知道这个就不慌）**

LazyVim 实际用的是：

```bash
:m .+1
:m .-2
```

配合：

```bash
==
```

来重新缩进。

所以即便快捷键失效，你也**永远有兜底方案**。

## 快速复制一行或多行

```bash
yy          # 复制当前行
yyp         # 复制当前行到下一行（= 快速 duplicate）
yyP         # 复制当前行到上一行

3yy         # 复制当前行 + 向下 2 行

V       # 行选择
j/k     # 选中多行
y       # 复制
```

> :point_right: **这是 Vim 世界里最接近 VS Code「复制一行」的操作**。

## 注释 / 反注释

**一、LazyVim 默认注释快捷键（必记）**

LazyVim 默认集成的是 **Comment.nvim**。

1. 注释 / 反注释行

   ```bash
   gcc      # 当前行
   3gcc     # 当前行 + 向下 2 行

   # 选中多行
   V       # 行可视模式
   j / k   # 选中多行
   gc
   ```

   - 再按一次会取消注释
   - 自动根据语言选择 `# // /* */`

   等价于 VS Code 的 <kbd>Ctrl + /</kbd>

2. 注释到某个动作范围（理解后很强）

   ```bash
   gcj     # 注释当前行 + 下一行
   gck     # 当前 + 上一行
   gc}     # 注释到下一个空行
   ```

3. 块注释（语言支持时）

   ```bash
   gbc        # 当前行块注释
   V + gb
   ```

   > 是否用 `/* */` 取决于语言和 Treesitter。

四、常见使用场景速查

| 场景         | 操作               |
| ------------ | ------------------ |
| 注释当前行   | `gcc`              |
| 取消注释     | `gcc`              |
| 注释 5 行    | `5gcc`             |
| 注释选中多行 | `V` → 选中 → `gc`  |
| 块注释       | `gbc` / `V` → `gb` |

六、常见问题排查

1. 注释符号不对？

   检查：

   ```bash
   :set filetype?
   ```

   如果 filetype 错了，注释一定错。

2. `gcc` 没反应？

   可能原因：

   - 光标不在 Normal 模式
   - 插件未加载

   检查：

   ```bash
   :Lazy
   ```

   搜索 `Comment.nvim`。

# 配置

## SSH 时系统剪切板同步

在 SSH 远程连接的情况下，由于远程 Linux 和本地 Windows/Linux 不共享剪贴板，传统的 `y` 命令只能将内容复制到远程服务器的寄存器中。

可以通过**支持 OSC52 协议的终端**把远端 Neovim 复制的内容同步到本地剪切板。
**OSC52** 协议的原理是：Neovim 将要复制的内容转义为一段特殊的 Base64 字符串发送给终端，终端识别后将其写入本地系统的剪贴板。

要在 Windows + SSH + LazyVim 环境下实现这一功能，请按照以下三个步骤操作：

1. 确认终端支持

   首先，你需要确保你在 Windows 上使用的终端软件支持 OSC52。

   | 终端软件             | 是否支持 | 说明                     |
   | -------------------- | -------- | ------------------------ |
   | **Windows Terminal** | **支持** | 默认支持，建议使用。     |
   | **WezTerm**          | **支持** | 深度支持，体验极佳。     |
   | **PuTTY**            | 不支持   | 较老版本不支持，不推荐。 |
   | **MobaXterm**        | 部分支持 | 需要在设置中开启。       |

   > **注意**：传统的 `cmd.exe` 或旧版 `PowerShell` 窗口对 OSC52 支持极差。

2. 第二步：配置 LazyVim (Neovim)

   从 Neovim 0.10 版本开始，官方已经内置了对 OSC52 的原生支持，通常不需要额外插件。但为了确保在各种环境下（尤其是嵌套了 Tmux 时）都能稳定工作，我们可以通过 LazyVim 的配置来显式开启。
   在新版本（如：**v0.12.0-dev**）中，最标准、最干净的做法是在 `options.lua` 中进行配置。

   由于 LazyVim 默认会自动同步系统剪贴板（通常配置了 `vim.opt.clipboard = "unnamedplus"`），我们只需要告诉 Neovim 使用内置的 OSC52 处理器即可。

   编辑你的 `~/.config/nvim/lua/config/options.lua` 文件，在文件末尾添加以下代码：

   ```Lua
   -- 显式配置 OSC52 剪贴板后端
   vim.g.clipboard = {
     name = 'OSC 52',
     copy = {
       ['+'] = require('vim.ui.clipboard.osc52').copy('+'),
       ['*'] = require('vim.ui.clipboard.osc52').copy('*'),
     },
     paste = {
       ['+'] = require('vim.ui.clipboard.osc52').paste('+'),
       ['*'] = require('vim.ui.clipboard.osc52').paste('*'),
     },
   }

   -- 确保 LazyVim 使用系统剪贴板寄存器
   vim.opt.clipboard = "unnamedplus"
   ```

   > **注意**：如果你使用的是旧版 Neovim，建议安装插件 `ojroques/nvim-osc52`。但在 LazyVim 默认环境中，升级到最新的 Neovim 是最简单的解决方案。

3. 第三步：特殊场景处理 (Tmux)

   如果你是在 SSH 连过去后又开了 **Tmux**，OSC52 默认会被 Tmux 截断。你必须在 **远程 Linux** 的 `~/.tmux.conf` 中加入：

   ```Bash
   # 允许 Tmux 转发 OSC52 序列
   set -s set-clipboard on
   # 如果是较新版本，可能需要
   set -as terminal-features ',xterm-256color:clipboard'
   ```

   然后退出 Tmux 并重新进入，或者在 Tmux 内按下 `Prefix + :` 输入 `source-file ~/.tmux.conf`。

**验证功能：**

1. 重启你的 Neovim。
2. 进入 Visual 模式选中一段文字。
3. 按下 `y`（如果你在 LazyVim 中配置了同步剪贴板）或者在命令行输入 `:yank +`。
4. 尝试在 Windows 的记事本或浏览器中按 `Ctrl + V` 粘贴。

# 插件介绍

## flash.nvim

> ==> 快速跳转插件 <==

**LazyVim 默认使用的是 `flash.nvim`**。（不是 hop，不是 leap）

因为它是：

- 作者：**folke**（LazyVim 作者本人）
- 特点：
  - 非常快
  - 视觉提示清晰
  - 支持 Treesitter / LSP
  - 能替代大量传统跳转操作

**一、Flash.nvim 的核心使用方式（你必须掌握）**

Flash 的理念是：**“两次按键，跳到屏幕任意位置”**。

1. `s` —— 单字符跳转（最常用）

   ```bash
   s + 任意字符
   ```

   例：

   ```bash
   s f
   ```

   效果：

   - 屏幕上所有 `f` 都被高亮并标上字母
   - 再按提示字母，瞬间跳过去

2. 可视模式下的 `s`

   ```bash
   v → 选中 → s
   ```

   不是编辑，而是：

   - **在选中区域内跳转**
   - 用于精确定位修改点

**二、Flash 的进阶用法（这才是它的价值）**

1. `S` —— Treesitter 语义跳转（强烈推荐）

   ```bash
   S
   ```

   效果：

   - 跳转到：
     - 函数
     - if / for / while
     - class
   - **不需要输入字符**
   - 基于语法结构

   > :point_right: 对 **读代码 / 改代码** 非常有用。

2. `/` + Flash（搜索增强）

   ```bash
   /
   输入关键词
   回车
   ```

   LazyVim 会自动用 Flash 高亮所有匹配点
   你可以直接：

   ```bash
   输入提示字母跳转
   ```

3. 操作符 + Flash（这是高手用法）

   Flash **不是只能跳**，还能配合编辑：

   示例：删除到任意位置

   ```bash
   d s x
   ```

   解释：

   - `d`：delete
   - `s`：flash jump
   - `x`：跳到字符 x

   👉 删除光标到目标位置的内容。

   同理：

   ```bash
   c s f   # 改到 f
   y s }   # 复制到 }
   ```

**三、为什么 LazyVim 要“抢走” `s`**

这是一个**设计取舍**：

| 原生 Vim      | LazyVim       |
| ------------- | ------------- |
| `s`：低频修改 | `s`：高频跳转 |
| 修改靠 `c`    | 修改靠 `c`    |
| 跳转慢        | 跳转极快      |

LazyVim 的假设是：

> **你应该用 `c` 编辑，用 `s` 移动**

一旦接受这个分工，效率会明显提升。

**四、你现在应该怎么用（现实建议）**

如果你是 Vim / VS Code 迁移用户，建议：

- 不要用 `s` 来编辑，编辑一律用：

  ```bash
  c / cw / ciw / v + c
  ```

- 把 `s` 当作：**“超级 Ctrl + 鼠标点击”**

- 强烈推荐学习如下 3 个操作：

  ```bash
  s + 字符     # 精确跳
  S            # 语义跳
  d s + 字符   # 跳转式删除
  ```

## nvim-treesitter

**Requirements:**

- Neovim 0.11.0 or later (nightly)
- `tar` and `curl` in your path
- [`tree-sitter-cli`](https://github.com/tree-sitter/tree-sitter/blob/master/crates/cli/README.md) (0.26.1 or later)
- a C compiler in your path (see https://docs.rs/cc/latest/cc/#compile-time-requirements)

### Tree-sitter CLI

The Tree-sitter CLI allows you to develop, test, and use Tree-sitter grammars from the command line. It works on `MacOS`, `Linux`, and `Windows`.

Dependencies

The `tree-sitter` binary itself has no dependencies, but specific commands have dependencies that must be present at runtime:

- To generate a parser from a grammar, you must have [`node`](https://nodejs.org) on your PATH.
- To run and test parsers, you must have a C and C++ compiler on your system.

1. 使用 cargo 安装

   如果你有 Rust：

   ```bash
   cargo install tree-sitter-cli
   ```

   若 cargo 安装报错如下：

   ```bash
   error: failed to compile tree-sitter-cli v0.22.6, intermediate artifacts can be found at /tmp/cargo-installrHz7hW.
   To reuse those artifacts with a future compilation, set the environment variable CARGO_TARGET_DIR to that path.
   Caused by:
     package icu_properties_data v2.0.1 cannot be built because it requires rustc 1.82 or newer, while the currently active rustc version is 1.72.0
     Try re-running cargo install with --locked
   ```

   则原因为：Rust 版本太旧（1.72.0），需要 1.82+。**解决方案**：更新 Rust

   ```bash
   # 更新 Rust 到最新版本
   rustup update stable
   rustup default stable

   # 验证版本
   rustc --version

   # 然后重试安装
   cargo install tree-sitter-cli
   ```

2. 使用 npm 安装

   ```bash
   npm install -g tree-sitter-cli
   ```

   如果没有 npm，先安装 Node.js：

   ```bash
   # Ubuntu 22.04
   sudo apt update
   sudo apt install nodejs npm
   ```

   若 npm 安装卡住，可能是网络问题，npm 默认源在国外访问慢。**解决方案**：使用**国内镜像源**。如果是内网则需要使用**内网镜像源**。

   ```bash
   # 方法1：使用淘宝镜像
   npm install -g tree-sitter-cli --registry=https://registry.npmmirror.com

   # 或者永久设置镜像源
   npm config set registry https://registry.npmmirror.com
   npm install -g tree-sitter-cli
   ```

3. 直接下载预编译二进制

   ```bash
   # 下载最新版本
   curl -L https://github.com/tree-sitter/tree-sitter/releases/latest/download/tree-sitter-linux-x64.gz -o tree-sitter.gz

   # 解压
   gunzip tree-sitter.gz

   # 移动到可执行路径
   chmod +x tree-sitter
   sudo mv tree-sitter /usr/local/bin/
   ```

**验证安装**：

```bash
tree-sitter --version
```

### `:TSInstall cpp` 失败

安装后有如下日志，也没有单独报错：

```bash
[nvim-treesitter/install/c]: Downloading tree-sitter-c...
[nvim-treesitter/install/cpp]: Downloading tree-sitter-cpp...
[nvim-treesitter/install/c]: Compiling parser
[nvim-treesitter/install/cpp]: Compiling parser
[nvim-treesitter]: Installed 0/2 languages
```

排查：

1. **检查编译工具链**

   TreeSitter 需要 C/C++ 编译器。检查是否安装：
   TreeSitter 需要 git 来下载解析器，检查是否安装：

   ```bash
   # Linux/macOS
   gcc --version
   # 或
   clang --version

   # Windows (如果使用)
   gcc --version  # MinGW/MSYS2
   cl            # MSVC

   git --version
   ```

   如果没有，需要安装：

   - **Ubuntu/Debian**: `sudo apt install build-essential`
   - **Arch Linux**: `sudo pacman -S base-devel`
   - **macOS**: `xcode-select --install`
   - **Windows**: 安装 MinGW 或 MSYS2

2. **检查 nvim-treesitter 是否正确加载**

   ```vim
   :checkhealth nvim-treesitter
   ```

   这会显示 TreeSitter 的健康状态和可能的问题。若是如下状态，则是缺少 `tree-sitter-cli`，参考章节 [Tree-sitter CLI](#tree-sitter-cli) 安装。

   ```bash
   nvim-treesitter:                                                          1 ❌
   Requirements ~
   - ✅ OK Neovim was compiled with tree-sitter runtime ABI version 15 (required >=13).
   - ❌ ERROR tree-sitter-cli not found
   - ✅ OK tar 1.34.0 (/usr/bin/tar)
   - ✅ OK curl 7.81.0 (/usr/bin/curl)
   ```
