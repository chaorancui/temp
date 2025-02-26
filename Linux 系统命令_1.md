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

### grep 命令

- grep 的作用是**在文件中**提取和匹配符合条件的字符串行。命令格式如下

```bash
grep [选项] "搜索内容" 文件名
```

find 也是搜索命令，那么 find 命令和 grep 命令有什么区别呢？
find 命令
find 命令用于在系统中搜索符合条件的文件名，如果需要模糊查询，则使用通配符进行匹配，通配符是完全匹配（find 命令可以通过-regex 选项，把匹配规则转为正则表达式规则，但是不建议如此）。
grep 命令
grep 命令用于在文件中搜索符合条件的字符串，如果需要模糊查询，则使用正则表达式进行匹配，正则表达式是包含匹配。

### 通配符与正则表达式的区别

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

# 文件操作命令

## cp 命令

## mv 命令

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

# 压缩解压命令

## tar 包

`tar` 是 Linux 中常用的打包和压缩工具，可以将多个文件或目录打包成一个归档文件，也可以用于解压这些归档文件。

### 解压 `.tar` 包

如果你有一个 `.tar` 格式的文件，没有经过压缩，只是打包文件，可以使用以下命令：

```bash
tar -xvf archive.tar
```

- `x`：表示解压。
- `v`：显示详细过程（可选，但通常会显示解压过程中的每个文件）。
- `f`：后面跟的是归档文件名。

总结

- **`.tar` 文件**：`tar -xvf archive.tar`
- **`.tar.gz` 或 `.tgz` 文件**：`tar -xzvf archive.tar.gz`
- **`.tar.bz2` 文件**：`tar -xjvf archive.tar.bz2`
- **`.tar.xz` 文件**：`tar -xJvf archive.tar.xz`

## zip 包

在 Linux 系统中，解压 `.zip` 文件通常使用 `unzip` 命令。如果系统上没有安装 `unzip`，你可以先安装它。

1. `unzip` 解压：

   Debian/Ubuntu 系统上安装：`sudo apt-get install unzip`

   **解压 `.zip` 文件**：

   ```bash
   # 解压到当前目录中
   unzip archive.zip
   ```

   - `x`：表示解压并保持文件夹结构。

   **解压到指定目录**： 如果你想将 `.zip` 文件解压到指定目录，可以使用 `-d` 选项：

   ```bash
   unzip archive.zip -d /path/to/destination/
   ```

   **列出 `.zip` 文件内容**（不解压）： 如果你只想查看 `.zip` 文件内包含的文件列表，可以使用：

   ```bash
   unzip -l archive.zip
   ```

## rar 包

1. `unrar` 解压：

   `unrar` 是一个开源工具，通常用于解压 `.rar` 文件。Debian/Ubuntu 系统上安装：`sudo apt-get install unrar`

   **解压 `.rar` 文件**：

   ```bash
   # 解压到当前目录中
   unrar x archive.rar
   ```

   - `x`：表示解压并保持文件夹结构。

   **解压到指定目录**： 如果你想将 `.rar` 文件解压到指定目录，可以使用 `-d` 选项：

   ```bash
   unrar x archive.rar -d /path/to/extract/directory/
   ```

   **列出 `.rar` 文件内容**（不解压）： 如果你只想查看 `.rar` 文件内包含的文件列表，可以使用：

   ```bash
   unrar l archive.rar
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

总结

`printf` 是一个非常强大的工具，适用于需要格式化输出的场合。它能够提供丰富的格式控制选项，帮助用户创建更易读和专业的输出结果。与 `echo` 相比，`printf` 更加灵活，适合在脚本中处理复杂的输出需求。

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
