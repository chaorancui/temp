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

## 软件使用记录

### Total Commander

[【Win10 软件】Total Commander 基本配置及使用（整理）](https://www.cnblogs.com/sjsea/p/13213210.html)

### Typora_Unlocker

<https://github.com/743859910/Typora_Unlocker>

<https://www.ghxi.com/typora.html>
