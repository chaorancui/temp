[toc]

# LazyVim 技巧

## 替代 ESC 键

1. 经典双键组合：`jk` 或 `kj`

   这是 Vim 用户中最流行的配置。因为 `j` 和 `k` 就在右手食指和中指下面，快速连按这两个键几乎不需要移动手腕。
   - **配置方法：** 在 `~/.config/nvim/lua/config/keymaps.lua` 中添加：

   ```lua
   local keymap = vim.keymap

   -- 快速连按 jk 进入 Normal 模式
   keymap.set("i", "jk", "<Esc>", { desc = "Escape to Normal Mode" })
   -- 如果你也想在 Visual 模式下通过 jk 回到 Normal 模式
   -- keymap.set("v", "jk", "<Esc>", { desc = "Escape to Normal Mode" })
   ```

2. 使用 `Caps Lock` 映射为 `Esc` (推荐)

   这不仅是 LazyVim 的习惯，更是许多程序员的“终极方案”。将键盘上利用率极低的 **大写锁定键 (Caps Lock)** 在**系统层级**映射为 **Esc**。
   - **优点：** 离小指极近，且不占用任何输入字符，全局生效（所有软件都能用）。
   - **实现：**
     - **macOS:** 设置 -> 键盘 -> 修饰键。
     - **Windows:** 使用 PowerToys 或 SharpKeys。
     - **Linux:** 使用 `setxkbmap` 或 Tweaks 工具。

3. 系统原生快捷键：`Ctrl + [`

   这是 Vim 原生支持的映射，不需要任何额外配置。
   - **原理：** 在 ASCII 码中，`Ctrl + [` 等同于 `Esc`。
   - **优点：** 零配置，任何环境下（服务器上的 vi、远程 SSH 等）都有效。

总结建议：

- 如果你不想折腾系统设置：**选 `jk`**。
- 如果你追求最科学的键位：**将系统的 `Caps Lock` 改为 `Esc`**。
- 如果你经常需要远程登录各种服务器：**养成使用 `Ctrl + [` 的习惯**。

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

## 代码高亮

针对阅读时高亮（视觉辅助），下面的 lua 配置可以实现如下功能：**自动循环颜色、支持多单词高亮、一键清除**。

```lua
return {
  {
    "nvim-lua/plenary.nvim", -- 大部分 LazyVim 插件都依赖它，确保它存在
    config = function()
      -- 定义颜色池（Catppuccin 风格）
      local colors = {
        { bg = "#89b4fa", fg = "#11111b" }, -- Blue
        { bg = "#f38ba8", fg = "#11111b" }, -- Red
        { bg = "#a6e3a1", fg = "#11111b" }, -- Green
        { bg = "#f9e2af", fg = "#11111b" }, -- Yellow
        { bg = "#fab387", fg = "#11111b" }, -- Orange
        { bg = "#cba6f7", fg = "#11111b" }, -- Mauve
      }

      local current_color_idx = 1
      local word_match_ids = {} -- 存储单词到 match id 的映射

      -- 核心高亮函数
      local function toggle_word_highlight()
        local word = vim.fn.expand("<cword>")
        if word == "" then return end

        -- 如果该单词已经高亮，则取消它
        if word_match_ids[word] then
          vim.fn.matchdelete(word_match_ids[word])
          word_match_ids[word] = nil
          return
        end

        -- 获取下一个颜色
        local color = colors[current_color_idx]
        local group_name = "CustomWordHL" .. current_color_idx

        -- 定义高亮组
        vim.api.nvim_set_hl(0, group_name, { bg = color.bg, fg = color.fg, bold = true })

        -- 执行高亮匹配
        local match_id = vim.fn.matchadd(group_name, "\\<" .. word .. "\\>")
        word_match_ids[word] = match_id

        -- 循环索引
        current_color_idx = (current_color_idx % #colors) + 1
      end

      -- 清除所有高亮函数
      local function clear_all_highlights()
        for word, id in pairs(word_match_ids) do
          pcall(vim.fn.matchdelete, id)
        end
        word_match_ids = {}
        current_color_idx = 1
      end

      -- 绑定快捷键 (LazyVim 风格)
      vim.keymap.set("n", "<leader>hl", toggle_word_highlight, { desc = "Highlight Word (Cycle Color)" })
      vim.keymap.set("n", "<leader>hc", clear_all_highlights, { desc = "Clear All Highlights" })
    end,
  },
}
```

