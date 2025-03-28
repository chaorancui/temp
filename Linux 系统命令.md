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

在 Ubuntu 24.04 之前，Ubuntu 的软件源配置文件使用传统的 One-Line-Style，路径为 `/etc/apt/sources.list`；
从 Ubuntu 24.04 开始，Ubuntu 的软件源配置文件变更为 DEB822 格式，路径为 `/etc/apt/sources.list.d/ubuntu.source`。

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

`systemctl` 是 Linux 系统中用于与 **systemd** 系统和服务管理器交互的命令行工具。`systemd` 是现代 Linux 发行版（如 Ubuntu、CentOS、Debian 和 Fedora 等）中用于初始化系统和管理系统服务的核心组件。通过 `systemctl`，你可以管理和控制系统的服务、守护进程、系统状态等。

**列出所有 service**：

```shell
systemctl list-units --type=service
systemctl --type=service
```

**常用命令**，ssh 服务为例：

```bash
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

**其他命令**：

```bash
# 重新加载服务配置，某些服务（例如 Nginx、Apache）支持在不完全重启服务的情况下重新加载配置
sudo systemctl reload <service_name>

# 查看日志
# 查看特定服务的日志输出，通常通过 journalctl 配合 systemctl 使用
sudo journalctl -u <service_name>
```

## systemd 服务

`systemd` 是现代 Linux 系统中用来管理系统启动、服务管理、进程监控等任务的初始化系统和系统管理器。它是许多主流 Linux 发行版（如 Ubuntu、Fedora、Debian、CentOS 等）的默认系统和服务管理工具。

在传统的 Unix 系统中，使用的是老式的 SysVinit 系统来启动服务和管理进程，而 `systemd` 是一个现代化的替代方案，它解决了许多传统初始化系统的问题，提供了更高效、更强大的功能。

### 启动过程

`systemd` 在 Linux 系统启动时首先启动，并接管系统的初始化过程，取代了传统的 SysVinit。它通过 **并行化** 启动服务和处理任务，从而加速了系统的启动过程。与传统的线性启动方式不同，`systemd` 可以同时启动多个服务，提高了系统的启动效率。

### 主要组件和功能

1. Unit（单元）

   `systemd` 通过 **unit**（单元）管理系统的各类服务、挂载点、套接字等。每个单元有不同的类型，用于表示不同的任务或资源。例如：

   - **service unit**（服务单元）：用于管理后台服务进程（例如 HTTP 服务、数据库服务等）。
   - **mount unit**（挂载单元）：用于挂载文件系统。
   - **socket unit**（套接字单元）：用于处理网络通信或文件 I/O 等任务。
   - **target unit**（目标单元）：用于定义系统的运行级别，类似于传统的运行级别概念（例如，图形界面模式、多用户模式等）。

2. 并行启动

   传统的系统初始化使用串行启动，即服务依赖于前一个服务的启动，而 `systemd` 支持 **并行启动**，可以在没有相互依赖的情况下同时启动多个服务，显著提高了启动速度。

3. 依赖关系

   `systemd` 允许服务之间建立依赖关系，确保服务按照特定的顺序启动或停止。例如，一个 Web 服务器可能依赖于数据库服务，`systemd` 会确保数据库服务在 Web 服务器启动之前完成启动。

4. 日志管理（Journal）

   `systemd` 内置了日志系统，称为 **journal**，它能够收集和存储系统和服务的日志消息。与传统的日志文件不同，`journal` 将日志存储在二进制文件中，能够提供更强的查询功能。通过 `journalctl` 命令，用户可以轻松查看和分析系统日志。

5. 并发和依赖控制

   `systemd` 允许服务的启动、停止和重启依赖于其他服务的状态。例如，一个网络服务的启动可能依赖于网络接口的激活，`systemd` 会自动处理这些依赖关系。

6. 服务监控和自动重启

   `systemd` 提供了 **服务监控** 功能，可以检测服务是否崩溃或停止运行。如果服务失败，`systemd` 可以自动重启服务，确保系统的稳定性和可靠性。

7. 控制系统资源

   `systemd` 可以控制和管理服务的资源使用，例如，限制内存、CPU、磁盘 I/O 等资源的使用，从而避免某些服务占用过多资源导致系统不稳定。

8. **与传统 SysVinit 的对比**

   | 特性         | SysVinit                 | systemd                                |
   | ------------ | ------------------------ | -------------------------------------- |
   | 启动方式     | 串行启动                 | 并行启动                               |
   | 服务管理     | 基于脚本（/etc/init.d/） | 基于 unit 文件（/etc/systemd/system/） |
   | 服务依赖管理 | 不支持自动管理依赖关系   | 支持服务依赖自动管理                   |
   | 系统日志     | 单独的日志文件           | 集成的日志系统（journal）              |
   | 服务重启     | 手动配置                 | 支持自动重启服务                       |

### 常见命令和操作

使用 `systemd` 时，常用的命令包括：

- **启动服务**：`sudo systemctl start <service_name>`
- **停止服务**：`sudo systemctl stop <service_name>`
- **查看服务状态**：`sudo systemctl status <service_name>`
- **重启服务**：`sudo systemctl restart <service_name>`
- **启用服务（开机启动）**：`sudo systemctl enable <service_name>`
- **禁用服务（禁止开机启动）**：`sudo systemctl disable <service_name>`
- **查看日志**：`sudo journalctl -u <service_name>`

### systemd 的优势

- **快速启动**：并行化的服务启动显著缩短了系统启动时间。
- **精确的依赖管理**：服务可以按需自动启动和停止，避免不必要的依赖。
- **日志集成**：内置日志管理功能，简化了日志的存储和查看。
- **容错性**：支持自动重启崩溃的服务，确保系统稳定运行。
- **资源控制**：更好地控制每个服务的资源使用，防止某个服务影响整个系统的稳定性。

总结来说，`systemd` 是一个功能强大、灵活且高效的系统和服务管理工具，它提升了系统启动、服务管理、资源分配和日志管理的能力，逐步成为现代 Linux 系统的标准初始化系统。

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

## dig

`dig`（Domain Information Groper）是一个用于查询 DNS（域名系统）信息的命令行工具。在 Linux 和其他 Unix-like 系统中，`dig` 是最常用的 DNS 查询工具之一。它可以用于查询域名的各种信息，如 IP 地址、MX 记录、NS 记录等。

`dig` 提供了比传统的 `nslookup` 更强大和灵活的功能，支持更多的查询选项、查询类型以及更详细的输出。

1. **基本语法**

   ```bash
   dig [@server] [name] [type] [options]
   ```

   - `@server`：指定要查询的 DNS 服务器。默认情况下，`dig` 会查询系统配置的 DNS 服务器。
   - `name`：要查询的域名。
   - `type`：查询类型（例如，A、MX、NS 等）。如果不指定，默认查询 A 记录。
   - `options`：一些附加选项，用于修改查询的行为或输出。

2. **常见查询类型**

   以下是 `dig` 支持的一些常见查询类型：

   - **A**：查询 IPv4 地址（默认查询类型）。
   - **AAAA**：查询 IPv6 地址。
   - **MX**：查询邮件交换记录（Mail Exchange）。
   - **NS**：查询域名服务器记录（Name Server）。
   - **CNAME**：查询别名记录（Canonical Name）。
   - **SOA**：查询授权记录（Start of Authority）。
   - **PTR**：查询反向 DNS 查找记录。
   - **TXT**：查询文本记录，常用于域名验证或 SPF 配置。

3. **常用选项**

   - `+short`：仅显示简洁的输出（例如，只显示 IP 地址）。
   - `+trace`：显示 DNS 查询的完整跟踪路径，查看从根服务器到目标服务器的所有查询过程。
   - `+all`：显示所有相关信息，包括查询的每个步骤和每个 DNS 记录。
   - `+noall +answer`：仅显示答案部分，过滤掉不相关的信息。
   - `+ndots=<num>`：指定域名解析时要求的最小点数，默认是 1。

4. **基本用法**

   1. 查询 A/MX/NS/CNAME/TXT/PTR/SOA 记录

      ```bash
      dig example.com      # 查询某个域名的 A 记录（IPv4 地址），默认情况下，dig 会查询 A 记录
      dig example.com MX   # 查询域名的 MX 记录（邮件交换服务器）
      dig example.com NS   # 查询域名的 NS 记录（域名服务器）
      dig www.example.com CNAME  # 查询域名的 CNAME 记录（别名记录）
      dig example.com TXT        # 查询域名的 TXT 记录（文本记录）
      dig example.com A MX NS    # 可以在同一个命令中查询多个记录， 这将同时查询 A、MX 和 NS 记录。
      dig -x 8.8.8.8       # 反向查询某个 IP 地址对应的域名，这将查询 IP 地址 8.8.8.8 对应的域名
      dig example.com SOA  # 查询一个域名的授权记录（SOA）
      ```

   2. 查询指定的 DNS 服务器

      如果你想要指定某个 DNS 服务器来执行查询，可以使用 `@` 来指定：

      ```bash
      dig @8.8.8.8 example.com
      ```

      这会使用 Google 的公共 DNS 服务器 `8.8.8.8` 来查询 `example.com` 的 A 记录。

   3. 选项使用

      ```bash
      # +trace：使用 `+trace` 查看从根 DNS 服务器到目标服务器的查询路径，这会显示详细的查询过程，包括所有递归查询
      dig +trace example.com
      # +short：如果你只关心简洁的输出，可以使用 `+short` 选项，这只会输出 IP 地址或其他查询的简洁结果
      dig example.com +short
      # +noall +answer：如果你只想查看答案部分，可以使用 `+noall +answer`，这会过滤掉其他部分，仅显示查询的答案
      dig example.com +noall +answer
      ```

5. **输出示例**

   以查询 `example.com` 的 A 记录为例，执行 `dig example.com` 后的输出通常包括以下几部分：

   - **QUESTION SECTION**：显示查询的目标域名和查询类型。
   - **ANSWER SECTION**：显示查询的结果（例如，`example.com` 的 IP 地址）。
   - **AUTHORITY SECTION**：显示负责该域名的授权 DNS 服务器。
   - **ADDITIONAL SECTION**：可能会显示额外的相关信息。

6. **常见用途**

- **检查域名是否解析正常**：使用 `dig` 可以快速确认某个域名是否能够正确解析为 IP 地址。
- **诊断 DNS 问题**：当出现 DNS 问题时，`dig` 可帮助分析域名解析过程，确认 DNS 配置是否正确。
- **了解 DNS 记录**：你可以通过 `dig` 查询各类 DNS 记录，获取域名的详细配置信息。

**总结**：

`dig` 是一个非常强大的 DNS 查询工具，适用于从简单的域名解析查询到复杂的 DNS 配置分析。通过灵活的查询类型和选项，它可以帮助你全面了解 DNS 配置、调试 DNS 问题并进行网络故障排查。

# 程序分析命令

## ldd

(list dynamic dependencies)

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

> [Docs » 工具参考篇 » 18. scp 跨机远程拷贝](https://linuxtools-rst.readthedocs.io/zh-cn/latest/tool/scp.html)
> 帮助文档：`man scp`

scp 是 secure copy 的简写，用于在 Linux 下进行远程拷贝文件的命令，和它类似的命令有 cp，不过 cp 只是在本机进行拷贝不能跨服务器，而且 scp 传输是加密的。当你服务器硬盘变为只读 read only system 时，用 scp 可以帮你把文件移出来。

> :page_with_curl: **注解：**
> 类似的工具有 rsync；scp 消耗资源少，不会提高多少系统负荷，在这一点上，rsync 就远远不及它了。rsync 比 scp 会快一点，但当小文件多的情况下，rsync 会导致硬盘 I/O 非常高，而 scp 基本不影响系统正常使用。

**命令格式**：

```bash
scp [参数] [原路径] [目标路径]
```

**命令参数**：

- `-1` 强制 scp 命令使用协议 ssh1
- `-2` 强制 scp 命令使用协议 ssh2
- `-4` 强制 scp 命令只使用 IPv4 寻址
- `-6` 强制 scp 命令只使用 IPv6 寻址
- `-B` 使用批处理模式（传输过程中不询问传输口令或短语）
- `-C` 允许压缩。（将-C 标志传递给 ssh，从而打开压缩功能）
- `-p` 留原文件的修改时间，访问时间和访问权限。
- `-q` 不显示传输进度条。
- `-r` 递归复制整个目录。
- `-v` 详细方式显示输出。scp 和 ssh(1)会显示出整个过程的调试信息。这些信息用于调试连接，验证和配置问题。
- `-c` cipher 以 cipher 将数据传输进行加密，这个选项将直接传递给 ssh。
- `-F` ssh_config 指定一个替代的 ssh 配置文件，此参数直接传递给 ssh。
- `-i` identity_file 从指定文件中读取传输时使用的密钥文件，此参数直接传递给 ssh。
- `-l` limit 限定用户所能使用的带宽，以 Kbit/s 为单位。
- `-o` ssh_option 如果习惯于使用 ssh_config(5)中的参数传递方式，
- `-P` port 注意是大写的 P, port 是指定数据传输用到的端口号
- `-S` program 指定加密传输时所使用的程序。此程序必须能够理解 ssh(1)的选项。

**使用示例**：

1. **从本地拷贝文件到远程服务器**：

   ```bash
   scp /path/to/local/file username@remote_host:/path/to/remote/directory
   scp /path/to/local/file remote_host:/path/to/remote/directory

   # 例如，把本地的 `file.txt` 拷贝到远程服务器的 `/home/user/` 目录：
   scp file.txt user@192.168.1.10:/home/user/
   ```

   指定了用户名，命令执行后需要输入用户密码；如果不指定用户名，命令执行后需要输入用户名和密码；

2. **从远程服务器拷贝文件到本地**：

   ```bash
   scp username@remote_host:/path/to/remote/file /path/to/local/directory

   # 例如，从远程服务器的 `/home/user/` 目录下载 `file.txt` 到本地：
   scp user@192.168.1.10:/home/user/file.txt /path/to/local/directory
   ```

3. **递归拷贝目录**： 使用 `-r` 选项，可以拷贝整个目录：

   ```bash
   scp -r /path/to/local/directory username@remote_host:/path/to/remote/directory
   ```

4. **指定端口号**： 如果远程服务器的 SSH 服务运行在非标准端口（例如 10086），你可以通过 `-P` 选项指定端口：

   ```bash
   scp -P 10086 file.txt user@192.168.1.10:/home/user/
   ```

5. **使用 SSH 密钥文件**： 如果你需要使用 SSH 密钥进行认证，可以使用 `-i` 选项指定密钥文件：

   ```bash
   scp -i /path/to/private_key file.txt user@192.168.1.10:/home/user/
   ```

6. **显示详细信息**： 使用 `-v` 选项来查看详细的传输过程：

   ```bash
   scp -v file.txt user@192.168.1.10:/home/user/
   ```

7. **启用压缩**： 使用 `-C` 选项来启用压缩，以加快大文件的传输速度：

   ```bash
   scp -C largefile.zip user@192.168.1.10:/home/user/
   ```

`scp` 是一个非常方便且安全的工具，适用于快速传输文件。如果你有需要使用 SSH 协议进行文件传输的场景，`scp` 可以高效地帮助你完成工作。

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
PermitRootLogin yes  # 原文件为`PermitRootLogin without-password`，需要改成左边，没有就新增
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
