[toc]

## git 技巧

### 导出/应用 patch

有时候需要一个代码仓导出差异，然后应用到另一个代码仓。有两种常用的方法可以实现这个需求:

1. **普通格式补丁**：使用 git diff 和 git apply

   ```bash
   # 工作区未提交的更改导出为一个 patch 文件
   git diff > changes.patch

   # 在目标仓库中应用 patch
   git apply changes.patch
   ```

2. **邮件格式补丁**：使用 git format-patch 和 git am

   ```bash
   # 在源仓库生成格式化的 patch
   git format-patch HEAD~1  # 最近一次提交的改动
   # 或从指定提交开始的最近三个提交，省略<commit_id>默认为最近的三个提交
   git format-patch -3 <commit_id>
   # 或者指定提交范围
   git format-patch <start-commit>..<end-commit> # 包含头尾

   # 在目标仓库应用改动
   git am < 0001-commit-message.patch
   ```

   - `-o` 选项指定 patch 保存目录：`git format-patch -3 -o /path/to/patches/`

git format-patch 相比 git diff 的**优势是可以保留提交信息和作者信息**。

### 应用 patch 冲突

**冲突报错**：

直接应用 patch 有时候会失败，

```log
warning: xxx.xxx has type xxx, expected xxx
error: patch failed: xxx
error: xxx: patch does not apply
```

原因可能如下：

- 目标文件的内容已经被修改，和补丁中的内容不匹配。
- 补丁的上下文（即修改所在的行号或内容）发生了变化，导致无法应用。

**解决方法**：

1. 使用 git apply 时可以尝试 --reject 参数

   ```bash
   git apply --reject xxx.patch
   ```

   这会在冲突文件旁生成 `.rej` 文件，表示无法应用的补丁部分，然后需要手动查看 `.rej` 文件，手动把未应用的部分修改到目标文件上。`.rej` 文件较大时不适用。

2. wiggle 命令处理 .rej 文件

   wiggle 是一个用于解决 git apply 生成的 .rej 文件中的冲突并自动合并的工具。它可以帮助你将补丁文件应用到目标文件，并且自动解决冲突，避免手动编辑 .rej 文件的繁琐过程。

   wiggle 的作用
   当 git apply 无法应用补丁时，它会生成 .rej 文件，其中包含无法应用的部分。wiggle 的作用就是帮助你自动合并这些无法应用的部分，尤其是在补丁冲突时，能够自动尝试进行三方合并。它会尝试使用文件中的上下文来自动解决冲突，而无需你手动干预。

### git 仓库忽略大小写

```bash
git config core.ignorecase true
```

### 调整 commit 之间顺序

1. 使用 `git rebase -i` 进入编辑

   ```shell
   git rebase -i <after-this-commit> # 不含本次commit id
   git rebase -i HEAD~3
   ```

2. vim 命令模式（Command mode），调整 commit id 的`行的顺序`。dd 剪切，p 粘贴（后），P 粘贴（前）。

3. 编辑完成之后，:wq 退出编辑模式，即可完成 commit 顺序的调整。

