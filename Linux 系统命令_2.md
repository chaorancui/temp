[toc]

# Linux 相关网址记录

1. [Linux Tools Quick Tutorial](https://linuxtools-rst.readthedocs.io/zh-cn/latest/base/index.html)

# 终端设置命令

## alias 命令

`alias` 命令是 Linux 和类 Unix 系统中用于为常用命令创建别名的命令。通过 `alias`，你可以将复杂的命令简化为更简短、更易记的命令，或者为某些命令指定默认的选项或参数。

**基本语法**：

```bash
alias <别名>=<命令>
```

- `<别名>`：你希望创建的短名称（即你将用来代替完整命令的名字）。
- `<命令>`：你希望别名代表的完整命令（包括可选的参数或选项）。

> 注意：
>
> `alias` 是可以嵌套的，也就是说，你可以在一个别名的定义中使用另一个别名。定义别名时**不能**出现**别名中直接引用自己**或者**存在无限递归**的情况。

**示例**：

1. 创建一个简单的别名

   ```bash
   alias ll='ls -l'
   ```

   这个命令将 `ll` 设置为 `ls -l` 的别名。之后，你只需要输入 `ll`，就会执行 `ls -l`，显示文件的详细信息。

2. 创建带参数的别名

   ```bash
   alias gs='git status'
   ```

   这里，`gs` 成为 `git status` 命令的别名，简化了 Git 命令的输入。

3. 别名包含多个命令

   你还可以创建一个别名来执行多个命令。例如，如果你想每次进入某个目录时都自动列出目录内容并打开一个编辑器：

   ```bash
   alias goedit='cd /path/to/project && ls -l && vim .'
   ```

   这个别名会执行 `cd` 进入指定目录，列出该目录下的文件，并启动 `vim` 编辑器打开当前目录。

4. 查看已定义的别名

   要查看当前 shell 会话中已定义的所有别名，可以简单地输入：

   ```bash
   alias
   ```

   这将显示当前用户为所有常用命令定义的别名。例如，默认情况下，很多系统可能会为 `ls` 和其他命令定义一些常见别名，如：

   ```bash
   alias ls='ls --color=auto'
   alias ll='ls -alF'
   ```

5. 删除别名

   如果你不再需要某个别名，可以使用 `unalias` 命令删除它：

   ```bash
   unalias <别名>
   ```

   例如，删除 `ll` 别名：

   ```bash
   unalias ll
   ```

   如果你想删除所有别名，可以使用：

   ```bash
   unalias -a
   ```

6. 使别名永久生效

   默认情况下，通过 `alias` 创建的别名只会在当前 shell 会话中有效。如果你希望在每次打开终端时都能使用某些别名，需要将它们添加到你的 shell 配置文件中。

   对于 **Bash** 用户，通常是将别名添加到 `~/.bashrc` 文件中：

   ```bash
   echo "alias ll='ls -l'" >> ~/.bashrc
   source ~/.bashrc
   ```

   对于 **Zsh** 用户，可以将别名添加到 `~/.zshrc` 文件：

   ```bash
   echo "alias gs='git status'" >> ~/.zshrc
   source ~/.zshrc
   ```

**常见的 `alias` 用法**

1. **列出文件和目录（详细模式）：**

   ```bash
   alias ll='ls -alF'
   ```

2. **避免误用 `rm` 命令（加上 `-i` 选项，确认删除）：**

   ```bash
   alias rm='rm -i'
   ```

3. **查看目录大小：**

   ```bash
   alias du='du -h --max-depth=1'
   ```

4. **查找并列出文件的 `man` 页面：**

   ```bash
   alias man='man -a'
   ```

5. **快速跳转到主目录：**

   ```bash
   alias home='cd ~'
   ```

6. **查看网络接口信息：**

   ```bash
   alias ifconfig='ifconfig -a'
   ```

**注意事项**：

- 别名 **不能包含空格**，例如，`alias gs = 'git status'` 是不合法的，应该写成 `alias gs='git status'`。
- 在一些命令中，使用别名可能会导致预期以外的行为。特别是，当你使用诸如 `sudo` 之类的命令时，默认情况下别名不会被应用。可以通过 `sudo` 加 `-E` 选项让 `sudo` 执行时保留用户的环境变量（包括别名），但这通常不推荐，因可能影响系统安全性。

**总结**：

`alias` 是一个非常有用的命令，能够帮助用户自定义并简化常用的命令。通过合理使用别名，可以提高工作效率，使得命令的输入更加便捷。不过，别名的使用要适度，避免产生不必要的混淆，特别是在涉及系统级命令时。

# 文件查找/匹配命令

## find 命令和 grep 命令区别

find 也是搜索命令，那么 find 命令和 grep 命令有什么区别呢？
find 命令
find 命令用于在系统中搜索符合条件的文件名，如果需要模糊查询，则使用通配符进行匹配，通配符是完全匹配（find 命令可以通过-regex 选项，把匹配规则转为正则表达式规则，但是不建议如此）。
grep 命令
grep 命令用于在文件中搜索符合条件的字符串，如果需要模糊查询，则使用正则表达式进行匹配，正则表达式是包含匹配。

## find 命令

`find` 是 Linux / Unix 系统中非常强大的命令行工具之一，可实现：

- 精准搜索（按名称、时间、权限、大小等）；
- 灵活组合条件（使用逻辑操作）；
- 执行各种动作（复制、删除、移动、统计等）；

可用 `find --help` 查看命令帮助文档。

**一、基本格式**

```bash
Usage: find [-H] [-L] [-P] [-Olevel] [-D debugopts] [path...] [expression]

# 中文：
用法：find [选项] [起始路径...] [表达式]

说明：
- `path`：要搜索的路径，默认为当前目录（`.`）；
- `expression`：匹配条件，默认是 `-print`（即列出路径）；
```

**二、表达式类型说明**

**表达式可以包含以下部分**：

- 操作符（operators）
- 选项（options）
- 测试条件（tests）
- 动作（actions）

1. **操作符（operators）**

   用于组合或控制多个条件的逻辑关系：

   ```bash
   ( EXPR )        —— 括号分组（要加反斜线：`\(` `\)`）
   ! EXPR          —— 逻辑非
   -not EXPR       —— 等价于 `!`
   EXPR1 -a EXPR2  —— 逻辑与（可省略）
   EXPR1 -and EXPR2 —— 同上
   EXPR1 -o EXPR2  —— 逻辑或
   EXPR1 -or EXPR2 —— 同上
   EXPR1 , EXPR2   —— 顺序执行 EXPR1 再执行 EXPR2（不管 EXPR1 成功与否）
   ```

2. **位置相关选项（positional options）**

   这些选项**总是返回 true**，必须写在表达式之前：

   ```bash
   -daystart         —— 以当天凌晨为时间计算起点
   -follow           —— 跟踪符号链接（等价于 `-L`）
   -regextype        —— 设置正则表达式语法类型（例如 `posix-extended`）
   ```

3. **常规选项（normal options）**

   也是总是为 true 的，必须在其他条件之前写：

   ```bash
   -depth               —— 先处理文件，再处理目录（深度优先）
   --help               —— 显示帮助信息
   -maxdepth LEVELS     —— 最大搜索层级
   -mindepth LEVELS     —— 最小搜索层级
   -mount / -xdev       —— 不跨越挂载点
   -noleaf              —— 不假设目录结构优化（对非 GNU 系统有用）
   --version            —— 显示版本
   -ignore_readdir_race —— 忽略读取目录竞争条件
   -noignore_readdir_race —— 不忽略读取目录竞争
   ```

4. **测试条件（tests）**

   这些条件用于匹配文件特征：

   | 参数                                      | 说明                              |
   | ----------------------------------------- | --------------------------------- |
   | `-name PATTERN`                           | 按文件名匹配（支持通配符）        |
   | `-iname PATTERN`                          | 不区分大小写的文件名匹配          |
   | `-regex PATTERN`                          | 使用正则表达式**匹配整个路径**    |
   | `-size N[单位]`                           | 文件大小，单位如 `k`、`M`、`G` 等 |
   | `-mtime N`                                | 修改时间（按天）                  |
   | `-atime N`                                | 访问时间（按天）                  |
   | `-ctime N`                                | 状态变更时间（按天）              |
   | `-mmin N`                                 | 修改时间（按分钟）                |
   | `-type f` / `d`                           | 文件 / 目录                       |
   | `-user NAME`                              | 文件属主                          |
   | `-group NAME`                             | 文件属组                          |
   | `-perm MODE`                              | 权限匹配                          |
   | `-empty`                                  | 空目录或空文件                    |
   | `-false` / `-true`                        | 总是假 / 总是对                   |
   | `-readable` / `-writable` / `-executable` | 是否可读 / 可写 / 可执行          |

   说明：

   - `N` 可以是 `+N`（大于），`-N`（小于），`N`（等于）。
   - 正则表达式中，如果想要匹配**特殊字符则需要转义**，如 `* . ? + $ ^ [ ] ( ) { } | \ /`，。

5. **动作（actions）**

   对匹配文件执行的操作：

   | 参数                  | 功能                                       |
   | --------------------- | ------------------------------------------ |
   | `-print`              | 打印路径（默认动作）                       |
   | `-ls`                 | 类似 `ls -l` 的详细列表                    |
   | `-delete`             | 删除匹配文件（⚠️ 危险操作）                |
   | `-exec COMMAND {} \;` | 对每个文件执行命令（如：`cp {} /backup/`） |
   | `-exec ... +`         | 一次性对多个文件执行命令（更高效）         |
   | `-ok`                 | 类似 `-exec`，但执行前会提示确认           |
   | `-prune`              | 跳过该目录（常用于排除路径）               |

6. **-D 调试选项**

   ```bash
   -D exec,opt,rates,search,stat,time,tree,all,help
   ```

   用于调试 `find` 行为，一般不常用，比如：

   - `-D exec` 显示执行命令的详细过程；
   - `-D tree` 显示目录结构遍历过程；
   - `-D help` 显示所有调试项说明。

**三、查找条件（匹配过滤）总结**

**文件名相关**

- `-name` | `-name "*.log"` | 按名字（通配符）查找 |
- `-iname` | `-iname "*.LOG"` | 不区分大小写 |
- `-regex` | `-regex '.*\.log'` | 使用正则表达式匹配路径 |
- `-regextype` | `-regextype posix-extended` | 设定正则语法类型（配合 `-regex`） |

**类型相关**

- `-type f` | 查找普通文件 | |
- `-type d` | 查找目录 | |
- `-type l` | 查找符号链接 | |
- `-type b/c` | 块/字符设备文件 | |

**时间相关**

- `-mtime +7` | 7 天前修改的文件 | |
- `-atime -1` | 1 天内被访问的文件 | |
- `-newer file` | 比指定文件更新的文件 | |

**大小相关**

- `-size +100M` | 大于 100MB 的文件 | |
- `-size -10k` | 小于 10KB 的文件 | |

**权限/用户相关**

- `-user root` | 属主是 root 的文件 | |
- `-group dev` | 属组是 dev 的文件 | |
- `-perm 644` | 权限为 644 的文件 | |

**搜索控制**

- `-maxdepth 1` | 只搜索当前目录，不进入子目录 | |
- `-mindepth 2` | 跳过前几层，只搜索更深层 | |

**操作动作（对匹配结果的处理）**

- `-print` | 输出文件路径（默认行为） | |
- `-exec` | `-exec rm {} \;`：对每个文件执行操作 | |
- `-ok` | 类似 `-exec`，但每次操作前询问确认 | |
- `-delete` | 删除匹配的文件或目录（**需谨慎！**） | |

**四、典型场景**

| 任务                          | 命令                                        |
| ----------------------------- | ------------------------------------------- |
| 查找当前目录下所有 `.c` 文件  | `find . -name "*.c"`                        |
| 查找 7 天内修改的 `.log` 文件 | `find . -name "*.log" -mtime -7`            |
| 查找大于 100MB 的文件         | `find . -type f -size +100M`                |
| 删除所有空目录                | `find . -type d -empty -delete`             |
| 拷贝所有包含 `_0_` 的文件     | `find . -name "*_0_*" -exec cp {} /dst/ \;` |

一、查找路径/文件

| 任务                                     | 命令                                         |
| ---------------------------------------- | -------------------------------------------- |
| 查找所有 `.log` 文件                     | `find /path/to/search -type f -name "*.log"` |
| 查找最近 3 天内修改过的文件              | `find /path/to/search -type f -mtime -3`     |
| 查找文件大小大于 100MB 的文件            | `find /path/to/search -type f -size +100M`   |
| 查找目录（比如项目根目录下的所有子目录） | `find /path/to/search -type d -maxdepth 1`   |

二、查找后本地 `cp` 拷贝

| 任务                                                 | 命令                                                                                     |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 拷贝所有 `.txt` 到指定目录                           | `find . -type f -name "*.txt" -exec cp {} /backup/ \;`                                   |
| 拷贝匹配正则文件名（如：`data_0001_0_*`）            | `find . -regextype posix-extended -regex './data_[0-9]{4}_0_.*' -exec cp {} /backup/ \;` |
| 保留原目录结构地拷贝文件（推荐用 `rsync` 替代 `cp`） | `find ./src -type f -name "\*.conf" -exec rsync -R {} /backup/ \;`                       |
| 自动创建目标目录（本地）                             | `find . -name "*.txt" -exec cp {} /backup/dir/ \;`                                       |
| 使用 `basename` 改文件名或只拷贝文件本身             | `find . -type f -name "*.txt" -exec sh -c 'cp "$1" /target/$(basename "$1")' _ {} \;`    |

> `rsync -R` 会保留源路径结构（如 `src/app/a.conf` 复制为 `backup/src/app/a.conf`）

三、查找后远程拷贝（scp / rsync）

| 任务                                      | 命令                                                                             |
| ----------------------------------------- | -------------------------------------------------------------------------------- |
| 使用 `scp` 拷贝所有 `.log` 文件到远程主机 | `find . -type f -name "*.txt" -exec cp {} /backup/ \;`                           |
| 使用 `rsync` 批量拷贝并保留目录结构       | `find ./data -type f -name "*.bin" -exec rsync -R {} user@host:/remote/data/ \;` |
| `scp` 加速小技巧（用 `xargs` 批量处理）   | `find . -name "\*.cfg" \| xargs -I {} scp {} user@host:/remote/configs/`         |

## grep 命令

`grep` 是 Linux / Unix 系统中一个非常常用的命令行工具，用于 **搜索文件中符合条件的字符串**。它基于正则表达式进行匹配，并输出包含匹配内容的行。

**一、基本语法**

```bash
grep [选项] '搜索字符串或正则表达式' 文件名
```

**二、常用参数详解**

| 参数        | 说明                                     |
| ----------- | ---------------------------------------- |
| `-i`        | 忽略大小写（ignore case）                |
| `-v`        | 反向选择，显示不匹配的行（invert match） |
| `-n`        | 显示匹配行的行号（line number）          |
| `-r` / `-R` | 递归搜索目录（recursive）                |
| `-l`        | 只列出匹配的文件名（list file names）    |
| `-L`        | 列出不含匹配内容的文件名                 |
| `-c`        | 只输出匹配的行数（count）                |
| `-o`        | 只输出匹配的部分（而非整行）             |
| `-e`        | 支持多个匹配模式（pattern）              |
| `-w`        | 精确匹配整个单词（word match）           |
| `-A N`      | 匹配行后输出 N 行（after）               |
| `-B N`      | 匹配行前输出 N 行（before）              |
| `-C N`      | 匹配行前后各输出 N 行（context）         |
| `--color`   | 高亮显示匹配字符串（彩色显示）           |

**三、示例用法**

```bash
# 1. 在文件中查找包含 "hello" 的行：
grep 'hello' file.txt

# 2. 忽略大小写查找：
grep -i 'hello' file.txt

# 3. 显示行号：
grep -n 'hello' file.txt

# 4. 查找不包含某字符串的行：
grep -v 'hello' file.txt

# 5. 递归查找整个目录：
grep -r 'hello' /path/to/dir

# 6. 查找多个关键词：
grep -e 'hello' -e 'world' file.txt

# 7. 只输出匹配内容本身：
grep -o 'hello' file.txt

# 8. 统计匹配的行数：
grep -c 'hello' file.txt

# 9. 匹配行及前后内容：
grep -C 2 'hello' file.txt
```

四、正则表达式支持（基础）：

| 表达式 | 含义                      |
| ------ | ------------------------- |
| `.`    | 匹配任意单个字符          |
| `*`    | 匹配前一个字符 0 次或多次 |
| `^`    | 匹配行开头                |
| `$`    | 匹配行结尾                |
| `[]`   | 匹配字符集合              |
| `[^]`  | 匹配不在集合中的字符      |
| `\`    | 转义字符                  |
| `      | `                         |

> 如果你需要更强大的正则支持，可以使用 `grep -E`（等同于 `egrep`），支持扩展正则（如 `+`, `{m,n}`, `()` 等）。

## 常用 grep 命令速查表

**一、基本语法**

```bash
Usage: grep [OPTION]... PATTERNS [FILE]...
Search for PATTERNS in each FILE.
Example: grep -i 'hello world' menu.h main.c
PATTERNS can contain multiple patterns separated by newlines.
```

**二、匹配相关**

| 命令                      | 含义                 |
| ------------------------- | -------------------- |
| `grep 'text' file.txt`    | 查找包含 "text" 的行 |
| `grep -i 'text' file.txt` | 忽略大小写查找       |
| `grep -w 'text' file.txt` | 匹配整个单词         |
| `grep -x 'text' file.txt` | 匹配整行             |
| `grep -E 'foo             | bar' file.txt`       |
| `grep -o 'text' file.txt` | 只输出匹配部分       |

**三、文件和目录**

| 命令                      | 含义                   |
| ------------------------- | ---------------------- |
| `grep 'text' file1 file2` | 在多个文件中查找       |
| `grep -r 'text' dir/`     | 递归搜索目录           |
| `grep -l 'text' *.log`    | 仅显示匹配的文件名     |
| `grep -L 'text' *.log`    | 显示不包含匹配的文件名 |

**四、输出控制**

| 命令                           | 含义                       |
| ------------------------------ | -------------------------- |
| `grep -n 'text' file.txt`      | 显示匹配行的行号           |
| `grep -c 'text' file.txt`      | 显示匹配的行数             |
| `grep -v 'text' file.txt`      | 显示不包含匹配的行         |
| `grep --color 'text' file.txt` | 高亮匹配文本               |
| `grep -H 'text' file.txt`      | 显示文件名（默认多文件时） |
| `grep -h 'text' file.txt`      | 不显示文件名（用于多文件） |

**五、匹配上下文**

| 命令                        | 含义                  |
| --------------------------- | --------------------- |
| `grep -A 3 'text' file.txt` | 匹配行及其后 3 行     |
| `grep -B 3 'text' file.txt` | 匹配行及其前 3 行     |
| `grep -C 3 'text' file.txt` | 匹配行及其前后各 3 行 |

**六、高级用法**

| 命令                  | 含义               |
| --------------------- | ------------------ |
| `ps aux               | grep nginx`        |
| `dmesg                | grep -i error`     |
| `find . -name "\*.py" | xargs grep 'main'` |

**七、正则表达式速览（基础）**

| 符号     | 意义                     |
| -------- | ------------------------ |
| `.`      | 匹配任意单字符           |
| `*`      | 匹配前一个字符零次或多次 |
| `^`      | 匹配行开头               |
| `$`      | 匹配行结尾               |
| `[abc]`  | 匹配 a 或 b 或 c         |
| `[^abc]` | 匹配不是 a/b/c 的字符    |
| `\`      | 转义字符                 |
| `        | `                        |

**八、示例组合**

```bash
grep -ir 'error' /var/log/             # 忽略大小写递归搜索日志
grep -nA2 'fail' app.log               # 显示匹配和之后2行
grep -Ev '^#|^$' config.txt            # 去除注释和空行
```

## 通配符与正则表达式的区别

**通配符：用于匹配文件名，完全匹配**。

| 通配符 | 作用                                                                                    |
| ------ | --------------------------------------------------------------------------------------- |
| ？     | 匹配一个任意字符                                                                        |
| \*     | 匹配 0 个或任意多个任意字符，也就是可以匹配任何内容                                     |
| []     | 匹配中括号中任意一个字符。例如，[abc]代表一定匹配一个字符，或者是 a，或者是 b，或者是 c |
| [-]    | 匹配中括号中任意一个字符，-代表一个范围。例如，[a-z]代表匹配一个小写字母                |
| [^]    | 逻辑非，表示匹配不是中括号内的一个字符。例如， `[^0-9]`代表匹配一个不是数字的字符       |

**正则表达式：用于匹配字符串，包含匹配**。

| 正则符 | 作用                                                                                    |
| ------ | --------------------------------------------------------------------------------------- |
| ？     | 匹配一个任意字符                                                                        |
| \*     | 匹配 0 个或任意多个任意字符，也就是可以匹配任何内容                                     |
| []     | 匹配中括号中任意一个字符。例如，[abc]代表一定匹配一个字符，或者是 a，或者是 b，或者是 c |
| [-]    | 匹配中括号中任意一个字符，-代表一个范围。例如，[a-z]代表匹配一个小写字母                |
| [^]    | 逻辑非，表示匹配不是中括号内的一个字符。例如， `[^0-9]`代表匹配一个不是数字的字符       |
| ^      | 匹配行首                                                                                |
| $      | 匹配行尾                                                                                |

> [Linux grep 命令和通配符](https://blog.csdn.net/baidu_41388533/article/details/107610827)

## sort 命令

`sort` 是 Linux 中一个非常实用的命令，用于对文本文件中的 **行** 进行排序。它支持按字典序、数值大小、月份、版本号、人类可读大小等多种方式排序。

**一、基本语法**

```bash
sort [选项] [文件...]
```

如果不指定文件，`sort` 会从标准输入读取数据，也可以用管道输入。

**常用选项详解**

| 选项           | 说明                                       |
| -------------- | ------------------------------------------ |
| `-n`           | 按**数值**排序（Number）                   |
| `-h`           | 按**人类可读大小**排序（比如 1K, 2M）      |
| `-r`           | **逆序**排序（reverse）                    |
| `-k`           | 指定**按第几列**排序（支持范围如 `-k2,2`） |
| `-t`           | 指定列之间的**分隔符**（默认是空格或 Tab） |
| `-u`           | 去重（只输出唯一行）                       |
| `-o`           | 指定**输出文件**                           |
| `-M`           | 按**月份**排序（如 Jan, Feb...）           |
| `-V`           | 按**版本号**排序（1.2.9 < 1.10.2）         |
| `--parallel=N` | 使用 N 个线程进行排序（大文件有用）        |
| `-b`           | 忽略每行前导空格进行排序                   |

**二、排序类型对比**

| 类型     | 示例选项  | 示例内容        | 排序顺序        |
| -------- | --------- | --------------- | --------------- |
| 字典序   | `sort`    | apple, cat, boy | a → z           |
| 数字     | `sort -n` | 10, 2, 33       | 2 → 10 → 33     |
| 人类大小 | `sort -h` | 1K, 5M, 900B    | 900B → 1K → 5M  |
| 月份     | `sort -M` | Jan, Feb, Dec   | Jan → Feb → Dec |
| 版本号   | `sort -V` | v1.9, v1.10     | v1.9 → v1.10    |

**三、常用实例**

1. 按字典序排序文件内容

   ```bash
   sort filename.txt
   ```

2. 按数值排序（比如第二列是数字）

   ```bash
   sort -k2 -n filename.txt
   ```

3. 按文件大小（人类可读）排序

   ```bash
   du -h --max-depth=1 | sort -hr
   ```

4. 按版本号排序

   ```bash
   sort -V versions.txt
   ```

5. 按某列（比如以冒号分隔）排序

   ```bash
   sort -t ':' -k3 -n file.txt
   ```

6. 逆序 + 数值排序 + 取前 10 行

   ```bash
   sort -nr filename.txt | head -n 10
   ```

7. 去重排序

   ```bash
   sort -u filename.txt
   ```

**注意事项**

- `sort` 是**基于行**的排序工具。
- 默认排序是按**整行**的字典序。
- 使用 `-k` 时，**列的范围非常重要**，如 `-k2,2` 表示只看第二列。
- 如果使用 `sort` 对大文件操作，建议配合 `--parallel` 和临时目录优化，如：

  ```bash
  sort --parallel=4 -T /tmp bigfile.txt
  ```

## ripgrep 工具

`rg` 是 **ripgrep** 的命令行工具缩写，它是一个用 Rust 写的文本搜索工具，主要功能和 `grep` 类似，但速度更快，特别适合在大规模代码仓库里查找。

**一、ripgrep (`rg`) 的特点**

1. **高性能**
   - 使用 Rust 实现，性能优于传统 `grep` 和 `ack`。
   - 内置了对 `.gitignore` 的支持，会自动忽略 Git 忽略的文件。
2. **默认递归搜索**
   - 不需要额外加 `-r`，直接递归子目录。
3. **智能文件过滤**
   - 默认只搜索文本文件，自动跳过二进制文件。
   - 支持 `--type` 选项，比如 `--type py` 只搜索 Python 文件。
4. **强大的正则支持**
   - 使用 Rust 的 `regex` 库，语法和 PCRE 类似（但不完全一样）。

**二、安装**

1. Linux

   大部分发行版仓库都提供了 `ripgrep` 包：

   ```bash
   # Debian / Ubuntu
   sudo apt update
   sudo apt install ripgrep
   # Arch Linux
   sudo pacman -S ripgrep
   # macOS
   brew install ripgrep
   ```

2. Windows

   - 包管理工具

     ```bash
     # 方法一：用 scoop
     scoop install ripgrep
     # 方法二：用 chocolatey
     choco install ripgrep
     ```

   - 二进制程序安装

     直接从 GitHub Releases 下载预编译二进制：
     <https://github.com/BurntSushi/ripgrep/releases>

**三、用法**

```bash
USAGE:
    rg [OPTIONS] PATTERN [PATH ...]
    rg [OPTIONS] -e PATTERN ... [PATH ...]
    rg [OPTIONS] -f PATTERNFILE ... [PATH ...]
    rg [OPTIONS] --files [PATH ...]
    rg [OPTIONS] --type-list
    command | rg [OPTIONS] PATTERN
    rg [OPTIONS] --help
    rg [OPTIONS] --version
```

示例：

```bash
# 配合正则
rg "func\s+\w+\("
# 限制目录/文件
rg pattern path/to/dir
rg pattern file.txt
```

> :pushpin: `rg` 默认开启行号、默认递归、默认大小写敏感。

`rg` 常用参数速查表：

| 参数                   | 功能                                      | 示例                                              |
| ---------------------- | ----------------------------------------- | ------------------------------------------------- |
| `-i`                   | 忽略大小写（默认大小写敏感）              | `rg -i error log.txt`                             |
| `-n`                   | 显示行号（默认开启，可手动指定）          | `rg -n foo file.txt`                              |
| `-l`                   | 只显示**匹配的文件名**                    | `rg -l TODO`                                      |
| `-L`                   | 显示不包含匹配的文件（哪些文件没写 main） | `rg -L main`                                      |
| `-c`                   | 统计每个文件匹配的次数                    | `rg -c import -t py`                              |
| `-o`                   | 只输出匹配内容                            | `rg -o "\d{4}-\d{2}-\d{2}" log.txt`               |
| `-v`                   | 反向匹配（显示不匹配的行）                | `rg -v DEBUG app.log`                             |
| `-w`                   | 匹配整个单词                              | `rg -w main`                                      |
| `-x`                   | 整行匹配                                  | `rg -x "Hello World"`                             |
| `-t <type>`            | 按**文件类型**搜索                        | `rg foo -t py`                                    |
| `--type-list`          | 列出支持的文件类型                        | `rg --type-list`                                  |
| `--ignore <pattern>`   | 忽略指定文件/目录                         | `rg "pattern" --ignore "*.log" --ignore "build/"` |
| `--ignore-file <file>` | 忽略 <file> 里指定文件/目录               | `rg foo --ignore-file .ignore`                    |
| `--no-ignore`          | 即使 `.gitignore` 忽略的文件也强制搜索    | `rg foo --no-ignore`                              |
| `-a`                   | **强制把二进制**文件当文本搜索            | `rg -a password binary.dat`                       |
| `-U`                   | 启用多行搜索                              | `rg -U "foo\nbar"`                                |
| `--color=always`       | 强制彩色输出                              | `rg --color=always foo`                           |
| `--json`               | 输出 JSON 结果（脚本处理用）              | `rg foo --json`                                   |

代码相关：

| 场景            | 命令                             | 说明                 |
| --------------- | -------------------------------- | -------------------- |
| 查找函数定义    | `rg "def\s+\w+\(" -t py`         | 查找 Python 函数定义 |
| 查找类定义      | `rg "^class\s+\w+" -t py`        | Python 类            |
| 查找 C 函数声明 | `rg "^\w+\s+\w+\(.*\)\s*{" -t c` | C 语言函数           |
| 查找 TODO/FIXME | `rg "TODO \| FIXME"`             | TODO 位置            |
| 查找变量赋值    | `rg "^\s*my_var\s*=" -t py`      | 精确定位变量         |

配置文件 / 日志：

| 场景             | 命令                                          | 说明            |
| ---------------- | --------------------------------------------- | --------------- |
| 查找配置项       | `rg "max_connections" -t conf`                | 找配置参数      |
| 查找日志里的报错 | `rg -i "error" /var/log/syslog`               | 日志排障        |
| 查找 IP 地址     | `rg -o "\b\d{1,3}(\.\d{1,3}){3}\b"`           | 提取日志中的 IP |
| 查找时间戳       | `rg -o "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"` | 抓取日志时间    |

# 文件操作命令

## cp 命令

`cp` 命令是 Linux 中用于复制文件或目录的命令。它是最基本和最常用的命令之一，用于将源文件或源目录复制到目标位置。`cp` 的语法非常简单，但它有一些常用的选项，可以使其更加灵活和强大。

**基本语法：**

```bash
Usage: cp [OPTION]... [-T] SOURCE DEST
  or:  cp [OPTION]... SOURCE... DIRECTORY
  or:  cp [OPTION]... -t DIRECTORY SOURCE...
```

Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.

**常用选项：**

1. **`-r` 或 `--recursive`**：用于递归复制目录。如果源是一个目录，并且你希望复制目录内容及其子目录，那么需要使用这个选项。

   - 示例：`cp -r /home/user/source_dir /home/user/destination_dir`

2. **`-f` 或 `--force`**：强制复制文件，并且如果目标文件无法写入，则会删除目标文件后重新复制。这对于避免覆盖的交互提示非常有用。

   - 示例：`cp -f file1.txt /home/user/destination/`

3. **`-i` 或 `--interactive`**：在目标文件已经存在时，提示用户确认是否覆盖。

   - 示例：`cp -i file1.txt /home/user/destination/`

4. **`-v` 或 `--verbose`**： 显示详细的复制过程，包括源文件和目标文件的路径。

   - 示例：`cp -v file1.txt /home/user/destination/`

5. **`-p` 或 `--preserve`**：保留文件的属性（如修改时间、权限、所有者等）。通常在复制文件时，源文件的权限和时间戳不会被保留，使用该选项可以避免这种情况。
   - 示例：`cp -p file1.txt /home/user/destination/`
6. **`-u` 或 `--update`**：仅在源文件比目标文件更新，或者目标文件不存在时才复制。

   - 示例：`cp -u file1.txt /home/user/destination/`

7. **`-a` 或 `--archive`**：这个选项是 `-dR --preserve=all` 的组合，意味着会复制文件及其所有属性（包括符号链接、文件权限、时间戳等），并且递归地复制目录。

   - 示例：`cp -a source_dir /home/user/destination/`

8. **`-l` 或 `--link`**：创建源文件的硬链接，而不是复制源文件。这意味着多个文件将指向相同的数据块。

   - 示例：`cp -l file1.txt /home/user/destination/`

9. **`--no-clobber`**：如果目标文件已存在，则不复制，不会覆盖目标文件。

   - 示例：`cp --no-clobber file1.txt /home/user/destination/`

**注意：**

`cp` 命令本身**不支持正则表达式**来筛选文件，它只支持通配符（如 `*`、`?`），这是由 shell（比如 bash）进行展开的。

1. 使用通配符匹配文件

   这是最常见的方式，例如：

   ```bash
   cp *.txt /target/dir/
   ```

   会拷贝当前目录下所有 `.txt` 文件。

2. 如果你确实需要用 **正则表达式筛选文件名**，可以结合 `find` 或 `ls | grep` 使用：

   （1）使用 `find` 搭配正则（推荐方式）

   ```bash
   find . -maxdepth 1 -regextype posix-extended -regex './file[0-9]+\.txt' -exec cp {} /target/dir/ \;
   ```

   这会拷贝所有形如 `file123.txt` 的文件。

   （2）使用 `grep` 和 `xargs`

   ```bash
   ls | grep -E '^file[0-9]+\.txt$' | xargs -I {} cp {} /target/dir/
   ```

   这也能实现正则筛选，但 `ls` 对特殊字符（如空格）处理不好，慎用。

## mv 命令

**一、基本语法**

```bash
mv [源文件或目录] [目标文件或目录]
```

**二、重命名的情况**

当 **目标参数不是一个已存在的目录** 时，`mv` 会把源当作一个整体改名：

1. 文件重命名

   ```bash
   mv a.txt b.txt
   ```

   - 如果 `b.txt` **不存在** → `a.txt` 被重命名为 `b.txt`。
   - 如果 `b.txt` **已存在文件** → `a.txt` 会覆盖掉 `b.txt`（默认直接替换，可能提示确认，取决于 `alias mv='mv -i'` 设置）。

2. 目录重命名

   ```bash
   mv dir1 dir2
   ```

   - 如果 `dir2` **不存在** → `dir1` 被重命名为 `dir2`。
   - 如果 `dir2` **已存在且是文件** → 报错（不能把目录移到文件）。

**三、移动的情况**

当 **目标参数是一个已存在的目录** 时，`mv` 会把源放到目标目录里：

1. 移动文件到目录

   ```bash
   mv a.txt dir1/
   ```

   结果：`a.txt` 被移到 `dir1/a.txt`。

2. 移动目录到目录

   ```bash
   mv dir1 dir2/
   ```

   结果：`dir1` 整个目录被移到 `dir2/dir1` 下。

**四、特殊情况**

- **多个源 → 目标必须是目录**

  ```bash
  mv a.txt b.txt c.txt dir1/
  ```

  把 a、b、c 都移到 `dir1/` 下。
  如果 `dir1` 不是目录 → 报错。

- **跨分区移动**
  如果源和目标不在同一个文件系统，`mv` 实际上会做 **拷贝 + 删除**。

**总结**

- **目标不存在** → 重命名。
- **目标存在且是目录** → 移动到该目录下。
- **多个源** → 目标必须是目录，否则报错。

`mv` 命令行为总结表（含示例）

| 源类型                      | 目标路径情况             | 行为结果                                 | 示例命令                          |
| --------------------------- | ------------------------ | ---------------------------------------- | --------------------------------- |
| **文件**                    | 目标不存在               | 文件被**重命名**为目标名                 | `mv a.txt b.txt`                  |
| 文件                        | 目标已存在，且是**文件** | 源文件覆盖目标文件                       | `mv a.txt b.txt` （b.txt 已存在） |
| 文件                        | 目标已存在，且是**目录** | 源文件被移动到该目录下                   | `mv a.txt dir/`                   |
| **目录**                    | 目标不存在               | 源目录被**重命名**为目标名               | `mv dir1 dir2`                    |
| 目录                        | 目标已存在，且是**目录** | 源目录整体被移到目标目录下（变成子目录） | `mv dir1 dir2/`                   |
| 目录                        | 目标已存在，且是**文件** | 报错：不能把目录移到文件                 | `mv dir1 a.txt`                   |
| **多个源（文件/目录混合）** | 目标必须是已存在目录     | 所有源被移动到该目录下                   | `mv a.txt b.txt dir1 target_dir/` |
| 多个源                      | 目标不存在或是文件       | 报错：目标必须是目录                     | `mv a.txt b.txt not_exist/`       |

## install 命令

install 命令与 cp 命令类似，均可以将文件或目录拷贝到指定的路径；但是 install 命令可以控制目标文件的属性。

命令格式

```css
install [OPTION]... [-T] SOURCE DEST
install [OPTION]... SOURCE... DIRECTORY
install [OPTION]... -t DIRECTORY SOURCE...
install [OPTION]... -d DIRECTORY...
```

前三个格式会将指定的 source 复制到 Dest 地址或者将多个 source 复制到已存在的目标目录，同时设定相应的权限模式或者属主，属组等信息；第四个格式会创建给定的目录路径。

常用选项

- `-g，--group=Group`：指定目标文件的属组；
- `-o，--owner=user`：指定目标文件的属主；
- `-m，--mode=mode`：指定目标文件的权限模式；
- `-S`：设置目标文件的后缀；
- `-D`：创建指定文件路径中不存在的目录；

使用实例

复制 source 文件到指定的文件路径：

```ruby
[root@localhost ~]# install /etc/passwd /tmp/passwd.bak
[root@localhost ~]# cat /tmp/passwd.bak | head -5
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
```

复制多个 source 文件到对应的目录路径：

```csharp
[root@localhost ~]# mkdir /tmp/test
[root@localhost ~]# install -t /tmp/test/ /etc/passwd /home/charlie/autocreate
[root@localhost ~]# ll /tmp/test/
总用量 8
-rwxr-xr-x. 1 root root   12 2月   9 17:00 autocreate
-rwxr-xr-x. 1 root root 3595 2月   9 17:00 passwd
```

## realpath

`realpath` 是一个 Linux 和 Unix 系统中的命令，用于**解析符号链接或相对路径**并**返回文件或目录的绝对路径**。它对于处理路径、确认文件位置、确保路径的一致性非常有用。

**主要功能**：

1. **解析相对路径**：将给定的相对路径转换为绝对路径。
2. **解析符号链接**：将符号链接解析为其实际的目标路径。
3. **去除冗余**：移除 `.` 和 `..` 这样的路径部分，并返回简化的路径。

**常见用法**：

```shell
realpath [选项] [文件/目录]
```

**常用选项**：

- `--relative-to=DIR`：显示相对于指定目录的相对路径。
- `--no-symlinks`：不解析符号链接，只对路径进行规范化。
- `--canonicalize-missing`：即使路径不存在，也返回规范化后的路径。

**示例**：

```shell
# 1. 将相对路径转换为绝对路径：
realpath ./mydir
# 输出：/home/user/mydir

# 2. 解析符号链接：假设 `/tmp/mylink` 是指向 `/home/user/mydir` 的符号链接：
realpath /tmp/mylink
# 输出：/home/user/mydir

# 3. 获取相对路径：
realpath --relative-to=/home /home/user/mydir
# 输出：user/mydir

# 4. 脚本中获取当前脚本路径
SCRIPT_DIR=$(realpath "$(dirname "$0")") # 可解析符号链接
echo "$SCRIPT_DIR"

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd) # 跨平台兼容性好
```

`realpath` 命令非常适用于需要在脚本中确保路径一致性的场景。

## basename 命令

`basename` 是一个常用的 Unix/Linux 命令，用于提取文件路径中的文件名部分，或从文件名中去掉指定的后缀。它特别适用于从完整的文件路径中提取文件名。

**基本语法**：

```bash
basename [OPTION] NAME [SUFFIX]
```

- `NAME`：指定文件的路径。
- `SUFFIX`：可选参数，指定要从文件名中移除的后缀（如果文件名以该后缀结尾）。

**主要选项**：

- `-a` 或 `--multiple`：允许同时处理多个路径。
- `-s` 或 `--suffix=SUFFIX`：指定一个后缀进行删除，相当于直接写在 `basename` 命令的第二个参数位置。

**功能**：

- **去除路径信息**：`basename` 可以去除文件路径，仅保留文件名。
- **去除后缀**：可以指定一个后缀，`basename` 会去掉文件名中匹配的后缀部分。

**使用示例**：

1. 从文件路径中提取文件名

   ```bash
   basename /home/user/docs/file.txt
   # 输出: file.txt
   ```

2. 去除文件名中的后缀

   可以指定一个后缀，如果文件名以该后缀结尾，则会被去除：

   ```bash
   basename /home/user/docs/file.txt .txt
   # 输出: file
   basename -s .h include/stdio.h
   # 输出: stdio
   basename "file.tar.gz" .tar.gz
   # 输出：file
   ```

3. 提取目录名称

   如果你需要提取目录名称而不是文件名，可以结合 `dirname` 和 `basename` 使用。例如，获取文件所属的最上级目录名：

   ```bash
   dirname /home/user/docs/file.txt | xargs basename
   # 输出: docs
   ```

4. 与 `find` 命令结合使用

   结合 `find` 命令，可以提取目录中多个文件的文件名。例如，列出当前目录中所有 `.txt` 文件的文件名：

   ```bash
   find . -type f -name "*.txt" -exec basename {} \;
   ```

5. 在脚本中获取当前脚本名：

   ```bash
   script_name=$(basename "$0")
   ```

6. 批量处理文件名：

   ```bash
   # 结合find使用
   find . -type f | while read file; do
       name=$(basename "$file")
       echo "Processing $name"
   done
   ```

## dirname 命令

`dirname`它主要用于**从路径中提取目录部分（即去掉文件名）**。

**一、基本作用**

> **`dirname` 从给定路径中删除最后一个 `/` 及其后面的内容。**

语法：

```bash
dirname PATH
```

**二、常见用法示例**

| 命令                          | 输出         | 说明                                    |
| ----------------------------- | ------------ | --------------------------------------- |
| `dirname /home/user/file.txt` | `/home/user` | 去掉最后一级文件名                      |
| `dirname /home/user/dir/`     | `/home/user` | 去掉最后的目录名（如果路径以 `/` 结尾） |
| `dirname file.txt`            | `.`          | 当前目录（因为路径中没有 `/`）          |
| `dirname /file.txt`           | `/`          | 根目录                                  |
| `dirname ../src/main.c`       | `../src`     | 保留相对路径部分                        |

**与 `basename` 配合使用（常见搭档）**

`dirname` 和 `basename` 通常搭配使用：

```bash
path="/home/user/project/file.txt"
echo "目录名:   $(dirname "$path")"
echo "文件名:   $(basename "$path")"

