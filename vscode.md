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

