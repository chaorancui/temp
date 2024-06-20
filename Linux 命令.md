[toc]



# bash 命令

## shell 配置文件介绍

> [详解/etc/profile、/etc/bash.bahsrc、\~/.profile、\~/.bashrc的用途](https://blog.csdn.net/jirryzhang/article/details/70833544?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-12-70833544-blog-138886149.235^v43^pc_blog_bottom_relevance_base3&spm=1001.2101.3001.4242.7&utm_relevant_index=15)
>
> [ubuntu中环境变量文件/etc/profile、.profile、.bashrc、/etc/bash.bashrc之间的区别和联系](https://blog.csdn.net/qq_51246603/article/details/127459786?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-5-127459786-blog-119089926.235^v43^pc_blog_bottom_relevance_base3&spm=1001.2101.3001.4242.4&utm_relevant_index=8)

Linux 是一个多用户的操作系统。每个用户登录系统后，都会有一个专用的运行环境。通常每个用户默认的环境都是相同的，这个默认环境实际上就是一组环境变量的定义。用户可以对自己的运行环境进行定制，其方法就是修改相应的系统环境变量。

### 配置文件

Linux 安装时可能要修改的配置文件：

```shell
/etc/profile
/etc/bashrc			# ubuntu没有这个文件，对应地，其有/etc/bash.bashrc文件
~/.bash_profile		# 一般有.bash_profile、.bash_login、.profile中一个或多个
~/.bash_login
~/.profile
~/.bashrc
```

> [Shell-环境变量的配置文件介绍](https://www.cnblogs.com/ygbh/p/17427943.html)

* 系统级别

  针对所有的用户的所有的 shell / 各别 shell，登录时读取

  ```shell
  /etc/profile 			# 操作系统级别，登录 shell 时执行，并从 /etc/profile.d 目录的配置文件中搜集 shell 的设置
  /etc/profile.d/*.sh		# 系统软件级别
  /etc/bashrc				# 登录 bash shell 时读取
  /etc/bash.bashrc		# 登录 bash shell 时读取
  ```

* 个人级别

  某个用户的所有shell，登录时读取，一般默认读取 ~/.bashrc

  ```shell
  # 个人级别： (优先级从上到下，一般只会读取优先级高的一个，不会覆盖)
  ~/.bash_profile
  ~/.bash_login
  ~/.profile
  ```

* bash级别

  某个用户的 bash，登录及打开新 shell 时都会读取

  ```shell
  ~/.bashrc
  ```

### 文件执行顺序

![](https://img2023.cnblogs.com/blog/918540/202305/918540-20230524122028472-1978276734.png)

当登入系统时候获得一个shell进程时，其读取环境设定档有三步：

1. 首先读入的是全局环境变量设定档/etc/profile，然后根据其内容读取额外的设定的文档，如
   /etc/profile.d和 /etc/inputrc。

2. 然后根据不同使用者帐号，去其家目录读取/.bash_profile，如果这读取不了就读取/.bash_login，这个也读取不了才会读取
   ~/.profile，这三个文档设定基本上是一样的，读取有优先关系。

3. 然后先读取/etc/bashrc或/etc/bash.bashrc，再根据用户帐号读取~/.bashrc。



### Q & A：

* **Q：**/etc/profile与/etc/bashrc的区别？

  **A：**/etc/profile，/etc/bashrc 都是系统全局环境变量设定。

  * 前一个主要用来设置一些系统变量，比如 JAVA_HOME 等等。
  * 后面一个主要用来保存一些 bash 的设置。

* **Q：**/.profile与/.bashrc的区别？

  **A：**都具有个性化定制功能。

  * ~/.profile 可以设定本用户专有的路径，环境变量，等，它只能登入的时候执行一次。
  * ~/.bashrc 也是某用户专有设定文档，可以设定路径，命令别名，每次 shell script 的执行都会使用它一次。



## 交互式_非交互式_登录式_非登录式 shell

> [Linux-命令-交互式_非交互式_登录式_非登录式.md](https://wetts.github.io/2020/03/14/%E7%B3%BB%E7%BB%9F%E3%80%81%E6%9C%8D%E5%8A%A1%E5%99%A8/%E7%B3%BB%E7%BB%9F/Linux/Linux-%E5%91%BD%E4%BB%A4-%E4%BA%A4%E4%BA%92%E5%BC%8F_%E9%9D%9E%E4%BA%A4%E4%BA%92%E5%BC%8F_%E7%99%BB%E5%BD%95%E5%BC%8F_%E9%9D%9E%E7%99%BB%E5%BD%95%E5%BC%8F/)

Linux shell 是用户与 Linux 系统进行交互的媒介，而 bash 作为目前 Linux 系统中最常用的 shell，它在运行时具有两种属性，即“交互”与“登陆”。

- 按照 bash 是否与用户进行交互，可以将其分为“交互式”与“非交互式”；
- 而按照 bash 是否被用户登陆，又可将其分为“登陆 shell”与“非登陆 shell”。

| 执行方式              | profile | bashrc |                             示例                             |
| :-------------------- | :-----: | :----: | :----------------------------------------------------------: |
| 非交互式且非登录shell | 不加载  | 不加载 |                  `crontab`中执行的bash脚本                   |
| 非交互式登录shell     |  加载   |  加载  |               `crontab`中通过`su -l`执行的脚本               |
| 交互式非登录shell     | 不加载  |  加载  |             如命令行中通过`su 用户名`执行的命令              |
| 交互式登录shell       |  加载   |  加载  | 普通的终端登录, ssh远程登录, 以及使用`su - l 用户名`切换身份等 |

### “交互式”与“非交互式”

#### 含义说明

- 交互式，是 shell 的一种运行模式，交互式 shell **等待你输入命令**，并且立即执行，然后将结果反馈给你。这是每个 CLI 用户都非常熟悉的流程：登录、执行一些命令、登出。当你登出后，这个 shell 就终止了。
- 非交互式，是 shell 的另一种运行模式，它专门被用来执行预先设定的命令。在这种模式下，shell 不与用户进行交互，而是**读取存放在脚本文件中的命令**并执行它们。当它读到文件的结尾，这个 shell 就终止了。

#### 启动方法

根据bash手册上的描述：

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

#### 判别方法

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

### “登陆 shell”与“非登陆 shell”

#### 含义说明

“登陆 shell”通常指的是：

1. 用户通过输入用户名/密码（或证书认证）后启动的 shell；
2. 通过带有 `-l|--login` 参数的 bash 命令启动的 shell。

例如，系统启动、远程登录、使用 `su -` 切换用户、通过 `bash --login` 命令启动 bash 等。

而其他情况启动的 shell 基本上就都是“非登陆 shell”了。

例如，从图形界面启动终端、使用 `su` 切换用户、通过 `bash` 命令启动 bash 等。

#### 判别方法

根据 bash 手册上的描述：

> A login shell is one whose first character of argument zero is a `-`, or one started with the `--login` option.

我们可以通过在 shell 中 `echo $0` 查看，显示 `-bash` 的一定是“登陆 shell”，反之显示 bash 的则不好说。

```
[chen@localhost ~]$ bash --login
[chen@localhost ~]$ echo $0
bash
[chen@localhost ~]$ 
```

可以看出，使用 `bash --login` 启动的“登陆 shell”，其 `$0` 也并非以 `-` 开头，这也就是为什么手册上的描述里使用“or”的原因。

另外，当我们执行 exit 命令退出 shell 时，也可以观察到它们的不同之处：

```
[chen@localhost ~]$ bash --login
[chen@localhost ~]$ exit   # 退出登陆shell
logout
[chen@localhost ~]$ bash
[chen@localhost ~]$ exit   # 退出非登陆shell
exit
[chen@localhost ~]$
```

原则上讲，我们使用 logout 退出“登陆 shell”，使用 exit 退出“非登录 shell”。但其实 exit 命令会判断当前 shell 的“登陆”属性，并分别调用 logout 或 exit 指令，因此使用起来相对方便（即执行exit命令，退出的shell可以是登录或者非登录shell；执行logout命令，则只能退出登录shell，不能退出非登录shell）。

#### 主要区别

对于用户而言，“登录 shell”和“非登陆 shell”的主要区别在于启动 shell 时所执行的 startup 文件不同。

简单来说，“登录 shell”执行的 startup 文件为 `~/.bash_profile`，而“非登陆 shell”执行的 startup 文件为 `~/.bashrc`。



登录shell（包括交互式登录shell和使用“–login”选项的非交互shell），它会首先读取和执行 ` /etc/profile`全局配置文件中的命令，然后依次查找`~/.bash_profile`、`~/.bash_login` 和 `~/.profile` 这三个配置文件，读取和执行这三个中的第一个存在且可读的文件中命令。除非被“–noprofile”选项禁止了。

在非登录shell里，只读取 `~/.bashrc` （和 `/etc/bash.bashrc`、`/etc/bashrc` ）文件，不同的发行版里面可能有所不同，如RHEL6.3中非登录shell仅执行了“~/.bashrc”文件（没有执行/etc/bashrc），而KUbuntu10.04中却依次执行了/etc/bash.bashrc 和 ~/.bashrc 文件。





# Linux命令

## 查看 Linux 发行版本名和版本号

如果你加入了一家新公司，要为开发团队安装所需的软件并重启服务，这个时候首先要弄清楚它们运行在什么发行版以及哪个版本的系统上，你才能正确完成后续的工作。作为系统管理员，充分了解系统信息是首要的任务。

因为对于诸如 RHEL、Debian、openSUSE、Arch Linux 这几种主流发行版来说，它们各自拥有不同的包管理器来管理系统上的软件包，如果不知道所使用的是哪一个发行版的系统，在软件包安装的时候就会无从下手，而且由于大多数发行版都是用 systemd 命令而不是 SysVinit 脚本，在重启服务的时候也难以执行正确的命令。

### 方法 1： lsb_release 命令

LSB（Linux 标准库Linux Standard Base）能够打印发行版的具体信息，包括发行版名称、版本号、代号等。

```bash
# lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description: Ubuntu 16.04.3 LTS
Release: 16.04
Codename: xenial
```

### 方法 2： /etc/*-release 文件

release 文件通常被视为操作系统的标识。在 `/etc` 目录下放置了很多记录着发行版各种信息的文件，每个发行版都各自有一套这样记录着相关信息的文件。下面是一组在 Ubuntu/Debian 系统上显示出来的文件内容 `cat /etc/lsb-release`。

```bash
# cat /etc/issue
Ubuntu 16.04.3 LTS \n \l

# cat /etc/issue.net
Ubuntu 16.04.3 LTS

# cat /etc/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=16.04
DISTRIB_CODENAME=xenial
DISTRIB_DESCRIPTION="Ubuntu 16.04.3 LTS"

# cat /etc/os-release
NAME="Ubuntu"
VERSION="16.04.3 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.3 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial

# cat /etc/debian_version
9.3
```

下面这一组是在 RHEL/CentOS/Fedora 系统上显示出来的文件内容。其中 `/etc/redhat-release` 和 `/etc/system-release` 文件是指向 `/etc/[发行版名称]-release` 文件的一个连接。

```bash
# cat /etc/centos-release
CentOS release 6.9 (Final)

# cat /etc/fedora-release
Fedora release 27 (Twenty Seven)

# cat /etc/os-release
NAME=Fedora
VERSION="27 (Twenty Seven)"
ID=fedora
VERSION_ID=27
PRETTY_NAME="Fedora 27 (Twenty Seven)"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:fedoraproject:fedora:27"
HOME_URL="https://fedoraproject.org/"
SUPPORT_URL="https://fedoraproject.org/wiki/Communicating_and_getting_help"
BUG_REPORT_URL="https://bugzilla.redhat.com/"
REDHAT_BUGZILLA_PRODUCT="Fedora"
REDHAT_BUGZILLA_PRODUCT_VERSION=27
REDHAT_SUPPORT_PRODUCT="Fedora"
REDHAT_SUPPORT_PRODUCT_VERSION=27
PRIVACY_POLICY_URL="https://fedoraproject.org/wiki/Legal:PrivacyPolicy"

# cat /etc/redhat-release
Fedora release 27 (Twenty Seven)

# cat /etc/system-release
Fedora release 27 (Twenty Seven)
```

### 方法 3： uname 命令

uname（unix name 的意思） 是一个打印系统信息的工具，包括内核名称、版本号、系统详细信息以及所运行的操作系统等等。

- **建议阅读：** [6种查看系统 Linux 内核的方法](https://www.2daygeek.com/check-find-determine-running-installed-linux-kernel-version/)

```bash
# uname -a
Linux 2grhel8node 4.18.0-477.13.1.el8_8.x86_64 #1 SMP Thu May 18 10:27:05 EDT 2023 x86_64 x86_64 x86_64 GNU/Linux
```

解释如下:
* Linux – Kernel name. The name of the kernel running on your system.
* 2grhel8node – Hostname
* 4.18.0-477.13.1.el8_8.x86_64 – Kernel release
* 1 SMP Thu May 18 10:27:05 EDT 2023 – Kernel version and last compiled date and time.
* x86_64 – Machine architecture
* x86_64 – Processor architecture
* x86_64 – Operating system architecture
* GNU/Linux – Operating system

### 方法 4： /proc/version 文件

这个文件记录了 Linux 内核的版本、用于编译内核的 gcc 的版本、内核编译的时间，以及内核编译者的用户名。

```bash
# cat /proc/version
Linux version 4.12.14-300.fc26.x86_64 ([email protected]) (gcc version 7.2.1 20170915 (Red Hat 7.2.1-2) (GCC) ) #1 SMP Wed Sep 20 16:28:07 UTC 2017
```



## SUSE 的包管理工具 zypper

**1. 安装包**
语法： # zypper install 示例：安装Mozilla firefox

```bash
zypper install MozillaFirefox
```

**2. 安装源码包**
语法：# zypper source-install 示例：从库中安装 apache

```bash
zypper source-install apache2-mod_nss
```

**3. 更新包**

更新某一软件包： # zypper update 更新所有软件包： # zypper update
查看所有可用的更新列表：# zypper list-updates

```shell
zypper update xxx
```

**4. 删除包**

语法：# zypper remove 示例：移除Mozilla Firefox

```bash
zypper remove MozillaFirefox
```

**5. 查找包**

语法：# zypper search 示例：查找所有usb开头的软件包

```bash
zypper search usb*
```

**6. 查看软件包详情**

语法： zypper info 示例：查看usbutils的信息

```bash
zypper info usbutils
```

**7. 打补丁**

查看所有可打补丁: zypper patches
安装指定补丁：zypper patch

**8. 锁住包**

软件包被锁之后将不能被移除或升级，下面演示一下如何加锁
1）加al选项锁住包文件“usbutils”, al 是 add lock的缩写

```bash
zypper al usbutils
```

2）加ll选项查看所有已被锁住的软件包, ll 是 List Locks的缩写

```bash
zypper ll
```

**9. 解锁包**

加rl选项解锁usbutils, rl 是 remove lock的缩写

```bash
zypper rl usbutils
```



> [zypper命令使用示例](https://www.linuxprobe.com/zypper-commands-examples.html)



## 常用命令

### curl 命令

> [curl 的用法指南](https://www.ruanyifeng.com/blog/2019/09/curl-reference.html)
>
> [curl命令详解](https://handerfly.github.io/linux/2019/05/26/curl%E5%91%BD%E4%BB%A4%E8%AF%A6%E8%A7%A3/)
>
> [Linux curl命令详解](https://www.cnblogs.com/duhuo/p/5695256.html)

`curl` 命令是一个功能强大的网络工具，它的名字就是客户端（client）的 URL 工具的意思。它能够通过http、ftp等方式下载文件，也能够上传文件，同时支持HTTPS等众多协议，还支持POST、cookies、认证、从指定偏移处下载部分文件、用户代理字符串、限速、文件大小、进度条等特征。其实curl远不止前面所说的那些功能，大家可以通过man curl阅读手册页获取更多的信息。

类似的工具还有 wget。

常用参数 curl 命令参数很多，这里只列出 shell 脚本中经常用到过的那些。

```shell
-a/--append 上传文件时，附加到目标文件

-A:随意指定自己这次访问所宣称的自己的浏览器信息

-b/--cookie <name=string/file> cookie字符串或文件读取位置，使用option来把上次的cookie信息追加到http request里面去。

-c/--cookie-jar <file> 操作结束后把cookie写入到这个文件中

-C/--continue-at <offset>  断点续转

-d/--data <data>   HTTP POST方式传送数据

    --data-ascii <data>	以ascii的方式post数据
     --data-binary <data>	以二进制的方式post数据
     --negotiate	使用HTTP身份验证
     --digest	使用数字身份验证
     --disable-eprt	禁止使用EPRT或LPRT
     --disable-epsv	禁止使用EPSV
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









### wget 命令





### ssh 登录命令

> 参考：
>
> ```shell
> man ssh
> ```

Linux 一般作为服务器使用，而服务器一般放在机房，你不可能在机房操作你的 Linux 服务器。

这时我们就需要远程登录到Linux服务器来管理维护系统。

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
 `ssh://[user@]hostname[:port]`.  The user must prove their identity to the remote machine using one of several methods (see below).

常用登录命令：

```shell
ssh -p 22 my@127.0.0.1
# 输入密码：
```

**-p** 后面是端口

**my** 是服务器用户名

**127.0.0.1** 是服务器 ip

回车输入密码即可登录

> [设置SSH通过秘钥登录](https://www.runoob.com/w3cnote/set-ssh-login-key.html)



### scp

> 参考：
>
> ```shell
> man scp
> ```

scp 在网络上的主机之间复制文件。

它使用 ssh 进行数据传输，并使用与登录会话相同的身份验证和提供相同的安全性。

scp 将要求提供密码或密码短语（如果身份验证需要它们）。

源和目标可以被指定为本地路径名、带有可选路径的远程主机（格式为`[user@]host:[path]`）或URI（格式为：
`scp://[user@]host[:port][/path]`）。可以使用绝对或相对路径名显式指定本地文件名，以避免scp处理包含“：”的文件名
作为主机说明符。

在两个远程主机之间进行复制时，如果使用URI格式，则在使用-R选项的情况下，无法指定目标上的端口。

```js
scp 【本地要上传文件地址】  [用户名]@[ip地址]：远程地址

//例如我的本地要上传的文件地址是c://user/code/demo/dist,用户名是root，IP地址是192.168.9.25
scp -r c://user/code/demo/dist root@192.168.9.25:/home/root/demo/fe/ 
//如果我当前在c://user/code/demo/下(比如在vscode打开demo项目打开终端)，就可以执行以下命令直接上传
//-r代表上传的是文件夹以及文件夹里所有的东西
scp -r dist root@192.168.9.25:/home/root/demo/fe/ 
```





### cat/head/tail

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
cat filename	# 查看文件内容：显示文件 filename 的内容。

cat > filename	# 创建文件：将标准输入重定向到文件 filename，覆盖该文件的内容。

cat >> filename	# 追加内容到文件：将标准输入追加到文件 filename 的末尾。

cat file1 file2 > file3	# 连接文件：将 file1 和 file2 的内容合并到 file3 中。

cat file1 file2	# 显示多个文件的内容：同时显示 file1 和 file2 的内容。

cat filename | command	# 使用管道：将 cat 命令的输出作为另一个命令的输入。

cat filename | tail -n 10	# 查看文件的最后几行：显示文件 filename 的最后 10 行。

cat -n filename	# 使用 -n 选项显示行号：显示文件 filename 的内容，并在每行的前面加上行号。

cat -b filename	# 使用 -b 选项仅显示非空行的行号：

cat -s filename	# 使用 -s 选项合并空行：显示文件 filename 的内容，并合并连续的空行。

cat -t filename	# 使用 -t 选项显示制表符：显示文件 filename 的内容，并用 ^I 表示制表符。

cat -e filename	# 使用 -e 选项显示行结束符：显示文件 filename 的内容，并用 $ 表示行结束。

cat -n textfile1 > textfile2	# 把 textfile1 的文档内容加上行号后输入 textfile2 这个文档里：

cat -b textfile1 textfile2 >> textfile3	# 把 textfile1 和 textfile2 的文档内容加上行号（空白行不加）之后将内容附加到 textfile3 文档里：

cat /dev/null > /etc/test.txt	# 清空 /etc/test.txt 文档内容：
```



head 命令可用于查看文件的开头部分的内容，有一个常用的参数 **-n** 用于显示行数，默认为 10，即显示 10 行的内容。

```shell
head [参数] [文件]  
```

- -q 隐藏文件名
- -v 显示文件名
- -c<数目> 显示的字节数。
- -n<行数> 显示的行数。

```shell
head -n 5 runoob_notes.log	# 显示 notes.log 文件的开头 5 行，请输入以下命令

head -c 20 runoob_notes.log	# 显示文件前 20 个字节
```



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
- --pid=PID 与-f合用,表示在进程ID,PID死掉之后结束
- -q, --quiet, --silent 从不输出给出文件名的首部
- -s, --sleep-interval=S 与-f合用,表示在每次反复的间隔休眠S秒

```shell
tail -n +20 notes.log	# 显示文件 notes.log 的内容，从第 20 行至文件末尾

tail -f notes.log	# 此命令显示 notes.log 文件的最后 10 行。当将某些行添加至 notes.log 文件时，tail 命令会继续显示这些行。 显示一直继续，直到您按下（Ctrl-C）组合键停止显示。即，可跟踪名为 notes.log 的文件的增长情况。
```



组合使用：

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









# oh-my-zsh on Windows

The function will not be run in future, but you can run
it yourself as follows:
  autoload -Uz zsh-newuser-install
  zsh-newuser-install -f

The code added to ~/.zshrc is marked by the lines

 Lines configured by zsh-newuser-install

 End of lines configured by zsh-newuser-install

You should not edit anything between these lines if you intend to
run zsh-newuser-install again.  You may, however, edit any other part
of the file.



curl 命令报错：curl: (60) SSL certificate problem: unable to get local issuer certificate:

用 [curl](https://so.csdn.net/so/search?q=curl&spm=1001.2101.3001.7020) 请求的时候，出现 SSL certificate problem，现在不懂证书什么怎么装，总之加上一个 -k 的参数可以解燃眉之急。

```shell
curl -k https://baidu.com
```

Windows 系统中配置终端 Oh-My-Zsh 教程:https://dreamhomes.top/posts/202201092010/

Git-Zsh on Windows安装与配置:https://amagi.yukisaki.io/article/96e5adc4-1212-4260-8399-4dfd3964dc3b/

Zsh / Oh-my-zsh on Windows Git Bash:https://gist.github.com/fworks/af4c896c9de47d827d4caa6fd7154b6b





