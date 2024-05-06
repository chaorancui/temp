
### Vim 上下移动一行或多行的按键序列
https://zhuanlan.zhihu.com/p/588627413

### vim 使用技巧
https://pengfeixc.com/blogs/developer-handbook/vim-shortcuts



Vim中切换窗口（在文件之间切换）
切换窗口：Ctrl + w + (h/j/k/l) 。
即h左、j下、k上、l右，表示窗口切换的方向。


map简介

map是一个映射命令,将常用的很长的命令映射到一个新的功能键上。map是Vim强大的一个重要原因，可以自定义各种快捷键，用起来自然得心应手。

映射的种类

有五种映射存在：

用于普通模式: 输入命令时。
用于可视模式: 可视区域高亮并输入命令时。
用于操作符等待模式: 操作符等待中 (“d”，”y”，”c” 等等之后)。
用于插入模式: 也用于替换模式。
用于命令行模式: 输入 “:” 或 “/” 命令时。

几种模式的介绍

Normal Mode
也就是最一般的普通模式，默认进入vim之后，处于这种模式。

Visual Mode
一般译作可视模式，在这种模式下选定一些字符、行、多列。
在普通模式下，可以按v进入。

Insert Mode
插入模式，其实就是指处在编辑输入的状态。普通模式下，可以按i进入。

Select Mode
选择模式。用鼠标拖选区域的时候，就进入了选择模式。和可视模式不同的是，在这个模式下，选择完了高亮区域后，敲任何按键就直接输入并替换选择的文本了。和windows下的编辑器选定编辑的效果一致。普通模式下，可以按gh进入。

Command-Line/Ex Mode
命令行模式和Ex模式。两者略有不同，普通模式下按冒号(:)进入Command-Line模式，可以输入各种命令，
使用vim的各种强大功能。普通模式下按Q进入Ex模式，其实就是多行的Command-Line模式。

命令的组合

同Vim下的其他命令一样，命令的名字往往由好几段组成。前缀作为命令本身的修饰符，微调命令的效果。
对于map而言，可能有这么几种前缀：

nore
表示非递归。
递归的映射。其实很好理解，也就是如果键a被映射成了b，c又被映射成了a，如果映射是递归的，那么c就被映射成了b。
n
表示在普通模式下生效
v
表示在可视模式下生效
i
表示在插入模式下生效
c
表示在命令行模式下生效
普通模式的映射命令
map
命令格式：
:map {lhs} {rhs}
其含义是，在:map作用的模式中把键系列 {lhs} 映射为 {rhs}，{rhs}可进行映射扫描，也就是可递归映射。

举例：
:map td :tabnew .<cr>
含义：在其作用模式（普通、可视、操作符）下，输入td等价于输入 :tabnew . <cr>。而普通模式下输入:tabnew . <cr>就是打开当前目录
如果再定义绑定 :map ts td，就是指在其作用模式下输入ts等价于td，也就是打开当前目录。不过如果没有特殊需要，一般不建议递归映射。

noremap
:noremap和:map命令相对，作用模式和命令格式都相同，只不过不允许再对{rhs}进行映射扫描，也就是{lhs}定义后的映射就是{rhs}的键序列，不会再对{rhs}键序列重新解释扫描。它一般用于重定义一个命令，当然如果:map不需要递归映射的话，建议使用:noremap
比如：
:noremap ts td
它的意思是在其作用模式下，输入ts就是输入td，但是和:map不同的是，此时td再不会做进一步扫描解释。虽然之前已经定义了td，但是不会对td再做扫描。

unmap
:unmap是对应取消:map绑定的｛lhs｝，作用模式相同，命令格式 :unmap {lhs}。
例如：
:unmap td
就是取消在其作用模式中td的绑定，比如之前td被绑定为:tabnew .<cr>，此时此绑定消失。

mapclear
:mapclear时对应取消所有:map绑定的，慎用！

只用于普通模式的
:nmap
:nmap是:map的普通模式板，也就是说其绑定的键只作用于普通模式。
例如：
:nmap td :tabnew .<cr> 和 :map td :tabnew .<cr> 在普通模式下等效
:nnoremap
:nnorempa和:nmap的关系和:noremap和:map的关系一样，只是:nmap的非递归版
:nunmap
:nunmap和:nmap的关系和:unmap和:map的关系一样，取消:nmap的绑定。
:nmapclear
:nmapclear是对应取消所有:map绑定的，慎用！

另外
{rhs} 之前可能显示一个特殊字符:

- 表示它不可重映射
& 表示仅脚本的局部映射可以被重映射
@ 表示缓冲区的局部映射

到这一步你可以轻松的长吸一口气，因为相关的命令已经都了解了，记不住没关系，可以随时:help map一下。

