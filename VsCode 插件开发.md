[toc]

# VsCode 插件介绍

## 插件本质

VSCode 插件其实就是一个 **Node.js 项目 + 插件描述文件**。

核心组件：

```log
extension/
 ├─ package.json        # 插件清单（最重要）
 ├─ extension.js / ts   # 插件入口代码
 ├─ syntaxes/           # 语法高亮
 ├─ language-configuration.json
 ├─ README.md
 └─ node_modules/
```

插件最终会被打包成：

```log
xxx-0.0.1.vsix
```

`.vsix` 本质是一个 **zip包**，里面就是插件文件。

## 插件的核心文件

所有插件的行为都由 `package.json` 定义。

典型结构：

```json
{
  "name": "shell-formatter",
  "displayName": "Shell Formatter",
  "version": "0.0.1",
  "publisher": "bdq460",
  "engines": {
    "vscode": "^1.60.0"
  },
  "main": "./extension.js",

  "contributes": {
    "languages": [],
    "commands": [],
    "configuration": []
  }
}
```

关键字段：

| 字段           | 作用           |
| -------------- | -------------- |
| name           | 插件ID         |
| publisher      | 发布者         |
| version        | 插件版本       |
| engines.vscode | 兼容VSCode版本 |
| main           | 插件入口       |
| contributes    | 声明功能       |

VSCode 启动时会读取这些配置决定插件能力。

## 插件打包工具

官方工具：

```bash
@vscode/vsce
```

作用：

- 打包 `.vsix`
- 发布 Marketplace
- 校验插件

安装：

```bash
npm install -g @vscode/vsce
```

`vsce` 是 VSCode Extension Manager 的 CLI 工具。

# VsCode 插件编译

以项目 **shell-formatter** 为例，讲一下 **源码 → VSIX 的完整流程**，以及 **是否区分平台**。
我会按“工程结构 → 构建 → 打包 → 安装 → 跨平台”这条主线讲清楚。

## 编译流程

1. 克隆源码

   以你的项目为例：

   ```bash
   git clone https://github.com/bdq460/shell-formatter.git
   cd shell-formatter
   ```

2. 安装依赖

   VSCode 插件基本都是 Node 项目：

   ```bash
   npm install
   ```

   如果项目用 TypeScript：

   ```bash
   npm run compile
   # 或
   npm run build
   ```

3. 本地测试插件（推荐）

   在 VSCode 中：

   ```bash
   F5
   ```

   会启动一个：

   ```log
   Extension Development Host
   ```

   用于调试插件。

4. 打包 VSIX

最关键一步：

```bash
vsce package
```

生成：

```bash
shell-formatter-0.0.1.vsix
```

VSCE 会做几件事：

1️⃣ 读取 `package.json`
2️⃣ 收集项目文件
3️⃣ 生成插件 manifest
4️⃣ 压缩成 `.vsix`

这个流程就是 **VSIX packaging pipeline**。

## 打包文件

打包时 VSCE 会读取：

```bash
.vscodeignore
```

类似 `.gitignore`。

例如：

```log
node_modules
src
test
.vscode
```

这些不会被打包。

可以查看：

```log
vsce ls
```

## VSIX 是否区分平台

- **99% VSCode插件是跨平台的。**

  原因：

  VSCode 插件运行在 `Node.js runtime`，只要 JS 能运行就可以，所以一般无需重新编译。

- 什么时候需要区分平台？

  只有两种情况：
  1. 插件包含 native binary

     例如：

     ```bash
     formatter
     tree-sitter
     clang
     ripgrep
     ```

     这时会有：

     ```bash
     bin/linux-x64
     bin/win-x64
     bin/darwin
     ```

     插件运行时根据平台加载。

  2. Node native module

     例如：

     ```bash
     node-gyp
     native addon
     ```

     需要针对平台编译。

## 总结

1. VSCode 插件打包流程：

   ```log
   源码
    ↓
   npm install
    ↓
   build (optional)
    ↓
   vsce package
    ↓
   xxx.vsix
    ↓
   VSCode install
   ```

   特点：
   - `.vsix` 本质 zip
   - 默认跨平台
   - 只有 native 组件才区分 OS

2. VSCode插件发布流程（完整）

   开发者通常：

   ```log
   源码
    ↓
   npm install
    ↓
   npm run build
    ↓
   vsce package
    ↓
   vsce publish
    ↓
   Marketplace
   ```

   Marketplace 实际存储的也是 `.vsix`。

# VsCode 插件开发

## 推荐开发流程（专业做法）

如果你以后也写 VSCode 插件：

建议结构：

```log
extension/
 ├─ src/
 ├─ package.json
 ├─ tsconfig.json
 ├─ .vscodeignore
 ├─ webpack.config.js
 └─ README.md
```

构建：

```bash
npm run build
vsce package
```

CI 自动发布。

# VSIX 安装方式

1. 方法1 CLI

   ```bash
   code --install-extension shell-formatter-0.0.1.vsix
   ```

2. 方法2 GUI

   ```log
   Extensions
    → ...
    → Install from VSIX
   ```

# SSH 远程时插件运行情况

当 Windows + SSH Linux server 时，VSCode 实际运行结构是：

```log
Windows VSCode
        │
        │ SSH
        ▼
Linux VSCode Server
        │
        ▼
Extension Host
```

所以插件可能运行在：

| 插件类型 | 运行位置 |
| -------- | -------- |
| UI插件   | 本地     |
| 语言服务 | 远端     |

很多插件会声明 `extensionKind`，例如：`"extensionKind": ["workspace"]`，意思在 remote server 运行。

# VsCode 插件分析

## VSIX 可以直接解压

你可以 **直接解压 VSIX 看结构**：

```log
unzip extension.vsix
```

结构类似：

```log
extension.vsix
 ├─ extension/
 │   ├─ package.json
 │   ├─ extension.js
 │   └─ ...
 └─ [Content_Types].xml
```

如果你愿意，我可以再给你讲 **VSCode 插件内部运行机制（Extension Host / LSP / Remote Extension）**。

很多高级插件（Python、Rust、Copilot）都用这个架构，理解后你会对 VSCode 的插件系统非常清晰。
