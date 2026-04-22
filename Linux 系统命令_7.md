[toc]

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
   - 测试条件根据需要加 `\( \)`，避免歧义：
     如：`find ${src_dir} -type f -name "*.log" -o -name "*.txt"` 被理解为：
     - `( -type f -a -name "*.log" )  -o  ( -name "*.txt" )`，而不是
     - `-type f \( -name "_.log" -o -name "_.txt" \)`

5. **动作（actions）**

   对匹配文件执行的操作：

   | 参数                  | 功能                                       |
   | --------------------- | ------------------------------------------ |
   | `-print`              | 打印路径（默认是换行符 `\n` 分隔符输出）   |
   | `-print0`             | 打印路径（用 `\0`（NUL 字符） 分隔符输出） |
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

四、遍历文件夹，执行操作

```shell
# GNU find 可以使用
find "$src_dir" -type f \( -name "*.log" -o -name "*.txt" \) -print0 |
  while IFS= read -r -d '' file; do
    cp "$file" "$dst_dir/"
  done

# toybox find 可以使用，因为其 -print0 在某些find版本下行为不可靠
adb shell 'find "'"$src_dir"'" -type f \( -name "*.log" -o -name "*.txt" \) -printf "%p\n"' |
  tr -d '\r' |
  while IFS= read -r file; do
    adb pull -a "$file" "$dst_dir/"
  done
```

命令分析：
一、`find` 命令的解析（重点）

1. `find` 的语法本质不是**参数式命令**，而是一个**表达式解释器**。

   ```bash
   find <路径> <测试条件> <逻辑运算符> <动作>
   ```

   每一个 `-type`、`-name`、`-o`、`-print0` 都是表达式的一部分。

   但`find` 里**有一个非常关键的优先级问题**：

   | 运算符                   | 优先级 |
   | ------------------------ | ------ |
   | 测试（`-type`, `-name`） | 高     |
   | `-a`（AND，默认）        | 中     |
   | `-o`（OR）               | **低** |

   而且：
   **多个条件默认用 `-a` 连接**

   不加括号会发生什么？

   如果你写成：

   ```bash
   # 不加括号
   find "$src_dir" -type f -name "*.log" -o -name "*.txt"
   # 实际理解为:
   ( -type f -a -name "*.log" )  -o  ( -name "*.txt" )

   # 加括号
   -type f \( -name "*.log" -o -name "*.txt" \)
   ```

2. `-print0` 作用是
   - 每找到一个文件
   - 用 **`\0`（NUL 字符）** 作为分隔符输出。而不是默认的换行符 `\n`。

   **目的：** 支持文件名包含：空格、制表符、换行、各种奇怪字符。这是和后面的 `read -d ''` **成对使用的**。

二、`while IFS= read -r -d '' file` 逐项拆解

1. `while ...; do ... done`

   这是标准 shell 循环：

   ```bash
   while <命令>; do
       ...
   done
   ```

   只要 `<命令>` 返回成功（0），循环就继续。

2. 管道的含义

   ```bash
   find ... -print0 | while ...
   ```

   把 `find` 的输出一条一条“喂”给 `read`

3. `IFS= read -r -d '' file` 作用

   这不是两个命令，而是**一条命令 + 临时环境赋值**，这是 **POSIX shell 的标准语法**。

   ```bash
   IFS= read -r -d '' file
   <变量临时赋值>  <命令>  <参数...>
   VAR=value command arg1 arg2
   ```

   - `IFS=` 置空
     IFS 被设置为“空值（unset-like empty）”，在 POSIX shell 中，其效果是：
     - **禁用字段分割**
     - read 会把整行（或整个记录）原样读入变量，**不做任何分隔**

     这是 read 官方推荐的用法。
     而 `IFS=''` 会随 shell 版本不同行为不一致，不推荐。

     这是严格模式下**必须的防御性写法**。

   - `read -r -d '' file` 表示：

     从标准输入读数据，直到遇到 **NUL 字符**，把内容存入变量 `file`。

     | 选项    | 含义                               |
     | ------- | ---------------------------------- |
     | `-d ''` | 分隔符是 `\0`（与 `-print0` 对应） |
     | `-r`    | 不处理反斜杠转义（防止路径被破坏） |
     | `file`  | 存放读到的完整文件路径             |