# 输出：
# 目录名:   /home/user/project
# 文件名:   file.txt
```

**三、在脚本中常用的组合**

1. 获取当前脚本所在目录（经典写法）

   ```bash
   SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)    # 兼容性好
   SCRIPT_DIR=$(realpath "$(dirname "$0")")     # 可解析符号链接
   echo "$SCRIPT_DIR"
   ```

   解释：

   - `$0`：脚本路径（可能是相对路径）
   - `dirname "$0"`：取出脚本所在目录
   - `cd ... && pwd`：转为绝对路径

   > 用处：在脚本中访问相对路径的配置文件、依赖等。

2. 获取上级目录

   ```bash
   # 获取上2级目录
   PARENT_DIR=$(dirname "$(dirname "$path")")      # 连续两次 `dirname` 即可

   for ((i=0; i<2; i++)); do DIR=$(dirname "$DIR"); done
   ```

   函数写法：

   ```bash
   #!/bin/bash
   set -e

   get_dir_up() {
      local n=${2:-1}
      local dir
      dir=$(realpath "$1")
      while [ "$n" -gt 0 ]; do
         dir=$(dirname "$dir")
         n=$((n-1))
      done
      echo "$dir"
   }

   SCRIPT_DIR=$(realpath "$(dirname "$0")")
   ROOT_DIR=$(get_dir_up "$SCRIPT_DIR" 3)
   echo "当前脚本: $SCRIPT_DIR"
   echo "项目根目录: $ROOT_DIR"
   ```

   > 如果不传第二个参数，默认取上一级。

**四、边界与特殊情况**

| 输入       | 输出       | 解释                       |
| ---------- | ---------- | -------------------------- |
| `/`        | `/`        | 根目录的 dirname 是它自己  |
| `/foo`     | `/`        | 去掉 `foo`，剩下 `/`       |
| `foo`      | `.`        | 当前目录                   |
| `foo/bar/` | `foo`      | 去掉最后的 `/`             |
| 空字符串   | （未定义） | 可能报错 “missing operand” |

# 压缩解压命令

## tar 包

`tar` 是 Linux 中常用的打包和压缩工具，可以将多个文件或目录打包成一个归档文件，也可以用于解压这些归档文件。

`tar` 是 Linux/Unix 系统中用于**打包（归档）文件和目录**的命令，全称是 **tape archive**。它常用于备份文件、软件发布包的生成等场景。`tar` 不压缩文件，但可与 gzip、bzip2、xz 等工具结合实现压缩打包。

**常用参数详解**

以下是 `tar` 的常用参数（区分长短参数形式）：

| 参数                           | 含义                                                   |
| ------------------------------ | ------------------------------------------------------ |
| `-c` 或 `--create`             | 创建新归档文件（archive）                              |
| `-x` 或 `--extract`            | 解包归档文件                                           |
| `-t` 或 `--list`               | 查看归档文件内容                                       |
| `-f <file>` 或 `--file=<file>` | 指定归档文件名（必须紧跟 `-f`）                        |
| `-v` 或 `--verbose`            | 显示处理过程中的文件名（verbose 模式）                 |
| `-z` 或 `--gzip`               | 使用 gzip 压缩或解压（`.tar.gz` 或 `.tgz`）            |
| `-j` 或 `--bzip2`              | 使用 bzip2 压缩（`.tar.bz2`）                          |
| `-J` 或 `--xz`                 | 使用 xz 压缩（`.tar.xz`）                              |
| `--lzma`                       | 使用 lzma 压缩（`.tar.lzma`）                          |
| `-C <dir>`                     | 切换目录再操作（常用于解压时指定目标目录）             |
| `--exclude=<pattern>`          | 排除匹配的文件/目录                                    |
| `--include=<pattern>`          | 包含匹配的文件/目录，仅包含要配合 `--exclude="*"` 使用 |
| `--wildcards '*.txt'`          | 启用 shell 风格的通配符匹配（\*, ?, []）               |

> 注：默认情况下 `--exclude` 里的模式是 字面量匹配，必须配合 `--wildcards` 才能按通配符匹配。

### `tar -c` 压缩

**常见用法示例**

1. 创建归档文件（不压缩）

   ```bash
   tar -cvf archive.tar dir1 file2
   ```

   - 将 `dir1` 和 `file2` 打包成 `archive.tar`，不压缩

2. 创建 gzip 压缩包（`.tar.gz` 或 `.tgz`）

   ```bash
   tar -czvf archive.tar.gz dir/
   ```

   - `c`: 创建
   - `z`: gzip 压缩
   - `v`: 显示详情
   - `f`: 指定文件名

3. 创建归档时**排除**某些文件或目录

   ```bash
   tar --exclude='*.log' -czvf archive.tar.gz dir/
   ```

4. 创建归档时**仅包含**某些文件或目录

   ```bash
   tar -cvf code.tar \
       --wildcards \
       --include="*.c" \
       --include="*.h" \
       --exclude="*"
   ```

5. 追加文件到已存在的 `.tar` 文件中（仅限未压缩的 tar）

   ```bash
   tar -rvf archive.tar newfile.txt
   ```

6. 查看归档文件内容

   ```bash
   tar -tvf archive.tar.gz
   ```

   > 不解压，仅显示文件列表。

### `tar -x` 解压

**常见用法示例**

1. 解包归档文件（不解压）

   ```bash
   tar -xvf archive.tar
   ```

2. 解压 `tar.gz` 文件

   ```bash
   # 到当前目录
   tar -xzvf archive.tar.gz
   # 到指定目录
   tar -xzvf archive.tar.gz -C /path/to/target/
   ```

3. 解压 `.tar.bz2` 文件

   ```bash
   tar -xjvf archive.tar.bz2
   ```

4. 解压 `.tar.xz` 文件

   ```bash
   tar -xJvf archive.tar.xz
   ```

5. 仅解压指定文件（部分解压）

   ```bash
   tar -xzvf archive.tar.gz path/inside/tar.txt
   ```

6. 查看归档文件内容

   ```bash
   tar -tvf archive.tar.gz
   ```

   > 不解压，仅显示文件列表。

### 后缀与压缩方式对照表

| 文件后缀           | 说明            | 命令中使用的参数 |
| ------------------ | --------------- | ---------------- |
| `.tar`             | 仅打包，无压缩  | `-cvf`、`-xvf`   |
| `.tar.gz` / `.tgz` | 使用 gzip 压缩  | `-czvf`、`-xzvf` |
| `.tar.bz2`         | 使用 bzip2 压缩 | `-cjvf`、`-xjvf` |
| `.tar.xz`          | 使用 xz 压缩    | `-cJvf`、`-xJvf` |

**实战建议**

- 打包发布时，推荐 `.tar.gz` 或 `.tar.xz`，兼顾兼容性和压缩率。
- 解压时优先加上 `-C` 指定目录，避免文件铺开到当前路径。
- 可以将参数合并成一组，例如 `-xvzf`，也可以拆开 `-x -v -z -f`。

## zip 包

在 Linux 系统中，`zip`和`unzip`是处理 ZIP 压缩文件的标准工具。

**安装工具**

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install zip unzip
# CentOS/RHEL
sudo yum install zip unzip
# Arch Linux
sudo pacman -S zip unzip
```

