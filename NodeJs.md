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

## npm 和 npx

**一、npm vs npx 对比**

| 维度         | npm      | npx            |
| ------------ | -------- | -------------- |
| 主要用途     | 管理依赖 | 执行工具       |
| 是否安装包   | 是       | 否（临时下载） |
| 是否全局安装 | 支持     | 不需要         |
| 使用场景     | 项目构建 | CLI 工具运行   |

一句话总结：

- **npm：用来“安装和管理包”**
- **npx：用来“直接运行包里的工具”**

1. **npm 是什么**

   **npm（Node Package Manager）** 是 Node.js 的官方包管理工具，主要用于：
   - 管理项目依赖（安装 / 卸载 / 更新）
   - 发布和分发 JavaScript 包
   - 管理版本（package.json / package-lock.json）

   核心作用

   | 能力     | 说明                           |
   | -------- | ------------------------------ |
   | 依赖管理 | 安装项目所需库                 |
   | 版本控制 | 锁定依赖版本                   |
   | 脚本运行 | 执行 package.json 中的 scripts |
   | 包发布   | 发布自己的 npm 包              |

2. **npx 是什么**

   **npx（Node Package Executor）** 是 npm 提供的一个工具（npm ≥ 5.2 内置），用于：

   > **直接执行 npm 包中的 CLI 工具，而无需全局安装**

   npx 解决的问题

   在没有 npx 时：

   ```bash
   npm install -g some-cli
   some-cli
   ```

   问题：
   - 污染全局环境
   - 版本冲突
   - 一次性工具也要安装

   使用 npx：

   ```bash
   npx some-cli
   ```

   优势：
   - 不需要全局安装
   - 自动下载并执行
   - 用完即可丢弃

3. **npx 执行机制**

   执行优先级：

   ```log
   1. 当前项目 node_modules/.bin
   2. 全局已安装包
   3. 远程 npm registry（临时下载）
   ```

**二、npm 和 npx 的典型用法**

npm 常用命令

1. 初始化项目

   ```bash
   npm init
   npm init -y
   ```

2. 安装依赖

   ```bash
   # 安装到项目（推荐）
   npm install lodash

   # 安装为开发依赖
   npm install --save-dev eslint
   ```

3. 全局安装

   ```bash
   npm install -g typescript
   ```

4. 卸载依赖

   ```bash
   npm uninstall lodash
   ```

5. 更新依赖

   ```bash
   npm update
   ```

6. 运行脚本

   ```bash
   npm run build
   npm run start
   ```

7. 查看依赖

   ```bash
   npm list
   npm list -g
   ```

8. 配置（企业环境常用）

   ```bash
   npm config set proxy http://host:port
   npm config set https-proxy http://host:port
   npm config set strict-ssl false
   ```

**npx 常用命令**

1. 直接运行 CLI（最常用）

   ```bash
   npx cowsay hello
   ```

2. 创建项目（脚手架工具）

   ```bash
   npx create-react-app myapp
   npx create-next-app
   ```

3. 指定版本运行（推荐）

   ```bash
   npx create-react-app@5.0.1 myapp
   ```

   避免版本不一致

4. 运行本地依赖

   ```bash
   npx eslint .
   ```

   等价于：

   ```bash
   ./node_modules/.bin/eslint .
   ```

5. 一次性工具执行

   ```bash
   npx degit user/repo project
   npx prisma migrate dev
   npx vite
   ```

6. 忽略本地版本

   ```bash
   npx --ignore-existing eslint .
   ```

7. 指定 registry（网络问题常用）

   ```bash
   npx --registry=https://registry.npmmirror.com cowsay hi
   ```

8. 自动确认（CI/CD）

   ```bash
   npx --yes some-cli
   ```

9. 传递参数

   ```bash
   npx cowsay "hello world"
   ```

**三、使用建议（实践经验）**

什么时候用 npm：

- 项目依赖管理
- 长期使用的工具
- 构建 / 编译 / 发布流程

什么时候用 npx：

- 一次性工具
- 脚手架创建项目
- 临时执行 CLI
- 避免全局污染

企业网络建议：

```bash
npm config set strict-ssl false
npm config set proxy http://proxy:port
```
