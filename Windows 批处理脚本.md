# Windows批处理脚本(.bat文件）语法笔记

[toc]

[批处理](https://blog.csdn.net/weixin_44627151/article/details/113728735?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-4-113728735-blog-124805612.235^v43^pc_blog_bottom_relevance_base4&spm=1001.2101.3001.4242.3&utm_relevant_index=5)

[批处理 for循环](https://blog.csdn.net/bigbear00007/article/details/105759830)

<https://www.jb51.net/article/97204.htm>

批处理(bat)脚本语言(3) - SET命令和变量使用

<https://blog.csdn.net/fw0124/article/details/39996265>

[批处理命令——for](https://www.cnblogs.com/Braveliu/p/5081087.html)

## 批处理脚本的使用方法

首先是批处理脚本的使用方法。一般是新建一个文本文档，然后将后缀名改为.bat。然后选中该文件，右键选择编辑，编写脚本代码。编码完成后双击文件运行。

### 注释

1. 在批处理脚本中，使用 `::` 或 `REM` 表示注释当前行。

2. 使用 `@echo off` 表示此后不显示执行的命令本身。也就是说，如果不加这个，你的脚本在执行时，代码中的命令也会出现在cmd窗口中。

```bat
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

### 批处理文件bat中，路径包含空格应该怎么处理

### 问题描述

- 在bat文件中，定义了一个路径变量：set projectpath=C:\Users\user name\Desktop，基于这个路径，需要进行一些处理，所以定义了另一个路径变量：set output=%projectpath%\output。
- 在bat运行时就出问题了，因为projectpath表示的路径中有空格，所以在取变量projectpath的值时被截断了，只能取作C:\Users\user，自然的，变量output的值也不是我想要的。
- 针对这个问题要怎么解决呢。

### 解决过程

- 我是真没想到这么个问题还让我查了挺长时间的，感觉bat好烂呀（当然是因为我不熟悉哈，只是单纯的觉得烂，发泄一下）。
- 空格没法用转义来表示，字符串和变量两个双引号时也不能直接拼接，真是烦死了。
- **如果只是路径中包含了空格，那么加一个双引号就可以了，但是我这里用到了变量来确定另一个路径，加引号解决不了问题。**
- 最后看到了[这篇帖子](https://www.cnblogs.com/Onlyou/p/4357522.html)，问题才算解决了，感谢。

此for循环将列出目录中的所有文件。

pushd somedir

for /f "delims=" %%f in ('dir /b /a-d-h-s') do echo %%f

popd

“ delims =”可用于显示长文件名并带有空格。

'/ b“仅显示名称，不显示大小日期等。

关于dir的/ a参数要了解的一些事情。

任何使用“ / a”都会列出所有内容，包括隐藏属性和系统属性。

“ / ad”将仅显示子目录，包括隐藏目录和系统目录。

“ / ad”参数消除具有'D'irectory属性的内容。

“ / adhs”将显示所有内容，但条目带有'D'irectory，'H'idden'S'ystem属性。

如果在命令行上使用此命令，请删除“％”。

[Windows 批处理的字符运算（未完待续）](https://faradays-studio.gitee.io/202008200927/)

## Windows 批处理中字符的基本常识

1. 批处理中变量的赋值符号两侧不能包含空格，如 `set str_date='20200820'`，这与很多编程规范是相悖的。
2. 批处理中的字符可以不添加双引号，但是如果包含空格的话，必须使用引号，，如 `set str_name="20200820 Windows 批处理的字符运算经验总结"`。
3. 自定义变量使用 % 来包围来进行引用，即 `%变量%` ；而 Windows 内置变量（含文件路径变量扩展）则使用 % 符号来引导，即 `%内置变量` 。

# 打开文件目录要几个斜杠

在Windows操作系统中，打开文件目录时需要使用反斜杠`\`来表示路径。如果要打开一个文件夹，通常需要在路径末尾添加一个反斜杠，例如：

```makefile
makefile
复制代码C:\Users\Username\Documents\
```

在Unix/Linux操作系统中，使用正斜杠`/`来表示路径。同样的，如果要打开一个文件夹，通常需要在路径末尾添加一个正斜杠，例如：

```arduino
/home/username/documents/
```

需要注意的是，如果路径中有空格或其他特殊字符，需要使用引号或转义符来处理，以确保路径能够正确解析。

# BAT 与 SHELL 脚本

下面从**定位差异**出发，对 **Windows BAT（cmd）脚本** 与 **Linux/Unix Shell（bash 为主）脚本** 的**常用语法、注释、变量、流程控制、函数、错误处理**等进行系统对比，偏向工程实践而不是入门流水账。

## 一、运行环境与设计理念差异

| 维度           | BAT（cmd.exe）     | Shell（bash/sh）       |
| -------------- | ------------------ | ---------------------- |
| 设计年代       | DOS / Windows NT   | Unix                   |
| 解释器         | `cmd.exe`          | `/bin/sh`、`/bin/bash` |
| 语法风格       | 命令驱动、弱结构   | 语言化、强组合         |
| 管道 / 文本流  | 弱（不是一等公民） | 强（一切皆文本）       |
| 工程复杂度上限 | 低                 | 高                     |

**一句话总结**：BAT 是“命令自动化脚本”，Shell 是“编程语言”。

## 二、注释（Comment）

1. Shell 注释

   ```bash
   # 单行注释

   : <<'EOF'
   多行注释
   EOF
   ```

   - `#` 是**真正的语法级注释**
   - Here-doc 多行注释常用于临时屏蔽代码

2. BAT 注释

   ```bat
   REM 这是注释
   :: 这也是注释（非官方）
   ```

⚠️ 差异重点：

| 方式  | 特点                                             |
| ----- | ------------------------------------------------ |
| `REM` | 官方、稳定                                       |
| `::`  | 实际是 label，**在某些场景会出 bug**（如括号块） |

👉 **工程建议**：

> **只用 `REM`，别用 `::`**

## 三、变量定义与使用

1. Shell

   ```bash
   var=hello
   echo "$var"
   ```

   - **等号两边不能有空格**
   - 使用时要 `$`
   - 双引号非常重要（防止单词分裂）

2. BAT

   ```bat
   set var=hello
   echo %var%
   ```

   **延迟展开（必须掌握）**

   ```bat
   setlocal enabledelayedexpansion
   set var=1
   echo !var!
   ```

   | 场景            | `%var%` | `!var!` |
   | --------------- | ------- | ------- |
   | 普通            | ✅      | ❌      |
   | `if / for` 块内 | ❌      | ✅      |

   > 👉 BAT 最反直觉的点，没有之一。

## 四、参数（命令行参数）

1. Shell

   ```bash
   $0   # 脚本名
   $1   # 第一个参数
   $@   # 所有参数
   $#   # 参数个数
   ```

2. BAT

   ```bat
   %0   脚本名
   %1   第一个参数
   %*   所有参数
   ```

   判断参数是否存在：

   ```bat
   if "%1"=="" (
       echo missing arg
   )
   ```

## 五、条件判断（if）

1. Shell

   ```bash
   if [ -f file.txt ]; then
       echo exists
   fi
   if [[ "$a" == "x" ]]; then
       ...
   fi
   ```

   - `[` 是命令
   - `[[ ]]` 是 bash 扩展（**更安全**）

2. BAT

   ```bash
   if exist file.txt (
       echo exists
   )

   if "%a%"=="x" (
       ...
   )
   ```

   **注意**：字符串比较必须加引号（否则空变量直接炸）

## 六、循环（for）

1. Shell

   ```bash
   for f in *.txt; do
       echo "$f"
   done
   for ((i=0;i<10;i++)); do
       echo $i
   done
   ```

2. BAT（极其反人类）

   ```bat
   for %%f in (*.txt) do (
       echo %%f
   )
   ```

   - 命令行用 `%f`
   - 脚本里必须 `%%f`

   ```bat
   for /L %%i in (0,1,9) do echo %%i
   ```

## 七、函数 / 子程序

1. Shell（真函数）

   ```bash
   foo() {
       echo "hello"
   }

   foo
   ```

   - 有作用域
   - 有返回码 `$?`

2. BAT（伪函数）

   ```bat
   call :foo
   goto :eof

   :foo
   echo hello
   goto :eof
   ```

   ❌ 没有返回值
   ❌ 没有局部变量
   ❌ 本质是跳转

## 八、错误处理（工程关键）

1. Shell（工业级）

   ```bash
   set -euo pipefail
   ```

   | 选项       | 含义                 |
   | ---------- | -------------------- |
   | `-e`       | 命令失败即退出       |
   | `-u`       | 未定义变量即报错     |
   | `pipefail` | 管道中任一失败即失败 |

   获取返回值：

   ```bash
   cmd
   ret=$?
   ```

2. BAT（极弱）

   ```bat
   somecmd
   if errorlevel 1 (
       echo failed
   )
   ```

   :warning: `errorlevel` 判断是 `>=`，不是 `==`。

## 九、路径 & 命令替换

1. Shell

   ```bash
   pwd
   BASEDIR=$(dirname "$(realpath "$0")")
   ```

2. BAT

   ```bat
   cd
   %~dp0
   ```

   | 表达    | 含义              |
   | ------- | ----------------- |
   | `%~dp0` | 当前 bat 所在目录 |

## 十、工程级总结（重点）

1. 核心差异速记

   | 方面         | Shell      | BAT            |
   | ------------ | ---------- | -------------- |
   | 语言能力     | ⭐⭐⭐⭐⭐ | ⭐⭐           |
   | 错误处理     | 强         | 极弱           |
   | 可维护性     | 高         | 低             |
   | 心智负担     | 中         | 高（延迟展开） |
   | 适合复杂工程 | ✅         | ❌             |

2. 实战建议（结合你最近在写 bat 的场景）
   1. **BAT 只做“胶水”**
      - 调程序
      - 拷文件
      - 环境准备

   2. **复杂逻辑全部放 Python / Shell**

   3. BAT 必须写：

      ```bat
      setlocal enabledelayedexpansion
      ```
