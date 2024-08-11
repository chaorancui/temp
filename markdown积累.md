### markdown 中空格
在 Markdown 文档中，可以直接采用 HTML 标记插入空格（blank space），而且无需任何其他前缀或分隔符。具体如下所示：

插入一个空格 (non-breaking space)
　　　　&nbsp;    或    &#160;     或      &#xA0;

插入两个空格 (en space)
　　　　&ensp;     或    &#8194;   或      &#x2002;
其占据的宽度正好是1/2个中文宽度，而且基本上不受字体影响。

插入四个空格 (em space)
　　　　&emsp;    或    &#8195;   或      &#x2003;
其占据的宽度正好是1个中文宽度，而且基本上不受字体影响。

插入细空格 (thin space)
　　　　&thinsp;   或     &#8201;  或      &#x2009;

　　注意：不要漏掉分号。
对于不同宽度的空格的字符实体引用表示中，en 和 em 两者均为排版单位 (typographic unit), en 的宽度是 em 宽度的一半。
在排印（typography）中，细空格(thin space)通常是宽度为 em 的 1/5 或 1/6 的空格字符。它用于添加一个狭窄的空格，例如在嵌套的引号之间或分隔相互干扰的标志符号。普通空格，即是不换行空格（Non-breaking space）。

### 使用VSCode编辑MarkDown文件（vditor 所见及所得）
https://www.cnblogs.com/springsnow/p/16256915.html
**Office Viewer(Markdown Editor)**插件
**Markdown Editor**插件



[Markdown样式自定义及详解-博客园、Typora、Markdown Nice](https://www.cnblogs.com/Sky-seeker/p/14255593.html)



markdown 插件：

> https://www.thisfaner.com/p/edit-markdown-efficiently-in-vscode/#markdown-preview-enhancedmpe-%E6%8F%92%E4%BB%B6

markdown preview enhanced 插件，部分配置项介绍：

* Enable Extended Table Syntax：打开后支持合并单元格
* 

Prettier - Code formatter 插件：

可以格式化markdown，除基本的格式化之外，它的优点是：

* 可以为 英文 和中文 之间添加空格。
* 



markdownlint 插件：自定义规则

markdownlint是一款VSCode下的markdown文件lint插件。可以格式化markdown文件。但是markdown默认的规则较多，查看markdownlint的商店介绍页面，有MD001-MD048共48条规则。其中有些规则可能是对个人不必要的，可以自定义启用的规则。

## 自定义规则的两种方式

markdownlint支持两种自定义启用规则的方式，分别是使用.markdownlint.json和使用VSCode的setting.json文件。

### 1.使用.markdownlint.json配置

> Rules can be enabled, disabled, and customized by creating a JSON file named .markdownlint.json (or .markdownlintrc) or a YAML file named .markdownlint.yaml (or .markdownlint.yml) in any directory of a project. The rules defined by .markdownlint{.json,.yaml,.yml,rc} apply to Markdown files in the same directory and any sub-directories without their own .markdownlint{.json,.yaml,.yml,rc}.

markdownlint的规则可以被使用，被警用或者自定义。只需要在项目的任意目录下新建一个名为`.markdownlint.json`的文件。`.markdownlint.json`中的配置被应用到同级和子目录下(如果子目录下不包含`.markdownlint.json`文件)的md文件。该配置文件支持`.json`,`.yaml`,`.yml`,`rc`等格式，作用是相同的。

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
第二行第三行是修改MD003的默认条件
第四行是修改markdownlint的设置
如果要忽略某个规则，例如忽略MD025，可以加上一条`"MD025: false"`,就可以禁用MD025这条规则了

### 2.使用VSCode的setting.json文件

markdownlint同时也支持在VSCode的user或workspace下的settings.json中添加markdownlint自定义配置
例如在user的setting.json下添加如下配置：

```json
"markdownlint.config": {
    "default": true,
    "MD025": false,
    "MD045": false,
    "no-hard-tabs": false
}
```

该配置就会全局生效
如果配置在workspace下的setting.json中，就对当前项目生效。
通过user和workspace下的setting.json配合可以实现一套通用的规则组合和某个项目下适用的特殊规则组合