> 注：若这个提交有先后依赖关系，则不会成功。
>
> 参考网址：[7.6 Git 工具 - 重写历史](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E9%87%8D%E5%86%99%E5%8E%86%E5%8F%B2)
>
> [git rebase 调整 commit 之间顺序](https://blog.csdn.net/allanGold/article/details/92836941)

### Git 修改已提交 commit 的信息

修改最后一次提交 commit 的信息

```shell
# 修改最近提交的 commit 信息
git commit --amend --message="modify message by daodaotest" --author="jiangliheng <jiang_liheng@163.com>"

# 仅修改 message 信息
git commit --amend --message="modify message by daodaotest"

# 仅修改 author 信息
git commit --amend --author="jiangliheng <jiang_liheng@163.com>"
```

修改历史提交 commit 的信息

操作步骤：

- `git rebase -i` 列出 commit 列表
- 找到需要修改的 commit 记录，把 `pick` 修改为 `edit` 或 `e`，`:wq` 保存退出
- 修改 commit 的具体信息`git commit --amend`，保存并继续下一条`git rebase --continue`，直到全部完成
- 中间也可跳过或退出`git rebase (--skip | --abort)`

```shell
# 列出 rebase 的 commit 列表，不包含 <commit id>
git rebase -i <commit id>
# 最近 3 条
git rebase -i HEAD~3
# 本地仓库没 push 到远程仓库的 commit 信息
git rebase -i

# vi 下，找到需要修改的 commit 记录，`pick` 修改为 `edit` 或 `e`，`:wq` 保存退出
# 重复执行如下命令直到完成
git commit --amend --message="modify message by daodaotest" --author="jiangliheng <jiang_liheng@163.com>"
git rebase --continue

# 中间也可跳过或退出 rebase 模式
git rebase --skip
git rebase --abort
```

> 参考网址：[7.6 Git 工具 - 重写历史](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E9%87%8D%E5%86%99%E5%8E%86%E5%8F%B2)

### git 修改.gitignore 后重新生效

```shell
git rm -r --cached .  #清除缓存
git add . #重新trace file
git commit -m "update .gitignore" #提交和注释
git push origin master #可选，如果需要同步到remote上的话
```

会在已有的提交上新增一个提交，并且刷新 `.gitignore` 文件。

配置语法:

以斜杠“/”开头表示目录；
以星号“\*”通配多个字符；
以问号“?”通配单个字符
以方括号“[]”包含单个字符的匹配列表；
以叹号“!”表示不忽略(跟踪)匹配到的文件或目录；

### 利用 git bisec 二分法查找定位 bug 问题

如果出现 bug，很容易想到的是回滚 git 记录查找 bug 出现的提交，通常可以手动回滚记录进行定位，找到引入 bug 的提交进行修复。git 提供了一种二分查找的方式帮助开发者快速定位 bug 引入的提交。很久没用做个记录。

步骤：
开始 git 二分定位
标记包含 bug 提交
标记上一个不含 bug 的提交
运行验证
进行标记
重复 2~5 步
定位 bug git 提交
结束 git 二分查找
修复 bug

实战
步骤 1：开始二分查找
git bisec start

步骤 2：假设当前提交包含 bug，进行标记
git bisec bad

步骤 3：找到上一个不含 bug 的提交，假设在之前的提交 46aa1abd5 不含 bug，进行标记
git bisec good 46aa1abd5

步骤 4：git 会自动回滚到两次提交中间的提交，运行代码进行验证
步骤 5：进行标记，标记后代码会自动回滚或者前进到中间 git 提交

如果回滚后依旧存在 bug，进行 bad 标记：$ git bisec bad
如果回滚后 bug 没了，进行 good 标记：$ git bisec good，这里不用跟 commit hash 也行了，默认是当前提交。

步骤 6：重复前前几步，知道 git 提示找到了 bug 引入的提交记录
步骤 7：根据之前的标记，git 会找到引入 bug 的 commit 提交
提示如：
bash 复制代码 da5207dec2(这里是你的 git 记录) is the first bad commit
// 下面的提示省略。。。

关键字在 is the first bad commit，说明这个提交引入了 bug，review 代码进行修复吧。
步骤 8：结束 git 二分查找
git bisec reset

### git 对象在一个项目里面具体的运作方式

Git 文件版本管理依赖于核心四对象及相互之间指向关系：标签(tag)->提交(commit)->目录树(tree) )->块(blob).
Git 为了降低对象文件的存储、传输成本，提供了 GC 机制，将松散对象等文件收纳到包文件。

```shell
git cat-file -t <commit-id>

git cat-file commit <commit-id>

git cat-file tree <tree-id>
git ls-tree <tree-id>

git cat-file blob <blob-id>
```

### git 钩子机制

和其它版本控制系统一样，Git 能在特定的动作发生时触发执行用户自定义脚本，这便是钩子机制。
Git 可以在客户端部署和触发钩子，也能在服务器端部署和触发钩子。

- 客户端钩子
  对于非裸版本库，客户端钩子在本地工程。git/hooks 目录下，可以在提交、合并、推送等操作时候触发用户自定义脚本。

- 服务端钩子
  服务器端的钩子是项目管理人员用来给项目执行强制管理策略的，可以在接收到推送、拉取请求时候触发用户自定义脚本。
  1.Git 的钩子样例均以。sample 结尾，表示不生效，如需生效钩子，请删除该后缀
  2.Git 的钩子脚本并无类型限制 shell、python 等均可，但勿直接设置二进制执行件为钩子 3.部分 Git 钩子是支持逃逸的，在执行相应 git 命令时候增加--no-verify 选项即可跳过钩子调用 4.多数钩子分 pre 和 post，也就是指定在 git 命令操作前还是后进行调用，注意钩子是阻塞性的

Git 钩子机制分为客户端钩子与服务器端钩子：客户端钩子可用于开发人员前置的门禁检查等，服务器端钩子可用于项目管理员对项目执行自动化的远端管理操作。

