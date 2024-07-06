# gerrit

> [Gerrit，这是啥玩意？和git, 或则说github这类代码仓有什么区别？](https://bbs.huaweicloud.com/blogs/408361)

## Gerrit是什么

Gerrit是一个**免费的基于网页的**，让软件开发者在团队中可以使用**网页浏览器互相审查各自源代码**的工具，它支持对代码的修改，并支持开发者接受或拒绝这些修改。可以这么说，几乎任何需要团队协作，需要正式发布的项目都应该使用Gerrit来支持代码审查功能。

Gerrit的工作流程大概是这样的：

1. 开发者在本地修改代码后，提交到**Gerrit上一个特殊分支里**，比如dev/ref，这样就创建了一个**待审查的变更**（change）
2. Gerrit则会给每个变更分配一个**唯一的Change-Id**，用来跟踪、管理变更的版本和状态
3. 开发者可以在Gerrit网页界面上查看变更的内容，同时支持添加评论，指定审查人，以及给变更打分（vote）
4. 而指定的审查人则可以在Gerrit网页界面上审查变更的内容，给变更打分（vote），或则直接拒绝变更（abandon）
5. 如果该变更被拒绝/需要重新修改，开发者可以在本地修改后，再次提交到Gerrit这个分支上，这样就更新了变更的版本，但不会改变Change-Id
6. 直至变更得到了足够的分数，**满足了通过条件**（这个条件可以在Gerrit的配置里修改），就可以**被合并到代码仓的目标分支**了，比如master

我们其实也可以感受到了，Gerrit因为是一个**基于git的代码审查系统**，它可以与github这类代码仓协同，或则也可以直接使用，因为它里面也会存有代码（提供代码托管功能）。所以Gerrit确实也支持作为代码源。

## Gerrit和Git, github等代码仓的区别是什么？

Git是一种开源的分布式版本控制系统，可以高效管理不同大小的项目。而且正因为它是分布式的，没有中央服务器，那每个使用它的电脑可以说连都存了一个完整的版本库，支持不联网也可以操作，后续等联网之后，把修改推送给团队就可以了。

Github，GitLab这类代码仓则是基于git的代码托管平台，它们支持开发者在云端创建、管理、分享和协作代码项目；而它们本身则使用git作为版本控制系统。同时，它们**也额外支持代码审查功能**。

Gerrit 则是**专业的代码审查系统**，它可以在 Git / GitHub / GitLab 的基础上增加更强大和灵活的代码审查功能。比如使用 Change-Id 来跟踪和管理变更的版本和状态，使用特殊的分支模型来上传和合并变更，使用强大的权限控制机制来设置谁可以提交、审查、合并代码，以及使用**丰富的插件系统**来扩展和定制 Gerrit 的功能和界面。



### 下载或者检出变更

<https://fabric-docs-cn-topjohn.readthedocs.io/zh-cn/latest/Gerrit/best-practices.html>

```shell
git fetch REMOTE refs/changes/NN/CHANGEIDNN/VERSION \ && git checkout FETCH_HEAD
# 对于第四版更改 2464，NN是前两位数（24）：
git fetch REMOTE refs/changes/24/2464/4 \ && git checkout FETCH_HEAD
```



当 Gerrit 通过其服务器接收对象数据时，**它会将每项提交转变成一项变更**，以便审核者可以单独针对每项提交给出意见。要将几项“检查点”提交合并为一项提交，请使用 git rebase -i，然后再运行 repo upload。<font color=red>【意味着如果不合并 commit-id，就会生成多个 change-id，审核者需要逐个检视。如果只想生成一个 change-id 给别人检视，则需要合并多个 commit-id 为一个。】</font>



## change-id 与 patch-id 与 commit-id

在版本控制系统（如 Git）和代码评审工具（如 Gerrit）中，`change-id`、`patch-id` 和 `commit-id` 是重要的标识符，用于管理和追踪代码更改。以下是对它们的详细解释和用途：

1. **Commit ID**

   - **定义**：Commit ID 是一个唯一的 SHA-1 哈希值，由 Git 自动生成，用于唯一标识一个提交。

   - **用途**：每个提交在 Git 仓库中都有一个唯一的 Commit ID，可以用来检索、引用和操作特定的提交。

   - **生成**：由 Git 自动生成，基于提交内容、时间戳、作者等信息。

   示例

   ```txt
   commit 1a2b3c4d5e6f7g8h9i0j
   Author: Your Name <your.email@example.com>
   Date:   Mon Jul 6 15:00:00 2024 +0000
   
       Your commit message
   ```

2. **Change-ID**

   - **定义**：Change-ID 是 Gerrit 中的一个概念，用于标识一系列关联的更改（可能包含多个 patch sets）。

   - **用途**：在 Gerrit 中，一个 Change-ID 允许将多个版本（patch sets）的更改关联到同一个代码评审。这样，在评审过程中进行的更改和修改都可以追踪到同一个 Change-ID。

   - **生成**：通常在提交信息中手动添加，格式为 `Change-Id: I<40位哈希值>`。一些开发工具或插件也可以自动生成。

   示例

   ```txt
   commit 1a2b3c4d5e6f7g8h9i0j
   Author: Your Name <your.email@example.com>
   Date:   Mon Jul 6 15:00:00 2024 +0000
   
       Your commit message
   
       Change-Id: I1234567890abcdef1234567890abcdef12345678
   ```

3. **Patch-ID**

   - **定义**：Patch-ID 是一个基于补丁内容的唯一标识符，用于标识代码变更的特定版本。

   - **用途**：Patch-ID 可用于识别相同内容的补丁，即使它们的元数据（如作者、日期）不同。Git 可以通过 `git patch-id` 命令生成 Patch-ID。

   - **生成**：通过 `git patch-id` 命令生成，基于补丁的内容。

   示例

   ```shell
   git diff | git patch-id
   ```

4. **区别与关系**

   - **Commit ID**：唯一标识一个具体的提交。在整个 Git 仓库中是唯一的。

   - **Change-ID**：用于 Gerrit 中标识一组关联的更改（可能包含多个版本）。有助于在代码评审过程中关联和追踪更改。

   - **Patch-ID**：基于补丁内容生成的标识符，用于识别相同内容的补丁。即使提交的元数据不同，相同内容的补丁也会有相同的 Patch-ID。

5. **应用场景**

   - **Commit ID**：用于引用、检索特定的提交，回滚到某个提交，查看提交历史等。

   - **Change-ID**：用于 Gerrit 代码评审系统，管理和追踪多个版本的代码变更。

   - **Patch-ID**：用于比较两个补丁是否相同，即使它们的元数据（如作者、日期）不同。

6. 代码示例

   添加 Change-ID

   通常在提交时添加 Change-ID，可以使用以下方式：

   ```shell
   git commit -m "Your commit message
   
   Change-Id: I1234567890abcdef1234567890abcdef12345678"
   ```

   获取 Patch-ID

   可以通过以下命令获取补丁的 Patch-ID：

   ```shell
   git diff | git patch-id
   ```

总结

- **Commit ID** 是 Git 提交的唯一标识符。
- **Change-ID** 是 Gerrit 中标识一组关联更改的标识符，用于代码评审。
- **Patch-ID** 是基于补丁内容生成的标识符，用于识别相同内容的补丁。

这些标识符在版本控制和代码评审过程中扮演着重要角色，有助于更好地管理和追踪代码变更。