### `zip` 压缩

**基本语法**

```bash
zip [参数] 压缩包名.zip 文件或目录
```

**常用参数**

| 参数          | 作用                               |
| :------------ | :--------------------------------- |
| `-r`          | 递归压缩目录（包含子目录）         |
| `-q`          | 静默模式（不显示输出信息）         |
| `-e`          | 加密压缩（设置密码）               |
| `-1`~`-9`     | 压缩级别（1 最快压缩，9 最佳压缩） |
| `-v`          | 显示详细压缩过程                   |
| `-x`          | 排除指定文件/目录                  |
| `-m`          | 压缩后删除原文件                   |
| `-F`          | 修复损坏的 ZIP 文件                |
| `-s 分割大小` | 分卷压缩（如 `-s 100M`）           |

**典型示例**

1. **压缩单个文件**：

   ```bash
   zip archive.zip file.txt
   ```

2. **递归压缩目录**（含子目录）：

   ```bash
   zip -r archive.zip /path/to/dir/
   zip -r combined.zip dir1/ dir2/ file1.txt
   ```

3. **排除特定文件**：

   ```bash
   zip -r archive.zip dir/ -x "*.tmp" "temp/*"
   ```

4. **分卷压缩**（每卷 50MB）：

   ```bash
   zip -r -s 50M split_archive.zip large_dir/
   ```

   > 生成文件：`split_archive.z01`, `split_archive.z02`, ..., `split_archive.zip`

