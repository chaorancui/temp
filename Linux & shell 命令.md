[toc]

# bash 命令

## shell 配置文件介绍

> [详解/etc/profile、/etc/bash.bahsrc、\~/.profile、\~/.bashrc 的用途](https://blog.csdn.net/jirryzhang/article/details/70833544?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-12-70833544-blog-138886149.235^v43^pc_blog_bottom_relevance_base3&spm=1001.2101.3001.4242.7&utm_relevant_index=15)
>
> [ubuntu 中环境变量文件/etc/profile、.profile、.bashrc、/etc/bash.bashrc 之间的区别和联系](https://blog.csdn.net/qq_51246603/article/details/127459786?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-5-127459786-blog-119089926.235^v43^pc_blog_bottom_relevance_base3&spm=1001.2101.3001.4242.4&utm_relevant_index=8)

Linux 是一个多用户的操作系统。每个用户登录系统后，都会有一个专用的运行环境。通常每个用户默认的环境都是相同的，这个默认环境实际上就是一组环境变量的定义。用户可以对自己的运行环境进行定制，其方法就是修改相应的系统环境变量。

### 配置文件

Linux 安装时可能要修改的配置文件：

```shell
/etc/profile
/etc/bashrc   # ubuntu没有这个文件，对应地，其有/etc/bash.bashrc文件
~/.bash_profile  # 一般有.bash_profile、.bash_login、.profile中一个或多个
~/.bash_login
~/.profile
~/.bashrc
```

> [Shell-环境变量的配置文件介绍](https://www.cnblogs.com/ygbh/p/17427943.html)

- 系统级别

  针对所有的用户的所有的 shell / 各别 shell，登录时读取

  ```shell
  /etc/profile    # 操作系统级别，登录 shell 时执行，并从 /etc/profile.d 目录的配置文件中搜集 shell 的设置
  /etc/profile.d/*.sh  # 系统软件级别
  /etc/bashrc    # 登录 bash shell 时读取
  /etc/bash.bashrc  # 登录 bash shell 时读取
  ```

- 个人级别

  某个用户的所有 shell，登录时读取，一般默认读取 ~/.bashrc

  ```shell
  # 个人级别： (优先级从上到下，一般只会读取优先级高的一个，不会覆盖)
  ~/.bash_profile
  ~/.bash_login
  ~/.profile
  ```

- bash 级别

  某个用户的 bash，登录及打开新 shell 时都会读取

  ```shell
  ~/.bashrc
  ```

### 文件执行顺序

![](https://img2023.cnblogs.com/blog/918540/202305/918540-20230524122028472-1978276734.png)

当登入系统时候获得一个 shell 进程时，其读取环境设定档有三步：

1. 首先读入的是全局环境变量设定档/etc/profile，然后根据其内容读取额外的设定的文档，如
   /etc/profile.d 和 /etc/inputrc。
2. 然后根据不同使用者帐号，去其家目录读取/.bash_profile，如果这读取不了就读取/.bash_login，这个也读取不了才会读取
   ~/.profile，这三个文档设定基本上是一样的，读取有优先关系。
3. 然后先读取/etc/bashrc 或/etc/bash.bashrc，再根据用户帐号读取~/.bashrc。

### Q & A

- **Q：**/etc/profile 与/etc/bashrc 的区别？

  **A：**/etc/profile，/etc/bashrc 都是系统全局环境变量设定。

  - 前一个主要用来设置一些系统变量，比如 JAVA_HOME 等等。
  - 后面一个主要用来保存一些 bash 的设置。

- **Q：**/.profile 与/.bashrc 的区别？

  **A：**都具有个性化定制功能。

  - ~/.profile 可以设定本用户专有的路径，环境变量，等，它只能登入的时候执行一次。
  - ~/.bashrc 也是某用户专有设定文档，可以设定路径，命令别名，每次 shell script 的执行都会使用它一次。

## shell 类型 - 交互式、登录式

> [Linux-命令-交互式*非交互式*登录式\_非登录式.md](https://wetts.github.io/2020/03/14/%E7%B3%BB%E7%BB%9F%E3%80%81%E6%9C%8D%E5%8A%A1%E5%99%A8/%E7%B3%BB%E7%BB%9F/Linux/Linux-%E5%91%BD%E4%BB%A4-%E4%BA%A4%E4%BA%92%E5%BC%8F_%E9%9D%9E%E4%BA%A4%E4%BA%92%E5%BC%8F_%E7%99%BB%E5%BD%95%E5%BC%8F_%E9%9D%9E%E7%99%BB%E5%BD%95%E5%BC%8F/)

Linux shell 是用户与 Linux 系统进行交互的媒介，而 bash 作为目前 Linux 系统中最常用的 shell，它在运行时具有两种属性，即“交互”与“登陆”。

- 按照 bash 是否与用户进行交互，可以将其分为“交互式”与“非交互式”；
- 而按照 bash 是否被用户登陆，又可将其分为“登陆 shell”与“非登陆 shell”。

| 执行方式               | profile | bashrc |                               示例                               |
| :--------------------- | :-----: | :----: | :--------------------------------------------------------------: |
| 非交互式且非登录 shell | 不加载  | 不加载 |                   `crontab`中执行的 bash 脚本                    |
| 非交互式登录 shell     |  加载   |  加载  |                `crontab`中通过 `su -l`执行的脚本                 |
| 交互式非登录 shell     | 不加载  |  加载  |               如命令行中通过 `su 用户名`执行的命令               |
| 交互式登录 shell       |  加载   |  加载  | 普通的终端登录, ssh 远程登录, 以及使用 `su - l 用户名`切换身份等 |

### “交互式”与“非交互式”

**含义说明**：

- 交互式，是 shell 的一种运行模式，交互式 shell **等待你输入命令**，并且立即执行，然后将结果反馈给你。这是每个 CLI 用户都非常熟悉的流程：登录、执行一些命令、登出。当你登出后，这个 shell 就终止了。
- 非交互式，是 shell 的另一种运行模式，它专门被用来执行预先设定的命令。在这种模式下，shell 不与用户进行交互，而是**读取存放在脚本文件中的命令**并执行它们。当它读到文件的结尾，这个 shell 就终止了。

**启动方法**：

根据 bash 手册上的描述：

> An interactive shell is one started without non-option arguments and without the -c option whose standard input and error are both connected to terminals (as determined by isatty(3)), or one started with the -i option.

从上面的描述看，只要执行 bash 命令的时候，**不带有“选项以外的参数”**或者**不带 -c** 选项，就会启动一个交互式 shell。要理解这句话，就要弄懂“选项以外的参数”是什么意思，其实它指的就是 **shell 的脚本文件**；而 -c 选项将指定**字符串作为命令读入 bash**，也就相当于执行指定的命令，它和前者有些类似，只是不从脚本文件中读取罢了。请看例子：

```shell
[chen@localhost Temp]$ echo "uname -r; date" > script.sh
[chen@localhost Temp]$ bash ./script.sh
3.10.0-514.el7.x86_64
Tue Apr 18 14:43:50 CST 2017
[chen@localhost Temp]$
[chen@localhost Temp]$ bash -c "uname -r; date"
3.10.0-514.el7.x86_64
Tue Apr 18 14:44:49 CST 2017
[chen@localhost Temp]$
```

通常来说，用于执行脚本的 shell 都是“非交互式”的，但我们也有办法把它启动为“交互式” shell，方法就是在执行 bash 命令时，添加 -i 选项：

```shell
[chen@localhost Temp]$ bash -c "echo \$-"
hBc
[chen@localhost Temp]$ bash -i -c "echo \$-"
himBHc
```

我们看到，添加了 -i 选项的 bash -c 命令为我们启动了一个“交互式” shell。

**判别方法**：

根据 bash 手册上的描述：

> PS1 is set and $- includes i if bash is interactive, allowing a shell script or a startup file to test this state.

用于在 shell 脚本和 startup 文件中判断当前 shell“交互”属性的方法，就是判断变量 PS1 是否有值，或者判断变量 $- 是否包含 i，请看例子：

```shell
[chen@localhost Temp]$ cat ./test1.sh
echo "\$0   : $0"
echo "\$-   : $-"
echo "\$PS1 : $PS1"
[chen@localhost Temp]$ bash ./test1.sh     # 非交互式shell
$0   : ./test1.sh
$-   : hB
$PS1 :
[chen@localhost Temp]$ bash -i ./test1.sh  # 交互式shell
$0   : ./test1.sh
$-   : himB
$PS1 : [\u@\h \W]\$
[chen@localhost Temp]$
```

### “登陆式”与“非登陆式”

**含义说明**：

“登陆 shell”通常指的是：

1. 用户通过输入用户名/密码（或证书认证）后启动的 shell；
2. 通过带有 `-l|--login` 参数的 bash 命令启动的 shell。

例如，系统启动、远程登录、使用 `su -` 切换用户、通过 `bash --login` 命令启动 bash 等。

而其他情况启动的 shell 基本上就都是“非登陆 shell”了。

例如，从图形界面启动终端、使用 `su` 切换用户、通过 `bash` 命令启动 bash 等。

**判别方法**：

根据 bash 手册上的描述：

> A login shell is one whose first character of argument zero is a `-`, or one started with the `--login` option.

我们可以通过在 shell 中 `echo $0` 查看，显示 `-bash` 的一定是“登陆 shell”，反之显示 bash 的则不好说。

```shell
[chen@localhost ~]$ bash --login
[chen@localhost ~]$ echo $0
bash
[chen@localhost ~]$
```

可以看出，使用 `bash --login` 启动的“登陆 shell”，其 `$0` 也并非以 `-` 开头，这也就是为什么手册上的描述里使用“or”的原因。

另外，当我们执行 exit 命令退出 shell 时，也可以观察到它们的不同之处：

```shell
[chen@localhost ~]$ bash --login
[chen@localhost ~]$ exit   # 退出登陆shell
logout
[chen@localhost ~]$ bash
[chen@localhost ~]$ exit   # 退出非登陆shell
exit
[chen@localhost ~]$
```

原则上讲，我们使用 logout 退出“登陆 shell”，使用 exit 退出“非登录 shell”。但其实 exit 命令会判断当前 shell 的“登陆”属性，并分别调用 logout 或 exit 指令，因此使用起来相对方便（即执行 exit 命令，退出的 shell 可以是登录或者非登录 shell；执行 logout 命令，则只能退出登录 shell，不能退出非登录 shell）。

**主要区别**：

对于用户而言，“登录 shell”和“非登陆 shell”的主要区别在于启动 shell 时所执行的 startup 文件不同。

简单来说，“登录 shell”执行的 startup 文件为 `~/.bash_profile`，而“非登陆 shell”执行的 startup 文件为 `~/.bashrc`。

登录 shell（包括交互式登录 shell 和使用“–login”选项的非交互 shell），它会首先读取和执行 `/etc/profile`全局配置文件中的命令，然后依次查找 `~/.bash_profile`、`~/.bash_login` 和 `~/.profile` 这三个配置文件，读取和执行这三个中的第一个存在且可读的文件中命令。除非被“–noprofile”选项禁止了。

在非登录 shell 里，只读取 `~/.bashrc` （和 `/etc/bash.bashrc`、`/etc/bashrc` ）文件，不同的发行版里面可能有所不同，如 RHEL6.3 中非登录 shell 仅执行了“~/.bashrc”文件（没有执行/etc/bashrc），而 KUbuntu10.04 中却依次执行了/etc/bash.bashrc 和 ~/.bashrc 文件。

## 无法自动加载 .bashrc

今天遇到一个问题，linux 下某用户登陆后无法加在其自身的 `.bashrc`，通过 `source .bashrc` 发现 `.bashrc` 是没有问题的，文件的权限也是没有问题的。

后来发现是因为该用户下的 `.bash_profile` 被删除（`~/.bash_profile`，`~/.bash_login`，`~/.profile` 按优先级执行高的一个）。

其实加在顺序不是首先加载 `.bashrc`，而是先加载 `.bash_profile` （优先级 3 选 1）。

将 `.bash_profile` （3 选 1）文件补一下就好了，可以找个存在这个文件的系统，下面是 ubuntu22.04 中的 `.profile`，可作为参考：

```shell
# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
 . "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
```

## 切换到 root 用户

### 四种方式

1. `sudo -i`

   ```bash
   sudo -i
   ```

   特点：

   - 模拟 root 用户正常登录
   - 需要输入当前用户的密码
   - 会加载 root 的环境变量
   - 切换到 root 的 home 目录(/root)
   - 使用 root 的配置文件

2. `sudo -s`

   ```bash
   sudo -s
   ```

   特点：

   - 保留当前用户的环境变量
   - 需要输入当前用户的密码
   - 不会切换目录
   - 继承当前用户的环境设置

3. `sudo su`

   ```bash
   sudo su
   ```

   > 效果与 `sudo -s` 一样。

   特点：

   - 保留原用户的环境变量
   - 需要输入当前用户的密码
   - 切换后提示符为 #
   - 继承当前用户的环境设置

4. `su`

   ```bash
   su
   ```

   特点：

   - 需要输入 root 密码（默认 Ubuntu root 账户是锁定的）
   - 不加载环境变量
   - 不推荐使用，因为需要启用 root 账户

### 主要区别

**环境变量**：

- sudo -i：使用 root 的环境变量
- sudo su/sudo -s：保留当前用户的环境变量

**工作目录**：

- sudo -i：切换到/root
- sudo -s/sudo su：保持在当前目录

**安全性**：

- sudo 命令更安全，可以通过/etc/sudoers 控制权限
- 直接使用 su 需要启用 root 账户，安全性较低

**日志记录**：

- sudo 命令会记录日志
- su 命令不会记录日志

### 建议

- 推荐使用 sudo -i，这是最标准的 root 切换方式
- 日常使用建议用 sudo 执行单个命令，而不是切换到 root
- 不建议启用 root 账户，保持默认禁用状态

## shell 脚本执行方式

> [Shell 的多种执行方式](https://blog.csdn.net/swadian2008/article/details/122310011)
>
> [理解$0 和 BASH_SOURCE](https://www.junmajinlong.com/shell/bash_source/)

Shell 本身是一个用 C 语言编写的程序，它是用户使用 Unix/Linux 的桥梁，用户的大部分工作都是通过 Shell 完成的。**Shell 既是一种命令语言，又是一种程序设计语言**。作为命令语言，它交互式地解释和执行用户输入的命令；作为程序设计语言，它定义了各种变量和参数，并提供了许多在高级语言中才具有的控制结构，包括循环和分支。

**Shell 有两种执行命令的方式：**

- 交互式（Interactive）：解释执行用户的命令，用户输入一条命令，Shell 就解释执行一条。
- 批处理（Batch）：用户事先写一个 Shell 脚本(Script)，其中有很多条命令，让 Shell 一次把这些命令执行完，而不必一条一条地敲命令。

Shell 脚本和编程语言很相似，也有变量和流程控制语句，但 Shell 脚本是解释执行的，不需要编译，Shell 程序从脚本中一行一行读取并执行这些命令，相当于一个用户把脚本中的命令一行一行敲到 Shell 提示符下执行。

**运行 Shell 脚本有两种方法：**

一种在新进程中运行，一种是在当前 Shell 进程中运行。

### 一、在新进程中运行 Shell 脚本(bash)

在新进程中运行 Shell 脚本有多种方法。

#### 将 Shell 脚本作为程序运行

Shell 脚本也是一种解释执行的程序，可以在终端直接调用（需要使用 chmod 命令给 Shell 脚本**加上执行权限**），如下所示：

```shell
# 给脚本增加执行权限
chmod +x test.sh

# 执行脚本
./test.sh
```

> Note：
>
> - `./`表示当前目录，整条命令的意思是执行当前目录下的 test.sh 脚本。如果不写 `./`，Linux 会到系统路径（由 PATH 环境变量指定）下查找 test.sh，而系统路径下显然不存在这个脚本，所以会执行失败。
> - 通过这种方式运行脚本，脚本文件第一行的 `#!/bin/bash`一定要写对，好让系统查找到正确的[解释器](https://so.csdn.net/so/search?q=解释器&spm=1001.2101.3001.7020)。

#### 将 Shell 脚本作为参数传递给 Bash 解释器

你也可以直接运行 Bash 解释器，将脚本文件的名字作为参数传递给 Bash，如下所示：

```shell
/bin/bash test.sh
# 或
bash test.sh # 写法更简洁
```

> Note:
>
> - 通过这种方式运行脚本，不需要在脚本文件的第一行指定解释器信息，写了也没用。
> - /bin/bash 和 bash 写法本质是一样的，第一种写法给出了绝对路径，会直接运行 Bash 解释器；第二种写法通过 bash 命令找到 Bash 解释器所在的目录，然后再运行，只不过多了一个查找的过程而已。

**检测是否开启了新进程**：

Linux 中的每一个进程都有一个唯一的 ID，称为 PID，使用**`$$`**变量就可以获取当前进程的 PID。

首先编写如下的脚本文件，并命名为 check.sh：

```bash
#!/bin/bash
echo $$
```

然后使用以上两种方式来运行 check.sh：

```crystal
[root123@localhost addon]$ ./check.sh
27579  # 新进程
[root123@localhost addon]$ bash check.sh
27623  # 新进程
[root123@localhost addon]$ echo $$
23797  # 当前进程
```

你看，进程的 PID 都不一样，当然就是不同进程了。

### 二、在当前进程中运行 Shell 脚本(source)

这里需要引入一个新的命令——source 命令。source 是 [Shell 内置命令](http://c.biancheng.net/view/1136.html)的一种，它会读取脚本文件中的代码，并依次执行所有语句。你也可以理解为，source 命令会强制执行脚本文件中的全部命令，而忽略脚本文件的权限。

source 命令的用法为：

```bash
source filename
# 也可以简写为：
. filename  # 两种写法的效果相同。注意点号`.`和文件名中间有一个空格。
```

使用 source 命令不用给脚本增加执行权限，并且写不写 `./`都行，是不是很方便呢？

**检测是否在当前 Shell 进程中**：

我们仍然借助**`$$`**变量来输出进程的 PID，如下所示：

```crystal
[root123@localhost addon]$ echo $$
23797
[root123@localhost addon]$ . check.sh
23797
```

你看，进程的 PID 都是一样的，当然是同一个进程了。

### 理解$0 和 BASH_SOURCE

如上所述，一个 shell(bash)脚本有两种执行方式：

- 直接执行，新起进程执行，类似于执行二进制程序
- source 执行，当前进程从文件读取和执行命令，类似于加载库文件

`$0`保存了被执行脚本的程序名称。注意，它保存的是以二进制方式执行的脚本名而非以 source 方式加载的脚本名称。

例如，执行 a.sh 时，a.sh 中的 `$0`的值是 a.sh，如果 a.sh 执行 b.sh，b.sh 中的 `$0`的值是 b.sh，如果 a.sh 中 source b.sh，则 b.sh 中的 `$0`的值为 a.sh。

除了 `$0`，bash 还提供了一个数组变量 `BASH_SOURCE`，该数组保存了 bash 的 SOURCE 调用层次。这个层次是怎么体现的，参考下面的示例。

执行 shell 脚本 a.sh 时，shell 脚本的程序名 `a.sh`将被添加到 `BASH_SOURCE`数组的第一个元素中，即 `${BASH_SOURCE[0]}`的值为 `a.sh`，这时 `${BASH_SOURCE[0]}`等价于 `$0`。

当在 a.sh 中执行 b.sh 时：

```shell
# a.sh中的$0和BASH_SOURCE
$0 --> "a.sh"
${BASH_SOURCE[0]} -> "a.sh"

# b.sh中的$0和BASH_SOURCE
$0 --> "b.sh"
${BASH_SOURCE[0]} -> "b.sh"
```

当在 a.sh 中 source b.sh 时：

```shell
# a.sh中的$0和BASH_SOURCE
$0 --> "a.sh"
${BASH_SOURCE[0]} -> "a.sh"

# b.sh中的$0和BASH_SOURCE
$0 --> "a.sh"
${BASH_SOURCE[0]} -> "b.sh"
${BASH_SOURCE[1]} -> "a.sh"
```

当在 a.sh 中 source b.sh 时，如果 b.sh 中还执行了 source c.sh，那么：

```shell
# a.sh中的$0和BASH_SOURCE
$0 --> "a.sh"
${BASH_SOURCE[0]} -> "a.sh"

# b.sh中的$0和BASH_SOURCE
$0 --> "a.sh"
${BASH_SOURCE[0]} -> "b.sh"
${BASH_SOURCE[1]} -> "a.sh"

# c.sh中的$0和BASH_SOURCE
$0 --> "a.sh"
${BASH_SOURCE[0]} -> "c.sh"
${BASH_SOURCE[1]} -> "b.sh"
${BASH_SOURCE[2]} -> "a.sh"
```

使用脚本来验证一下 `BASH_SOURCE`和 `$0`。在 x.sh 中 source y.sh，在 y.sh 中 source z.sh：

```shell
# x.sh
source y.sh
echo "x.sh: ${BASH_SOURCE[@]}"

# y.sh
source z.sh
echo "y.sh: ${BASH_SOURCE[@]}"

# z.sh
echo "z.sh: ${BASH_SOURCE[@]}"
```

执行 x.sh 输出结果：

```shell
$ bash x.sh
z.sh: z.sh y.sh x.sh
y.sh: y.sh x.sh
x.sh: x.sh
```

## 取消 tab 补全报警声

- Linux 发行版 Terminal

  在 `/etc/inputrc` 中添加 `set bell-style none`
  这是一个通用的禁止 DEL 字符提示音的方法。不只适用于 Windows Terminal ，还适用于所有 Linux 发行版的 Terminal。

- Windows Terminal

  设置打开 settings.json，在 profiles.defaults 下增加 "bellStyle": "none"，如下：

  ```shell
      "profiles":
      {
          "defaults":
          {
              "opacity": 85,
              "bellStyle": "none"
          },
          ...
      }
  ```

# 常用技巧

## 长命令换行及注释的处理

```shell
xxxx \
a `# 注释` \
b \
c \
`# d` \
e \
f \
g
```

## bash 补全忽略大小写

> [配置 bash 补全忽略大小写](https://tinychen.com/20191023-bash-completion-ignore-case/)

一般在 centos 和 ubuntu 中使用 bash 的时候，都会使用 `bash-completion`来进行自动补全命令，在默认情况下，补全是区分大小写的，关闭区分大小写功能只需要在 `inputrc`文件中修改一下即可。

如果是最小化安装，可能没有安装这个补全工具。

```shell
# 在centos中使用yum安装
yum install bash-completion -y

# 在/etc/inputrc中添加使全局所有用户生效
echo 'set completion-ignore-case on' >> /etc/inputrc

# 对于个别用户，则可以在用户home目录下添加
echo 'set completion-ignore-case on' >> ~/.inputrc
```

添加完成之后我们重新启动 bash 命令行或者是重新登录一下就可以生效了。

# bash 和 zsh

在 `zsh` 中，`BASH_SOURCE` 是不可用的，因为它是 `bash` 特有的变量。`zsh` 有自己的方式来处理脚本路径和调用栈的访问。

### 在 `zsh` 中的等效方法

尽管 `zsh` 没有直接等价的 `BASH_SOURCE`，你可以通过以下方法来获取类似的信息：

1. **使用 `0` 特殊参数**： `0` 是 `zsh` 中的特殊参数，表示当前脚本的文件名。

   ```shell
   echo "Current script name: $0"
   ```

   然而，`$0` 在某些情况下可能返回的是执行脚本的命令名，而不是文件路径。

2. **使用 `funcfiletrace` 和 `funcstack`**： `zsh` 提供了 `funcfiletrace` 和 `funcstack`，可以获取调用栈和脚本文件路径。

   - `funcstack`：包含当前调用堆栈中函数的名称。
   - `funcfiletrace`：包含当前调用堆栈中函数的文件和行号。

   ```shell
   function show_source {
       echo "Current script file: ${funcfiletrace[1]%:*}"
   }

   show_source
   ```

   在这个例子中，`funcfiletrace[1]` 获取的是当前函数所在的文件和行号，通过去掉行号部分可以得到文件路径。

3. **直接使用 `$0` 和 `dirname`**： 如果你只是想获取脚本的目录路径，可以结合 `$0` 和 `dirname` 来实现：

   ```shell
   script_dir=$(dirname "$0")
   echo "Script directory: $script_dir"
   ```

# oh-my-zsh

**先决条件**：

- [应该安装 Zsh](https://www.zsh.org/)（v4.3.9 或更新版本也可以，但我们更喜欢 5.0.8 及更新版本）。如果没有预安装（运行 `zsh --version`以确认），请查看以下 wiki 说明：[安装 ZSH](https://github.com/ohmyzsh/ohmyzsh/wiki/Installing-ZSH)
- `curl`或者 `wget`应该安装
- `git`应该安装（建议使用 v2.4.11 或更高版本）

## 在线安装

1. 安装 zsh

   - Linux 直接使用 apt 命令：`sudo apt install zsh`
   - Windows 需要以 Git Bash 为基础，参考 [https://juejin.cn/post/7229507721795993661](https://juejin.cn/post/7229507721795993661)

2. 安装 oh-my-zsh

   在命令行输入命令并按回车执行：

   ```sh
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```

   > curl 命令报错：curl: (60) SSL certificate problem: unable to get local issuer certificate:
   >
   > 用 [curl](https://so.csdn.net/so/search?q=curl&spm=1001.2101.3001.7020) 请求的时候，出现 SSL certificate problem，现在不懂证书什么怎么装，总之加上一个 -k 的参数可以解燃眉之急。
   >
   > ```shell
   > sh -c "$(curl -fsSLk https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   > ```

## 离线安装

### 离线安装 zsh

如果你没有 `root` 权限，并且需要离线安装 `zsh`，可以通过下载 `zsh` 的源代码进行本地编译和安装。

> 基本思路是使用 `exec <zsh-path>` 把当前 shell 替换为 zsh。通常，您可以在登录文件（例如 `.profile`（如果您的 shell 是 sh 或 ksh）或 `.login`（如果是 csh））中执行此操作。

以下是详细的步骤：

1. 下载 `zsh` 源代码

   首先，在有互联网连接的计算机上，下载 `zsh` 的源代码压缩包。

   1. 访问 `zsh` 官方网站或 GitHub 仓库：
      - 官方网站: [https://www.zsh.org/](https://www.zsh.org/)
      - GitHub 仓库: [https://github.com/zsh-users/zsh](https://github.com/zsh-users/zsh)
   2. 在 GitHub 上，进入 `Releases` 页面，找到最新版本并下载源代码压缩包（例如 `zsh-5.8.tar.xz`）。

2. 传输源代码

   将下载的压缩包传输到目标机器上，例如通过 USB 驱动器或其他方式。

3. 解压缩源代码

   在目标机器上，解压缩下载的 `zsh` 源代码压缩包：

   ```shell
   tar -xf zsh-5.8.tar.xz
   ```

4. 编译并安装 `zsh`

   进入解压缩后的目录，配置、编译并安装 `zsh` 到你的用户目录：

   ```sh
   cd zsh-5.8

   # 配置安装目录
   ./configure --prefix=$HOME/zsh

   # 编译 zsh
   make

   # 安装 zsh 到指定目录
   make install
   ```

5. 配置 `zsh`

   为了使用新安装的 `zsh`，需要更新你的 `PATH` 环境变量，并将 `zsh` 设置为默认的 shell。

   - 更新 `PATH`

   在你的 shell 配置文件中（例如 `~/.profile` (优先) 或 `~/.bashrc` ），添加以下行：

   ```sh
   export PATH=$HOME/zsh/bin:$PATH
   ```

   然后重新加载配置文件：

   ```sh
   source ~/.profile  # 或者 source ~/.bashrc
   ```

   - 设置 `zsh` 为默认 shell

   在你的 shell 配置文件中，添加以下行：

   ```sh
   export SHELL=$HOME/zsh/bin/zsh
   [ -f $HOME/bin/zsh/bin/zsh ] && exec $HOME/bin/zsh/bin/zsh -l
   ```

   这将使你的 shell 会话在启动时自动切换到 `zsh`。

6. 验证安装

   ```sh
   zsh --version
   ```

   如果显示 `zsh` 的版本信息，则说明安装成功。

### 离线安装 oh-my-zsh

1. 克隆存储库

   ```sh
   git clone https://github.com/ohmyzsh/ohmyzsh.git ~/.oh-my-zsh
   ```

2. _可选_，备份现有 `~/.zshrc`文件

   ```sh
   cp ~/.zshrc ~/.zshrc.orig
   ```

3. 创建一个新的 Zsh 配置文件

   您可以通过复制我们为您提供的模板来创建一个新的 zsh 配置文件。

   ```sh
   cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
   ```

4. source zsh 的配置文件

   - 将默认终端切换成 zsh，

     ```sh
     # 有root权限
     chsh -s $(which zsh)
     # 无root权限
     # 参见 zsh 离线安装
     ```

   - 执行：

     ```sh
     source ~/.zshrc
     ```

## 更改 oh-my-zsh 配置

- 主题：官方文档 | [https://github.com/ohmyzsh/ohmyzsh/wiki/Themes](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes)

  修改 `~/.zshrc`

  ```sh
  # ZSH_THEME="robbyrussell"
  ZSH_THEME="ys"
  # ZSH_THEME="ys_simple"
  ```

  `ys_simple` 详见下面文件。

- 插件：

  - zsh-autosuggestions 官方文档：[zsh-autosuggestions 官方文档](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fzsh-users%2Fzsh-autosuggestions%23suggestion-highlight-style)

    安装：

    ```sh
    cd ~/.oh-my-zsh/custom/plugins
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
    ```

    修改 `vim ~/.zshrc`

    ```sh
    # plugins=(git)
    plugins=(git zsh-autosuggestions)
    ```

- ls 别名

  打开 `zsh` 配置文件（通常是 `vim ~/.zshrc`）进行编辑，在文件尾添加：

  ```sh
  # some more ls aliases
  alias ll='ls -alF'
  alias la='ls -A'
  alias l='ls -CF'
  ```

## PROMPT 语法

PROMPT 语法是 Zsh 用来定义命令行提示符的一种特殊格式。它使用各种转义序列和占位符来显示信息。以下是 PROMPT 语法的主要元素：

1. 基本语法：
   PROMPT 变量使用单引号或双引号包围，如：

   ```zsh
   PROMPT='your prompt here'
   ```

2. 常用占位符：

   - `%n`: 当前用户名
   - `%m`: 主机名（短）
   - `%M`: 完整主机名
   - `%~`: 当前工作目录（相对于家目录）
   - `%/`: 当前工作目录（完整路径）
   - `%c` 或 `%.`: 当前目录名
   - `%D`: 当前日期
   - `%T`: 当前时间（24 小时制）
   - `%*`: 当前时间（带毫秒）
   - `%#`: 如果是超级用户显示 #，否则显示 %

3. 颜色和格式：

   - `%F{color}`: 开始指定颜色的文本
   - `%f`: 结束颜色设置
   - `%B`: 开始粗体文本
   - `%b`: 结束粗体文本
   - `%U`: 开始下划线文本
   - `%u`: 结束下划线文本

   颜色可以是名称（如 red, blue）或数字（0-255）

4. 条件表达式：

   - `%(x.true-text.false-text)`: 条件表达式，x 是条件

5. 转义字符：

   - `%`: 显示 % 字符本身
   - `''`: 在单引号字符串中表示单引号本身

6. 特殊字符：

   - `$`: 通常用于提示符结尾
   - `>`: 常用于多行提示符

示例：

```zsh
PROMPT='%F{green}%n@%m%f:%F{blue}%~%f$ '
```

这会创建一个绿色的用户名和主机名，后跟蓝色的当前目录，最后是一个 $ 符号。

```zsh
PROMPT='[%*] %F{yellow}%~%f %(?.%F{green}√.%F{red}?%?)%f $ '
```

这个例子显示当前时间，黄色的当前目录，如果上一个命令成功则显示绿色的 √，否则显示红色的 ? 和错误代码。

PROMPT 语法非常灵活，允许您创建高度自定义的提示符。您可以组合这些元素来创建符合您需求的提示符。如果您想尝试特定的 PROMPT 设计，我可以帮您构建语法。

示例：

`ys_simple.zsh-theme` 主题：与 ys 主题相同，但是只显示当前路径

```zsh
# Clean, simple, compatible and meaningful.
# Tested on Linux, Unix and Windows under ANSI colors.
# It is recommended to use with a dark background.
# Colors: black, red, green, yellow, *blue, magenta, cyan, and white.
#
# Author: Yad Smood (Modified)

# VCS
YS_VCS_PROMPT_PREFIX1=" %{$fg[white]%}on%{$reset_color%} "
YS_VCS_PROMPT_PREFIX2=":%{$fg[cyan]%}"
YS_VCS_PROMPT_SUFFIX="%{$reset_color%}"
YS_VCS_PROMPT_DIRTY=" %{$fg[red]%}x"
YS_VCS_PROMPT_CLEAN=" %{$fg[green]%}o"

# Git info
local git_info='$(git_prompt_info)'
ZSH_THEME_GIT_PROMPT_PREFIX="${YS_VCS_PROMPT_PREFIX1}git${YS_VCS_PROMPT_PREFIX2}"
ZSH_THEME_GIT_PROMPT_SUFFIX="$YS_VCS_PROMPT_SUFFIX"
ZSH_THEME_GIT_PROMPT_DIRTY="$YS_VCS_PROMPT_DIRTY"
ZSH_THEME_GIT_PROMPT_CLEAN="$YS_VCS_PROMPT_CLEAN"

# HG info
local hg_info='$(ys_hg_prompt_info)'
ys_hg_prompt_info() {
    # make sure this is a hg dir
    if [ -d '.hg' ]; then
        echo -n "${YS_VCS_PROMPT_PREFIX1}hg${YS_VCS_PROMPT_PREFIX2}"
        echo -n $(hg branch 2>/dev/null)
        if [ -n "$(hg status 2>/dev/null)" ]; then
            echo -n "$YS_VCS_PROMPT_DIRTY"
        else
            echo -n "$YS_VCS_PROMPT_CLEAN"
        fi
        echo -n "$YS_VCS_PROMPT_SUFFIX"
    fi
}

local exit_code="%(?,,C:%{$fg[red]%}%?%{$reset_color%})"

# Prompt format:
#
# PRIVILEGES USER @ MACHINE in DIRECTORY on git:BRANCH STATE [TIME] C:LAST_EXIT_CODE
# $ COMMAND
#
# For example:
#
# % ys @ ys-mbp in ~/.oh-my-zsh on git:master x [21:47:42] C:0
# $
PROMPT="
%{$terminfo[bold]$fg[blue]%}#%{$reset_color%} \
%{$fg[cyan]%}%c%{$reset_color%}\
${hg_info}\
${git_info}\
 \
%{$fg[white]%}[%*]%{$reset_color%} \
$exit_code
%{$terminfo[bold]$fg[red]%}$ %{$reset_color%}"
```

## Windows 安装 zsh 终端

Windows 安装 Zsh 终端：[https://juejin.cn/post/7229507721795993661](https://juejin.cn/post/7229507721795993661)

# github 被墙

常见现象：当脚本需要到 `raw.githubusercontent.com` 上拉取代码，出现如下**类似报错**：

```shell
curl: (7) Failed to connect to raw.githubusercontent.com port 443: Connection refused
```

网上搜索了一下，发现是 github 的一些域名的 DNS 解析被污染，导致 DNS 解析过程无法通过域名取得正确的 IP 地址。

**解决方案**：

1. 查询 DNS 对应的 IP
   打开网址 <https://www.ipaddress.com/> ，左侧页签找到 `DNS Lookup`，输入访问不了的域名，如 `raw.githubusercontent.com`，点击【DNS Lookup】，便可查询之后可以获得正确的 IP 地址：

   > `IP Address To Country`也可以查询

   ```shell
   raw.githubusercontent.com has IPv4 address 185.199.108.133
   raw.githubusercontent.com has IPv4 address 185.199.109.133
   raw.githubusercontent.com has IPv4 address 185.199.110.133
   raw.githubusercontent.com has IPv4 address 185.199.111.133
   raw.githubusercontent.com has IPv6 address 2606:50c0:8000::154
   raw.githubusercontent.com has IPv6 address 2606:50c0:8001::154
   raw.githubusercontent.com has IPv6 address 2606:50c0:8002::154
   raw.githubusercontent.com has IPv6 address 2606:50c0:8003::154
   raw.githubusercontent.com has no CNAME resource record
   raw.githubusercontent.com has no TXT resource record
   ```

2. 修改本机 hosts 文件
   hosts 文件在不同系统位置不一，详情如下：

   - Windows 系统：`C:\Windows\System32\drivers\etc\hosts`。
   - Mac（苹果电脑）系统：`/etc/hosts`。
   - Linux 系统：`/etc/hosts`。

   修改方法：把 1 中查询到的 IP 添加到 hosts 文件中 IPV4 或 IPV6 配置末尾，如：

   ```shell
   # This file was automatically generated by WSL. To stop automatic generation of this file, add the following entry to /etc/wsl.conf:
   # [network]
   # generateHosts = false
   127.0.0.1       localhost
   127.0.1.1       cui.localdomain cui
   0.0.0.0 ssl-lvlt.cdn.ea.com
   # 新添加内容
   185.199.108.133 raw.githubusercontent.com
   185.199.108.133 user-images.githubusercontent.com
   185.199.108.133 avatars2.githubusercontent.com
   185.199.108.133 avatars1.githubusercontent.com

   # The following lines are desirable for IPv6 capable hosts
   ::1     ip6-localhost ip6-loopback
   fe00::0 ip6-localnet
   ff00::0 ip6-mcastprefix
   ff02::1 ip6-allnodes
   ff02::2 ip6-allrouters
   ```

3. 激活生效
   大部分情况下是直接生效，如未生效可尝试下面的办法，刷新 DNS：

   - Windows：在 CMD 窗口输入：`ipconfig /flushdns`
   - Mac 命令：`sudo killall -HUP mDNSResponder`
   - Linux 命令：`sudo nscd restart`

   Tips： 如以上刷新不好使，请重启尝试