commit-msg 脚本文件应该放在代码根目录的 .git/hooks 文件夹下，该文件夹下有许多的脚本文件，这些脚本文件也被称之为钩子，在被特定的事件触发后这些文件将会被调用。当一个 git 仓库被初始化生成时，一些非常有用的钩子脚本将会生成在仓库的 .git/hooks 目录中，但是在默认情况下它们是不生效的，把这些钩子文件的 ”.sample”文件后缀名去掉就可以使它们生效。

Git 提供了 4 个提交工作流钩子：pre-commit、prepare-commit-msg、commit-msg、post-commit。其中 commit-msg 钩子，会在我们执行 `git commit` 时被执行。

在 gerrit 的 Change-Id 生成机制中，gerrit 会利用 commit-msg 的钩子，在我们提交代码后，按照一定规则修改提交日志，在其末尾添加了一行 Change-Id。

### git 报错：SSL certificate

```markdown
_SSL certificate problem: unable to get local issuer certificate_
```

这个是由于 Git 默认开启了 SSL 验证，关闭即可；

或报错

```shell
fatal: unable to access 'https://github.com/xxx/': server certificate verification failed.
```

在使用镜像网站或者代理进行 git clone 时，可能出现 ssl 证书验证失败的问题。

解决方式：

```bash
git config --global http.sslVerify false
```

执行以上 git 命令，关闭 ssl 验证。

### git 报错：Received HTTP code 504

**Windows**：在连接 **Bitbucket**（AKA **stash**）之前，您需要从 Git 和控制台环境中清除所有代理：

```shell
SET HTTP_PROXY=
SET HTTPS_PROXY=
git config --global --unset http.proxy
git config --global --unset https.proxy
# git clone http://yourUser@stashAddress:stashPort/apptest.git
```

但是如果你需要连接到像 **github** 这样的公共存储库，那么就需要再次定义代理：

```shell
SET HTTP_PROXY=proxyaddress:port
SET HTTPS_PROXY=proxyaddress:port
git config --global http.proxy http://proxyaddress:port
git config --global https.proxy http://proxyaddress:port
```

我认为它可能对在公司防火墙后面工作的其他开发人员有用。

**Linux**：

```shell
unset HTTP_PROXY
unset HTTPS_PROXY
git config --global --unset http.proxy
git config --global --unset https.proxy
# git clone http://yourUser@stashAddress:stashPort/apptest.git
```

再次定义代理：

```shell
export HTTP_PROXY=proxyaddress:port
export HTTPS_PROXY=proxyaddress:port
git config --global http.proxy http://proxyaddress:port
git config --global https.proxy http://proxyaddress:port
```

_注意环境变量的大写。某些操作系统版本可能需要小写字母或默认定义了小写字母变量。_

### git 报错：port 443 : Timed out

```shell
# 设置全局代理：
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

git config --global http.proxy http://127.0.0.1:1080
git config --global https.proxy http://127.0.0.1:1080

# 取消全局代理：
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### GIT 自动补全

git 可以配置自动补全命令，补全分支名，以及高亮显示当前分支

【注】`~/.bashrc` 是 Linux 的，对应到 Mac 是 `~/.bash_profile` ，看网上的教程要注意区分和替换

1. 执行以下命令，克隆官方 git 库，然后在`git/contrib/completion`找到两个关键文件

   ```shell
   git clone https://github.com/git/git.git
   cd git/contrib/completion
   ```

   - `contrib/completion/git-completion.bash` 自动补全
   - `contrib/completion/git-prompt.sh` 高亮显示当前分支名称

2. 执行以下命令，将两个文件复制到用户目录，并设置隐藏

   ```shell
   cp git-completion.bash ~/.git-completion.bash
   cp git-prompt.sh ~/.git-prompt.sh
   ```

3. 配置 `~/.bash_profile` 文件，没有该文件就新增，然后加入以下内容(会使命令响应时间变长...)

   ```bash
   # git命令自动补全
   source ~/.git-completion.bash
   # git显示分支官方实现
   GIT_PS1_SHOWDIRTYSTATE=true
   GIT_PS1_SHOWCOLORHINTS=true
   GIT_PS1_SHOWSTASHSTATE=true
   GIT_PS1_SHOWUNTRACKEDFILES=true
   #GIT_PS1_SHOWUPSTREAM=auto
   if [ -f ~/.git-completion.bash ]; then
     source ~/.git-prompt.sh
     PROMPT_COMMAND='__git_ps1 "[\t][\u@\h:\w]" "\\\$ "'
   fi
   ```

4. 执行以下命令进行刷新

   ```shell
   source ~/.bash_profile
   ```

### git 命令结果输出到单独窗口

这与 git 的 pager 设置有关。

pager 其实就是分页器，也就是对一大段内容进行分页显示的工具，git 在一些版本中**默认使用的是 less 工具**，不同的版本默认设置会有差异，这也就是造成我在 windows 下没有自动分页，而在 linux 下会打开新窗口进行分页的原因。

git 的分页器可以通过 core.pager 来进行设置，他会被 git 命令行解释，影响分页器的变量有多个，他们起作用的顺序依次是

1. `$GIT_PAGER` 环境变量
2. `core.pager` git 配置
3. `$PAGER` 环境变量

如果这些都没有设置，默认会选择编译时的选项（通常为 less），具体细节可以参考官方文档 [git core.pager](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corepager)。

```shell
# 全局禁用分页器，直接显示在终端窗口上，不再进行分页处理
# git branch 比较方便，但 git log 等长页显示会一直滚屏，巨难用
git config --global core.pager ''

