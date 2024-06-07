[toc]

# git

> git 官方使用说明：
>
> https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%85%B3%E4%BA%8E%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6
>
> 推荐博文
> [玩转Git三剑客笔记](https://www.cnblogs.com/xiaochenNN/p/17234617.html)
> [三年 Git 使用心得 & 常见问题整理](https://segmentfault.com/a/1190000023734704)



在Git管理下，大家实际操作的目录被称为工作树，也就是工作区域

### git 别名

Git 并不会在你输入部分命令时自动推断出你想要的命令。 如果不想每次都输入完整的 Git 命令，可以通过 `git config` 文件来轻松地为每一个命令设置一个别名。

```bash
git config --global alias.co checkout
git config --global alias.sw switch
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
```



### git SSH 秘钥生成

秘钥路径：

```	bash
cd ~/.ssh
================>>
authorized_keys2  id_dsa       known_hosts
config            id_dsa.pub
```

在 git bash 中输入命令，引号中内容为邮箱：

```bash
ssh-keygen -t rsa -C "915422643@qq.com"
```

该命令会在用户主目录（Windows：C:\Users\用户名\，Linux：~/）里生产.ssh文件夹，里面有id_rsa和id_rsa.pub两个文件，这两个文件就是SSH Key的秘钥对。其中，id_rsa是私钥，不能泄露，id_rsa.pub是公钥，可以告诉别人。

拷贝 SSH 秘钥后要修改权限，原因是拷贝过来的密钥权限会变宽报错permissions are too open，一般修改为600就好：

```bash 
一般拷贝后文件权限会改变，
chmod 700 id_rsa id_rsa.pub
# 或者
chmod 600 id_rsa id_rsa.pub
# 再不行
chmod 400 id_rsa id_rsa.pub
```

Windows下秘钥默认权限：-rw-r--r--

> 参考资料
>
> [服务器上的 Git - 生成 SSH 公钥](https://git-scm.com/book/zh/v2/%E6%9C%8D%E5%8A%A1%E5%99%A8%E4%B8%8A%E7%9A%84-Git-%E7%94%9F%E6%88%90-SSH-%E5%85%AC%E9%92%A5)


### git 配置
git 有三种配置
* 系统配置（对所有用户都适用）
  存放在 git 的安装目录下：%Git%/etc/gitconfig；若使用 git config 时使用 --system 选项，读写的就是这个文件：
  ```bash
  git config --system core.autocrlf
  ```
* 用户配置（只适用于改用户）
  存放在用户目录下。例如 Linux 存放在：~/.gitconfig；若使用 git config 时使用 --global 选项，读写的就是这个文件：
  ```bash
  git config --global user.name
  ```
* 仓库配置（只对当前项目有效）
  当前仓库的配置文件（也就是工作目录中的 .git/config文件）；若使用 git config 时使用 --local 选项，读写的就是这个文件：
  ```bash
  git config --local remote.origin.url
  ```
  注：每一个级别的配置都会覆盖上层的相同配置，例如 .git/config 里的配置会覆盖 %Git$/etc/gitconfig 中的同名变量。

### 配置个人身份

首次的 Git 设定（设定身份，自己做主）
```bash
git config --global user.name "Zhang San"
git config --global user.email zhangsan@qq.com
```
这个配置信息会在 Git 仓库中提交的修改信息中体现，但和 Git 服务器认证使用的密码或者公钥密码无关。

### 文本换行符配置


### 与服务器认证的配置
常见的两种协议认证的方式
* http/https 协议认证
  设置口令缓存，可以不用每次都输入用户名和密码：
  
  ```bash
  git config --global credential.helper store
  ```
  设置HTTPS证书信任：
  ```bash
  git config http.sslverfy false
  ```
* ssh 协议认证
  SSH 协议是一种非常常用的 Git 仓库访问协议，使用公钥认证、无需输入密码，加密传输，操作便利又保证安全。

### Git 凭证存储

如果大家使用http协议向fetch或push私有库（或push公有库）的话，命令行（或其他git工具）会提示输入用户名和密码，每次这样做都很麻烦，那设置下git证书缓存就好了。

在Git Bash上执行即可：

```shell
git config --global credential.helper wincred
```

然后使用 http 协议操作仓库时输入一次用户名密码就会被缓存起来，后面就不需要重复输入了。



### 创建 git 仓库
创建 git 仓库:
```bash
mkdir git-test
cd git-test
git init 
touch README.md
git add README.md
git commit -m "first commit"
git remote add origin https://gitee.com/cuichaoran/git-test.git
git push -u origin "master"
```
已有仓库?
```bash
cd existing_git_repo
git remote add origin https://gitee.com/cuichaoran/git-test.git
git push -u origin "master"
```


### git remote

* 查看已关联的远程仓库

  ```bash
  git remote -v
  ```

* 添加一个远程仓库（输入的时候不需要输入 `<` 和 `>`）

  ```bash
  git remote add <name> <url>
  ```

  其中，`name` 表示你要给这个远程库起的名字，`url` 表示这个库的地址

* 取消本地目录下关联的远程库

  ```bash
  git remote remove <name>
  ```

  其中，`name` 表示你要给这个远程库起的名字

* 命修改远程主机名

  ```bash
  git remote rename <原主机名> <新主机名>
  ```

  其中，`name` 表示你要给这个远程库起的名字
  

------

补充：
推送到远程库上面已经说了。删除远程分支比较麻烦。一种方式是，可以直接在 github 网页上操作，另一种方式是：
```shell
git push <remote> --delete <branch>
或
git push <remote> :<branch>   #（注意冒号前的空格）
```


### git clone

git clone 只能 clone 远程库的 master 分支，无法 clone 所有分支。

* 从远程主机克隆一个版本库，未指定本地目录名则与远程主机的版本库同名。
```bash
git clone <版本库的网址>
git clone <版本库的网址> <本地目录名>
```




### git fetch

git fetch 命令命令用于从远程获取代码库。

* 将某个远程主机的所有分支的更新，全部取回本地。如果只想取回特定分支的更新，可以指定分支名。
```bash
git fetch <远程主机名>
git fetch <远程主机名> <分支名>
```

> 注：所取回的更新，在本地主机上要用 "远程主机名/分支名" 的形式读取。
> 比如origin主机的master，就要用origin/master读取。

* 取回远程主机的更新以后，可以在它的基础上，使用git switch/checkout命令创建一个新的分支。
```bash
# 在本地创建和远程分支对应的分支，本地和远程分支的名称一致
git checkout -b <branch_name> origin/<branch_name>
```

* 此外，也可以使用 git merge 命令或者 git rebase 命令，在本地分支上合并远程分支。
```bash
git merge origin/master
# 或者
git rebase origin/master
```

 

### git pull

在克隆远程项目的时候，本地分支会自动与远程仓库建立追踪关系，可以使用默认的origin来替代远程仓库名，因此下文中的 <仓库关联命名> 常常写成 origin。若一个本地仓库关联了多个远程仓库，则需要根据实际情况选择 <仓库关联命名>。

* 将远程指定分支拉取且合并到本地**指定**分支上：

  ```bash
  git pull <仓库关联命名> <远程分支名>:<本地分支名>
  
  # 取回origin主机的next分支，与本地的master分支合并
  git pull origin next:master
  ```


* 将远程指定分支拉取且合并到本地**当前**分支上：

  ```bash
  git pull <仓库关联命名> <远程分支名>
  
  # 取回origin/master分支，与当前分支合并
  git pull origin master
  ```

* 将与本地当前分支**同名**的远程分支拉取到本地**当前**分支上(需先关联远程分支，方法如下)

  ```bash
  git pull
  
  // 将本地分支与远程同名分支相关联
  git push --set-upstream origin <本地分支名>
  // 简写方式：
  git push -u origin <本地分支名>
  ```

  在克隆远程项目的时候，本地分支会自动与远程仓库建立追踪关系，可以使用默认的origin来替代远程仓库名，
  所以，我常用的命令就是 git pull origin <远程仓库名>，操作简单，安全可控。

* 将远程指定分支拉取到本地**指定**分支上（本地不存在的分支）:

  ```bash
  git fetch
  git checkout -b 本地分支名 origin/远程分支名
  ```

* 远端分支强制覆盖本地分支

  ```bash
  git fetch origin <远程分支名>
  git reset --hard origin/<远程分支名>
  #  或者使用下面的命令
  git fetch --all
  git reset --hard origin/<远程分支名>
  ```


> **git fetch**：这将更新 git remote 中所有的远程仓库所包含分支的最新commit-id, 将其记录到.git/FETCH_HEAD文件中
>
> 
>
> 所以**可以认为git pull是git fetch和git merge两个步骤的结合**。



### git push

* 将本地当前分支推送到远程**指定**分支上：

  ```bash
  git push <仓库关联命名> <本地分支名>:<远程分支名>
  ```

* 将本地当前分支推送到与本地当前分支**同名**的远程分支上（如果远程仓库没有这个分支，则会新建一个该分支）：

  ```bash
  git push <仓库关联命名> <本地分支名>
  ```

* 将本地当前分支推送到与本地当前分支**同名**的远程分支上(需先关联远程分支，方法方法如下)

  ```bash
  git push
  
  // 将本地分支与远程同名分支相关联
  git push --set-upstream origin <本地分支名>
  // 简写方式：
  git push -u origin <本地分支名>
  ```

  同样的，推荐使用第2种方式，git push origin <远程同名分支名>

> 注意：pull是远程在前本地在后，push相反



### git merge
将指定分支合并到当前分支
  ```bash
  git merge <branch>
  
  # 如果当前是 master 分支，那么下面代码就是将 dev 分支合并到 master 分支
  git merge dev

  # 将源分支合并到目的分支
  git merge <source_branch> <dest_branch>
  ```






### git add

经常会有这么一种情况，一个文件修改了很多次代码，才发现 – 咦？忘记commit了。 而且往往这些修改可能它们本来应该属于不同的提交。

怎么办？总不可能将就一下，直接把一些乱七八糟的修改放在一个commit里吧？

这个时候git add的`-p, --patch`参数就派上大用场了。



这个`(1/1) Stage this hunk [y,n,q,a,d,s,e,?]? `提示是什么意思？

执行`git add --help`然后跳到`INTERACTIVE MODE` 下的 `patch`部分，有详细的解释

默认是按下上述键后还需要按下回车确认的，如果想要直接单键确认，可以修改配置 `interactive.singleKey = true`

(所有的操作都是针对hunk的)

```bash
    y - 取了
    n - 不取
    q - 我不干了，啥也别add,退出吧
    a - 取了这个和此文件后续所有的
    d - 这个不取了，此文件后续所有的我也不取了
    g - 搜索以跳到某个hunk
    / - 以正则搜索某个hunk
    j - 这个未决, 并跳到下一个未决hunk
    J - 这个未决, 并跳到下一个hunk
    k - 这个未决, 并跳到上一个未决hunk
    K - 这个未决, 并跳到上一个hunk
    s - 这个hunk太大了，拆分成更小的hunks吧
    e - 手动编辑当前hunk
    ? - 显示当前帮助信息(当你不记得这些缩写是什么意思时相当有用)
```

```bash
Update>> 1,2
           staged     unstaged path
* 1:    unchanged        +0/-1 TODO
* 2:    unchanged        +1/-1 index.html
  3:    unchanged        +5/-1 lib/simplegit.rb
```

> [7.2 Git 工具 - 交互式暂存](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E4%BA%A4%E4%BA%92%E5%BC%8F%E6%9A%82%E5%AD%98)
> [Git tips – 同一个文件修改了多处如何分作多个提交](https://ttys3.dev/blog/git-how-to-commit-only-parts-of-a-file)



### git commit

`git commit`命令用于将暂存区中的变化提交到仓库区。

`-m`参数用于指定 commit 信息，是必需的。如果省略`-m`参数，`git commit`会自动打开文本编辑器，要求输入。

```shell
git commit -m "message"
```

`git commit`命令可以跳过暂存区，直接将文件从工作区提交到仓库区。

```shell
git commit <filename>  -m "message"
```

上面命令会将工作区中指定文件的变化，先添加到暂存区，然后再将暂存区提交到仓库区。



-a

`-a`参数用于先将所有工作区的变动文件，提交到暂存区，再运行`git commit`。用了`-a`参数，就不用执行`git add .`命令了。

```shell
git commit -am "message"
```



--amend

`--amend`参数用于撤销上一次 commit，然后生成一个新的 commit。

```shell
git commit --amend - m "new commit message"
```

```bash
git commit --amend
```

在弹出的 vim 编辑窗口中，最上方，修改 message 后，:wq 即可。

> 参考网址：[7.6 Git 工具 - 重写历史](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E9%87%8D%E5%86%99%E5%8E%86%E5%8F%B2)
> [git-cz 讓你的 Git Commit 訊息更美一點！](https://israynotarray.com/git/20221115/721294310/)



### git stash

贮藏（stash）会处理工作目录的脏的状态——即跟踪文件的修改与暂存的改动——然后将未完成的修改保存到一个栈上， 而你可以在任何时候重新应用这些改动（甚至在不同的分支上）。

```shell
# 贮藏修改，将新的贮藏推送到栈上（ git stash 或 git stash push）
git status
git stash push -m "save message"
# git stash save 会逐渐弃用

# 查看贮藏的东西
git stash list

# 应用其中一个的贮藏，栈上不删除（指定一个贮藏，Git 认为指定的是最近的贮藏）
git stash apply
git stash apply stash@{2}

# 应用贮藏并从栈上删除
git stash pop

# 移除贮藏
git stash drop stash@{0}
```



### git log

`git log`命令用于显示提交日志信息。

```shell
git log [<options>] [<revision range>] [[\--] <path>…]
```

* 将显示最近三次的提交。

  ```shell
  git log -3
  ```

* 根据提交ID查询日志

  ```shell
  git log commit_id  　　			#查询ID(如：6bab70a08afdbf3f7faffaff9f5252a2e4e2d552)之前的记录，包含commit
  git log commit1_id commit2_id 	 #查询commit1与commit2之间的记录，包括commit1和commit2
  git log commit1_id..commit2_id 	 #同上，但是不包括commit1
  ```

  > 其中，commit_id可以是提交哈希值的简写模式，也可以使用HEAD代替。HEAD代表最后一次提交，`HEAD^`为最后一个提交的父提交，等同于`HEAD～1`，`HEAD～2`代表倒数第二次提交

* `--pretty`按指定格式显示日志信息,可选项有：oneline,short,medium,full,fuller,email,raw以及format:,默认为medium，可以通过修改配置文件来指定默认的方式。

  ```shell
  git log (--pretty=)oneline
  ```

* 图形显示

  ```shell
  git log --oneline --decorate --graph --all
  ```






### git branch

* 查看分支

  ```bash
  # 查看本地分支
  git branch
  
  # 查看远端分支
  git branch -r
  
  # 查看所有分支（本地和远端，标红的是远端）
  git branch -a
  ```

* 显示分支 sha1、commit 信息、工作区(工作树)

  ```bash
  git branch -v
  
  # 指定两次 v，会打印工作树（如果有）和上游分支名
  git branch -vv
  # 如：
  # master23b		bd52c0c1953 [23B/master] merge 'br_l3_l00504464_23A_23B_2' into 'master'
  ```

* 在本地新建一个分支（新分支commit信息与当前分支commit信息相同）

  ```bash
  git branch <新分支名>
  ```

* 本地关联远程分支
  使用git在本地新建一个分支后，需要做远程分支关联。如果没有关联，git会在下面的操作中提示你显示的添加关联。

关联目的是在执行git pull, git push操作时就不需要指定对应的远程分支，你只要没有显示指定，git pull的时候，就会提示你。

  ```bash
  # 本地当前分支关联远程分支
  git branch -u origin/<remote_branch>
  git branch --set-upstream-to=origin/<remote_branch>

  # 本地指定分支关联远程分支
  git branch -u origin/<remote_branch> <local_branch>
  git branch --set-upstream-to=origin/<remote_branch> <local_branch>
  ```


* 本地分支重命名（还没有推送到远程）

  ```shell
  # 如果对于分支不是当前分支，可以使用下面代码：
  git branch -m <原分支名> <新分支名>
  
  # 如果是当前分支，那么可以使用加上新名字：
  git branch -m <新分支名>
  ```

* 远程分支重命名（已经推送远程-假设本地分支和远程对应分支名称相同，且处于本地分支）

  step1. 重命名远程分支对应的本地分支

  ```shell
  git branch -m <原分支名> <新分支名>
  ```

  step2. 删除远程分支

  ```shell
  git push --delete origin <原分支名>
  ```

  step3. 上传新命名的本地分支

  ```shell
  git push origin <新分支名>
  ```

  step4. 把修改后的本地分支与远程分支关联

  ```shell
  git branch --set-upstream-to origin/<新分支名>
  git branch --set-upstream-to=23B/master 23bmaster
  ```

* 



### git chekcout

git checkout 这个命令承担了太多职责，既被用来切换分支，又被用来恢复工作区文件，对用户造成了很大的认知负担。

Git社区发布了Git的新版本2.23。在该版本中，有一个特性非常引人瞩目，就是新版本的Git引入了两个新命令 git switch 和 git restore，用以替代现在的 git checkout。换言之，git checkout 将逐渐退出历史舞台。

Git社区决定这样做，是因为目前 git checkout 命令承载了太多的功能，这让新手们感到困惑。git checkout 的核心功能包括两个方面，一个是分支的管理，一个是文件的恢复。这两个核心功能，未来将由 git switch 和 git restore 分别负责。

1. 切换与创建分支

    ```shell
    git checkout <branch_name > 切换分支
    #git switch <branch_name> 切换分支
    git checkout -b <branch_name> 创建并切换至分支
    # git switch -c <branch_name> 创建并切换至分支
    ```

​	**git checkout -b** <branch_name>**origin/**<branch_name> 在本地创建和远程分支对应的分支，本地和远程分支的名称最好一致

2. 还原工作区（文件内容）
   git checkout – <file_name> 丢弃工作区的修改，并用最近一次的commit内容还原到当前工作区（对文件中内容的操作，无法对添加文件、删除文件起作用）

   git checkout HEAD^ – <file_name> 将指定commit提交的内容(HEAD^表示上一个版本)还原到当前工作区

   git checkout <branch_name> – <file_name> 将指定分支的指定提交内容还原到当前分支工作区



> [工具系列 | git checkout 可替换命令 git switch 和 git restore](https://www.cnblogs.com/tinywan/p/12344267.html)
>
> https://blog.csdn.net/Sweet_19BaBa/article/details/111950384



### git switch

* 切换分支（本地已有分支 / 本地不存在但远端存在分支）

  ```bash
  git switch <branchName>
  # 如果要切换到某个commit-id，只能用 checkout，如
  git checkout commitid # 切换到某个commit id
  ```

  > 远程有而本地没有的分支，而如果要从远程分支建一个同名的本地分支，并且关联远程分支。可以理解为拉取远程分支到本地，并建立远程分支和本地分支的关联关系

* 切换到上一个切换的分支

  ```bash
  git switch -
  ```

* 创建一个新分支并切换到该新分支

  ```bash
  git switch -c <branchName>
  ```

* 以一个提交commit来创建一个分支

  ```bash
  git switch -c <new_branch_name> <commid_id>
  # 或用
  git checkout -b <new_branch_name> <commid_id>
  ```

  其中，`new_branch_name` 是要创建的新的本地分支名称，`commid_id` 是 cherry-pick 或 fetch 后的最新commit id。

  显示 commit id 而不是分支名的情况：

  1. 在本地 A 仓库拉取 B 仓库 master 分支，checkout 到 B/master 后，是只有最新 commit id 而没有分支名称的。

  2. cherry-pick 后的代码没有分支名，只有最新的 commit id，同样需要为最新的 commit id 创建一个分支，用于推送远程仓库时

> 切换分支时，如果有未提交的修改，会把修改带到切换后的分支。如果想保证切换后的分支干净，需要在切换前 commit 或 stash 修改。



### git store

**git restore** 命令用于恢复或撤销文件的更改。

**git restore** 命令作用包括还原文件到最新提交的状态、丢弃未暂存的更改、丢弃已暂存但未提交的更改等。

```shell
# 「工作区修改撤销」将 <file> 恢复到最新的提交状态，丢弃所有未提交的更改。对于撤销不需要的更改非常有用
git restore <file>
git restore .		# 全部文件，工作区修改撤销

# 「暂存区重新放回工作区」如果你已经使用 git add 将文件添加到暂存区，但希望重新放回工作区
git restore --staged <file>
git restore --staged .		# 全部文件，暂存区重新放回工作区

# 「还原文件到指定提交的状态」将文件 <file> 恢复到特定提交 <commit> 的状态，但分支已有提交节点不会变化，且回退的差异会保存在工作区。将文件还原到历史版本时非常有用
git restore --source=<commit> <file>

# 「交互式还原」执行这个命令它会打开一个交互式界面，让你选择如何处理每个更改。
git restore -i
```



### git reset

git reset 命令用于回退版本，可以指定退回某一次提交的版本。

```
git reset [--soft | --mixed | --hard] [HEAD]
```

--mixed(默认)：将指定 commit id 撤回之后所有内容`全部放进工作区`中。

--soft：将指定 commit id 撤回之后所有内容`全部放进暂存区`。

--hard：将指定 commit id 撤回并`清空工作目录及暂存区`所有修改。

```bash
HEAD 说明：
HEAD 表示当前版本
HEAD^ 上一个版本
HEAD^^ 上上一个版本
HEAD^^^ 上上上一个版本
以此类推...

可以使用 ~ 数字表示
HEAD~0 表示当前版本
HEAD~1 上一个版本
HEAD^2 上上一个版本
HEAD^3 上上上一个版本
以此类推...
```






### git diff

假定：HEAD、缓存区、工作区中的 <file_name> 文件内容均不相同。

```shell
# 工作区（已track未add） <=> 暂存区（已add未commit）。若暂存区为空对比的是：工作区 <=> 最近一次commit。
git diff <file_name>

# 暂存区（已add未commit） <=> 最近一次commit(HEAD)
git diff --cached <file_name>	# 或
git diff --staged <file_name>

# 工作区（已track未add）+暂存区（已add未commit） <=> 最近一次commit(HEAD)
git diff HEAD <file_name>

# 最近一次commit(HEAD) <=> 过去X个的之前的 commit。
git diff HEAD~X		# X为正整数
git diff HEAD^^^	# 有X个^符号


# 两个分支上最后 commit 的内容的差别
git diff <branch_name1> <branch_name2> <file_name>

# 两个 commit 节点的差异
git diff <commit_hash> <commit_hash> <file_name>
```






### git rebase

rebase的作用简要概括为：可以对某一段线性提交历史进行编辑、删除、复制、粘贴；因此，合理使用rebase命令可以使我们的提交历史干净、简洁！

**使用git rebase合并多次commit：**

* 方法1：指名要合并的版本号区间

  ```bash
  git rebase -i  [startpoint]  [endpoint]
  ```

  其中 `-i` 的意思是 `--interactive`，即弹出交互式的界面让用户编辑完成合并操作，`[startpoint] [endpoint]`则指定了一个编辑区间，如果不指定`[endpoint]`，则该区间的终点默认是当前分支 HEAD 所指向的 commit （注：该区间指定的是一个前开后闭的区间，`[startpoint]` **本身不参与合并**，可以把它当做一个坐标）。

* 方法2：从HEAD版本开始往过去数3个版本

  ```bash
  git rebase -i HEAD~3 
  ```

  在弹出的 vim 编辑窗口中，会列出要合并的 commit message，提交时间最早的列在上面，最晚的在下面，由于 squash 是要和前一个 commit 合并，因此**最早的一个填 pick，比较晚的几个都填 squash**，然后 `:wq` 即可。

  > 指令解释（交互编辑时使用）：
  >
  > pick：保留该commit（缩写:p）
  >
  > reword：保留该commit，但我需要修改该commit的注释（缩写:r）
  >
  > edit：保留该commit, 但我要停下来修改该提交(不仅仅修改注释)（缩写:e）
  >
  > squash：将该commit和前一个commit合并（缩写:s）
  >
  > fixup：将该commit和前一个commit合并，但我不要保留该提交的注释信息（缩写:f）
  >
  > exec：执行shell命令（缩写:x）
  >
  > drop：我要丢弃该commit（缩写:d）



```shell
# 重新打开vim窗口
git rebase --edit-todo
```



### git revert

Git revert 用于撤回某次提交的内容，同时再产生一个新的提交(commit)。原理就是在一个新的提交中，对之前提交的内容相反的操作。

```shell
git revert -n commit-id
# 反做多个commit-id
git revert -n commit-idA..commit-idB
```



### git reflog

git reflog 命令是用来恢复本地错误操作很重要的一个命令，可处理代码丢失、恢复代码。
> reflog 是 Git 操作的一道安全保障，它能够记录几乎所有本地仓库的改变。包括所有分支 commit 提交，已经删除（其实并未被实际删除）commit 都会被记录。总结而言，只要 HEAD 发生变化，就可以通过 reflog 查看到。

```bash
# 执行 git reflog 查看操作日志
git reflog

# 查看对应的版本号,就可以恢复到任意版本:
git reset --hard <commit-id>
```



### git cherry-pick

* 将指定的提交（commit）应用于其他分支（先 checkout 到目的分支，在目的分支上执行此命令）。

  ```bash
  git cherry-pick <commitHash>
  ```

* 一次转移多个提交

  ```bash
  # 任意多个
  git cherry-pick <HashA> <HashB> <HashN>
  # 连续多个，不包含A，(A, B]
  git cherry-pick A..B 
  # 连续多个，包含A，[A, B]
  git cherry-pick A^..B 
  ```

  > 连续多个提交，它们必须按照正确的顺序放置：提交 A 必须早于提交 B，否则命令将失败，但不会报错。

* 合并节点转移

  如果原始提交是一个合并节点，来自于两个分支的合并，那么 Cherry pick 默认将失败，因为它不知道应该采用哪个分支的代码变动。

  `-m`配置项告诉 Git，应该采用哪个分支的变动。它的参数`parent-number`是一个从`1`开始的整数，代表原始提交的父分支编号。

  ```bash
  # 采用提交commitHash来自编号1的父分支的变动。
  git cherry-pick -m 1 <commitHash>
  ```

  > 一般来说，1号父分支是接受变动的分支（the branch being merged into），2号父分支是作为变动来源的分支（the branch being merged from）。

* 代码冲突

  ```bash
  # 继续 cherry-pick（先执行 `git add .` 将修改加入暂存区，再执行下面命令）
  git cherry-pick --continue
  # 取消 cherry-pick（这种情况下当前分支恢复到cherry-pick前的状态，没有改变）
  git cherry-pick --abort
  # 终止 cherry-pick（这种情况下当前分支中未冲突的内容状态将为modified）
  git cherry-pick --quit
  ```



### git rm

git rm 命令用于删除文件。

如果只是简单地从工作目录中手工删除文件，运行 **git status** 时就会在 **Changes not staged for commit** 的提示。

git rm 删除文件有以下几种形式：

1. 将文件从暂存区和工作区中删除：

   ```shell
   git rm <file>
   
   # 如果删除之前修改过并且已经放到暂存区域的话，则必须要用强制删除选项 -f。
   git rm -f <file>
   ```

2. 如果想把文件从暂存区域移除，但仍然希望保留在当前工作目录中，换句话说，仅是从跟踪清单中删除，使用 **--cached** 选项即可：

   ```shell
   git rm --cached <file>
   ```



### git clean

`git clean` 命令用来从你的工作目录中删除所有没有 tracked 过的文件。

`git clean` 经常和 `git reset --hard` 一起结合使用。reset 只影响被 track 过的文件, 所以需要 clean 来删除没有 track 过的文件。结合使用这两个命令能让你的工作目录完全回到一个指定的 <commit> 的状态

* 用法

  ```bash
  # 列出哪些文件会被删除，但不会真正的删除文件，只是一个提醒
  git clean -n
  
  # 删除当前目录下所有没有track过的文件。不会删除.gitignore文件里面指定的文件夹和文件, 不管这些文件有没有被track过
  git clean -f
  
  # 删除指定路径下的没有被track过的文件
  git clean -f <path>
  
  # 删除当前目录下没有被track过的文件和文件夹 ---- 常用
  git clean -df
  
  # 删除当前目录下所有没有track过的文件. 不管是否为.gitignore文件里面指定的文件夹和文件
  git clean -xf
  
  ```

git reset --hard 和 git clean -f 是一对好基友，结合使用他们能让你的工作目录完全回退到最近一次 <commit> 的时候。

下面的例子要删除所有工作目录下面的修改, 包括新添加的文件. 假设你已经提交了一些快照了, 而且做了一些新的开发运行后, 工作目录和缓存区回到最近一次 <commit> 时候一摸一样的状态，git status 会告诉你这是一个干净的工作目录, 又是一个新的开始了！

```bash
git reset --hard
git clean -df
```

git clean 对于刚编译过的项目也非常有用. 如, 他能轻易删除掉编译后生成的.o和.exe等文件. 这个在打包要发布一个release的时候非常有用



### git 仓库忽略大小写

```bash
git config core.ignorecase true
```



### git rebase调整commit之间顺序

1. 使用 `git rebase -i` 进入编辑

   ```shell
   git rebase -i <after-this-commit>	# 不含本次commit id
   git rebase -i HEAD~3 
   ```

2. vim 命令模式（Command mode），调整 commit id 的`行的顺序`。dd剪切，p粘贴（后），P粘贴（前）。

3. 编辑完成之后，:wq退出编辑模式，即可完成commit顺序的调整。

> 注：若这个提交有先后依赖关系，则不会成功。
>
> 参考网址：[7.6 Git 工具 - 重写历史](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E9%87%8D%E5%86%99%E5%8E%86%E5%8F%B2)
>
> [git rebase调整commit之间顺序](https://blog.csdn.net/allanGold/article/details/92836941)



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





### git 修改.gitignore后重新生效

```shell
git rm -r --cached .  #清除缓存
git add . #重新trace file
git commit -m "update .gitignore" #提交和注释
git push origin master #可选，如果需要同步到remote上的话
```

会在已有的提交上新增一个提交，并且刷新 `.gitignore` 文件。



配置语法:

以斜杠“/”开头表示目录；
以星号“*”通配多个字符；
以问号“?”通配单个字符
以方括号“[]”包含单个字符的匹配列表；
以叹号“!”表示不忽略(跟踪)匹配到的文件或目录；





### 利用git bisec二分法查找定位bug问题
如果出现bug，很容易想到的是回滚git记录查找bug出现的提交，通常可以手动回滚记录进行定位，找到引入bug的提交进行修复。git提供了一种二分查找的方式帮助开发者快速定位bug引入的提交。很久没用做个记录。

步骤：
开始git二分定位
标记包含bug提交
标记上一个不含bug的提交
运行验证
进行标记
重复2~5步
定位bug git提交
结束git二分查找
修复bug

实战
步骤1：开始二分查找
git bisec start

步骤2：假设当前提交包含bug，进行标记
git bisec bad

步骤3：找到上一个不含bug的提交，假设在之前的提交46aa1abd5不含bug，进行标记
git bisec good 46aa1abd5

步骤4：git会自动回滚到两次提交中间的提交，运行代码进行验证
步骤5：进行标记，标记后代码会自动回滚或者前进到中间git提交

如果回滚后依旧存在bug，进行bad标记：$ git bisec bad
如果回滚后bug没了，进行good标记：$ git bisec good，这里不用跟commit hash也行了，默认是当前提交。

步骤6：重复前前几步，知道git提示找到了bug引入的提交记录
步骤7：根据之前的标记，git会找到引入bug的commit提交
提示如：
bash复制代码da5207dec2(这里是你的git记录) is the first bad commit
// 下面的提示省略。。。

关键字在 is the first bad commit，说明这个提交引入了bug，review代码进行修复吧。
步骤8：结束git二分查找
git bisec reset




### git 对象在一个项目里面具体的运作方式
Git文件版本管理依赖于核心四对象及相互之间指向关系：标签(tag)->提交(commit)->目录树(tree) )->块(blob).
Git为了降低对象文件的存储、传输成本，提供了GC机制，将松散对象等文件收纳到包文件。


git cat-file -t <commit-id>

git cat-file commit <commit-id>

git cat-file tree <tree-id>
git ls-tree <tree-id>

git cat-file blob <blob-id>


### git 钩子机制
和其它版本控制系统一样，Git能在特定的动作发生时触发执行用户自定义脚本，这便是钩子机制。
Git可以在客户端部署和触发钩子，也能在服务器端部署和触发钩子。

* 客户端钩子
对于非裸版本库，客户端钩子在本地工程。git/hooks目录下，可以在提交、合并、推送等操作时候触发用户自定义脚本。

* 服务端钩子
服务器端的钩子是项目管理人员用来给项目执行强制管理策略的，可以在接收到推送、拉取请求时候触发用户自定义脚本。
1.Git的钩子样例均以。sample结尾，表示不生效，如需生效钩子，请删除该后缀
2.Git的钩子脚本并无类型限制shell、python等均可，但勿直接设置二进制执行件为钩子
3.部分Git钩子是支持逃逸的，在执行相应git命令时候增加--no-verify选项即可跳过钩子调用
4.多数钩子分pre和post，也就是指定在git命令操作前还是后进行调用，注意钩子是阻塞性的

Git钩子机制分为客户端钩子与服务器端钩子：客户端钩子可用于开发人员前置的门禁检查等，服务器端钩子可用于项目管理员对项目执行自动化的远端管理操作。




### git 报错：SSL certificate

```markdown
*SSL certificate problem: unable to get local issuer certificate*
```

这个是由于Git默认开启了SSL验证，关闭即可；

解决方式：

```bash
git config --global http.sslVerify false
```

执行以上git命令，关闭ssl验证。



### git 报错：Received HTTP code 504

**Windows**：在连接 **Bitbucket**（AKA **stash**）之前，您需要从 Git 和控制台环境中清除所有代理：

```
SET HTTP_PROXY=
SET HTTPS_PROXY=
git config --global --unset http.proxy
git config --global --unset https.proxy
# git clone http://yourUser@stashAddress:stashPort/apptest.git
```

但是如果你需要连接到像 **github** 这样的公共存储库，那么就需要再次定义代理：

```
SET HTTP_PROXY=proxyaddress:port
SET HTTPS_PROXY=proxyaddress:port
git config --global http.proxy http://proxyaddress:port
git config --global https.proxy http://proxyaddress:port
```

我认为它可能对在公司防火墙后面工作的其他开发人员有用。

**Linux**

```
unset HTTP_PROXY
unset HTTPS_PROXY
git config --global --unset http.proxy
git config --global --unset https.proxy
# git clone http://yourUser@stashAddress:stashPort/apptest.git
```

再次定义代理：

```
export HTTP_PROXY=proxyaddress:port
export HTTPS_PROXY=proxyaddress:port
git config --global http.proxy http://proxyaddress:port
git config --global https.proxy http://proxyaddress:port
```

*注意环境变量的大写。某些操作系统版本可能需要小写字母或默认定义了小写字母变量。*





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


### GIT 自动补全命令,分支名 以及 高亮显示当前分支

【注】`~/.bashrc` 是 Linux 的，对应到 Mac 是 `~/.bash_profile` ，看网上的教程要注意区分和替换

##### 1、执行以下命令，克隆官方git库，然后在`git/contrib/completion`找到两个关键文件

```shell
git clone https://github.com/git/git.git
cd git/contrib/completion
```

- `contrib/completion/git-completion.bash` 自动补全
- `contrib/completion/git-prompt.sh` 高亮显示当前分支名称

##### 2、执行以下命令，将两个文件复制到用户目录，并设置隐藏

```shell
cp git-completion.bash ~/.git-completion.bash
cp git-prompt.sh ~/.git-prompt.sh
```

##### 3、配置 `~/.bash_profile` 文件，没有该文件就新增，然后加入以下内容(会使命令响应时间变长...)

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

##### 4、执行以下命令进行刷新

```
source ~/.bash_profile
```


### 解决git命令会将结果输出到单独窗口必须按q才能退出的问题

这与 git 的 pager 设置有关。

pager 其实就是分页器，也就是对一大段内容进行分页显示的工具，git 在一些版本中**默认使用的是 less 工具**，不同的版本默认设置会有差异，这也就是造成我在 windows 下没有自动分页，而在 linux 下会打开新窗口进行分页的原因。

git 的分页器可以通过 core.pager 来进行设置，他会被 git 命令行解释，影响分页器的变量有多个，他们起作用的顺序依次是

1. `$GIT_PAGER` 环境变量
2. `core.pager` git配置
3. `$PAGER` 环境变量

如果这些都没有设置，默认会选择编译时的选项（通常为less），具体细节可以参考官方文档 [git core.pager](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corepager)。

```shell
# 全局禁用分页器，直接显示在终端窗口上，不再进行分页处理
# git branch 比较方便，但 git log 等长页显示会一直滚屏，巨难用
git config --global core.pager ''

# 对某个命令禁用分页器，只想屏蔽 git branch 的分页，而想保留git show 和 git log 等的分页显示
git config --global pager.branch false # git branch 不分页
# 重新启用分页器
git config --global pager.branch true # git branch 分页
```

> [解决git命令会将结果输出到单独窗口必须按q才能退出的问题](https://blog.csdn.net/albertsh/article/details/114806994)



### vscode git 不显示修改颜色标记  Gutter Indicators

搜了半天，发现这玩意叫做Gutter Indicators。作用是在一个git仓库中，如果对某个文件做了修改，编辑器会在行号旁边用不同颜色标志该文件的修改情况。

原因是在项目最外层文件夹（项目名的同级目录下）git init了，产生了.git文件。

解决方法：在终端进入最外层（项目名所在目录，而不是下一层）的文件夹执行 rm -rf .git 命令即可。

https://www.jianshu.com/p/2d70f26e4229

git项目,VSCode显示不同颜色块的含义:https://www.cnblogs.com/soyxiaobi/p/9708518.html





## Git commit 规范

### Git commit 规范

https://zhuanlan.zhihu.com/p/182553920

**commit message格式**

```text
<type>(<scope>): <subject>
```

**type(必须)**

用于说明git commit的类别，只允许使用下面的标识。

feat：新功能（feature）。

fix/to：修复bug，可以是QA发现的BUG，也可以是研发自己发现的BUG。

* fix：产生diff并自动修复此问题。适合于一次提交直接修复问题
* to：只产生diff不自动修复此问题。适合于多次提交。最终修复问题提交时使用fix

docs：文档（documentation）。

style：格式（不影响代码运行的变动）。

refactor：重构（即不是新增功能，也不是修改bug的代码变动）。

perf：优化相关，比如提升性能、体验。

test：增加测试。

chore：构建过程或辅助工具的变动。

revert：回滚到上一个版本。

merge：代码合并。

sync：同步主线或分支的Bug。

**scope(可选)**

scope用于说明 commit 影响的范围，比如数据层、控制层、视图层等等，视项目不同而不同。



### Git-cz 工具







## 代码对比工具

### diff命令

`diff` 命令是 Linux 下自带的一个强大的文本比对工具，而且使用起来非常方便。而且它在大多数的 Linux 发行版里已经预装了，它可以逐行比对两个文本文件，并输出它们的差异点。更多介绍可以直接查看它的 man 手册。

```text
$ man diff
```

但是，diff 命令虽然强大，但它的输出结果实在是太感人了，不直观也不清晰。于是，有大佬为了弥补这个缺点，基于 diff 开发了更强大的工具。这里推荐两个：`colordiff` 和 `wdiff` 。

**colordiff命令**

`colordiff` 是一个 Perl 脚本工具，它的输出结果和 diff 命令一样，但是会给代码着色，并且具有语法高亮功能。同时，你如果不喜欢它的默认颜色的话，还可以自定义主题。

你可以自行安装 colordiff 到你的电脑，根据不同的发行版选择不同的安装命令。

```text
$ yum install colordiff             [On CentOS/RHEL/Fedora]
$ dnf install colordiff             [On Fedora 23+ version]
$ sudo apt-get install colordiff    [On Debian/Ubuntu/Mint]
```

同样，你可以使用 man 命令查看它的帮助文档：

```text
$ man colordiff
```

**wdiff命令**

diff 命令是逐行比较差异，而 `wdiff` 更变态，是逐字比较。所以如果你的文本只是修改了少数一些词语的话，使用 wdiff 命令将更加高效。

安装命令如下：

```java
$ yum install wdiff             [On CentOS/RHEL/Fedora]
$ dnf install wdiff             [On Fedora 23+ version]
$ sudo apt-get install wdiff    [On Debian/Ubuntu/Mint]
```

更详细内容可以查看它的 man 手册。

```text
$ man wdiff
```

### vimdiff命令

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

鼠标移动到MERGED窗口(CTRL-w切换窗口)，

:diffget REMOTE # 获取REMOTE的修改到MERGED文件, 忽略大小写
:diffg BASE # get from base
:diffg LOCAL # get from local

注意：通过diffget只能选取local, base, remote三种的一种，要想都需要3种或者两种，只能通过修改MERGED文件

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



> [推荐9款代码对比工具](https://zhuanlan.zhihu.com/p/336414874)



## [如何解决Git中的合并冲突？详细操作步骤指南](https://www.lsbin.com/9410.html)

### [Git 冲突显示方式](https://taoshu.in/git/git-diff3.html)

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

这其中`<<<<<<< HEAD`与`=======`之间的部分表示当前所在分支（也就是HEAD）的内容，而`=======`与`>>>>>>> feature_branch`之间的部分则是 feature_branch 分支的内容。看到这个冲突就头大，因为我们无法确定要留哪一行删哪一行。



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

```
git checkout --ours <file name>
```

或者，要接受**所有**冲突文件的本地版本，请使用：

```
git merge --strategy-option ours
```

2.**接受远程版本**。要从远程分支更新文件的更改，请运行：

```
git checkout --theirs <file name>
```

接受**所有**冲突文件的远程版本：

```
git merge --strategy-option theirs
```

3.**单独审查更改**。最后一个选项是分别查看每个更改。此选项也是最佳选择，尤其是在处理多个文件和人员时。为了使这项工作更易于管理，请使用特殊工具来帮助查看个别冲突。

最终，选择保留哪些代码部分以及不保留哪些部分取决于开发人员对当前项目的决定。



### git 使用ours和theirs

> [Git-优雅地解决冲突：使用ours和theirs]https://blog.csdn.net/qq_41603165/article/details/104922336

对于merge和rebase来说，ours 和 theirs 对应的分支正好是相反的。

假设当前指向的分支为`branch_a`，

在使用 merge 时 `git merge branch_b`，ours 指的是当前分支，即branch_a，theirs 指的是要被合并的分支，即branch_b。

而在使用 rebase 时 `git rebase branch_b`，theirs 指的是当前分支，即branch_a，ours 指向修改参考分支，即branch_b。



git merge会抽取两个分支上新增的提交，并将其合并在一起，产生一个新的提交D，生成的D节点有两个父节点。其中在合并的过程中可能会发生冲突。

git rebase会以branch_a为参照，提取branch_b分支上的提交，将这些修改作用在branch_a分支上，最终结果不会产生新的提交节点。其中在将提取的修改作用在branch_a的过程中可能会发生冲突。

通常而言，在开发过程中很少应用git merge合并代码，更常用的是git rebase。此外在开发过程中，经常使用git rebase命令获取master主分支的最新提交代码，在完成个人的开发任务之后，也需要rebase master分支上的代码才能申请 Pull Request，自动合并。



### Git 设置默认 Diff 工具

[Git中的合并冲突如何解决](https://www.lsbin.com/tag/git中的合并冲突如何解决/)？为 设置默认差异工具**`git mergetool`**：

1. 在终端中运行以下行：

```shell
git mergetool --tool-help
```

输出打印出当前设置的所有支持的差异工具：

```shell
'git mergetool --tool=<tool>' may be set to one of the following:
                meld
                tortoisemerge
                vimdiff
                vimdiff1
                vimdiff2
                vimdiff
The following tools are valid, but not currently available:
                araxis
                bc
                bc3
                bc4
```

根据选择的编辑器，可以使用不同的工具。例如：

- **Emacs**差异工具：Ediff 或emerge
- **Vim**差异工具：vimdiff、vimdiff2 或 vimdiff3

[Git合并冲突的解决方法](https://www.lsbin.com/tag/git合并冲突的解决方法/)：进一步的步骤显示了如何为 Vim设置**vimdiff**工具的示例。

2. 更改 `git config` 设置默认合并工具：

```shell
git config merge.tool <tool name>
# 例如，如果使用 Vim，请运行：
git config merge.tool vimdiff
```

3. 设置冲突显示格式， diff3 工具以显示两个文件的共同祖先，即任何编辑之前的版本：

```shell
git config merge.conflictstyle diff3
```

4. 启动合并解析工具前不提示：

```
git config mergetool.prompt false
```

Git 的 diff 工具设置已完成。



### Mergetool 查看差异解决合并冲突

如何解决Git中的合并冲突？要使用**`mergetool `**并查看差异，请运行：

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

> 配置 vim 快捷键：**[Git_mergetool_tutorial_with_Vim.md](https://gist.github.com/karenyyng/f19ff75c60f18b4b8149)**
>
> ```shell
> let mapleader=','
> let g:mapleader=','
> 
> if &diff
>  map <leader>1 :diffget LOCAL<CR>
>  map <leader>2 :diffget BASE<CR>
>  map <leader>3 :diffget REMOTE<CR>
> endif
> ```
>
> vim 窗口移动
>
> ```shell
> Ctrl+W+W     # toggle between the diff columns
> Ctrl w + h   # move to the split on the left 
> Ctrl w + j   # move to the split below
> Ctrl w + k   # move to the split on top
> Ctrl w + l   # move to the split on the right
> # 对于高级导航，可通过命令获取信息:help window-moving。
> ```
>
> 
>
> [关于vim：使用vimdiff时加载不同的颜色](https://www.codenong.com/2019281/)



### vim 中用于解决冲突的相关命令

作为编辑器之神, vim 自然早早就考虑到了很多人会使用其进行冲突合并, 因此也内置了很多非常高效有用的操作命令, 我挑选了比较有用的列在下面:

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

- `:ls!`: 显示当前所有缓冲区的号码kkkjk

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

Git合并冲突的解决方法：最后一步是提交和清理额外的文件。通过运行提交更新的版本：

```
git commit -m "<your message>"
```

diff 工具会在项目上创建额外的文件来比较版本。用以下方法清理它们：

```
git clean -f
```

![如何解决Git中的合并冲突？详细操作步骤指南](https://www.lsbin.com/wp-content/uploads/2021/11/git-clean-output.png)



vimdiff命令

vimdiff命令

如果希望把一个差异点中当前文件的内容复制到另一个文件里，可以使用命令

    dp （":diffget"）

如果希望把另一个文件的内容复制到当前行中，可以使用命令

    do (":diffput"，"o" 表示 "obtain" (不能用"dg"，因为那可能是 "dgg" 的开始！))

在比较和合并告一段落之后，可以用下列命令对两个文件同时进行操作。比如同时退出：

    :qa （quit all）

如果希望保存全部文件：

    :wa （write all）

或者是两者的合并命令，保存全部文件，然后退出：

    :wqa （write, then quit all）

如果在退出的时候不希望保存任何操作的结果：

    :qa! （force to quit all）



如何防止 git vimdiff 以只读方式打开文件？

    [difftool "vimdiff"] 
            cmd = vimdiff "$LOCAL" "$REMOTE"

配置 Git 以使用 Vimdiff

默认情况下，vimdiff 将以只读模式打开文件，以便您无法进行任何更改。您可以通过运行以下命令在编辑器内启用编辑：

    :set noro

要使其成为默认值，请编辑您的$HOME/.vimrc配置，添加以下内容（您可能需要创建它）：



