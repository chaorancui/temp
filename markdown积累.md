## markdown 编辑器

### Typora

主题插件：

- blueTex：好看，推荐

### vscode

插件：

- prettier：

  使用此扩展配置 Prettier 有多种方式。您可以使用[VS Code 设置](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode#prettier-settings)、[Prettier 配置文件](https://prettier.io/docs/en/configuration.html)或`.editorconfig`文件。VS Code 设置旨在用作后备，通常仅用于非项目文件。**建议您始终在项目中包含一个 Prettier 配置文件，指定项目的所有设置**。这将确保无论您如何运行 Prettier（从此扩展、从 CLI 或从另一个带有 Prettier 的 IDE），都将应用相同的设置。

  建议使用[Prettier 配置文件](https://prettier.io/docs/en/configuration.html)来设置格式化选项。选项从正在格式化的文件开始递归搜索，因此如果您想将 Prettier 设置应用于整个项目，只需在根目录中设置配置即可。配置选项参考：[Options](https://prettier.io/docs/en/options.html)。

  在项目目录下新增文件 `.prettierrc.json`，内容如下：

  ```json
  {
    "//参考网址": "https://prettier.io/docs/en/options",
    "//printWidth": "默认 80",
    "printWidth": 120,
    "//tabWidth": "默认 2",
    "tabWidth": 2,
    "//useTabs": "默认 false",
    "useTabs": false,
    "//semi": "默认 false",
    "semi": false,
    "//singleQuote": "默认 false",
    "singleQuote": false,
    "//quoteProps": "默认 as-needed",
    "quoteProps": "as-needed",
    "//trailingComma": "默认 all",
    "trailingComma": "es5",
    "//bracketSpacing": "默认 true",
    "bracketSpacing": true,
    "//bracketSameLine": "默认 true",
    "bracketSameLine": false,
    "//arrowParens": "默认 always",
    "arrowParens": "always",
    "//proseWrap": "默认 preserve",
    "proseWrap": "preserve",
    "//endOfLine": "默认 lf",
    "endOfLine": "lf",
    "//embeddedLanguageFormatting": "默认 auto",
    "embeddedLanguageFormatting": "auto"
  }
  ```

  > :warning: 问题：在格式化 markdown 的时候，针对 markdown 中的公式 $ $，会把 `_` 换成 `*`，原因可能是 pretteir 默认使用 `*` 进行斜体的格式化，当公式中出现多个 `_` 时，可能被语法树分析成斜体从而被改成 `*`。问题如：
  >
  > `$$ \mu_B = \frac{1}{m} \sum_{i=1}^{m} x_i $$` 格式化成
  >
  > `$$ \mu*B = \frac{1}{m} \sum*{i=1}^{m} x*i $$`

## prettier 插件

要让 Prettier 在格式化 Markdown 文件时忽略数学公式（尤其是用 `$$` 包围的块级 LaTeX 数学公式），你可以通过以下几种方法实现：

### 使用 Prettier 的 `prettier-ignore` 注释

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

### 修改 Prettier 配置文件

目前，Prettier 并没有内置的选项来自动跳过 Markdown 中的数学公式。不过，可以通过结合 `remark` 插件来实现更细粒度的控制。你可以自己编写或使用现有的 `remark` 插件，来处理 Markdown 中的数学公式部分，并跳过对它们的格式化。

### 使用 `remark-math` 插件与 Prettier 配合

`remark-math` 是一个 `remark` 插件，它能够识别并处理 Markdown 中的数学公式。你可以使用它配合 Prettier 一起工作。

**步骤**：

1. 安装 `remark-math` 和 `remark-html-katex`（用于将数学公式转换成可视化效果）：

   ```bash
   npm install remark-math remark-html-katex
   ```

2. 在 Prettier 的配置文件中添加自定义的 `remark` 配置，以识别数学公式并跳过它们的格式化：

   ```javascript
   const remarkMath = require("remark-math");
   const remarkHtmlKatex = require("remark-html-katex");

   module.exports = {
     plugins: [
       // 使用 remark-math 插件来处理数学公式
       {
         name: "markdown",
         parse: "markdown",
         plugins: [remarkMath, remarkHtmlKatex],
       },
     ],
   };
   ```

3. 将公式用 `$$` 或 `$` 包围，Prettier 将能够识别出这些公式，并通过插件处理它们，而不会对公式内容进行重新格式化。

示例：

```markdown
Here is an inline formula: $E = mc^2$

Here is a block formula:

$$
a^2 + b^2 = c^2
$$
```

通过 `remark-math` 插件，Prettier 不会对这些数学公式的内容进行重新排版和格式化，而是保持公式原有的样式。

### 4. 使用 `.prettierignore` 文件（全局忽略）

如果你想完全避免 Prettier 格式化某些 Markdown 文件（或特定类型的文件），你可以使用 `.prettierignore` 文件来忽略这些文件的格式化。这对于包含大量数学公式的文件可能是一个简单的解决方案。

示例：

在项目根目录下创建一个 `.prettierignore` 文件，并添加你要忽略的 Markdown 文件路径：

```bash
# .prettierignore
docs/math-heavy-file.md
```

这种方法适用于需要跳过特定文件的情况，而不是局部忽略公式的格式化。

### 总结

- **局部忽略**：使用 `<!-- prettier-ignore -->` 注释跳过某个数学公式的格式化。
- **插件方式**：使用 `remark-math` 插件结合 Prettier，让 Prettier 识别数学公式并跳过其格式化。
- **全局忽略**：通过 `.prettierignore` 文件，忽略某些特定的 Markdown 文件的格式化。

选择其中一种方法可以帮助你控制 Prettier 对 Markdown 文件中数学公式的处理方式。

## markdown 写作

### 一些链接

#### markdown 语言指南

- [Markdown 官方教程](https://markdown.com.cn/basic-syntax/)
  基础知识，简单易懂

- [Markdown 指南中文版](https://www.markdown.xyz/cheat-sheet/)

- [markdown emoji](https://gist.github.com/rxaviers/7360908)

- [PlantUML 一览](https://plantuml.com/zh/)
  PlantUML 是一个通用性很强的工具，可以快速、直接地创建各种图表。
- [GitBook 支持的 Markdown](https://chrisniael.gitbooks.io/gitbook-documentation/content/format/markdown.html)

- [GitHub 支持的 Markdown](https://docs.github.com/zh/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

- [Markdown 基本语法](https://hugodoit.pages.dev/zh-cn/basic-markdown-syntax/#links)

#### 写作规范

- [Markdown 中文技术文档的写作规范](https://lujianan.com/2017/01/20/markdown-standard/)

- [中文技术文档写作风格指南](https://zh-style-guide.readthedocs.io/zh-cn/latest/index.html)
  语言风格、文档元素（空白、列表、表格等）、标点符号等

#### LaTeX 数学公式

> 好多 markdown 编辑器仅支持最简单的行内行间公式，不支持复杂的 LaTeX 公式对齐，公式编号等语法。

- [LaTeX 数学公式大全](https://blogbook.eu.org/post/LaTeX%20Mathematical%20formula/)

- [通用 LaTeX 数学公式语法手册](http://www.uinio.com/Math/LaTex/)
  数学符号及公式（网页加载巨慢 -\_-!）

- [LaTeX mathematical symbols](https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols)
  LaTex 数学符号，无公式

- [TeXPage 文档中心 - 排版数学公式](https://www.texpage.com/docs/zh/learning/chapter-4/)
- [latex 入门-简版-刘海洋](https://lrita.github.io/images/wiki/latex%E5%85%A5%E9%97%A8-%E7%AE%80%E7%89%88-%E5%88%98%E6%B5%B7%E6%B4%8B.pdf)

### 空格

在 Markdown 文档中，可以直接采用 HTML 标记插入空格（blank space），而且无需任何其他前缀或分隔符。具体如下所示：

插入一个空格 (non-breaking space)
　　　　&nbsp; 或 &#160; 或 &#xA0;

插入两个空格 (en space)
　　　　&ensp; 或 &#8194; 或 &#x2002;
其占据的宽度正好是 1/2 个中文宽度，而且基本上不受字体影响。

插入四个空格 (em space)
　　　　&emsp; 或 &#8195; 或 &#x2003;
其占据的宽度正好是 1 个中文宽度，而且基本上不受字体影响。

插入细空格 (thin space)
　　　　&thinsp; 或 &#8201; 或 &#x2009;

注意：不要漏掉分号。
对于不同宽度的空格的字符实体引用表示中，en 和 em 两者均为排版单位 (typographic unit), en 的宽度是 em 宽度的一半。
在排印（typography）中，细空格(thin space)通常是宽度为 em 的 1/5 或 1/6 的空格字符。它用于添加一个狭窄的空格，例如在嵌套的引号之间或分隔相互干扰的标志符号。普通空格，即是不换行空格（Non-breaking space）。

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

  :pencil: **分析/总结/附加**：这里是一些可选的分析/总结/附加内容，或总结内容。code：`或`:momo:`

- 存疑/进一步确认

  :question: 这个数据的准确性尚存疑，需要进一步验证。code：`:question:`

  :exclamation: 请注意，这个问题还需要进一步调查。code：`:exclamation:`

- 注意

  :warning:️ 请注意：此操作可能导致数据丢失。code：`:warning:`

  :exclamation: 重要提醒：请在继续之前备份您的文件。code：`:exclamation:`

- 强调

  :pushpin: ​**重要**：这是重要的强调信息，提示隐藏的关键内容。code：`:pushpin:`

  :zap: **强调**：请注意这个特别标注的信息。code：`:zap:`

### 强调

| 样式名   | 效果                     | Markdown                                                                                                                      |
| -------- | ------------------------ | :---------------------------------------------------------------------------------------------------------------------------- |
| 加粗     | **文本**                 | `**文本** 或 __文本__ 或 <strong>文本</strong>`，用两个`*`或两个`_`包围文本                                                   |
| 斜体     | _文本_                   | `*文本* 或 _文本_ 或 <em>文本</em>`，用一个`*`或一个`_`包围文本                                                               |
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
- 空格由连字符 (`-`) 代替。 任何其他空格或标点符号都将被删除。
- 前导和尾随空格被删除。
- 标记格式被删除，只保留内容（例如，`_italics_` 变为 `italics`）。
- 如果标题的自动生成的定位点与同一文档中的早期定位点相同，那么通过追加连字符和自动递增整数来生成唯一标识符。

例如：[点击跳转到文件开头](#markdown-编辑器)，其代码为 `[点击跳转到文件开头](#markdown-编辑器)`。

### 使用 VSCode 编辑 MarkDown 文件（vditor 所见及所得）

<https://www.cnblogs.com/springsnow/p/16256915.html>

**Office Viewer(Markdown Editor)**插件
**Markdown Editor**插件

[Markdown 样式自定义及详解-博客园、Typora、Markdown Nice](https://www.cnblogs.com/Sky-seeker/p/14255593.html)

[Markdown 写作心得](https://wu-kan.cn/2020/01/18/Markdown%E5%86%99%E4%BD%9C%E5%BF%83%E5%BE%97/)

markdown 插件：

> <https://www.thisfaner.com/p/edit-markdown-efficiently-in-vscode/#markdown-preview-enhancedmpe-%E6%8F%92%E4%BB%B6>

markdown preview enhanced 插件，部分配置项介绍：

- Enable Extended Table Syntax：打开后支持合并单元格
-

Prettier - Code formatter 插件：

可以格式化 markdown，除基本的格式化之外，它的优点是：

- 可以为 英文 和中文 之间添加空格。
-

markdownlint 插件：自定义规则

markdownlint 是一款 VSCode 下的 markdown 文件 lint 插件。可以格式化 markdown 文件。但是 markdown 默认的规则较多，查看 markdownlint 的商店介绍页面，有 MD001-MD048 共 48 条规则。其中有些规则可能是对个人不必要的，可以自定义启用的规则。

## 自定义规则的两种方式

markdownlint 支持两种自定义启用规则的方式，分别是使用.markdownlint.json 和使用 VSCode 的 setting.json 文件。

### 1.使用.markdownlint.json 配置

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

### 2.使用 VSCode 的 setting.json 文件

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
    "MD033": false,  // 禁用HTML标签内的警告
    "MD032": false,   // 禁用列表上下有空行
    "MD041": false, // 禁用首行应该为top-level标题
},
```

该配置就会全局生效
如果配置在 workspace 下的 setting.json 中，就对当前项目生效。
通过 user 和 workspace 下的 setting.json 配合可以实现一套通用的规则组合和某个项目下适用的特殊规则组合