此方案：

1. **绝对稳定**：使用的是 Neovim 内置的 `matchadd` API，不依赖第三方不稳定的代码结构。
2. **逻辑透明**：
   - **`<leader>hl`**：自动取下一个颜色高亮单词。再次按同一个单词则取消高亮。
   - **`<leader>hc`**：瞬间清空所有手动标记的高亮。
3. **完全自洽**：你可以直接在 `colors` 列表里添加或修改你喜欢的 hex 颜色值。

## 批量编辑

对于批量修改，LazyVim 社区最推荐的是类似 VS Code 的**多光标 (Multi-cursor)** 体验，或者更具 Vim 哲学的 **`gn` 操作**。

**方案 A**：Vim 原生高亮 + `cgn` (推荐：最符合 LazyVim 逻辑)

这种方式不需要安装新插件，利用搜索高亮进行修改。

1. **高亮：** 光标移动到单词上，按 `*`。此时所有相同单词都会高亮。
2. **修改：** 输入 `cgn`。这会删除当前单词并进入插入模式。
3. **输入：** 输入新单词，按 `<Esc>` 退出。
4. **重复：** 按 `.` (点号)，Vim 会自动跳到下一个高亮的单词并应用同样的修改。
   - _优点：_ 你可以有选择性地跳过某个单词（按 `n` 跳过，按 `.` 修改）。

**方案 B**：vim-visual-multi（推荐）

这是最流行和功能最强大的 Neovim 多光标插件，类似 VSCode 的多光标体验。

```lua
return {
  {
    "mg979/vim-visual-multi",
  },
}
```

