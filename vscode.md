# vscode

> [Visual Studio Code 的按键绑定](https://code.visualstudio.com/docs/getstarted/keybindings#_keyboard-shortcuts-reference)


### VSCode Terminal 快捷键设置
> https://zgljl2012.com/vscode-terminal-kuai-jie-jian-she-zhi/

首先输入：command + p，然后输入：keyboard，接下来，选择：

Preferences: Open Keyboard shortcurs(JSON)，就进入了 快捷键文件 keybindings.json 编辑页面。

输入：

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


这就设置好了基础的配置。ctrl+1-9 用于切换终端， ctrl+t 用于创建新终端。





### vscode 标签页高亮
在系统的`settings.json`里添加

    "workbench.colorCustomizations": {
        "tab.activeBackground": "#d9ff009d",
        "editor.lineHighlightBackground": "#ffd00033"
    },


# CLion

### clion 高亮快捷键

选中文本，Ctrl+Shift+f7：高亮显示所有该文本，按ESC高亮消失（类似Ctrl+Shift+F）