5. **管道操作**

   压缩日志文件并直接传输：

   ```bash
   cat /var/log/syslog | zip logs.zip -
   ```

6. **最快压缩（低压缩率）**：

   ```bash
   zip -1 fast.zip large_file.iso
   ```

7. **加密压缩**（会提示输入密码）：

   ```bash
   zip -e secret.zip sensitive_file.txt
   ```

### `unzip` 解压

**基本语法**

```bash
unzip [参数] 压缩包名.zip -d 目标目录
```

**常用参数**

| 参数      | 作用                                 |
| :-------- | :----------------------------------- |
| `-d`      | 指定解压目录                         |
| `-l`      | 仅列出压缩包内容（不解压）           |
| `-o`      | 强制覆盖已存在文件                   |
| `-n`      | 不覆盖已存在文件                     |
| `-P 密码` | 直接指定密码（不安全，建议交互输入） |
| `-q`      | 静默解压                             |
| `-j`      | 忽略路径，所有文件解压到同一目录     |

**典型示例**

1. **解压到当前目录**：

   ```bash
   unzip archive.zip
   ```

2. **解压到指定目录**：

   ```bash
   unzip archive.zip -d /target/path/
   ```

3. **强制覆盖解压**：

   ```bash
   unzip -o archive.zip
   ```