4. 总结（给你一个记忆锚点）
   - `\( ... -o ... \)`
     → **控制 OR 的作用范围**
   - `-print0 + read -d ''`
     → **安全处理任意文件名**
   - `IFS=`
     → **禁止拆词**
   - `-r`
     → **禁止反斜杠转义**

   这是一段**生产级、安全、严格模式兼容**的标准写法。

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

# ripgrep (rg) 使用手册

> ripgrep 是一个极速的递归文本搜索工具，默认遵守 `.gitignore` 规则，自动跳过隐藏文件和二进制文件。

## 安装

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

## 基本语法

```log
rg [OPTIONS] PATTERN [PATH ...]
rg [OPTIONS] -e PATTERN ... [PATH ...]
rg [OPTIONS] -f PATTERNFILE ... [PATH ...]
rg [OPTIONS] --files [PATH ...]
command | rg [OPTIONS] PATTERN
```

## 常用命令示例

1. **基础搜索**

   ```bash
   # 在当前目录递归搜索 "foo"
   rg foo

   # 在指定目录搜索
   rg foo ./src

   # 在指定文件中搜索
   rg foo main.cpp

   # 搜索以 - 开头的模式（用 -e 或 -- 避免歧义）
   rg -e -foo
   rg -- -foo
   ```

2. **大小写控制**

   ```bash
   # 忽略大小写
   rg -i foo

   # 智能大小写（全小写模式时忽略大小写，含大写时区分）
   rg -S Foo

   # 强制区分大小写
   rg -s Foo
   ```

3. **上下文显示**

   ```bash
   # 显示匹配行前后各 3 行
   rg -C 3 foo

   # 只显示匹配行后 2 行
   rg -A 2 foo

   # 只显示匹配行前 2 行
   rg -B 2 foo
   ```

4. 文件类型过滤

   ```bash
   # 只搜索 Python 文件
   rg -t py foo

   # 只搜索 C++ 文件
   rg -t cpp foo

   # 排除 JSON 文件
   rg -T json foo

   # 查看所有支持的文件类型
   rg --type-list
   ```

5. Glob 模式过滤

   ```bash
   # 只搜索 .cpp 和 .h 文件
   rg -g '*.cpp' -g '*.h' foo

   # 排除所有测试文件
   rg -g '!*test*' foo

   # 只搜索某个子目录下的文件
   rg -g 'src/**' foo
   ```

6. 统计匹配

   ```bash
   # 统计每个文件的匹配行数
   rg -c foo

   # 统计每个文件的匹配次数（同一行多个算多次）
   rg --count-matches foo

   # 显示有匹配的文件路径（不显示内容）
   rg -l foo

   # 显示没有匹配的文件路径
   rg --files-without-match foo
   ```

7. 输出格式控制

   ```bash
   # 显示行号（终端下默认开启）
   rg -n foo

   # 显示列号
   rg --column foo

   # 只输出匹配的部分（非整行）
   rg -o 'foo\w+'

   # 替换输出中的匹配内容（不修改文件）
   rg foo -r bar

   # 使用捕获组替换
   rg '(\w+)@(\w+)' -r '$1 at $2'

   # 美化输出（强制彩色 + 行号 + 分组）
   rg -p foo | less -R
   ```

8. 搜索隐藏文件 / 忽略规则控制

   ```bash
   # 搜索隐藏文件和目录（以 . 开头的）
   rg -. foo
   rg --hidden foo

   # 忽略 .gitignore 规则
   rg -u foo

   # 忽略 .gitignore + 搜索隐藏文件
   rg -uu foo

   # 等价于 grep -r（忽略所有过滤规则 + 搜索二进制）
   rg -uuu foo
   ```

