# vim

## vim 基本操作

> [Linux vi/vim](https://www.runoob.com/linux/linux-vim.html)
>
> [史上最全 Vim 快捷键键位图（入门到进阶）](https://www.runoob.com/w3cnote/all-vim-cheatsheat.html)

Vim 是从 vi 发展出来的一个文本编辑器。代码补全、编译及错误跳转等方便编程的功能特别丰富，在程序员中被广泛使用。

简单的来说， vi 是老式的字处理器，不过功能已经很齐全了，但是还是有可以进步的地方。 vim 则可以说是程序开发者的一项很好用的工具。

连 vim 的官方网站 (<https://www.vim.org/>) 自己也说 vim 是一个程序开发工具而不是文字处理软件。

![img](https://www.runoob.com/wp-content/uploads/2015/10/vi-vim-cheat-sheet-sch.gif)

### vi/vim 的使用

基本上 vi/vim 共分为三种模式，**命令模式（Command Mode）、输入模式（Insert Mode）和命令行模式（Command-Line Mode）**。

### 命令模式

**用户刚刚启动 vi/vim，便进入了命令模式。**

此状态下敲击键盘动作会被 Vim 识别为命令，而非输入字符，比如我们此时按下 **i**，并不会输入一个字符，**i** 被当作了一个命令。

以下是普通模式常用的几个命令：

- **i** -- 切换到输入模式，在光标当前位置开始输入文本。
- **x** -- 删除当前光标所在处的字符。
- **:** -- 切换到底线命令模式，以在最底一行输入命令。
- **a** -- 进入插入模式，在光标下一个位置开始输入文本。
- **o**：在当前行的下方插入一个新行，并进入插入模式。
- **u** -- 撤销上一次操作。
- **Ctrl + r** -- 重做上一次撤销的操作。
- **:w** -- 保存文件。
- **:q** -- 退出 Vim 编辑器。
- **:q!** -- 强制退出 Vim 编辑器，不保存修改。

若想要编辑文本，只需要启动 Vim，进入了命令模式，按下 **i** 切换到输入模式即可。

命令模式只有一些最基本的命令，因此仍要依靠**底线命令行模式**输入更多命令。

### 输入模式

在命令模式下按下 **i** 就进入了输入模式，使用 **Esc** 键可以返回到普通模式。

在输入模式中，可以使用以下按键：

- **字符按键以及 Shift 组合**，输入字符
- **ENTER**，回车键，换行
- **BACK SPACE**，退格键，删除光标前一个字符
- **DEL**，删除键，删除光标后一个字符
- **方向键**，在文本中移动光标
- **HOME**/**END**，移动光标到行首/行尾
- **Page Up**/**Page Down**，上/下翻页
- **Insert**，切换光标为输入/替换模式，光标将变成竖线/下划线
- **ESC**，退出输入模式，切换到命令模式

### 底线命令模式

在命令模式下按下 **:**（英文冒号）就进入了底线命令模式。

底线命令模式可以输入单个或多个字符的命令，可用的命令非常多。

在底线命令模式中，基本的命令有（已经省略了冒号）：

- `:w`：保存文件。
- `:q`：退出 Vim 编辑器。
- `:wq`：保存文件并退出 Vim 编辑器。
- `:q!`：强制退出 Vim 编辑器，不保存修改。

按 **ESC** 键可随时退出底线命令模式。

简单的说，我们可以将这三个模式想成底下的图标来表示：

![img](https://www.runoob.com/wp-content/uploads/2014/07/vim-vi-workmodel.png)

> 模式补充：
>
> Select Mode
> 选择模式。用鼠标拖选区域的时候，就进入了选择模式。和可视模式不同的是，在这个模式下，选择完了高亮区域后，敲任何按键就直接输入并替换选择的文本了。和 windows 下的编辑器选定编辑的效果一致。普通模式下，可以按 gh 进入。
>
> Command-Line/Ex Mode
> 命令行模式和 Ex 模式。两者略有不同，普通模式下按冒号(:)进入 Command-Line 模式，可以输入各种命令，
> 使用 vim 的各种强大功能。普通模式下按 Q 进入 Ex 模式，其实就是多行的 Command-Line 模式。

## vim 插件

### vim 插件管理

> [6 个最佳 Vim 插件管理器](https://www.linuxmi.com/vim-6-top-plugin-managers.html)
>
> [vim 有哪些插件管理程序？都有些什么特点？](https://blog.csdn.net/kunkliu/article/details/123577850)
>
> [Vim 插件应用篇 vim-plug：简洁高效的 Vim 插件管理工具](https://blog.csdn.net/Linux7985/article/details/132745874) --> vim-plug 主要操作介绍

vim 下的插件管理插件是非常多的，最为有名的要数 vundle(Vim bundle) 和 vim-plug。

对比如下：

- `vundle` 是一款老款的插件管理工具
- `vim-plug` 相对较新，特点是支持异步加载，相比 vundle 而言

vim-plug 优势：

- vim-plug 是一个轻量级且功能强大的插件管理器，**易于设置和使用**。所有配置和插件都列在一个文件中。它只有几个命令，因此您无需记住任何内容即可使用该工具。vim-plug 还支持一次并行安装和更新多个插件。最重要的是，它非常快。

  其他出色的功能包括按需加载、支持查看和回滚更新以及最小化磁盘空间使用。

  vim-plug 有**详细的文档**，如果您是 Vim 或插件管理器的新手，它非常适合。大多数 Vim 插件和插件管理器，包括 vim-plug，都有一个 [GitHub 页面](https://github.com/junegunn/vim-plug)来指导您完成安装。

总结：

如果你使用的是 vim8 的话，还是更为推荐 vim-plug，因为他已经支持 vim8 的 async process 特性了。

#### vim-plug

Vim-plug 的获取链接：<https://github.com/junegunn/vim-plug>

- 目录说明

  检查用户下是否有 `~/.vim` 文件夹

  ```bash
  mkdir ~/.vim
  cd ~/.vim
  mkdir plugged plugin syntax colors doc autoload（autoload文件夹也可在安装Vim-plug插件时创建）
  ```

  `~/.vim`文件夹下目录介绍

  | 目录               | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
  | :----------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | `~/.vim/autoload/` | 它是一个非常重要的目录，尽管听起来比实际复杂。简而言之，它里面放置的是当你真正需要的时候才被自动加载运行的文件，而不是在 vim 启动时就加载。                                                                                                                                                                                                                                                                                                                                |
  | `~/.vim/colors/`   | 是用来存放 vim 配色方案的。                                                                                                                                                                                                                                                                                                                                                                                                                                                |
  | `~/.vim/plugin/`   | 存放的是每次启动`vim`都会被运行一次的插件，也就是说只要你想在 vim 启动时就运行的插件就放在这个目录下。我们可以放从`vim-plug`官方下载下来的插件.vim                                                                                                                                                                                                                                                                                                                         |
  | `~/.vim/syntax/`   | 语法描述脚本。我们放有关文本（比如 c 语言）语法相关的插件                                                                                                                                                                                                                                                                                                                                                                                                                  |
  | `~/.vim/doc/`      | 为插件放置文档的地方。例如`:help`的时候可以用到。                                                                                                                                                                                                                                                                                                                                                                                                                          |
  | `~/.vim/ftdetect/` | 中的文件同样也会在 vim 启动时就运行。有些时候可能没有这个目录。ftdetect 代表的是“filetype detection（文件类型检测）”。此目录中的文件应该用自动命令（autocommands）来检测和设置文件的类型，除此之外并无其他。也就是说，它们只该有一两行而已。                                                                                                                                                                                                                               |
  | `~/.vim/ftplugin/` | 此目录中的文件有些不同。当`vim`给缓冲区的`filetype`设置一个值时，`vim`将会在`~/.vim/ftplugin/`目录下来查找和`filetype`相同名字的文件。例如你运行`set filetype=derp`这条命令后，vim 将查找`~/.vim/ftplugin/derp.vim`此文件，如果存在就运行它。不仅如此，它还会运行`ftplugin`下相同名字的子目录中的所有文件，如`~/.vim/ftplugin/derp/`这个文件夹下的文件都会被运行。每次启用时，应该为不同的文件类型设置局部缓冲选项，如果设置为全局缓冲选项的话，将会覆盖所有打开的缓冲区。 |
  | `~/.vim/indent/`   | 这里面的文件和`ftplugin`中的很像，它们也是根据它们的名字来加载的。它放置了相关文件类型的缩进。例如`python`应该怎么缩进，`java`应该怎么缩进等等。其实放在`ftplugin`中也可以，但单独列出来只是为了方便文件管理和理解。                                                                                                                                                                                                                                                       |
  | `~/.vim/compiler/` | 和 indent 很像，它放的是相应文件类型应该如何编译的选项。                                                                                                                                                                                                                                                                                                                                                                                                                   |
  | `~/.vim/after/`    | 这里面的文件也会在 vim 每次启动的时候加载，不过是等待`~/.vim/plugin/`加载完成之后才加载`after`里的内容，所以叫做`after`。                                                                                                                                                                                                                                                                                                                                                  |
  | `~/.vim/spell/`    | 拼写检查脚本。                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

- Vim-plug 的安装

  ```shell
  curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
      https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  ```

  > Note:
  >
  > 可能会遇到报错：`curl: (60) SSL certificate problem: self-signed certificate in certificate chain`
  >
  > 官网的解释是说因为证书认证缺失，所以可以考虑请求里面关闭 ssl 证书认证，命令行中加上-k 即可
  >
  > ```shell
  > curl -kfLo ~/.vim/autoload/plug.vim --create-dirs \
  >     https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim插件的添加和删除
  > ```

- 插件的添加和删除

  `vim-plug` 支持源码托管在 `GitHub` 的插件，你可以在`"https://github.com/vim-scripts/"`上找到 vim 官网(`https://www.vim.org`)里所有插件的镜像。也可以安装 Windows 版本的 Git 查看 vim 插件。

  要安装插件，你必须如下所示首先在 Vim 配置文件中声明它们。

  一般 Vim 的配置文件是 `~/.vimrc`，Neovim 的配置文件是 `~/.config/nvim/init.vim`。

  请记住，当你在配置文件中声明插件时，列表应该以 `call plug#begin(PLUGIN_DIRECTORY)` 开始，并以 `plug#end()` 结束。

  编辑 `~/.vimrc` 文件中的内容，比如安装`“lightline.vim”` 插件

  ```shell
  call plug#begin('~/.vim/plugged')
  "
  Plug 'tpope/vim-sensible'
  "
  " 目录树，可以支持在不退出vim的编辑器的前提下，在文件中快速切换，同时能让开发人员快速掌握项目目录结构
  Plug 'preservim/nerdtree'                                                                                                     "
  "
  Plug 'itchyny/lightline.vim'

  call plug#end()
  ```

  运行命令重新加载：

  ```bash
  :source ~/.vimrc
  ```

  安装、更新插件等：

  ```shell
  #### 安装插件
  # 找到插件 github 网址，追加至 vimrc 配置文件中的 `call plug#begin()` 和 `call plug#end()` 之间，执行下面命令安装所有引用的插件
  :PlugInstall
  # 注：插件网址添加方式如下：
  # 1.可用完整的地址：Plug 'https://github.com/用户名/项目名.git'
  # 2.可用简写形式：Plug 'github用户/项目名'

  # 指定安装特定的插件，可以使用以下命令：
  :PlugInstall gist-vim


  #### 卸载插件
  # 请先在vimrc配置文件中注释或者删除对应插件的配置信息，然后再执行以下命令：
  :PlugClean

  #### 更新 vim-plug 插件自身：
  :PlugUpgrade

  #### 查看当前已安装插件的状态信息
  :PlugStatus
  ```

  > Note:
  >
  > 因为每个插件配置均有不同，插件作者会在 Git 中添加插件配置方法，所以各个插件的配置方法请参考插件作者的使用说明！
  >
  > [VIM 插件网站](https://vimawesome.com/)

### vim 插件介绍

> 一个比较好的 vim 插件网站：[vimawesome](https://vimawesome.com/) > <font color=red>Note:</font>
>
> 下面的安装命令适用于 **vim-plug** 插件管理

#### NERDTree | 「[github](https://github.com/preservim/nerdtree)」

NERDTree 是 Vim 编辑器的文件系统浏览器。使用此插件，用户可以直观地浏览复杂的目录层次结构、快速打开文件进行读取或编辑，以及执行基本的文件系统操作。

![img](https://raw.githubusercontent.com/preservim/nerdtree/master/screenshot.png)

- 安装

  使用 vim-plug，`~/.vimrc` 中配置

  ```shell
  call plug#begin('~/.vim/plugged')
        Plug 'preservim/nerdtree'
  call plug#end()
  ```

- 使用

  12

#### lightline |「[github](https://github.com/itchyny/lightline.vim)」

适用于 Vim 的轻量且可配置的状态行/标签行插件

电力线（默认）

[![lightline.vim - 电力线](https://raw.githubusercontent.com/wiki/itchyny/lightline.vim/image/powerline.png)](https://raw.githubusercontent.com/wiki/itchyny/lightline.vim/image/powerline.png)

- [vim-powerline](https://github.com/Lokaltog/vim-powerline)是一个很好的插件，但已被弃用。
- [powerline](https://github.com/powerline/powerline)是一个很好的插件，但配置起来很困难。
- [vim-airline](https://github.com/vim-airline/vim-airline)是一款不错的插件，但是它使用了太多其他插件的功能，这些功能应该由用户来完成`.vimrc`。

如果您使用 wombat colorscheme，请将以下设置添加到您的`.vimrc`，

```
let g:lightline = {
      \ 'colorscheme': 'wombat',
      \ }
```

重新启动 Vim，状态行如下所示：

#### leaderF

LeaderF 现在基本是 Vim 最好的模糊查找插件. 参考

<https://github.com/Yggdroot/LeaderF>

<https://retzzz.github.io/dc9af5aa/>

#### YouCompleteMe

## vim 配置文件

> 参考：[Docs --> 第四章 常见问答 --> Vim 配置文件](https://vim80.readthedocs.io/zh/latest/faq/vimrc.html#id1)

基本配置文件，将上面 WIKI 中的 Vundle 换成了 vim-plug，同时自定义插件配置

```shell
set nocompatible              " be iMproved, required
" filetype off                  " required

" pass a path where vim-plug should install plugins
call plug#begin('~/.vim/plugged')
" The following are examples of different formats supported.
" Keep Plugin commands between plug#begin/end.
"
" plugin from https://github.com/tpope/vim-sensible
" 主要为 :set 调用，如：'backspace':在插入模式下按退格键可删除任何内容。
Plug 'tpope/vim-sensible'
"
" plugin from https://github.com/preservim/nerdtree
" 目录树，可以支持在不退出vim的编辑器的前提下，在文件中快速切换，同时能让开发人员快速掌握项目目录结构
Plug 'preservim/nerdtree'                                                                                                     "  "
" plugin from https://github.com/itchyny/lightline.vim
" 适用于 Vim 的轻量且可配置的状态行/标签行插件
Plug 'itchyny/lightline.vim'
"
"
"
" All of your Plugins must be added before the following line
call plug#end()

" basic
set number                      " 设定行号
set ruler      " 设定尺标以显示行列（经纬）信息
set clipboard=unnamed        " 设定操作系统剪切板和vim寄存器互通（默认不通）
set cursorline     " 设定光标所在行有行下划线
" set noswapfile                " 设定不会产生.swp文件
set wrap      " 设定开启文本过长折叠（默认开启）。使用"set nowrap"来关闭。
set linebreak     " 设定文本过长折叠时以一个word为基本unit，而不是字母。避免一个单词被分割在两行的情况。
set showmode     " 设定显示当前所处模式（默认开启）。使用"set noshowmode"来关闭，但是不建议关闭。
set showcmd      " 设定显示当前命令（默认开启）。使用"set noshowcmd"来关闭，但是不建议关闭。
set nolist      " 设定显示换行等默认隐藏的信息。使用"set nolist"来关闭。建议保持关闭。
set encoding=utf-8
" set autoindent

" search
set hlsearch     " 设定查找内容高亮
set ignorecase     " 设定查找时忽略大小写敏感
set smartcase     " 设定当目标词中存在大写时，暂时忽略ignorecase
set incsearch     " 设定渐进式查找（随着对目标单词输入时长度的增加，文档中会越来越精确的找到目标单词）

" tab and space
set softtabstop=2    " 设定在insert模式下tab键每次移动距离
set shiftwidth=2    " 设定在normal模式下">"或"<"键进行缩排调节的距离
set expandtab     " 设定将一个tab的距离软化成多个space

" tab page
set showtabline=2    " 设定标签页的显示情况（0为永不显示，1为至少存在两个才显示，2为一直显示）
set splitbelow     " 设定通过":new"水平开新视窗时在原视窗下面（默认为上面）
set splitright     " 设定通过":vnew"垂直开新视窗时在原视窗右侧（默认为左侧）

" color
syntax on      " 设定vim打开高亮，根据文件内容渲染颜色
" colorscheme darkblue   " 设定vim的主题颜色为darkblue（默认是default）

" filetype
filetype on      " 设定filetype功能打开
filetype indent on    " 设定filetype自动缩排
filetype plugin on    " 设定filetype基于文件后缀开启对应外挂插件


" 按键映射：重新定义窗口跳转快捷键
" nnoremap <C-J> <C-W><C-J>
" nnoremap <C-K> <C-W><C-K>
" nnoremap <C-H> <C-W><C-H>
" nnoremap <C-L> <C-W><C-L>

" 高亮不必要的空白字符
" highlight BadWhitespace ctermbg=red guibg=darkred
" au BufRead,BufNewFile *.py,*.pyw,*.rst,*.c,*.h match BadWhitespace /\s\+$/

" 插件设置：nerdtree
nnoremap <C-T> :NERDTreeToggle<CR>
let g:NERDTreeDirArrowExpandable = '+'
let g:NERDTreeDirArrowCollapsible = '-'
let NERDTreeWinPos='left'
let NERDTreeWinSize=20
```

> > [使用上古神器找回逝去的青春（四）：Vim 使用方法简介](https://blog.csdn.net/weixin_43394859/article/details/112296900)
>
> 可以在 vim 中输入":set"来查看当前所有自主设定
>
> 可以在 vim 中输入":set all"来查看所有的设定内容
>
> 若要罗列出 vim 所支持的所有主题，则可以使用如下命令实现：
>
> :colorscheme "Ctrl+d"

## vim 按键映射

> 参考：[vim map](https://vimcdoc.sourceforge.net/doc/map.html#:imap)

### 配置按键映射

Vim 强大的一个重要原因是它的高度可配置性。你可以自定义各种快捷键，让它用起来更符合自己的使用习惯从而更得心应手。

vim 里最基本的映射配置有 map、noremap、unmap、mapclear 几种。

|           |              |
| :-------- | ------------ |
| map:      | 递归的映射   |
| noremap:  | 非递归的映射 |
| unmap:    | 删除某个映射 |
| mapclear: | 清除某个映射 |

同 Vim 下的其他命令一样，map 命令的名字往往由好几段组成。在不同的模式下，同一组按键可以被映射到不同的组合上，前缀作为命令本身的修饰符，微调命令的效果。map 有以下几种前缀：

|     |                    |
| :-- | ------------------ |
| n:  | 在普通模式下生效   |
| v:  | 在可视模式下生效   |
| i:  | 在插入模式下生效   |
| c:  | 在命令行模式下生效 |

#### 递归和非递归的映射

递归的映射其实很好理解，也就是如果键 a 被映射成了 b，c 又被映射成了 a，如果映射是递归的，那么 c 就被映射成了 b。

```
:map a b
:map c a
```

对于 c 效果等同于：

```
:map c b
```

默认的 map 就是递归的。如果遇到 nore 这种前缀，比如 :noremap，就表示这种 map 是非递归的。

#### 命令模式下的实例

新建一个 mapping，将 b 映射成 a。在普通模式下，按下 b，会进入插入模式：

```
:nmap b a
```

新建一个 mapping，赶紧进入插入模式，输入 bug 这个单词吧！

```
:imap b a
```

注意如果向上边那样，按 b 输入的确是 a，那么恭喜，你已经把 vim 的按键弄得乱七八糟了，试着用 unmap 和 mapclear 清除这些 mapping 吧。

#### 写入配置文件

把常用的快捷键操作写入 `.vimrc` 中，使其永久生效是个不错的主意,这样每次打开 vim 就会自动准备好。一般自定义的快捷键映射都使用非递归的方式。下边的快捷键定义在普通模式下按 Ctrl 和相应的上下左右键，跳转到分割的屏幕上。

```
"split navigations
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-H> <C-W><C-H>
nnoremap <C-L> <C-W><C-L>
```

#### 阅读更多

VIM 键映射 <http://vimcdoc.sourceforge.net/doc/map.html#:imap>

普通模式的映射命令
map
命令格式：
:map {lhs} {rhs}
其含义是，在:map 作用的模式中把键系列 {lhs} 映射为 {rhs}，{rhs}可进行映射扫描，也就是可递归映射。

举例：
:map td :tabnew .<cr>
含义：在其作用模式（普通、可视、操作符）下，输入 td 等价于输入 :tabnew . <cr>。而普通模式下输入:tabnew . <cr>就是打开当前目录
如果再定义绑定 :map ts td，就是指在其作用模式下输入 ts 等价于 td，也就是打开当前目录。不过如果没有特殊需要，一般不建议递归映射。

noremap
:noremap 和:map 命令相对，作用模式和命令格式都相同，只不过不允许再对{rhs}进行映射扫描，也就是{lhs}定义后的映射就是{rhs}的键序列，不会再对{rhs}键序列重新解释扫描。它一般用于重定义一个命令，当然如果:map 不需要递归映射的话，建议使用:noremap
比如：
:noremap ts td
它的意思是在其作用模式下，输入 ts 就是输入 td，但是和:map 不同的是，此时 td 再不会做进一步扫描解释。虽然之前已经定义了 td，但是不会对 td 再做扫描。

unmap
:unmap 是对应取消:map 绑定的｛lhs｝，作用模式相同，命令格式 :unmap {lhs}。
例如：
:unmap td
就是取消在其作用模式中 td 的绑定，比如之前 td 被绑定为:tabnew .<cr>，此时此绑定消失。

mapclear
:mapclear 时对应取消所有:map 绑定的，慎用！

只用于普通模式的
:nmap
:nmap 是:map 的普通模式板，也就是说其绑定的键只作用于普通模式。
例如：
:nmap td :tabnew .<cr> 和 :map td :tabnew .<cr> 在普通模式下等效
:nnoremap
:nnorempa 和:nmap 的关系和:noremap 和:map 的关系一样，只是:nmap 的非递归版
:nunmap
:nunmap 和:nmap 的关系和:unmap 和:map 的关系一样，取消:nmap 的绑定。
:nmapclear
:nmapclear 是对应取消所有:map 绑定的，慎用！

另外
{rhs} 之前可能显示一个特殊字符:

- 表示它不可重映射
  & 表示仅脚本的局部映射可以被重映射
  @ 表示缓冲区的局部映射

到这一步你可以轻松的长吸一口气，因为相关的命令已经都了解了，记不住没关系，可以随时:help map 一下。

键表
<k0> - <k9> 小键盘 0 到 9
<S-...> Shift ＋键
<C-...> Control ＋键
<M-...> Alt ＋键 或 meta ＋键
<A-...> 同 <M-...>
<Esc> Escape 键
<Up> 光标上移键
<Space> 插入空格
<Tab> 插入 Tab
<CR> 等于<Enter>

特殊参数
有些特殊参数必须映射命令的后边，在其他任何参数的前面。

<buffer>
<buffer>如果这些映射命令的第一个参数是<buffer>，映射将只局限于当前缓冲区（也就是你此时正编辑的文件）内。比如：
:map <buffer> ,w /a<CR>
它的意思时在当前缓冲区里定义键绑定，“,w”将在当前缓冲区里查找字符a。同样你可以在其他缓冲区里定义：
:map <buffer> ,w /b<CR>
比如我经常打开多个标签(:tabedit)，想要在各自标签里定义”,w”键绑定，那么你只要在每个标签页里分别定义就可，其作用域也只在各自的标签里。同样要清除这些缓冲区的键绑定也要加上<buffer>参数，比如：
:unmap <buffer> ,w
:mapclear <buffer>

<silent>
<silent>是指执行键绑定时不在命令行上回显，比如：
:map <silent> ,w /abcd<CR>
你在输入,w查找abcd时，命令行上不会显示/abcd，如果没有<silent>参数就会显示出来。

<special>
<special>一般用于定义特殊键怕有副作用的场合。比如：
:map <special> <F12> /Header<CR>

<expr>
<expr>. 如果定义新映射的第一个参数是<expr>，那么参数会作为表达式来进行计算，结果使用实际使用的，例如：
:inoremap <expr> . InsertDot()
这可以用来检查光标之前的文本并在一定条件下启动全能 (omni) 补全。
一个例子：

let counter = 0
inoremap <expr> <C-L> ListItem()
inoremap <expr> <C-R> ListReset()

func ListItem()
let g:counter += 1
return g:counter . '. '
endfunc

func ListReset()
let g:counter = 0
return ''
endfunc

在插入模式下，CTRL-L 插入顺序的列表编号，并返回；CTRL-R 复位列表编号到 0，并返回空。

<unique>
<unique>一般用于定义新的键映射或者缩写命令的同时检查是否该键已经被映射，如果该映射或者缩写已经存在，则该命令会失败

<Leader>和 mapleader 变量
mapleader 变量对所有 map 映射命令起效，它的作用是将参数<leader>替换成 mapleader 变量的值，比如：
:map <Leader>A oanother line<Esc>
如果 mapleader 变量没有设置，则用默认的反斜杠代替，因此这个映射等效于：
:map \A oanother line<Esc>
意思时输入\A 键时，在下一行输入 another line 并返回到普通模式。
如果设置了 mapleader 变量，比如：
let mapleader = ","
那么就等效于：
:map ,A oanother line<Esc>

<LocalLeader>和 maplocalleader 变量
<LocalLeader>和<Leader>类似，只不过它只作用于缓冲区。
因此在设置 mapleader 和 maplocalleader 时最好区分开，不要出现冲突。

<https://blog.csdn.net/zzyczzyc/article/details/86529138>

【Vim】使用 map 自定义快捷键：<https://blog.csdn.net/JasonDing1354/article/details/45372007>

vim 编辑模式下移动光标一般是先按 ESC 键，回到 Normal 模式后才去移动光标。

这样在 编辑模式 和 正常模式 下频繁切换的情况下，操作很麻烦。

所以在 .vimrc 里追加了如下的快捷键：

```json
inoremap <C-f> <Right>
inoremap <C-b> <Left>
inoremap <C-a> <Home>
inoremap <C-e> <End>
inoremap <C-k> <Up>
inoremap <C-l> <Down>
inoremap <C-q> <PageUp>
inoremap <C-z> <PageDown>

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
]
```

## vim 脚本

让 vim 自动化。

参见：[Docs --> 第三章 脚本 --> 简介](https://vim80.readthedocs.io/zh/latest/script/one.html)

## 常见问答

参见：[Docs --> 第三章 常见问答](https://vim80.readthedocs.io/zh/latest/chapters/04.html)

## 自整理

### vim 打开文件

- vim 还没有启动时

  ```shell
  vim file1 file2 ... filen
  ```

- vim 已经启动

  ```shell
  :e ../myFile
  ```

vim 缓冲区操作：

```shell
:n  # 打开下一个文件
:N  # 打开上一个文件
# 如果有任何未保存的更改，Vim将不允许您移动到下一个文件。要将更改保存在当前文件中，请键入：ZZ

# 查看当前打开的buffer（文件），二选一
:buffers
:ls

# 在缓冲区之间切换文件
:bf  ＃转到第一个文件。
:bl  ＃转到最后一个文件
:bn  ＃转到下一个文件。
:bp  ＃转到上一个文件。
:b number ＃转到第n个文件（例如：b 2）
:bw  ＃关闭当前文件。
```

> [vim 技巧：在不同文件 buffer 间切换](https://segmentfault.com/a/1190000021070194)

### Vim 上下移动一行或多行的按键序列

<https://zhuanlan.zhihu.com/p/588627413>

### vim 使用技巧

<https://pengfeixc.com/blogs/developer-handbook/vim-shortcuts>

Vim 中切换窗口（在文件之间切换）
切换窗口：Ctrl + w + (h/j/k/l) 。
即 h 左、j 下、k 上、l 右，表示窗口切换的方向。

### VScode when 子句上下文

<https://juejin.cn/post/7072621434605928462>

### VIM 剪切复制粘贴

<https://linux265.com/course/vim-cut-copy-paste.html>

### Vim 查找与替换

<https://linux265.com/course/vim-find-replace.html>

### Vim 复制粘贴与寄存器

> [Vim 复制粘贴与寄存器](https://blog.csdn.net/halazi100/article/details/47807033)
> 在 Vim 中的复制，删除，替换等操作的临时内容，都会存储在寄存器中

1. 无名寄存器("")
   两个双引号，Vim 中叫做无名寄存器。x,s,d,c,y 等操作，如果不指定寄存器，都是将临时内容放到这个寄存器中，也就是相当于一个默认寄存器。
   可以通过 :reg 来查看当前寄存器的值，操作一下，然后查寄存器内容，就明白了。
   例如：
   复制当前行(yy)，并粘贴(p)。
   这里 y 命令会将当前行内容放入寄存器""，按 p 时，会到寄存器""中取内容。

2. 复制专用寄存器("0)
   通过 y 命令复制的内容，会保存到寄存器 0 中。
   寄存器的使用是通过"后面跟寄存器名字。
   例如：
   复制当前行(yy)，
   又做了几次删除单词操作(dw)
   但是只想粘贴刚才复制的行，那么就不能用无名寄存器""去粘贴了，不能直接 p 进行粘贴，需要用"0p，指定使用寄存器 0，因为"0 里只存放 y 命令存入的内容。

3. 删除专用寄存器("1-"9)
   通过 d 或 c 命令，删掉的内容，会保存打"1-"9 这 9 个寄存器中。
   最新删除的内容，会在"1 中，其他顺延。
   例如：
   删除当前行(yy)
   删除当前行(yy)
   想复制第一次删除的行，"2p

4. 命名寄存器("a-"z)
   可以将重要内容放到命名寄存器"a-"z 中，一共 26 个。
   例如：
   把当前行放入寄存器"j 里，"jyy
   复制寄存器"j 的内容， "jp

5. 黑洞寄存器("\_d)
   放到这个寄存器的内容，将不会放到任何其他寄存器中，相当于彻底删除内容。
   例如：
   彻底删除当前行，不放入任何寄存器，"\_dd

6. 系统剪贴板("+)
   通过"+寄存器可以把内容复制到系统剪贴板，也可以从系统剪贴板粘贴内容但 Vim 中。
   例如：
   复制当前行到系统剪贴板中，"+yy
   复制系统剪贴板到 vim 中，"+p

总之，如果要使用一个寄存器，按以下形式

> [双引号][寄存器名][命令]

### vim 命令/搜索模式下粘贴寄存器内容

使用 `ctrl + R + [寄存器名]`。
如：

1. 使用 y 复制数据，按 `:` 进入命令模式，然后 `ctrl + R + 0`
2. 复制数据到全局寄存器，按 `/` 进入搜索模式，然后 `ctrl + R + +`

### 单词上下文查找

我想要拷贝一个单词，然后进行上下文的查找。

方法一：Shift + *
命令模式下，将光标移动到单词上，按下 Shift + * 两个按键，即可直接进入命令行查找该单词模式。

方法二：搜索模式下查找
输入/word 或者?word 查找单词 word，如果想接着查找该单词，按 n 或 N。

/def 从上往下搜索字符串 def，即向后搜索。

?def 从下往上搜索字符串 def，即向前搜索。

> 注：输入/或？后，可以按 Ctrl + R 进入寄存选择

### 16 进制显示

`:%!xxd` 是一个用于在 Vim 或 Neovim 编辑器中将文件内容转换为十六进制（hex）显示的命令。

- `:` 开头表示你在 Vim/Neovim 中进入命令模式。
- `%` 代表当前编辑的整个文件，所有行。
- `!` 表示将文件内容通过外部程序处理。
- `xxd` 是一个 Unix/Linux 系统上的工具，用于将二进制文件转换为十六进制格式（hex dump）。

所以，`:%!xxd` 这个命令的作用就是将当前文件的内容通过 `xxd` 转换为十六进制格式，并显示在 Vim/Neovim 中。如果你想把十六进制显示的内容恢复为原来的二进制格式，你可以使用 `:%!xxd -r`。

### 块级删除

常用 di*和 da*，这里的\*表示边界字符，可以是 双引号，小括号，大括号 等；

比如你要删除双引号中的内容："hello world"；你就可以通过 di" 进行删除，如果不仅想删除双引号里的内容，还想把双引号一起删除，就可以使用 da" 来完成；删除完双引号里的内容想立即切换到 插入模式 也可以使用 ci" 来完成；

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
  > 方法1：打开 Neovim，输入 `:h init.vim` 查看 Neovim 的配置文件位置
  > 方法2：打开 Neovim，输入 `:echo stdpath('config')` 查看
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

### 基础配置