4. **解压时排除文件**

   ```bash
   unzip archive.zip -x "*.bak" "temp/*"
   ```

5. **列出压缩包内容**：

   ```bash
   unzip -l archive.zip
   ```

6. **解压加密 ZIP**（交互式输入密码）：

   ```bash
   unzip secret.zip
   ```

7. **解压分卷 ZIP**：

   ```bash
   zip -F split_archive.zip --out repaired.zip  # 先修复（可选）
   unzip repaired.zip
   ```

**注意事项**

1. ZIP 格式默认不保留 Linux 文件权限（需用`-X`参数保留 UID/GID）。
2. 分卷压缩时，分卷文件需放在同一目录下才能解压。
3. 加密密码在命令行中使用`-P`会暴露历史记录，建议交互输入。

对比`zip`与`tar.gz`

| 特性       | ZIP                 | tar.gz             |
| :--------- | :------------------ | :----------------- |
| **压缩率** | 中等                | 通常更高           |
| **功能**   | 支持加密/分卷       | 保留权限/符号链接  |
| **跨平台** | Windows/Linux/macOS | 主要类 Unix 系统   |
| **速度**   | 较快                | 较慢（高压缩率时） |

## rar 包

在 Linux 下，`.rar` 格式不是开源的压缩格式，需要安装官方的 **RAR** 工具（通常包含 `rar` 和 `unrar` 两个命令）对 `.rar` 文件的压缩和解压。

**RAR 格式简介**

- `.rar` 是一种专有压缩格式，压缩率较高，常用于 Windows 系统。
- Linux 系统默认**不支持 RAR 格式**，需要手动安装工具包（如 `rar`、`unrar`）。
- 工具来源：由 RARLab 官方发布（非开源）。

