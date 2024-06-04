[toc]



# bash 命令

cat 显示指定行
head -n [行数a] # 显示开始a行

head -num [文件名]

tail -n [行数a] # 显示最后a行
tail -n +[行数a] # 从a行以后开始显示

例子
显示前1000行
cat [filename] | head -n 1000

显示最后1000行
cat [filename] | tail -n 1000

从1000行以后开始显示
cat [filename] | tail -n +1000

组合例子
从1000行开始显示3000行
cat [filename] | tail -n +1000 | head -n 3000

从3000行开始显示1000行
cat [filename] | tail -n +3000 | head -n 1000

显示1000行到3000行
cat [filename] | head -n 3000 | tail -n +1000



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



# x

## oh-my-zsh on Windows

The function will not be run in future, but you can run
it yourself as follows:
  autoload -Uz zsh-newuser-install
  zsh-newuser-install -f

The code added to ~/.zshrc is marked by the lines
# Lines configured by zsh-newuser-install
# End of lines configured by zsh-newuser-install
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
