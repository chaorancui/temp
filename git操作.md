[toc]

# git

在Git管理下，大家实际操作的目录被称为工作树，也就是工作区域

### git 别名

Git 并不会在你输入部分命令时自动推断出你想要的命令。 如果不想每次都输入完整的 Git 命令，可以通过 `git config` 文件来轻松地为每一个命令设置一个别名。

```bash
git config --global alias.co checkout
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
ssh-keygen -t rsa -C "cuichaoran@huawei.com"
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

  

------

补充：
推送到远程库上面已经说了。删除远程分支比较麻烦。一种方式是，可以直接在 github 网页上操作，另一种方式是：`git push <name> :<branch>` （注意冒号前的空格）



### git switch

* 切换分支（本地已有分支 / 本地不存在但远端存在分支）

  ```bash
  git switch <branchName>
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

  2. cherry-pick 后的代码没有分支名，只有最新的 commit id，同样需要为最新的 commit id 创建一个分支，用于推送远程仓库时。



### git clone

git clone 只能 clone 远程库的 master 分支，无法 clone 所有分支。



### git pull

在克隆远程项目的时候，本地分支会自动与远程仓库建立追踪关系，可以使用默认的origin来替代远程仓库名，因此下文中的 <仓库关联命名> 常常写成 origin。若一个本地仓库关联了多个远程仓库，则需要根据实际情况选择 <仓库关联命名>。

* 将远程指定分支拉取到本地**指定**分支上：

  ```bash
  git pull <仓库关联命名> <远程分支名>:<本地分支名>
  ```


* 将远程指定分支拉取到本地**当前**分支上：

  ```bash
  git pull <仓库关联命名> <远程分支名>
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



### git commit

> --amend 通过创建一个新的 commit 来替换当前分支的尖端。

修改 commit message，「amend：修改、修正」

```bash
git commit --amend
```

在弹出的 vim 编辑窗口中，最上方，修改 message 后，:wq 即可。

> 参考网址：[7.6 Git 工具 - 重写历史](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E9%87%8D%E5%86%99%E5%8E%86%E5%8F%B2)



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





### git reset

git reset 命令用于回退版本，可以指定退回某一次提交的版本。

```
git reset [--soft | --mixed | --hard] [HEAD]
```

**--mixed** 为默认，可以不用带该参数，用于重置暂存区的文件与上一次的提交(commit)保持一致，工作区文件内容保持不变。



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

* 本地分支重命名（还没有推送到远程）

  如果对于分支不是当前分支，可以使用下面代码：

  ```bash
  git branch -m <原分支名> <新分支名>
  ```

  如果是当前分支，那么可以使用加上新名字：

  ```bash
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
  ```

* 





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

  

### git 仓库忽略大小写

```bash
git config core.ignorecase true
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