**安装方法**

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install rar unrar
# CentOS / RHEL
sudo yum install epel-release
sudo yum install rar unrar
```

### `rar` 压缩

**基本语法：**

```bash
rar <命令> [参数] <压缩文件.rar> <文件或目录>
```

**常用命令：**

- `a`：添加文件到压缩包（若压缩包不存在则创建）。
- `d`：删除压缩包内文件。
- `l`：列出压缩包内容。
- `t`：测试压缩包是否损坏。
- `u`：更新压缩包中的文件。

**常用参数：**

- `-r`：递归处理子目录。
- `-p[密码]`：设置密码（如 `-p123`）。
- `-m<n>`：设置压缩级别（`0`存储，`3`默认，`5`最大）。
- `-v<大小>`：分卷压缩（如 `-v100M` 每卷 100MB）。
- `-sfx`：创建自解压包（Windows 格式）。
- `-lock`：锁定压缩包（禁止修改）。

**典型使用示例**

1. 压缩文件/目录：

   ```bash
   rar a archive.rar /path/to/dir
   rar a -r archive.rar /path/to/dir
   ```

   - `-r` 表示递归压缩子目录
     假设有如下目录：

     ```log
     /path/to/dir/
     ├── file1.txt
     ├── file2.log
     └── subdir/
         ├── file3.txt
         └── file4.log
     ```

   - **不带 `-r` 参数**：仅压缩指定目录下的直接文件，**忽略子目录及其内容**。

     生成的 `archive.rar` 将包含如下，其中 `subdir/` 及其内容不会被压缩：

     ```log
     file1.txt
     file2.log
     ```

   - **带 `-r` 参数**：递归压缩指定目录下的**所有文件和子目录**（包括子目录中的内容）。

     生成的 `archive.rar` 将包含：

     ```log
     file1.txt
     file2.log
     subdir/file3.txt
     subdir/file4.log
     ```

2. 分卷压缩（每卷 50MB）：

   ```bash
   rar a -v50M archive.rar largefile.iso
   ```

3. 添加密码压缩

   ```bash
   rar a -p123456 secure.rar file.txt
   ```

   > 用密码 `123456` 进行压缩（注意密码可能在命令行历史中留下）

4. 查看压缩包内容

   ```bash
   rar l archive.rar
   ```

### `unrar` 解压

**基本语法：**

```bash
unrar <命令> [参数] <压缩文件.rar> [目标目录]
```

**常用命令：**

- `x`：解压保留路径。
- `e`：解压到当前目录（忽略路径）。
- `l`：列出压缩包内容。
- `t`：测试压缩包完整性。
- `p`：打印文件到标准输出。

**常用参数：**

- `-p[密码]`：指定密码（如 `-p123`）。
- `-o+`：覆盖已存在文件。
- `-o-`：不覆盖文件。
- `-y`：所有操作均回答“是”。

**典型使用示例**

1. 完整解压到当前目录

   ```bash
   unrar e archive.rar  # 不保留路径
   unrar x archive.rar  # 保留路径
   ```

   `unrar e`和 `unrar x` 对比，如果压缩包 archive.rar 内文件如下：

   ```log
   project/
   ├── src/
   │   └── app.c
   └── config.yaml
   ```

   - **`unrar e` 行为**：将所有文件解压到**当前目录**，**忽略压缩包内的目录结构**，所有文件都会平铺在当前文件夹中。
     解压后当前目录会变成：

     ```log
     app.c       # 原路径 project/src/app.c
     config.yaml # 原路径 project/config.yaml
     ```

     **注意**：同名文件会被覆盖（可通过`-o+`强制覆盖或`-o-`跳过）！

     **适用场景**：

     - 压缩包内文件没有层级目录，或你不需要保留目录结构。
     - 希望所有文件直接解压到当前目录，避免嵌套文件夹。

   - **`unrar x` 行为**：严格按照压缩包内的目录结构解压，**还原完整的文件路径**。如果路径中的目录不存在，会自动创建。

     ```log
     project/
     ├── src/
     │   └── app.c
     └── config.yaml
     ```

     **适用场景**：

     - 压缩包内有复杂的目录结构需要保留。
     - 解压后需维持原始文件组织方式（如软件源码、项目文档等）。

2. 解压到指定目录

   - 使用 `x` 时，可指定目标路径（自动创建子目录）

     ```bash
     unrar x archive.rar /target/path/  # 保持结构解压到/target/path/
     ```

   - 使用 `e` 时，需先进入目标目录（否则文件会散落在当前目录）：

     ```bash
     cd /target/path/ && unrar e /path/to/archive.rar
     ```

3. 只解压指定文件

   ```bash
   unrar x archive.rar file1.txt
   ```

4. 查看压缩包内容

   ```bash
   unrar l archive.rar
   ```

5. 解压加密文件

   ```bash
   unrar x -p123 secret.rar
   ```

# 文件显示命令

## cat

cat（英文全拼：concatenate）命令用于连接文件并打印到标准输出设备上，它的主要作用是用于查看和连接文件。

```shell
cat [选项] [文件]
```

**参数说明：**

- `-n`：显示行号，会在输出的每一行前加上行号。
- `-b`：显示行号，但只对非空行进行编号。
- `-s`：压缩连续的空行，只显示一个空行。
- `-E`：在每一行的末尾显示 `$` 符号。
- `-T`：将 Tab 字符显示为 `^I`。
- `-v`：显示一些非打印字符。

```shell
cat filename # 查看文件内容：显示文件 filename 的内容。

cat > filename # 创建文件：将标准输入重定向到文件 filename，覆盖该文件的内容。

cat >> filename # 追加内容到文件：将标准输入追加到文件 filename 的末尾。

cat file1 file2 > file3 # 连接文件：将 file1 和 file2 的内容合并到 file3 中。

cat file1 file2 # 显示多个文件的内容：同时显示 file1 和 file2 的内容。

cat filename | command # 使用管道：将 cat 命令的输出作为另一个命令的输入。

cat filename | tail -n 10 # 查看文件的最后几行：显示文件 filename 的最后 10 行。

cat -n filename # 使用 -n 选项显示行号：显示文件 filename 的内容，并在每行的前面加上行号。

cat -b filename # 使用 -b 选项仅显示非空行的行号：

cat -s filename # 使用 -s 选项合并空行：显示文件 filename 的内容，并合并连续的空行。

cat -t filename # 使用 -t 选项显示制表符：显示文件 filename 的内容，并用 ^I 表示制表符。

cat -e filename # 使用 -e 选项显示行结束符：显示文件 filename 的内容，并用 $ 表示行结束。

cat -n textfile1 > textfile2 # 把 textfile1 的文档内容加上行号后输入 textfile2 这个文档里：

cat -b textfile1 textfile2 >> textfile3 # 把 textfile1 和 textfile2 的文档内容加上行号（空白行不加）之后将内容附加到 textfile3 文档里：

cat /dev/null > /etc/test.txt # 清空 /etc/test.txt 文档内容：
```

```shell
# 要创建一个新文件并将内容写入它，你可以使用重定向操作符>或者cat命令本身。
# 1.使用重定向操作符>：你可以输入你想要写入文件的内容。按下 Ctrl + D 来保存并退出。
cat > new_file.txt
# 2.使用cat命令：在<< EOF和EOF之间的文本是你要写入文件的内容。按下Enter后，然后按下Ctrl + D来保存并退出。
cat > new_file.txt << EOF
这是新文件的内容。
它可以有多行。
EOF

# 要向现有文件追加内容，可以使用重定向操作符>>或者cat命令。
# 1.使用重定向操作符>>：你可以输入你想要写入文件的内容。按下 Ctrl + D 来保存并退出。
cat >> existing_file.txt
# 2.使用cat命令：在<< EOF和EOF之间的文本是你要写入文件的内容。按下Enter后，然后按下Ctrl + D来保存并退出。
cat >> existing_file.txt << EOF
这是要追加到文件的内容。
它可以有多行。
EOF
```

## head

head 命令可用于查看文件的开头部分的内容，有一个常用的参数 **-n** 用于显示行数，默认为 10，即显示 10 行的内容。

```shell
head [参数] [文件]
```

- -q 隐藏文件名
- -v 显示文件名
- -c<数目> 显示的字节数。
- -n<行数> 显示的行数。

```shell
head -n 5 runoob_notes.log # 显示 notes.log 文件的开头 5 行，请输入以下命令

head -c 20 runoob_notes.log # 显示文件前 20 个字节
```

## tail

tail 命令可用于查看文件的内容，有一个常用的参数 **-f** 常用于查阅正在改变的日志文件。参数 **-n** 用于显示行数，默认为 10，即显示 10 行的内容。

**tail -f filename** 会把 filename 文件里的最尾部的内容显示在屏幕上，并且不断刷新，只要 filename 更新就可以看到最新的文件内容。

```shell
tail [参数] [文件]
```

- -f 循环读取
- -q 不显示处理信息
- -v 显示详细的处理信息
- -c<数目> 显示的字节数
- -n<行数> 显示文件的尾部 n 行内容
- --pid=PID 与-f 合用,表示在进程 ID,PID 死掉之后结束
- -q, --quiet, --silent 从不输出给出文件名的首部
- -s, --sleep-interval=S 与-f 合用,表示在每次反复的间隔休眠 S 秒

```shell
tail -n +20 notes.log # 显示文件 notes.log 的内容，从第 20 行至文件末尾

tail -f notes.log # 此命令显示 notes.log 文件的最后 10 行。当将某些行添加至 notes.log 文件时，tail 命令会继续显示这些行。 显示一直继续，直到您按下（Ctrl-C）组合键停止显示。即，可跟踪名为 notes.log 的文件的增长情况。
```

## cat/head/tail 组合

```shell
# 显示前1000行
cat [filename] | head -n 1000

# 显示最后1000行
cat [filename] | tail -n 1000

# 从1000行以后开始显示
cat [filename] | tail -n +1000

# 从1000行开始显示3000行
cat [filename] | tail -n +1000 | head -n 3000

# 显示1000行到3000行
cat [filename] | head -n 3000 | tail -n +1000
```

## tee 命令

`tee` 是一个在 Unix/Linux 系统中常用的命令行工具，用于读取标准输入并将其内容写入标准输出和一个或多个文件。它的名称来源于字母 "T"，因为它的作用类似于一个 "T" 型分流器。

**基本语法**：

```bash
tee [OPTION]... [FILE]...
```

- **OPTION**：可选参数，用于修改 `tee` 的行为。
- **FILE**：要写入的一个或多个文件名。如果不指定文件，则输出到标准输出。

**常用选项**：

- `-a` 或 `--append`：追加内容到指定文件，而不是覆盖。
- `-i` 或 `--ignore-interrupts`：在信号中断时忽略中断。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

**常见用法**：

1. 基本使用

   将命令的输出同时写入到文件和标准输出：

   ```bash
   echo "Hello, World!" | tee output.txt
   ```

   这条命令会将 "Hello, World!" 打印到屏幕上，同时写入到 `output.txt` 文件中。

2. 追加内容

   使用 `-a` 选项可以将内容追加到文件末尾，而不是覆盖文件：

   ```bash
   echo "Hello again!" | tee -a output.txt
   ```

   如果 `output.txt` 已存在，这条命令会在文件末尾添加 "Hello again!"。

3. 多个文件

   可以将输出同时写入多个文件：

   ```bash
   echo "Logging data" | tee file1.txt file2.txt
   ```

   这会将 "Logging data" 同时写入 `file1.txt` 和 `file2.txt`。

4. 结合其他命令

   `tee` 常用于将输出流中的数据分流给多个命令。例如，可以将一个命令的输出保存到文件，同时将其传递给另一个命令：

   ```bash
   ps aux | tee processes.txt | grep bash
   ```

   这会将当前运行的所有进程信息保存到 `processes.txt` 文件中，同时筛选出包含 "bash" 的行并显示在屏幕上。

5. 在脚本中使用

   ```shell
   #!/bin/bash
   # 记录脚本执行过程
   {
       echo "Starting process..."
       date
       some_command
       echo "Process completed."
   } | tee process.log
   ```

6. 追加模式插入空行

```shell
echo "First line" | tee -a output.txt
echo -e "\n\n\n" | tee -a output.txt  # 输出3个空行
echo "Second line" | tee -a output.txt
```

**示例**：

1. 输出到文件并显示

   ```bash
   df -h | tee disk_usage.txt
   ```

   这条命令会显示当前的磁盘使用情况，并将其写入到 `disk_usage.txt` 文件中。

2. 与管道结合

   ```bash
   cat /var/log/syslog | tee syslog_copy.txt | grep error
   ```

   这会将系统日志文件的内容输出到标准输出并写入 `syslog_copy.txt`，同时筛选出包含 "error" 的行。

**总结**：

`tee` 命令是一个非常有用的工具，特别是在处理数据流时，可以有效地将输出分流到多个目的地。它在脚本编写、日志记录和调试过程中非常有用，能够帮助用户同时查看和存储命令的输出。

## printf 命令

`printf` 是一个在 Unix/Linux 系统中广泛使用的命令行工具，用于格式化输出文本。它比 `echo` 更强大和灵活，能够提供更复杂的格式控制，特别是在处理数字和字符串时。

**基本语法**：

```bash
printf FORMAT_STRING [ARGUMENTS...]
```

- **FORMAT_STRING**：指定输出的格式，可以包含普通文本和格式说明符。
- **ARGUMENTS**：要格式化输出的值。

**常见格式说明符**：

- `%s`：字符串
- `%d`：十进制整数
- `%f`：浮点数
- `%x`：十六进制整数
- `%o`：八进制整数
- `%c`：字符
- `%p`：指针（地址）

**常见用法**：

1. 格式化输出数字

   格式化整数和浮点数：

   ```bash
   printf "Integer: %d\n" 42
   printf "Float: %.2f\n" 3.14159
   ```

   - `%.2f` 表示输出浮点数并保留两位小数。

2. 输出多个参数

   可以一次性输出多个参数：

   ```bash
   printf "Name: %s, Age: %d\n" "Alice" 30
   ```

   这将输出 `Name: Alice, Age: 30`。

3. 设定宽度和对齐方式

   可以设定输出的宽度：

   ```bash
   printf "|%10s|%5d|\n" "Item" 123
   ```

   - `%10s` 表示字符串占用 10 个字符宽，右对齐。
   - `%5d` 表示整数占用 5 个字符宽，右对齐。

   左对齐可以使用负号：

   ```bash
   printf "|%-10s|%-5d|\n" "Item" 123
   ```

4. 使用转义字符

   `printf` 也支持转义字符，比如换行符 `\n` 和制表符 `\t`：

   ```bash
   printf "Column1\tColumn2\nValue1\tValue2\n"
   ```

5. 生成多个重复字符

   ```shell
   printf '=%.0s' {1..20}
   ```

   - 格式字符串 `'=%.0s'`

     在这里，格式字符串是 `'=%.0s'`。这个格式字符串可以分解为以下部分：

     - **`=`**：这是要输出的字符。由于 `printf` 在处理格式字符串时，会将每个格式说明符与对应的参数结合起来输出，因此这里的 `=` 是固定的，它会被输出 20 次。
     - **`%.0s`**：这是格式说明符，表示以字符串形式输出。具体来说：
       - **`%s`** 表示输出字符串。
       - **`.0`** 是一个精度修饰符，表示不输出字符串的内容，而是仅仅输出字符串的“空字符”。因此，`%.0s` 实际上不会输出任何字符，但会使得 `printf` 进行相应次数的调用。

   - `{1..20}`

     这是一个 Bash 的序列扩展（Brace Expansion），用于生成一个从 1 到 20 的序列。这里，它实际上并不使用这些数字的值，而是仅仅用来确定输出多少次格式字符串。

**示例**：

以下是一个完整的示例，演示 `printf` 的各种功能：

```bash
#!/bin/bash