键表
<k0> - <k9> 小键盘 0 到 9
<S-...> Shift＋键
<C-...> Control＋键
<M-...> Alt＋键 或 meta＋键
<A-...> 同 <M-...>
<Esc> Escape 键
<Up> 光标上移键
<Space> 插入空格
<Tab> 插入Tab
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

在插入模式下，CTRL-L插入顺序的列表编号，并返回；CTRL-R复位列表编号到0，并返回空。

<unique>
<unique>一般用于定义新的键映射或者缩写命令的同时检查是否该键已经被映射，如果该映射或者缩写已经存在，则该命令会失败

<Leader>和mapleader变量
mapleader变量对所有map映射命令起效，它的作用是将参数<leader>替换成mapleader变量的值，比如：
:map <Leader>A oanother line<Esc>
如果mapleader变量没有设置，则用默认的反斜杠代替，因此这个映射等效于：
:map \A oanother line<Esc>
意思时输入\A键时，在下一行输入another line并返回到普通模式。
如果设置了mapleader变量，比如：
let mapleader = ","
那么就等效于：
:map ,A oanother line<Esc>

<LocalLeader>和maplocalleader变量
<LocalLeader>和<Leader>类似，只不过它只作用于缓冲区。
因此在设置mapleader和maplocalleader时最好区分开，不要出现冲突。



https://blog.csdn.net/zzyczzyc/article/details/86529138

【Vim】使用map自定义快捷键：https://blog.csdn.net/JasonDing1354/article/details/45372007

  

vim 编辑模式下移动光标一般是先按 ESC 键，回到 Normal 模式后才去移动光标。

这样在 编辑模式 和 正常模式 下频繁切换的情况下，操作很麻烦。

所以在 .vimrc 里追加了如下的快捷键：

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

### VSCode when 子句上下文：
https://juejin.cn/post/7072621434605928462

### VIM 剪切复制粘贴：
https://linux265.com/course/vim-cut-copy-paste.html

### Vim复制粘贴与寄存器
> [Vim复制粘贴与寄存器](https://blog.csdn.net/halazi100/article/details/47807033)
在Vim中的复制，删除，替换等操作的临时内容，都会存储在寄存器中


1.无名寄存器("")
两个双引号，Vim中叫做无名寄存器。x,s,d,c,y等操作，如果不指定寄存器，都是将临时内容放到这个寄存器中，也就是相当于一个默认寄存器。
可以通过 :reg 来查看当前寄存器的值，操作一下，然后查寄存器内容，就明白了。
例如：
复制当前行(yy)，并粘贴(p)。
这里y命令会将当前行内容放入寄存器""，按p时，会到寄存器""中取内容。

2. 复制专用寄存器("0)
通过y命令复制的内容，会保存到寄存器0中。
寄存器的使用是通过"后面跟寄存器名字。
例如：
复制当前行(yy)，
又做了几次删除单词操作(dw)
但是只想粘贴刚才复制的行，那么就不能用无名寄存器""去粘贴了，不能直接p进行粘贴，需要用"0p，指定使用寄存器0，因为"0里只存放y命令存入的内容。

3. 删除专用寄存器("1-"9)
通过d或c命令，删掉的内容，会保存打"1-"9这9个寄存器中。
最新删除的内容，会在"1中，其他顺延。
例如：
删除当前行(yy)
删除当前行(yy)
想复制第一次删除的行，"2p

4. 命名寄存器("a-"z)
可以将重要内容放到命名寄存器"a-"z中，一共26个。
例如：
把当前行放入寄存器"j里，"jyy
复制寄存器"j的内容， "jp

5. 黑洞寄存器("_d)
放到这个寄存器的内容，将不会放到任何其他寄存器中，相当于彻底删除内容。
例如：
彻底删除当前行，不放入任何寄存器，"_dd

6. 系统剪贴板("+)
通过"+寄存器可以把内容复制到系统剪贴板，也可以从系统剪贴板粘贴内容但Vim中。
例如：
复制当前行到系统剪贴板中，"+yy
复制系统剪贴板到vim中，"+p

总之，如果要使用一个寄存器，按以下形式

       [双引号][寄存器名][命令]



### vim 在搜索模式下粘贴

复制：

1) v (或在视觉模式下用鼠标突出显示)

2) y (yank)

粘贴：

1) / (搜索模式)

2) Ctrl + R + 0 (0是寄存器编号)


### 单词上下文查找

我想要拷贝一个单词，然后进行上下文的查找。

方法一：Shift + *
命令模式下，将光标移动到单词上，按下 Shift + * 两个按键，即可直接进入命令行查找该单词模式。

方法二：搜索模式下查找
输入/word或者?word查找单词word，如果想接着查找该单词，按n或N。

/def  从上往下搜索字符串def，即向后搜索。

?def  从下往上搜索字符串def，即向前搜索。

> 注：输入/或？后，可以按Ctrl + R 进入寄存选择
