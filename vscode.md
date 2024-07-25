# vsCode 配置

## 软件

### 安装版

* 安装过程可以添加右键菜单
* 插件安装目录默认，需要额外修改



### 便携版

* 插件安装位置在便携解压目录
* 需要自己添加右键菜单

官方文档在Portable Mode部分已经说明了，你只需要在解压后的VSCode目录里新建一个名为data的文件夹，那么以后所有的数据文件（包括用户配置、插件等）都会安装到这个data文件夹里。

以前网上流传的加启动选项--extensions-dir [path] 的方法，在部分情景下有不少缺点，这里提到的方法应该是最完美的，百闻不如一试，赶快动手吧~



最后，附上一段把 VSCode 添加到右键菜单的[bat代码](https://www.zhihu.com/search?q=bat代码&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1139906712})，保存到一个.bat文件里并放到 VSCode 目录中，双击运行：

```bat
@ECHO OFF
PUSHD %~DP0
TITLE VSCode
Md "%WinDir%\System32\test_permissions" 2>NUL||(Echo 请使用右键管理员身份运行&&Pause >NUL&&Exit)
Rd "%WinDir%\System32\test_permissions" 2>NUL
SetLocal EnableDelayedExpansion
SET /P ST=输入a添加右键菜单，输入d删除右键菜单：
if /I "%ST%"=="a" goto Add
if /I "%ST%"=="d" goto Remove
:Add
reg add "HKEY_CLASSES_ROOT\*\shell\VSCode"         /t REG_SZ /v "" /d "&VSCode"   /f
reg add "HKEY_CLASSES_ROOT\*\shell\VSCode"         /t REG_EXPAND_SZ /v "Icon" /d "%~dp0Code.exe" /f
reg add "HKEY_CLASSES_ROOT\*\shell\VSCode\command" /t REG_SZ /v "" /d "%~dp0Code.exe \"%%1\"" /f
 
exit
:Remove
reg delete "HKEY_CLASSES_ROOT\*\shell\VSCode" /f
exit
```



## vscode-server

当你使用 Visual Studio Code (VS Code) 的 Remote-SSH 扩展连接到远程服务器时，VS Code 会自动在远程服务器上安装一个名为 "VS Code Server" 的组件，以便在远程环境中运行代码编辑功能。首次 SSH 到远程服务器时下载，所以首次可能会比较慢。

> VSCode Server 的版本要和 VSCode 的版本对应，当 VSCode 更新时，下次 SSH 登陆远程服务器，VSCode Server 会重新下载安装更新后的版本。二者对应用的是<commit_id>，可以在 【VSCode 菜单栏】-->【Help】->【About】下查看【Commit】的值 。

### 自动安装 VS Code Server

1. **安装 Remote-SSH 扩展**：
   - 在 VS Code 中，打开扩展市场（快捷键：`Ctrl+Shift+X`）。
   - 搜索并安装 `Remote - SSH` 扩展。
2. **配置 SSH 连接**：
   - 打开命令面板（快捷键：`Ctrl+Shift+P`）。
   - 输入并选择 `Remote-SSH: Connect to Host...`。
   - 如果这是你第一次设置连接，你需要配置 SSH 主机。在弹出的对话框中，输入远程主机的 SSH 地址（如 `user@hostname`）。
   - 如果 SSH 主机已经配置好，选择你要连接的主机。
3. **连接到远程主机**：
   - 选择要连接的远程主机后，VS Code 将使用配置的 SSH 密钥或密码进行连接。
   - 连接成功后，VS Code 会自动在远程主机上安装所需的 VS Code Server。这通常包括下载并解压必要的文件。
4. **安装过程**：
   - 在连接的过程中，你可能会看到 VS Code 的输出窗口显示安装进度。
   - 一旦安装完成，你将在 VS Code 的左下角看到一个绿色的远程连接图标，表示你已经连接到远程主机。

### 手动安装或解决安装问题

在某些情况下，自动安装可能失败或你可能需要手动干预（远程服务器无法访问外网或网络不稳定一直安装失败）。这种情况下，你可以通过以下步骤手动安装或调试：

1. **查看日志**：
   - 打开输出窗口（`View` -> `Output`）。
   - 从下拉菜单中选择 `Remote - SSH` 查看连接和安装过程的日志。
2. **手动安装 VS Code Server**：
   - 从日志中找到 VS Code Server 的下载 URL。
   - 在远程主机上使用 `wget` 或 `curl` 下载该文件。
   - 解压下载的文件并确保正确的权限设置。
3. **检查权限**：
   - 确保你的用户对安装目录有写权限。
   - 如果需要，尝试使用 `sudo` 权限进行安装（注意安全性和权限管理）。

总结

### 手动下载和安装 VS Code Server

1. **下载 VS Code Server**：

   - 使用 `wget` 或 `curl`

      从能联网的机器上运行下述命令下载 VS Code Server。例如：

     ```shell
     wget https://update.code.visualstudio.com/commit:<commit_id>/server/<platform>/<architecture>/stable -O vscode-server.tar.gz
     # 这个 URL 包含了具体的 `commit_id`、`platform` 和 `architecture` 信息。
     
     # 例子：
     wget https://update.code.visualstudio.com/commit:f1e16e1e6214d7c44d078b1f0607b2388f29d729/server-linux-x64/stable -O vscode-server.tar.gz
     ```

     下载完成之后，把软件包拷贝到不能联网的远程服务器。可以使用scp命令或者winscp等ftp工具。

2. **解压下载的文件**：

   - 解压下载的 tar 文件：

     ```shell
     tar -xzf vscode-server.tar.gz -C ~/.vscode-server/bin/<commit_id>
     ```

   - 创建解压目录（如果它不存在的话）：

     ```shell
     mkdir -p ~/.vscode-server/bin/<commit_id>
     ```

3. **设置权限**：

   - 确保文件和目录具有正确的权限，以便 VS Code 可以运行：

     ```shell
     chmod -R 755 ~/.vscode-server/bin/<commit_id>
     ```

4. **重启 VS Code 并重新连接**：

   - 断开远程连接，然后重新连接。VS Code 应该检测到 VS Code Server 已经安装，并直接使用它。

### 需要注意的事项

- **下载 URL 的结构**：
  - `commit_id` 是 VS Code 的特定版本标识。
  - `platform` 是操作系统，例如 `linux`。
  - `architecture` 是系统架构，例如 `x64`。
- **确保网络连接**：
  - 你的远程服务器需要能够访问互联网，以便下载 VS Code Server。
  - 如果你的服务器在防火墙后面或没有互联网访问权限，可能需要通过其他方式将文件传输到服务器上。

通过这些步骤，你可以手动下载和安装 VS Code Server，在需要时进行故障排除或确保安装顺利。

自动安装要求远程服务器可以访问`VS Code Server 下载 URL` ：

```shell
https://update.code.visualstudio.com/commit:<commit_id>/server/<platform>/<architecture>/stable
```

这个 URL 包含了具体的 `commit_id`、`platform` 和 `architecture` 信息。



## 插件

### 系统安装

* MinGw
* Operator Mono 字体



### 软件安装

* vscode-icons: Icons for Visual Studio Code
* C/C++: C/C++ IntelliSense, debugging, and code browsing.
* C/C++ Extension Pack: Popular extensions for C++ development in Visual Studio Code.
* Markdown Preview Enhanced: Markdown Preview Enhanced ported to vscode
* Vim: Vim emulation for Visual Studio Code
* LeetCode: Solve LeetCode problems in VS Code
* LeetCode with labuladong: 帮助 labuladong 的读者高效刷题
* 



## 配置

首先输入：`command + p`，然后输入：`Settings`，接下来，选择：`Preferences: Open Settings (UI)`，就进入了快捷键文件 `settings.json` 编辑页面。

路径：C:\Users\c00619335\AppData\Roaming\Code\User\settings.json

### 基础配置参考

```json
{
    // leetcode
    "leetcode.endpoint": "leetcode-cn",
    "leetcode.defaultLanguage": "cpp",
    "leetcode.showDescription": "Both",
    "leetcode.showLocked": true,
    
    // 信任区域
    "security.workspace.trust.banner": "never",
    "security.workspace.trust.untrustedFiles": "open",
    
    // markdown 插件
    "markdown-preview-enhanced.codeBlockTheme": "solarized-dark.css",
    "markdown-preview-enhanced.previewTheme": "solarized-dark.css",
    
    // editor
    "editor.minimap.enabled": false,
    "editor.lineNumbers": "relative",
    "workbench.iconTheme": "vscode-icons",
    "C_Cpp.clang_format_fallbackStyle": " { BasedOnStyle: Visual Studio,  ColumnLimit: 120 }",
    // "editor.fontFamily": "Fira Code, Consolas, 'Courier New', monospace",
    // "editor.fontLigatures": true,
    "editor.fontFamily": "Operator Mono",
    "editor.fontLigatures": true, // 这个控制是否启用字体连字，true启用，false不启用，这里选择启用
    "editor.tokenColorCustomizations": {
        "textMateRules": [
            {
                "name": "italic font",
                "scope": [
                    "comment",
                    "keyword",
                    "storage",
                    "keyword.control.import",
                    "keyword.control.default",
                    "keyword.control.from",
                    "keyword.operator.new",
                    "keyword.control.export",
                    "keyword.control.flow",
                    "storage.type.class",
                    "storage.type.function",
                    "storage.type",
                    "storage.type.class",
                    "variable.language",
                    "variable.language.super",
                    "variable.language.this",
                    "meta.class",
                    "meta.var.expr",
                    "constant.language.null",
                    "support.type.primitive",
                    "entity.name.method.js",
                    "entity.other.attribute-name",
                    "punctuation.definition.comment",
                    "text.html.basic entity.other.attribute-name.html",
                    "text.html.basic entity.other.attribute-name",
                    "tag.decorator.js entity.name.tag.js",
                    "tag.decorator.js punctuation.definition.tag.js",
                    "source.js constant.other.object.key.js string.unquoted.label.js",
                ],
                "settings": {
                    "fontStyle": "italic",
                }
            },
        ]
    },
    "editor.fontSize": 16,
    "terminal.integrated.cursorStyle": "line",
    "terminal.integrated.defaultProfile.windows": "Git Bash",
    "[cpp]": {
        "editor.defaultFormatter": "NextCode.nextcode-check"
    },
    "vim.insertModeKeyBindings": [
        {
            "before": [
              "j",
              "j"
            ],
            "after": [
              "<Esc>"
            ]
        },
      ],
    "vim.vimrc.enable": true
}
```

### vscode 标签页高亮

在系统的 `settings.json` 里添加

    "workbench.colorCustomizations": {
        "tab.activeBackground": "#d9ff009d",
        "editor.lineHighlightBackground": "#ffd00033"
    },







## 按键映射

> [Visual Studio Code 的按键绑定](https://code.visualstudio.com/docs/getstarted/keybindings#_keyboard-shortcuts-reference)

首先输入：`command + p`，然后输入：`keyboard`，接下来，选择：`Preferences: Open Keyboard shortcurs(JSON)`，就进入了快捷键文件 keybindings.json 编辑页面。

路径：C:\Users\c00619335\AppData\Roaming\Code\User\keybindings.json

```json
// 将键绑定放在此文件中以覆盖默认值
[
    {
        "key": "ctrl+f",
        "command": "cursorRight",
        "when": "editorTextFocus && vim.active && vim.use<C-f> && !inDebugRepl && vim.mode == 'Insert'"
    },
    {
        "key": "ctrl+b",
        "command": "cursorLeft",
        "when": "editorTextFocus && vim.active && vim.use<C-b> && !inDebugRepl && vim.mode == 'Insert'"
    },
    {
        "key": "ctrl+p",
        "command": "cursorUp",
        "when": "editorTextFocus && vim.active && vim.use<C-p> && !inDebugRepl && vim.mode == 'Insert'"
    },
    {
        "key": "ctrl+n",
        "command": "cursorDown",
        "when": "editorTextFocus && vim.active && vim.use<C-n> && !inDebugRepl && vim.mode == 'Insert'"
    },
]
```

其他可参考：

> [VSCode Terminal 快捷键设置](https://zgljl2012.com/vscode-terminal-kuai-jie-jian-she-zhi/)

```json
// Place your key bindings in this file to override the defaults
[
    { "key": "ctrl+1",                "command": "workbench.action.terminal.focusAtIndex1", "when": "terminalFocus" },
    { "key": "ctrl+2",                "command": "workbench.action.terminal.focusAtIndex2", "when": "terminalFocus" },
    { "key": "ctrl+3",                "command": "workbench.action.terminal.focusAtIndex3", "when": "terminalFocus" },
    { "key": "ctrl+4",                "command": "workbench.action.terminal.focusAtIndex4", "when": "terminalFocus" },
    { "key": "ctrl+5",                "command": "workbench.action.terminal.focusAtIndex5", "when": "terminalFocus" },
    { "key": "ctrl+6",                "command": "workbench.action.terminal.focusAtIndex6", "when": "terminalFocus" },
    { "key": "ctrl+7",                "command": "workbench.action.terminal.focusAtIndex7", "when": "terminalFocus" },
    { "key": "ctrl+8",                "command": "workbench.action.terminal.focusAtIndex8", "when": "terminalFocus" },
    { "key": "ctrl+9",                "command": "workbench.action.terminal.focusAtIndex9", "when": "terminalFocus" },
    { "key": "ctrl+t",                "command": "workbench.action.terminal.new", "when": "terminalFocus" },
    { "key": "ctrl+p",                "command": "cursorup", "when": "terminalFocus" },
    { "key": "ctrl+n",                "command": "cursordown", "when": "terminalFocus" }

]
// 这就设置好了基础的配置。ctrl+1-9 用于切换终端， ctrl+t 用于创建新终端。
```

### vscode 标签页高亮

在系统的`settings.json`里添加

    "workbench.colorCustomizations": {
        "tab.activeBackground": "#d9ff009d",
        "editor.lineHighlightBackground": "#ffd00033"
    },





## 调试

### vscode 调试添加运行参数

`launch.json` 中添加 `args` 项，每个运行参数是一个字符串，如：

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "args": [
                "./xxx/xxx.yaml",
                "--xxx=xxx"
            ]
        }
    ]
}
```



### vscode 调试添加环境变量

`launch.json` 中添加 `envs` 项：

> python 用 `env`
>
> C/C++ 用 `environment`
>
> ```json
> "environment":[
>  {
>      "name":"squid",
>      "value":"clam"
>  }
> ]
> ```

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {
                "PYTHONPATH": "/usr/local/xxx/xxx/python:$PYTHONPATH",
                "PATH": "~/xxx/xxx:$PATH",
                "LD_LIBRARY_PATH": "~/xxx/lib64:$LD_LIBRARY_PATH"
            }
        }
    ]
}
```