# 输出字符串
printf "Hello, World!\n"

# 输出整数和浮点数
printf "Integer: %d\n" 42
printf "Float: %.2f\n" 3.14159

# 输出多个参数
name="Alice"
age=30
printf "Name: %s, Age: %d\n" "$name" "$age"

# 设置宽度和对齐
printf "|%10s|%5d|\n" "Item" 123
printf "|%-10s|%-5d|\n" "Item" 123

# 使用转义字符
printf "Column1\tColumn2\nValue1\tValue2\n"
```

运行这个脚本将输出如下内容：

```log
Hello, World!
Integer: 42
Float: 3.14
Name: Alice, Age: 30
|      Item|  123|
|Item      |123  |
Column1   Column2
Value1    Value2
```

**总结：**

`printf` 是一个非常强大的工具，适用于需要格式化输出的场合。它能够提供丰富的格式控制选项，帮助用户创建更易读和专业的输出结果。与 `echo` 相比，`printf` 更加灵活，适合在脚本中处理复杂的输出需求。

## tree 命令

`tree` 是一个非常有用的命令行工具，用于以树状结构显示目录和文件的层次结构。它通过递归地列出目录及其内容，可以帮助用户更直观地查看文件系统的结构。

**1. 基本语法：**

```bash
tree [选项] [目录...]
```

- **[选项]**：用于修改 `tree` 输出的格式。
- **[目录]**：指定要显示结构的目录，默认为当前目录。

**2. 常用选项：**

- `-L <level>` ：限制显示目录的深度，`<level>` 是要显示的目录层级。例如 `-L 2` 只显示两级目录结构。
- `-d` ：只显示目录，不显示文件。
- `-a` ：显示所有文件和目录（包括隐藏文件）。
- `-f` ：在每个文件名前面加上完整的路径（不适用于相对路径）。
- `-s` ：显示每个文件或目录的大小（以字节为单位）。
- `-h` ：与 `-s` 配合使用，以可读性较高的方式显示文件大小（如 KB、MB）。
- `-T` ：在文件或目录的末尾显示与其相关的详细时间戳。
- `-I <pattern>` ：排除匹配 `<pattern>` 的文件或目录。例如 `-I "*.log"` 排除所有 `.log` 文件。
- `--noreport` ：不显示报告统计信息（文件数和目录数）。
- `-v` ：显示详细信息，包括文件的权限和修改时间。

**3. 示例：**

1. 显示当前目录的树形结构

   ```bash
   tree

   # 输出：
   ├── file1.txt
   ├── file2.txt
   └── subdir
       ├── file3.txt
       └── file4.txt

   2 directories, 4 files
   ```

2. 限制显示深度为 2

   ```bash
   tree -L 2

   # 输出：
   ├── file1.txt
   ├── file2.txt
   └── subdir
       ├── file3.txt
       └── file4.txt

   2 directories, 4 files
   ```

3. 只显示目录，不显示文件

   ```bash
   tree -d

   # 输出：
   └── subdir

   1 directory
   ```

4. 显示所有文件，包括隐藏文件

   ```bash
   tree -a

   # 输出：
   ├── .hiddenfile
   ├── file1.txt
   ├── file2.txt
   └── subdir
       ├── .hiddenfile
       ├── file3.txt
       └── file4.txt

   2 directories, 6 files
   ```

5. 显示文件和目录大小

   ```bash
   tree -s

   # 输出：
   ├── 123 file1.txt
   ├── 456 file2.txt
   └── subdir
       ├── 789 file3.txt
       └── 101 file4.txt

   2 directories, 4 files
   ```

6. 显示文件大小以人类可读格式

   ```bash
   tree -sh

   # 输出：
   ├── 12K file1.txt
   ├── 45K file2.txt
   └── subdir
       ├── 123K file3.txt
       └── 56K file4.txt

   2 directories, 4 files
   ```

7. 排除特定文件类型

   ```bash
   tree -I "*.log"

   # 输出：
   ├── file1.txt
   ├── file2.txt
   └── subdir
       ├── file3.txt
       └── file4.txt

   2 directories, 4 files
   ```

   （`*.log` 文件被排除）

8. 显示完整路径

   ```bash
   tree -f

   # 输出：
   /home/user/file1.txt
   /home/user/file2.txt
   /home/user/subdir/file3.txt
   /home/user/subdir/file4.txt
   ```

9. 不显示统计报告

   ```bash
   tree --noreport

   # 输出：
   ├── file1.txt
   ├── file2.txt
   └── subdir
       ├── file3.txt
       └── file4.txt
   ```

**4. 用途：**

- **目录结构查看**：使用 `tree` 可以方便地查看一个目录的层次结构，特别是在文件夹层级很深的情况下，帮助用户了解整个文件系统的布局。
- **目录内容筛选**：通过排除特定类型的文件或文件夹，用户可以更容易地获取他们需要的信息。
- **文件大小分析**：通过显示每个文件的大小，可以帮助用户了解哪些文件占用了磁盘空间。
- **脚本自动化**：在自动化任务中，`tree` 可以生成可视化的目录结构，便于日志记录和处理。

**5. 安装：**

`tree` 不是 Linux 系统的默认工具，但可以通过包管理器进行安装：

```bash
# Debian/Ubuntu
sudo apt-get install tree

# RedHat/CentOS
sudo yum install tree

# macOs（通过 Homebrew）
brew install tree
```

**6. 总结：**

`tree` 是一个非常直观的命令行工具，可以以树状结构显示文件系统的层次结构。通过各种选项，用户可以定制输出的内容，例如限制深度、显示文件大小、排除特定类型的文件等。这些功能使得 `tree` 成为文件管理和脚本自动化任务中的一个强大工具。

# 文本操作命令

## sed 命令

`sed`（Stream Editor）是一个强大的文本处理工具，主要用于对文本流进行**过滤和转换**。它常用于 Unix/Linux 系统中，可以对文件内容或标准输入流进行文本替换、插入、删除和其他处理。

**基本语法**：

```bash
sed [OPTIONS] 'command' file
```

- **OPTIONS**：选项，可以影响 `sed` 的行为。
- **command**：要执行的命令，通常包括地址和操作。
- **file**：要处理的文件名，可以是一个或多个文件。

**常见功能和用法**：

1. 文本替换

   使用 `s` 命令进行替换：

   ```bash
   sed 's/old-text/new-text/' filename
   ```

   - 默认只替换第一处匹配的文本。
   - 添加 `g` 可以替换所有匹配的文本：

   ```bash
   sed 's/old-text/new-text/g' filename
   ```

2. 在行首/行尾添加文本

   - 在每行的开头添加文本：

   ```bash
   sed 's/^/new-text /' filename
   ```

   - 在每行的末尾添加文本：

   ```bash
   sed 's/$/ new-text/' filename
   ```

3. 删除行

   - 删除特定行：

   ```bash
   sed '3d' filename   # 删除第三行
   ```

   - 删除包含特定模式的行：

   ```bash
   sed '/pattern/d' filename
   ```

4. 选择特定行

   - 仅显示特定行：

   ```bash
   sed -n '2p' filename   # 只打印第二行
   ```

   - 打印范围行：

   ```bash
   sed -n '2,5p' filename   # 打印第2到第5行
   ```

5. 使用正则表达式

   `sed` 支持基本正则表达式和扩展正则表达式：

   - 基本正则表达式（BRE）：

   ```bash
   sed 's/[0-9]/X/' filename   # 将数字替换为 X
   ```

   - 扩展正则表达式（ERE），需要使用 `-E` 选项：

   ```bash
   sed -E 's/[a-zA-Z]+/WORD/' filename   # 将单词替换为 "WORD"
   ```

6. 直接编辑文件

   使用 `-i` 选项可以直接修改文件而不输出到标准输出：

   ```bash
   sed -i 's/old-text/new-text/g' filename
   ```

   - 注意：直接编辑文件前最好备份原文件。

**分隔符：**

`sed` 命令中，**理论上可以使用任意非字母数字的单字符**作为分隔符。最常见的替代 `/` 的分隔符包括：

| 分隔符 | 示例         | 说明                      |
| ------ | ------------ | ------------------------- |
| `/`    | `s/old/new/` | 默认分隔符                |
| `#`    | `s#old#new#` | URL 最常用，避免 `/` 冲突 |
| `      | `            | `s                        |
| `:`    | `s:old:new:` | 偶尔使用，避免和路径混淆  |
| `@`    | `s@old@new@` | 有时用在配置替换中        |
| `~`    | `s~old~new~` | 常用于 shell 脚本中       |
| `!`    | `s!old!new!` | 某些脚本环境下使用频繁    |

推荐选择依据：

- 替换内容含有 `/` → 用 `#`、`|`、`@`、`~`
- 替换内容含有多个特殊符号 → 选一个该内容**不会出现**的字符作为分隔符

