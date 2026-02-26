[toc]

# LazyVim 安装

GitHub 地址：<https://github.com/LazyVim/LazyVim/blob/main/README-CN.md>

GitHub 文档：<https://www.lazyvim.org/>

LazyVim 是一个基于 [💤 lazy.nvim](https://github.com/folke/lazy.nvim) 的 Neovim 配置方案，让定制和扩展变得简单直观。 您不必再在“从零配置”和“使用预制发行版”之间做选择，LazyVim 提供了一个两全其美的方式——既可以享受默认配置带来的便利，又能根据个人需求来灵活调整各项设置。

## LazyVim 和 lazy.nvim

以下是 **`lazy.nvim`** 和 **`LazyVim`** 的核心区别：

**一、`lazy.nvim`：插件管理器**

- **作用**：只是一个用于管理和懒加载 Neovim 插件的工具，相当于 `packer.nvim`、`vim-plug` 的替代品，但更现代化、高性能。
- **GitHub 地址**：<https://github.com/folke/lazy.nvim>
- **作者**：@folke（也是 LazyVim 的作者）
- **特性**：
  - 超快的启动时间（支持懒加载、缓存分析等）。
  - 配置插件方式模块化、声明式。
  - 提供 UI 显示插件加载状态。
  - 不带任何 Neovim 配置，只是个插件加载器。

> 简单来说，`lazy.nvim` 就是一个「插件安装 + 加载系统」，不干涉你怎么配置 Neovim，只负责**怎么加载插件**。

**二、`LazyVim`：完整 Neovim 配置框架**

- **作用**：一个预配置的、模块化的 Neovim 配置集合，使用 `lazy.nvim` 作为插件管理器，提供了完整的编辑体验。
- **GitHub 地址**：<https://github.com/LazyVim/LazyVim>
- **作者**：同样是 @folke
- **特性**：
  - 内置了 LSP、自动补全、代码高亮、Git 支持等功能。
  - 采用 `lazy.nvim` 来加载插件。
  - 可通过 `~/.config/nvim/lua/plugins/*.lua` 扩展自己的插件。
  - 适合想用 Neovim 但不想从零配置的人。

> 简单来说，`LazyVim` 是一个基于 `lazy.nvim` 的「现代 Neovim 配置框架」，帮你把整个开发环境都搭好了。

**二、总结**

| 项目        | 类型       | 是否包含 Neovim 配置 | 是否包含插件 | 面向用户            | 它提供什么？                                |
| ----------- | ---------- | -------------------- | ------------ | ------------------- | ------------------------------------------- |
| `lazy.nvim` | 插件管理器 | ❌                   | ❌           | 插件作者 / 高级用户 | 装/更新/懒加载插件                          |
| `LazyVim`   | 配置框架   | ✅                   | ✅           | 普通用户 / 开发者   | 提供全套配置（LSP、UI、插件集成、快捷键等） |

如果你已经在手动配置 Neovim，可以**单独使用 `lazy.nvim`** 来管理插件；
如果你想要一个**现成可用、可拓展的 Neovim 环境**，可以选择 **LazyVim**。

## 安装

[Installation](https://www.lazyvim.org/installation)

## 图标/字体乱码

注意，需要修改 terminal 的字体为 nerdfonts 中才不会出现乱码。

Nerd Fonts 字体下载：<https://www.nerdfonts.com/#home>
个人推荐：

- `CommitMono Nerd Font`：
  - Info: An anonymous and neutral programming typeface
  - `0, g` 等字符格式比较喜欢，整体无槽点
- `FiraCode Nerd Font`：
  - Info: Programming ligatures, extension of Fira Mono font, enlarged operators
  - `0, g` 等字符格式比较规整，但是不喜欢连起来的判等号
- `FiraMono Nerd Font`：
  - Info: Mozilla typeface, dotted zero
  - `0, g` 等 字符差点意思，整体挺好

- **Windows 安装字体**：所有字体都存储在 `C:\Windows\Fonts` 文件夹中。只需将字体文件从提取的文件文件夹拖动到此文件夹中即可添加字体。

## 启用额外插件

LazyVim 除了预装了很多插件，还有一些默认不启用的插件，称为 `Lazy Extras`。可以在启动页按 x 进入该插件库。
注：建议安装带 `recommended` 的插件。

# LazyVim 介绍

## LazyVim 加载顺序

在 LazyVim 中，理解配置文件的加载顺序是掌握这款配置框架的关键。由于 LazyVim 深度依赖 `lazy.nvim` 的懒加载机制，文件的加载顺序直接决定了你的配置是否能生效（或者是否会被插件覆盖）。

**一、配置文件作用与加载顺序**

LazyVim 的启动流程是严格定义的，按时间先后顺序如下：

| **顺序** | **配置文件**              | **作用说明**                                                                                                                                                          |
| -------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**    | `lua/config/options.lua`  | **最先加载**。用于设置全局变量（如 `mapleader`）和 Neovim 内置选项（如 `relativenumber`）。此时插件系统还没启动。                                                     |
| **2**    | `lua/config/lazy.lua`     | **插件系统的引擎**。负责初始化 `lazy.nvim`，并定义哪些目录（通常是 `lua/plugins`）会被扫描。                                                                          |
| **3**    | `lua/plugins/*.lua`       | **插件规格加载**。`lazy.nvim` 开始扫描插件文件夹，合并你自定义的 `opts`、`keys` 等。注意：此时只是“注册”插件，不一定会立即“执行”插件代码（除非设置了 `lazy=false`）。 |
| **4**    | `lua/config/keymaps.lua`  | **通用快捷键**。在插件规格注册后加载。建议只放不依赖特定插件的快捷键（如窗口切换、文字移动）。                                                                        |
| **5**    | `lua/config/autocmds.lua` | **通用自动命令**。最后加载的通用配置。适合放一些简单的 Neovim 原生事件监听。                                                                                          |

- 有时 `autocmds.lua` 命令会无效的原因：

  因为 `autocmds.lua` 加载时，`persistence.nvim` 插件虽然被“注册”了，但它往往是按需加载的。如果在自动命令执行时，插件的 `require` 路径还没被加入 runtimepath，或者插件还没完成 `setup`，调用就会报错或无效。

**二、插件配置的最佳组织方式**

为了避免顺序导致的冲突，最合理的组织方式是 **“功能高内聚”**：将插件的安装、配置、快捷键、以及与之相关的自动命令**全部封装在 `lua/plugins/` 下的一个独立文件中**。

推荐的目录结构：

```log
lua/
├── config/
│   ├── options.lua    -- 只放基础设置 (shiftwidth, leader key)
│   ├── keymaps.lua    -- 只放全局快捷键 (jk 映射, 窗口跳转)
│   └── autocmds.lua   -- 只放全局自动命令 (高亮复制内容)
└── plugins/
    ├── ui.lua         -- 组织 UI 相关插件 (bufferline, lualine)
    ├── editor.lua     -- 组织编辑器功能 (neo-tree, flash.nvim)
    └── session.lua    -- 组织会话管理 (persistence + 你的自动恢复逻辑)
```

**三、组织建议总结**

1. **解耦**：如果配置不依赖插件（如：`set number`），放 `config/options.lua`。
2. **联动**：如果配置强依赖插件（如：你的自动恢复逻辑），放 `plugins/` 对应插件的 `config` 或 `init` 函数里。
3. **原子化**：尽量一个文件负责一个功能模块。比如 `ui.lua` 负责界面，`lsp.lua` 负责语言支持。

[LazyVim configuration and demo](https://www.youtube.com/watch?v=N93cTbtLCIM)

这个视频展示了 LazyVim 的基础安装和文件组织方式，能帮你更直观地理解 `config` 与 `plugins` 文件夹在实际开发中是如何配合的。

- **`config/` 目录**：用于配置 Neovim 内置行为（比如按键、基础选项、全局自动命令）。
- **`plugins/` 目录**：用于配置依赖于特定插件的行为。

## 加载时序的冲突

打开上次 buffer，文件不显示 git 状态，这是 **LazyVim 的懒加载机制（Lazy Loading）与会话恢复（Session Restore）之间的时序冲突**。

在 LazyVim 中，Git 相关插件（如 `gitsigns`）通常被设置为 `event = "LazyFile"` 或 `event = "BufReadPost"` 触发。

1. **时序问题**：当你通过 `persistence.load()` 恢复会话时，它会瞬间打开多个文件（Buffers）。
2. **事件漏掉**：在某些情况下，由于会话恢复是在 `VimEnter` 瞬间完成的，`gitsigns` 插件可能还没来得及捕获到这些 Buffers 的打开事件，或者它的初始化逻辑在会话加载之后才完成，导致它没有为这些恢复的文件开启 Git 追踪。
3. **Neo-tree 刷新**：Neo-tree 的 Git 状态依赖于底层的 Git 插件（如 `gitsigns` 或原生 git 指令）。如果底层没识别，侧边栏也就没有图标。

**解决方案**：手动触发一次刷新

我们可以在恢复会话后，通过代码强制让 Neovim 触发一次相关事件，或者手动调用一次刷新。请尝试修改 `lua/plugins/session.lua`：

```Lua
return {
  {
    "folke/persistence.nvim",
    event = "VimEnter",
    config = function(_, opts)
      local persistence = require("persistence")
      persistence.setup(opts)

      vim.api.nvim_create_autocmd("VimEnter", {
        group = vim.api.nvim_create_augroup("auto_restore_session", { clear = true }),
        callback = function()
          if vim.fn.argc() == 0 and not vim.g.started_with_stdin then
            -- 1. 恢复会话
            persistence.load()

            -- 2. 强制触发 BufReadPost 事件，确保 gitsigns 等插件开始工作
            vim.schedule(function()
              for _, buf in ipairs(vim.api.nvim_list_bufs()) do
                if vim.api.nvim_buf_is_valid(buf) then
                  vim.api.nvim_exec_autocmds("BufReadPost", { buffer = buf })
                end
              end
            end)
          end
        end,
      })
    end,
  },
}
```

加上 `vim.schedule` 和 `BufReadPost` 的原因：

- **`vim.schedule`**：这会将任务推迟到 Neovim 主循环的下一帧。这样可以确保在执行刷新之前，所有的会话文件都已经真正加载到了内存中。
- **`BufReadPost`**：这是大多数 Git 插件启动的信号。我们遍历所有打开的窗口（Buffers），手动给它们发送这个信号，强迫 `gitsigns` 去检查这些文件的 Git 状态。

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

# 配置

## 配置文件

### `config/xx.lua`

通常情况下，配置文件路径：`~/.config/nvim/lua/config/xx.lua`，此目录用于配置 Neovim 内置行为（比如按键、基础选项、全局自动命令）。

**`~/.config/lua/config/options.lua`**

```Lua
-- 1. 启用系统剪贴板
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

### `plugins/xx.lua`

通常情况下，配置文件路径：`~/.config/nvim/lua/plugins/xx.lua`，此目录用于配置依赖于特定插件的行为。

**`~/.config/lua/plugins/ui.lua`**

```Lua
return {
  -- 1. 优化 Snacks.picker (处理长路径显示问题)
  {
    "folke/snacks.nvim",
    opts = {
      picker = {
        formatters = {
          file = {
            filename_first = true, -- 文件名在前，路径在后，解决长路径截断看不清文件名的问题
          },
        },
        sources = {
          buffers = {
            layout = { preset = "ivy" }, -- 使用底部全宽布局，给路径留出最大显示空间
            devicons = true,
          },
        },
      },
    },
    -- 覆盖 LazyVim 默认快捷键，确保调用我们配置好的 picker
    keys = {
      {
        "<leader>bb",
        function()
          Snacks.picker.buffers()
        end,
        desc = "Buffers (Snacks)",
      },
      {
        "<leader>,",
        function()
          Snacks.picker.buffers()
        end,
        desc = "Buffers (Snacks)",
      },
    },
  },

  {
    "RRethy/vim-illuminate",
    event = "VeryLazy",
    opts = {
      delay = 100,
      large_file_cutoff = 2000,
      large_file_overrides = nil,
      min_count_to_highlight = 2, -- 至少出现 2 次才高亮
      -- 直接使用 filetypes_denylist 就够了，删除 should_enable
      filetypes_denylist = {
        "dirvish",
        "fugitive",
        "alpha",
        "neo-tree",
        "Trouble",
        "lazy",
        "mason",
        "help",
        "dashboard",
        "TelescopePrompt",
      },
      under_cursor = true,
    },
    config = function(_, opts)
      require("illuminate").configure(opts)

      -- 使用更柔和的颜色，避免与 Visual 混淆
      -- 淡灰色背景 + 下划线，区别于 interestingwords 的彩色高亮
      vim.api.nvim_set_hl(0, "IlluminatedWordText", {
        bg = "#3a3a3a",
        underline = false,
      })
      vim.api.nvim_set_hl(0, "IlluminatedWordRead", {
        bg = "#3a3a3a",
        underline = false,
      })
      vim.api.nvim_set_hl(0, "IlluminatedWordWrite", {
        bg = "#4a4a4a",
        underline = false,
      })
    end,
  },


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
        if word == "" then
          return
        end

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

**`~/.config/lua/plugins/editor.lua`**

```Lua
return {
  {
    "nvim-treesitter/nvim-treesitter",
    version = "v0.9.2", -- 兼容 tree-sitter-cli 0.22.x
    build = ":TSUpdate",
    opts = function(_, opts)
      local install = require("nvim-treesitter.install")
      -- 1. 既然你的 git clone 通，强制用 git
      install.prefer_git = true
      -- 2. 既然没有能用的 CLI，强制用 gcc
      install.compilers = { "gcc" }
      -- 3. 核心：强制不使用外部 tree-sitter CLI
      install.use_native_parsers = false

      -- 确保基础语言在列表中
      opts.ensure_installed = opts.ensure_installed or {}
      vim.list_extend(opts.ensure_installed, { "cpp", "c", "lua", "vim", "vimdoc" })
    end,
  },

  -- 会话恢复后，Neo-tree 能够自动对齐到当前打开的文件
  {
    "nvim-neo-tree/neo-tree.nvim",
    opts = {
      filesystem = {
        -- 核心配置：让 Neo-tree 始终跟随当前编辑的文件
        follow_current_file = {
          enabled = true, -- 每次切换标签页，左侧目录树会自动展开并定位到该文件
          leave_dirs_open = true, -- 切换文件时保持之前打开的目录不折叠
        },
        -- 配合会话管理，确保重新打开时处于正确的 CWD
        bind_to_cwd = true,
      },
    },
  },

  {
    "ludovicchabant/vim-gutentags",
    event = "VeryLazy",
    config = function()
      -- 项目根目录标识
      vim.g.gutentags_project_root = { ".repo", ".git", ".svn", ".project" }

      -- tags 文件存放位置
      vim.g.gutentags_cache_dir = vim.fn.expand("~/.cache/nvim/tags")

      -- 启用 gtags 模块（可选，用于更强大的代码索引）
      vim.g.gutentags_modules = { "ctags" }

      -- ctags 参数
      vim.g.gutentags_ctags_extra_args = {
        "--fields=+niazS",
        "--extras=+q",
        "--c++-kinds=+px",
        "--c-kinds=+px",
        "--languages=C,C++", -- 只索引 C/C++ 文件
        "--exclude=.git",
        "--exclude=build",
        "--exclude=.cache",
      }

      -- 生成时机
      vim.g.gutentags_generate_on_new = 1 -- 打开新文件时生成
      vim.g.gutentags_generate_on_missing = 1 -- tags 文件不存在时生成
      vim.g.gutentags_generate_on_write = 1 -- 保存文件时更新
      vim.g.gutentags_generate_on_empty_buffer = 0 -- 空 buffer 不生成

      -- 在状态栏显示 gutentags 状态（可选）
      vim.g.gutentags_enabled = 1

      -- 调试选项（如果有问题可以开启）
      -- vim.g.gutentags_trace = 1
      -- vim.g.gutentags_define_advanced_commands = 1
    end,
  },
}

```

**`~/.config/lua/plugins/session.lua`**

```Lua
return {
  -- 进入项目且没有打开特定文件时，自动加载上次的标签页
  {
    "folke/persistence.nvim",
    event = "VimEnter", -- 进入 Vim 之后触发
    config = function(_, opts)
      local persistence = require("persistence")
      persistence.setup(opts)

      -- 在这里注册自动命令，此时插件环境已经 Ready
      vim.api.nvim_create_autocmd("VimEnter", {
        group = vim.api.nvim_create_augroup("auto_restore_session", { clear = true }),
        callback = function()
          -- 仅在直接输入 nvim (argc == 0) 且不是从管道读入数据时恢复
          if vim.fn.argc() == 0 and not vim.g.started_with_stdin then
            -- 1. 恢复文件标签页
            persistence.load()

            -- 2. 强制触发 BufReadPost 事件，确保 gitsigns 等插件开始工作
            vim.schedule(function()
              -- 解决 Git 状态不显示的问题
              for _, buf in ipairs(vim.api.nvim_list_bufs()) do
                if vim.api.nvim_buf_is_valid(buf) then
                  vim.api.nvim_exec_autocmds("BufReadPost", { buffer = buf })
                end
              end
            end)
          end
        end,
      })
    end,
  },
}

```

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

## neo-tree.nvim

### 回复上次文件状态

在 LazyVim 中，想要实现类似 VSCode 那样“再次打开项目时恢复上次的文件标签和目录树状态”，主要依靠 **Persistence.nvim**（LazyVim 默认已包含的会话管理器）和一些 **Neo-tree** 的配置。

1. 恢复文件标签（Session 恢复）

   LazyVim 默认集成了 `persistence.nvim`，它会自动保存你每个项目的会话。
   - **手动恢复：** 当你进入一个项目目录并打开 nvim 时，可以使用以下快捷键：
     - `<leader>qs`：恢复**当前目录**的上次会话（最常用，等同于 VSCode 恢复项目）。
     - `<leader>ql`：恢复**最后一次**使用的会话（不限目录）。
   - **自动恢复（进阶）：** 如果你希望每次打开 nvim 时**全自动**恢复上次的状态，而不需要按快捷键，可以在 `lua/config/options.lua` 或 `lua/plugins/` 下创建一个文件来配置。

2. 让 Neo-tree 记住路径和状态

   Neo-tree 默认可能在恢复会话后不会自动聚焦到上次的文件，或者显示不一致。你可以通过以下配置增强它的“记忆力”：

   在你的 `lua/plugins/example.lua`（或专门的 `neotree.lua`）中添加：

   ```Lua
   return {
     {
       "nvim-neo-tree/neo-tree.nvim",
       opts = {
         filesystem = {
           -- 核心配置：让 Neo-tree 始终跟随当前编辑的文件
           follow_current_file = {
             enabled = true, -- 每次切换标签页，左侧目录树会自动展开并定位到该文件
             leave_dirs_open = true, -- 切换文件时保持之前打开的目录不折叠
           },
           -- 配合会话管理，确保重新打开时处于正确的 CWD
           bind_to_cwd = true,
         },
       },
     },
   }
   ```

3. 实现“完全自动恢复”的终极配置

   如果你想彻底摆脱手动按 `<leader>qs`，可以添加一个自动命令。在 `lua/config/autocmds.lua` 中加入：

   ```Lua
   -- 只有在不带参数打开 nvim 时才自动恢复会话（防止 nvim filename 时也触发）
   vim.api.nvim_create_autocmd("VimEnter", {
     group = vim.api.nvim_create_augroup("restore_session", { clear = true }),
     callback = function()
       if vim.fn.argc() == 0 and not vim.g.started_with_stdin then
         require("persistence").load()
       end
     end,
     nested = true,
   })
   ```

**总结：**

- **文件标签：** 依靠 `persistence.nvim`。按 `<leader>qs` 即可找回所有 Tab。
- **侧边栏位置：** 在 Neo-tree 配置中开启 `follow_current_file`，这样只要文件恢复了，侧边栏会自动同步到对应的位置。

## bufferline.nvim

LazyVim 默认安装了 `bufferline.nvim`。它是 Bufferline 顶栏导航，相比于弹出搜索框，直接在顶部查看标签页通常更直观。

- **快捷键**：使用 `[b` 和 `]b` 在 buffer 之间快速左右切换。
- **点击**：如果你开启了鼠标支持，可以直接点击顶部的标签。
- 如果你觉得顶部标签也太长，可以配置 bufferline 的截断策略：

  ```Lua
  -- 在 bufferline 的 opts 中
  options = {
    mode = "buffers",
    max_name_length = 18,
    tab_size = 18,
  }
  ```

## snacks.nvim

你的直觉非常准确。**新版 LazyVim（v14.0+）确实已经不再默认使用 Telescope 了**。

作者 folke 对 LazyVim 进行了重大重构，现在默认的“全能插件”是 **`snacks.nvim`**。它内置了一个更轻量、速度更快的 **`Snacks.picker`**，用来替代原先 Telescope 的大部分功能（如文件搜索、Buffer 切换等）。

## blink.cmp

在最近的 LazyVim 版本更新中，默认的补全引擎已经从旧的 `nvim-cmp` 切换到了 **`blink.cmp`**。

`blink.cmp` 是一个用 Rust 编写的新一代补全插件，它的速度极快，且配置比 `nvim-cmp` 更简洁。LazyVim 官方认为它更稳定、性能更好，所以将其作为了默认选项。

**`blink.cmp` 默认操作逻辑如下：**

- **`Ctrl + n` / `Ctrl + p`**：在补全列表中上下移动。
- **`Enter` (回车)**：确认选择当前高亮的项目。
- **`Ctrl + y`**：也可以用来确认选择（有些老用户习惯这个）。
- **`Ctrl + Space`**：手动触发补全。
- **`Tab` 和 `Shift + Tab`**：
  - 在有补全菜单时：**选择**下一个/上一个建议。
  - 在没有补全菜单但在代码片段中时：**跳到**下一个/上一个占位符。

**自定义 blink.cmp 的按键：**

如果你想修改它的行为（例如想让补全菜单看起来更像 VS Code，或者修改 Tab 的逻辑），你需要修改 `blink.cmp` 的配置。

在 `~/.config/nvim/lua/plugins/` 下创建一个文件（比如 `blink.lua`）：

```Lua
return {
  "saghen/blink.cmp",
  opts = {
    keymap = {
      preset = "default", -- 或者使用 'super-tab' 预设

      -- 如果你想完全自定义，可以在这里覆盖
      -- ['<CR>'] = { 'accept', 'fallback' },
      -- ['<Tab>'] = { 'select_next', 'fallback' },
    },
    -- 你甚至可以开启补全框的边框
    completion = {
      menu = { border = "rounded" },
      documentation = { window = { border = "rounded" } },
    }
  },
}
```

确认补全是否生效：

1. 输入代码触发提示（比如输入 `tab` 或 `os.`）。
2. 使用 `Ctrl + n` 看到某个选项变色（被高亮）。
3. 直接按 **回车**。
4. 如果该项被填入代码中，说明补全成功。

# 终端文件管理器

NeoVim 集成终端文件管理器（尤其是 **Yazi**）可以极大地提升你的“终端体验”，它结合了 GUI 的直观和 CLI 的速度。

## 推荐原因

相比于默认的终端或 NeoTree，集成 `Yazi`/`Ranger` 的核心优势在于：

1. **极速导航与操作**：
   - NeoTree 是“侧边栏”，适合看结构；Yazi 是“全屏工作台”，适合**快速移动**。
   - 你不需要输入 `:cd long/path/to/dir`，只需按几个键就能飞速跳转（配合 `zoxide` 更是神器）。
2. **无缝集成（关键优势）**：
   - 如果你只是在普通终端运行 `yazi`，选中文件回车会用另一个 Vim 打开（导致嵌套）。
   - **LazyVim 集成版**：在 Yazi 中选中文件按下回车，它会**直接在当前的 Neovim 窗口中打开该文件**。这让它变成了一个超级强大的“文件选择器”。
3. **多媒体预览**：
   - Yazi 支持高清图片、视频缩略图、PDF 预览，这是 NeoTree 做不到的，也是普通终端 `ls` 做不到的。
4. **批量操作**：
   - 想把 10 个文件批量重命名？在 Yazi 中选中它们，按 `r`，它会调用你的编辑器（Neovim）让你一次性修改，保存即生效。

**最佳方案：推荐使用 Yazi**

虽然 Ranger 是经典，但在 Neovim 社区，**Yazi 是目前的绝对主流**。

- **Yazi**: Rust 编写（极快），原生支持异步（不卡顿），现代化的图片预览。
- **Ranger**: Python 编写，大文件夹下可能会卡顿，配置相对复杂。

## 在 LazyVim 中集成 Yazi

LazyVim 官方已经内置了对 Yazi 的完美支持（通过 `LazyExtras`），你不需要自己写复杂的配置。

1. 安装 Yazi (前提)

   你首先需要在你的系统终端里安装 Yazi 本体。
   - **MacOS**: `brew install yazi`
   - **Windows (Winget)**: `winget install sxyazi.yazi`
   - **Linux**: 请参考官方文档（通常是 `cargo install --locked yazi-fm` 或包管理器）。

2. 在 LazyVim 中启用

   LazyVim 提供了一个“开关”来开启这个功能。
   1. 在 Neovim 中输入命令：`:LazyExtras`
   2. 在列表中找到 **`util.yazi`**（通常在列表下方）。
   3. 按 **`x`** 键选中启用它。
   4. 按 **`q`** 退出，LazyVim 会自动安装 `mikavil/yazi.nvim` 插件。

3. 如何使用

   启用后，你的快捷键通常是：
   - **`<leader>-`** (Leader键 + 减号)：这是 LazyVim 为 Yazi 默认绑定的快捷键。

   **操作流程：**
   1. 按下 `<leader>-`，会弹出一个浮动的 Yazi 窗口。
   2. 像在终端一样浏览文件（使用 `h/j/k/l`）。
   3. 选中文件按 **Enter** -> **在当前 Neovim buffer 打开**。
   4. 选中文件按 **`<C-v>`** (Ctrl+v) -> **垂直分屏打开**。
   5. 选中文件按 **`<C-x>`** (Ctrl+x) -> **水平分屏打开**。

**总结建议**

| **工具**                  | **场景**                           | **评价**                                   |
| ------------------------- | ---------------------------------- | ------------------------------------------ |
| **Terminal (`<C-/>`)**    | 运行脚本、Git命令、编译            | 必须有，但**不适合找文件**。               |
| **NeoTree (`<leader>e`)** | 查看项目结构、新增/删除文件        | 直观，但键盘操作较慢。                     |
| **Yazi (`<leader>-`)**    | **极速找文件**、预览图片、批量操作 | **强烈推荐**，能替代 80% 的 NeoTree 场景。 |

## 注意

**一、yazi 安装方案（含离线）**

在 Linux 上，如果 `cargo install` 失败（通常是因为编译环境缺少依赖或内存不足），你可以直接根据你的发行版使用包管理器或直接下载编译好的二进制文件。

以下是除了 Cargo 之外最推荐的几种安装方式：

1. 使用系统包管理器 (最快)

   根据你使用的 Linux 发行版，执行对应的命令：

   ```bash
   # Arch Linux / Manjaro
   sudo pacman -S yazi

   # Fedora / RHEL / CentOS
   sudo dnf copr enable lihaohong/yazi
   udo dnf install yazi

   # Ubuntu / Debian / Linux Mint**: Yazi 目前在官方旧仓库可能没有，推荐使用第三方仓库或 Snap
   sudo snap install yazi --classic
   ```

2. 下载预编译二进制文件 (无需编译，成功率 100%)

   如果你不想处理复杂的依赖报错，直接从 GitHub 下载官方编译好的运行文件即可：
   1. 前往 [Yazi GitHub Releases](https://github.com/sxyazi/yazi/releases) 页面。

   2. 找到最新版本（Latest），下载符合你架构的文件，例如：
      - `yazi-x86_64-unknown-linux-gnu.zip` (大多数 PC 使用这个)
      - `yazi-aarch64-unknown-linux-gnu.zip` (ARM 架构如树莓派使用)

      &nbsp;
      如果安装后运行，**有 `GLIBC version not found` 相关的报错**，则说明系统版本的 `GLIBC` 版本和 yazi 需要的版本不匹配。
      可以选择 Yazi 官方通常都会提供的 `musl` 版本（静态链接版本）的二进制包。`musl` 版本将所有依赖库都打包进了二进制文件，**不依赖系统的 GLIBC 版本**，几乎可以在任何 Linux 发行版上运行。
      - `yazi-x86_64-unknown-linux-musl.zip` (静态链接版本 Musl)

      ```bash
      $ yazi -v
      yazi: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.39' not found (required by yazi)
      ```

   3. 解压并将二进制文件移动到你的路径中：

      ```bash
      unzip yazi-x86_64-unknown-linux-gnu.zip
      cd yazi-x86_64-unknown-linux-gnu
      # 移动到 /usr/local/bin 即可在全局使用
      sudo cp yazi ya /usr/local/bin/
      ```

3. 安装必要的运行时依赖 (解决报错的关键)

   无论用哪种方式安装，Yazi 的核心体验依赖于一些外部工具。如果你的系统缺少这些，Yazi 运行起来可能“不好用”。建议顺手装上：
   - **fd**: 用于快速搜索文件名。
   - **ripgrep (rg)**: 用于搜索文件内容。
   - **fzf**: 用于模糊找回。
   - **zoxide**: 用于目录快速跳转。

   ```bash
   # 安装示例 (Ubuntu/Debian)
   sudo apt install fd-find ripgrep fzf zoxide
   ```

**二、在 LazyVim 中集成 Yazi**

如果在 LazyVim 中找不到 `util.yazi`，原因通常有两点：

1. **LazyVim 版本较旧**：`util.yazi` 是较新版本中引入的 Extra。
2. **索引未更新**：有时候 `:LazyExtras` 的缓存列表没有及时刷新。

别担心，**手动集成 Yazi 插件**也非常简单，而且能让你获得更好的自定义空间。

1. 创建或打开文件： `~/.config/nvim/lua/plugins/yazi.lua`，将以下代码粘贴进去。

   ```lua
   return {
     {
       "mikavilpas/yazi.nvim",
       event = "VeryLazy",
       keys = {
         -- 在当前文件所在目录打开 Yazi
         {
           "<leader>-",
           function()
             require("yazi").yazi()
           end,
           desc = "Open yazi at the current file",
         },
         -- 在项目根目录打开 Yazi
         {
           "<leader>fy",
           function()
             require("yazi").yazi(nil, vim.fn.getcwd())
           end,
           desc = "Open yazi in project root",
         },
       },
       opts = {
         -- 如果你想让 Yazi 浮动窗口更漂亮，可以保持默认或自定义
         floating_window_styling = {
           border = "rounded",
         },
       },
     },
   }
   ```

   这段代码会自动下载插件，并设置好推荐的快捷键。

2. 重启并安装

   保存文件后，重启 Neovim。
   - 你会看到 `Lazy.nvim` 的界面弹出，自动下载并安装 `yazi.nvim`。
   - 安装完成后，按 **`<leader>-`** (空格 + 减号)。