### vscode 设置调试器当前工作路径

`launch.json` 中添加 `cwd` 项：

Specifies the current working directory for the debugger, which is the base folder for any relative paths used in code. If omitted, defaults to `${workspaceFolder}` (the folder open in VS Code).

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "cwd": "xxx/xxx"
        }
    ]
}
```





# CLion

### clion 高亮快捷键

选中文本，Ctrl+Shift+f7：高亮显示所有该文本，按ESC高亮消失（类似Ctrl+Shift+F）





# Nodejs

```
registry=https://registry.npm.taobao.org/
strict-ssl=false
proxy=http://user:password@proxy.huawei.com:8080/
https-proxy=http://user:password@proxy.huawei.com:8080/
```

> **密码中特殊字符的处理**
> 如果密码中有@等特殊字符，会出错，此时要对其中的特殊符号进行处理，使用百分比编码(Percent-encoding)对特殊字符进行转换，转换列表如下：
> ! --> %21  # --> %23  $ --> %24  & --> %26  ' --> %27
> ( --> %28  ) --> %29  * --> %2A  + --> %2B  , --> %2C
> / --> %2F  : --> %3A  ; --> %3B  = --> %3D  ? --> %3F
> @ --> %40  [ --> %5B  ] --> %5D
>
> 例如：密码是12#，转义之后就是12%23

## 离线安装

1. 下载 linux 版本的 node.js

   下载网址：<https://nodejs.org/zh-cn/download/package-manager>

   Linux 选择【预构建二进制文件】-->【Linux】-->【x64】-->【v20.16.0(LTS)】-->下载，会得到如 `node-v20.16.0-linux-x64.tar.xz` 的文件。

   

   

   
