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

### win11 修改蓝牙设备的名称教程

<https://zhuanlan.zhihu.com/p/625885504>

### 安装字体

下面是安装或管理字体的两种方法：

- 所有字体都存储在 `C:\Windows\Fonts` 文件夹中。 （可选）只需将字体文件从提取的文件文件夹拖动到此文件夹中即可添加字体。 然后，Windows 会自动安装它们。 若要查看字体的外观，请打开“字体”文件夹，右键单击字体文件，然后选择“预览”。

- 还可以通过控制面板查看已安装的字体。 根据你的 Windows 版本，你将转到**控制面板** > **字体** -- 或 - **控制面板** > **外观和个性化** > **字体**。

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
