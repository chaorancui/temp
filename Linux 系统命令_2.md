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

## ln 命令

`ln`（link） 是 Unix / Linux 系统中用于**创建链接**的核心命令，主要用途是让**多个路径指向同一个文件或目录**。在工程、构建系统、软件部署中非常常见。

**一、基本语法**

```bash
ln [选项] TARGET [LINK_NAME]
ln [选项] TARGET... DIRECTORY
```

`ln` 可以创建两种链接：

1. **硬链接（hard link）** —— 默认
2. **符号链接（symbolic link / soft link）** —— 最常用

从效果上看，链接就像“另一个名字”或“一个指向目标的快捷方式”。

**二、硬链接**

```bash
ln target_file link_name
```

特点：

- **与原文件共享 inode**
- 删除原文件 **不影响** 链接
- **不能链接目录**
- **不能跨文件系统**

```bash
ln a.txt b.txt
# 用 `ls -li a.txt b.txt` 查看，会发现 inode 相同
```

适用场景:

- 节省磁盘空间
- 需要多个等价文件名
- 系统内部文件（如 `/bin`、`/usr/bin`）

⚠️ 工程中 **不推荐大量使用**，可读性和可维护性差。

**三、符号链接**

```bash
ln -s TARGET LINK_NAME
ln -s /usr/local/bin/python3 python
```

特点：

- 本质是一个**保存路径的特殊文件**
- **可以链接目录**
- **可以跨文件系统**
- 原目标删除后 → 链接失效（dangling symlink）

```bash
ls -l python
# lrwxrwxrwx 1 user user 20 python -> /usr/local/bin/python3
```

工程中的典型用途：

| 场景     | 示例                     |
| -------- | ------------------------ |
| 版本切换 | `current -> app_v2.1`    |
| 构建产物 | `build -> build_release` |
| 命令别名 | `python -> python3.10`   |
| 部署     | `www -> /data/web_root`  |

**四、常用选项（非常重要）**

- `-s`：创建符号链接

  ```bash
  ln -s target link
  ```

- `-f`：强制覆盖（force）

  ```bash
  ln -sf new_target link
  ```

  > **部署脚本中常用**

- `-n`：不跟随已存在的符号链接

  ```bash
  ln -sfn new_target link
  ```

  > 防止把链接指向的目录当作真实目录

- **部署 / CI 脚本强烈推荐组合：**

  ```bash
  ln -sfn release_v2 current
  ```

- `-v`：显示详细过程

  ```bash
  ln -sv target link
  ```

**五、ln 的几个“坑点”（工程实践很重要）**

1. 顺序写反（新手常犯）

   ```bash
   ln -s link target   # ❌ 错
   ln -s target link   # ✅ 对
   ```

   记忆口诀：**“目标在前，名字在后”**

2. 相对路径 vs 绝对路径

   ```bash
   ln -s ../bin/tool tool
   ```

   - 相对路径是**相对于链接所在目录**
   - 移动链接后可能失效

   📌 **部署场景推荐绝对路径**

3. 覆盖目录时不加 `-n`

   ```bash
   ln -sf new current   # ❌ 可能进入 current 目录
   ln -sfn new current  # ✅ 安全
   ```

**总结**

- 硬链接是“同一个文件的多个名字”，
- 符号链接是“指向路径的快捷方式”。
- 99% 情况使用：`ln -sfn`

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

# 脚本所在目录
SCRIPT_PATH=$(realpath "$(dirname "$0")")  # 可解析符号链接
SCRIPT_PATH=$(cd "$(dirname "$0")" && pwd) # 跨平台兼容性好
echo "SCRIPT_PATH: $SCRIPT_PATH"