# 对某个命令禁用分页器，只想屏蔽 git branch 的分页，而想保留git show 和 git log 等的分页显示
git config --global pager.branch false # git branch 不分页
# 重新启用分页器
git config --global pager.branch true # git branch 分页
```

> [解决 git 命令会将结果输出到单独窗口必须按 q 才能退出的问题](https://blog.csdn.net/albertsh/article/details/114806994)

### 不显示修改颜色标记

搜了半天，发现这玩意叫做 Gutter Indicators。作用是在一个 git 仓库中，如果对某个文件做了修改，vsocde 编辑器会在行号旁边用不同颜色标志该文件的修改情况。

原因是在项目最外层文件夹（项目名的同级目录下）git init 了，产生了.git 文件。

解决方法：在终端进入最外层（项目名所在目录，而不是下一层）的文件夹执行 rm -rf .git 命令即可。

<https://www.jianshu.com/p/2d70f26e4229>

git 项目,VSCode 显示不同颜色块的含义：<https://www.cnblogs.com/soyxiaobi/p/9708518.html>

## Git commit 规范

### commit 规范介绍

<https://zhuanlan.zhihu.com/p/182553920>

**commit message 格式**：

```text
<type>(<scope>): <subject>
```

**type(必须)**：

用于说明 git commit 的类别，只允许使用下面的标识。

feat：新功能（feature）。

fix/to：修复 bug，可以是 QA 发现的 BUG，也可以是研发自己发现的 BUG。

- fix：产生 diff 并自动修复此问题。适合于一次提交直接修复问题
- to：只产生 diff 不自动修复此问题。适合于多次提交。最终修复问题提交时使用 fix

docs：文档（documentation）。

style：格式（不影响代码运行的变动）。

refactor：重构（即不是新增功能，也不是修改 bug 的代码变动）。

perf：优化相关，比如提升性能、体验。

test：增加测试。

chore：构建过程或辅助工具的变动。

revert：回滚到上一个版本。

merge：代码合并。

sync：同步主线或分支的 Bug。

**scope(可选)**：

scope 用于说明 commit 影响的范围，比如数据层、控制层、视图层等等，视项目不同而不同。

### Git-cz 工具

## 代码对比工具

### diff 命令

`diff` 命令是 Linux 下自带的一个强大的文本比对工具，而且使用起来非常方便。而且它在大多数的 Linux 发行版里已经预装了，它可以逐行比对两个文本文件，并输出它们的差异点。更多介绍可以直接查看它的 man 手册。

```text
man diff
```

但是，diff 命令虽然强大，但它的输出结果实在是太感人了，不直观也不清晰。于是，有大佬为了弥补这个缺点，基于 diff 开发了更强大的工具。这里推荐两个：`colordiff` 和 `wdiff` 。

**colordiff 命令**

`colordiff` 是一个 Perl 脚本工具，它的输出结果和 diff 命令一样，但是会给代码着色，并且具有语法高亮功能。同时，你如果不喜欢它的默认颜色的话，还可以自定义主题。

你可以自行安装 colordiff 到你的电脑，根据不同的发行版选择不同的安装命令。

```text
yum install colordiff             [On CentOS/RHEL/Fedora]
dnf install colordiff             [On Fedora 23+ version]
sudo apt-get install colordiff    [On Debian/Ubuntu/Mint]
```

同样，你可以使用 man 命令查看它的帮助文档：

```text
man colordiff
```

**wdiff 命令**：

diff 命令是逐行比较差异，而 `wdiff` 更变态，是逐字比较。所以如果你的文本只是修改了少数一些词语的话，使用 wdiff 命令将更加高效。

安装命令如下：

```java
yum install wdiff             [On CentOS/RHEL/Fedora]
dnf install wdiff             [On Fedora 23+ version]
sudo apt-get install wdiff    [On Debian/Ubuntu/Mint]
```

更详细内容可以查看它的 man 手册。

```text
man wdiff
```

### vimdiff 命令

`vimdiff` 等同于 `vim -d` 命令，即 Vim 编辑器的 diff 模式。

该命令后面通常会接两个或多个文件名作为参数，这些文件会同时在 Vim 编辑器的分割窗口中打开，并高亮显示文件中内容有差异的部分。

![img](https://pic2.zhimg.com/80/v2-848d80bd879ae1afbee71f01c14b4ad1_720w.webp)

它的中文主页是：[http://vimcdoc.sourceforge.net/doc/diff.html](https://link.zhihu.com/?target=http%3A//vimcdoc.sourceforge.net/doc/diff.html)

以上介绍的两款是 Linux 命令行的对比工具，我们再来看一些 GUI 比对工具。

配置方法：

```shell
git config --global merge.tool vimdiff
git config --global merge.conflictstyle diff3
git config --global mergetool.prompt false

