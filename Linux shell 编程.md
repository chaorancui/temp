[toc]

# 正则表达式

> [正则表达式全集](https://tool.oschina.net/uploads/apidocs/jquery/regexp.html) --> 介绍每个字符含义
> [揭开正则表达式的神秘面纱](https://www.regexlab.com/zh/regref.htm) --> 有例子
> [regular-expressions.info](https://www.regular-expressions.info/) --> 关于正则表达式的首要网站
>
> [RegexBuddy 的正则表达式详细教程](https://www.regexbuddy.com/tutorial.html) --> 擦，工具要付费
>
> [RegexBuddy.pdf](https://www.balsas-nahuatl.org/mixtec/Programas/JGsoft/RegexBuddy/)

- 基本正则表达式

  [Docs » 通配机制 » 正则表达式 » 正则表达式语法 » 基本正则表达式](https://codetoolchains.readthedocs.io/en/latest/5-Wildcard/2-Regular/1-syntax/1-bRegEx.html)

- 扩展正则表达式

  [Docs » 通配机制 » 正则表达式 » 正则表达式语法 » 扩展正则表达式](https://codetoolchains.readthedocs.io/en/latest/5-Wildcard/2-Regular/1-syntax/2-eRegEx.html)

- Perl 正则表达式(PCRE)

  [Perl 正则匹配和正则表达式](https://dulunar.github.io/2021/01/01/Perl%E6%AD%A3%E5%88%99%E5%8C%B9%E9%85%8D%E5%92%8C%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F-%E5%89%AF%E6%9C%AC/)

  [Perldoc 浏览器](https://perldoc.perl.org/perlre)

> 注意:
>
> - 通配的`*`和正则里面的`*`是不一样的含义。

## 正则表达式介绍

[Linux 文本处理：掌握基础、扩展和 Perl 正则表达式的威力](https://blog.csdn.net/dgwxligg/article/details/138875027)

当探讨 Linux 文本处理时，**基础正则表达式**（Basic Regular Expressions, BRE）、**扩展正则表达式**（Extended Regular Expressions, ERE）和**Perl 兼容正则表达式**（Perl-Compatible Regular Expressions, PCRE）这三种正则表达式非常重要。它们在功能和语法上有所区别，并由不同的工具和命令支持。

1. **基本正则表达式（BRE）**

   **标准**：POSIX 定义的基础规范
   **工具代表**：传统 `grep`、`sed`（默认模式）
   **核心特点**：

   - **元字符需转义**：
     基础元字符（如 `.`、`*`、`^`、`$`）可直接使用，但扩展功能（如分组、量词）需转义：
     - `\( \)` 表示分组，`\+` 表示“1 次或多次”。
     - 例如：`a\+` 匹配 `a`、`aa`，但不支持 `a+`（未转义的 `+` 是普通字符）。
   - **功能受限**：
     - **默认不支持** `|`（逻辑或）、`?`（零次或一次）、`{n,m}`（量词范围）。但部分工具（如 GNU 扩展版的 `grep`、`sed`）可以通过 **转义** 来启用它们。
     - 无预定义字符类（如 `\w`、`\s`），需用 POSIX 类（如 `[[:digit:]]`）。

   ```bash
   # 匹配 "color" 或 "colour"（需转义分组和量词）
   grep 'colou\?r' file.txt  # GNU grep 扩展支持 \?，但严格 BRE 需用 'color\|colour'
   ```

2. **扩展正则表达式（ERE）**

   **标准**：POSIX 扩展规范
   **工具代表**：`grep -E`、`egrep`、`awk`、`find -regextype posix-extended`
   **核心特点**：

   - **元字符无需转义**：
     直接使用 `+`、`?`、`|`、`()` 等：
     - `(ab)+` 匹配 `ab`、`abab` 等。
     - `a|b` 匹配 `a` 或 `b`。
   - **仍不支持部分高级特性**：
     - 无 `\w`、`\s`、`\d` 等快捷方式（需用 `[[:alnum:]]`）。
     - 不支持非贪婪量词（如 `*?`）、零宽断言（如 `(?=)`）。

   ```bash
   # 匹配邮箱（ERE 更简洁）
   grep -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' file.txt
   ```

3. **Perl 兼容正则表达式（PCRE）**

   **标准**：Perl 语言定义，事实上的现代标准
   **工具代表**：Perl、Python、Ruby、现代编程语言、`grep -P`（GNU 扩展）
   **核心特点**：

   - **元字符丰富且无需转义**：
     - 直接使用 `+`、`?`、`|`、`()`，支持 `\w`（单词字符）、`\d`（数字）、`\s`（空白）等。
   - **高级功能**：
     - **非贪婪量词**：`*?`、`+?` 最小化匹配。
     - **零宽断言**：`(?=pattern)`（前瞻）、`(?<=pattern)`（后顾）。
     - **条件与回溯**：复杂模式匹配和替换。
   - **Unicode 支持**：
     - `\p{L}` 匹配任意字母，`\p{Sc}` 匹配货币符号等。

   ```python
   # 非贪婪匹配 HTML 标签（PCRE）
   import re
   re.findall(r'<.*?>', '<div>test</div>')  # 结果: ['<div>', '</div>']
   ```

**三者的主要差异对比**

| **特性**                 | **BRE**                       | **ERE**            | **PCRE**                   |
| :----------------------- | :---------------------------- | :----------------- | :------------------------- |
| **元字符转义**           | `\+`、`\(` 需转义             | `+`、`()` 无需转义 | 同 ERE，且支持更多快捷方式 |
| **逻辑或 $\vert$**       | 不支持（需 $\setminus\vert$） | 直接支持           | 直接支持                   |
| **量词 `?` `+` `{n,m}`** | 需转义：`\?` `\+`             | 直接支持           | 直接支持                   |
| **分组 `()`**            | 需转义：`\( \)`               | 直接支持           | 直接支持，支持命名分组     |
| **预定义字符类**         | 仅 POSIX 类                   | 仅 POSIX 类        | `\w`、`\d`、`\s` 等        |
| **非贪婪匹配**           | 不支持                        | 不支持             | 支持（`*?`、`+?`）         |
| **零宽断言**             | 不支持                        | 不支持             | 支持（`(?=)`、`(?<=)` 等） |
| **Unicode**              | 不支持                        | 不支持             | 支持（`\p{...}`）          |

**使用场景建议**

1. **BRE**：
   - 需兼容老旧 Unix 工具（如 `sed` 默认模式）或严格 POSIX 环境时使用。
   - 语法繁琐，现代场景尽量避免。
2. **ERE**：
   - 脚本中需要平衡功能与可移植性时的首选（如 `grep -E`、`awk`）。
   - 比 BRE 更易读，但功能仍有限。
3. **PCRE**：
   - 现代编程（Python、Perl 等）或复杂文本处理（如提取嵌套结构）。
   - 功能最强大，但需注意工具支持（如 GNU `grep -P` 非标准）。

**经典案例对比**

```bash
# 匹配 "file1" 到 "file9"：
BRE:  grep 'file[1-9]'           # 基础字符集
ERE:  grep -E 'file[1-9]'        # 同 BRE，但更清晰
PCRE: grep -P 'file\d'           # 使用 \d 快捷方式

# 匹配 "color" 或 "colour"：
BRE:  grep 'colou\?r'            # 需转义量词
ERE:  grep -E 'colou?r'          # 无需转义
PCRE: grep -P 'colou?r'          # 同 ERE，但可与其他 PCRE 特性组合
```

理解这些差异后，可以根据工具和环境选择最合适的正则表达式类型。

**注意事项：**

1. `|` 或
   在正则表达式中，`|` 两边的空格会被视为正则表达式的一部分，而不是忽略它们。因此，如果在 `|` 两边加了空格如 `(x | y)_pos`，正则表达式将会匹配包含空格的字符串，
   即：`x␣_pos`（x 后面有一个空格）和 `␣y_pos`（y 前面有一个空格）。
   如果你不希望匹配到空格，那么在 `|` 两边不要添加空格，即使用 `(x|y)_pos`，会匹配 `x_pos` 或 `y_pos`。

## 正则表达式需要转义的字符

正则表达式中有些字符具有特殊的含义，如果在匹配中要用到它本来的含义，需要进行转义（在其前面加一个 `\`）。下面总结了常见的一些需要转义的特殊字符：

1. `$`：匹配输入字符串的结尾位置。如果设置了 RegExp 对象的 Multiline 属性，则 `$` 也匹配，如 `\n` 或 `\r`。
2. `()`：标记一个子表达式的开始和结束位置。子表达式可以获取供以后使用。要匹配这些字符。
3. `*`：匹配前面的子表达式零次或多次。
4. `+`：匹配前面的子表达式一次或多次。
5. `.`：匹配除换行符 `\n` 之外的任何单字符。
6. `[]`：标记一个中括号表达式的开始。
7. `?`：匹配前面子表达式零次或一次，或指明一个非贪婪限定符
8. `\`：将下一个字符标记为或特殊字符或原意字符或后向引用或八进制转义符。例如：`n` 匹配字符 `n`，而 `\n` 匹配换行符。序列 `\\` 匹配 `\`。
9. `^`：匹配输入字符串的开始位置，除非在方括号表达式中使用，此时他表示不接受该字符集合。
10. `{}`：标记限定符表达式的开始。
11. `|`：指明两项之间的一个选择。

**总结**：`* . ? + $ ^ [ ] ( ) { } | \ /`

## "通配符"和"正则表达式"的区别

> [正则表达式和通配符的区别](https://blog.csdn.net/bytxl/article/details/8801304)

**通配符**：

说白了一般只用于文件名匹配，它是由 shell 解析的。所谓的系统 level 的概念非常含糊，什么是系统 level 的？我们知道 shell 是一个命令解释器，它是内核的外壳，用于完成操作系统使用者与内核的沟通，因此，**通配符实际上就是一个 shell 解释器去解析的符号**，它的特殊涵义是由 shell 这个命令解释器赋予的。通配符的英文名是 **wildcard**，就是万用牌的意思，它相当简单，一般来说，_nix 系统上面的 shell 大多将三个特殊符号当作通配符，它们是 `_` `?` `[...]`， 其中\* 表示匹配任意长度的任意字符； ? 表示匹配一个任意字符， 而[...]则表示匹配括号中列出的字符中的任意一个。

**正则表达式**：

是一种对字符串匹配模式的描述和规定，并且是一种标准，需要相关工具的支持。而不同的工具程序，也就是`egrep、sed、awk、perl等`这样的程序，以各种程度来支持这种字符串搜索模式，它们就是标准的实现，你可以在这种软件中使用正则表达式这种“匹配模式标准”。

**在什么地方使用通配符？**

答案是只要是**shell 命令行或者 shell 脚本**中，你都可以使用通配符；如命令 find，ls，cp 等等。

**在什么地方使用正则表达式？**

当你使用能够**支持正则表达式的工具软件进行字符串处理**时你就可以使用正则表达式。你还可以在支持正则表达式的语言中使用正则表达式，比如 perl, java... C++中也有专门用于支持正则表达式的库。正则表达式总是和“使用什么工具软件或者语言”相关。相对来说，不同的工具和语言对正则表达式的支持程度不同，\*nix 里面将这些工具软件的对正则表达式的支持分类，因此也就有了“基础正则表达式”和“扩展正则表达式”。

不同的工具对正则表达式的支持，其实有些许的微妙不同；但是总体来说，使用正则还是基本按照标准来的。这些不同的工具支持程度，被称之为“正则流派”。而工具软件中支持这种匹配模式的那部分代码，称之为“正则引擎”。由于 perl 对正则表达式的支持非常到位，其正则引擎也比较优秀，因此 perl 语言算是正则的一大流派，目前大部分对正则的支持都或多或少参考了 perl 语言中的标准。

**通配符**：

| 符号       |                                                         |
| ---------- | ------------------------------------------------------- |
| ？         | 任意一个字符                                            |
| \*         | 0-多个任意字符                                          |
| [ab]       | 只匹配其中的一个字符                                    |
| [a-z]      | 只匹配 a-z 其中的一个字符                               |
| [^ab]      | 除了 a 或 b                                             |
| [^a-z]?    | 除了 a-z 开头后面有一个字符，第一个字符不能是字母开头的 |
| [a-z][0-9] | 第一个字符是字母，第二个是数字                          |
| ?\*        | 第一个任意字符，后面随意                                |
| \*         | 0-多个任意字符                                          |

# shell 编程

## shell 中转义字符$

在 linux shell 脚本中经常用到字符`$`，下面是`$`的一些常见用法

| 名称 | 含义                                                                    |
| ---- | ----------------------------------------------------------------------- |
| $#   | 传给脚本的参数个数                                                      |
| $0   | 脚本本身的名字                                                          |
| $1   | 传递给该 shell 脚本的第一个参数                                         |
| $2   | 传递给该 shell 脚本的第二个参数                                         |
| $@   | 传给脚本的所有参数的列表                                                |
| $\*  | 以一个单字符串显示所有向脚本传递的参数，与位置变量不同，参数可超过 9 个 |
| $$   | 脚本运行的当前进程 ID 号                                                |
| $?   | 显示最后命令的退出状态，0 表示没有错误，其他表示有错误                  |

- 文件名`test`

```shell
#!/bin/sh
echo "number:$#"
echo "scname:$0"
echo "first :$1"
echo "second:$2"
echo "argume:$@"
```

- 运行结果

```shell
number:2   //$# 是传给脚本的参数个数
scname:./test //$0 是脚本本身的名字
first: aa  //$1是传递给该shell脚本的第一个参数
second:bb  //$2是传递给该shell脚本的第二个参数
argume:aa bb //$@ 是传给脚本的所有参数的列表
```

## 重定向

在 Shell 中，输出重定向是一种将命令的标准输出（stdout）或标准错误（stderr）保存到文件或传递给另一个命令的技术。输出重定向使你能够灵活地管理和处理命令的输出。

1. 基本输出重定向
   将标准输出重定向到文件

   - `>`：将命令的标准输出重定向到一个文件。如果文件已经存在，会覆盖文件的内容。

     ```shell
     command > filename

     echo "Hello, World!" > output.txt
     # 这会将 "Hello, World!" 保存到 output.txt 文件中。如果 output.txt 已存在，其内容会被覆盖。
     ```

   - `>>`：将命令的标准输出追加到文件的末尾。如果文件不存在，会创建文件；如果文件已经存在，新的输出内容会追加到文件末尾。

     ```shell
     command >> filename

     echo "Hello again!" >> output.txt
     # 这会将 "Hello again!" 追加到 output.txt 的末尾，而不会覆盖之前的内容。
     ```

2. 重定向标准错误
   标准错误输出（stderr）通常用于输出错误信息，可以将其重定向到文件。

   - `2>`：将标准错误输出重定向到文件。

     ```shell
     command 2> errorfile.txt

     ls non_existent_file 2> error.txt
     # 这会将 ls 命令的错误信息保存到 error.txt 文件中。
     ```

3. 同时重定向标准输出和标准错误

   - `&>` 或 `2>&1`：将标准输出和标准错误一起重定向到同一个文件。

     ```shell
     command &> outputfile.txt
     # 等价于
     command > outputfile.txt 2>&1

     ls /nonexistent_directory &> all_output.txt
     # 这会将 ls 命令的标准输出和错误输出都保存到 all_output.txt 文件中。

     # 重定向 + 管道组合
     command 2>&1 | tee output.log
     ```

     注意：

     - `&>` 是 Bash 的语法糖（语法简写），只能用于 Bash（不是 POSIX 标准，因此在 sh 或某些老版本 shell 中不支持）。
     - `command 2>&1 | tee output.log` <font color=red>重定向 + 管道组合</font>：
       - `2>&1`：先把标准错误（fd 2）重定向到标准输出（fd 1）
       - 整个 stdout + stderr 一起通过 `|` 管道交给 tee
       - `tee`：一边将输入写入 output.log，一边输出到终端（屏幕）
     - `command > file 2>&1` <font color=red>顺序非常重要！</font>这表示：
       - 先把 stdout 重定向到 file
       - 再把 stderr 重定向到 stdout（此时 stdout 已经是 file）
     - `command 2>&1 > file` 是错误写法：
       - `2>&1`：把 stderr 重定向到当前的 stdout，此时 stdout 还指向终端
       - `> file`：把 stdout 重定向到 file，但是 stderr 已经绑定到了“原始的终端 stdout”，不会跟着变
       - 结果是：stdout 输出进 file，stderr 仍然输出到终端！

4. 重定向到 `/dev/null`
   `/dev/null` 是一个特殊的文件，任何写入它的数据都会被丢弃。可以使用它来忽略不需要的输出。

   - 忽略标准输出/标准错误/标注输出和错误：

     ```shell
     # 忽略标准输出：
     command > /dev/null

     # 忽略标准错误：
     command 2> /dev/null

     # 忽略标准输出和标准错误：
     command > /dev/null 2>&1

     ls /nonexistent_directory > /dev/null 2>&1
     # 这会忽略 ls 命令的所有输出。
     ```

5. 管道（|）
   管道将一个命令的标准输出作为下一个命令的标准输入。常用于将多个命令串联起来处理数据。

   - 使用管道：

     ```shell
     command1 | command2

     ls -l | grep "^d"
     这会将 ls -l 的输出传递给 grep 命令，只显示目录条目。
     ```

6. 文件描述符的重定向
   在 Shell 中，文件描述符用于标识不同的输入和输出流：

   - 标准输入 (stdin)：文件描述符 0
   - 标准输出 (stdout)：文件描述符 1
   - 标准错误 (stderr)：文件描述符 2

   你可以使用文件描述符进行更精细的重定向控制。

   ```shell
   command 1> stdout.txt 2> stderr.txt
   # 这会将标准输出重定向到 stdout.txt，将标准错误重定向到 stderr.txt。
   ```

7. Here Document (<<)
   Here Document 用于将多行字符串作为输入传递给命令。

   ```shell
   command << EOF
   line1
   line2
   EOF
   ```

   - command：这是需要接收多行输入的命令。
   - <<：这个符号告诉 Shell 开始一个 Here Document。
   - EOF：这个是标识符（delimiter），表示 Here Document 的开始和结束。EOF 只是一个常用的标识符名称，你可以用其他任何字符串代替，只要它在开始和结束时保持一致即可。

   如下命令，在 << EOF 之后的所有内容都将作为输入传递给指定的命令，直到遇到结尾标识符（如 EOF）。

   ```shell
   cat << EOF > file.txt
   This is line 1
   This is line 2
   EOF
   # 这会将多行文本保存到 file.txt 中。
   ```

总结

- `>`：将标准输出重定向到文件（覆盖文件内容）。
- `>>`：将标准输出追加到文件末尾。
- `2>`：将标准错误输出重定向到文件。
- `&>` 或 `2>&1`：同时重定向标准输出和标准错误。
- `/dev/null`：丢弃输出。
- `|`：将一个命令的输出作为下一个命令的输入。
- `Here Document (<<)`：用于传递多行输入。

## shell 中 `;` `|` `()` `{}` `&&` `||` `!`

在 Shell 编程中，`;`、`|`、`()`、`{}`、`&&`、`||`、`!` 等符号用于控制命令的执行顺序、条件判断和组合，以下是它们的详细介绍：

1. **`;` (命令分隔符)**

   `;` 用于在同一行中执行多个命令，命令之间没有依赖关系。无论前一个命令是否成功，后一个命令都会执行。

   示例：

   ```bash
   echo "First command" ; sleep 2; echo "Second command"
   ```

   这里，`echo "First command"` 和 `echo "Second command"` 会**依次执行**。

2. **`|` (管道操作符)**

   `|` 是管道符号，用于将前一个命令的输出作为下一个命令的输入，即将一个命令的结果“管道”给另一个命令。

   示例：

   ```bash
   ls -l | grep ^- | sort -k5 -nr
   ```

   - `ls -l`：以长格式列出文件和目录。
   - `grep ^-`：过滤出文件（忽略目录）。在 ls -l 输出中，文件以 - 开头，目录以 d 开头，符号链接以 l 开头。
   - `sort -k5 -nr`：按第 5 列（文件大小）进行数值排序（-n 表示数值排序，-r 表示从大到小排序）。

3. **`()` (子 shell)**

   `()` 用于在子 **Shell 中执行命令序列**，子 Shell 是一个独立的环境，子 Shell 中的变量或状态不会影响当前 Shell。

   示例：

   ```bash
   (cd .. && ls)
   ```

   在子 Shell 中进入父目录并列出内容，执行完毕后，当前 Shell 仍在原来的目录。

4. **`{}` (命令块)**

   `{}` 表示命令块，内部的多个命令会在**当前 Shell 中执行**。不同于 `()`，它不会创建子 Shell。
   **正确格式要求**：

   - 大括号 `{` 和 `}` 必须与内部命令之间有**空格**。
   - 多个命令之间需要用 `;` 或换行符分隔（即在 Shell 中，`{}` 内的命令必须用分号 `;` 连接，不能使用 `&&` 直接连接）。

   ```bash
   { cd ..; ls; }
   # 或
   {
     cd ..
     ls
   }
   ```

   在当前 Shell 中进入父目录并列出内容，执行完毕后，当前 Shell 会切换至父目录。

5. **`()` 和 `{}` 对比**

   如果希望把几个命令合在一起执行，shell 提供了两种方法：

   1. `()` 在子 shell 中执行一组命令
   2. `{  }` 在当前 shell 中执行一组命令

   ```shell
   # () 在子 shell 中执行
   A=1; echo $A; (A=2;); echo $A
   1
   1
   # {  } 在当前 shell 中执行
   A=1; echo $A; { A=2; }; echo $A
   1
   2
   ```

6. **`&&` (逻辑与, AND)**

   `&&` 是逻辑与操作符，

   - 表示前一个命令成功（退出状态码 $? 为 0）时才执行下一个命令。
   - 只要有一个命令失败（退出状态码 $? 为 1），后面的命令就不会被执行。

   示例：

   ```bash
   mkdir new_dir && cd new_dir
   ```

   如果 `mkdir new_dir` 成功，则 `cd new_dir` 会被执行。

   > 技巧：
   >
   > - `cp xx && rm -f xx && echo "copy and rm success!"`，拷贝后删除原文件

7. **`||` (逻辑或, OR)**

   `||` 是逻辑或操作符，

   - 表示前一个命令失败（退出状态码 $? 非 0）时才执行下一个命令。
   - 只要有一个命令成功（退出状态码 $? 为 0），后面的命令就不会被执行。

   示例 1：

   ```bash
   mkdir new_dir || echo "Failed to create directory"
   ```

   如果 `mkdir new_dir` 失败，则会执行 `echo "Failed to create directory"` 命令。

   示例 2：

   ```shell
   ls dir &> /dev/null && echo"SUCCESS" || echo "FAIL"
   # 如果 dir 目录存在，将输出 SUCCESS 提示信息；否则输出 FAIL 提示信息。

   # shell 脚本中常用的组合示例
   echo $BASH | grep -q 'bash' || { exec bash "$0" "$@" || exit 1; }
   # 系统调用exec是以新的进程去代替原来的进程，但进程的PID保持不变。
   # 因此可以这样认为，exec系统调用并没有创建新的进程，只是替换了原来进程上下文的内容。原进程的代码段，数据段，堆栈段被新的进程所代替。
   ```

   > `&&` 的优先级高于 `||`，会优先执行。`cmd1 && cmd2 || cmd3` 等价于 `(cmd1 && cmd2) || cmd3`。

8. **`!` (逻辑非, NOT)**

   `!` 是逻辑非操作符，用于取反。它会将一个命令的退出状态反转。即，如果命令成功，`!` 会将其视为失败；如果命令失败，`!` 会将其视为成功。

   示例：

   ```bash
   ! ls nonexistent_file && echo "File does not exist"
   ```

   这里，`ls nonexistent_file` 失败，`!` 将其反转为成功状态，所以后面的 `echo` 命令会执行。

9. **条件测试中与或非**

   这些操作符主要用于 `test` 或 `[ ]` 结构中，用于测试文件属性或条件。

   - **`!`**：逻辑非（NOT），用于取反。
   - **`-a`**：逻辑与（AND），表示两个条件都必须为真。
   - **`-o`**：逻辑或（OR），表示其中一个条件为真即可。

   示例：

   ```bash
   [ ! -f "file.txt" ]  # 如果 file.txt 文件不存在，则返回真
   [ -f "file1.txt" -a -f "file2.txt" ]  # 两个文件都存在则返回真
   [ -f "file1.txt" -o -f "file2.txt" ]  # 其中一个文件存在则返回真
   ```

10. 条件测试中与或非和命令执行中与或非

    在 Shell 表达式中，`!`、`-a`、`-o`、`&&`、`||` 等符号用于逻辑操作，但是它们用于不同的上下文和语法场景。

    1. **条件测试中的逻辑与或非**（`!`、`-a`、`-o`）：

       ```bash
       if [ -f file1 -a -f file2 ]; then
         echo "Both files exist"
       fi
       ```

       这里 `-a` 检查两个文件是否都存在。

    2. **命令执行中的逻辑与或非**（`&&`、`||`、`!`）：

       ```bash
       ! ls nonexistent_file && echo "File does not exist"
       ```

       这里 `!` 将 `ls nonexistent_file` 的失败状态反转为成功，从而执行后面的 `echo`。

    **区别总结**：

    - **`! -a -o`** 用于条件测试（如 `[ ]` 或 `test`），典型场景是检查文件状态、比较字符串等。
    - **`&& ||`** 用于命令执行顺序控制，用来根据前一个命令的执行结果来决定是否执行后续命令。

这些符号和操作符是 Shell 脚本中的基础工具，用于控制命令执行顺序和条件逻辑，帮助我们构建复杂的命令逻辑。

## 运算符优先级

> [Bash 脚本进阶指南：正文 > 第二部分 shell 基础 > 8. 运算符相关话题](https://linuxstory.gitbook.io/advanced-bash-scripting-guide-in-chinese/zheng-wen/part2/08_operations_and_related_topics/08_4_operator_precedence)

## 单/双/反引号

在 Shell 中，单引号 `' '`, 双引号 `" "`, 和反引号 ` `` ` 用于不同的目的，尤其是在处理字符串和命令替换时。它们的功能如下：

1. 单引号 `' '`

   - **功能**：将字符串完全保留为字面值，不进行变量和命令替换。

   - **用途**：当你想确保字符串中的特殊字符（如 `$`, `*`, `\` 等）不被解释或替换时，使用单引号。

   - 示例：

     ```bash
     echo 'Hello $USER'
     ```

     输出：`Hello $USER`（`$USER` 不会被解析）

2. 双引号 `" "`

   - **功能**：允许变量替换和命令替换，但保留大多数其他字符的字面意义。

   - **用途**：当需要字符串保留特殊字符（如空格）并希望进行变量替换或命令替换时，使用双引号。

   - 示例：

     ```bash
     echo "Hello $USER"
     ```

     输出：`Hello your_username`（`$USER` 被替换成实际的用户名）

3. 反引号 ` `` ` 或 `$(...)`（推荐）

   - **功能**：用于**命令替换**，即执行括号中的命令，并将结果插入到外部命令中。

   - **用途**：当你需要将命令的输出用作另一个命令的参数时，使用反引号或 `$()`。

   - 示例：

     ```bash
     echo "Today is `date`"
     ```

     或者：

     ```bash
     echo "Today is $(date)"
     ```

     两者输出相同，例如：`Today is Fri Nov 8 15:30:00 UTC 2024`

   > **注意**：推荐使用 `$()` 语法，因为它支持嵌套，而反引号不支持。

**小结**:

- **单引号**：完全保留字符串内容。
- **双引号**：允许变量替换和命令替换，但保留大多数字符。
- **反引号或 `$()`**：用于命令替换，将命令的输出作为参数传递。

## shell 命令展开

Shell 命令的展开是单次展开，按照固定顺序进行一次性展开。每种展开类型只会执行一次。不是递归展开。

举例说明：

1. 变量展开不会递归

   ```bash
   a='$b'
   b='$c'
   c='hello'
   echo $a  # 输出 $b，而不是递归展开到 hello
   ```

2. 命令替换不会递归

   ```bash
   cmd1='$(echo $cmd2)'
   cmd2='$(echo hello)'
   echo $(echo $cmd1)  # 输出 $(echo $cmd2)，不会继续展开
   ```

3. 要实现多次展开，需要使用 eval

   ```bash
   # 使用eval实现递归展开
   a='$b'
   b='$c'
   c='hello'
   eval echo $a  # 输出 $c
   eval eval echo $a  # 输出 hello
   ```

4. 实际应用示例

   ```bash
   # 单次展开
   var1="world"
   var2='$var1'
   echo $var2  # 输出: $var1

   # 使用eval强制多次展开
   eval echo $var2  # 输出: world

   # 命令替换也是单次
   cmd='$(echo "$(date)")'
   echo $cmd  # 输出: $(echo "$(date)")
   eval echo $cmd  # 输出: 当前日期
   ```

**重要说明**：

- shell 的标准展开是单次的
- 需要多次展开时必须显式使用 eval
- 过多的展开层次会使代码**难以维护和理解**
- 应尽量**避免复杂的多层展开**

## shell 命令展开优先级

Shell 命令展开遵循特定的顺序，完整的展开优先级（从高到低）：

- Brace expansion（大括号展开）
- Tilde expansion（波浪号展开）
- Parameter and variable expansion（参数和变量展开）
- Command substitution（命令替换）
- Arithmetic expansion（算术展开）
- Word splitting（词分割）
- Pathname expansion（路径名展开/通配符展开）

1. 大括号展开

   ```bash
   echo th{i,a}t  # 展开为 thit that
   ```

2. 波浪号展开 (~)

   ```bash
   echo ~/dir  # 展开为 /home/user/dir
   ```

3. 参数和变量展开

   ```bash
   name="John"
   echo $name    # 展开为 John
   echo ${name}  # 同上
   ```

4. 命令替换

   ```bash
   echo $(date)  # 执行date命令并替换结果
   echo `date`   # 同上
   ```

5. 算术展开

   ```bash
   echo $((2 + 2))  # 展开为 4
   ```

6. 单词分割(IFS)

   ```bash
   var="a b c"
   echo $var     # 分割为三个单词：a b c
   echo "$var"   # 保持为一个单词："a b c"
   ```

7. 路径名展开(通配符)

   ```bash
   echo *.txt    # 展开为所有.txt文件
   ```

**示例**：

```bash
# 展开顺序示例
user="john"
echo ~/${user}_file{1,2}.{txt,log}

# 展开步骤：
# 1. 大括号展开：~/john_file1.txt ~/john_file1.log ~/john_file2.txt ~/john_file2.log
# 2. 波浪号展开：/home/user/john_file1.txt ...
# 3. 变量展开：已在步骤1中完成
```

**注意事项**：

- 展开顺序是固定的，不可更改
- 引号会影响展开行为
- 展开结果会作为命令的参数

## `set` 命令

在 **shell 脚本** 中，`set` 命令用于更改脚本的执行选项，以控制脚本的行为。以下是一些常见选项及其作用：

1. `set -e` 与 `set +e`

   - **`set -e`**:
     当设置此选项时，脚本会在遇到非零退出状态的命令时立即退出（除非该命令已被 `if`、`while` 或 `||` 等控制结构捕获）。
     适用于希望脚本严格执行并在错误时立即停止的场景。

     示例：

     ```bash
     set -e
     echo "开始"
     ls /不存在的路径  # 这里会导致脚本退出
     echo "不会执行到这里"
     ```

   - **`set +e`**:
     关闭 `-e` 模式（即默认模式）。脚本即使遇到非零退出状态的命令，也会继续执行。可以自己添加异常处理逻辑。

2. `set -x` 与 `set +x`

   - **`set -x`**:
     开启调试模式，会在执行每一行命令前将其打印到标准错误输出。这对于调试脚本非常有用。

     示例：

     ```bash
     set -x
     echo "Hello"
     ls
     set +x
     ```

     输出示例：

     ```bash
     + echo "Hello"
     Hello
     + ls
     ```

   - **`set +x`**:
     关闭调试模式（即默认模式），不再打印命令。

3. 其他常用选项

   - **`set -u`**
     在脚本中引用未定义的变量时，立即退出并报错（默认情况下引用未定义变量会返回空值）。

     示例：

     ```bash
     set -u
     echo $未定义变量  # 会导致脚本退出
     ```

   - **`set +u`**
     关闭 `-u` 模式，允许使用未定义的变量。

   - **`set -o pipefail`**
     当命令管道中的任何一个命令失败时，返回非零状态。默认情况下，管道返回最后一个命令的退出状态。

     示例：

     ```bash
     set -o pipefail
     ls /不存在的路径 | grep "something"  # 返回非零状态
     ```

   - **`set +o pipefail`**
     关闭 `pipefail` 模式，恢复默认行为。

**总结**：

通过 `set`，可以细粒度控制脚本的行为。常见的组合：

- **调试脚本**: `set -x`
- **严格执行**: `set -euo pipefail`
- **临时关闭选项**: 用 `set +<option>` 在局部关闭某些特性。

## 路径处理

在 shell 脚本中处理路径有几种常用方法：

1. 获取相对路径:

   ```bash
   # 获取当前脚本所在目录
   current_dir=$(dirname "$0")

   # 获取当前工作目录
   pwd_dir=$(pwd)
   ```

2. 从绝对路径提取部分路径:

   ```bash
   full_path="/home/user/projects/test/file.txt"

   # 获取目录部分
   dir_path=$(dirname "$full_path")  # 结果: /home/user/projects/test

   # 获取文件名部分
   file_name=$(basename "$full_path")  # 结果: file.txt

   # 获取不带扩展名的文件名
   name_only=$(basename "$full_path" .txt)  # 结果: file
   ```

3. 使用参数展开:

   ```bash
   path="/home/user/projects/test/file.txt"

   # 提取最后一个/之前的内容
   before_last_slash=${path%/*}  # 结果: /home/user/projects/test

   # 提取最后一个/之后的内容
   after_last_slash=${path##*/}  # 结果: file.txt

   # 提取指定目录之后的路径
   sub_path=${path#*/user/}  # 结果: projects/test/file.txt
   ```

   参数展开匹配：

   ```bash
   file_folder="/home/user/test/project/file.txt"

   # 从开头匹配并删除最短匹配
   sub_path=${file_folder#*/test/}  # 结果: project/file.txt

   # 从开头匹配并删除最长匹配
   sub_path=${file_folder##*/test/}  # 结果: project/file.txt

   # 从结尾匹配并删除最短匹配
   sub_path=${file_folder%/test/*}  # 结果: /home/user

   # 从结尾匹配并删除最长匹配
   sub_path=${file_folder%%/test/*}  # 结果: /home/user
   ```

   参数展开操作符说明：

   - `#` - 从开头匹配，删除最短匹配
   - `##` - 从开头匹配，删除最长匹配
   - `%` - 从结尾匹配，删除最短匹配
   - `%%` - 从结尾匹配，删除最长匹配

## 参数展开操作符

**Shell 参数展开操作符的介绍**：

1. 基本的参数展开：`${}`

   ```bash
   var="hello"
   echo ${var}        # 等同于 $var
   echo ${var}world   # 拼接字符串，输出: helloworld
   ```

2. 长度获取：`#`

   ```bash
   str="hello"
   echo ${#str}      # 输出字符串长度: 5

   array=(1 2 3 4 5)
   echo ${#array[@]} # 输出数组长度: 5
   ```

3. 从开头删除匹配模式：`#` 和 `##`

   ```bash
   path="/usr/local/bin/python"
   # #  从开头删除最短匹配
   echo ${path#*/}      # 输出: usr/local/bin/python
   # ## 从开头删除最长匹配
   echo ${path##*/}     # 输出: python

   # 实际应用：提取文件名
   filename="script.test.sh"
   echo ${filename#*.}  # 输出: test.sh
   echo ${filename##*.} # 输出: sh
   ```

4. 从结尾删除匹配模式：`%` 和 `%%`

   ```bash
   path="/usr/local/bin/python"
   # %  从结尾删除最短匹配
   echo ${path%/*}      # 输出: /usr/local/bin
   # %% 从结尾删除最长匹配
   echo ${path%%/*}     # 输出: (空)

   # 实际应用：删除文件扩展名
   filename="script.test.sh"
   echo ${filename%.*}  # 输出: script.test
   echo ${filename%%.*} # 输出: script
   ```

5. 替换模式：`/` 和 `//`

   ```bash
   text="hello hello world"
   # / 替换第一次匹配
   echo ${text/hello/hi}   # 输出: hi hello world
   # // 替换所有匹配
   echo ${text//hello/hi}  # 输出: hi hi world

   # 实际应用：替换路径分隔符
   path="C:\Windows\System32"
   echo ${path//\\/\/}    # 输出: C:/Windows/System32
   ```

6. 默认值操作符：`:-`、`:=`、`:+`、`:?`

   ```bash
   # :- 如果变量未设置或为空，则使用默认值
   echo ${var:-default}   # var未设置，输出: default
   var=""; echo ${var:-default}  # var为空，输出: default
   var="value"; echo ${var:-default}  # var有值，输出: value

   # := 如果变量未设置或为空，则设置默认值并返回
   echo ${var:=default}   # 设置var为default并输出

   # :+ 如果变量设置且非空，则使用替代值
   var="value"
   echo ${var:+replaced}  # 输出: replaced

   # :? 如果变量未设置或为空，则显示错误信息并退出
   echo ${var:?"错误：var未设置"}
   ```

7. 子字符串提取：`:offset` 和 `:offset:length`

   ```bash
   str="Hello World"
   echo ${str:6}      # 输出: World
   echo ${str:0:5}    # 输出: Hello
   echo ${str: -5}    # 输出: World (注意空格)
   echo ${str: -5:2}  # 输出: Wo
   ```

**典型使用场景**：

1. 文件路径处理

   ```bash
   # 提取文件目录
   full_path="/home/user/docs/file.txt"
   dir=${full_path%/*}         # 输出: /home/user/docs

   # 提取文件名
   filename=${full_path##*/}   # 输出: file.txt

   # 提取不带扩展名的文件名
   name=${filename%.*}         # 输出: file

   # 提取扩展名
   ext=${filename##*.}         # 输出: txt
   ```

2. URL 处理

   ```bash
   url="https://example.com/path/to/page.html"
   # 提取域名
   domain=${url#*//}
   domain=${domain%%/*}       # 输出: example.com

   # 提取路径
   path=${url##*/}           # 输出: page.html
   ```

3. 批量重命名

   ```bash
   # 将所有.txt文件重命名为.md文件
   for file in *.txt; do
       mv "$file" "${file%.txt}.md"
   done
   ```

4. 环境变量处理

   ```bash
   # 添加路径到PATH，避免重复
   export PATH="${PATH:+$PATH:}/new/path"

   # 设置默认值
   TIMEOUT=${TIMEOUT:-30}
   ```

5. 字符串处理

   ```bash
   # 移除字符串中的所有空格
   str="hello world"
   echo ${str// /}      # 输出: helloworld

   # 将字符串中的下划线替换为空格
   var="hello_world_test"
   echo ${var//_/ }     # 输出: hello world test
   ```

这些操作符在 shell 脚本中非常有用，可以大大简化文本处理和路径操作的代码。需要注意的是，不同的 shell 可能支持的特性略有不同，上述例子主要基于 bash shell。

## 引用变量：`$VAR` 和 `${VAR}`

在 Shell 中，`$VAR` 和 `${VAR}` 都是用来引用变量 `VAR` 的，**在大多数情况下它们是等价的**。但 `${VAR}` 更加**稳健、推荐使用**，因为在某些上下文中能避免歧义。

| 表达式   | 含义                                   | 推荐度 |
| -------- | -------------------------------------- | ------ |
| `$VAR`   | 简写形式，适用于没有后缀的情况         | 简洁   |
| `${VAR}` | 标准形式，能防止歧义、支持更多扩展功能 | 推荐   |

情况 1：后面跟着其他字符时，`${VAR}` 能防止歧义

```bash
NAME="file"
echo "$NAME.txt"      # 输出空，Shell 会尝试找变量 NAME.txt
echo "${NAME}.txt"    # 正确输出：file.txt
```

情况 2：变量名后跟数组或替换表达式，必须用 `${}`：

```bash
echo "${ARRAY[0]}"    # 正确
echo "${VAR:-default}" # 使用默认值
```

结论：

- `"$VAR"`：在变量后无其他紧跟字符时可以用，简洁。
- `"${VAR}"`：更安全、通用，**推荐养成习惯**总是加大括号。
- **小技巧**：加双引号 `"` 防止字符串带空格被分割，如 `echo "${FILE}"`。

## Shell 中调用 Python

除了直接以 `python xxx.py` 的方式运行 py 文件，对于简单的 python 代码，还可以使用 `python -c`。
`python -c` 是 Python 提供的一个命令行参数，意思是 **直接在命令行执行一段 Python 代码字符串**。

```python
python -c "代码"
```

比如：

```shell
yaml_file="xxx.yaml"
config_file=$(python3 -c "
import yaml,sys
with open('$yaml_file') as f:
    data = yaml.safe_load(f)
print(data['config_file'])
")
```

注意事项

- 代码一般用 **双引号** `"..."` 包裹，如果里面也要用引号，需要转义。
- 多行语句可以用 `;` 分隔。
- 如果逻辑太复杂，不建议用 `-c`，而是写到 `.py` 脚本里。

## Shell 中 `return`

**一、`return` 的基本概念**

`return` 用于从**函数**或**被 source 的脚本**中返回，并可以设置返回值（退出状态）。

`return` vs `exit` 的区别：

| 命令   | 作用范围                 | 效果                              |
| ------ | ------------------------ | --------------------------------- |
| exit   | 整个进程                 | 终止当前进程（脚本或 Shell 会话） |
| return | 当前函数或 source 的脚本 | 从函数或 source 返回到调用者      |

二、**`return` 的使用场景**

1. 在函数中使用

   ```bash
   #!/bin/bash

   my_function() {
       echo "In function"
       return 5        # 从函数返回，设置退出状态为5
       echo "Never printed"
   }

   echo "Before function call"
   my_function
   echo "Function exit code: $?"
   echo "Script continues"
   ```

   **输出：**

   ```bash
   Before function call
   In function
   Function exit code: 5
   Script continues
   ```

2. 在被 source 的脚本中使用

   ```bash
   # lib.sh
   #!/bin/bash
   echo "In lib.sh"
   return 10           # 从source返回
   echo "Never printed"

   # main.sh
   #!/bin/bash
   echo "Before source"
   source lib.sh
   echo "Source exit code: $?"
   echo "Main script continues"
   ```

   **输出：**

   ```bash
   Before source
   In lib.sh
   Source exit code: 10
   Main script continues
   ```

3. 在主脚本中直接使用 `return`（错误用法）

   ```bash
   #!/bin/bash
   echo "Start"
   return 1            # 错误！会导致 "can only return from function or sourced script"
   echo "Never reached"
   ```

**三、`return` 的退出状态**

- `return` 不带参数：返回上一个命令的退出状态
- `return 0`：成功返回
- `return 1-255`：带错误代码返回

# shell 编程学习

## 学习笔记

> 中文：
>
> [Bash 脚本进阶指南](https://linuxstory.gitbook.io/advanced-bash-scripting-guide-in-chinese)
>
> [ShellScript](https://shellscript.readthedocs.io/zh-cn/latest/#)
>
> [CodeToolchains](https://codetoolchains.readthedocs.io/en/latest/5-Wildcard/2-Regular/1-syntax/1-bRegEx.html) ---- 基本正则表达式 / 扩展正则表达式
>
> 英文：
>
> [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/) ---- 非常详细，非常易读，大量 example，既可以当入门教材，也可以当做工具书查阅
>
> [Linux Shell Scripting Tutorial - A Beginner's handbook](http://bash.cyberciti.biz/guide/Main_Page)
>
> Note：
>
> [ShellScipt：Docs --> 语法基础 --> 数据类型](https://shellscript.readthedocs.io/zh-cn/latest/1-syntax/2-datatype/index.html)
>
> - 数值型（算数、比较运算操作）
> - 字符串型（消除、提取、替换）
> - 数组型（长度、元素消除、提取、替换）
> - 列表型（常用来 for 循环）
>
> [ShellScipt：Docs --> 语法基础 --> 变量](https://shellscript.readthedocs.io/zh-cn/latest/1-syntax/3-variable/index.html)
>
> `$?` 等特殊变量、`${var:-default}` 等变量赋值
>
> [ShellScipt：Docs --> 语法基础 --> 操作符](https://shellscript.readthedocs.io/zh-cn/latest/1-syntax/4-operator/index.html)
>
> - 引用操作符（变量引用、命令引用、字符引用）
>
> - 算术操作符（执行算术表达式的操作符有 `$[算术表达式]`、`$((算术表达式))`）
>
> - 条件测试操作符
>
>   > - 整数条件测试（如 `-eq` 等。执行整数条件测试表达式的操作符有 `[ 整数条件测试表达式 ]`、`[[ 整数条件测试表达式 ]]`，**注意前后有空格**）
>   > - 字符条件测试（如 `==`、`-n`、`-z` 等。执行字符条件测试表达式的操作符有 `[ 字符条件测试表达式 ]`、`[[ 字符条件测试表达式 ]]`，**注意前后有空格**）
>   > - 文件条件测试（如 `-e file`：文件是否存在，`-d directory`： 是否为目录文件等。执行文件条件测试表达式的操作符有 `[ 文件条件测试表达式 ]`、`[[ 文件条件测试表达式 ]]`，**注意前后有空格**）
>
> - 逻辑操作符（逻辑与`&&`，逻辑或`||`，逻辑非`!`。**注意：各种编译语言对逻辑真、假的定义不同，在 shell 中，状态值为 0 代表真，状态值为非 0 代表假**）
>
> - 括号操作符（`()`，`(())`，`[]`，`[[]]`，`{}`）
>
> [ShellScipt：Docs --> 语法基础 --> 控制流程语句](https://shellscript.readthedocs.io/zh-cn/latest/1-syntax/5-control/index.html)
>
> - 顺序执行语句
> - 条件执行语句
>   - if 条件语句
>   - case 条件语句
>   - select 条件语句
>   - 数字/字符/文件测试表达式
> - 循环执行语句
>   - for 循环语句
>   - while 循环语句
>   - untile 循环语句
>   - 循环退出语句
>
> [ShellScipt：Docs --> 语法基础 --> 函数](https://shellscript.readthedocs.io/zh-cn/latest/1-syntax/6-functions/index.html)
>
> - 函数定义
> - 函数调用（在优先级方面：`别名别名>函数>命令自身`)
> - 函数退出
>
> [ShellScipt：Docs --> 语法基础 --> 知识碎片](https://shellscript.readthedocs.io/zh-cn/latest/1-syntax/7-pieceofkn/index.html)
>
> 在编写 shell 脚本时，需要注意以下几点：
>
> - 标准输出：在编写 shell 脚本的时候，要考虑下该命令语句是否存在标准输出。有则问是否要输出到标准输出设备上；不需要则输出重定向到`/dev/null`。
> - 常见逻辑错误：输入为空、字符串大小写、输入是佛存在问题。
> - 编程思想：脚本输入输出是什么；根据输入可能存在逻辑错误的地方；不能举输出判断使用什么控制流程；在保证功能实现的前提下进行优化精简代码。
>
> [ShellScipt：Docs --> 语法基础 --> 常用类库](https://shellscript.readthedocs.io/zh-cn/latest/2-library/0-commonvar/index.html)
>
> - shell 脚本中常用的环境变量有：`IFS`是 shell 内部字段分隔符的环境变量；`RANDOM`环境变量是 bash 的伪随机数生成器。
> - shell 脚本中高频次的几个命令：[read](https://shellscript.readthedocs.io/zh-cn/latest/2-library/1-commoncmd/index.html#readll)：获取用户输入；[echo](https://shellscript.readthedocs.io/zh-cn/latest/2-library/1-commoncmd/index.html#echoll)：打印输出；[printf](https://shellscript.readthedocs.io/zh-cn/latest/2-library/1-commoncmd/index.html#printfll)：打印输出；[shift](https://shellscript.readthedocs.io/zh-cn/latest/2-library/1-commoncmd/index.html#shiftll)：剔除位置参数。

要点记录：

- `-x`选项可用来跟踪脚本的执行，是**调试 shell 脚本**的强有力工具。“-x”选项使 shell 在执行脚本的过程中把它实际执行的每一个命令行显示出来，并且在行首显示一个"+"号。 "+"号后面显示的是**经过了变量替换之后的命令行**的内容，有助于分析实际执行的是什么命令。 “-x”选项使用起来简单方便，可以轻松对付大多数的 shell 调试任务,应把其当作首选的调试手段。

  shell 的执行选项除了可以在**启动 shell 时指定外，亦可在脚本中用 set 命令来指定**。 "set -参数"表示启用某选项，"set +参数"表示关闭某选项。

  ```shell
  set -x  #启动"-x"选项 要跟踪的程序段
  set +x  #关闭"-x"选项
  ```

  set 命令同样可以使用调试钩子—DEBUG 函数来调用，这样可以避免脚本交付使用时删除这些调试语句的麻烦，如以下脚本片段所示：

  ```shell
  DEBUG set -x #启动"-x"选项 要跟踪的程序段
  DEBUG set +x #关闭"-x"选项
  ```

  对"-x"选项的增强：

  `$LINENO`：代表 shell 脚本的当前行号，类似于 C 语言中的内置宏`__LINE__`

  `$FUNCNAME`： 函数的名字，类似于 C 语言中的内置宏 `__func__`，但宏 `__func__` 只能代表当前所在的函数名，而 `$FUNCNAME` 的功能更强大，它是一个数组变量，其中包含了整个调用链上所有的函数的名字，故变量 `${FUNCNAME[0]}` 代表 shell 脚本当前正在执行的函数的名字，而变量 `${FUNCNAME[1]}` 则代表调用函数 `${FUNCNAME[0]}` 的函数的名字，余者可以依此类推。

  `$PS4`：主提示符变量 `$PS1` 和第二级提示符变量 `$PS2` 比较常见，但很少有人注意到第四级提示符变量 `$PS4` 的作用。`$PS4` 的值将被显示在 `-x` 选项输出的每一条命令的前面。在 Bash Shell 中，缺省的$PS4 的值是"+"号。现在知道为什么使用"-x"选项时，输出的命令前面有一个"+"号了吧。

  ```shell
  # 先执行下面命令，然后再使用“-x”选项来执行脚本，就能在每一条实际执行的命令前面显示其行号以及所属的函数名。
  export PS4='+{$LINENO:${FUNCNAME[0]}}'
  ```

  > [使用 sh -x 调试 shell 脚本](http://blog.chinaunix.net/uid-20564848-id-73502.html)

- `-c` 如果存在-c 选项，则从第一个非选项参数 command_string 读取命令。 如果 command_string 后面有参数，则第一个参数被赋值为`$0`，其余的参数被赋值为位置参数。 对 `$0` 的赋值设置了 shell 的名称，该名称用于警告和错误消息。会启动非交互式 shell。

- 按照惯例，用户编写的 Bourne shell 脚本应该在文件名后加上`.sh`的扩展名。而那些系统脚本，比如在`/etc/rc.d`中的脚本通常不遵循这种规范。

- exit 正确终止脚本的方式

  ```shell
  exit # 正确终止脚本的方式。
       # 不带参数的exit返回上一条指令的运行结果。
  ```

- 再重复一次，`#!/bin/sh`调用的是系统默认 shell 解释器，在 Linux 系统中默认为`/bin/bash`。

- 这个例子鼓励读者使用模块化的方式编写脚本，并在平时记录和收集一些在以后可能会用到的代码模板。最终你将拥有一个相当丰富易用的代码库。以下的代码可以用来测试脚本被调用时的参数数量是否正确。

- 你可以通过`sh scriptname`或`bash scriptname`来调用它（不推荐使用`sh <scriptname`调用脚本，因为这会禁用脚本从标准输入（stdin）读入数据）。当你使用`sh scriptname`调用*Bash*脚本时，将会禁用与 Bash 特性相关的功能，脚本有可能会执行失败。

- 脚本需要同时具有读取和执行的权限，因为 shell 需要读取脚本执行。

- `为什么不直接使用`scriptname`来调用脚本？为什么当工作目录（$PWD）正好是`scriptname`所在目录时也不起作用？因为一些安全原因，当前目录（`./`）并不会被默认添加到用户的$PATH路径中。因此需要用户显式使用`./scriptname`在当前目录下调用脚本。`

- ROOT_UID=0 # UID 为 0 的用户才拥有 root 权限。

  ```shell
  LOG_DIR=/var/log
  ROOT_UID=0     # UID为0的用户才拥有root权限。
  LINES=50       # 默认保存messages日志文件行数。
  E_XCD=86       # 无法切换工作目录的错误码。
  E_NOTROOT=87   # 非root权限用户执行的错误码。

  # 请使用root权限运行。
  if [ "$UID" -ne "$ROOT_UID" ]
  then
    echo "Must be root to run this script."
    exit $E_NOTROOT
  fi
  ```

- {xxx,yyy,zzz,...} 花括号扩展结构。

  理解：相当于把一个命令，展开成多个命令

  除非被引用或被转义，否则空白符不应在花括号中出现。

  ```shell
  echo {file1,file2}\ :{\ A," B",' C'}
  file1 : A file1 : B file1 : C file2 : A file2 : B file2 : C
  ```

- 通过()括号执行一系列命令会产生一个子 shell（subshell）。 括号中的变量，即在子 shell 中的变量，在脚本的其他部分是不可见的。父进程脚本不能访问子进程（子 shell）所创建的变量。

- 与由圆括号包裹起来的命令组不同，由花括号包裹起来的代码块不产生子进程。

- & 后台运行操作符。如果命令后带&，那么此命令将转至后台运行。

- 实际上, `$variable` 这种写法是 `${variable}` 的简化形式。在某些特殊情况下，使用 `$variable` 写法会造成语法错误，使用完整形式会更好（查看章节 10.2）。

- 初始化变量时，赋值号 = 的两侧绝不允许有空格出现。

  ```shell
  # 如果有空格会发生什么？

  #   "VARIABLE =value"
  #            ^
  #% 脚本将会尝试运行带参数 "=value" 的 "VARIABLE " 命令。
  ```

- 字符串内引用变量将会保留变量的空白符。

  ```shell
  hello="A B  C   D"
  echo $hello   # A B C D
  echo "$hello" # A B  C   D
  # 正如我们所见，echo $hello 与 echo "$hello" 的结果不同。
  # ====================================
  # 字符串内引用变量将会保留变量的空白符。
  # ====================================

  a=`ls -l`         # 将 'ls -l' 命令的结果赋值给 'a'
  echo $a           # 不带引号引用，将会移除所有的制表符与分行符
  echo
  echo "$a"         # 引号引用变量将会保留空白符
                    # 查看 "引用" 章节。
  ```

- 不要混淆 = 与 -eq，后者用来进行比较而非赋值。

  同时也要注意 = 根据使用场景既可作赋值操作符，也可作比较操作符。

- 注意在命令替换结构中包含感叹号(!)在命令行中使用将会失效，

  ```shell
  a=`echo Hello!`   # 将 'echo' 命令的结果赋值给 'a'
  echo $a
  #  注意在命令替换结构中包含感叹号(!)在命令行中使用将会失效，
  #+ 因为它将会触发 Bash 的历史(history)机制。
  #  在shell脚本内，Bash 的历史机制默认关闭。
  ```

- Bash 并不区分变量的类型。本质上说，_Bash 变量是字符串_，但在某些情况下，Bash 允许对变量进行算术运算和比较。决定因素则是变量值是否只含有数字。

- 每当 shell 启动时，都会创建出与其环境对应的 shell 环境变量。改变或增加 shell 环境变量会使 shell 更新其自身的环境。**_子进程_（由父进程执行产生）会继承*父进程*的环境变量**。

  分配给环境变量的空间是有限的。创建过多环境变量或占用空间过大的环境变量有可能会造成问题。

- 如果在脚本中设置了环境变量，那么这些环境变量需要被“导出”，也就是通知脚本所在的*环境*做出相应的更新。这个“导出”操作就是 `export` 命令。

  **脚本只能将变量导出到子进程**，即在这个脚本中所调用的命令或程序。在命令行中调用的脚本不能够将变量回传给命令行环境，即*子进程不能将变量回传给父进程*。

- 从命令行中传递给脚本的参数：`$0, $1, $2, $3 ...` 即**命令行参数**。

  `$0` 代表脚本名称，`$1` 代表第一个参数，`$2` 代表第二个，`$3` 代表第三个，以此类推。在 `$9` 之后的参数必须被包含在大括号中，如 `${10}, ${11}, ${12}`。

  特殊变量 `$*` 与 `$@` 代表所有位置参数。

- 在位置参数中使用大括号助记符提供了一种非常简单的方式来访问传入脚本的最后一个参数。在其中会使用到间接引用。

  ```shell
  args=$#           # 传入参数的个数
  lastarg=${!args}
  # 这是 $args 的一种间接引用方式

  # 也可以使用:       lastarg=${!#}             (感谢 Chris Monson.)
  # 这是 $# 的一种间接引用方式。
  # 注意 lastarg=${!$#} 是无效的。
  ```

- 使用 `shift` 命令步进访问所有的位置参数。

- 引用的一个重用用途是保护 Shell 中的命令行参数，但仍然允许调用的程序扩展它。

- 使用双引号可以防止字符串被分割。即使参数中拥有很多空白分隔符，被包在双引号中后依旧是算作单一字符。

  ```shell
  List="one two three"

  for a in $List     # 空白符将变量分成几个部分。
  do
    echo "$a"
  done
  # one
  # two
  # three

  echo "---"

  for a in "$List"   # 在单一变量中保留所有空格。
  do #     ^     ^
    echo "$a"
  done
  # one two three

  variable1="a variable containing five words"
  COMMAND This is $variable1    # 带上7个参数执行COMMAND命令：
  # "This" "is" "a" "variable" "containing" "five" "words"

  COMMAND "This is $variable1"  # 带上1个参数执行COMMAND命令：
  # "This is a variable containing five words"


  variable2=""    # 空值。

  COMMAND  $variable2 $variable2 $variable2
                  # 不带参数执行COMMAND命令。
  COMMAND "$variable2" "$variable2" "$variable2"
                  # 带上3个参数执行COMMAND命令。
  COMMAND "$variable2 $variable2 $variable2"
                  # 带上1个参数执行COMMAND命令（2空格）。
  ```

- 根据转义符所在的上下文（强引用、弱引用，命令替换或者在 here document）的不同，它的行为也会有所不同。

  ```shell
                        #  简单转义与引用
  echo \z               #  z
  echo \\z              # \z
  echo '\z'             # \z
  ehco '\\z'            # \\z
  echo "\z"             # \z
  echo "\\z"            # \z
  >
                        #  命令替换
  echo `echo \z`        #  z -->echo z
  echo `echo \\z`       #  z -->echo \z -->???
  echo `echo \\\z`      # \z -->echo "\z" -->???
  echo `echo \\\\z`     # \z -->echo "\\z" -->???
  echo `echo \\\\\\z`   # \z -->echo "\\\z" -->???
  echo `echo \\\\\\\z`  # \\z -->???
  echo `echo "\z"`      # \z -->???
  echo `echo "\\z"`     # \z -->???
  ```

- 转义空格能够避免在命令参数列表中的字符分割问题。

- 转义符也提供一种可以撰写多行命令的方式。通常，每一行是一个命令，但是转义换行后命令就可以在下一行继续撰写。

  在脚本中，如果以 "|" 管道作为一行的结束字符，那么不需要加转义符 \ 也可以写多行命令。但是一个好的编程习惯就是在写多行命令的事后，无论什么情况都要在行尾加上转义符 \。

  ```shell
  echo "foo
  bar"
  #foo
  #bar

  echo

  echo 'foo
  bar'    # 没有区别。
  #foo
  #bar

  echo

  echo foo\
  bar     # 转义换行。
  #foobar

  echo

  echo "foo\
  bar"     # 没有区别，在弱引用中，\ 转义符仍旧转义了换行。
  #foobar

  echo

  echo 'foo\
  bar'     # 在强引用中，\ 就按照字面意思来解释了。
  #foo\
  #bar
  ```

- 跟 C 程序类似，`exit` 命令被用来结束脚本。同时，它也会返回一个值，返回值可以被交给父进程。

  每个命令都会返回一个退出状态（exit status），有时也叫做返回状态（return status）或退出码（exit code）。**命令执行成功返回 0，如果返回一个非 0 值**，通常情况下会被认为是一个错误代码。一个运行状态良好的 UNIX 命令、程序和工具在正常执行退出后都会返回一个 0 的退出码，当然也有例外。

  同样地，脚本中的函数和脚本本身也会返回一个退出状态。在脚本或者脚本函数中执行的最后的命令会决定它们的退出状态。在脚本中，`exit nnn` 命令将会把 nnn 退出状态码传递给 shell（nnn 必须是 0-255 之间的整型数）。

  当一个脚本以不带参数的 `exit` 来结束时，脚本的退出状态**由脚本最后执行命令决定**（`exit` 命令之前）。

- 在脚本终止后，命令行下键入`$?`会给出脚本的退出状态，即在脚本中最后一条命令执行后的退出状态。一般情况下，0 为成功，1-255 为失败。

  ```shell
  #!/bin/bash

  echo hello
  echo $?    # 返回值为0，因为执行成功。

  lskdf      # 不认识的命令。
  echo $?    # 返回非0值，因为失败了。

  echo

  exit 113   # 将返回113给shell
             # 为了验证这些，在脚本结束的地方使用“echo $?”

  #  按照惯例，'exit 0' 意味着执行成功，
  #+ 非0意味着错误或者异常情况。
  #  查看附录章节“退出码的特殊含义”
  ```

- 测试结构会使用一个特殊的命令 `[`（参看特殊字符章节 [左方括号](http://tldp.org/LDP/abs/html/special-chars.html#LEFTBRACKET)）。等同于 `test` 命令，它是一个[内建命令](http://tldp.org/LDP/abs/html/internal.html#BUILTINREF)，写法更加简洁高效。**该命令将其参数视为比较表达式或文件测试**，以比较结果作为其退出状态码返回（0 为真，1 为假）。

- 结构 [`(( ... ))`](http://tldp.org/LDP/abs/html/dblparens.html) 和 [`let ...`](http://tldp.org/LDP/abs/html/internal.html#LETREF) 根据其执行的**算术表达式的结果**决定退出状态码。这样的 [算术扩展](http://tldp.org/LDP/abs/html/arithexp.html#ARITHEXPREF) 结构可以用来进行 [数值比较](http://tldp.org/LDP/abs/html/comparison-ops.html#ICOMPARISON1)。----- 只能算数表达式，且返回结果。

- 注意，双括号算术扩展表达式的退出状态码不是一个错误的值。**算术表达式为 0，返回 1；算术表达式不为 0，返回 0。**

  **"let" 结构**的退出状态与双括号算术扩展的**退出状态是相同的**。

  ```shell
  var=-2 && (( var+=2 ))
  echo $?                   # 1

  var=-2 && (( var+=2 )) && echo $var
                            # 并不会输出 $var, 因为((var+=2))的状态码为1

  (( 200 | 11 ))               # 按位或
  echo $?                      # 0     ***
  # ...
  let "num = (( 200 | 11 ))"
  echo $num                    # 203
  let "num = (( 200 | 11 ))"
  echo $?                      # 0     ***

  # "let" 结构的退出状态与双括号算术扩展的退出状态是相同的。
  ```

- `if/then` 结构是用来检测一系列命令的 [退出状态](http://tldp.org/LDP/abs/html/exit-status.html#EXITSTATUSREF) 是否为 0（按 UNIX 惯例,退出码 0 表示命令执行成功），如果为 0，则执行接下来的一个或多个命令。即`if` 不仅可以用来测试括号内的条件表达式，**还可以用来测试其他任何命令**。

  ```shell
  # 下面介绍一个非常实用的 “if-grep" 结构：
  # -----------------------------------
  if grep -q Bash file
  # 使用 -q 选项消去 grep 的输出结果
    then echo "File contains at least one occurrence of Bash."
  fi

  word=Linux
  letter_sequence=inu
  if echo "$word" | grep -q "$letter_sequence"
  # 使用 -q 选项消去 grep 的输出结果
  then
    echo "$letter_sequence found in $word"
  else
    echo "$letter_sequence not found in $word"
  fi
  ```

- 重定向。

  `scriptname >filename` **将脚本** _scriptname_ 的输出重定向到 _filename_ 中。如果文件存在，那么覆盖掉文件内容。

  `command &>filename` **将命令** _command_ 的标准输出(stdout) 和标准错误输出(stderr) 重定向到 _filename_。

  重定向在用于清除测试条件的输出时特别有效。如：

  ```shell
  if cmp a b &> /dev/null  # 消去输出结果
  then echo "Files a and b are identical."
  else echo "Files a and b differ."
  fi
  ```

- 如果你不确定某个表达式的布尔值，可以用 if 结构进行测试。

  ```shell
  echo "Testing \"0\""
  if [ 0 ]
  then
    echo "0 is true."
  else
    echo "0 is false."
  fi            # 0 为真。


  # if [ 1 ] # 1 为真。
  # if [ -1 ] # -1 为真。
  # if [ ]  # NULL, 空，为假
  ```

  ```shell
  # if [ xyz ] # 字符串，随机字符串为真

  # if [ $xyz ] # 原意是测试 $xyz 是否为空，但是

                    # 现在 $xyz 只是一个没有初始化的变量。
                    # 未初始化变量含有null空值，为假。

  # if [ -n "$xyz" ] # 更加准确的写法，未初始化变量为假

  # if [ -n "$xyz" ] # xyz= # 初始化为空，空变量为假

  # if [ "false" ] # "false" 只是一个字符串，"false" 为真

  # if [ "$false" ] # 未初始化的变量，"$false" 为假。
  ```

- 如果把 `if` 和 `then` 写在同一行时，则必须在 `if` 语句后加上一个分号来结束语句。因为 `if` 和 `then` 都是 [关键字](http://tldp.org/LDP/abs/html/internal.html#KEYWORDREF)。以关键字（或者命令）开头的语句，必须先结束该语句(分号;)，才能执行下一条语句。

  ```shell
  if [ condition-true ]
  then
     command 1
     command 2
     ...
  fi

  # 或

  if [ -x "$filename" ]; then
  ```

- `elif` 是 `else if` 的缩写。可以把多个 `if/then` 语句连到外边去，更加简洁明了。

  ```shell
  if [ condition1 ]
  then
     command1
     command2
  elif [condition2 ]
  # 等价于 else if
  then
     command3
     command4
  else
     default-command
  fi
  ```

- `test` 和 `[` 都是 bash 的内建命令。 `if test condition-true` 完全等价于 `if [ condition-true ]`。当语句开始执行时，**左括号 `[` 是作为调用 `test` 命令的标记**，而右括号则不严格要求，但在新版本的 Bash 里，右括号必须补上。

  `test`，`/usr/bin/test`，`[]` 和 `/usr/bin/[` 是等价的。

  ```shell
  # if test -z "$1"

  # if /usr/bin/test -z "$1"      # 等价于内建命令 "test"
  #  ^^^^^^^^^^^^^              # 指定全路径

  # if [ -z "$1" ]                # 功能和上面的代码相同。
  #   if [ -z "$1"                理论上可行，但是 Bash 会提示缺失右括号

  # if /usr/bin/[ -z "$1" ]       # 功能和上面的代码相同。
  # if /usr/bin/[ -z "$1"       # 理论上可行，但是会报错
  #                             # 已经在 Bash 3.x 版本被修复了
  ```

- 在 Bash 里，`[[ ]]` 是比 `[ ]` 更加通用的写法。其作为扩展`test` 命令从 ksh88 中被继承了过来。

  在 `[[` 和 `]]` 中不会进行文件名扩展或字符串分割，但是可以进行参数扩展和命令替换。

  ```shell
  file=/etc/passwd

  if [[ -e $file ]]
  then
    echo "Password file exists."
  fi
  ```

  使用 `[[...]]` 代替 `[...]`可以避免很多逻辑错误。比如可以在 `[[]]` 中使用 `&&`，`||`，`<` 和 `>` 运算符，而在 `[]` 中使用会报错。在 `[[]]` 中会自动执行八进制和十六进制的进制转换操作。

  ```shell
  decimal=15
  octal=017   # = 15 (十进制)
  hex=0x0f    # = 15 (十进制)

  if [ "$decimal" -eq "$octal" ]
  then
    echo "$decimal equals $octal"
  else
    echo "$decimal is not equal to $octal"       # 15 不等于 017
  fi      # 在单括号 [ ] 之间不会进行进制转换。

  if [[ "$decimal" -eq "$octal" ]]
  then
    echo "$decimal equals $octal"                # 15 等于 017
  else
    echo "$decimal is not equal to $octal"
  fi      # 在双括号 [[ ]] 之间会进行进制转换。
  ```

- 语法上并不严格要求在 `if` 之后一定要写 `test` 命令或者测试结构（`[]` 或 `[[]]`）。

  ```shell
  dir=/home/bozo

  if cd "$dir" 2>/dev/null; then   # "2>/dev/null" 重定向消去错误输出。
    echo "Now in $dir."
  else
    echo "Can't change to $dir."
  fi
  ```

  `if COMMAND` 的退出状态就是`COMMAND` 的退出状态。

- [`(( ))` 结构](http://tldp.org/LDP/abs/html/dblparens.html) 扩展和执行算术表达式。如果执行结果为 0，其返回的 [退出状态码](http://tldp.org/LDP/abs/html/exit-status.html#EXITSTATUSREF) 为 1（假）。非 0 表达式返回的退出状态为 0（真）。这与上述所使用的 `test` 和 `[ ]` 结构形成鲜明的对比。

  ```shell
  # (( ... )) 结构执行并测试算术表达式。
  # 与 [ ... ] 结构的退出状态正好相反。

  (( 0 ))
  echo "Exit status of \"(( 0 ))\" is $?."         # 1

  (( 1 ))
  echo "Exit status of \"(( 1 ))\" is $?."         # 0
  ```

- 文件测试操作

  - `-e`：检测文件是否存在。`-a` 已被弃用，不推荐
  - `-f`：文件是常规文件(regular file)，而非目录或 [设备文件](http://tldp.org/LDP/abs/html/devref1.html#DEVFILEREF)
  - `-d`：文件是一个目录
  - `-h`：文件是一个 [符号链接](http://tldp.org/LDP/abs/html/basic.html#SYMLINKREF)
  - `-r`：该文件对执行测试的用户可读
  - ...

- 整数比较

  - `-eq`：等于。如 `if [ "$a" -eq "$b" ]`
  - 其他如 `-ne`，`-gt`，`-ge`，`-lt`，`-ge`
  - `<`：小于（使用 [双圆括号](http://tldp.org/LDP/abs/html/dblparens.html)）。如 `(("$a" < "$b"))`
  - 其他如 `<=`，`>`，`>=`

- 字符串比较

  - `=`：等于。如 `if [ "$a" = "$b" ]`，**注意在`=`前后要加上空格**。`if [ "$a"="$b" ]` 和上面不等价（会被当成判断随机字符串，固定为真）。

    ```shell
    if [ "$string1" = "$string2" ]
    then
       command
    fi

    #  [ "X$string1" = "X$string2" ] 这样写是安全的,<<<<====
    #  这样写可以避免任意一个变量为空时的报错。<<<<==== 实测没遇到报错
    #  (变量前加的"X"字符规避了变量为空的情况)
    ```

  - `==`：等于，和 `=` 同义，如 `if [ "$a" == "$b" ]`。**`==` 运算符在双方括号和单方括号里表现不同**。

    ```shell
    [[ $a == z* ]]   # $a 以 "z" 开头时为真（模式匹配）
    [[ $a == "z*" ]] # $a 等于 z* 时为真（字符匹配）

    [ $a == z* ]     # 发生文件匹配和字符分割。
    [ "$a" == "z*" ] # $a 等于 z* 时为真（字符匹配）
    ```

  - 其他如 `!=`，`<`，`>`，`<>`，`-z`，`-n`。注意**使用 `-n` 时字符串必须是在括号中且被引用的**。使用 `! -z` 判断未引用的字符串或者直接判断（样例 7-6）通常可行，但是非常危险。判断字符串时一定要引用。

- 算术比较和字符串比较

  ```shell
  a=4
  b=5

  # 这里的 "a" 和 "b" 可以是整数也可以是字符串。
  # 因为 Bash 的变量是弱类型的，因此字符串和整数比较有很多相同之处。

  # 在 Bash 中可以用处理整数的方式来处理全是数字的字符串。
  # 但是谨慎使用。

  echo

  if [ "$a" -ne "$b" ]
  then
    echo "$a is not equal to $b"
    echo "(arithmetic comparison)"
  fi

  # 在这个例子里 "-ne" 和 "!=" 都可以。
  ```

- 如果字符串未被初始化，则其值是未定义的。这种状态就是空 "null"（并不是 0）。

  ```shell
  #!/bin/bash

  if [ -n $string1 ]    # 并未声明或是初始化 string1。
  then
    echo "String \"string1\" is not null."
  else
    echo "String \"string1\" is null."
  fi
  # 尽管没有初始化 string1，但是结果显示其非空。

  if [ -n "$string1" ]   # 这次引用了 $string1。
  then
    echo "String \"string1\" is not null."
  else
    echo "String \"string1\" is null."
  fi                    # 在测试括号内引用字符串，结果为空。
  ```

- 复合比较

  - `-a`：逻辑与。`exp1 -a exp2` 返回真当且仅当 `exp1` 和 `exp2` 均为真。
  - `-o`：逻辑或。如果 `exp1` 或 `exp2` 为真，则 `exp1 -o exp2` 返回真。

  以上两个操作和 双方括号结构 中的 Bash 比较运算符号 `&&` 和 `||` 类似。`[[ condition1 && condition2 ]]`

  测试操作 `-o` 和 `-a` 可以在 [`test`](http://tldp.org/LDP/abs/html/testconstructs.html#TTESTREF) 命令或在测试括号中进行。但 **&& 和 || 具备“短路”机制**，而 -a 和 -o 则不是。

- 算术运算符常用于`expr`或`let`表达式中。

- Bash 版本 >= 2.05b, Bash 支持了 64-bit 整型数。注意，Bash 并不支持浮点运算，Bash 会将带小数点的数看做字符串。如果你想在脚本中使用浮点数运算，借助[bc](http://tldp.org/LDP/abs/html/mathc.html#BCREF)或外部数学函数库吧。

- 逻辑表达式：`!`，`&&`，`||`

  ```shell
  if [ $condition1 ] && [ $condition2 ]
  #  等同于:  if [ $condition1 -a $condition2 ]
  #  返回true如果 condition1 和 condition2 同时为真...

  if [[ $condition1 && $condition2 ]]    # 可行
  #  注意，&& 运算符不能用在[ ... ]结构里。

  # || 跟 && 一样。
  ```

- 通常情况下，shell 脚本会把数字以十进制整数看待(base 10)，除非数字加了特殊的前缀或标记。 带前缀 0 的数字是八进制数(base 8)；带前缀 0x 的数字是十六进制数(base 16)。 内嵌 # 的数字会以 BASE#NUMBER 的方式进行求值（不能超出当前 shell 支持整数的范围）。

  ```shell
  # 八进制数: 带前导'0'的数
  let "oct = 032"
  echo "octal number = $oct"               # 26
  # 结果以 十进制 打印输出了。

  # 其他进制数: BASE#NUMBER
  # BASE 范围:  2 - 64
  # NUMBER 必须以 BASE 规定的正确形式书写，如下:

  let "bin = 2#111100111001101"
  echo "binary number = $bin"              # 31181

  let "b32 = 32#77"
  echo "base-32 number = $b32"             # 231

  let "b64 = 64#@_"
  echo "base-64 number = $b64"             # 4031

  # 这种表示法只对进制范围(2 - 64)内的 ASCII 字符有效。
  # 10 数字 + 26 小写字母 + 26 大写字母 + @ + _
  ```

- 双圆括号结构

  与`let`命令类似，`(( ... ))` 结构允许**对算术表达式的扩展和求值**。它**是`let`命令的简化形式**。例如，a=$(( 5 + 3 )) 会将变量 a 赋值成 5 + 3，也就是 8。在 Bash 中，双圆括号结构也允许以 C 风格的方式操作变量。例如，(( var++ ))。

- **运算符优先级**

  - 先乘除取余，后加减，与算数运算相似
  - 复合逻辑运算符，&&, ||, -a, -o 优先级较低
  - 优先级相同的操作按*从左至右*顺序求值

## Bash 基本功能（多命令顺序执行)

<https://www.cnblogs.com/liuyuelinfighting/p/16082830.html>

# shell 脚本实践

## 执行二进制命令

shell 中执行二进制命令，并根据二进制命令设置 shell 脚本的返回值

```shell
# Execute command
ls -la .

# Check exit status and print error if failed
if [ $? -ne 0 ]; then
    echo "Error: xxx command failed. Exiting..."
    exit 1  # Exit with a non-zero status to indicate failure
fi

# If no error, continue with the script
echo "xxx command executed successfully."
exit 0  # Exit with status 0 if everything is okay
```