# 运行脚本的工作目录
RUN_PATH=$(realpath "$(pwd)")
echo "RUN_PATH: $RUN_PATH"
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
   SCRIPT_PATH=$(cd "$(dirname "$0")" && pwd)    # 兼容性好
   SCRIPT_PATH=$(realpath "$(dirname "$0")")     # 可解析符号链接
   echo "$SCRIPT_PATH"
   ```

   解释：
   - `$0`：脚本路径（可能是相对路径）
   - `dirname "$0"`：取出脚本所在目录
   - `cd ... && pwd`：转为绝对路径

   > 用处：在脚本中访问相对路径的配置文件、依赖等。

2. 获取上级目录

   ```bash
   # 获取上2级目录
   PARENT_PATH=$(dirname "$(dirname "$path")")      # 连续两次 `dirname` 即可

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

   SCRIPT_PATH=$(realpath "$(dirname "$0")")
   ROOT_PATH=$(get_dir_up "$SCRIPT_PATH" 3)
   echo "当前脚本: $SCRIPT_PATH"
   echo "项目根目录: $ROOT_PATH"
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

## gzip 命令

gzip 是 GNU 项目开发的一套文件压缩/解压工具，**采用 LZ77 算法与 Huffman 编码**，压缩后的文件后缀通常为 `.gz`。它在 Linux/Unix 系统中非常常见，主要用于减少文件体积、节省存储空间并加速网络传输。

基本用法

### `gzip` 压缩

```bash
gzip 文件名
```

- 执行后原文件会被替换为压缩文件，例如 `file.txt` 变为 `file.txt.gz`，原文件消失（除非使用 `-k` 保留）。

### `gzip -d/gunzip` 解压

有两种等价方式：

```bash
gunzip 文件名.gz
# 或
gzip -d 文件名.gz
```

- 解压后 `.gz` 文件被移除，恢复为原文件（除非使用 `-k` 保留）。

**常用参数详解**

| 参数         | 作用                                                                    | 示例                                               |
| :----------- | :---------------------------------------------------------------------- | :------------------------------------------------- |
| `-d`         | 解压缩（decompress）                                                    | `gzip -d file.gz`                                  |
| `-c`         | 将结果输出到标准输出（stdout），保留原文件                              | `gzip -c file.txt > file.txt.gz`                   |
| `-k`         | 压缩或解压后保留原始文件（keep）                                        | `gzip -k file.txt`（保留 file.txt 和 file.txt.gz） |
| `-l`         | 列出压缩文件的信息：压缩前后大小、压缩比、文件名                        | `gzip -l file.gz`                                  |
| `-r`         | 递归处理目录（会将目录下每个文件单独压缩成 `.gz`）                      | `gzip -r logs/`                                    |
| `-v`         | 显示详细的处理信息（verbose）                                           | `gzip -v file.txt`                                 |
| `-1` 到 `-9` | 指定压缩级别，`-1` 最快但压缩比最低，`-9` 最慢但压缩比最高。默认为 `-6` | `gzip -9 largefile.tar`                            |
| `-f`         | 强制压缩或解压，覆盖已有文件（force）                                   | `gzip -f file.txt`                                 |
| `-t`         | 测试压缩文件的完整性                                                    | `gzip -t file.gz`                                  |

参数组合示例：

- 压缩并保留原文件：`gzip -k file.txt`
- 查看压缩文件信息：`gzip -l file.gz`
- 以最高压缩比压缩：`gzip -9 file.txt`
- 递归压缩目录并显示详情：`gzip -rv /path/to/dir`

**使用场景**

1. 压缩日志文件

   服务器日志常随时间增长，对旧日志进行压缩可大幅节省磁盘空间：

   ```bash
   gzip access.log.2025-01-01
   ```

   配合 `-k` 保留原文件（如需要继续写入）：

   ```bash
   gzip -k access.log   # 生成 access.log.gz，原文件保留
   ```

2. 网络传输大文件

   压缩后文件体积减小，上传/下载更快。可与 `scp`、`rsync` 等结合使用。

3. 打包并压缩目录（与 tar 组合）

   `gzip` 本身不能压缩目录，但常与 `tar` 联用创建 `.tar.gz` 包：

   ```bash
   tar -czvf archive.tar.gz /path/to/dir   # -z 表示通过 gzip 压缩
   ```

   解压 `.tar.gz`：

   ```bash
   tar -xzvf archive.tar.gz
   ```

