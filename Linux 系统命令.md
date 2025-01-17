[toc]

# Linux 命令

> [Linux Tools Quick Tutorial](https://linuxtools-rst.readthedocs.io/zh-cn/latest/base/index.html)

# 系统版本命令

## 查看 Linux 发行版本名和版本号

如果你加入了一家新公司，要为开发团队安装所需的软件并重启服务，这个时候首先要弄清楚它们运行在什么发行版以及哪个版本的系统上，你才能正确完成后续的工作。作为系统管理员，充分了解系统信息是首要的任务。

因为对于诸如 RHEL、Debian、openSUSE、Arch Linux 这几种主流发行版来说，它们各自拥有不同的包管理器来管理系统上的软件包，如果不知道所使用的是哪一个发行版的系统，在软件包安装的时候就会无从下手，而且由于大多数发行版都是用 systemd 命令而不是 SysVinit 脚本，在重启服务的时候也难以执行正确的命令。

1. `lsb_release` 命令

   LSB（Linux 标准库 Linux Standard Base）能够打印发行版的具体信息，包括发行版名称、版本号、代号等。

   ```bash
   # lsb_release -a
   No LSB modules are available.
   Distributor ID: Ubuntu
   Description: Ubuntu 16.04.3 LTS
   Release: 16.04
   Codename: xenial
   ```

2. 查看 `/etc/*-release` 文件

   release 文件通常被视为操作系统的标识。在 `/etc` 目录下放置了很多记录着发行版各种信息的文件，每个发行版都各自有一套这样记录着相关信息的文件。下面是一组在 Ubuntu/Debian 系统上显示出来的文件内容 `cat /etc/lsb-release`。
   在 RHEL/CentOS/Fedora 系统上分别为 `/etc/redhat-release` 和 `/etc/system-release` 文件，他们是指向 `/etc/[发行版名称]-release` 文件的一个连接。

   ```bash
   # cat /etc/issue
   Ubuntu 16.04.3 LTS \n \l

   # cat /etc/issue.net
   Ubuntu 16.04.3 LTS

   # cat /etc/lsb-release
   DISTRIB_ID=Ubuntu
   DISTRIB_RELEASE=16.04
   ......

   # cat /etc/os-release
   NAME="Ubuntu"
   VERSION="16.04.3 LTS (Xenial Xerus)"
   ......

   # cat /etc/debian_version
   9.3

   # cat /etc/centos-release
   # cat /etc/fedora-release
   # cat /etc/os-release
   # cat /etc/redhat-release
   # cat /etc/system-release
   ```

3. `uname` 命令

   uname（unix name 的意思） 是一个打印系统信息的工具，包括内核名称、版本号、系统详细信息以及所运行的操作系统等等。

   - **建议阅读：** [6 种查看系统 Linux 内核的方法](https://www.2daygeek.com/check-find-determine-running-installed-linux-kernel-version/)

   ```bash
   # uname -a
   Linux 2grhel8node 4.18.0-477.13.1.el8_8.x86_64 #1 SMP Thu May 18 10:27:05 EDT 2023 x86_64 x86_64 x86_64 GNU/Linux
   ```

   解释如下:

   - Linux – Kernel name. The name of the kernel running on your system.
   - 2grhel8node – Hostname
   - 4.18.0-477.13.1.el8_8.x86_64 – Kernel release
   - 1 SMP Thu May 18 10:27:05 EDT 2023 – Kernel version and last compiled date and time.
   - x86_64 – Machine architecture
   - x86_64 – Processor architecture
   - x86_64 – Operating system architecture
   - GNU/Linux – Operating system

4. `/proc/version` 文件

   这个文件记录了 Linux 内核的版本、用于编译内核的 gcc 的版本、内核编译的时间，以及内核编译者的用户名。

   ```bash
   # cat /proc/version
   Linux version 4.12.14-300.fc26.x86_64 ([email protected]) (gcc version 7.2.1 20170915 (Red Hat 7.2.1-2) (GCC) ) #1 SMP Wed Sep 20 16:28:07 UTC 2017
   ```

## SUSE 的包管理工具 zypper

> [zypper 命令使用示例](https://www.linuxprobe.com/zypper-commands-examples.html)

1. 安装包

   ```bash
   zypper install

   # 示例：安装 Mozilla firefox
   zypper install MozillaFirefox
   ```

2. 安装源码包

   ```bash
   zypper source-install

   # 示例：从库中安装 apache
   zypper source-install apache2-mod_nss
   ```

3. 更新包

   ```shell
   zypper list-updates # 查看所有可用的更新列表
   zypper update xxx # 更新某一软件包
   zypper update # 更新所有软件包
   ```

4. 删除包

   ```bash
   zypper remove

   # 示例：移除 Mozilla Firefox
   zypper remove MozillaFirefox
   ```

5. 查找包

   ```bash
   zypper search

   # 示例：查找所有 usb 开头的软件包
   zypper search usb*
   ```

6. 查看软件包详情

   ```bash
   zypper info

   # 示例：查看 usbutils 的信息
   zypper info usbutils
   ```

7. 打补丁

   ```bash
   zypper patches # 查看所有可打补丁
   zypper patch # 安装指定补丁
   ```

8. 锁住包

   软件包被锁之后将不能被移除或升级，下面演示一下如何加锁

   ```bash
   zypper ll # List Locks，查看所有已被锁住的软件包
   zypper al usbutils # add lock，锁住包文件 usbutils
   zypper rl usbutils # remove lock，解锁 usbutils
   ```

## Terminal 终端快捷键汇总

1. 常用快捷键

   ctrl+左右键: 在单词之间跳转
   ctrl+a: 跳到本行的行首
   ctrl+e: 跳到页尾
   Ctrl+u：删除当前光标前面的文字 （还有剪切功能）
   ctrl+k：删除当前光标后面的文字(还有剪切功能)
   Ctrl+L：进行清屏操作
   Ctrl+y: 粘贴 Ctrl+u 或 ctrl+k 剪切的内容
   Ctrl+w: 删除光标前面的单词的字符
   Alt – d ：由光标位置开始，往右删除单词。往行尾删

2. 移动光标

   Ctrl – a ：移到行首
   Ctrl – e ：移到行尾
   Ctrl – b ：往回(左)移动一个字符
   Ctrl – f ：往后(右)移动一个字符
   Alt – b ：往回(左)移动一个单词
   Alt – f ：往后(右)移动一个单词
   Ctrl – xx ：在命令行尾和光标之间移动
   M-b ：往回(左)移动一个单词
   M-f ：往后(右)移动一个单词

3. 编辑命令

   Ctrl – h ：删除光标左方位置的字符
   Ctrl – d ：删除光标右方位置的字符（注意：当前命令行没有任何字符时，会注销系统或结束终端）
   Ctrl – w ：由光标位置开始，往左删除单词。往行首删
   Alt – d ：由光标位置开始，往右删除单词。往行尾删
   M – d ：由光标位置开始，删除单词，直到该单词结束。
   Ctrl – k ：由光标所在位置开始，删除右方所有的字符，直到该行结束。
   Ctrl – u ：由光标所在位置开始，删除左方所有的字符，直到该行开始。
   Ctrl – y ：粘贴之前删除的内容到光标后。
   ctrl – t ：交换光标处和之前两个字符的位置。
   Alt + . ：使用上一条命令的最后一个参数。
   Ctrl – \_ ：回复之前的状态。撤销操作。
   Ctrl -a + Ctrl -k 或 Ctrl -e + Ctrl -u 或 Ctrl -k + Ctrl -u 组合可删除整行。

4. Bang(!)命令

   !! ：执行上一条命令。
   !wget ：执行最近的以 wget 开头的命令。
   !wget:p ：仅打印最近的以 wget 开头的命令，不执行。
   !$ ：上一条命令的最后一个参数， 与 Alt - . 和 $\_ 相同。
   !_：上一条命令的所有参数
   !_:p ：打印上一条命令是所有参数，也即 !\*的内容。
   ^abc ：删除上一条命令中的 abc。
   !-n ：执行前 n 条命令，执行上一条命令： !-1， 执行前 5 条命令的格式是： !-5 查找历史命令
   Ctrl – p ：显示当前命令的上一条历史命令
   Ctrl – n ：显示当前命令的下一条历史命令
   Ctrl – r ：搜索历史命令，随着输入会显示历史命令中的一条匹配命令，Enter 键执行匹配命令；ESC 键在命令行显示而不执行匹配命令。
   Ctrl – g ：从历史搜索模式（Ctrl – r）退出。

5. 控制命令

   Ctrl – l ：清除屏幕，然后，在最上面重新显示目前光标所在的这一行的内容。
   Ctrl – o ：执行当前命令，并选择上一条命令。
   Ctrl – s ：阻止屏幕输出
   Ctrl – q ：允许屏幕输出
   Ctrl – c ：终止命令
   Ctrl – z ：挂起命令

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

# 系统设备命令

## lspci 命令

**lspci** 是一个用来显示系统中所有 PCI 总线设备或连接到该总线上的所有设备的工具。

```bash
lspci [options]
```

- **-v**

  使得 _lspci_ 以冗余模式显示所有设备的详细信息。

- **-vv**

  使得 _lspci_ 以过冗余模式显示更详细的信息 (事实上是 PCI 设备能给出的所有东西)。这些数据的确切意义没有在此手册页中解释，如果你想知道更多，请参照 **/usr/include/linux/pci.h** 或者 PCI 规范。

- **-t**

  以树形方式显示包含所有总线、桥、设备和它们的连接的图表。

```shell
# 实例
# 查看网卡生产商，型号
lspci | grep -i net
```

# 系统信息命令

## dmesg 命令

[dmesg 命令](https://www.runoob.com/linux/linux-comm-dmesg.html)

Linux dmesg（英文全称：display message）命令用于显示开机信息。

kernel 会将开机信息存储在 ring buffer 中。您若是开机时来不及查看信息，可利用 dmesg 来查看。开机信息亦保存在 /var/log 目录中，名称为 dmesg 的文件里。

```bash
dmesg [-cn][-s <缓冲区大小>]
```

- -c 　显示信息后，清除 ring buffer 中的内容。
- -s<缓冲区大小> 　预设置为 8196，刚好等于 ring buffer 的大小。
- -n 　设置记录信息的层级。

```bash
# 实例
# 显示开机信息
dmesg |less
```

# 系统服务命令

## systemctl 命令

列出所有 service

```shell
systemctl list-units --type=service
systemctl --type=service
```

服务开机自启动，以 ssh 服务为例：

```shell
# 开机自动启动ssh命令
sudo systemctl enable ssh

# 关闭ssh开机自动启动命令
sudo systemctl disable ssh

# 单次开启ssh
sudo systemctl start ssh

# 单次关闭ssh
sudo systemctl stop ssh

# 设置好后重启系统
reboot

#查看ssh是否启动，看到Active: active (running)即表示成功
sudo systemctl status ssh
```

# 网络命令

## ip 命令

Linux 下 [ip](https://www.runoob.com/linux/linux-comm-ip.html) 命令与 [ifconfig](https://www.runoob.com/linux/linux-comm-ifconfig.html) 命令类似，但比 ifconfig 命令更加强大，主要功能是用于显示或设置网络设备。

ip 命令是 Linux 加强版的的网络配置工具，用于代替 ifconfig 命令。

```shell
ip [ OPTIONS ] OBJECT { COMMAND | help }
```

OBJECT 为常用对象，值可以是以下几种：

```shell
OBJECT={ link | addr | addrlabel | route | rule | neigh | ntable | tunnel | maddr | mroute | mrule | monitor | xfrm | token }
```

常用对象的取值含义如下：

- link：网络设备
- address：设备上的协议（IP 或 IPv6）地址
- addrlabel：协议地址选择的标签配置
- route：路由表条目
- rule：路由策略数据库中的规则

OPTIONS 为常用选项，值可以是以下几种：

```shell
OPTIONS={ -V[ersion] | -s[tatistics] | -d[etails] | -r[esolve] | -h[uman-readable] | -iec | -f[amily] { inet | inet6 | ipx | dnet | link } | -o[neline] | -t[imestamp] | -b[atch] [filename] | -rc[vbuf] [size] }
```

常用选项的取值含义如下：

- -V：显示命令的版本信息；
- -s：输出更详细的信息；
- -f：强制使用指定的协议族；
- -4：指定使用的网络层协议是 IPv4 协议；
- -6：指定使用的网络层协议是 IPv6 协议；
- -0：输出信息每条记录输出一行，即使内容较多也不换行显示；
- -r：显示主机时，不使用 IP 地址，而使用主机的域名。

```shell
# 实例
ip link show         # 显示网络接口信息
ip link list         # 用 ip 命令显示网络设备的运行状态：
ip -s link list      # 显示更加详细的设备信息：
ip addr show         # 显示网卡IP信息
ip route list        # 显示核心路由表：
ip link | grep -E '^[0-9]' | awk -F: '{print $2}'  # 获取主机所有网络接口：
```

## ifconfig 命令

[ifconfig 命令](https://www.runoob.com/linux/linux-comm-ifconfig.html)

需要安装如下工具：

```shell
apt install net-tools
```

配置和显示 Linux 系统网卡的网络参数。用 ifconfig 命令配置的网卡信息，在网卡重启后机器重启后，配置就不存在。要想将上述的配置信息永远的存的电脑里，那就要修改网卡的配置文件了。

```shell
ifconfig [网络设备][down up -allmulti -arp -promisc][add<地址>][del<地址>][<hw<网络设备类型><硬件地址>][io_addr<I/O地址>][irq<IRQ地址>][media<网络媒介类型>][mem_start<内存地址>][metric<数目>][mtu<字节>][netmask<子网掩码>][tunnel<地址>][-broadcast<地址>][-pointopoint<地址>][IP地址]
```

**参数说明**：

- add<地址> 设置网络设备 IPv6 的 IP 地址。
- del<地址> 删除网络设备 IPv6 的 IP 地址。
- down 关闭指定的网络设备。
- <hw<网络设备类型><硬件地址> 设置网络设备的类型与硬件地址。
- io_addr<I/O 地址> 设置网络设备的 I/O 地址。
- irq<IRQ 地址> 设置网络设备的 IRQ。
- media<网络媒介类型> 设置网络设备的媒介类型。
- mem_start<内存地址> 设置网络设备在主内存所占用的起始地址。
- metric<数目> 指定在计算数据包的转送次数时，所要加上的数目。
- mtu<字节> 设置网络设备的 MTU。
- netmask<子网掩码> 设置网络设备的子网掩码。
- tunnel<地址> 建立 IPv4 与 IPv6 之间的隧道通信地址。
- up 启动指定的网络设备。
- -broadcast<地址> 将要送往指定地址的数据包当成广播数据包来处理。
- -pointopoint<地址> 与指定地址的网络设备建立直接连线，此模式具有保密功能。
- -promisc 关闭或启动指定网络设备的 promiscuous 模式。
- [IP 地址] 指定网络设备的 IP 地址。
- [网络设备] 指定网络设备的名称。

```shell
# 实例
ifconfig   #处于激活状态的网络接口
ifconfig -a  #所有配置的网络接口，不论其是否激活
ifconfig eth0  #显示eth0的网卡信息

# 显示网络设备信息（激活状态的）：
[root@localhost ~]# ifconfig
eth0      Link encap:Ethernet  HWaddr 00:16:3E:00:1E:51
          inet addr:10.160.7.81  Bcast:10.160.15.255  Mask:255.255.240.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:61430830 errors:0 dropped:0 overruns:0 frame:0
          TX packets:88534 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:3607197869 (3.3 GiB)  TX bytes:6115042 (5.8 MiB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:56103 errors:0 dropped:0 overruns:0 frame:0
          TX packets:56103 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:5079451 (4.8 MiB)  TX bytes:5079451 (4.8 MiB)
```

说明：

**eth0** 表示第一块网卡，其中`HWaddr`表示网卡的物理地址，可以看到目前这个网卡的物理地址(MAC 地址）是`00:16:3E:00:1E:51`。

**inet addr** 用来表示网卡的 IP 地址，此网卡的 IP 地址是`10.160.7.81`，广播地址`Bcast:10.160.15.255`，掩码地址`Mask:255.255.240.0`。

**lo** 是表示主机的回坏地址，这个一般是用来测试一个网络程序，但又不想让局域网或外网的用户能够查看，只能在此台主机上运行和查看所用的网络接口。比如把 httpd 服务器的指定到回坏地址，在浏览器输入 127.0.0.1 就能看到你所架 WEB 网站了。但只是您能看得到，局域网的其它主机或用户无从知道。

- 第一行：连接类型：Ethernet（以太网）HWaddr（硬件 mac 地址）。
- 第二行：网卡的 IP 地址、子网、掩码。
- 第三行：UP（代表网卡开启状态）RUNNING（代表网卡的网线被接上）MULTICAST（支持组播）MTU:1500（最大传输单元）：1500 字节。
- 第四、五行：接收、发送数据包情况统计。
- 第七行：接收、发送数据字节数统计信息。

**启动关闭指定网卡：**

```shell
ifconfig eth0 up
ifconfig eth0 down
```

`ifconfig eth0 up`为启动网卡 eth0，`ifconfig eth0 down`为关闭网卡 eth0。ssh 登陆 linux 服务器操作要小心，关闭了就不能开启了，除非你有多网卡。

**为网卡配置和删除 IPv6 地址：**

```shell
ifconfig eth0 add 33ffe:3240:800:1005::2/64    #为网卡eth0配置IPv6地址
ifconfig eth0 del 33ffe:3240:800:1005::2/64    #为网卡eth0删除IPv6地址
```

**用 ifconfig 修改 MAC 地址：**

```shell
ifconfig eth0 hw ether 00:AA:BB:CC:dd:EE
```

**配置 IP 地址：**

```shell
[root@localhost ~]# ifconfig eth0 192.168.2.10
[root@localhost ~]# ifconfig eth0 192.168.2.10 netmask 255.255.255.0
[root@localhost ~]# ifconfig eth0 192.168.2.10 netmask 255.255.255.0 broadcast 192.168.2.255
```

## iwconfig 命令

需要安装如下工具：

```shell
sudo apt install wireless-tools
```

iwconfig 系统配置无线网络设备或显示无线网络设备信息。iwconfig 命令类似于 ifconfig 命令，但是他配置对象是无线网卡，它对网络设备进行无线操作，如设置无线通信频段

```shell
iwconfig [interface]
```

- auto 自动模式
- essid 设置 ESSID
- nwid 设置网络 ID
- freq 设置无线网络通信频段
- chanel 设置无线网络通信频段
- sens 设置无线网络设备的感知阀值
- mode 设置无线网络设备的通信设备
- ap 强迫无线网卡向给定地址的接入点注册
- nick<名字> 为网卡设定别名
- rate<速率> 设定无线网卡的速率
- rts<阀值> 在传输数据包之前增加一次握手，确信信道在正常的
- power 无线网卡的功率设置

```shell
# 实例
iwconfig    # 显示无线网络配置
```

## wpa_supplicant 工具

wpa_supplicant 工具集，包括 wpa_supplicant*、*wpa_passphrase、wpa_cli

# 程序分析命令

## ldd(list dynamic dependencies)

# 网络协议命令

## curl 命令

> [curl 的用法指南](https://www.ruanyifeng.com/blog/2019/09/curl-reference.html)
>
> [curl 命令详解](https://handerfly.github.io/linux/2019/05/26/curl%E5%91%BD%E4%BB%A4%E8%AF%A6%E8%A7%A3/)
>
> [Linux curl 命令详解](https://www.cnblogs.com/duhuo/p/5695256.html)

`curl` 命令是一个功能强大的网络工具，它的名字就是客户端（client）的 URL 工具的意思。它能够通过 http、ftp 等方式下载文件，也能够上传文件，同时支持 HTTPS 等众多协议，还支持 POST、cookies、认证、从指定偏移处下载部分文件、用户代理字符串、限速、文件大小、进度条等特征。其实 curl 远不止前面所说的那些功能，大家可以通过 man curl 阅读手册页获取更多的信息。

类似的工具还有 wget。

常用参数 curl 命令参数很多，这里只列出 shell 脚本中经常用到过的那些。

```shell
-a/--append 上传文件时，附加到目标文件

-A:随意指定自己这次访问所宣称的自己的浏览器信息

-b/--cookie <name=string/file> cookie字符串或文件读取位置，使用option来把上次的cookie信息追加到http request里面去。

-c/--cookie-jar <file> 操作结束后把cookie写入到这个文件中

-C/--continue-at <offset>  断点续转

-d/--data <data>   HTTP POST方式传送数据

    --data-ascii <data> 以ascii的方式post数据
     --data-binary <data> 以二进制的方式post数据
     --negotiate 使用HTTP身份验证
     --digest 使用数字身份验证
     --disable-eprt 禁止使用EPRT或LPRT
     --disable-epsv 禁止使用EPSV
-D/--dump-header <file> 把header信息写入到该文件中

     --egd-file <file>  为随机数据(SSL)设置EGD socket路径

     --tcp-nodelay     使用TCP_NODELAY选项

-e/--referer <URL>  指定引用地址

-F/--form <name=content>   模拟http表单提交数据

     --form-string <name=string> 模拟http表单提交数据

-G/--get    以get的方式来发送数据

-H/--header <header> 指定请求头参数

    --ignore-content-length  忽略的HTTP头信息的长度

-i/--include     输出时包括protocol头信息

-I/--head 仅返回头部信息，使用HEAD请求

-k/--insecure  允许不使用证书到SSL站点

-K/--config    指定的配置文件读取

-l/--list-only   列出ftp目录下的文件名称

    --limit-rate <rate> 设置传输速度

     --local-port<NUM>  强制使用本地端口号

-m/--max-time <seconds> 指定处理的最大时长

     --max-redirs <num>    设置最大读取的目录数

     --max-filesize <bytes>  设置最大下载的文件总量

-o/--output <file>   指定输出文件名称

-O/--remote-name  把输出写到该文件中，保留远程文件的文件名



-v/--verbose  小写的v参数，用于打印更多信息，包括发送的请求信息，这在调试脚本是特别有用。

-s/--slient 减少输出的信息，比如进度

--connect-timeout <seconds> 指定尝试连接的最大时长

-x/--proxy <proxyhost[:port]> 指定代理服务器地址和端口，端口默认为1080


-u/--user <user[:password]>设置服务器的用户和密码

-r/--range <range>检索来自HTTP/1.1或FTP服务器字节范围

   --range-file 读取（SSL）的随机文件

-R/--remote-time   在本地生成文件时，保留远程文件时间

    --retry <num>   指定重试次数

    --retry-delay <seconds>   传输出现问题时，设置重试间隔时间

    --retry-max-time <seconds>  传输出现问题时，设置最大重试时间

-s/--silent  静默模式。不输出任何东西

-S/--show-error  显示错误

    --socks4 <host[:port]> 用socks4代理给定主机和端口

    --socks5 <host[:port]> 用socks5代理给定主机和端口

    --stderr <file>

-x/--proxy <host[:port]> 在给定的端口上使用HTTP代理

-X/--request <command> 指定什么命令。curl默认的HTTP动词是GET，使用-X参数可以支持其他动词。

-T/--upload-file <file> 指定上传文件路径
```

## wget 命令

## scp 命令

> 参考：
>
> ```shell
> man scp
> ```

scp 在网络上的主机之间复制文件。

它使用 ssh 进行数据传输，并使用与登录会话相同的身份验证和提供相同的安全性。

scp 将要求提供密码或密码短语（如果身份验证需要它们）。

源和目标可以被指定为本地路径名、带有可选路径的远程主机（格式为 `[user@]host:[path]`）或 URI（格式为：
`scp://[user@]host[:port][/path]`）。可以使用绝对或相对路径名显式指定本地文件名，以避免 scp 处理包含“：”的文件名
作为主机说明符。

在两个远程主机之间进行复制时，如果使用 URI 格式，则在使用-R 选项的情况下，无法指定目标上的端口。

```js
scp 【本地要上传文件地址】  [用户名]@[ip地址]：远程地址

//例如我的本地要上传的文件地址是c://user/code/demo/dist,用户名是root，IP地址是192.168.9.25
scp -r c://user/code/demo/dist root@192.168.9.25:/home/root/demo/fe/
//如果我当前在c://user/code/demo/下(比如在vscode打开demo项目打开终端)，就可以执行以下命令直接上传
//-r代表上传的是文件夹以及文件夹里所有的东西
scp -r dist root@192.168.9.25:/home/root/demo/fe/
```

## ssh 命令

> 参考：
>
> ```shell
> man ssh
> ```

Linux 一般作为服务器使用，而服务器一般放在机房，你不可能在机房操作你的 Linux 服务器。

这时我们就需要远程登录到 Linux 服务器来管理维护系统。

Linux 系统中是通过 ssh 服务实现的远程登录功能，默认 ssh 服务端口号为 22。

SSH 为 Secure Shell 的缩写，由 IETF 的网络工作小组（Network Working Group）所制定。

SSH 为建立在应用层和传输层基础上的安全协议。

```shell
ssh [-46AaCfGgKkMNnqsTtVvXxYy] [-B bind_interface]
    [-b bind_address] [-c cipher_spec] [-D [bind_address:]port]
    [-E log_file] [-e escape_char] [-F configfile] [-I pkcs11]
    [-i identity_file] [-J [user@]host[:port]] [-L address]
    [-l login_name] [-m mac_spec] [-O ctl_cmd] [-o option] [-p port]
    [-Q query_option] [-R address] [-S ctl_path] [-W host:port]
    [-w local_tun[:remote_tun]] destination [command [argument ...]]
```

ssh connects and logs into the specified destination, which may be specified as either `[user@]hostname` or a URI of the form
`ssh://[user@]hostname[:port]`. The user must prove their identity to the remote machine using one of several methods (see below).

常用登录命令：

```shell
ssh -p 22 my@127.0.0.1
# 输入密码：
```

**-p** 后面是端口

**my** 是服务器用户名

**127.0.0.1** 是服务器 ip

回车输入密码即可登录

### ssh 免密登录

> [设置 SSH 通过秘钥登录](https://www.runoob.com/w3cnote/set-ssh-login-key.html)
>
> [ssh 免密登录配置方法及配置](https://blog.csdn.net/weixin_44966641/article/details/123955997) ----主要
>
> [VSCode——SSH 免密登录](https://blog.csdn.net/qq_45779334/article/details/129308235?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ECtr-2-129308235-blog-123031276.235%5Ev43%5Epc_blog_bottom_relevance_base3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ECtr-2-129308235-blog-123031276.235%5Ev43%5Epc_blog_bottom_relevance_base3&utm_relevant_index=4) ----主要
>
> [git/ssh 捋不清的几个问题](https://www.barretlee.com/blog/2014/03/11/cb-problems-in-git-when-ssh/)

1. 生成秘钥对

   在本地机器上生成公钥、私钥：（一路回车默认即可）

   ```shell
   # 自行查阅命令参数，-t 秘钥类型；-C 注释；-f 生成文件名；
   # 最好先进入 `~/.ssh` 目录，这样文件直接生成在这个目录下。
   ssh-keygen -t rsa -C "user@host" -f "path/id_rsa_user@host"
   ```

   可以在 `~/.ssh` 目录下看到两个秘钥文件，即我们刚生成的私钥 `id_rsa_user@host` 和公钥 `id_rsa_user@host.pub`（具体名称取决于你的命名）。

2. 上传公钥到服务器

   在本地机器上生成秘钥对之后，需要将公钥 `id_rsa_user@host.pub` 中的内容放到对应服务器上的 `~/.ssh/authorized_keys` 文件中，此步有 2 种方式：

   ```shell
   # 1.通过 ssh-copy-id 命令，命令有点类似 scp，需要输入密码
   ssh-copy-id -i /path/id_rsa_user@host.pub user@host

   # 2.手动将直接将公钥文件内容拷贝到服务器的 ~/.ssh/authorized_keys 文件中，没有文件则创建文件
   ```

   > NOTE ：
   >
   > ⚠️ 设置 ssh 路径下的权限（重要！）---- 本人未设置
   > 远程服务器～/.ssh/authorized_keys 文件设置好后，一定要修改路径下的权限，否则 ssh 密钥认证会失效！！
   >
   > 由于 authorized_keys 这个文件我们自己创建的，而 ssh 处于安全性考虑，对.ssh 目录下的文件权限内容有着严格的权限要求，如果权限设置不对，在配对秘钥的时候会无法打开 authorized_keys 文件从而导致秘钥配对失败。而 ssh 此时没有放弃连接，依然会尝试询问用户密码。最终产生的结果就是用户配置了公钥却仍然需要输入密码的问题。很多教程都没有说明这一点，导致我也是费了很大功夫才找到问题
   >
   > [vscode 在 remote SSH 免密远程登录](https://blog.csdn.net/weixin_42907822/article/details/125237307)

3. 配置 config 文件

   配置本地机器的 `~/.ssh/config` 文件，在对应 ip 下增加下面内容即可：

   ```shell
   Host 10.143.123.230
     HostName 10.143.123.230
     Port 22
     User c00619335
     IdentityFile ~/.ssh/id_rsa_c00619335@10.143.123.230
   ```

   > - ssh config 配置文件的基本格式
   >
   >   ```shell
   >   Host      # hostName的别名
   >     HostName  # 是目标主机的主机名，也就是平时我们使用ssh后面跟的地址名称。
   >     Port   # 指定的端口号。
   >     User   # 指定的登陆用户名。
   >     IdentifyFile # 指定的私钥地址。
   >   ```
   >
   > - 不要加 PreferredAuthentications publickey，否则连接远程服务器上 docker 时，会报错 **Connection refused**。
   >
   >   `<font color=red>`**被坑死了 -\_\_-!!!**`</font>`

   同时要确保服务器上允许使用公钥链接

   ```shell
   # /etc/ssh/sshd_config 文件中
   PubkeyAuthentication yes # 把#号去掉（默认在39行附近），这样公钥验证才生效。
   ```

   重启远程服务器的 ssh 服务

   ```shell
   service ssh start
   ```

4. 测试免密登录

### ssh 远程连接 docker

> [设置 SSH 远程连接 docker 容器](https://www.cnblogs.com/luochunxi/p/16699704.html)

```shell
# 1.创建容器，默认是root用户，需自定义<>中内容
# `host` 模式 `-p` 选项不需要，因为 `host` 模式下容器直接使用宿主机的网络栈，端口是共享的。
docker run -d \
    -it \
    --privileged \
    -h <hostname> \
    --restart always \
    --network host \
    --name <dockername> \
    -v /data/<path>:/data/<path> \
    IMAGE \
    /bin/bash

# `bridge` 模式可以使用 `-p` 选项指定端口
docker run -d \
    -it \
    --privileged \
    -h <hostname> \
    --restart always \
    --network bridge \
    -p <port_h:port_c> \
    --name <dockername> \
    -v /data/<path>:/data/<path> \
    IMAGE \
    /bin/bash

# 2.进入容器
docker exec -it <docker_name> bash

# 3.设置密码，修改容器的root密码
passwd
密码设置为：123456

# 4.安装 ssh
apt-get update
apt-get install openssh-server -y

# 5.查看 ssh 是否启动
ps -e | grep ssh # 有sshd,说明ssh服务已经启动。如果没有启动，输入`service ssh start`启动服务

# 6.修改配置，
# 打开配置文件`/etc/ssh/sshd_config`
PermitRootLogin yes  # 原文件为`PermitRootLogin without-password`，需要改成左边
Port 22  # 可能原文件为`#Port 22`，即默认放开 22 端口给 ssh 用。
Port xxx # 如果 docker run 用的是 host 模式，这里直接指定一个合法端口给 ssh 用就可以，如 10086，宿主机和 docker 都是用这个端口，注意不要冲突。如果 docker run 命令中为 bridge 模式（默认）且用 -p <host_port>:<container_port>的<container_port>为22，此处`Port 22`；若<container_port>为其他值如10086，则此处需要改成`Port 10086`。放开多个端口需同时添加多条`Port xxx`。

# 7.启动 ssh，重启用`service ssh restart`
service ssh start
# 开机自动启动ssh命令
sudo systemctl enable ssh

# 8.ssh远程登录上述创建的容器
# 注意这里要用 root 用户登录
ssh root@xx.xx.xx.xx -p <port>
```

> NOTE：
>
> 一定要检查 `~/.ssh/config` 文件，不要添加 PreferredAuthentications publickey，否则连接远程服务器上 docker 时，会报错 **Connection refused**。
>
> `<font color=red>`被坑死了 -\_\_-!!!`</font>`
>
> ```shell
> # 上面步骤修改配置文件`/etc/ssh/sshd_config`时，部分 wiki 说要放开下面配置，实测未放开也可以，未深究
> PasswordAuthentication yes
> ```

### ssh 启动报错

如果 ssh 启动报错：

```shell
Badly formatted port number
```

说明 `/etc/ssh/sshd_config` 中端口号有问题，改正默认值 22，然后重启 ssh 服务即可。如

```shell
# 打开文件 /etc/ssh/sshd_config，将 Port 改成22
Port 22

# 重启 ssh 服务
service ssh start
```

## ssh-keygen

> [ssh-keygen](http://linux.51yip.com/search/ssh-keygen)

ssh-keygen 用于为 ssh(1)生成、管理和转换认证密钥，包括 RSA 和 DSA 两种密钥。**密钥类型可以用 -t 选项指定**。如果没有指定则默认生成用于 SSH-2 的 RSA 密钥。

通常，这个程序产生一个密钥对，并要求**指定一个文件存放私钥**，同时将公钥存放在附加了".pub"后缀的同名文件中。

程序同时要求输入一个密语字符串(passphrase)，空表示没有密语(主机密钥的密语必须为空)。

密语和口令(password)非常相似，但是密语可以是一句话，里面有单词、标点符号、数字、空格或任何你想要的字符。好的密语要 30 个以上的字符，难以猜出，由大小写字母、数字、非字母混合组成。密语可以用 -p 选项修改。丢失的密语不可恢复。如果丢失或忘记了密语，用户必须产生新的密钥，然后把相应的公钥分发到其他机器上去。

RSA1 的密钥文件中有一个**"注释"字段**，可以方便用户标识这个密钥，指出密钥的用途或其他有用的信息。创建密钥的时候，注释域初始化为"user@host"，以后可以用 -c 选项修改。

```shell
 -C comment 提供一个新注释
 -f filename 指定密钥文件名。(要输入完整路劲，否则在当前路径下生成)
-P passphrase 提供(旧)密语。
-t type  指定要创建的密钥类型。可以使用："rsa1"(SSH-1) "rsa"(SSH-2) "dsa"(SSH-2)

ssh-keygen -t rsa -C "user@host" -f "id_rsa_user@host"
```
