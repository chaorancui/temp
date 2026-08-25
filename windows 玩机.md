[toc]

# windows 玩机

## 系统相关记录

### 互换 Ctrl 和 Caps 键位

<https://www.cnblogs.com/CoolMark-blog/p/12317492.html>

<https://gist.github.com/joshschmelzle/5e88dabc71014d7427ff01bca3fed33d>

### 大文件探测清理

[快速清理 Windows 大文件，它比「老牌」更好用：WizTree | App +1](https://sspai.com/post/64363)

[WizTree 官网](https://diskanalyzer.com/download)

[删除 pagefile.sys 与 hiberfil.sys 释放 C 盘空间](https://pc.poppur.com/notebook/6661.html)

[是否所有 Memory.dmp 的文件都可以删除](https://answers.microsoft.com/zh-hans/windows/forum/all/%E6%98%AF%E5%90%A6%E6%89%80%E6%9C%89memorydmp/c1a1878f-ec69-4035-9233-311b71d699cc)

[Windows.edb 删除](https://zhuanlan.zhihu.com/p/507590692)

### WSL 安装与使用

<https://docs.eesast.com/docs/tools/wsl>

<https://juejin.cn/post/7024498662935904269>

更改默认安装的 Linux 发行版
<https://learn.microsoft.com/zh-cn/windows/wsl/install>

开始通过适用于 Linux 的 Windows 子系统使用 Visual Studio Code
<https://learn.microsoft.com/zh-cn/windows/wsl/tutorials/wsl-vscode>

### ssh 到 wsl

一、最常用：Windows 本机 SSH 到 WSL（推荐）

> **同一台 Windows 机器**，这是 90% 场景

1. 确保 WSL 内 sshd 已启动

   在 **WSL 里**：

   ```bash
   sudo apt install -y openssh-server
   sudo service ssh start
   ```

   确认监听：

   ```bash
   ss -lnpt | grep sshd
   ```

   必须看到 `:22`

   ***

2. Windows → WSL（localhost）

   在 **Windows PowerShell / CMD**：

   ```bash
   ssh <用户名>@localhost
   ```

   例如：

   ```bash
   ssh cui@localhost
   ```

   ✅ 原因说明（很关键）：
   - WSL2 会**自动把 Linux 的端口映射到 Windows 的 localhost**
   - **不需要知道 WSL 的 IP**
   - 前提：`sshd` 监听 `0.0.0.0:22`

二、从局域网其他机器 SSH 到 WSL

> ⚠️ **WSL2 是 NAT 虚拟机，不能直接用 WSL IP**

方案 A(推荐方案)：端口转发（稳定）

1. 查 WSL IP（WSL 内）

   ```bash
   ip addr show eth0
   ```

   例如：

   ```bash
   172.29.88.101
   ```

2. Windows 设置端口转发（管理员 PowerShell）

   ```bash
   netsh interface portproxy add v4tov4 `
     listenaddress=0.0.0.0 listenport=2222 `
     connectaddress=172.29.88.101 connectport=22
   ```

3. 局域网访问

   ```bash
   ssh <用户名>@<Windows_IP> -p 2222
   ```

方案 B（不推荐）：直接连 WSL IP

```bash
ssh user@172.29.88.101
```

❌ 缺点：

- WSL IP **每次重启都会变**
- 防火墙经常拦

### win11 修改蓝牙设备的名称教程

<https://zhuanlan.zhihu.com/p/625885504>

### 安装字体

下面是安装或管理字体的两种方法：

- 所有字体都存储在 `C:\Windows\Fonts` 文件夹中。 （可选）只需将字体文件从提取的文件文件夹拖动到此文件夹中即可添加字体。 然后，Windows 会自动安装它们。 若要查看字体的外观，请打开“字体”文件夹，右键单击字体文件，然后选择“预览”。

- 还可以通过控制面板查看已安装的字体。 根据你的 Windows 版本，你将转到**控制面板** > **字体** -- 或 - **控制面板** > **外观和个性化** > **字体**。

## OpenSSH 服务

### 开启 OpenSSH 服务

在 Windows 10 和 Windows 11 上开启 OpenSSH 服务，主要有两种方法：**图形界面**和**命令行**。如果你的系统版本在 Windows 10 1809 及以上，就已经内置了 OpenSSH 服务。

**安装方式：**

1. 方法一：通过图形界面安装（适合不熟悉命令行的用户）
   1. **打开设置**：按 `Win + I` 键打开"设置"。
   2. **进入可选功能**：点击"**应用**" -> "**可选功能**"。
   3. **添加可选功能**：在"可选功能"页面，点击"**添加可选功能**"（Win11 后面会显示"查看功能"）。
   4. **安装服务**：在列表中找到"**OpenSSH 服务器**"（OpenSSH Server），勾选并点击"**安装**"（或"添加"）。

2. 方法二：通过 PowerShell 命令行安装（推荐）

   这个方法更快捷，不容易卡顿。
   1. **以管理员身份运行 PowerShell**：右键点击"开始"菜单，选择"**Windows PowerShell (管理员)**"或"**终端 (管理员)**"。
   2. **安装 OpenSSH 服务器**：在窗口中输入以下命令并按回车：

      ```powershell
      Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
      ```

3. 方法三：离线安装（使用第三方编译的安装包）

   可以使用由 PowerShell 团队在 GitHub 上维护的 Windows 版 OpenSSH。
   1. **下载安装包**：访问 [**PowerShell/Win32-OpenSSH**](https://github.com/PowerShell/Win32-OpenSSH/releases) 的GitHub发布页面。

   2. **选择文件**：根据你的系统位数，下载对应的 `.msi` 安装包文件或 `.zip` 压缩包。
      - **对于 `.msi` 文件**：直接双击运行，按照向导提示完成安装即可。
      - **对于 `.zip` 压缩包**：
        - 将压缩包解压到一个目录，例如 `C:\Program Files\OpenSSH`。
        - 以**管理员身份**打开PowerShell，并切换到该目录，然后执行安装脚本：

          ```powershell
          cd "C:\Program Files\OpenSSH"
          .\install-sshd.ps1
          ```

          (如果遇到执行策略错误，可先运行 `powershell.exe -ExecutionPolicy Bypass -File install-sshd.ps1`)

**安装后的验证与配置：**

无论通过哪种方式安装，后续的启动和配置步骤都是一样的。

1. **启动SSH服务并设置为开机自启**（以管理员身份在PowerShell中执行）：

   ```powershell
   # 启动服务
   Start-Service sshd
   # 检查服务状态 Running 说明启动成功
   Get-Service sshd
   # 设置开机自启
   Set-Service -Name sshd -StartupType 'Automatic'
   ```

2. **检查防火墙规则**：确保防火墙允许TCP端口22的入站连接。可以执行以下命令来创建规则（如果已存在可跳过）：

   ```powershell
   New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
   ```

完成以上步骤后，你就可以从Linux系统通过 `ssh 用户名@IP地址` 的方式连接到你的Windows电脑了。

如果安装后还是有问题，可以检查一下事件查看器里的“Windows日志” -> “应用程序”和“系统”，看看有没有相关的错误记录。

### SSH 服务配置文件

配置文件位于 `C:\ProgramData\ssh\sshd_config`（注意 `ProgramData` 是隐藏文件夹）。
**以管理员身份**用记事本打开该文件，重点检查以下几项：

```conf
# 确保允许密码认证
PasswordAuthentication yes

# 确保不允许空密码（默认 no，不用改）
PermitEmptyPassword no

# 如果启用了公钥认证，暂时可以先不管，但下面这条要确保没有把密码认证禁用
PubkeyAuthentication yes   # 可保留，不影响密码登录

# 检查是否有 AllowUsers 或 DenyUsers 指令
# 如果有 AllowUsers，必须明确包含 c00619335，例如：
AllowUsers c00619335
# 如果有 DenyUsers，确保没有包含该用户
```

**修改后保存文件，然后重启 sshd 服务**（在 PowerShell 管理员下执行）：

```powershell
Restart-Service sshd
```

### Windows 使用 sshpass

如果需要在 Windows 本机上直接使用 `sshpass`，可以安装第三方移植版本。

1. **通过 `winget` 安装**（推荐）：

   ```powershell
   winget install xhcoding.sshpass-win32
   ```

2. **通过 `scoop` 安装**：

   ```powershell
   scoop install sshpass
   ```

安装后，在 Windows 的命令行或 PowerShell 中，用法与 Linux 下类似。例如：

```powershell
sshpass -p '密码' ssh 用户名@主机
```

## 日常使用问题

### 文件夹无法删除

> 参考链接：[操作无法完成，因为其中的文件，或文件夹已在另一个程序中打开](https://answers.microsoft.com/zh-hans/windows/forum/all/%E6%93%8D%E4%BD%9C%E6%97%A0%E6%B3%95%E5%AE%8C/0ebfe72e-274a-4dca-ac59-e1aeb7f97440)

1. 按 `Win + S` 键搜索 【**资源监视器**】 并打开;
2. 点击窗口上的 【**CPU**】 标签;
3. 点击下方 “关联的句柄” 右侧的**搜索框输入要删除文件夹的名称或完整路径** (例如 C:\Users\App\Local);
4. 接着下面的搜索结果列表中，会看到**正在使用该文件夹的程序**;
5. 然后右键选择**结束进程**就可以了。

### 你需要来自 XXX 的权限才能对此文件进行更改

<https://zhuanlan.zhihu.com/p/82036101>

### CMD

在 CMD 中查看系统环境变量的指令为（该指令还可以在不重启系统的情况下更新环境变量）：

```cmd
echo %PATH%
```

## windows 下路径

在Windows中，不同命令行环境的路径写法确实存在差异，核心区别在于**路径分隔符**（正斜杠`/` vs 反斜杠`\`）和**路径表示方式**（Windows原生 vs Linux风格）。以下是各环境的详细对比。

**一、CMD (命令提示符)**

CMD是Windows的原生命令行，路径规则最传统。

- **路径分隔符**：使用反斜杠 `\`（如 `C:\Windows\System32`）。
- **支持正斜杠**：虽然标准是反斜杠，但许多内部命令也接受正斜杠 `/`，不过这并非标准做法。
- **绝对与相对路径**：
  - **绝对路径**：从盘符开始的完整路径，如 `C:\Users\YourName`。
  - **相对路径**：基于当前目录，如 `.\Documents`（当前目录）或 `..\`（上级目录）。
- **UNC路径**：访问网络共享时使用，以双反斜杠开头，如 `\\server\share\file.txt`。
- **环境变量**：支持使用 `%` 包裹的环境变量，如 `%USERPROFILE%\Documents`。
- **处理空格**：路径中的空格必须用英文双引号括起来，如 `"C:\Program Files\MyApp"`。

**二、PowerShell**

PowerShell是更强大的现代Shell，路径处理上兼具兼容性和灵活性。

- **分隔符兼容**：**反斜杠 `\` 和正斜杠 `/` 都接受**，这在跨平台脚本中非常有用。
- **路径类型**：同样支持绝对路径和相对路径（`.` 和 `..`）。
- **根路径简写**：单独的 `\` 代表当前驱动器的根目录。
- **主目录简写**：波浪号 `~` 代表当前用户的主目录。
- **特殊路径（Provider Path）**：支持更复杂的路径格式，如 `HKLM:\Software` 访问注册表。

**三、BAT脚本 (批处理文件)**

BAT脚本基于CMD命令，其路径写法与CMD基本一致，但有一些**脚本特有的变量**：

- **`%~dp0`**：代表脚本文件所在的**文件夹路径**（以反斜杠结尾），常用于获取脚本自身位置。
- **`%0`**：代表脚本文件的**完整路径和文件名**。
- **`%cd%`**：代表**当前工作目录**的路径，其值会随 `cd` 命令改变。
- **`/d` 参数**：切换驱动器时，建议使用 `cd /d "D:\YourFolder"`。

**四、Git Bash**

Git Bash在Windows上模拟了Linux环境，其路径规则很独特。

- **分隔符**：使用正斜杠 `/`，这是Unix标准。
- **驱动器表示**：Windows的 `C:\` 在Git Bash中表示为 `/c/`。
- **路径转换 (MSYS2)**：Git Bash会自动将类Unix路径转换为Windows路径。例如，`/c/Windows` 会被转为 `C:\Windows`。这种转换有时会引发问题，比如执行 `cmd /c` 时，`/c` 可能被误转为 `C:/`。
  - **解决方法**：可以用 `//` 来“逃逸”，如 `cmd //c`；或通过设置环境变量 `MSYS_NO_PATHCONV=1` 来禁用转换。
- **工具**：Git Bash自带的 `cygpath` 工具可以显式地进行路径格式转换。

**总结对比**

| 特性             | CMD        | PowerShell               | BAT脚本         | Git Bash   |
| :--------------- | :--------- | :----------------------- | :-------------- | :--------- |
| **路径分隔符**   | 反斜杠 `\` | 反斜杠 `\` 或 正斜杠 `/` | 反斜杠 `\`      | 正斜杠 `/` |
| **驱动器表示**   | `C:`       | `C:`                     | `C:`            | `/c/`      |
| **根目录简写**   | 无         | `\`                      | 无              | `/`        |
| **主目录简写**   | 无         | `~`                      | 无              | `~`        |
| **特殊变量**     | 无         | 无                       | `%~dp0`, `%cd%` | 无         |
| **路径自动转换** | 无         | 无                       | 无              | 有 (MSYS2) |

## 双反斜杠 `\\`

在实际工作中主要出现在 **5种完全不同的场景**。它们的目的各不相同，并非都是“路径”本身，但经常被混淆。

我帮你按**实际用途**分类，这样你一看就懂：

1. 访问网络共享（UNC路径）—— 最经典的用途

   这是你**在命令行中直接输入**双反斜杠最常见的原因。
   - **写法**：`\\服务器名\共享文件夹\子目录`
   - **例子**：`\\192.168.1.100\SharedDocs` 或 `\\MyNAS\Video`
   - **说明**：这代表网络路径（通用命名约定，UNC），**必须以两个反斜杠开头**。无论是 CMD、PowerShell 还是资源管理器地址栏，都是这样写。

2. 在编程/脚本代码中转义反斜杠（字符串字面量）

   当你在写**代码**（如 C#、Python、JSON、Java）或 **PowerShell 脚本**给变量赋路径字符串时，单个反斜杠 `\` 通常是“转义符”（比如 `\n` 代表换行）。为了表示一个真正的反斜杠，你必须写两个 `\\`。
   - **注意**：这不是最终路径，而是**源代码里的写法**，程序运行时会被解释为单个 `\`。
   - **PowerShell 示例**：`$path = "C:\\Users\\Admin\\file.txt"`（因为在双引号字符串中，`\` 不是转义符？
     **更正**：PowerShell 的转义符是反引号 ```，不是反斜杠。所以在 PowerShell 中，`"C:\Users"`直接写即可，**不需要**转义为`\\`。但在 C#、Java、Python 中必须写 `\\`）。
   - **常见场景**：配置 JSON 文件时，必须写成 `"path": "C:\\Windows\\System32"`，因为 JSON 标准要求反斜杠必须转义。

3. 正则表达式（用于匹配路径）

   如果你在 CMD 的 `findstr` 或 PowerShell 的 `-replace` 正则匹配中**查找路径**，由于正则里 `\` 也是转义符，为了匹配一个文本意义上的反斜杠，你需要写 `\\`。
   - **PowerShell 示例**：`"C:\Test" -replace "\\", "/"`（将路径中的反斜杠替换为正斜杠）。这里 `\\` 在正则中代表“匹配一个反斜杠字符”。

4. 避开 Git Bash 的路径自动转换（MSYS2 机制）

   **这是你之前问到的 Git Bash 特有的坑**。
   - 当你在 Git Bash 中执行 Windows 原生命令（如 `cmd`、`cls`）时，如果参数里只有一个 `/c`，Git Bash 会自作主张把它转成 `C:\`。
   - 为了**阻止**这个自动转换，你可以把单个斜杠写成双斜杠 `//`，或者把反斜杠变成双反斜杠`\\`。
   - **经典写法**：`cmd //c dir`（这里 `//` 是为了告诉 MSYS2“别动我的参数”，传给 cmd 时它会被理解为 `/c`）。虽然这是正斜杠，但原理相同。

5. 批处理（BAT）中的特殊转义（极少见）

   在 BAT 脚本中，反斜杠 `\` **不是**转义符（转义符是 `^`）。所以路径直接写 `C:\Test` 即可。
   **唯一例外**：如果你要用 `reg add` 操作注册表，且路径包含带空格的键名，通常不会用到 `\\`。除非你在 `for /f` 循环中对路径做复杂拼接，需要把 `\` 当成普通字符来处理，但这种情况基本遇不到。

**重要提醒：别搞混了！**

**在 CMD 或 PowerShell 的命令行提示符下，你直接敲 `cd C:\\Windows` 是错的！**
因为命令行解释器（Shell）在接收命令时，反斜杠本身就是普通字符，不需要转义。直接写 `cd C:\Windows` 或 `cd C:/Windows` 即可。

| 你遇到的情况                         | 是否需要写 `\\`                | 原因                              |
| :----------------------------------- | :----------------------------- | :-------------------------------- |
| 访问局域网共享文件夹                 | **必须** `\\192.168.x.x\share` | UNC 路径固定语法                  |
| 在 Python/Java/C# 代码里写路径字符串 | **必须** `"C:\\Test"`          | 源代码字符串转义规则              |
| 在 PowerShell 命令中直接敲路径       | **不需要**，写 `C:\Test`       | PowerShell 命令解析器不转义反斜杠 |
| 在 JSON/YAML 配置文件中写路径        | **必须** `"C:\\Test"`          | 配置文件格式强制要求              |
| 在正则表达式中匹配反斜杠             | **必须** `\\`                  | 正则转义规则                      |
| 在 BAT 脚本里写路径                  | **不需要**，写 `C:\Test`       | 批处理不把 `\` 当转义符           |

## cygwin

<https://cn.x-cmd.com/install/cygwin>

## Powershell

### 查看环境变量

[PowerShell 命令行输出和添加系统环境变量](https://juejin.cn/post/7159196080842735652)

在 PowerShell 中查看系统环境变量的指令为：

```powershell
$env:path
# 或
echo $env:path
# 或
type env:path
```

如果想要每条环境变量逐行显示：

```powershell
(type env:path) -split ';'
```

## 使用 rar gzip 命令行

### 使用 rar 命令

在 Windows 下使用`rar`命令行工具需要先安装 WinRAR 软件，WinRAR 软件安装后的目录中包含 `Rar.exe` 和 `UnRAR.exe`，然后就可以在 CMD 或 powershell 中直接使用命令 `rar a`（添加文件压缩）和 `rar x`（解压文件）。

- **步骤一：安装 WinRAR**
- **步骤二：把 WinRAR 添加到系统环境变量**
  如把 `C:\Program Files\WinRAR` 添加到系统环境变量。
- **步骤三：执行 RAR 命令**
  - **压缩文件**：

    使用`rar a`命令来创建压缩包。
    - **命令格式**:

      `rar a <输出压缩包名.rar> <文件或文件夹名称>`
      示例：`rar a -r my_archive.rar my_folder`（将`my_folder`文件夹及其所有内容压缩到`my_archive.rar`文件中，`-r`参数用于递归处理子目录）。

  - **解压文件**：

    使用`rar x`命令来解压压缩包。
    - **命令格式**:

      `rar x <压缩包名.rar> <目标目录>`
      示例：`rar x my_archive.rar C:\Extract`（将`my_archive.rar`解压到`C:\Extract`目录）。

  **常见命令和参数**
  - `a`：将文件添加到压缩文件中。

  - `x`：解压文件。

  - `-r`：递归地将目录中的所有文件和子目录添加到压缩文件中。

  - `-ag`：在创建压缩文件时，附加当前日期和时间字符串（如`backupYYYYMMDDHHMMSS.rar`）。

  - `-p<password>`：为压缩文件设置密码，密码必须紧跟`-p`后面。

  - `-o+`：覆盖已存在的解压文件。

### 使用 gzip 命令

Gun Win 项目为 Win32 提供了 GNU Linux 平台的一些工具包，可以在 Window 平台使用 Linux 的部分工具, [具体介绍和工具列表](http://gnuwin32.sourceforge.net/summary.html)

打开[下载地址](https://gnuwin32.sourceforge.net/packages/gzip.htm)，这里我们可以选择使用第一个(Complete package, except sources 安装包方式)或者第三个(Binaries 二进制文件)，两个使用方法略有不同：

**安装包方式**
安装下载的 exe 文件，安装完成之后设置环境变量，我本机安装在了 C:\Program Files (x86)\GnuWin32\bin\ 把这个变量配置到系统环境变量的 PATH 中，即可在命令行中使用 gzip 命令进行压缩文件
**二进制文件方式**
解压下载的 zip 文件，在 bin 目录下有 gzip.exe 可执行文件，可以配置当前 bin 目录到 PATH，或者直接在命令行中直接使用 exe 进行压缩。