9. 正则表达式进阶

   ```bash
   # 固定字符串搜索（不解析正则元字符）
   rg -F 'foo.bar()'

   # 整行匹配
   rg -x 'exact line content'

   # 单词边界匹配
   rg -w foo

   # 多模式搜索（匹配任意一个）
   rg -e foo -e bar

   # 从文件读取多个模式
   rg -f patterns.txt

   # 启用 PCRE2（支持 lookahead、backreference）
   rg -P '(?<=@)\w+'

   # 多行匹配
   rg -U 'start.*end'
   ```

10. 目录遍历控制

    ```bash
    # 限制搜索深度为 2 层
    rg --max-depth 2 foo

    # 跟随符号链接
    rg -L foo

    # 不跨文件系统边界
    rg --one-file-system foo

    # 列出将被搜索的文件（不实际搜索）
    rg --files
    rg --files src/
    ```

11. 搜索二进制 / 压缩文件

    ```bash
    # 把二进制文件当文本搜索
    rg -a foo

    # 搜索压缩文件（gzip/bzip2/xz/zstd 等）
    rg -z foo

    # 启用二进制搜索（遇到 NUL 字节继续）
    rg --binary foo
    ```

12. 管道与组合使用

    ```bash
    # 在命令输出中搜索
    ps aux | rg nginx

    # 配合 xargs 处理匹配文件（用 -0 避免空格问题）
    rg -l foo -0 | xargs -0 wc -l

    # 多级管道（实时日志过滤）
    tail -f app.log | rg ERROR --line-buffered | rg timeout

    # 输出 JSON 格式（供程序解析）
    rg --json foo
    ```

13. 排序输出

    ```bash
    # 按文件路径排序
    rg --sort path foo

    # 按最近修改时间排序（新→旧）
    rg --sortr modified foo
    ```

## 选项速查表

**匹配控制**

| 选项         | 说明                       |
| ------------ | -------------------------- |
| `-e PATTERN` | 指定模式（可多次使用）     |
| `-f FILE`    | 从文件读取模式             |
| `-i`         | 忽略大小写                 |
| `-s`         | 强制区分大小写             |
| `-S`         | 智能大小写                 |
| `-F`         | 固定字符串（不解析正则）   |
| `-w`         | 单词边界匹配               |
| `-x`         | 整行匹配                   |
| `-v`         | 反向匹配（输出不匹配的行） |
| `-U`         | 多行匹配模式               |
| `-P`         | 使用 PCRE2 引擎            |

**输出控制**

| 选项              | 说明                       |
| ----------------- | -------------------------- |
| `-n`              | 显示行号                   |
| `-N`              | 不显示行号                 |
| `--column`        | 显示列号                   |
| `-l`              | 只输出匹配的文件名         |
| `-c`              | 输出每文件匹配行数         |
| `--count-matches` | 输出每文件匹配次数         |
| `-o`              | 只输出匹配部分             |
| `-r TEXT`         | 替换输出中的匹配内容       |
| `-A NUM`          | 显示匹配后 N 行            |
| `-B NUM`          | 显示匹配前 N 行            |
| `-C NUM`          | 显示匹配前后各 N 行        |
| `--passthru`      | 输出所有行（匹配行高亮）   |
| `-p`              | 美化输出（彩色+行号+分组） |
| `--json`          | 输出 JSON Lines 格式       |

**文件过滤**

| 选项                 | 说明                           |
| -------------------- | ------------------------------ |
| `-t TYPE`            | 只搜索指定类型文件             |
| `-T TYPE`            | 排除指定类型文件               |
| `-g GLOB`            | 按 glob 包含/排除文件          |
| `--iglob`            | 大小写不敏感 glob              |
| `--hidden` / `-.`    | 搜索隐藏文件                   |
| `--no-ignore` / `-u` | 忽略 .gitignore 等规则         |
| `-uu`                | 同上 + 搜索隐藏文件            |
| `-uuu`               | 同上 + 搜索二进制（≈ grep -r） |
| `--max-depth NUM`    | 限制目录递归深度               |
| `-L`                 | 跟随符号链接                   |
| `--max-filesize`     | 忽略超过指定大小的文件         |
| `-z`                 | 搜索压缩文件                   |
| `-a`                 | 把二进制当文本搜索             |

