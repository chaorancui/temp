[toc]

# Linux 相关网址记录

1. [Linux Tools Quick Tutorial](https://linuxtools-rst.readthedocs.io/zh-cn/latest/base/index.html)

# 系统

## 软件源

### 更换软件源

1. 备份软件源

   ```bash
   sudo cp /etc/apt/sources.list /etc/apt/sources.list.bkp
   ```

2. 更换软件源
   根据 ubuntu 系统版本，从下面网站中找到相应的软件源，然后更新到 `/etc/apt/sources.list` 或 `/etc/apt/sources.list.d/ubuntu.sources` 文件中，更改文件后再运行 `sudo apt-get update` 更新索引以生效。

   - [[中科大镜像源 | mirrors.ustc.edu.cn]](https://mirrors.ustc.edu.cn/repogen/)
   - [[清华镜像源 | mirrors.tuna.tsinghua.edu.cn]](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)

   ```bash
   sudo vim /etc/apt/sources.list
   # 修改内容 xxxx
   sudo apt-get update
   ```

**无内置编辑器**

ubuntu 最小安装时，可能会遇到没有内置的编辑器的情况，vi/vim/emacs/nano/gedit(一个 GUI 的文本编辑器，Ubuntu 默认安装)。这时候无法编辑软件源，可以使用如下方法：

1. `sources.list` 格式

   ```bash
   # 备份
   sudo cp /etc/apt/sources.list /etc/apt/sources.list.bkp

   # 更新默认源
   # 从 http://archive.ubuntu.com/ 替换为 http://mirrors.ustc.edu.cn/ 即可。
   sudo sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list

   # 更新安全源，因镜像站同步有延迟，可能会导致生产环境系统不能及时检查、安装上最新的安全更新，不建议替换 security 源。
   # 从 http://security.ubuntu.com/ 替换为 https://mirrors.ustc.edu.cn/ 即可。
   sudo sed -i 's/security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
   ```

2. `DEB822` 格式

   ```bash
   # 备份
   sudo cp /etc/apt/sources.list /etc/apt/sources.list.bkp

   # 更新默认源
   # 从 http://archive.ubuntu.com/ 替换为 http://mirrors.ustc.edu.cn/ 即可。
   sudo sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list.d/ubuntu.sources

   # 更新安全源，因镜像站同步有延迟，可能会导致生产环境系统不能及时检查、安装上最新的安全更新，不建议替换 security 源。
   # 从 http://security.ubuntu.com/ 替换为 https://mirrors.ustc.edu.cn/ 即可。
   sudo sed -i 's/security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/ubuntu.sources
   ```

> Tip:
> 使用 HTTPS 可以有效避免国内运营商的缓存劫持。可以运行以下命令替换：
>
> ```bash
> sudo sed -i 's/http:/https:/g' /etc/apt/sources.list   # sources.list
> sudo sed -i 's/http:/https:/g' /etc/apt/sources.list.d/ubuntu.sources    # deb822
> ```

### 传统 & deb822

**Ubuntu：**

在 Ubuntu 24.04 之前，Ubuntu 的软件源配置文件使用传统的 One-Line-Style，路径为 `/etc/apt/sources.list`；
从 Ubuntu 24.04 开始，Ubuntu 的软件源配置文件变更为 DEB822 格式，路径为 `/etc/apt/sources.list.d/ubuntu.source`。

**Debian：**

大部分 Debian 的软件源配置文件使用传统的 One-Line-Style，路径为 `/etc/apt/sources.list`；
但是对于容器镜像，从 Debian 12 开始，其软件源配置文件变更为 DEB822 格式，路径为 `/etc/apt/sources.list.d/debian.sources`。
一般情况下，将对应文件中 Debian 默认的源地址 `http://deb.debian.org/` 替换为镜像地址即可。

> 什么是 DEB822 (.sources) 文件格式？
>
> 自新版本的 Debian 与 Ubuntu 起，例如：
>
> - Debian 12 的容器镜像
> - Ubuntu 24.04
>
> 默认预装的系统中 APT 的系统源配置文件不再是传统的 `/etc/apt/sources.list`。传统格式（又被称为 One-Line-Style 格式）类似如下：
>
> ```bash
> deb http://mirrors.ustc.edu.cn/debian/ bookworm main contrib
> ```
>
> 新的 DEB822 格式自 APT 1.1（2015 年发布）起支持，后缀为 `.sources`，存储在 `/etc/apt/sources.list.d/` 目录下，格式类似如下：
>
> ```txt
> Types: deb
> URIs: https://mirrors.ustc.edu.cn/debian
> Suites: bookworm
> Components: main contrib
> Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
> ```
>
> 在切换软件源时，**需要根据实际情况选择对应的格式进行修改**。
>
> 关于 DEB822 格式的设计考虑，可以参考[官方文档](https://repolib.readthedocs.io/en/latest/deb822-format.html)（英文）。

## 系统版本

### 发行版本名和版本号

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

### SUSE 包管理 zypper

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

# 账户操作命令

## useradd 命令

`useradd` 是一个用于在 Linux 系统中创建新用户的命令。它是一个低级命令，没有 `adduser` 那么多交互式功能，因此通常需要手动指定更多的选项，如密码、用户组、家目录等。相比于 `adduser`，`useradd` 更加简洁且灵活，适用于需要脚本化管理用户的场景。

**基本语法：**

```bash
sudo useradd [选项] <用户名>
```

**常见选项和用法：**

1. **创建新用户**

   最基本的 `useradd` 命令是创建一个新用户。默认情况下，这个命令会为新用户创建一个家目录，并使用系统默认的 shell。

   ```bash
   sudo useradd <username>
   ```

   例如，创建一个名为 `alice` 的新用户： `sudo useradd alice`。
   此命令会创建用户 `alice`，但不会为其设置密码、全名等。用户的家目录默认会创建在 `/home/alice`，并使用默认的 shell（通常是 `/bin/bash`）。

2. **为用户设置密码**

   `useradd` 命令只负责创建用户，设置密码是一个单独的操作。可以使用 `passwd` 命令来为用户设置密码：

   ```bash
   sudo passwd <username>
   ```

   例如，为 `alice` 设置密码：`sudo passwd alice`。 这会提示你输入并确认密码。

3. **指定用户的用户组**

   默认情况下，`useradd` 会为每个新用户创建一个与用户名相同的组，并将该用户添加到该组中。你也可以使用 `-g` 选项指定一个现有的组。

   ```bash
   sudo useradd -g <groupname> <username>
   ```

   例如，将 `alice` 添加到 `developers` 组：`sudo useradd -g developers alice`。

4. **为用户设置家目录**

   默认情况下，`useradd` 会在 `/home/` 下创建用户的家目录。如果你想指定一个不同的家目录位置，可以使用 `-d` 选项。

   ```bash
   sudo useradd -d /path/to/home <username>
   ```

   例如，将 `alice` 的家目录设置为 `/data/alice`：`sudo useradd -d /data/alice alice`。

5. **为用户设置默认 shell**

   使用 `-s` 选项，可以指定用户的默认 shell。默认情况下，`useradd` 会使用系统默认的 shell（通常是 `/bin/bash`），但你可以通过此选项更改：

   ```bash
   sudo useradd -s /bin/zsh <username>
   ```

   例如，将 `alice` 的默认 shell 设置为 `zsh`：`sudo useradd -s /bin/zsh alice`。

6. **为用户指定 UID 和 GID**

   你可以使用 `-u` 和 `-g` 选项来指定用户的 UID（用户 ID）和 GID（组 ID）。这在需要与其他系统共享用户和组 ID 时非常有用。

   ```bash
   sudo useradd -u <UID> -g <GID> <username>
   ```

   例如，将 `alice` 的 UID 设置为 `1001`，GID 设置为 `1001`：`sudo useradd -u 1001 -g 1001 alice`。

7. **为用户创建附加组**

   如果你想将用户添加到多个组，可以使用 `-G` 选项。此选项允许将用户添加到一个或多个附加组（以逗号分隔）。

   ```bash
   sudo useradd -G <group1>,<group2>,<group3> <username>
   ```

   例如，将 `alice` 添加到 `developers` 和 `admins` 两个附加组：`sudo useradd -G developers,admins alice`。

8. **创建系统用户**

   使用 `-r` 选项可以创建一个系统用户，系统用户通常用于运行系统服务，并且不会有登录权限。

   ```bash
   sudo useradd -r <username>
   ```

   例如，创建一个名为 `myservice` 的系统用户：`sudo useradd -r myservice`。

9. **创建用户并指定密码**

   `useradd` 本身不支持直接为用户设置密码，但你可以将 `passwd` 命令与 `useradd` 命令结合使用，在创建用户后立即为其设置密码。

   ```bash
   sudo useradd <username> && sudo passwd <username>
   ```

   例如：`sudo useradd alice && sudo passwd alice`。

10. **删除用户**

    `userdel` 命令用于删除用户。使用 `-r` 选项可以删除用户及其家目录。

    ```bash
    sudo userdel -r <username>
    ```

    例如，删除用户 `alice` 和其家目录：`sudo userdel -r alice`。

**常见选项总结：**

| 选项 | 描述                                         |
| ---- | -------------------------------------------- |
| `-d` | 设置用户的家目录路径                         |
| `-s` | 设置用户的默认 shell                         |
| `-u` | 设置用户的 UID（用户 ID）                    |
| `-g` | 设置用户的主组（GID）                        |
| `-G` | 设置用户的附加组（以逗号分隔）               |
| `-r` | 创建一个系统用户，通常没有登录权限           |
| `-m` | 创建用户时自动创建家目录（默认会创建）       |
| `-f` | 设置密码过期前的宽限期（指定天数）           |
| `-p` | 设置用户的密码（通过加密字符串，通常不推荐） |

**示例：**

1. **创建一个新用户 `alice` 并设置其密码**

   ```bash
   sudo useradd -m -s /bin/bash alice && sudo passwd alice
   ```

2. **为 `alice` 设置自定义家目录和默认 shell**

   ```bash
   sudo useradd -d /data/alice -s /bin/zsh -m alice
   ```

3. **创建系统用户 `myservice`**

   ```bash
   sudo useradd -r myservice
   ```

4. **将用户 `alice` 添加到 `developers` 和 `admins` 组**

   ```bash
   sudo useradd -G developers,admins alice
   ```

5. **删除用户并同时删除其家目录**

   ```bash
   sudo userdel -r alice
   ```

**总结：**

`useradd` 是一个强大且灵活的工具，用于创建和管理用户账户。它适用于需要脚本化或系统化管理用户的场景，允许用户指定更多详细的配置选项（如 UID、GID、家目录、shell 等）。然而，它不像 `adduser` 那样交互式，因此需要手动设置更多的选项来完成用户的创建和配置。

## adduser 交互命令

`adduser` 是一个在 Linux 系统中用来创建新用户的命令。它是 `useradd` 命令的一个更为友好的前端，并提供了更多的交互式选项。与 `useradd` 不同，`adduser` 会自动创建用户的家目录并询问一些额外的设置，比如用户全名、密码等。

**基本语法：**

```bash
sudo adduser [选项] <用户名>
```

**常见用法：**

1. **创建一个新用户**

   最基本的使用方式是创建一个新用户。你只需指定用户名，`adduser` 命令会创建一个新的用户账户，**并执行一些初始化操作（如创建家目录、设置默认 shell 等）**：

   ```bash
   sudo adduser <username>
   ```

   例如，要创建名为 `alice` 的用户：`sudo adduser alice`。

   在执行此命令时，系统会要求你输入以下信息：

   - 密码（需要输入两次）
   - 用户全名
   - 房间号码
   - 工作电话
   - 个人电话
   - 其他信息（可选）

   如果你不想填写某个字段，可以直接按 `Enter` 跳过。创建完成后，`alice` 用户就被添加到系统中，并且其家目录通常是 `/home/alice`。

2. **指定用户的用户组**

   你可以指定用户所在的用户组。`adduser` 命令默认会为新用户创建一个与用户名相同的组，但你可以通过 `--ingroup` 选项指定用户属于的组：

   ```bash
   sudo adduser <username> --ingroup <groupname>
   ```

   例如，将 `alice` 用户添加到名为 `developers` 的组：`sudo adduser alice --ingroup developers`。

3. **指定用户的家目录**

   你可以使用 `--home` 选项指定用户的家目录。默认情况下，`adduser` 会将用户的家目录创建在 `/home/` 下，但你可以通过此选项指定其他目录路径：

   ```bash
   sudo adduser <username> --home /path/to/home
   ```

   例如，将 `alice` 用户的家目录设置为 `/data/alice`：`sudo adduser alice --home /data/alice`。

4. **禁用用户创建密码**

   如果你不希望用户在创建时设置密码，可以使用 `--disabled-password` 选项：

   ```bash
   sudo adduser <username> --disabled-password
   ```

   例如，创建没有密码的 `bob` 用户：`sudo adduser bob --disabled-password`。

   此命令会创建一个用户，但不会设置密码。用户可以通过其他认证方法（如 SSH 密钥）登录。

5. **指定用户的默认 shell**

   你可以使用 `--shell` 选项为用户指定默认 shell：

   ```bash
   sudo adduser <username> --shell /bin/bash
   ```

   例如，指定 `alice` 使用 `/bin/zsh` 作为默认 shell：`sudo adduser alice --shell /bin/zsh`。

6. **使用特定的用户 ID 和组 ID**

   通过 `--uid` 和 `--gid` 选项，可以分别指定用户的 UID（用户 ID）和 GID（组 ID）。通常不需要指定这些选项，但如果需要与其他系统共享用户或组 ID，则可以使用这些选项：

   ```bash
   sudo adduser <username> --uid 1234 --gid 5678
   ```

7. **创建系统用户**

   你可以通过 `--system` 选项创建一个系统用户。系统用户通常用于运行系统服务和进程，通常不需要登录权限：

   ```bash
   sudo adduser --system <username>
   ```

   例如，创建一个名为 `myservice` 的系统用户：`sudo adduser --system myservice`。

8. **删除用户**

   `adduser` 命令本身并没有直接删除用户的选项，删除用户时需要使用 `deluser` 命令。要删除 `alice` 用户，可以使用：

   ```bash
   sudo deluser alice
   ```

9. **删除用户及其家目录**

   如果想要在删除用户时一起删除其家目录，可以使用 `--remove-home` 选项：

   ```bash
   sudo deluser --remove-home alice
   ```

**总结：**

`adduser` 是一个创建新用户的命令，通常比 `useradd` 更加友好。它会交互式地要求你设置用户的密码、全名等，并自动执行一些任务（如创建家目录和设置默认 shell）。常用选项包括：

- `--ingroup <group>`：指定用户所在的组。
- `--home <path>`：指定用户的家目录。
- `--disabled-password`：创建没有密码的用户。
- `--shell <shell>`：指定用户的默认 shell。
- `--system`：创建系统用户。

这些选项使得 `adduser` 成为一个非常方便的命令来管理用户账户。

## 新建账户 - root 同权限

在 Ubuntu 中，您可以通过以下步骤创建一个具有与 `root` 相同权限的新账户：

1. **打开终端**：首先，打开一个终端窗口。

2. **创建一个新用户**： 使用 `adduser` 命令创建一个新用户。替换 `<username>` 为您希望创建的用户名：

   ```bash
   sudo adduser <username>
   ```

   该命令会提示您输入用户的密码、姓名等信息，可以按需要填写，或者直接按回车跳过。

3. **将新用户添加到 `sudo` 组**： 要让新用户具有与 `root` 相同的权限，需要将该用户添加到 `sudo` 组中。运行以下命令：

   ```bash
   sudo usermod -aG sudo <username>
   ```

4. **确认新用户是否具有 `sudo` 权限**： 切换到新用户并验证权限：

   ```bash
   su - <username>
   sudo whoami
   ```

   如果返回 `root`，则表示新用户具有 `root` 权限。

5. **完成**：现在，新账户就有了与 `root` 相同的权限。

## 新用户默认信息

在 Linux 系统中，使用 `useradd` 命令创建一个新用户时，会有一些默认的设置。这些默认设置会根据不同的发行版有所变化，但通常情况下，以下是大多数 Linux 系统的默认值。

1. **默认组 (Primary Group)**

   - 默认情况下，新用户的主组会与用户名相同。这意味着如果你创建一个名为 `alice` 的新用户，系统会自动为该用户创建一个名为 `alice` 的主组，并将该用户添加到该组。

     ```bash
     sudo useradd alice
     ```

     这会创建一个用户名为 `alice` 的用户，并将其主组设置为 `alice`。

   - 如果你希望将用户添加到其他组，可以使用 `-g` 选项来指定主组，或者使用 `-G` 来指定附加组。

2. **默认家目录 (Home Directory)**

   - 默认情况下，新用户的家目录位于 `/home/用户名` 下。如果你创建用户 `alice`，那么家目录的默认路径是 `/home/alice`。

   - 如果你希望将用户的家目录设置为其他位置，可以使用 `-d` 选项来指定目录路径。

     ```bash
     sudo useradd -d /data/alice alice
     ```

     这会将用户 `alice` 的家目录设置为 `/data/alice`。

   - 如果指定了 `-m` 选项（通常会自动使用），系统会自动创建该目录。如果没有指定 `-m`，则不会自动创建家目录。

3. **默认登录 Shell**

   - 默认情况下，用户的登录 shell 通常是 `/bin/bash`，这是大多数 Linux 系统中的默认 shell。

   - 如果你希望指定其他的登录 shell，可以使用 `-s` 选项。例如，如果你想为用户 `alice` 设置 `zsh` 作为登录 shell，可以这样做：

     ```bash
     sudo useradd -s /bin/zsh alice
     ```

4. **默认密码**

   - 默认情况下，新用户不会设置密码，用户必须通过 `passwd` 命令设置密码。你可以为新用户指定一个初始密码：

     ```bash
     sudo passwd alice
     ```

     然后输入密码。

5. **默认用户 ID 和组 ID**

   - 系统会为新用户分配一个唯一的用户 ID（UID）和组 ID（GID）。这些 ID 会自动分配，通常从系统中空闲的最小值开始。UID 和 GID 是系统内部用来标识用户和组的唯一数字标识。

6. **默认账户过期**

   - 默认情况下，新用户账户没有过期日期。你可以使用 `-e` 选项来指定过期日期。例如：

     ```bash
     sudo useradd -e 2025-12-31 alice
     ```

     这会将用户的账户设置为在 2025 年 12 月 31 日过期。

7. **默认用户目录权限**

   - 默认情况下，新用户的家目录权限为 `755`，即用户对家目录有完全权限，而其他人只能读取和执行该目录。

8. **默认附加组**

   - 默认情况下，新用户只会被添加到其主组中（即与用户名相同的组），没有其他附加组。如果你希望将新用户添加到其他组，可以使用 `-G` 选项。

     ```bash
     sudo useradd -G sudo,adm alice
     ```

     这会将用户 `alice` 添加到 `sudo` 和 `adm` 附加组中。

9. **默认用户账户锁定状态**

   - 默认情况下，新创建的用户账户是解锁的。用户可以立即登录。如果你希望禁用账户，可以在创建用户时使用 `-L` 选项来锁定账户，或者创建后使用 `passwd -l <username>` 来锁定用户。

10. **默认登录限制**

    - 默认情况下，用户可以在任何时间登录。如果你希望为用户设置登录时间限制（例如，仅允许在特定时间段内登录），可以使用 `-e` 或 `-f` 选项来设置限制。

11. **默认环境变量**

    - 新创建的用户将继承系统默认的环境变量设置，如 `PATH` 等。这些设置通常在 `/etc/profile` 或 `/etc/bash.bashrc` 中定义。

12. **默认用户的 umask 设置**

    - `umask` 是一种控制文件和目录默认权限的机制。新创建的用户通常会继承 `/etc/profile` 中定义的默认 `umask` 值，通常是 `022`，这意味着创建的新文件会具有 `644` 权限（用户读写，组和其他用户只读），目录会具有 `755` 权限。

**总结：**

当你创建一个新用户时，通常会得到以下默认设置：

- **默认主组**：与用户名相同。
- **默认家目录**：`/home/<username>`。
- **默认登录 shell**：`/bin/bash`。
- **默认密码**：用户没有密码，必须使用 `passwd` 设置。
- **默认 UID 和 GID**：由系统自动分配。
- **默认附加组**：无（只属于主组）。
- **默认账户状态**：解锁状态，可以立即登录。

这些默认设置可以通过 `useradd` 命令的选项进行定制化。

## 查看用户

在 Linux 系统中，有几种方法可以查看当前系统上有哪些用户：

1. **查看 `/etc/passwd` 文件**

   - 系统中的所有用户信息（包括用户名、UID、GID、用户的家目录、默认 shell 等）都存储在 `/etc/passwd` 文件中。
   - 可以使用 `cat`、`less` 或 `grep` 等命令查看该文件：

     ```bash
     cat /etc/passwd
     ```

     `/etc/passwd` 文件中的每一行代表一个用户，字段之间使用冒号（:）分隔，结构如下：

     ```bash
     username:password:UID:GID:comment:home_directory:shell
     ```

   - 其中：
     - `username`：用户名。
     - `password`：通常是一个占位符（在现代系统中，密码通常存储在 `/etc/shadow` 文件中）。
     - `UID`：用户 ID。
     - `GID`：组 ID。
     - `comment`：通常是用户的全名或描述信息。
     - `home_directory`：用户的家目录。
     - `shell`：用户的默认 shell。

2. **使用 `getent` 命令**

   `getent` 命令用于查询系统的各种数据库，包括用户数据库。它从 `/etc/passwd` 获取信息，但也可以查询其他来源，如 LDAP 或 NIS（如果系统配置了这些）。

   ```bash
   getent passwd
   ```

   这会列出所有用户，包括系统用户和普通用户。输出的格式与 `/etc/passwd` 文件相同。

3. **查看当前登录的用户**

   如果你只关心当前登录的用户，可以使用以下命令：

   ```bash
   who
   ```

   这些命令会列出当前正在登录的用户及其会话信息。

4. **查看系统组信息**

如果你也想查看系统中的所有组（有时用户会加入多个组），可以查看 `/etc/group` 文件：

```bash
cat /etc/group
```

**总结：**

- **查看所有用户**：使用 `cat /etc/passwd` 或 `getent passwd`。
- **列出用户名**：使用 `cut -d: -f1 /etc/passwd`。
- **查看当前登录的用户**：使用 `who` 或 `w`。

通过这些方法，你可以轻松查看计算机上的所有用户及其相关信息。

## 查看组

要查看 Linux 系统中有哪些组，可以使用以下几种方法：

1. **查看 `/etc/group` 文件**

   - 系统中所有的用户组信息都存储在 `/etc/group` 文件中。可以使用 `cat`、`less` 或 `grep` 等命令查看该文件。

     ```bash
     cat /etc/group
     ```

     每一行代表一个组，字段之间使用冒号（:）分隔，结构如下：

     ```bash
     groupname:password:GID:user_list
     ```

   - 其中：
     - `groupname`：组名。
     - `password`：组密码（通常为空或占位符）。
     - `GID`：组 ID。
     - `user_list`：属于该组的用户（用户名之间用逗号分隔）。

2. **使用 `getent` 命令**

   `getent` 命令可以从系统的各种数据库中查询信息，包括组信息。它会从 `/etc/group` 或其他配置了的源（如 LDAP 或 NIS）中获取组信息。

   ```bash
   getent group
   ```

   这会列出所有组及其相关信息。

3. **查看当前用户的组**

   如果你想查看某个特定用户属于哪些组，可以使用 `groups` 命令。这个命令会列出当前用户或指定用户所在的所有组。

   ```bash
   groups <username>
   ```

   如果不指定用户名，它会列出当前登录用户所在的所有组。

4. **查看当前系统的组和成员**

   你可以使用 `getent group` 命令结合 `grep` 来查找特定的组和组成员：

   ```bash
   getent group | grep <groupname>
   ```

   例如，查看 `sudo` 组的成员：

   ```bash
   getent group | grep sudo
   ```

**总结：**

- **查看所有组**：使用 `cat /etc/group` 或 `getent group`。
- **列出所有组名**：使用 `cut -d: -f1 /etc/group`。
- **查看当前用户所在组**：使用 `groups` 命令。
- **查看特定组信息**：使用 `getent group | grep <groupname>`。

这些方法可以帮助你快速查看和管理系统中的组信息。

## usermod 命令

`usermod` 是 Linux 系统中的一个命令，用于修改现有用户的属性。它允许你更改用户的各种设置，例如**用户名、用户组、用户的家目录、登录 shell 等**。以下是 `usermod` 命令的一些常见用法和选项。

**基本语法：**

```bash
usermod [选项] <用户名>
```

**常见选项：**

1. **`-aG`** (Add to Groups)

   - 这个选项用于将用户添加到一个或多个附加组中，而不会从原有的组中移除该用户。使用时要指定组名。

     ```bash
     sudo usermod -aG sudo <username>
     ```

     这会将用户 `<username>` 添加到 `sudo` 组中。

2. **`-d`** (Home Directory)

   - 用于更改用户的家目录。`-d` 后面跟新的家目录路径。

     ```bash
     sudo usermod -d /home/newhome <username>
     ```

     这会将用户的家目录更改为 `/home/newhome`。

3. **`-m`** (Move the Home Directory)

   - 这个选项与 `-d` 一起使用，它会把旧的家目录内容移动到新的目录。必须同时指定 `-d` 和新目录路径。

     ```bash
     sudo usermod -d /home/newhome -m <username>
     ```

     这会将用户的家目录移动到 `/home/newhome`，并将所有文件从旧目录迁移过去。

4. **`-l`** (Login Name)

   - 用于更改用户的登录名。

     ```bash
     sudo usermod -l newname oldname
     ```

     这会将用户名 `oldname` 更改为 `newname`。

5. **`-g`** (Primary Group)

   - 用于更改用户的主组。该组将成为用户的默认组。

     ```bash
     sudo usermod -g newgroup <username>
     ```

     这会将用户的主组更改为 `newgroup`。

6. **`-G`** (Supplementary Groups)

   - 用于指定一个或多个附加组。与 `-aG` 不同，使用 `-G` 时会替换用户的附加组，而不是追加。

     ```bash
     sudo usermod -G group1,group2 <username>
     ```

     这会将用户 `<username>` 的附加组更改为 `group1` 和 `group2`。

7. **`-s`** (Shell)

   - 用于更改用户的登录 shell。

     ```bash
     sudo usermod -s /bin/zsh <username>
     ```

     这会将用户的默认 shell 更改为 `zsh`。

8. **`-e`** (Expire Date)

   - 用于设置用户帐户的过期日期，格式为 `YYYY-MM-DD`。过期日期之后，用户将无法登录。

     ```bash
     sudo usermod -e 2025-12-31 <username>
     ```

     这会将用户的帐户设置为在 2025 年 12 月 31 日过期。

9. **`-f`** (Inactive)

   - 用于指定用户账户的非活动期，即账户在登录失败后的多少天将被禁用。

     ```bash
     sudo usermod -f 30 <username>
     ```

     这会设置用户在 30 天未活动后账户将被禁用。

10. **`-p`** (Password)

    - 用于更改用户的密码。通常这个选项配合一个加密的密码（使用 `openssl` 或其他工具加密）一起使用。

      ```bash
      sudo usermod -p '$6$rounds=656000$...' <username>
      ```

      这会将用户 `<username>` 的密码更改为给定的加密密码。

**注意事项：**

- 必须以 root 或具有适当权限的用户身份执行 `usermod` 命令。
- 如果更改了用户名或用户的主目录，用户可能需要重新登录，以确保所有更改生效。
- 使用 `-aG` 时非常重要，因为如果不加 `-a`，会替换用户原有的附加组，导致用户失去访问权限。

**示例：**

1. **将用户添加到多个组**：

   ```bash
   sudo usermod -aG sudo,adm <username>
   ```

   这将用户 `<username>` 添加到 `sudo` 和 `adm` 组中，保留该用户原本的其他组。

2. **更改用户登录 shell**：

   ```bash
   sudo usermod -s /bin/bash <username>
   ```

   这将用户 `<username>` 的默认 shell 更改为 `bash`。

3. **更改用户的家目录并迁移文件**：

   ```bash
   sudo usermod -d /home/newhome -m <username>
   ```

   这将用户 `<username>` 的家目录更改为 `/home/newhome`，并将所有旧目录中的文件迁移到新目录。

## passwd 命令

`passwd` 是一个 Linux 系统中的命令，用于更改用户密码。该命令既可以用来为新用户**设置密码**，也可以**修改**现有用户的密码。管理员可以使用 `passwd` 来管理系统中的用户密码。

**基本语法：**

```bash
passwd [选项] [用户名]
```

- **选项**：可以用来修改 `passwd` 命令的行为。
- **用户名**：指定要更改密码的用户，如果不指定用户名，则默认更改当前用户的密码。

**常见用法和选项**

1. **修改当前用户密码**

   如果你不指定用户名，`passwd` 命令将更改当前登录用户的密码。执行命令后，系统会提示输入当前密码和新密码。

   ```bash
   passwd
   ```

   这会要求你输入当前密码，然后输入两次新密码。

2. **为指定用户设置密码**

   作为管理员（root 用户）或具有 `sudo` 权限的用户，可以为其他用户设置或修改密码。

   ```bash
   sudo passwd <username>
   ```

   这会为指定的用户 `<username>` 设置或更改密码。系统会要求输入新密码，并确认密码。

3. **禁用用户密码**

   禁用用户的密码，使其无法通过密码登录。你可以使用 `-l` 选项来锁定用户密码。

   ```bash
   sudo passwd -l <username>
   ```

   锁定用户的密码后，该用户将无法通过传统的密码身份验证登录。**但仍可通过其他认证方法（如 SSH 密钥）登录**。

4. **解锁用户密码**

   如果一个用户的密码被锁定（例如通过 `passwd -l` 锁定），你可以使用 `-u` 选项来解锁用户的密码：

   ```bash
   sudo passwd -u <username>
   ```

   这将解锁指定用户的密码，使其能够重新使用密码登录。

5. **删除用户密码**

   `passwd` 命令提供了 `-d` 选项，用来删除用户的密码，这样用户就没有密码了，从而可以通过其他方式登录（例如使用 SSH 密钥认证）。

   ```bash
   sudo passwd -d <username>
   ```

   这条命令会删除 `<username>` 用户的密码，使其无法通过密码进行登录。

6. **设置空密码（无密码登录）**

   通过修改 `/etc/shadow` 文件，你也可以手动删除密码哈希值，使得用户密码为空。

   1. 打开 `/etc/shadow` 文件：

      ```bash
      sudo nano /etc/shadow
      ```

   2. 找到目标用户的行，例如：

      ```log
      alice:$6$abc123$abcdefg:18344:0:99999:7:::
      ```

   3. 删除密码哈希（即冒号和 `$` 符号之间的内容），使该行变为空密码：

      ```log
      alice::18344:0:99999:7:::
      ```

   4. 保存文件并退出。

   这种方法会使用户 `alice` 没有密码，从而可以进行无密码登录。

7. **强制用户下次登录时修改密码**

   你可以使用 `-e` 选项强制用户下次登录时修改密码：

   ```bash
   sudo passwd -e <username>
   ```

   这将使得用户下次登录时必须输入新密码。

8. **设置密码过期时间**

   `passwd` 命令还可以用来设置用户密码的过期时间。使用 `-x` 选项可以设置密码的最大使用期限，超过这个时间，用户必须修改密码。

   ```bash
   sudo passwd -x <days> <username>
   ```

   其中 `<days>` 是密码的最大有效天数。例如，如果设置为 `30`，那么用户的密码在 30 天后将过期，必须重新设置。

9. **设置密码最小使用期限**

   你可以设置密码修改后用户必须等待的最小天数才能再次更改密码。使用 `-n` 选项来设置最小使用期限：

   ```bash
   sudo passwd -n <days> <username>
   ```

   例如，如果设置为 `7`，用户必须等待 7 天才能再次修改密码。

10. **设置密码警告天数**

    `-w` 选项可以设置密码过期前的警告天数。在密码到期之前，系统会提醒用户修改密码。

    ```bash
    sudo passwd -w <days> <username>
    ```

    例如，设置为 `7` 表示在密码到期前 7 天开始警告用户。

11. **查看密码过期信息**

    使用 `chage` 命令可以查看用户密码的过期信息，虽然 `passwd` 命令本身不直接提供查看过期信息的功能。

**总结：**

- **新建用户**：使用 `sudo useradd <username>` 创建新用户。
- **设置用户密码**：使用 `sudo passwd <username>` 设置密码。
- **修改密码**：同样使用 `sudo passwd <username>` 修改密码。
- **禁用用户密码**：使用 `sudo passwd -l <username>` 锁定用户密码。
- **解锁用户密码**：使用 `sudo passwd -u <username>` 解锁密码。
- **强制用户下次修改密码**：使用 `sudo passwd -e <username>` 强制更改密码。

## chown 命令

`chown` 是 Linux 中用于更改文件或目录 **所有者**（user）和/或 **所属组**（group）的命令。该命令常用于权限管理，确保某些用户或组可以访问和操作指定文件或目录。

**一、基本语法**

```bash
chown [选项] 用户[:用户组] 文件/目录
```

- `用户`：新文件拥有者。
- `用户组`：新所属用户组，可选。
- 文件/目录：要操作的目标对象。

**二、常用示例**

1. **更改文件拥有者**

   ```bash
   sudo chown alice file.txt
   ```

   将 `file.txt` 的拥有者改为用户 `alice`，用户组保持不变。

2. **更改文件拥有者和所属组**

   ```bash
   sudo chown alice:developers file.txt
   ```

   将 `file.txt` 的拥有者改为 `alice`，所属用户组改为 `developers`。

3. **只更改所属组**

   ```bash
   sudo chown :developers file.txt
   ```

   拥有者不变，只将文件的用户组改为 `developers`。

4. **递归更改目录及其内部所有文件/子目录的所有者**

   ```bash
   sudo chown -R alice:developers /data/share
   ```

   使用 `-R`（`--recursive`） 选项可以递归更改整个目录树的拥有者和组。

5. **使用 UID 和 GID 更改**

   ```bash
   sudo chown 1001:1002 file.txt
   ```

   将文件所有者和组设置为对应的 UID 和 GID。

**三、常用选项**

| 选项                 | 说明                                                     |
| -------------------- | -------------------------------------------------------- |
| `-R`                 | 递归地更改目录及其中所有文件和子目录的拥有者/用户组。    |
| `-f`                 | 忽略错误信息，不显示警告。                               |
| `-v`                 | 显示处理信息，输出详细更改内容。                         |
| `--from=旧用户:旧组` | 仅当文件当前的拥有者和组匹配时才更改（常用于安全脚本）。 |

你可以使用 `ls -l` 来查看文件所有者和用户组：

```bash
ls -l file.txt

# 示例输出：
-rw-r--r-- 1 alice developers  1234 Jun 5 12:34 file.txt
其中：

- `alice` 是文件拥有者。
- `developers` 是所属用户组。
```

**四、注意事项**

- 修改所有权通常需要超级用户权限（使用 `sudo`）。
- `chown` 无法用于普通用户修改他们无权访问的文件。
- 更改系统关键文件的拥有者可能导致系统异常，请谨慎使用。

## chmod 命令

`chmod`（**change mode**）是 Linux 和类 Unix 系统中用于更改文件或目录的权限的命令。它允许你为文件的**所有者（owner）**、**所属组（group）** 和 **其他用户（others）** 指定读、写和执行权限。

**一、文件权限基础知识**

Linux 中每个文件或目录都关联着三类用户的权限：

| 权限字符 | 含义               | 数值表示 |
| -------- | ------------------ | -------- |
| r        | 读权限 (read)      | 4        |
| w        | 写权限 (write)     | 2        |
| x        | 执行权限 (execute) | 1        |
| -        | 无权限             | 0        |

三类用户：

| 类别 | 含义               |
| ---- | ------------------ |
| u    | 用户（user/owner） |
| g    | 组用户（group）    |
| o    | 其他用户（others） |
| a    | 所有用户（u+g+o）  |

**二、chmod 的两种用法**

1. 数字法（八进制表示）

   ```bash
   chmod 755 filename
   ```

   - `7` = 4 + 2 + 1（rwx）
   - `5` = 4 + 0 + 1（r-x）
   - `5` = 4 + 0 + 1（r-x）

   > 等价于：`rwxr-xr-x`

   典型数字权限：

   | 命令             | 权限说明                 | 权限字符串形式 |
   | ---------------- | ------------------------ | -------------- |
   | `chmod 777 file` | 所有人可读写执行         | `rwxrwxrwx`    |
   | `chmod 755 file` | 所有者 rwx，其他人 rx    | `rwxr-xr-x`    |
   | `chmod 700 file` | 仅所有者可读写执行       | `rwx------`    |
   | `chmod 644 file` | 所有者 rw，其他人 r      | `rw-r--r--`    |
   | `chmod 600 file` | 所有者可读写，其他无权限 | `rw-------`    |
   | `chmod 444 file` | 所有人只读               | `r--r--r--`    |
   | `chmod 000 file` | 所有人无任何权限         | `----------`   |

2. 符号法（字母+操作符）

   ```bash
   chmod [who][operator][permission] filename
   ```

   - `who`：u / g / o / a
   - `operator`：+ 增加、- 删除、= 赋值
   - `permission`：r / w / x

   **添加权限**

   | 命令                  | 含义                   |
   | --------------------- | ---------------------- |
   | `chmod u+x file`      | 给所有者添加执行权限   |
   | `chmod g+w file`      | 给所属组添加写权限     |
   | `chmod o+r file`      | 给其他用户添加读权限   |
   | `chmod a+x script.sh` | 给所有用户添加执行权限 |

   **移除权限**

   | 命令              | 含义                   |
   | ----------------- | ---------------------- |
   | `chmod u-w file`  | 删除所有者写权限       |
   | `chmod go-r file` | 删除组和其他用户读权限 |
   | `chmod a-x file`  | 所有人删除执行权限     |

   **设置为特定权限（覆盖）**

   | 命令              | 含义                 |
   | ----------------- | -------------------- |
   | `chmod u=r file`  | 所有者设为只读       |
   | `chmod g=rw file` | 所属组设为可读写     |
   | `chmod o= file`   | 清除其他用户所有权限 |
   | `chmod a=r file`  | 所有人只读           |

**三、递归修改权限（目录及其所有子文件）**

```bash
chmod -R 755 mydir
```

> 递归更改 `mydir` 及其所有子目录/文件的权限。

**四、目录权限相关**

- 目录的执行权限 `x` 表示是否能进入该目录
- 读权限 `r` 表示是否能列出目录内容
- 写权限 `w` 表示是否能在目录中创建或删除文件

| 命令                | 含义                              |
| ------------------- | --------------------------------- |
| `chmod 755 dir/`    | 目录所有者可写，其他用户可访问    |
| `chmod a+rx dir/`   | 所有人可进入并列出目录内容        |
| `chmod -R 755 dir/` | 递归设置目录及其子文件为 755 权限 |

**五、实用建议**

| 场景                       | 建议权限            |
| -------------------------- | ------------------- |
| 可执行脚本 `.sh` 文件      | `chmod 755`         |
| 配置文件 `.conf`, `.json`  | `chmod 644`         |
| 私密数据（仅限本人使用）   | `chmod 600`         |
| 网站根目录 `/var/www`      | `chmod -R 755`      |
| 临时上传目录 `/tmp/upload` | `chmod 777`（慎用） |
