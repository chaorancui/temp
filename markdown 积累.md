# markdown 编辑器

## Typora

主题插件：

- blueTex：好看，推荐

## VNote

[github 仓库连接](https://github.com/vnotex/vnote)。
VNote 是一款基于 Qt 的免费开源笔记应用，**目前专注于 Markdown 语言**。VNote 旨在为用户提供一个愉悦的笔记平台和极佳的编辑体验。
VNote 不仅仅是一个简单的 Markdown 编辑器。通过提供**笔记管理功能**，VNote 让 Markdown 笔记变得更简单。未来，VNote 将支持除 Markdown 之外的更多格式。
利用 Qt，VNote 可以在 Linux、Windows 和 macOS 上运行。

优点（已体验）：笔记方式管理，支持带格式粘贴，可以同时显示文件和目录。
缺点（已体验）：markdown 特性支持较少，latex 支持都不太全。

## vscode

- **Markdown Preview Enhanced**：超级强大的 Markdown 插件，预览滑动同步、Pandoc、自定义预览 css、TOC、Latex、渲染代码运行结果（配置复杂）。
- **Markdown All in One**：Markdown 所需的一切（键盘快捷键、目录、自动预览、数学公式、列表编辑、自动补全等）。
- **PlantUML**：提供 UML 支持。如要在 markdown 中渲染，需配置 Markdown Preview Enhanced。
- **Markdown Table Prettifier**：编辑/格式化表格，将 csv 文本转化为表格。
- **Prettier - Code formatter**：主要支持前端语言，JavaScript、[JSX](https://facebook.github.io/jsx/)、[Angular](https://angular.io/)、[Vue](https://vuejs.org/)、[Flow](https://flow.org/)、[TypeScript](https://www.typescriptlang.org/)、CSS, [Less](http://lesscss.org/), and [SCSS](https://sass-lang.com/)、[HTML](https://en.wikipedia.org/wiki/HTML)、[Ember/Handlebars](https://handlebarsjs.com/)、[JSON](https://json.org/)、[GraphQL](https://graphql.org/)、[Markdown](https://commonmark.org/), including [GFM](https://github.github.com/gfm/) and [MDX v1](https://mdxjs.com/)、[YAML](https://yaml.org/)

### prettier 插件问题

> :warning: 在格式化 markdown 的时候，针对 **markdown 中的数学公式** $ $，会把 `_` 换成 `*`，原因可能是 pretteir 默认使用 `*` 进行斜体的格式化，当公式中出现多个 `_` 时，可能被语法树分析成斜体从而被改成 `*`。

**问题**：
`$$ \mu_B = \frac{1}{m} \sum_{i=1}^{m} x_i $$` 格式化成
`$$ \mu*B = \frac{1}{m} \sum*{i=1}^{m} x*i $$`

**解决方案**：

要让 Prettier 在格式化 Markdown 文件时忽略数学公式（尤其是用 `$$` 包围的块级 LaTeX 数学公式），你可以通过以下方法实现：

1. 使用 Prettier 的 `prettier-ignore` 注释

   Prettier 支持在文件中添加 `prettier-ignore` 注释，来忽略特定部分的格式化。你可以在公式的上方加上 `<!-- prettier-ignore -->` 注释，让 Prettier 跳过格式化该公式。
   Prettier 只会忽略**紧随注释的多行代码块或段落**（即**遇到空行结束**，可以包含空格或换行），其他部分仍会遵循默认的格式化规则。

   示例：

   ```markdown
   <!-- prettier-ignore -->
   添加 `prettier-ignore` 注释，下面的两行都不会被格式化。直至遇见空行。
   对于两个矩阵 $ A_{m \times p} $ 和 $ B_{p \times n} $，它们的乘积 $ C_{m \times n} = AB $ 是一个 $ m \times n $ 的矩阵。
   $$ C_{(i, j)} = \Sigma_{k=1}^n A_{(i, k)} \times B_{(k, j)} $$

   上面有空行，这里以及下面的代码会被格式化。
   $$ C*{(i, j)} = \Sigma*{k=1}^n A*{(i, k)} \times B*{(k, j)} $$
   ```

   当 Prettier 遇到这个注释时，它会跳过对这个公式的格式化。

# markdown 写作

## markdown 语言指南

- [Markdown 官方教程](https://markdown.com.cn/basic-syntax/)
  基础知识，简单易懂

- [Markdown 指南中文版](https://www.markdown.xyz/cheat-sheet/)

- [markdown emoji](https://gist.github.com/rxaviers/7360908)

- [PlantUML 一览](https://plantuml.com/zh/)
  PlantUML 是一个通用性很强的工具，可以快速、直接地创建各种图表。
- [GitBook 支持的 Markdown](https://chrisniael.gitbooks.io/gitbook-documentation/content/format/markdown.html)

- [GitHub 支持的 Markdown](https://docs.github.com/zh/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

- [Markdown 基本语法](https://hugodoit.pages.dev/zh-cn/basic-markdown-syntax/#links)

## 写作规范

- [Markdown 中文技术文档的写作规范](https://lujianan.com/2017/01/20/markdown-standard/)

- [中文技术文档写作风格指南](https://zh-style-guide.readthedocs.io/zh-cn/latest/index.html)
  语言风格、文档元素（空白、列表、表格等）、标点符号等

## LaTeX 数学公式

> 好多 markdown 编辑器仅支持最简单的行内行间公式，不支持复杂的 LaTeX 公式对齐，公式编号等语法。

- [LaTeX 数学公式大全](https://blogbook.eu.org/post/LaTeX%20Mathematical%20formula/)

- [通用 LaTeX 数学公式语法手册](http://www.uinio.com/Math/LaTex/)
  数学符号及公式（网页加载巨慢 -\_-!）

- [LaTeX mathematical symbols](https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols)
  LaTex 数学符号，无公式

- [TeXPage 文档中心 - 排版数学公式](https://www.texpage.com/docs/zh/learning/chapter-4/)
- [latex 入门-简版-刘海洋](https://lrita.github.io/images/wiki/latex%E5%85%A5%E9%97%A8-%E7%AE%80%E7%89%88-%E5%88%98%E6%B5%B7%E6%B4%8B.pdf)

## markdown 使用记录

### 不同宽度的空格

1. **插入一个空格 (Non-breaking space) / 空行**

   用途：
   - 用于防止文本在换行时被拆分。例如：在网页中需要保证某些词组不被断开。
   - 插入空行

   对应的 HTML 实体：
   - `&nbsp;`
   - `&#160;`、`&#xA0;`

   **效果**：「Hello&nbsp;World」（“Hello”和“World”之间有一个空格，且不会在换行时分开。）

2. **插入两个空格 (En space)**

   用途：
   - 宽度约为 1/2 个中文字符的宽度，常用于排版时控制文本的对齐和间距。

   对应的 HTML 实体：
   - `&ensp;`
   - `&#8194;`、`&#x2002;`

   **效果**：「Hello&ensp;World」（两个空格宽度，相当于 1/2 个中文字符的宽度。）

3. **插入四个空格 (Em space)**

   用途：
   - 宽度等于一个中文字符的宽度，通常用于需要较大间隔的场景，比如在中文排版中创建较大的空隙。

   对应的 HTML 实体：
   - `&emsp;`
   - `&#8195;`、`&#x2003;`

   **效果**：「Hello&emsp;World」（四个空格宽度，相当于一个中文字符的宽度。）

4. **插入细空格 (Thin space)**

   用途：
   - 比普通空格小，用于精细排版，尤其是数字和符号之间的小间距。

   对应的 HTML 实体：
   - `&thinsp;`
   - `&#8201;`、`&#x2009;`

   **效果**：「$10&thinsp;000」（数字之间插入一个细空格，空隙较小。）

**注意**：

- 不要漏掉分号。
- 对于不同宽度的空格的字符实体引用表示中，en 和 em 两者均为排版单位 (typographic unit), en 的宽度是 em 宽度的一半。
- 在排印（typography）中，细空格(thin space)通常是宽度为 em 的 1/5 或 1/6 的空格字符。它用于添加一个狭窄的空格，例如在嵌套的引号之间或分隔相互干扰的标志符号。普通空格，即是不换行空格（Non-breaking space）。

**总结**：

| 空格类型               | HTML 实体                          | 代码示例           | 结果示例         |
| ---------------------- | ---------------------------------- | ------------------ | ---------------- |
| **Non-breaking space** | `&nbsp;` / `&#160;` /`&#xA0;`      | `Hello&nbsp;World` | Hello&nbsp;World |
| **En space**           | `&ensp;` / `&#8194;` / `&#x2002;`  | `Hello&ensp;World` | Hello&ensp;World |
| **Em space**           | `&emsp;` / `&#8195;` / `&#x2003;`  | `Hello&emsp;World` | Hello&emsp;World |
| **Thin space**         | `&thinsp;` / `&#8201;` /`&#x2009;` | `$10&thinsp;000`   | $10&thinsp;000   |

### emoji

> 查询网站：<https://gist.github.com/rxaviers/7360908>
>
> code：`::`

- 未完成的事情

  :hourglass: 这个任务还未完成。code：`:hourglass:`

  :exclamation: ​ 这项工作仍然在进行中。code：`:exclamation:`

  :calendar: 记得下周完成此任务。code：`:calendar:`

- 解释说明

  ️:page_with_curl: **说明**：这是一些重要的信息说明。code：`:page_with_curl:`

  :bulb: **提示**：这里有一个提示，可以帮助你更好地理解内容。code：`:bulb:`

  :bell: **提示**：这里有一个提示，可以帮助你更好地理解内容。code：`:bell:`

- 扩展阅读

  :book: **扩展阅读**：你可以阅读《深入了解 Markdown》这本书来获取更多信息。code：`:book:`

  :link: **更多内容**：[点击这里查看相关资料](https://gist.github.com/rxaviers/7360908)。code：`:link:`

  :pencil: **分析/总结/附加**：这里是一些可选的分析/总结/附加内容，或总结内容。code：`:pencil:` 或 `:momo:`

- 存疑/进一步确认

  :question: 这个数据的准确性尚存疑，需要进一步验证。code：`:question:`

  :exclamation: 请注意，这个问题还需要进一步调查。code：`:exclamation:`

- 注意

  :warning:️ 请注意：此操作可能导致数据丢失。code：`:warning:`

  :exclamation: 重要提醒：请在继续之前备份您的文件。code：`:exclamation:`

- 强调

  :pushpin: ​**重要**：这是重要的强调信息，提示隐藏的关键内容。code：`:pushpin:`

  :zap: **强调**：请注意这个特别标注的信息。code：`:zap:`

- 条目

  :small_orange_diamond: ​code：`:small_orange_diamond:`

  :large_orange_diamond: code：`:large_orange_diamond:`

  :small_blue_diamond: code：`:small_blue_diamond:`

  :large_blue_diamond: code：`:large_blue_diamond:`

### Unicode

在 Markdown 中，可以通过直接输入 Unicode 字符的编号来显示特定字符。方法如下：

1. **直接复制粘贴 Unicode 字符**：
   如果知道需要的字符，可以直接从 [Unicode 表](https://unicode-table.com/) 等资源网站上复制字符，然后粘贴到 Markdown 文档中。例如，复制并粘贴 Unicode 字符 `␣` (U+2423) 代表“空格符号”。

2. **使用 HTML 十六进制或十进制代码**：
   在 Markdown 中，使用 HTML 的十六进制（`&#x...;`）或十进制代码（`&#...;`）来表示 Unicode 字符。例如：
   - 十六进制写法：

     ```markdown
     &#x2423; <!-- 会显示为␣ -->
     ```

     如：==x&#x2423;\_pos==。

   - 十进制写法：

     ```markdown
     &#9251; <!-- 会显示为␣ -->
     ```

     如：==x&#9251;\_pos==。

3. **使用 LaTeX 语法（适用于支持 LaTeX 的 Markdown 渲染器）**：
   如果 Markdown 渲染器支持 LaTeX 表达式，某些 Unicode 字符可以通过 LaTeX 语法来呈现，但支持较少，不如直接使用 HTML 代码稳定。

通过这种方式，你可以在 Markdown 中插入任意 Unicode 字符，只要确保你的渲染器或编辑器支持 HTML 编码。

### 强调

| 样式名   | 效果                     | Markdown                                                                                                                      |
| -------- | ------------------------ | :---------------------------------------------------------------------------------------------------------------------------- |
| 加粗     | **文本**                 | `**文本**` 或 `__文本__` 或 `<b>文本</b>`，用两个 `*` 或两个 `_` 或 `<b>` 包围文本                                            |
| 斜体     | _文本_                   | `*文本*` 或 `_文本_` 或 `<em>文本</em>`，用一个 `*` 或一个 `_` 或 `<em>` 包围文本                                             |
| 删除线   | ~~文本~~ <del>文本</del> | `~~文本~~` 或 `<del>文本</del>`                                                                                               |
| 下划线   | <u>文本</u>              | `<u>文本</u>`，Markdown 自身没有实现下划线，但它是 HTML 的子集，实现了`<u>`标签。<br>一般文本建议不要加下划线，容易误会成链接 |
| 上标     | 文本^上标^               | `文本^上标^`                                                                                                                  |
| 下标     | 文本~下标~               | `文本~下标~`                                                                                                                  |
| 小号字体 | <small>小号字体</small>  | `<small>小号字体</small>`                                                                                                     |
| 大号字体 | <big>大号字体</big>      | `<big>大号字体</big>`                                                                                                         |
| 键盘文本 | <kbd>Ctrl</kbd>          | `<kbd>Ctrl</kbd>`                                                                                                             |

注：删除线用~~括起来是不规范语法，有的 md 编辑器并不支持，比如：MarkdownPad2 中的 Markdown(扩展)模式就不行，但其 github 风格则可以，这里 CSDN 也支持。参考：[Markdown 语法](https://blog.csdn.net/frank_0713/article/details/80878883)

### 定位标记

参考：[基本格式语法 -> 章节链接](https://docs.github.com/zh/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#section-links)

Markdown 中定位标记使你可以跳至同一页面上的指定锚点。用法如下：

```markdown
跳转的链接，语法和普通链接的语法一样，区别就是括号内的链接以 `#` 起始。
[链接说明文字](#jump_pos)
```

如果需要确定要编辑的文件中标题的定位点，可使用以下基本规则：

- 字母转换成小写形式。
- 空格由连字符 (`-`) 代替。 任何其他空格或标点符号都将被删除，**数字之间的 `.` 会变成 `-`**。
- 前导和尾随空格被删除。
- 标记格式被删除，只保留内容（例如，`_italics_` 变为 `italics`）。
- 如果标题的自动生成的定位点与同一文档中的早期定位点相同，那么通过追加连字符和自动递增整数来生成唯一标识符。

例如：[点击跳转到文件开头](#markdown-编辑器)，其代码为 `[点击跳转到文件开头](#markdown-编辑器)`。

### 图片居中且调整比例

```markdown
<div style="text-align: center">
<img src="xxx.png" style="width: 70%">
</div>
```

### plantuml

<https://pdf.plantuml.net/PlantUML_Language_Reference_Guide_zh.pdf>

### Prettier

Prettier - Code formatter 插件：

可以格式化 markdown，除基本的格式化之外，它的优点是：

- 可以为 英文 和中文 之间添加空格。
-

## markdownlint 自定义规则

markdownlint 是一款 VSCode 下的 markdown 文件 lint 插件。可以格式化 markdown 文件。但是 markdown 默认的规则较多，查看 markdownlint 的商店介绍页面，有 MD001-MD048 共 48 条规则。其中有些规则可能是对个人不必要的，可以自定义启用的规则。

markdownlint 支持两种自定义启用规则的方式，分别是使用.markdownlint.json 和使用 VSCode 的 setting.json 文件。

1. 使用 `.markdownlint.json` 配置

   > Rules can be enabled, disabled, and customized by creating a JSON file named .markdownlint.json (or .markdownlintrc) or a YAML file named .markdownlint.yaml (or .markdownlint.yml) in any directory of a project. The rules defined by .markdownlint{.json,.yaml,.yml,rc} apply to Markdown files in the same directory and any sub-directories without their own .markdownlint{.json,.yaml,.yml,rc}.

   markdownlint 的规则可以被使用，被警用或者自定义。只需要在项目的任意目录下新建一个名为`.markdownlint.json`的文件。`.markdownlint.json`中的配置被应用到同级和子目录下(如果子目录下不包含`.markdownlint.json`文件)的 md 文件。该配置文件支持`.json`,`.yaml`,`.yml`,`rc`等格式，作用是相同的。

   在`.markdownlint.json`中可以定义如下配置：

   ```json
   {
     "default": true,
     "MD003": { "style": "atx_closed" },
     "MD007": { "indent": 4 },
     "no-hard-tabs": false
   }
   ```

   第一行是使用默认规则
   第二行第三行是修改 MD003 的默认条件
   第四行是修改 markdownlint 的设置
   如果要忽略某个规则，例如忽略 MD025，可以加上一条`"MD025: false"`,就可以禁用 MD025 这条规则了

2. 使用 VSCode 的 `setting.json` 文件

   markdownlint 同时也支持在 VSCode 的 user 或 workspace 下的 settings.json 中添加 markdownlint 自定义配置
   例如在 user 的 setting.json 下添加如下配置：

   ```json
       "markdownlint.config": {
           "default": true,
           "MD004": {
               "style": "dash"
           },
           "MD007": {
               "indent": 2
           },
           "MD012": false,
           "MD013": false,  // 禁用行长限制规则
           "MD024": false,  // 禁用重复标题
           "MD033": false,  // 禁用HTML标签内的警告
           "MD041": false, // 禁用首行应该为top-level标题
       },
   ```

   该配置就会全局生效
   如果配置在 workspace 下的 setting.json 中，就对当前项目生效。
   通过 user 和 workspace 下的 setting.json 配合可以实现一套通用的规则组合和某个项目下适用的特殊规则组合

# 图片管理

## 几种图片管理方式

在 GitHub 上通过 Markdown 维护 Wiki 并发布博客时，图片管理确实是最容易让人“劝退”的环节。为了平衡**方便程度**和**维护成本**，这里推荐几种主流的解决方案：

1. 纯 Git 管理方案（最省事）

   如果你不想引入额外的工具，直接利用 Git 仓库本身的存储能力是最简单的方式。
   - **操作方式**：在你的博客仓库根目录下建立一个 `assets/` 或 `images/` 文件夹。
   - **引用方式**：使用相对路径引用，例如 `![描述](./assets/my-photo.png)`。
   - **进阶优化**：
     - **使用 jsDelivr 加速**：GitHub 的原生图片在国内加载较慢。你可以将图片路径替换为 CDN 路径，例如：`https://cdn.jsdelivr.net/gh/你的用户名/仓库名/assets/my-photo.png`。
     - **利用 GitHub Actions**：设置一个自动化脚本，在推送代码时自动压缩图片体积，防止仓库过快膨胀。

2. “图床”工具自动化（最高效）

   这是目前 Markdown 创作者的主流选择。通过专门的工具，实现“截图 -> 上传 -> 自动返回 Markdown 链接”的一键操作。
   - **核心工具：PicGo**
     - **PicGo (GUI)**：支持拖拽上传和剪贴板上传，支持 GitHub、阿里云 OSS、腾讯云 COS 等多种存储后端。
     - **PicGo-Core (CLI)**：如果你习惯在终端或编辑器中工作，CLI 版本可以集成到各种流程中。
   - **存储后端选择**：
     - **GitHub 仓库**：免费，但大图多了会影响仓库性能。
     - **对象存储 (S3/OSS/COS)**：极其稳定且速度快，通常有免费额度或极低的存储费用。

3. GitHub Issues “借鸡生蛋”法

   这是一种非典型但异常方便的黑客手法，适合不想折腾任何配置的人。
   1. 打开你的博客仓库的 **Issues** 页面。
   2. 新建一个 Issue（不用发布），直接将图片**拖拽**进对话框。
   3. GitHub 会自动上传图片并生成一个官方域名（如 `user-images.githubusercontent.com`）的 Markdown 链接。
   4. 直接复制这个链接到你的 Wiki 文档中。
      - _优点_：图片永久托管在 GitHub CDN 上，不占用你本地仓库的体积。

4. 体系化管理方案：SSG 静态网站生成器

   如果你觉得手动管理 Wiki 和博客太零散，可以考虑使用成熟的静态网站框架，它们对图片资源有标准化的处理逻辑。
   - **Hugo / Astro**：这两个框架目前性能极佳。它们支持 **Page Bundles** 模式，即一个文件夹里放一个 `.md` 文件和它所需的所有图片。这种方式让你的博客内容和素材“同生共死”，迁移起来非常方便。
   - **Obsidian + GitHub Publisher**：如果你使用 Obsidian 写笔记，可以通过插件一键将带有本地图片的笔记转换并发布到 GitHub。

方案对比

| 方案               | 优点                       | 缺点                           | 推荐人群                 |
| ------------------ | -------------------------- | ------------------------------ | ------------------------ |
| **本地相对路径**   | 简单、离线可用、不依赖外链 | 仓库体积增长快、国内加载慢     | 追求极简、图片不多的用户 |
| **PicGo + 云存储** | 速度快、配置好后一劳永逸   | 需要初次配置、可能产生微量费用 | 重度博主、开发者         |
| **GitHub Issues**  | 零配置、白嫖 CDN 流量      | 无法离线预览、图片管理零散     | 偶尔发文、图省事的用户   |
| **Hugo/Astro**     | 架构专业、扩展性极强       | 有一定的学习曲线               | 想长期经营技术博客的用户 |

## 静态网站框架 Hugo

> 选择 Hugo，并配合“Page Bundles（页面包）”模式管理图片。

对于开发者（特别是习惯键盘驱动、追求工具链简洁的用户）来说，Hugo 的体验会比 Hexo 好很多。

1. Hugo vs Hexo
   相比于 Hexo，Hugo 有以下核心优势：
   - **零依赖（Single Binary）**：Hugo 是用 Go 写的，只有一个二进制文件。你不需要安装 Node.js、不需要配置 npm 镜像、不需要担心依赖版本冲突。
   - **极致性能**：Hugo 的构建速度通常比 Hexo 快两个数量级。对于几百篇博文的 Wiki，Hexo 可能需要几十秒，而 Hugo 几乎是毫秒级瞬间完成，这在本地预览（Live Reload）时体验极佳。
   - **图片管理的“正选”方案：Page Bundles**：这是 Hugo 击败 Hexo 的杀手锏，下文详细展开。

2. 完美的图片管理方案：Page Bundles（即一文一文件夹）

   在 Hexo 中，图片通常放在 `source/images` 或开启 `post_asset_folder` 后产生的散乱文件夹里。

   Hugo 的 **Page Bundles** 允许你这样组织内容：

   ```log
   content/
   └── posts/
       └── my-awesome-npu-optimization/   <-- 一个文件夹就是一个页面
           ├── index.md                   <-- 你的博文/Wiki内容
           ├── diagram.png                <-- 相关的图片
           └── profile.jpg
   ```

   - **引用非常简单**：在 `index.md` 里直接写 `![架构图](diagram.png)` 即可，无需考虑复杂的路径。
   - **高便携性**：如果你想移动这篇文章，直接剪切整个文件夹即可，图片永远跟着文档走，不会出现“断链”。
   - **自动优化**：Hugo 内置了强大的图像处理引擎，可以在构建时自动帮你压缩、调整图片大小或转换格式（如 WebP），而不需要你手动处理。

## Hugo 使用

Hugo 是目前世界上最快的静态网站生成器（SSG）。如果说 Hexo 是用 JavaScript 搭建的精巧积木，那么 Hugo 就是用 Go 语言锻造的一把瑞士军刀——**极速、单文件、无依赖**。

1. Hugo 核心特点
   - **构建极快**：毫秒级的渲染速度，即便有上千篇文章，构建通常也不超过几秒。
   - **单二进制文件**：不需要安装 Node.js、Ruby 或 Python 环境，下载一个 `.exe` 或 `.bin` 就能跑。
   - **内容驱动**：完美支持 Markdown，并提供强大的“Shortcodes”功能来扩展功能（如插入视频、推文等）。

2. 安装 Hugo

   > 推荐安装 **Extended 版本**（支持 Sass/SCSS）
   - 二进制安装：去 [Hugo GitHub Releases](https://github.com/gohugoio/hugo/releases) 下载最新的二进制包。
   - 命令行安装：

     ```bash
     # ubuntu
     sudo apt update
     sudo apt install hugo

     # Windows 终端，推荐用 `Scoop`
     scoop install hugo-extended
     ```

3. 主要命令用法

   | **命令**                     | **用途**                                     |
   | ---------------------------- | -------------------------------------------- |
   | `hugo new site [name]`       | 初始化一个新的站点目录                       |
   | `hugo new [path/to/file.md]` | 新建一篇文章（会自动填充 Front Matter 模板） |
   | `hugo server -D`             | 启动本地预览模式（`-D` 表示包含草稿文章）    |
   | `hugo`                       | 执行最终构建，生成 `public/` 静态文件夹      |
   | `hugo list drafts`           | 列出所有草稿                                 |

4. 从零到一：搭建博客全流程

   **第一步：创建站点**

   在你的工作目录下执行：

   ```bash
   hugo new site my-wiki
   cd my-wiki
   ```

   **第二步：添加主题**

   Hugo 本身不带主题。我们以极简且强大的 **PaperMod** 为例（非常适合做 Wiki）：

   ```bash
   git init
   git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
   ```

   然后在 `hugo.toml` (或 `config.toml`) 中指定主题：

   ```toml
   theme = "PaperMod"
   ```

   **第三步：配置站点**

   修改根目录下的 `hugo.toml`。这是 Hugo 的“大脑”：

   ```toml
   baseURL = "https://yourname.github.io/"
   languageCode = "zh-cn"
   title = "我的技术 Wiki"
   theme = "PaperMod"

   [params]
       defaultTheme = "auto" # 自动切换深色/浅色模式
       showCodeCopyButtons = true # 显示代码复制按钮
   ```

   **第四步：创建内容（Page Bundles 模式）**

   为了方便管理图片，我们不直接创建 `.md` 文件，而是创建**文件夹**：

   ```bash
   # 创建一个名为 "npu-optimization" 的页面包
   hugo new posts/npu-optimization/index.md
   ```

   此时目录结构如下：

   ```log
   content/
   └── posts/
       └── npu-optimization/
           ├── index.md      <-- 编辑这里
           └── my-npu-diag.png  <-- 直接把图丢进这里
   ```

   在 `index.md` 中引用图片：

   ```markdown
   ---
   title: "NPU 算子优化笔记"
   date: 2026-04-09
   draft: false
   ---

   这是我的优化思路：
   ![架构图](my-npu-diag.png)
   ```

   **第五步：预览与构建**

   运行预览服务：

   ```bash
   hugo server -D
   ```

   打开浏览器访问 `http://localhost:1313`。当你修改 Markdown 时，页面会实时刷新。

   **第六步：发布到 GitHub**
   1. 执行 `hugo` 命令，生成的 `public/` 目录就是整个静态网站。
   2. **更省事的方法**：不要手动部署。直接把整个 Hugo 源码仓库推送到 GitHub，并在仓库设置中开启 **GitHub Actions**，选择 Hugo 官方提供的部署模板。
   3. 小贴士：如何让写 Wiki 更爽？
      - **关于 Proxy**：如果你在公司内部网络，`git submodule` 可能会失败。记得配置好 Git 代理或使用内部镜像源。
      - **关于 Neovim**：建议给 `index.md` 设置一个快捷键，配合 `hugo server`。你甚至可以写一个简单的脚本，在 Neovim 保存时自动触发 Git 提交。
      - **F13 键位**：既然你喜欢 87% 键盘，可以把 F13 映射为一键启动 `hugo server` 的脚本，极大提升 Wiki 维护的幸福感。