Github 地址：[mg979/vim-visual-multi](https://github.com/mg979/vim-visual-multi)

Basic usage:

- select words with Ctrl-N (like `Ctrl-d` in Sublime Text/VS Code)
- create cursors vertically with `Ctrl-Down/Ctrl-Up`
- select one character at a time with `Shift-Arrows`
- press `n/N` to get next/previous occurrence
- press `[/]` to select next/previous cursor
- press `q` to skip current and get next occurrence
- press `Q` to remove current cursor/selection
- start insert mode with `i,a,I,A`

Two main modes:

- in **cursor mode** commands work as they would in normal mode
- in **extend mode** commands work as they would in visual mode
- press Tab to switch between «cursor» and «extend» mode

Most vim commands work as expected (motions, r to replace characters, ~ to change case, etc). Additionally you can:

- run macros/ex/normal commands at cursors
- align cursors
- transpose selections
- add patterns with regex, or from visual mode

And more... of course, you can enter insert mode and autocomplete will work.

## 代码跳转：字符匹配

传统的 ctags 可以扫描生成 tag 以实现跳转，在 LazyVim 中，又可以使用 vim-gutentags 自动管理 tags。

vim-gutentags 安装后会自动工作，但让我详细说明如何使用和验证：

**一、基本使用**

1. 基本使用方法

   **vim-gutentags 会自动在后台生成 tags**，你不需要手动运行任何命令。当你：
   - 打开项目文件
   - 保存文件
   - 新建文件

   它都会自动更新 tags 文件。

2. 跳转快捷键

   一旦 tags 生成完成，使用以下命令跳转：

   **基本跳转：**
   - `<C-]>` - 跳转到光标下符号的定义
   - `g<C-]>` - 如果有多个定义，显示列表让你选择
   - `<C-t>` - 跳回上一个位置
   - `<C-o>` - 跳回历史位置（可以多次跳回）

   **使用 fzf-lua （LazyVim 新版默认）集成跳转（更友好）：**
   - `:FzfLua tags` - 搜索所有 tags
   - `:FzfLua btags` - 当前 buffer 的 tags

   **或者使用 snacks.nvim 的功能：**
   - `<leader>sg` " 全局搜索
   - `<leader>sw` " 搜索当前单词

3. 验证 vim-gutentags 是否工作

   ```vim
   " 检查 tags 文件是否生成：
   ls ~/.cache/nvim/tags/

   " 查看当前加载的 tags 文件：
   :set tags?

   " 在 Neovim 中查看状态：
   :GutentagsUpdate!     " 手动强制更新 tags
   :messages             " 查看是否有 gutentags 的消息
   ```

**二、优化配置**

如果你想更好地控制，可以修改配置 `~/.config/nvim/lua/plugins/editor.lua`：

```lua
return {
  "ludovicchabant/vim-gutentags",
  event = "VeryLazy",
  config = function()
    -- 项目根目录标识
    vim.g.gutentags_project_root = {'.repo', '.git', '.svn', '.project'}

    -- tags 文件存放位置
    vim.g.gutentags_cache_dir = vim.fn.expand('~/.cache/nvim/tags')

    -- 启用 gtags 模块（可选，用于更强大的代码索引）
    vim.g.gutentags_modules = {'ctags'}

    -- ctags 参数
    vim.g.gutentags_ctags_extra_args = {
      '--fields=+niazS',
      '--extras=+q',
      '--c++-kinds=+px',
      '--c-kinds=+px',
      '--languages=C,C++',  -- 只索引 C/C++ 文件
      '--exclude=.git',
      '--exclude=build',
      '--exclude=.cache',
    }

    -- 生成时机
    vim.g.gutentags_generate_on_new = 1      -- 打开新文件时生成
    vim.g.gutentags_generate_on_missing = 1  -- tags 文件不存在时生成
    vim.g.gutentags_generate_on_write = 1    -- 保存文件时更新
    vim.g.gutentags_generate_on_empty_buffer = 0  -- 空 buffer 不生成

    -- 在状态栏显示 gutentags 状态（可选）
    vim.g.gutentags_enabled = 1

    -- 调试选项（如果有问题可以开启）
    -- vim.g.gutentags_trace = 1
    -- vim.g.gutentags_define_advanced_commands = 1
  end,
}
```

**三、常见问题排查**

如果跳转不工作：

1. 确认 ctags 已安装及版本：

   ```bash
   # 检查 ctags 版本
   ctags --version

   # 应该看到 "Universal Ctags"
   # 如果是 "Exuberant Ctags" 就是旧版本，需要更新

   # 旧版本更新：
   sudo apt remove ctags
   sudo apt remove exuberant-ctags
   sudo apt install universal-ctags
   ```

2. 项目根目录未识别

   vim-gutentags 依赖项目根目录标识（`.repo`, `.git` 等）。检查你的配置：

   ```lua
   return {
     "ludovicchabant/vim-gutentags",
     event = "VeryLazy",
     config = function()
       -- 确保包含 .repo
       vim.g.gutentags_project_root = {'.repo', '.git'}
       vim.g.gutentags_cache_dir = vim.fn.expand('~/.cache/nvim/tags')

       ......

     end,
   }
   ```

3. tags 文件生成中或失败

   第一次生成 tags 需要时间，特别是大型项目。等待几分钟后再试。

vim-gutentags 最大的优势就是**全自动**，你只需要正常编辑代码，它会在后台默默工作，保持 tags 文件是最新的。

## 代码跳转：LSP

LazyVim 已经预设了一套非常高效且符合直觉的快捷键，你不需要进行任何额外配置，直接使用即可。

### 跳转函数定义快捷键

1. **核心跳转快捷键**

   这是最常用的操作，光标移动到函数名上直接按：
   - **`gd`**: (Go to Definition) **跳转到定义**。
   - **`gr`**: (Go to References) **查看引用**。LazyVim 会弹出一个 Telescope 窗口，列出所有调用该函数的地方。
   - **`gD`**: (Go to Declaration) 跳转到声明（在 C++/C 中较常用）。
   - **`gI`**: (Go to Implementation) 跳转到接口实现。

   跳转到定义后的返回：
   - 依靠 Vim 的 **跳转列表 (Jumplist)**，适用于所有跳转操作（包括 `gd`、搜索跳转、大跨度移动等）：
     - **`Ctrl + o`**: **后退**。回到跳转前的位置（"o" 可以理解为 "outer" 或 "old"）。
     - **`Ctrl + i`**: **前进**。如果你后退过头了，按这个键可以再次跳回到函数定义处。

   - LazyVim 增强快捷键
     - **`<leader>sl`**: (Search Location list) 如果你刚才通过 `gr` (References) 打开了一个引用列表，这个键可以帮你快速找回那个列表。
     - **`''` (双单引号)**: 跳回到上一次光标所在的行。
     - **`Ctrl + ^` (或者 `Ctrl + 6`)**: 在**当前文件**和**上一个打开的文件**之间快速切换。如果你跳转定义时跨越了文件，这个键非常高效。

2. **预览与分屏跳转**

   有时候你不想离开当前位置，只是想“偷看”一眼定义：
   - **`gw`**: (Go to Definition in Window) 在**当前窗口内预览**定义（如果安装了特定的预览插件）。
   - **`Ctrl-W + v` 后按 `gd`**: 在**垂直分屏**中打开定义。
   - **`Ctrl-o`**: **跳回**刚才的位置（这是 Vim 的通用后退键）。

3. **利用 snacks.nvim 搜索（更直观）**

   LazyVim 可以直接搜索符号，类似vscode搜索函数：
   - 输入 **`<leader>ss`**: 搜索当前文件中的符号（Symbols），可以直接输入函数名定位。
   - 输入 **`<leader>sS`**: 在整个工作区搜索符号。

   > **注意：**
   > 如果有类似 `Invalid node type "except*":` 的报错，可以尝试：
   >
   > - 删除 parser 缓存（根据自己安装路径删除）：`rm -rf ~/.local/share/nvim/site/parser`
   > - 重新打开 nvim，执行 `:TSInstall python`。

4. 如果跳转失效了怎么办

   LazyVim 是基于 LSP 的，如果 `gd` 没反应，通常是以下原因：
   1. **LSP 还没加载完**：观察右下角是否有进度条在跑。
   2. **未安装对应的语言服务器**：
      - 按下 **`<leader>cm`** (或输入 `:Mason`)。
      - 在打开的界面中找到你正在使用的语言（如 Python, Go, Rust），确保对应的 LSP 已安装。
   3. **插件冲突**：如果你自己修改过 `keymap.lua`，可能会覆盖 LazyVim 的默认设置。

   > **小贴士**：在 LazyVim 中，你可以随时按 **`zk`** (在某些配置下是 `K`) 来查看光标下函数的浮窗文档（Hover Doc），这通常比直接跳过去看源码更快。

### LSP 安装

在 LazyVim 中安装和管理 LSP 非常简单，因为它预装了 **Mason.nvim**（插件管理器）和 **nvim-lspconfig**（配置工具）。

你可以通过“手动可视化安装”或“配置文件自动安装”两种方式来实现。

**方法一：可视化界面安装（最简单、即时生效）**

这是最直观的方法，适合临时需要增加某种语言支持。

1. 在 Neovim 中按下快捷键：**`<leader>cm`** (或者输入命令 `:Mason`)。
2. 在打开的界面中，你会看到不同的分类。
3. 搜索与安装：
   - 输入 `/` 进入搜索模式，输入语言名称（如 `clangd` 或 `pyright`）。
   - 找到目标后，按下 **`i`** (Install) 进行安装。
4. 各语言推荐安装项：

   | **语言**    | **推荐 LSP 名称**           | **备注**                |
   | ----------- | --------------------------- | ----------------------- |
   | **C / C++** | `clangd`                    | 功能最强大的 C 家族 LSP |
   | **Python**  | `pyright` 或 `basedpyright` | 微软出品，速度极快      |
   | **Shell**   | `bash-language-server`      | 支持 bash/sh 脚本       |
   | **Lua**     | `lua-language-server`       | 写 Neovim 配置必备      |

**方法二：配置文件声明（推荐，跨设备同步）**

如果你想在换一台电脑后自动安装这些 LSP，应该在 LazyVim 的插件配置中进行“硬编码”。

在你的配置文件目录下（通常是 `~/.config/nvim/lua/plugins/`），创建一个新文件如 `lsp.lua`，并添加以下内容：

```lua
return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        -- 在这里列出你需要的 LSP
        clangd = {},    -- C/C++
        pyright = {},   -- Python
        bashls = {},    -- Shell
        marksman = {},  -- Markdown
      },
    },
  },
}
```

LazyVim 会在你下次打开时自动检测并调用 Mason 下载这些服务器。

**方法三：使用 LazyVim 的 "Extras"（全家桶模式）**

LazyVim 官方提供了一些预定义的“语言特性包”，不仅包含 LSP，还包括调试器（DAP）、代码格式化工具和语法高亮。

1. 输入命令：**`:LazyExtras`**。
2. 在弹出的列表中找到对应的语言：
   - `lang.clangd`
   - `lang.python`
   - `lang.typescript`
3. 按下 **`x`** 键开启该选项。它会自动帮你配好该语言相关的所有最佳插件。

### 常见问题排查

- **安装了但没生效？** 确保你系统里安装了对应的编译器。例如 `clangd` 需要系统有 `clang` 或 `gcc` 环境。
- **Shell 脚本报错？** `bashls` 通常依赖 `shellcheck`（静态检查）和 `shfmt`（格式化），建议在 Mason 界面里也把这两个装上。

**你想让我演示一下如何为 Python 或 C++ 配置特定的代码格式化规则（比如缩进长度或风格）**

## 代码缩进

在 LazyVim 中,默认已经配置了**代码折叠(folding)**功能:

1. 基本折叠命令

   **按级别折叠:**
   - `zM` - 折叠所有(关闭所有折叠)
   - `zR` - 展开所有(打开所有折叠)
   - `zm` - 增加折叠级别(折叠更多)
   - `zr` - 减少折叠级别(展开更多)

   **单个折叠操作:**
   - `za` - 切换当前折叠的开/关
   - `zo` - 打开当前折叠
   - `zc` - 关闭当前折叠
   - `zA` - 递归切换当前折叠
   - `zO` - 递归打开当前折叠
   - `zC` - 递归关闭当前折叠

2. 按级别折叠(类似 VSCode)

   如果你想要类似 `Ctrl+K Ctrl+1/2/3` 的效果:
   - `zM` 然后按 `zr` 1 次 ≈ 折叠到级别 1
   - `zM` 然后按 `zr` 2 次 ≈ 折叠到级别 2
   - `zM` 然后按 `zr` 3 次 ≈ 折叠到级别 3

   或者反向操作:
   - `zR` 然后按 `zm` N 次 - 从展开状态折叠到特定级别

3. 自定义快捷键

   如果你想要更直接的快捷键,可以在 LazyVim 配置中添加:

   ```lua
   -- 在 ~/.config/nvim/lua/config/keymaps.lua 中添加
   vim.keymap.set('n', '<leader>z1', 'zMzr', { desc = '折叠到级别1' })
   vim.keymap.set('n', '<leader>z2', 'zMzrzr', { desc = '折叠到级别2' })
   vim.keymap.set('n', '<leader>z3', 'zMzrzrzr', { desc = '折叠到级别3' })
   vim.keymap.set('n', '<leader>z0', 'zR', { desc = '展开所有' })
   ```

   这样你就可以用 `<leader>z1`、`<leader>z2`、`<leader>z3` 来快速折叠到不同级别了(LazyVim 中 `<leader>` 默认是空格键)。

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

## 查看寄存器内容

LazyVim 中，可以使用快捷键 `shift + "` 来查看寄存器中的内容。

## 切换下一个buffer

在 LazyVim 中，管理和切换 Buffer（缓冲区）是非常高频的操作。LazyVim 默认集成了一些非常直观的快捷键，主要围绕 `bufferline.nvim` 插件构建。

1. 基础切换（最常用）

   这是在打开的多个文件之间快速横跳的最快方式：
   - **`L`** (大写 L): 切换到 **下一个** Buffer。
   - **`H`** (大写 H): 切换到 **上一个** Buffer。
   - **`[b`**: 切换到上一个 Buffer（与 LazyVim 的统一导航逻辑一致）。
   - **`]b`**: 切换到下一个 Buffer。

2. 关闭与管理

   当你工作区塞满了临时文件时，这些命令非常管用：
   - **`<leader>bd`**: 关闭当前 Buffer（保持布局不变，不会像 `:q` 那样关闭窗口）。
   - **`<leader>bD`**: 强制关闭当前 Buffer。
   - **`<leader>bo`**: 关闭 **除此之外** 的所有 Buffer。
   - **`<leader>bP`**: 关闭左侧所有 Buffer。
   - **`<leader>bR`**: 关闭右侧所有 Buffer。

3. 列表与跳转

   如果你打开了十几个文件，挨个切换太慢，可以使用列表选择：
   - **`<leader>bb`**: 切换到 **最近使用** 的两个 Buffer 之间（反转跳转）。
   - **`<leader>fb`**: 打开 **Telescope** Buffer 列表，输入文件名快速搜索并跳转。
   - **`<leader>be`**: 打开 Buffer 浏览器（通常是 BufferLine 的管理界面）。

4. 窗口与 Buffer 的区别

   在 Vim 中，Buffer 是内存中的文件，Window 是显示 Buffer 的容器。如果你想在不同**窗口**间切换：
   - **`<ctrl-h/j/k/l>`**: 分别向 左/下/上/右 移动光标到另一个窗口。

小贴士：

- **数字跳转**：如果你在配置中开启了 `bufferline` 的数字显示，你可以通过 `<leader>bj` 后面接数字来跳转到指定位置的 Buffer。
- **鼠标支持**：LazyVim 默认支持鼠标，你也可以直接点击顶部的标签栏进行切换。

## 插入模式快捷键

在 LazyVim（以及绝大多数类 Vim 编辑器）的 Insert 模式下，快捷键和经典的 **Unix/Shell 快捷键习惯**一致，完全不需要切回 Normal 模式。

1. **光标移动**

   | 快捷键     | 作用             | Vim Insert | Bash/Zsh |
   | ---------- | ---------------- | ---------- | -------- |
   | `Ctrl + a` | 移动到行首       | ✔          | ✔        |
   | `Ctrl + e` | 移动到行尾       | ✔          | ✔        |
   | `Alt + b`  | 向前移动一个单词 | ✔          | ✔        |
   | `Alt + f`  | 向后移动一个单词 | ✔          | ✔        |
   | `Ctrl + b` | 左移一个字符     | ✔          | ✔        |
   | `Ctrl + f` | 右移一个字符     | ✔          | ✔        |

2. **删除操作（最常用）**

   | 快捷键     | 作用           | Vim Insert | Bash/Zsh |
   | ---------- | -------------- | ---------- | -------- |
   | `Ctrl + h` | 删除一个字符   | ✔          | ✔        |
   | `Ctrl + w` | 删除前一个单词 | ✔          | ✔        |
   | `Alt + d`  | 删除后一个单词 | ✔          | ✔        |
   | `Ctrl + u` | 删除到行首     | ✔          | ✔        |
   | `Ctrl + k` | 删除到行尾     | ✔          | ✔        |

3. **剪切 / 粘贴（Kill / Yank）**

   Unix 行编辑使用 **kill-ring** 概念：

   | 快捷键     | 作用           |
   | ---------- | -------------- |
   | `Ctrl + k` | 剪切到行尾     |
   | `Ctrl + u` | 剪切到行首     |
   | `Ctrl + w` | 剪切前一个单词 |
   | `Alt + d`  | 剪切一个单词   |
   | `Ctrl + y` | 粘贴           |

4. **历史命令**

   （主要在 shell）

   | 快捷键     | 作用       |
   | ---------- | ---------- |
   | `Ctrl + p` | 上一条命令 |
   | `Ctrl + n` | 下一条命令 |
   | `Ctrl + r` | 搜索历史   |
   | `Ctrl + g` | 退出搜索   |

5. **屏幕控制**

   | 快捷键     | 作用       |
   | ---------- | ---------- |
   | `Ctrl + l` | 清屏       |
   | `Ctrl + c` | 中断程序   |
   | `Ctrl + d` | EOF / 退出 |
   | `Ctrl + z` | 挂起进程   |

6. **Vim Insert 模式特有的补充**

   这些是 **Vim 独有的**：

   | 快捷键              | 作用                 |
   | ------------------- | -------------------- |
   | `Ctrl + o`          | 执行一次 Normal 命令 |
   | `Ctrl + n`          | 自动补全             |
   | `Ctrl + p`          | 自动补全（反向）     |
   | `Ctrl + x Ctrl + f` | 文件名补全           |

   例如：

   ```bash
   Ctrl+o dw
   ```

   执行 `dw` 删除一个单词，然后继续 Insert。

**一个很有趣的历史事实**

这些快捷键来自：**1970s Emacs 终端编辑习惯**，后来：

```bash
Emacs keybindings
      ↓
GNU Readline
      ↓
Bash / Zsh / REPL
      ↓
Vim Insert Mode
```

所以程序员会感觉：Linux terminal、shell、vim insert mode 手感几乎一样。

**在 Neovim 的逻辑里，插件定义的快捷键优先级通常高于 Vim 的原始行为。**

所以当某个快捷键不生效的时候，大概率是被插件拦截了，可以使用如下命令进行键位冲突检查：

```vim
:verbose imap <C-f> （查看 Insert 模式下的 Ctrl + f）
```

解决方案：在 `keymaps.lua` 中强行覆盖（最简单）

在 `~/.config/nvim/lua/config/keymaps.lua` 中添加以下代码。这会无视插件设置，强行把 `<C-f>` 还给“向右移动”：

```lua
local keymap = vim.keymap

-- 快速连按 jk 进入 Normal 模式
keymap.set("i", "jk", "<Esc>", {desc = "Escape to Normal Mode"})
-- 如果你也想在 Visual 模式下通过 jk 回到 Normal 模式
-- keymap.set("v", "jk", "<Esc>", { desc = "Escape to Normal Mode" })


-- ==========================================================================
-- Insert 模式：Unix/Shell 快捷键全家桶
-- ==========================================================================
-- 移动光标
keymap.set("i", "<C-a>", "<Home>", { desc = "移动到行首 (Beginning of line)" })
keymap.set("i", "<C-e>", "<End>", { desc = "移动到行尾 (End of line)" })
keymap.set("i", "<C-f>", "<Right>", { desc = "向右移动一个字符 (Forward)" })
keymap.set("i", "<C-b>", "<Left>", { desc = "向左移动一个字符 (Backward)" })

-- 删除操作
-- <C-h> 和 <C-w> Vim 默认已有，这里补充常用的：
keymap.set("i", "<C-d>", "<Del>", { desc = "向后删除一个字符 (Delete forward)" })
keymap.set("i", "<C-k>", "<C-o>D", { desc = "删除至行尾 (Kill to end of line)" })
keymap.set("i", "<C-u>", "<C-o>d0", { desc = "删除至行首 (Kill to beginning of line)" })

-- ==========================================================================
-- 单词级别移动 (类似 Alt+f, Alt+b)
-- 注意：有些终端需要配置 "Use Alt as Meta key" 才能生效
-- ==========================================================================
keymap.set("i", "<M-f>", "<S-Right>", { desc = "向右移动一个单词" })
keymap.set("i", "<M-b>", "<S-Left>", { desc = "向左移动一个单词" })

-- ==========================================================================
-- Command-line 模式：也配上同样的习惯
-- ==========================================================================
keymap.set("c", "<C-a>", "<Home>")
keymap.set("c", "<C-e>", "<End>")
keymap.set("c", "<C-f>", "<Right>")
keymap.set("c", "<C-b>", "<Left>")
keymap.set("c", "<C-d>", "<Del>")
```

## 搜索使用寄存器的值

在 LazyVim（以及几乎所有基于 Neovim/Vim 的编辑器）中，要在搜索模式（按下 `/` 或 `?` 后）使用寄存器中的内容，最直接、最地道的方法是使用快捷键 **`Ctrl + r`**。

1. **最常用的：插入指定寄存器的内容**

   当你已经按下 `/` 进入搜索模式后：
   - **操作：** 按下 `Ctrl + r`，然后紧接着按下 **寄存器名称**。
   - **常用寄存器：**
     - `"` ：无名寄存器（最后一次复制或删除的内容）。
     - `0` ：最后一次复制（yank）的内容。
     - `*` 或 `+` ：系统剪贴板的内容。
     - `/` ：上一次搜索的关键词。

   > **示例：** 如果你刚刚 `yw` 复制了一个单词，现在想搜它，只需输入 `/` 然后按 `Ctrl + r` 再按 `0`。

2. **插入当前光标下的单词**

   如果你懒得复制，想直接搜索光标所在的词：
   - **方法 A：** 在普通模式下直接按 `*`（向后搜）或 `#`（向前搜）。这是最快的。
   - **方法 B：** 在按下 `/` 进入搜索模式后，按下 `Ctrl + r` 然后按 `Ctrl + w`。这会将光标下的单词抓取到搜索栏中。

3. **处理特殊字符（原样搜索）**

   如果你寄存器里的内容包含 `*`、`[`、`.` 等正则表达式特殊字符，直接粘贴进去可能会匹配不到你想要的结果。
   - **技巧：** 在搜索框输入 `\V`（原样搜索模式，Very Magic 的反面）。
   - **组合动作：** `/` -> `\V` -> `Ctrl + r` -> `"`

总结表：

| **功能**                        | **快捷键 (在 / 模式下)**  |
| ------------------------------- | ------------------------- |
| **粘贴寄存器内容**              | `Ctrl + r` + `[寄存器名]` |
| **粘贴光标下的单词**            | `Ctrl + r` + `Ctrl + w`   |
| **粘贴光标下的长单词 (含标点)** | `Ctrl + r` + `Ctrl + a`   |
| **粘贴剪贴板内容**              | `Ctrl + r` + `+`          |

进阶小贴士：

如果你发现自己频繁需要搜索选中的文本，LazyVim 默认集成的插件通常已经支持在**可视模式 (Visual Mode)** 下直接按 `/` 来自动填充选中的内容。你可以尝试选中一段文字后直接按 `/` 看看是否生效。

## 快速转换大小写

在 LazyVim（以及原生 Neovim）中，转换大小写其实非常高效。因为 LazyVim 主要是基于键盘驱动的，掌握几个简单的快捷键就能让你告别手动删除再重打。

以下是几种最常用的方式：

1. **基础转换（常用）**

   这是最快捷的单键操作，适用于普通模式（Normal Mode）：
   - **`~` (波浪号)**：将光标下的字符**反转大小写**（大写变小写，小写变大写），并自动向后移动一个字符。
   - **`gu + 运动命令`**：将指定范围转换为**小写**。例如 `guw` 转换当前单词。
   - **`gU + 运动命令`**：将指定范围转换为**大写**。例如 `gUw` 转换当前单词。

2. **批量转换（可视化模式）**

   如果你想对一大块代码进行操作，先进入可视化模式（Visual Mode）：
   1. 按下 **`v`** 或 **`V`** 选中你想要的区域。
   2. 按下 **`u`**：选中的内容全部变为**小写**。
   3. 按下 **`U`**：选中的内容全部变为**大写**。
   4. 按下 **`~`**：选中的内容全部**反转大小写**。

3. **整行操作**

   如果你想快速处理一整行：
   - **`guu`**：将当前行全部变**小写**。
   - **`gUU`**：将当前行全部变**大写**。
   - **`g~~`**：将当前行大小写**反转**。

4. **进阶：快速处理当前单词**

   在实际写代码时，最常用的可能就是转换当前光标所在的单词：
   - **`gUiw`**：将光标所在的**整个单词**变大写（无论光标在单词开头还是中间）。
   - **`guiw`**：将光标所在的**整个单词**变小写。

> **小贴士**： 在 Vim 的逻辑中，`gU` 后面可以接任何“运动命令”。比如 `gUe` 转换到单词结尾，`gU$` 转换到行尾。