**其他实用选项**

| 选项                       | 说明                         |
| -------------------------- | ---------------------------- |
| `--files`                  | 列出将被搜索的文件           |
| `-m NUM`                   | 每文件最多输出 N 个匹配行    |
| `-0`                       | 文件名后跟 NUL（配合 xargs） |
| `--sort path/modified/...` | 升序排序                     |
| `--sortr`                  | 降序排序                     |
| `-j NUM`                   | 指定线程数                   |
| `--stats`                  | 输出搜索统计信息             |
| `-q`                       | 静默模式（只用退出码）       |
| `--type-list`              | 列出所有支持的文件类型       |

## 正则语法速查（默认引擎）

| 语法                     | 含义                                   |
| ------------------------ | -------------------------------------- |
| `.`                      | 任意字符（不含换行）                   |
| `\w` / `\d` / `\s`       | 单词字符 / 数字 / 空白（Unicode 感知） |
| `^` / `$`                | 行首 / 行尾                            |
| `\b` / `\B`              | 词边界 / 非词边界                      |
| `[abc]`                  | 字符类                                 |
| `(foo\| bar)`            | 或                                     |
| `foo*` / `foo+` / `foo?` | 量词                                   |
| `foo{2,4}`               | 重复次数                               |
| `(?i)`                   | 内联忽略大小写                         |
| `(?s)`                   | 内联 dot-all 模式                      |

> 需要 lookahead/lookbehind/backreference 时请加 `-P` 使用 PCRE2 引擎。

## 默认开启选项

根据帮助文档，`rg <PATTERN>` 默认开启的行为如下：

**搜索范围**

- 从当前目录开始**递归搜索**
- 自动跳过 `.gitignore` / `.ignore` / `.git/info/exclude` 等忽略规则中的文件
- 自动跳过**隐藏文件和目录**（以 `.` 开头的）
- 自动跳过**二进制文件**（检测到 NUL 字节即停止）

**输出格式**

- 输出到终端时，自动开启**彩色高亮**（`--color auto`）
- 输出到终端时，自动开启**行号显示**（`-n`）
- 输出到终端时，自动开启**分组heading**（同一文件的匹配结果归在文件名下方）

**编码**

- 编码检测为 `auto`：仅对带 UTF-8/UTF-16 BOM 的文件做自动识别，其余按原始字节搜索

**正则引擎**

- 使用默认的有限自动机引擎（非 PCRE2），**Unicode 模式开启**，`\w \d \s` 等均为 Unicode 感知

**缓冲策略**

- 输出到终端时用**行缓冲**（每匹配一行立即输出）
- 输出到管道/文件时自动切换为**块缓冲**（更快）

**线程**

- 线程数由 ripgrep **自动启发式决定**（`-j 0`），通常等于 CPU 核心数，多线程并行搜索

**路径显示**

- 搜索多个文件时自动带文件名前缀；只搜索单个文件时默认不带

> 一句话总结：**默认是"聪明模式"** —— 快速、彩色、有行号、遵守 git 忽略规则、跳过隐藏和二进制，适合在代码仓库里日常使用。想突破这些限制就用 `-u`（逐级解除）。

## 配置文件

ripgrep 支持通过环境变量指定配置文件，把常用选项持久化：

```bash
# Linux/macOS：在 ~/.bashrc 或 ~/.zshrc 中添加
export RIPGREP_CONFIG_PATH="$HOME/.ripgreprc"
# ~/.ripgreprc 示例
--smart-case
--hidden
--glob=!.git
--glob=!node_modules
```
