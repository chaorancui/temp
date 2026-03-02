[toc]

# Node.js 介绍

## Node.js 和 npm

简要结论：
**Node.js 是一个能在本地/服务器上运行 JavaScript 的运行时环境；npm 是随 Node.js 一起提供的包管理器，用来安装、管理和发布 JavaScript 依赖库。**
两者**强相关，但分工明确**。

### 一、Node.js

**Node.js = JavaScript 的运行环境（runtime）**

在 Node.js 出现之前：

- JavaScript 只能在 **浏览器** 里运行（操作 DOM、写前端交互）

Node.js 出现之后：

- JavaScript 可以在 **浏览器之外** 运行
- 可以写：
  - Web 后端服务
  - CLI 工具（如 vue-cli、eslint、webpack）
  - 构建脚本 / 自动化工具
  - 本地工具链（你在 C/C++、Python 项目里经常“被动用到”的那种）

核心特性：

- 基于 **V8 引擎**（和 Chrome 用的一样）
- **事件驱动 + 非阻塞 I/O**
- 非常适合：
  - 高并发
  - I/O 密集型任务（网络、文件、RPC）

例:

```js
// server.js
const http = require('http');
http.createServer((req, res) => {
  res.end('Hello Node.js');
}).listen(3000);

node server.js
```

这就是 **Node.js 在跑 JS 程序**。

### 二、npm

**npm = Node Package Manager（包管理器）**

它的作用和你熟悉的这些工具是一个级别的东西：

| 语言        | 包管理器       |
| ----------- | -------------- |
| C/C++       | vcpkg / conan  |
| Python      | pip            |
| Java        | Maven / Gradle |
| **Node.js** | **npm**        |

npm 主要干 3 件事

1. **安装第三方库**

   ```bash
   npm install lodash
   ```

2. **管理依赖版本**
   - 记录在 `package.json`
   - 锁定在 `package-lock.json`

3. **运行脚本**

   ```bash
   npm run build
   npm run test
   ```

### 三、Node 和 npm 的关系

关系一句话总结：

**Node.js 是“发动机”，npm 是“仓库 + 管理系统”**

具体关系：

- 安装 Node.js 时：
  - ✅ 自动附带 npm
- npm 本身：
  - 是用 **Node.js 写的**
  - 运行时依赖 Node

注意：

- 大量后端、工具链、构建系统都依赖 Node + npm。**npm 已经是现代工程工具链的一部分，而不是“前端专属”**。
- npm 不是唯一选择，还有：yarn、pnpm，但**它们本质仍然围绕 Node.js 生态**。

# npm

## npm 配置代理

1. 命令行直接配置（最常用）
   在终端执行以下命令（请根据你公司的实际代理地址和端口进行修改，通常端口是 8080 或 7890）：

   ```bash
   npm config set proxy http://username:password@server:port
   npm config set https-proxy http://username:password@server:port
   ```

2. 编辑家目录配置文件 `.npmrc`
   - 打开文件：`vim ~/.npmrc`
   - 添加或修改以下行：

     ```bash
     proxy=http://username:password@server:port
     https-proxy=http://username:password@server:port
     registry=https://registry.npmmirror.com
     ```

     _(注：建议同时加上最后一行的镜像源，双重保险)_

3. 检查和取消配置

   配置完成后，你可以验证是否生效：
   - **查看当前代理：** `npm config get proxy`

   - **查看全部配置：** `npm config list`

   - **取消代理配置**（如果以后换了网络环境）：

     ```bash
     npm config delete proxy
     npm config delete https-proxy
     ```