4. 管道操作

   利用 `-c` 将压缩数据传递给其他程序，例如备份数据库并直接压缩：

   ```bash
   mysqldump database | gzip -c > backup.sql.gz
   ```

5. 检查压缩文件完整性

   下载后验证 `.gz` 文件是否损坏：

   ```bash
   gzip -t file.gz && echo "OK" || echo "Broken"
   ```

6. 查看压缩文件内容（不解压）

   ```bash
   zcat 文件名.gz      # 输出到终端
   # 或
   gzip -dc 文件名.gz  # -d 解压，-c 输出到标准输出
   ```

**注意事项：**

- **gzip 只能压缩单个文件**，不能直接压缩目录。若需压缩整个目录，应先使用 `tar` 打包再压缩。
- 压缩后原文件默认会被删除，若需保留请使用 `-k`。
- 压缩级别越高速度越慢，应根据实际需求权衡（日常使用 `-6` 即可）。
- 对于已经压缩过的文件（如 .jpg, .mp4），再次压缩效果甚微，甚至可能增大体积。
- 解压时若目标文件已存在，默认会询问是否覆盖，可用 `-f` 强制覆盖。

## tar 命令

`tar` 是 Linux 中常用的打包和压缩工具，可以将多个文件或目录打包成一个归档文件，也可以用于解压这些归档文件。

`tar` 是 Linux/Unix 系统中用于**打包（归档）文件和目录**的命令，全称是 **tape archive**。它常用于备份文件、软件发布包的生成等场景。`tar` 不压缩文件，但可与 gzip、bzip2、xz 等工具结合实现压缩打包。

**常用参数详解**

以下是 `tar` 的常用参数（区分长短参数形式）：

| 参数                           | 含义                                                                     |
| ------------------------------ | ------------------------------------------------------------------------ |
| `-c` 或 `--create`             | 创建新归档文件（archive）                                                |
| `-x` 或 `--extract`            | 解包归档文件                                                             |
| `-t` 或 `--list`               | 查看归档文件内容                                                         |
| `-f <file>` 或 `--file=<file>` | 指定归档文件名（必须紧跟 `-f`）                                          |
| `-v` 或 `--verbose`            | 显示处理过程中的文件名（verbose 模式）                                   |
| `-z` 或 `--gzip`               | 使用 gzip 压缩或解压（`.tar.gz` 或 `.tgz`）                              |
| `-j` 或 `--bzip2`              | 使用 bzip2 压缩（`.tar.bz2`）                                            |
| `-J` 或 `--xz`                 | 使用 xz 压缩（`.tar.xz`）                                                |
| `--lzma`                       | 使用 lzma 压缩（`.tar.lzma`）                                            |
| `-C <dir>`                     | 切换目录再操作（常用于压缩/解压时指定目标目录）                          |
| `--exclude=<pattern>`          | 排除匹配的文件/目录                                                      |
| `--include=<pattern>`          | 包含匹配的文件/目录，仅包含要配合 `--exclude="*"` 使用                   |
| `--wildcards '*/*.txt'`        | 启用 shell 风格的通配符匹配，匹配的是**完整路径**(default for exclusion) |

> :pushpin: **注：**
>
> - `--exclude` 默认就是通配符语义。
> - `--include` 默认是“字面路径匹配”，必须配合 `--wildcards` 才能按通配符匹配。
>   如 `tar -xvf a.tar '*.log'` 未加 --wildcards 时，tar 会尝试匹配一个名字就叫 `*.log` 的文件，通常结果是：解不出任何文件。
> - `--wildcards` **匹配的是完整路径**，因此如果报错找不到就要看下里面的文件结构 `tar -ztf xx.tar.gz`，然后换成 `--wildcards '*/*.txt'` 通配。

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

