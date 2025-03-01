# Windows 批处理脚本(.bat 文件）语法笔记

[toc]

[批处理](https://blog.csdn.net/weixin_44627151/article/details/113728735?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-4-113728735-blog-124805612.235^v43^pc_blog_bottom_relevance_base4&spm=1001.2101.3001.4242.3&utm_relevant_index=5)

[批处理 for 循环](https://blog.csdn.net/bigbear00007/article/details/105759830)

https://www.jb51.net/article/97204.htm

批处理(bat)脚本语言(3) - SET 命令和变量使用

https://blog.csdn.net/fw0124/article/details/39996265

[批处理命令——for](https://www.cnblogs.com/Braveliu/p/5081087.html)

## 批处理脚本的使用方法

首先是批处理脚本的使用方法。一般是新建一个文本文档，然后将后缀名改为.bat。然后选中该文件，右键选择编辑，编写脚本代码。编码完成后双击文件运行。

### 注释

1. 在批处理脚本中，使用 `#` 表示注释当前行。

2. 使用 `@echo off` 表示此后不显示执行的命令本身。也就是说，如果不加这个，你的脚本在执行时，代码中的命令也会出现在 cmd 窗口中。

3. 单行注释

   ```bash
   单行注释
   1、rem
   rem 注释内容
   2、::
   :: 注释内容

   多行注释

   goto :标记
   注释内容1
   注释内容2
   注释内容3
   :标记
   ```

### 批处理文件 bat 中，路径包含空格应该怎么处理

### 问题描述

- 在 bat 文件中，定义了一个路径变量：set projectpath=C:\Users\user name\Desktop，基于这个路径，需要进行一些处理，所以定义了另一个路径变量：set output=%projectpath%\output。
- 在 bat 运行时就出问题了，因为 projectpath 表示的路径中有空格，所以在取变量 projectpath 的值时被截断了，只能取作 C:\Users\user，自然的，变量 output 的值也不是我想要的。
- 针对这个问题要怎么解决呢。

### 解决过程

- 我是真没想到这么个问题还让我查了挺长时间的，感觉 bat 好烂呀（当然是因为我不熟悉哈，只是单纯的觉得烂，发泄一下）。
- 空格没法用转义来表示，字符串和变量两个双引号时也不能直接拼接，真是烦死了。
- **如果只是路径中包含了空格，那么加一个双引号就可以了，但是我这里用到了变量来确定另一个路径，加引号解决不了问题。**
- 最后看到了[这篇帖子](https://www.cnblogs.com/Onlyou/p/4357522.html)，问题才算解决了，感谢。


[Windows 批处理的字符运算（未完待续）](https://faradays-studio.gitee.io/202008200927/)

## Windows 批处理中字符的基本常识

1. 批处理中变量的赋值符号两侧不能包含空格，如 `set str_date='20200820'`，这与很多编程规范是相悖的。
2. 批处理中的字符可以不添加双引号，但是如果包含空格的话，必须使用引号，，如 `set str_name="20200820 Windows 批处理的字符运算经验总结"`。
3. 自定义变量使用 % 来包围来进行引用，即 `%变量%` ；而 Windows 内置变量（含文件路径变量扩展）则使用 % 符号来引导，即 `%内置变量` 。

# 打开文件目录要几个斜杠

在 Windows 操作系统中，打开文件目录时需要使用反斜杠 `\` 来表示路径。如果要打开一个文件夹，通常需要在路径末尾添加一个反斜杠，例如：`C:\Users\Username\Documents\`

在 Unix/Linux 操作系统中，使用正斜杠 `/` 来表示路径。同样的，如果要打开一个文件夹，通常需要在路径末尾添加一个正斜杠，例如：`/home/username/documents/`

需要注意的是，如果路径中有空格或其他特殊字符，需要使用引号或转义符来处理，以确保路径能够正确解析。