不推荐或不可用的分隔符：

- 字母数字（如 `a`, `1`）不可以作为分隔符。
- 空格或转义字符（如 `\n`、`\t`）也不可以直接当作分隔符。
- 多字符不能作为分隔符（必须是单字符）。

  ```bash
  # 替换 URL 的推荐方式（避免与 `/` 冲突）
  sed -i 's#https://a.com/path#https://b.com/new#' file.txt

  # 替换包含 "#" 的文本（换成用 "|"）
  sed -i 's|value#1|value#2|' file.txt
  ```

**使用示例**：

1. 替换文件中的文本

   假设有一个文本文件 `example.txt` 内容如下：

   ```bash
   Hello World
   This is a test file.
   Goodbye World
   ```

   要将所有的 "World" 替换为 "Everyone"，可以使用：

   ```bash
   sed 's/World/Everyone/g' example.txt
   ```

   输出：

   ```bash
   Hello Everyone
   This is a test file.
   Goodbye Everyone
   ```

2. 删除特定行

   要删除第二行：

   ```bash
   sed '2d' example.txt
   ```

   输出：

   ```bash
   Hello World
   Goodbye World
   ```

3. 在每行前添加文本

   要在每行前添加 "Line: "：

   ```bash
   sed 's/^/Line: /' example.txt
   ```

   输出：

   ```bash
   Line: Hello World
   Line: This is a test file.
   Line: Goodbye World
   ```

`sed` 是一个非常灵活且强大的文本处理工具，适用于各种文本编辑任务。通过组合不同的命令和选项，可以完成复杂的文本处理工作。

# 命令行命令

## eval 命令

`eval` 是 Shell 中的一个内建命令，用于**将一段字符串解析为命令并执行**。它通常用于将字符串形式的命令转换为可执行的命令，特别是在需要动态构建和运行复杂命令时。

**语法**：

```bash
eval [命令字符串]
```

**工作原理**：

`eval` 会对提供的命令字符串进行两次解析：

1. **第一次解析**：解释字符串中的变量和命令替换。
2. **第二次解析**：将解析后的内容作为命令执行。

因此，`eval` 对于动态生成命令非常有用，可以在运行时生成复杂的命令行。

**使用场景和示例**：

eval 命令用于计算并执行包含 shell 命令的字符串。有几个重要的应用场景：

1. 变量的间接引用

   ```bash
   # 根据变量名的内容来访问不同的变量值
   var_name="path"
   path="/usr/local/bin"
   eval echo \$$var_name  # /usr/local/bin

   # 动态设置变量
   key="my_var"
   value="hello"
   eval "$key='$value'"  # 相当于 my_var='hello'
   ```

   **说明**：`\$$var_name` 经过两次解析后变成了 `$path`，最终输出 `/usr/local/bin`。

2. 动态生成和执行命令

   ```bash
   # 根据条件构建命令
   options="-l -h"
   cmd="ls $options"
   eval $cmd

   # 构建带参数的复杂命令
   port=8080
   host="localhost"
   eval "curl -X POST http://$host:$port/api"

   # 多个命令组合成一个字符串进行一次性执行
   cmd1="echo Hello"
   cmd2="echo World"
   eval "$cmd1; $cmd2"  # 输出2行，Hello 和 World
   ```

3. 环境变量的展开

   ```bash
   # 展开环境变量字符串
   path_var='$HOME/documents'
   eval echo $path_var  # 将输出实际的home路径
   ```

4. 处理命令行参数

   ```bash
   # 处理带引号的参数
   args='"arg1 with space" arg2'
   eval set -- $args
   echo $1  # 输出: arg1 with space
   ```

5. 配置文件处理

   ```bash
   # 读取配置文件中的变量定义
   config_line="export JAVA_HOME=/usr/lib/java"
   eval $config_line
   ```

6. 处理复杂的命令组合

   ```bash
   eval "for i in {1..3}; do echo \$i; done"
   ```

**注意事项**：

- **安全性**：由于 `eval` 会执行传入的所有内容，因此要注意不要用 `eval` 直接运行来自不可信源的输入，避免安全风险。
- **调试难度**：因为 `eval` 会两次解析内容，所以可能会导致调试较复杂的命令困难。
- 避免直接执行来自用户输入的命令，可能存在安全风险
- 在使用 `eval` 前应该检查用户输入和对特殊字符进行转义
- 优先考虑使用数组或其他内置命令
- 谨慎处理包含空格或特殊字符的字符串
- 尽可能使用其他更安全的替代方法

### `eval` 后跟命令/字符串

在 `eval` 中，我们可以直接跟字符串，也可以跟其他命令（如 `echo` 等），它们的执行结果会有所不同。

1. `eval` 后面直接跟字符串

   当 `eval` 后面直接跟字符串时，`eval` 会把这个字符串当作命令执行。通常，我们会把这个字符串放在**双引号**中，来确保变量替换和命令替换正常进行。

   ```bash
   cmd="echo Hello $USER"
   eval "$cmd"
   ```

   这里，`eval` 会首先解析 `$cmd` 的内容，把它变成 `echo Hello your_username`，然后执行这个命令。最终输出 `Hello your_username`。

2. `eval` 后面跟 `echo`

   当 `eval` 后面跟 `echo` 时，`eval` 会先解析其后面的内容，然后执行它。`echo` 只会把内容打印出来，而不真正执行任何命令。

   ```bash
   cmd="echo Hello $USER"
   eval echo "$cmd"
   ```

   在这个例子中，`eval` 会解析 `"$cmd"`，将其内容变为 `echo Hello your_username`，然后执行这个 `echo` 命令。最终输出的结果是：`echo Hello your_username`

   > **总结**：
   >
   > - **`eval "$cmd"`**：会把 `cmd` 中的内容当作命令来执行。
   > - **`eval echo "$cmd"`**：只是将 `$cmd` 的内容打印出来，但不执行。

3. `eval` 后面跟其他命令

   `eval` 也可以跟任何其他有效的 Shell 命令，不只是字符串或 `echo`，如 `ls`、`cat` 等命令。一般来说，`eval` 会先对整个命令进行一次预处理（如变量解析、命令替换等），然后再执行。

   假设我们有文件路径变量 `path` 和文件名变量 `filename`：

   ```bash
   path="/usr/local"
   filename="bin"
   eval "ls $path/$filename"  # 效果与 eval ls "$path/$filename" 一样
   ```

   `eval` 会将 `ls $path/$filename` 解析为 `ls /usr/local/bin`，然后执行 `ls /usr/local/bin`，列出该目录内容。

### `eval` 后跟单/双/反引号

`eval` 后面跟不同类型的引号效果不同：

1. 双引号 (")：

   - 变量会在 eval 执行前展开
   - 允许变量和命令替换

   ```bash
   name="John"
   eval "echo Hello $name"  # 输出：Hello John
   ```

2. 单引号 (')：

   - 变量不会被展开
   - 内容会被原样解释

   ```bash
   name="John"
   eval 'echo Hello $name'  # 输出：Hello $name
   ```

3. 反引号 (`) 或 $()：

   - 用于命令替换
   - 命令会被执行并返回结果

   ```bash
   eval `echo "ls -l"`    # 执行 ls -l
   eval $(echo "ls -l")   # 同上，更现代的写法
   ```

**示例**：

```bash
# 双引号使用场景
var="world"
eval "message='Hello $var'"  # 变量会被展开

# 单引号使用场景
eval 'echo $PATH'  # $PATH 会在eval执行时才被展开

# 命令替换使用场景
eval `date "+now='%Y-%m-%d'"`
eval $(date "+now='%Y-%m-%d'")
```

**建议**：

- 优先使用双引号，便于变量展开
- 需要延迟变量展开时使用单引号
- 命令替换优先使用 $() 语法，更清晰易读

## xargs 命令

`xargs` 是 Linux 和 Unix 系统中的一个常用命令，用于将标准输入（例如管道或文件中的内容）转换为命令行参数。它允许你将其他命令的输出作为参数传递给指定的命令，特别适合处理多个输入，并将其批量传递给其他命令执行。

**基本语法**：

```bash
command | xargs [options] [command [initial-arguments]]
```

**常用选项**：

- `-n`：每次传递给命令的参数数目。

  ```shell
  echo "a b c" | xargs -n 1
  # 输出：
  # a
  # b
  # c
  ```

- `-d`: 自定义分隔符

  ```shell
  echo "a:b:c" | xargs -d ":" -n 1
  ```

- `-I`：指定占位符，用于替换输入。

  ```shell
  echo "file1 file2" | xargs -I {} cp {} backup/    # 每个文件拷贝到backup文件夹下
  ```

- `-P`：并行处理

  ```shell
  find . -type f | xargs -P 4 -I {} gzip {}  # 4个并行进程
  ```

- `-p`：提示用户确认执行每条命令。

  ```shell
  echo "a b c" | xargs -n 1 -p
  ```

- `-t`：打印每个命令（用于调试）。

  ```shell
  echo "a b c" | xargs -n 1 -t
  ```

- `-0`：配合 `find ... -print0` 使用，用于处理文件名中的空格或特殊字符。

**`xargs` 的主要功能**：

- **批量传递参数**：`xargs` 可以将多个输入拼接成一个命令的参数列表，以便一次性处理。
- **自动分批执行**：如果参数太多导致命令长度超限，`xargs` 会自动将其分批执行。
- **结合管道使用**：`xargs` 常与 `find`、`grep`、`cat` 等命令结合，通过管道传递数据，完成复杂任务。

**常见示例**：

1. `xargs` 批量删除文件：
   假设要删除当前目录下 `.tmp` 结尾的所有文件，可以使用 `find` 和 `xargs` 组合：

   ```bash
   find . -name "*.tmp" | xargs rm
   ```

   这里，`find` 会找到所有 `.txt` 文件并传递给 `xargs`，然后 `xargs` 执行 `rm` 命令来删除它们。

2. `xargs` 批量重命名：

   ```bash
   ls *.txt | xargs -I {} mv {} {}.bak
   ```

3. `xargs` 批量压缩：

   ```bash
   find . -name "*.log" | xargs gzip
   ```

4. 安全处理：
   处理包含空格的文件名：

   ```bash
   find . -type f -print0 | xargs -0 command
   ```

5. 使用 `xargs` 将单行转换为多行

   `xargs` 默认将输入按空格分隔为一行输出，即**前面命令的所有输出当成一行作为其他命令的参数**：

   ```bash
   echo "a b c d" | xargs
   # 输出: a b c d
   ```

6. 使用 `xargs` 和 `-I` 替换字符串

   `-I` 选项指定一个占位符（如 `{}`），`xargs` 将每个输入替换到占位符位置。当后面的命令有多个参数时使用，可以组装出更复杂的命令。例如：

   ```bash
   echo "file1 file2" | xargs -I {} mv {} /new_directory/
   ```

   这里 `{}` 是占位符，每个输入会替换 `{}`，然后执行 `mv` 命令将 `file1` 和 `file2` 移动到 `/new_directory/`。