3. 切换目录后，打包目录下的所有内容

   ```bash
   tar -czf archive.tar.gz -C /data/dump .
   ```

   - 打包目录下的所有内容
   - 不包含绝对路径
   - 不受文件数量限制

   **缺点**：<font color=blue>空文件夹或文件夹不存在，也会创建空压缩包</font>
   **解决**：

   ```bash
   # 目录不存在或空目录不压缩：
   SRC_DIR=/data/folder1
   OUT_TAR=/data/local/tmp/archive.tar.gz

   if [ -d "$SRC_DIR" ] && [ "$(ls -A "$SRC_DIR" 2>/dev/null)" ]; then
       tar czf "$OUT_TAR" -C "$SRC_DIR" .
   else
       echo "skip: $SRC_DIR not exist or empty"
   fi

   # 如果你对 嵌入式 / busybox / 奇葩环境 特别敏感，如下方法不依赖 ls 行为，不怕 alias
   if [ -d "$SRC_DIR" ] && find "$SRC_DIR" -mindepth 1 -print -quit | grep -q .; then
      tar czf "$OUT_TAR" -C "$SRC_DIR" .
   fi

   # 单行
   adb shell '[ -d /data/vendor ] && ls -A /data/vendor >/dev/null 2>&1 && tar czf /data/local/tmp/kernel_dump.tar.gz -C /data/vendor . || echo skip'
   ```

   还可以封装成函数：

   ```bash
   tar_if_not_empty() {
       local src="$1"
       local out="$2"

       if [ -d "$src" ] && [ "$(ls -A "$src" 2>/dev/null)" ]; then
           tar czf "$out" -C "$src" .
           return 0
       fi

       echo "skip: $src not exist or empty"
       return 1
   }
   ```

4. 创建归档时**排除**某些文件或目录

   ```bash
   tar --exclude='*.log' -czvf archive.tar.gz dir/
   ```

5. 创建归档时**仅包含**某些文件或目录

   ```bash
   tar -cvf code.tar \
     --wildcards \
     --include="*/" \
     --include="*.c" \
     --include="*.h" \
     --exclude="*" \
     your_directory/
   ```

   - tar 在递归目录时，**目录本身也要通过过滤**。`*.c` / `*.h` 不匹配目录名，目录会先被 `--exclude="*"` 排除，导致 tar 根本不会进入**子目录**去寻找 `.c` / `.h` 文件。
   - `--include="*/"` 放在最前面，让所有目录通过，tar 才能递归进去找目标文件。
   - `--include` 和 `--exclude` 的顺序敏感的。即：

     tar 的过滤规则是**按顺序逐条匹配**的，对每个文件，tar 从上到下扫描规则，**第一条匹配的规则生效，后续规则忽略**。所以顺序不同，结果可能完全不同：

     ```bash
     # 先排除所有，再包含 .c —— .c 文件已经被第一条排除了，include 不会"撤销"它
     --exclude="*" --include="*.c"   # ❌ 结果：什么都不打包

     # 先包含 .c，再排除所有 —— .c 先匹配到 include，后面的 exclude 不再作用于它
     --include="*.c" --exclude="*"   # ✅ 结果：只打包 .c 文件
     ```

6. 追加文件到已存在的 `.tar` 文件中（仅限未压缩的 tar）

   ```bash
   tar -rvf archive.tar newfile.txt
   ```

7. 查看归档文件内容

   ```bash
   tar -tvf archive.tar.gz
   ```

   > 不解压，仅显示文件列表。

### `tar -x` 解压

**常见用法示例**

1. 解包归档文件（不解压）

   ```bash
   tar -xvf archive.tar
   # 按pattern解包文件，如解包所有子目录下的 .bin 文件
   tar -xvf archive.tar --wildcards '**/*.bin'
   ```

   - pattern 是 **tar 内部看到的路径**，通常包含相对路径。
   - pattern 必须用**单引号**，避免被 shell 提前展开。

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

## zip 命令

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

## rar 命令

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
