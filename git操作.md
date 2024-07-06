
# repo

> 
>
> [Repo README](https://source.android.com/docs/setup/create/repo?hl=zh-cn)
>
> [Repo 命令参考资料](https://source.android.com/docs/setup/create/repo?hl=zh-cn)
>
> [Repo 工具使用介绍](https://help.gitee.com/enterprise/code-manage/%E9%9B%86%E6%88%90%E4%B8%8E%E7%94%9F%E6%80%81/Repo%20%E5%B7%A5%E5%85%B7%E4%BD%BF%E7%94%A8%E4%BB%8B%E7%BB%8D)
>
> 
>
> [repo入门和基本用法](https://blog.csdn.net/Jason_Lee155/article/details/123427571)
>
> [Windows安装repo的真正解决方案](https://juejin.cn/post/6844904057421742094)
>
> [Git-Repo 文档](https://git-repo.info/zh_cn/docs/)

Repo 是基于 Git 构建的工具。Repo 可帮助管理许多 Git 存储库、将代码上传到修订控制系统以及自动化部分开发工作流程。Repo 并非旨在取代 Git，而只是让使用 Git 变得更加容易。repo 命令是一个可执行 Python 脚本，您可以将其放在路径中的任何位置。



## Repo的安装：

1.Repo 是一个由 Google 开发的多仓库管理工具，通常用于管理 Android 项目。以下是Repo的安装步骤：

* 确保您已经安装了Git，因为Repo是建立在Git之上的工具。

* 打开命令行终端，并在系统可执行路径中创建一个名为 ‘repo’的可执行文件。例如，在Linux或[macOS](https://so.csdn.net/so/search?q=macOS&spm=1001.2101.3001.7020)上，可以使用以下命令：

  ```shell
  curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
  chmod a+x ~/bin/repo
  ```

  在Windows上，可以从 Git 官方仓库（https://gerrit.googlesource.com/git-repo/）下载 repo 工具，并将其放置在 Git 的bin 目录下。

* 确保您的 'PATH’环境变量中包含了包含 ‘repo’ 可执行文件的目录，这样就可以在任何位置使用 ‘repo’ 命令。

* 在您的项目根目录中创建一个名为 'manifest.xml’的清单文件，其中定义了您的多仓库结构和依赖关系。

* 使用以下命令初始化仓库并同步代码：

  ```shell
  repo init -u <清单文件URL> #这里一些外网资源可能会报错
  repo sync
  ```

* Repo 将根据清单文件中的配置将各个仓库的代码下载到本地。

请注意，上述安装步骤仅提供了基本指导，具体步骤可能因操作系统、软件版本和个人需求而有所不同。在安装过程中，建议参考各个工具的官方文档和安装指南，以确保正确的安装和配置。



## Repo的使用

> [Repo 命令参考资料](https://source.android.com/source/using-repo?hl=zh-cn)

使用 Repo 需遵循的格式如下：

```shell
repo <COMMAND> <OPTIONS>
```

可选元素显示在方括号 [ ] 中。例如，许多命令会将项目列表用作参数。您可以为项目指定项目列表，作为名称列表或本地源代码目录的路径列表：

```shell
repo sync [<PROJECT0> <PROJECT1> <PROJECTN>]
repo sync [</PATH/TO/PROJECT0> ... </PATH/TO/PROJECTN>]
```



### help

安装 Repo 后，您可以通过运行以下命令找到最新文档（开头是包含所有命令的摘要）：

```shell
repo help
```

您可以通过在 Repo 树中运行以下命令来获取有关某个命令的信息：

```shell
repo help <COMMAND>
```

例如，以下命令会生成 Repo `init` 参数的说明和选项列表，该参数会在当前目录中初始化 Repo。（要了解详情，请参阅 [init](https://source.android.com/source/using-repo?hl=zh-cn#init)。）

```shell
repo help init
```



### init - 初始化仓库

```shell
$ repo init -u <URL> [<OPTIONS>]
```

在当前目录中安装 Repo。这会创建一个 `.repo/` 目录，其中包含用于 Repo 源代码和标准 Android 清单文件的 Git 代码库。该 `.repo/` 目录中还包含 `manifest.xml`，这是一个指向 `.repo/manifests/` 目录中所选清单的符号链接。

选项：

- `-u`：指定要从中检索清单代码库的网址。您可以在 `https://android.googlesource.com/platform/manifest` 中找到常见清单
- `-m`：在代码库中选择清单文件。如果未选择任何清单名称，则会默认选择 default.xml。
- `-b`：指定修订版本，即特定的清单分支。

> :star:**注意**：对于其余的所有 Repo 命令，当前工作目录必须是 `.repo/` 的父目录或相应父目录的子目录。



### sync - 同步代码

```shell
repo sync [<PROJECT_LIST>]
```

下载新的更改并更新本地环境中的工作文件。如果您在未使用任何参数的情况下运行 `repo sync`，则该操作会同步所有项目的文件。

运行 `repo sync` 后，将出现以下情况：

- 如果目标项目从未同步过，则 `repo sync` 相当于 `git clone`。远程代码库中的所有分支都会复制到本地项目目录中。

- 如果目标项目已同步过，则 `repo sync` 相当于以下命令：

  ```shell
  git remote update
  git rebase origin/<BRANCH>
  ```

  其中 **`<BRANCH>`** 是本地项目目录中当前已检出的分支。如果本地分支没有在跟踪远程代码库中的分支，则相应项目不会发生任何同步。

- 如果 git rebase 操作导致合并冲突，那么您需要使用普通 Git 命令（例如 `git rebase --continue`）来解决冲突。

`repo sync` 运行成功后，指定项目中的代码会与远程代码库中的代码保持同步。

选项：

- `-c`：只同步当前分支。
- `-j <jobs>`：指定并行下载的线程数。
- `-f`：即使某些项目同步失败，也继续进行其他项目的同步。
- `-q`：安静模式，减少输出的信息量。
- `-n`：不要获取当前提交，而是只更新元数据。
- `--no-tags`：不要获取标签。
- `--force-broken`：即使有项目同步失败也继续。
- `--optimized-fetch`：优化的 fetch 操作以减少数据传输量。
- `--no-clone-bundle`：不使用预生成的克隆包，直接从服务器克隆。
- `--prune`：移除已删除的远程分支。
- `-d`：将指定项目切换回清单修订版本。如果项目当前属于某个主题分支，但只是临时需要清单修订版本，则此选项会有所帮助。
- `-s`：同步到当前清单中清单服务器元素指定的一个已知的良好版本。

示例

```shell
repo sync -c project1name project2name
```

仅同步 `project1` 和 `project2`的当前分支。



### upload - 推送更改

```shell
repo upload [<PROJECT_LIST>]
```

对于指定的项目，Repo 会将本地分支与最后一次 repo sync 时更新的远程分支进行比较。Repo 会提示您选择一个或多个尚未上传以供审核的分支。

您选择一个或多个分支后，所选分支上的所有提交都会通过 HTTPS 连接传输到 Gerrit。您需要配置一个 HTTPS 密码以启用上传授权。要生成新的用户名/密码对以用于 HTTPS 传输，请访问[密码生成器](https://android-review.googlesource.com/new-password)。

当 Gerrit 通过其服务器接收对象数据时，**它会将每项提交转变成一项变更**，以便审核者可以单独针对每项提交给出意见。要将几项“检查点”提交合并为一项提交，请使用 git rebase -i，然后再运行 repo upload。<font color=red>【意味着如果不合并 commit-id，就会生成多个 change-id，审核者需要逐个检视。如果只想生成一个 change-id 给别人检视，则需要合并多个 commit-id 为一个。】</font>

如果您在**未使用任何参数**的情况下运行 repo upload，则该操作会**搜索所有项目中的更改以进行上传**。

要在**更改上传之后对其进行修改**，您应该使用 `git rebase -i` 或 `git commit --amend` 等工具更新您的本地提交。修改完成之后，请执行以下操作：

- 进行核对以确保更新后的分支是当前已检出的分支。

- 对于相应系列中的每项提交，请在方括号内输入 Gerrit 更改 ID：

  ```shell
  # Replacing from branch foo
  [ 3021 ] 35f2596c Refactor part of GetUploadableBranches to lookup one specific...
  [ 2829 ] ec18b4ba Update proto client to support patch set replacments
  # Insert change numbers in the brackets to add a new patch set.
  # To create a new change record, leave the brackets empty.
  ```

上传完成后，这些更改将拥有一个**额外的补丁程序集**。

选项：

- `-c`：仅上传当前分支的修改，忽略其他分支的修改。
- `-m`：指定提交消息，用来描述上传的修改内容。
- `-n`：模拟上传，显示将要上传的修改但不实际执行上传操作。
- `-f`：强制上传，即使当前分支没有新的提交。有时候你可能想要强制上传以确保所有本地提交都被提交到远程审查系统。
- `-e`：在上传之前编辑提交消息。

示例

```shell
# 上传当前分支的修改，并指定提交消息和主题
repo upload -c -m "Fix issue #123" -t my-topic

# 强制上传当前分支的所有修改：
repo upload -c -f

# 模拟上传当前分支的修改，显示将要上传的内容但不实际上传：
repo upload -c -n
```

> :star:**注意**：`repo upload .` 命令意味着你想要上传**当前目录下所有项目**的本地修改到远程代码审查系统，例如使用 Gerrit。然而，`repo` 工具本身并不支持直接在当前目录下执行一次性上传所有项目的修改，需要自行实现脚本。如果可以用这个命令，说明自己做了适配。



### branch - 列出分支

`repo branch` 命令用于列出 `repo` 管理的所有项目中当前活跃的分支。它显示每个项目所在的分支信息，帮助开发者了解各个项目的当前状态。

```shell
repo branches [<project>...]
```

示例

执行 `repo branch` 后，输出类似如下信息：

```txt
platform/build:                   my-feature-branch
platform/frameworks/base:         my-feature-branch
platform/packages/apps/Settings:  my-feature-branch
```

解释：

- `platform/build`：项目的名称。
- `my-feature-branch`：当前项目所在的分支名称。



### start - 创建分支

```shell
repo start <BRANCH_NAME> [<PROJECT_LIST>]
```

从清单中指定的修订版本开始，创建一个新的分支进行开发。

`*<BRANCH_NAME>*` 参数应简要说明您尝试对项目进行的更改。如果您不知道，则不妨考虑使用默认名称。

`*<PROJECT_LIST>*` 指定了将参与此主题分支的项目。

> :star:**注意**：“.”是一个非常实用的简写形式，用来代表当前工作目录中的项目。



### checkout - 切换分支

`repo checkout` 命令用于切换到特定分支或标签，可以在所有项目中执行 Git 的 `checkout` 操作。这对于管理和切换多仓库项目中的分支非常有用。

```shell
repo checkout <branchname> [<project>...]
```

示例
```shell
repo checkout my-feature-branch
```

这会在所有项目中切换到 `my-feature-branch` 分支。如果某个项目中没有该分支，则会显示错误信息。



### status

```shell
repo status [<PROJECT_LIST>]
```

对于每个指定的项目，将工作树与临时区域（索引）以及此分支 (HEAD) 上的最近一次提交进行比较。在这三种状态存在差异之处显示每个文件的摘要行。

要仅查看当前分支的状态，请运行 `repo status`。系统会按项目列出状态信息。对于项目中的每个文件，系统使用两个字母的代码来表示：

在第一列中，大写字母表示临时区域与上次提交状态之间的不同之处。

| 字母 | 含义       | 说明                                         |
| :--- | :--------- | :------------------------------------------- |
| -    | 无更改     | HEAD 与索引中相同                            |
| A    | 已添加     | 不存在于 HEAD 中，但存在于索引中             |
| M    | 已修改     | 存在于 HEAD 中，但索引中的文件已修改         |
| D    | 已删除     | 存在于 HEAD 中，但不存在于索引中             |
| R    | 已重命名   | 不存在于 HEAD 中，但索引中的文件的路径已更改 |
| C    | 已复制     | 不存在于 HEAD 中，已从索引中的另一个文件复制 |
| T    | 模式已更改 | HEAD 与索引中的内容相同，但模式已更改        |
| U    | 未合并     | HEAD 与索引之间存在冲突；需要解决方案        |

在第二列中，小写字母表示工作目录与索引之间的不同之处。

| 字母 | 含义    | 说明                                       |
| :--- | :------ | :----------------------------------------- |
| -    | 新/未知 | 不存在于索引中，但存在于工作树中           |
| m    | 已修改  | 存在于索引中，也存在于工作树中（但已修改） |
| d    | 已删除  | 存在于索引中，不存在于工作树中             |



### diff

```shell
repo diff [<PROJECT_LIST>]
```

使用 `git diff` 显示提交与工作树之间的明显更改。



### download

```shell
repo download <TARGET> <CHANGE>
```

从审核系统中下载指定更改，并放在您项目的本地工作目录中供使用。

例如，要将[更改 23823](https://android-review.googlesource.com/23823) 下载到您的平台/编译目录，请运行以下命令：

```shell
$ repo download platform/build 23823
```

`repo sync` 应该可以有效移除通过 `repo download` 检索到的任何提交。或者，您可以将远程分支检出，例如 `git checkout m/master`。

> :star:**注意**：由于全球的所有服务器均存在复制延迟，因此某项更改（位于 [Gerrit](https://android-review.googlesource.com/) 中）出现在网络上的时间与所有用户可通过 `repo download` 找到此项更改的时间之间存在些许的镜像延迟。



### forall - 自定义命令

```shell
repo forall [<PROJECT_LIST>] -c <COMMAND>
```

在每个项目中运行指定的 shell 命令。通过 `repo forall` 可使用下列额外的环境变量：

- `REPO_PROJECT` 可设为项目的具有唯一性的名称。
- `REPO_PATH` 是客户端根目录的相对路径。
- `REPO_REMOTE` 是清单中远程系统的名称。
- `REPO_LREV` 是清单中修订版本的名称，已转换为本地跟踪分支。如果您需要将清单修订版本传递到某个本地运行的 Git 命令，则可使用此变量。
- `REPO_RREV` 是清单中修订版本的名称，与清单中显示的名称完全一致。

选项：

- `-c`：要运行的命令和参数。此命令会通过 `/bin/sh` 进行求值，它之后的任何参数都将作为 shell 位置参数传递。
- `-p`：在指定命令输出结果之前显示项目标头。这通过以下方式实现：将管道绑定到命令的 stdin、stdout 和 sterr 流，然后通过管道将所有输出结果传输到一个页面调度会话中显示的连续流中。
- `-v`：显示该命令向 stderr 写入的消息。

### prune

```shell
repo prune [<PROJECT_LIST>]
```

删减（删除）已合并的主题。



## manifest.xml

`repo` 是一个用于管理多个 Git 仓库的工具，广泛用于 Android 开源项目等大型项目中。`manifest.xml` 是 `repo` 工具用来定义和管理多个 Git 仓库的配置文件。下面是对 `manifest.xml` 文件的详细解析：

### 一、`manifest.xml` 的基本结构

一个典型的 `manifest.xml` 文件包含以下元素：

```xml
<manifest>
    <remote name="origin" fetch="..." />
    <default revision="..." remote="origin" sync-j="4" />
    <project name="project1" path="path/to/project1" revision="branch1" />
    <project name="project2" path="path/to/project2" groups="group1,group2" />
    <project name="project3" path="path/to/project3" upstream="branch3" />
    <include name="another_manifest.xml" />
</manifest>
```

### 二、主要元素和属性

1. **`<manifest>`**

   最顶层的XML元素，包含整个manifest文件的配置信息。

   - 无直接属性定义，但作为容器，包含了其它所有元素。

2. **`<remote>`**

   定义一个远程仓库。一个 `manifest.xml` 可以定义多个 `<remote>`。

   ```xml
   <remote name="origin" fetch="https://example.com/git/" review="https://review.example.com/" />
   ```

   - `name`: 远程仓库的别名。
   - `fetch`: 从远程仓库拉取数据时使用的URL。
   - 可选属性如`review`用于指定代码审查系统的URL等。

3. **`<default>`**

   定义默认配置，用于简化 `<project>` 元素的定义。

   ```xml
   <default revision="master" remote="origin" sync-j="4" />
   ```

   - `remote`: 默认的remote名称。
   - `revision`: 默认的版本或分支名。
   - `sync-j`: 同步时使用的最大并发数。

4. **`<project>`**

   定义单个Git项目的信息。

   ```xml
   <project name="platform/build" path="build" revision="android-11.0.0_r1" groups="group1,group2" upstream="master" clone-depth="1" />
   ```

   - `name`: 仓库名称或路径。
   - `path`: 仓库克隆到本地的工作目录路径。
   - `remote`: 使用的remote别名，如果未指定则使用`default`中定义的remote。
   - `revision`: 版本或分支名，未指定时使用`default`中的revision。
   - `clone-depth`: 克隆深度，用于浅克隆。
   - `groups`: 项目所属的组别，便于管理。项目所属的组，可以用于选择性同步项目。
   - `upstream`：上游分支，用于提交变更的基础分支。

5. `<include>`

   引用另一个 `manifest.xml` 文件，便于组织和分隔配置，实现manifest的模块化。

   ```xml
   <include name="another_manifest.xml" />
   ```

   - `name`: 要包含的 `manifest.xml` 文件的路径。

6. `<exclude-project>`

   在包含其他manifest时，排除特定项目。

   - `name`: 要排除的项目名称。

7. `<repo-hooks>`

   定义repo钩子脚本，用于自动化某些操作。

   ```xml
   <repo-hooks in-project="hooks/repo" enabled-list="pre-upload" />
   ```

   - `in-project`：包含钩子脚本的项目名称。
   - `enabled-list`：启用的钩子列表，多个钩子用逗号分隔。

8. `<notice>` (或其他自定义标签)

   可能包含版权信息或项目说明等自定义内容。

   - **属性**: 依据具体内容而定，通常为描述性文本。

以上是`manifest.xml`中一些基本且常用的元素和属性。根据项目需求，可能还会有更多的定制化元素和属性。开发者应根据具体项目文档或`repo`工具的官方指南来理解和配置这些元素。

### 三、示例解析

下面是一个完整的 `manifest.xml` 示例及其解析：

```xml
<manifest>
    <remote name="aosp" fetch="https://android.googlesource.com/" />
    <remote name="github" fetch="https://github.com/" />

    <default revision="main" remote="aosp" sync-j="8" />

    <project name="platform/build" path="build" />
    <project name="platform/frameworks/base" path="frameworks/base" revision="android-11.0.0_r1" />
    <project name="platform/packages/apps/Settings" path="packages/apps/Settings" groups="optional" />

    <extend-project name="platform/build">
        <annotation name="custom-annotation" value="custom-value" />
    </extend-project>

    <include name="custom_manifest.xml" />

    <repo-hooks in-project="platform/tools/hooks" enabled-list="pre-upload" />
</manifest>
```

1. **`<remote>` 元素**
   - 定义了两个远程仓库 `aosp` 和 `github`，分别指向不同的 URL 前缀。
2. **`<default>` 元素**
   - 指定默认使用 `aosp` 远程仓库，默认分支为 `main`，同步时使用 8 个并行线程。
3. **`<project>` 元素**
   - 第一个项目 `platform/build`，存储在本地 `build` 目录，使用默认分支 `main`。
   - 第二个项目 `platform/frameworks/base`，存储在本地 `frameworks/base` 目录，使用 `android-11.0.0_r1` 分支。
   - 第三个项目 `platform/packages/apps/Settings`，存储在本地 `packages/apps/Settings` 目录，属于 `optional` 组。
4. **`<extend-project>` 元素**
   - 为 `platform/build` 项目添加一个自定义注释。
5. **`<include>` 元素**
   - 包含一个额外的 `custom_manifest.xml` 文件，用于定义更多的项目和配置。
6. **`<repo-hooks>` 元素**
   - 指定了一个包含钩子脚本的项目，并启用了 `pre-upload` 钩子。

通过对 `manifest.xml` 文件中各个元素和属性的详细解析，可以更好地理解和管理使用 `repo` 工具的多仓库项目。这些配置使得项目的管理更加灵活和高效。