#让git mergetool不再生成备份文件(*.orig)
git config --global mergetool.keepBackup false
```

使用方法：

```shell
git mergetool <filename>
# 文件名参数是可选的。如果不传文件名，那么将会自动挨个打开有冲突的文件
```

上一层三个小窗口分别对应：

- `LOCAL` buffer: 当前分支
- `BASE` buffer: 两个分支共同祖先，代表两个分支修改前
- `REMOTE` buffer: 需要合并到当前分支的分支

下层窗口为：

- `MERGED` buffer: 合并后的，即有冲突的

鼠标移动到 MERGED 窗口(CTRL-w 切换窗口)，

:diffget REMOTE # 获取 REMOTE 的修改到 MERGED 文件, 忽略大小写
:diffg BASE # get from base
:diffg LOCAL # get from local

注意：通过 diffget 只能选取 local, base, remote 三种的一种，要想都需要 3 种或者两种，只能通过修改 MERGED 文件

修改完成后， 保存

:wqa

vimdiff 命令参考

```shell
]c      # nect difference
[c      # previous difference
zo      # open folded text
zc      # close folded text
zr      # open all folds
zm      # close all folds
:diffupdate     # re-scan the file for difference
do      # diff obtain
dp      # diff put
:set diffopt+=iwhite    # to avoid whitespace comparison
Ctrl+W+W                # toggle between the diff columns
Ctrl+W+h/j/k/l          # 移动鼠标到不同窗口
:set wrap               # wrap line
:set nowrap
:syn off                # remove colors
```

### 3.Kompare

`Kompare` 是基于 diff 的一个 GUI 工具，使用者可以很方便看到文件之间的差异，并且支持合并这些差异。

Kompare 的特性有如下：

- 支持多种 diff 格式；
- 支持目录之间的比对；
- 支持读取 diff 文件；
- 自定义界面；
- 创建及应用源文件的 patch 文件。

![img](https://pic2.zhimg.com/80/v2-71af4459230d42591e1cf8ee46a47fe1_720w.webp)

该工具的主页为：[https://www.kde.org/applications/de](https://link.zhihu.com/?target=https%3A//www.kde.org/applications/development/kompare/)

### 5.Meld

`Meld` 是一个轻量级 GUI 代码比对工具，它支持用户比对文件、目录，并且高度集成版本控制软件。但针对软件开发人员，它的以下几个特性尤为吸引人：

- 执行双向和三向差异并合并
- 轻松地在差异和冲突之间导航
- 逐个文件地比较两个或三个目录，显示新文件，缺失文件和更改文件
- 支持许多版本控制系统，包括 Git，Mercurial，Bazaar 和 SVN 等。

![img](https://pic2.zhimg.com/80/v2-aefe344aacb4f560ac927b068a044555_720w.webp)

它的官网为：[http://meldmerge.org/](https://link.zhihu.com/?target=http%3A//meldmerge.org/)

> [推荐 9 款代码对比工具](https://zhuanlan.zhihu.com/p/336414874)

## 解决 Git 合并冲突

> [如何解决 Git 中的合并冲突？详细操作步骤指南](https://www.lsbin.com/9410.html)

### Git 冲突显示方式

> [Git 冲突显示方式](https://taoshu.in/git/git-diff3.html)

git 的默认 `conflictstyle` 是 `merge`，遇到冲突后会显示如下标记：

```shell
<<<<<<< HEAD
Alice asked her parents if she could
borrow their car. They said ok but told
=======
Alice asked her father if she could
borrow his motorbike. He said ok but told
>>>>>>> feature_branch
her she had to be back by 11pm.
```

这其中`<<<<<<< HEAD`与`=======`之间的部分表示当前所在分支（也就是 HEAD）的内容，而`=======`与`>>>>>>> feature_branch`之间的部分则是 feature_branch 分支的内容。看到这个冲突就头大，因为我们无法确定要留哪一行删哪一行。

如果我们执行`git config --global merge.conflictstyle diff3`将`conflictstyle`设成`diff3`，则结果会变成

```shell
<<<<<<< HEAD
Alice asked her parents if she could
borrow their car. They said ok but told
||||||| merged common ancestors
Alice asked her father if she could
borrow his car. He said ok but told
=======
Alice asked her father if she could
borrow his motorbike. He said ok but told
>>>>>>> feature_branch
her she had to be back by 11pm.
```

大家注意多出来的`||||||| merged common ancestors`到`=======`之间的部分。git 在合并分支的时候用的是**三路合并**(3-way merge)。三路合并的关键就是找到两个分支的最新公共提交版本。在这个例子中，公共提交版本的内容就保存到了`||||||| merged common ancestors`和`=======`之间。

很显然，master 分支将`Alice asked her father if she could`改成了`Alice asked her parents if she could`，也就是 Alice 现在要向她的父母借车；而 feature_branch 分支则将 `borrow his car...`改成了`borrow his motorbike...`，也就是不借车了，要借摩托。两者合并，最终结果应该是：

```shell
Alice asked her parents if she could
borrow their motorbike. They said ok but told
her she had to be back by 11pm.
```

### Git 合并冲突的类型

合并冲突的一般类型取决于问题出现的时间。冲突发生在：

- **合并前**，表示有本地更改不是最新的。在合并开始之前会出现冲突错误消息以避免出现问题。
- **在合并期间**，表明存在覆盖问题。出现错误消息并停止合并过程以避免覆盖更改。

如何解决 Git 中的合并冲突

在 Git 中解决合并冲突的**方法**有以下**三种**：

1.**接受本地版本**。要接受来自本地版本的文件的所有更改，请运行：

```shell
git checkout --ours <file name>
```

或者，要接受**所有**冲突文件的本地版本，请使用：

```shell
git merge --strategy-option ours
```

2.**接受远程版本**。要从远程分支更新文件的更改，请运行：

```shell
git checkout --theirs <file name>
```

接受**所有**冲突文件的远程版本：

```shell
git merge --strategy-option theirs
```

3.**单独审查更改**。最后一个选项是分别查看每个更改。此选项也是最佳选择，尤其是在处理多个文件和人员时。为了使这项工作更易于管理，请使用特殊工具来帮助查看个别冲突。

最终，选择保留哪些代码部分以及不保留哪些部分取决于开发人员对当前项目的决定。

### git 使用 ours 和 theirs

> [Git-优雅地解决冲突：使用 ours 和 theirs]<https://blog.csdn.net/qq_41603165/article/details/104922336>

对于 merge 和 rebase 来说，ours 和 theirs 对应的分支正好是相反的。

假设当前指向的分支为`branch_a`，

在使用 merge 时 `git merge branch_b`，ours 指的是当前分支，即 branch_a，theirs 指的是要被合并的分支，即 branch_b。

而在使用 rebase 时 `git rebase branch_b`，theirs 指的是当前分支，即 branch_a，ours 指向修改参考分支，即 branch_b。

git merge 会抽取两个分支上新增的提交，并将其合并在一起，产生一个新的提交 D，生成的 D 节点有两个父节点。其中在合并的过程中可能会发生冲突。

git rebase 会以 branch_a 为参照，提取 branch_b 分支上的提交，将这些修改作用在 branch_a 分支上，最终结果不会产生新的提交节点。其中在将提取的修改作用在 branch_a 的过程中可能会发生冲突。

通常而言，在开发过程中很少应用 git merge 合并代码，更常用的是 git rebase。此外在开发过程中，经常使用 git rebase 命令获取 master 主分支的最新提交代码，在完成个人的开发任务之后，也需要 rebase master 分支上的代码才能申请 Pull Request，自动合并。

### git mergetool 介绍

**一、列出可用工具**

在终端中运行如下命令：

```shell
git mergetool --tool-help
```

输出打印出当前设置的所有支持的差异工具：

```shell
'git mergetool --tool=<tool>' may be set to one of the following:
                nvimdiff
                nvimdiff1
                nvimdiff2
                nvimdiff3
                vimdiff
                vimdiff1
                vimdiff2
                vimdiff3

The following tools are valid, but not currently available:
                araxis
                bc
                bc3
                bc4
                meld
                tortoisemerge
                winmerge
```

根据选择的编辑器，可以使用不同的工具。例如：

- Emacs 系: `Ediff`, `emerge`
- Vim 系: `vimdiff1`, `vimdiff2`, `vimdiff3`, `vimdiff`(= vimdiff3)
- Nvim 系: `nvimdiff1`, `nvimdiff2`, `nvimdiff3`, `nvimdiff`(= nvimdiff3)
- Vim 系: `vimdiff`
- GUI 系（跨平台）: `meld`
- 商业 GUI 天花板: `Araxis Merge`

**二、`*diff1 / *diff2 / *diff3` 差异**

这是 Git 的 **diff 参与窗口数量**：

| 工具     | 窗口数 | 含义                 |
| -------- | ------ | -------------------- |
| `*diff1` | 1      | 几乎没人用           |
| `*diff2` | 2      | ours vs theirs       |
| `*diff3` | 3      | base / ours / theirs |

强烈建议：**3-way diff**。原因很现实：

- 能看到 **base（共同祖先）**
- 判断“谁改了什么”更清晰
- cherry-pick / rebase 冲突更容易判断

**三、不同平台选择建议**

1. 纯终端 / 服务器 / SSH 场景: `nvimdiff / vimdiff`
   - 不依赖 X / GUI
   - 可脚本化
   - 键盘效率极高
   - 能和 git / lazygit / fugitive 深度集成
2. 桌面开发（Linux / macOS）: `meld`
   - 3-way
   - 颜色直观
   - 新人友好
   - 开源、跨平台
3. 商业 / 大型代码库 / 法务级别对比: Araxis Merge（付费）
   - 超强 3-way 算法
   - 大文件 / 二进制友好
   - GitHub、Perforce 官方推荐过

[Git 合并冲突的解决方法](https://www.lsbin.com/tag/git合并冲突的解决方法/)：进一步的步骤显示了如何为 Vim 设置**vimdiff**工具的示例。
[Git 中的合并冲突如何解决](https://www.lsbin.com/tag/git中的合并冲突如何解决/)？为 设置默认差异工具**`git mergetool`**：

**四、你这种环境下的「最优配置」**

1. 设置默认 mergetool

   ```bash
   # 设置默认合并工具
   git config --global merge.tool nvimdiff
   # 启动合并解析工具前不提示
   git config --global mergetool.prompt false
   ```

2. 冲突时直接一条命令

   ```bash
   git mergetool
   ```

   自动打开 **3 个窗口**：

   ```bash
   [ BASE ] [ OURS ] [ THEIRS ]
               ↓
            [ RESULT ]
   ```

**五、和 lazygit 的关系（很多人会搞混）**

> **lazygit ≠ mergetool**

推荐组合是：

- **lazygit**：
  - 选文件
  - 一键 ours / theirs
  - 触发 continue / abort
- **nvimdiff**：
  - 复杂冲突
  - 精确合并

实战中是 **lazygit 进，nvimdiff 出**

### git mergetool 解决合并冲突

Git 中解决合并冲突，请运行 `mergetool` 查看差异：

```shell
git mergetool
# 或
git mergetool <filename>
# 文件名参数是可选的。如果不传文件名，那么将会自动挨个打开有冲突的文件
```

![如何解决Git中的合并冲突？详细操作步骤指南](https://www.lsbin.com/wp-content/uploads/2021/11/git-mergetool-vimdiff.png)

输出显示一个具有四个视图的窗口：

`LOCAL` - 这个文件来自**当前分支**；

`BASE` - 两个分支的**共同祖先**，在两个分支上的文件改变之前的样子；

`REMOTE` - 要合并到你当前分支的**外部分支**上的文件；

`MERGED` - **合并结果**，将会保存到本地存储库的内容。

假设我们希望**`保留来自REMOTE`**。为此，为此，移动到 `MERGED` 文件上（Ctrl + w, j），**移动光标到一个合并冲突的区域**，然后：

```shell
:diffg RE
```

其他命令如下：

```shell
:diffg RE  # get from REMOTE
:diffg BA  # get ]c]c[cjkjfrom BASE
:diffg LO  # get from LOCAL
# or
:diffget REMOTE  # get from REMOTE
:diffget BASE  # get from BASE
:diffget LOCAL  # get from LOCAL
```

一旦信息被更新，保存并退出用**`:wqa`**。

#### 解决冲突操作（核心）

- `:diffget LOCAL`: 选择 LCOAL 作为本行最终结果

- `:diffget REMOTE`: 选择 REMOTE 作为本行最终结果

- `:diffget BASE`: 选择 BASE 作为本行最终结果

- `:diffput [num]`: 放置结果到缓冲区上, `num` 为缓冲区编号

- `:diffg LO`: 这里 vim 为我们做了简略命令, 同样可用于 `REMTOE` 与 `BASE` 上 === **重要**

- `:diffget //2`: `//2` 将被替换为左侧文件名

- `:diffget //3`: `//3` 将被替换为右侧文件名

- `:%diffget LO`: 将所有变更使用 local 的结果

- `:'<'>diffget LO`: 将当前选中范围的使用 local 的结果

- `dp/do`: 如果只有两个文件则可以使用 `dp/do` 来替代 `:diffput/:diffget`

- `:diffoff`: 关闭 diff mode

- `:diffthis`: 开启 diff mode

- `:ls!`: 显示当前所有缓冲区的号码 kkkjk

- `[c`: conflict, 移动到上一个冲突处

- `]c`: conflict, 移动到下一个冲突处

- `:diffsplit filename`: 已经在 vim 中时, 使用此命令与别的文件进行对比

- `:vert diffsplit filename`: 同上

- `vimidff file1 file2`: 对比 `file1` 与 `file2` 的差别

- `vim -d file1 file2`: 同上 🐷

- `:wqa`: 冲突修复完成保存退出, 如果仍然有文件冲突则进入下一个冲突

- `:cq`: 放弃修复, 终止流程(在 merge conflict 时很有用, 否则使用了 `qa` 的话，

  想再次进入 mergetool 就必须使用 `git checkout --conflict=diff3 {file}` 了)

> [使用 MacVim/GVim 作为 git 冲突解决工具 (mergetool)](https://hanleylee.com/articles/use-macvim_as_git_merge_tool/)
>
> 更多 vim 操作可参考 [神级编辑器 Vim 使用-操作篇](https://www.hanleylee.com/usage-of-vim-editor.html)

完成冲突合并

当我们使用 MacVim 完成了冲突文件的修复之后(或者因为其他原因不修复了), 那么以下命令你总会有用到的:

- `git merge --continue`: 冲突全部解决完后继续之前的 `merge` 操作
- `git merge --abort`: 放弃之前的 `merge` 操作
- `git checkout --conflict=diff3 test.txt`: 将文件重置回冲突状态, 适用于 merge 时发生冲突后没有完全解决时被一些其他工具将文件标记为了解决

### 提交和清理

Git 合并冲突的解决方法：最后一步是提交和清理额外的文件。通过运行提交更新的版本：

```shell
git commit -m "<your message>"
```

diff 工具会在项目上创建额外的文件来比较版本。用以下方法清理它们：

```shell
git clean -f
```

![如何解决Git中的合并冲突？详细操作步骤指南](https://www.lsbin.com/wp-content/uploads/2021/11/git-clean-output.png)

vimdiff 命令

vimdiff 命令

如果希望把一个差异点中当前文件的内容复制到另一个文件里，可以使用命令

```shell
dp （":diffget"）
```

如果希望把另一个文件的内容复制到当前行中，可以使用命令

```shell
do (":diffput"，"o" 表示 "obtain" (不能用"dg"，因为那可能是 "dgg" 的开始！))
```

在比较和合并告一段落之后，可以用下列命令对两个文件同时进行操作。比如同时退出：

```shell
:qa （quit all）
```

如果希望保存全部文件：

```shell
:wa （write all）
```

或者是两者的合并命令，保存全部文件，然后退出：

```shell
:wqa （write, then quit all）
```

如果在退出的时候不希望保存任何操作的结果：

```shell
:qa! （force to quit all）
```

如何防止 git vimdiff 以只读方式打开文件？

```shell
[difftool "vimdiff"]
    cmd = vimdiff "$LOCAL" "$REMOTE"
```

配置 Git 以使用 Vimdiff

默认情况下，vimdiff 将以只读模式打开文件，以便您无法进行任何更改。您可以通过运行以下命令在编辑器内启用编辑：

```shell
:set noro
```

要使其成为默认值，请编辑您的$HOME/.vimrc 配置，添加以下内容（您可能需要创建它）：
