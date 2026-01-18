[toc]

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
    branch = "master",
    event = "VeryLazy",
    init = function()
      -- 使用 Ctrl 而不是默认的 \
      vim.g.VM_maps = {
        ["Find Under"] = "<C-d>", -- 选中当前单词并添加光标
        ["Find Subword Under"] = "<C-d>", -- 同上
        ["Select All"] = "<C-S-l>", -- 选中所有匹配项
        ["Skip Region"] = "<C-x>", -- 跳过当前匹配
        ["Remove Region"] = "<C-p>", -- 移除当前光标
        ["Add Cursor Down"] = "<C-Down>", -- 向下添加光标
        ["Add Cursor Up"] = "<C-Up>", -- 向上添加光标
      }

      -- 设置主题
      vim.g.VM_theme = "iceblue"

      -- 其他配置
      vim.g.VM_highlight_matches = "underline" -- 匹配项显示下划线
    end,
  },
}
```

使用方法：

- `<C-d>` - 选中光标下的单词，再次按下选中下一个相同单词
- `<C-x>` - 跳过当前匹配，继续下一个
- `<C-p>` - 取消最后一个光标
- `<C-Down>` / `<C-Up>` - 在上下行添加光标
- `<C-S-l>` - 选中所有匹配的单词
- `n` / `N` - 在多光标间导航
- `q` - 退出多光标模式
- 在多光标模式下，可以正常使用 `i`, `a`, `c`, `d` 等编辑命令

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
