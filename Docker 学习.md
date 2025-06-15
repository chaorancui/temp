[toc]

# Docker 学习

> [什么是 Docker？看这一篇干货文章就够了！](https://zhuanlan.zhihu.com/p/187505981)

**目的**

为解决重复搭建开发/测试环境的问题，应运而生的技术。

**容器技术 vs 虚拟机**

虚拟机 clone 也可以解决问题，但虚拟机需要同步 clone 操作系统，内存浪费且启动慢。对于**仅部署应用程序**诉求来说，不是最优解。

**什么是容器**

容器一词的英文是 container，其实 container 还有集装箱的意思，集装箱绝对是商业史上了不起的一项发明，大大降低了海洋贸易运输成本。让我们来看看集装箱的好处：

- 集装箱之间相互隔离
- 长期反复使用
- 快速装载和卸载
- 规格标准，在港口和船上都可以摆放

回到软件中的容器，其实容器和集装箱在概念上是很相似的。

与虚拟机通过操作系统实现隔离不同，容器技术**只隔离应用程序的运行时环境但容器之间可以共享同一个操作系统**，这里的运行时环境指的是程序运行依赖的各种库以及配置。

容器更加的**轻量级且占用的资源更少**，与操作系统动辄几 G 的内存占用相比，容器技术只需数 M 空间，因此我们可以在同样规格的硬件上**大量部署容器**，这是虚拟机所不能比拟的，而且不同于操作系统数分钟的启动时间容器几乎瞬时启动，容器技术为**打包服务栈**提供了一种更加高效的方式，So cool。

那么我们该怎么使用容器呢？这就要讲到 docker 了。

==注意，**容器是一种通用技术，docker 只是其中的一种实现**。==

**什么是 docker**

docker 是一个用 Go 语言实现的开源项目，可以让我们方便的创建和使用容器，docker 将程序以及程序所有的依赖都打包到 docker container，这样你的程序可以在任何环境都会有一致的表现，这里程序运行的依赖也就是容器就好比集装箱，容器所处的操作系统环境就好比货船或港口，**程序的表现只和集装箱有关系(容器)，和集装箱放在哪个货船或者哪个港口(操作系统)没有关系**。

因此我们可以看到 docker 可以屏蔽环境差异，也就是说，只要你的程序打包到了 docker 中，那么无论运行在什么环境下程序的行为都是一致的，程序员再也无法施展表演才华了，**不会再有“在我的环境上可以运行”**，真正实现“build once, run everywhere”。

此外 docker 的另一个好处就是**快速部署**，这是当前互联网公司最常见的一个应用场景，一个原因在于容器启动速度非常快，另一个原因在于只要确保一个容器中的程序正确运行，那么你就能确信无论在生产环境部署多少都能正确运行。

**如何使用 docker**

docker 中有这样几个概念：

- dockerfile
- image
- container

实际上你可以简单的把 image 理解为可执行程序，container 就是运行起来的进程。

那么写程序需要源代码，那么“写”image 就需要 dockerfile，dockerfile 就是 image 的源代码，docker 就是"编译器"。

因此我们只需要在 dockerfile 中指定需要哪些程序、依赖什么样的配置，之后把 dockerfile 交给“编译器”docker 进行“编译”，也就是 docker build 命令，生成的可执行程序就是 image，之后就可以运行这个 image 了，这就是 docker run 命令，image 运行起来后就是 docker container。

具体的使用方法就不再这里赘述了，大家可以参考 docker 的官方文档，那里有详细的讲解。

**docker 是如何工作的**

实际上 docker 使用了常见的 CS 架构，也就是 client-server 模式，docker client 负责处理用户输入的各种命令，比如`docker build`、`docker run`，真正工作的其实是 server，也就是 docker daemon，值得注意的是，docker client 和 docker daemon 可以运行在同一台机器上。

接下来我们用几个命令来讲解一下 docker 的工作流程：

**1，docker build**

当我们写完 dockerfile 交给 docker“编译”时使用这个命令，那么 client 在接收到请求后转发给 docker daemon，接着 docker daemon 根据 dockerfile 创建出“可执行程序”image。

![img](https://pic3.zhimg.com/80/v2-f16577a98471b4c4b5b1af1036882caa_720w.webp)

**2，docker run**

有了“可执行程序”image 后就可以运行程序了，接下来使用命令 docker run，docker daemon 接收到该命令后找到具体的 image，然后加载到内存开始执行，image 执行起来就是所谓的 container。

![img](https://pic4.zhimg.com/80/v2-672b29e2d53d2ab044269b026c6bc473_720w.webp)

**3，docker pull**

其实 docker build 和 docker run 是两个最核心的命令，会用这两个命令基本上 docker 就可以用起来了，剩下的就是一些补充。

那么 docker pull 是什么意思呢？

我们之前说过，docker 中 image 的概念就类似于“可执行程序”，我们可以从哪里下载到别人写好的应用程序呢？很简单，那就是 APP Store，即应用商店。与之类似，既然 image 也是一种“可执行程序”，那么有没有"Docker Image Store"呢？答案是肯定的，这就是 Docker Hub，docker 官方的“应用商店”，你可以在这里下载到别人编写好的 image，这样你就不用自己编写 dockerfile 了。

docker registry 可以用来存放各种 image，公共的可以供任何人下载 image 的仓库就是 docker Hub。那么该怎么从 Docker Hub 中下载 image 呢，就是这里的 docker pull 命令了。

因此，这个命令的实现也很简单，那就是用户通过 docker client 发送命令，docker daemon 接收到命令后向 docker registry 发送 image 下载请求，下载后存放在本地，这样我们就可以使用 image 了。

**docker 的底层实现**

docker 基于 Linux 内核提供这样几项功能实现的：

- **NameSpace**
  我们知道 Linux 中的 PID、IPC、网络等资源是全局的，而 NameSpace 机制是一种资源隔离方案，在该机制下这些资源就不再是全局的了，而是属于某个特定的 NameSpace，各个 NameSpace 下的资源互不干扰，这就使得每个 NameSpace 看上去就像一个独立的操作系统一样，但是只有 NameSpace 是不够。
- **Control groups**
  虽然有了 NameSpace 技术可以实现资源隔离，但进程还是可以不受控的访问系统资源，比如 CPU、内存、磁盘、网络等，为了控制容器中进程对资源的访问，Docker 采用 control groups 技术(也就是 cgroup)，有了 cgroup 就可以控制容器中进程对系统资源的消耗了，比如你可以限制某个容器使用内存的上限、可以在哪些 CPU 上运行等等。

有了这两项技术，容器看起来就真的像是独立的操作系统了。

> 说明：
>
> “真正实现“build once, run everywhere””。这句话是错误的，实际上程序员依然有演戏的空间。因为容器只打包了用户空间的系统调用，执行系统调用的地方依然是宿主的 kernel，所以当你 docker run centos:6 bash 执行这句话的时候，在新的内核上可能会发生段错误，而老的宿主机却不会。**真正要做到 BORE，还是必使用同样的内核**，那样的话，和使用虚拟机就没差别了。总之不可能做到开发，测试，运维只要用同一个镜像就能表现完全一致，只要提供系统调用的内核版本不同，嗯，行为就绝对不能保证一致。

# **Docker 快速入门**

> [**Docker 快速入门**](https://docker.easydoc.net/doc/81170005/cCewZWoN/lTKfePfP)
>
> [Docker — 从入门到实践](https://yeasy.gitbook.io/docker_practice)
> [Docker — 从入门到实践](http://docker.baoshu.red/introduction/what.html) ---- 跟上面不一样

Docker 是一个应用打包、分发、部署的工具
你也可以把它理解为一个轻量的虚拟机，它只虚拟你软件需要的运行环境，多余的一点都不要，
而普通虚拟机则是一个完整而庞大的系统，包含各种不管你要不要的软件。

### 打包、分发、部署

**打包**：就是把你软件运行所需的**依赖**、**第三方库**、**软件**打包到一起，变成一个安装包
**分发**：你可以把你打包好的“安装包”上传到一个镜像仓库，其他人可以非常方便的获取和安装
**部署**：拿着“安装包”就可以一个命令运行起来你的应用，自动模拟出一摸一样的运行环境，不管是在 Windows/Mac/Linux。

### Docker 通常用来做什么

- 应用分发、部署，方便传播给他人安装。特别是开源软件和提供私有部署的应用
- 快速安装测试/学习软件，用完就丢（类似小程序），不把时间浪费在安装软件上。例如 Redis / MongoDB / ElasticSearch / ELK
- 多个版本软件共存，不污染系统，例如 Python2、Python3，Redis4.0，Redis5.0
- Windows 上体验/学习各种 Linux 系统

### **Docker** 包括三个基本概念：镜像、容器、仓库

- 镜像（`Image`）：Docker 镜像是一个特殊的文件系统，除了提供[容器](https://cloud.tencent.com/product/tke?from_column=20065&from=20065)运行时所需的程序、库、资源、配置等文件外，还包含了一些为运行时准备的一些配置参数（如匿名卷、环境变量、用户等）。镜像不包含任何动态数据，其内容在构建之后也不会被改变。
- 容器（`Container`）：镜像（`Image`）和容器（`Container`）的关系，就像是面向对象程序设计中的 `类` 和 `实例` 一样，镜像是静态的定义，容器是镜像运行时的实体。容器可以被创建、启动、停止、删除、暂停等。
- 仓库（`Repository`）：仓库（`Repository`）类似 Git 的远程仓库，集中存放镜像文件。

三者关系可以用下图表示：

![Docker](https://ask.qcloudimg.com/http-save/yehe-7565276/joa65awgh4.png)

# 震惊 😱 超详细的 Docker 常用命令

> [震惊 😱 超详细的 Docker 常用命令](https://juejin.cn/post/7245275769219203132)
>
> [一张脑图整理 Docker 常用命令](https://cloud.tencent.com/developer/article/1772136)

![Docker](https://ask.qcloudimg.com/http-save/yehe-7565276/6lldlbgfhn.png)

> tip:
>
> 下面的命令，也不是很全，需要更全命令的时候再另行寻找。

## 服务相关命令

```shell
# 启动 docker 服务
systemctl start docker

# 停止 docker 服务
systemctl stop docker

# 重启 docker 服务
systemctl restart docker

# 查看 docker 服务状态
systemctl status docker

# 设置开机启动 docker 服务
systemctl enable docker
```

## 镜像相关命令

目前 Docker 官方维护了一个公共仓库 [Docker Hub](https://hub.docker.com/)，其中已经包括了数量超过 [2,650,000](https://hub.docker.com/search/?type=image) 的镜像。大部分需求都可以通过在 Docker Hub 中直接下载镜像来实现。

可以在 https://hub.docker.com 免费注册一个 Docker 账号。

可以通过执行 `docker login` 命令交互式的输入用户名及密码来完成在命令行界面登录 Docker Hub。

可以通过 `docker logout` 退出登录。

### **搜索镜像**

```shell
# 从Docker Hub查找镜像
docker search [OPTIONS] TERM

--automated :只列出 automated build类型的镜像；
--no-trunc :显示完整的镜像描述；
-f <过滤条件>:列出收藏数不小于指定值的镜像。

# 例：
docker search -f stars=10 java # 从 Docker Hub 查找所有镜像名包含 java，并且收藏数大于 10 的镜像
```

### **拉取镜像**

```shell
# 从镜像仓库中拉取或者更新指定镜像
docker pull [OPTIONS] NAME[:TAG|@DIGEST]

-a :拉取所有 tagged 镜像
--disable-content-trust :忽略镜像的校验,默认开启

# 例：
docker pull java # 从Docker Hub下载java最新版镜像
```

> tip:
>
> ```shell
> # 指定版本号, 格式如下
> docker pull 镜像名:版本号tag
> ```
>
> 不加 `tag` 的情况下, 默认拉取的就是 `latest`(最新版本)，如果不知道 `tag` 有哪些, 可以去 [`Dockerhub`](https://link.juejin.cn/?target=https%3A%2F%2Fhub.docker.com) 查看

### **使用`Dockerfile`构建镜像**

```shell
# docker build 命令用于使用 Dockerfile 创建镜像

docker build [OPTIONS] PATH | URL | -

--build-arg=[] :设置镜像创建时的变量；
--cpu-shares :设置 cpu 使用权重；
--cpu-period :限制 CPU CFS周期；
--cpu-quota :限制 CPU CFS配额；
--cpuset-cpus :指定使用的CPU id；
--cpuset-mems :指定使用的内存 id；
--disable-content-trust :忽略校验，默认开启；
-f :指定要使用的Dockerfile路径；
--force-rm :设置镜像过程中删除中间容器；
--isolation :使用容器隔离技术；
--label=[] :设置镜像使用的元数据；
-m :设置内存最大值；
--memory-swap :设置Swap的最大值为内存+swap，"-1"表示不限swap；
--no-cache :创建镜像的过程不使用缓存；
--pull :尝试去更新镜像的新版本；
--quiet, -q :安静模式，成功后只输出镜像 ID；
--rm :设置镜像成功后删除中间容器；
--shm-size :设置/dev/shm的大小，默认值是64M；
--ulimit :Ulimit配置。
--squash :将 Dockerfile 中所有的操作压缩为一层。
--tag, -t: 镜像的名字及标签，通常 name:tag 或者 name 格式；可以在一次构建中为一个镜像设置多个标签。
--network: 默认 default。在构建期间设置RUN指令的网络模式

# 例：
# 使用当前目录的 Dockerfile 创建镜像，标签为 runoob/ubuntu:v1。注意最后边的点 `.` 表示当前目录, 别丢了
docker build -t runoob/ubuntu:v1 .

# 使用URL github.com/creack/docker-firefox 的 Dockerfile 创建镜像。
docker build github.com/creack/docker-firefox

# 也可以通过 -f Dockerfile 文件的位置：
docker build -f /path/to/a/Dockerfile .
```

`Docker` `build` 命令可以使用 `Dockerfile` 来构建镜像。默认情况下，`Dockerfile` 文件位于构建上下文的根目录下，因此 `docker build` 命令会自动读取上下文根路径下名为 `Dockerfile` 的文件。如果 `Dockerfile` 文件不在根目录下，可以使用 `-f` 选项来指定 `Dockerfile` 文件的路径。例如，以下命令将使用 `/path/to/Dockerfile` 文件构建镜像：

```shell
docker build -f /path/to/Dockerfile -t image_name:tag .
```

其中，

- `.` 表示当前目录.
- `-f` , `--file` Name of the Dockerfile (Default is PATH/Dockerfile)
- `-t` , `--tag` Name and optionally a tag in the name:tag format

[docker build [OPTIONS\]文档](https://link.juejin.cn/?target=https%3A%2F%2Fdocs.docker.com%2Fengine%2Freference%2Fcommandline%2Fbuild%2F%23options)

`Dockerfile` 简单列举几个指令:

- `FROM` : 指定基础镜像
- `WORKDIR` : 指定工作目录
- `COPY` : 将文件或者目录从构建上下文复制到容器中(推荐)
- `ADD` : 将文件或者目录从构建上下文复制到容器中,并且会将压缩文件解压缩,支持 `URL`
- `RUN` : 在容器中执行命令
- `CMD` : 容器启动时执行的命令
- `EXPOSE` : 指定要监听的端口以实现与外部通信

举个例子:

```Dockerfile
# nodejs server Dockerfile

# FROM node
# or
FROM node:16

WORKDIR /nodeApp

# COPY <宿主机目录或文件路径> <容器内目录或文件路径>
COPY ./package.json .
# ADD <宿主机目录或文件路径> <容器内目录或文件路径>
# ADD ./package.json .

# shell格式：就像在命令行中输入的Shell脚本命令一样。
RUN npm install

COPY ./src ./server

EXPOSE 8000

CMD ["node", "./server/index.js"]
```

详细了解请查看这篇[纯干货！Docker Dockerfile 指令大全](https://link.juejin.cn/?target=https%3A%2F%2Fzhuanlan.zhihu.com%2Fp%2F419175543)

### **docker image 命令**

```shell
docker image COMMAND

Commands:
  build       Build an image from a Dockerfile
  history     Show the history of an image
  import      Import the contents from a tarball to create a filesystem image
  inspect     Display detailed information on one or more images
  load        Load an image from a tar archive or STDIN
  ls          List images
  prune       Remove unused images
  pull        Pull an image or a repository from a registry
  push        Push an image or a repository to a registry
  rm          Remove one or more images
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
```

### **查看本地镜像**

```shell
# 列出本地镜像
docker images [OPTIONS] [REPOSITORY[:TAG]]

-a :列出本地所有的镜像（含中间映像层，默认情况下，过滤掉中间映像层）；
--digests :显示镜像的摘要信息；
-f :显示满足条件的镜像；
--format :指定返回值的模板文件；
--no-trunc :显示完整的镜像信息；
-q :只显示镜像ID。

# 例：
docker images # 查看本地镜像列表
docker images ubuntu # 列出本地镜像中REPOSITORY为ubuntu的镜像列表
```

### **删除本地镜像**

```shell
# 删除本地一个或多个镜像
docker rmi [OPTIONS] IMAGE [IMAGE...]

-f :强制删除；
--no-prune :不移除该镜像的过程镜像，默认移除；

# 例：
docker rmi mysql:5.7 # 使用镜像名:版本号tag删除
docker rmi 2be84dd575ee # 使用镜像ID删除
docker rmi `docker images -f "dangling=true" -q` # 删除tag为none的镜像
docker rmi `docker images -q` # 全部删除本地镜像
```

> tip:
> 为了准确删除你的目标镜像, 建议删除有多个版本存在的镜像时, 使用镜像名:版本号, 如果二者镜像 `ID` 不同也可以使用镜像 `ID` 进行删除, 防止误删
>
> 不能删除正在运行的容器使用着的镜像(假如是`nginx`镜像), 如果确实想要删除`nginx`, 需要先停止所有使用这个镜像的容器, 并且将这些容器删除, 才可以删除`nginx`镜像。

### **导出镜像**

```bash
# 将指定镜像保存成 tar 归档文件
docker save [OPTIONS] IMAGE [IMAGE...]

-o :输出到的文件。

# 例：
docker save -o my_ubuntu_v3.tar runoob/ubuntu:v3
```

### **导入镜像**

```shell
# 导入使用 docker save 命令导出的镜像
docker load [OPTIONS]

--input , -i : 指定导入的文件，代替 STDIN。
--quiet , -q : 精简输出信息。

# 例：
docker load -i fedora.tar
```

> tip:
> 如果用镜像 `ID` 导出的镜像在导入之后是没有名字和`tag`的, 这种情况我们可以使用 `docker tag` 给镜像改名字
>
> ```shell
> docker tag image_id new_image_name:tag
> ```

## 容器相关命令

### **创建容器**

```shell
# 创建一个新的容器并运行一个命令
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

-a stdin: 指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR 三项；
-d: 后台运行容器，并返回容器ID；
-i: 以交互模式运行容器，通常与 -t 同时使用；
-P: 随机端口映射，容器内部端口随机映射到主机的端口
-p: 指定端口映射，格式为：主机(宿主)端口:容器端口
-t: 为容器重新分配一个伪输入终端，通常与 -i 同时使用；
--name="nginx-lb": 为容器指定一个名称；
--dns 8.8.8.8: 指定容器使用的DNS服务器，默认和宿主一致；
--dns-search example.com: 指定容器DNS搜索域名，默认和宿主一致；
-h "mars": 指定容器的hostname；
-e username="ritchie": 设置环境变量；
--env-file=[]: 从指定文件读入环境变量；
--cpuset="0-2" or --cpuset="0,1,2": 绑定容器到指定CPU运行；
-m :设置容器使用内存最大值；
--net="bridge": 指定容器的网络连接类型，支持 bridge/host/none/container: 四种类型；
--link=[]: 添加链接到另一个容器；
--expose=[]: 开放一个端口或一组端口；
--volume , -v: 绑定一个卷，格式为：主机(宿主)卷:容器卷
--user：指定用户登录docker，默认的登陆用户为 root，--user $(id -u):$(id -g)可以用宿主机中当前uid和gid的用户登录docker
--privileged：默认情况下容器中的root用户只是host主机的一个普通用户，但如果docker run --privileged=true 就真正的给这个普通用户赋予了和host主机root用户的特权。
--network：在Docker中，默认情况下容器与容器、容器与外部宿主机的网络是隔离开来的。当你安装Docker的时候，docker会创建一个桥接器docker0，通过它才让容器与容器之间、与宿主机之间通信。Docker安装的时候默认会创建三个不同的网络。你可以通过docker network ls命令查看这些网络。网络模式为none的，即不为Docker Container创建任何的网络环境。如果你在创建容器的时候使用--network=host选项，那么容器会使用宿主机的网络，容器与宿主机的网络并没有隔离。桥接网络--network=bridge是默认的网络类型。

Dcoker容器在使用的过程中，默认的docker run时都是以普通方式启动的，有的时候是需要使用在容器中使用iptables进行启动的，这时候就需要开启权限，只需要在docker run时增加参数。
--cap-add list                   Add Linux capabilities # 添加某些权限
--cap-drop list                  Drop Linux capabilities # 关闭权限
--privileged                     Give extended privileges to this container # default false
privileged，权限全开，不利于宿主机安全。
cap-add/cap-drop，细粒度权限设置，需要什么开什么

--restart：可以设置容器的重启策略，以决定在容器退出时Docker守护进程是否重启刚刚退出的容器。
Docker容器的重启策略如下：
- no，默认策略，在容器退出时不重启容器
- on-failure，在容器非正常退出时（退出状态非0），才会重启容器
- on-failure:3，在容器非正常退出时重启容器，最多重启3次
- always，在容器退出时总是重启容器
- unless-stopped，在容器退出时总是重启容器，但是不考虑在Docker守护进程启动时就已经停止了的容器
在docker ps查看容器时，对于使用了--restart选项的容器，其可能的状态只有Up或Restarting两种状态。


# 例：
# 使用docker镜像nginx:latest以后台模式启动一个容器,并将容器命名为mynginx。
docker run --name mynginx -d nginx:latest

# 使用镜像nginx:latest以后台模式启动一个容器,并将容器的80端口映射到主机随机端口。
docker run -P -d nginx:latest

# 使用镜像 nginx:latest，以后台模式启动一个容器,将容器的 80 端口映射到主机的 80 端口,主机的目录 /data 映射到容器的 /data。
docker run -p 80:80 -v /data:/data -d nginx:latest

# 绑定容器的 8080 端口，并将其映射到本地主机 127.0.0.1 的 80 端口上。
docker run -p 127.0.0.1:80:8080/tcp ubuntu bash

# 使用镜像nginx:latest以交互模式启动一个容器,在容器内执行/bin/bash命令
docker run -it nginx:latest /bin/bash
```

> tip:
> 使用交互模式运行容器时, 会直接进入容器内部, 退出交互模式后, 该容器自动停止运行
>
> **注：** 容器是否会长久运行，是和 `docker run` 指定的命令有关，和 `-d` 参数无关。----啥意思?

> 当利用 `docker run` 来创建容器时，Docker 在后台运行的标准操作包括：
>
> - 检查本地是否存在指定的镜像，不存在就从 [registry](https://yeasy.gitbook.io/docker_practice/repository) 下载
> - 利用镜像创建并启动一个容器
> - 分配一个文件系统，并在只读的镜像层外面挂载一层可读写层
> - 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去
> - 从地址池配置一个 ip 地址给容器
> - 执行用户指定的应用程序
> - 执行完毕后容器被终止

> [Docker run 命令参数及使用](https://www.jianshu.com/p/ea4a00c6c21c)
>
> [Docker Network 入门用法](https://loocode.com/post/docker-network-ru-men-yong-fa)
>
> [docker 容器的权限设置](https://blog.csdn.net/myli92/article/details/127479212)
>
> [Docker 容器的重启策略及 docker run 的--restart 选项详解](https://blog.csdn.net/taiyangdao/article/details/73076019)
>
> [Docker Volume - 目录挂载以及文件共享](https://kebingzao.com/2019/02/25/docker-volume/)

```shell
# `host` 模式 `-p` 选项不需要，因为 `host` 模式下容器直接使用宿主机的网络栈，端口是共享的。
docker run -d \
    -it \
    --privileged \
    -h <hostname> \
    --restart always \
    --network host \
    --name ascendc_c00619335 \
    -v /data/c00619335:/data \
    IMAGE \
    /bin/bash

# `bridge` 模式可以使用 `-p` 选项指定端口
docker run -d \
    -it \
    --privileged \
    -h <hostname> \
    --restart always \
    --network bridge \
    -p <port_h:port_c> \
    --name ascendc_c00619335 \
    -v /data/c00619335:/data \
    IMAGE \
    /bin/bash

docker exec -it ascendc_c00619335 bash
```

### **删除容器**

docker rm 命令用于删除一个或多个已经停止的容器。
docker rm 命令不会删除正在运行的容器，如果你需要先停止容器，可以使用 docker stop 命令。

```shell
# docker start : 删除一个或多个已经停止的容器

docker rm [OPTIONS] CONTAINER [CONTAINER...]

OPTIONS说明：
-f, --force: 强制删除正在运行的容器（使用 SIGKILL 信号）。
-l, --link: 删除指定的连接，而不是容器本身。
-v, --volumes: 删除容器挂载的卷。

# 示例
docker rm my_container # 用容器名删除
docker rm container_id # 用容器ID删除
docker rm `docker ps -aq` # 删除多个未运行的容器, 运行中的无法删除
```

### **更新容器配置**

```shell
# 更新容器，动态更新容器的资源限制、重启策略等配置
docker update [OPTIONS] CONTAINER [CONTAINER...]

--blkio-weight		块 IO（相对权重），介于 10 到 1000 之间，或 0 禁用（默认 0）
--cpu-period		限制CPU CFS（完全公平调度程序）周期
--cpu-quota		限制CPU CFS（完全公平调度程序）配额
--cpu-rt-period		限制CPU实时周期（以微秒为单位）
--cpu-rt-runtime		将CPU实时运行时间限制在微秒级
--cpu-shares,-c		CPU 份额（相对权重）
--cpus		CPU数量
--cpuset-cpus		允许执行的 CPU (0-3, 0,1)
--cpuset-mems		允许执行的 MEM (0-3, 0,1)
--memory,-m		内存限制
--memory-reservation		内存软限制
--memory-swap		交换限制等于内存加交换：-1 启用无限制交换
--pids-limit		API 1.40+ 调整容器 pid 限制（设置 -1 表示无限制）
--restart		容器退出时应用的重新启动策略

# 例
# 更新容器重启策略
docker update --restart=on-failure:3 <container_name/id>
```

> [docker update 命令\_docker update -p-CSDN 博客](https://blog.csdn.net/agonie201218/article/details/132420832)

### **查看容器列表**

```shell
# 列出容器
docker ps [OPTIONS]

-a :显示所有的容器，包括未运行的。
-f :根据条件过滤显示的内容。
--format :指定返回值的模板文件。
-l :显示最近创建的容器。
-n :列出最近创建的n个容器。
--no-trunc :不截断输出。
-q :静默模式，只显示容器编号。
-s :显示总的文件大小

# 例：
docker ps # 查看正在运行的容器列表
docker ps -l # 查看最近一次创建的容器
docker ps -a # 查看全部容器(包括已经停止的容器)
```

> tip:
>
> STATUS: 容器状态。 状态有 7 种：
>
> created（已创建）
>
> restarting（重启中）
>
> running（运行中）
>
> removing（迁移中）
>
> paused（暂停）
>
> exited（停止）
>
> dead（死亡）
>
> 这些状态中，最重要和常见的是除了 restarting（重启中）和 removing（迁移中）之外的五个状态，下面基本上网络上大部分的容器生命周期图都只包含五个状态：created（已创建），running（运行中），paused（暂停），exited（停止），dead（死亡）。

### **启动/停止/重启运行的容器**

```shell
# docker start :启动一个或多个已经被停止的容器
# docker stop :停止一个运行中的容器
# docker restart :重启容器

docker start [OPTIONS] CONTAINER [CONTAINER...]
docker stop [OPTIONS] CONTAINER [CONTAINER...]
docker restart [OPTIONS] CONTAINER [CONTAINER...]

# 例：
docker start my_container # 用容器名启动
docker start container_id # 用容器ID启动
docker start `docker ps -aq` # 用容器ID启动多个已停止的容器

docker stop my_container # 用容器名停止
docker stop container_id # 用容器ID停止
docker stop `docker ps -q` # 使用容器ID停止多个正在运行的容器

docker rm my_container # 用容器名删除
docker rm container_id # 用容器ID删除
docker rm `docker ps -aq` # 删除多个未运行的容器, 运行中的无法删除
```

### **进入容器执行命令**(正在运行的容器才可以进入)

```shell
# 在运行的容器中执行命令
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]

-d :分离模式: 在后台运行
-i :即使没有附加也保持STDIN 打开
-t :分配一个伪终端

# 例：
# 在容器 mynginx 中以交互模式执行容器内 /root/runoob.sh 脚本
docker exec -it mynginx /bin/sh /root/runoob.sh

# 在容器 my_container 中开启一个交互模式的终端
docker exec -it my_container /bin/bash # 使用容器名
docker exec -it container_id /bin/bash # 使用容器ID

# 登录 docker 时切换路径
docker exec -it <container_name_or_id> bash -c "cd /path/to/directory && exec bash"
```

### **退出容器**

```shell
# 退出container
exit
# 或者按键：
<Ctrl + C>
```

### **查看容器信息**

```bash
# 获取容器/镜像的元数据
docker inspect [OPTIONS] NAME|ID [NAME|ID...]

-f :指定返回值的模板文件。
-s :显示总的文件大小。
--type :为指定类型返回JSON

# 例：
docker inspect my_container:version_tag # 容器名
docker inspect container_id # 容器ID
```

内容很多

### **容器与宿主机之间的数据拷贝**

```shell
# 用于容器与主机之间的数据拷贝。
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH

-L :保持源目标中的链接

# 例：
# 1、将容器中目录或文件拷贝到宿主机
# 将容器中 /app/html 目录拷贝到宿主机 /mnt/ 目录中
docker cp container_id:/app/html /mnt/

# 2、将宿主机目录或文件拷贝到容器中
# 将宿主机 /mnt/dist 目录拷贝到容器的 /app 目录中
docker cp /mnt/dist container_id:/app/

# 3、将宿主机/mnt/dist目录拷贝到容器中, 并重命名为html
# 将宿主机 /mnt/dist 目录拷贝到容器的 /app/ 中重命名为 html
docker cp /mnt/dist container_id:/app/html
# 将宿主机 /mnt/dist/index1.html 文件拷贝到容器的 /app/html/ 中重命名为 index.html
docker cp /mnt/dist/index1.html container_id:/app/html/index.html
```

### 网络模式更改

要将 Docker 容器的网络模式从 `bridge` 模式改为 `host` 模式，你不能直接修改正在运行容器的网络模式。你需要停止并删除当前容器，然后使用 `--network host` 重新启动它。以下是具体的步骤：

1. **查看正在运行的容器**

   首先，确认当前容器的名称或 ID。可以使用以下命令查看正在运行的容器：

   ```shell
   docker ps
   ```

   记下需要修改网络模式的容器的名称或 ID。

2. **停止并删除容器**

   要修改网络模式，首先需要停止并删除容器。使用以下命令停止容器：

   ```shell
   # 停止容器：
   docker stop <container_name_or_id>

   # 删除容器：
   docker rm <container_name_or_id>
   ```

3. **使用 `host` 网络模式重新运行容器**

   现在你可以使用 `--network host` 选项重新启动容器。

   如果你之前使用了 `docker run` 创建容器，可以类似地运行 `docker run`，只是这次使用 `--network host` 选项。

   ```shell
   # 假设原始命令是这样：
   docker run -d -p 80:80 --name my_container <image_name>

   # 修改为使用 `host` 网络模式的命令：
   docker run -d --network host --name my_container <image_name>
   ```

   在这个命令中，`-p` 选项已不再需要，因为 `host` 模式下容器直接使用宿主机的网络栈，端口是共享的。

4. **验证网络模式**

   容器启动后，你可以使用 `docker inspect` 验证容器的网络模式：

   ```shell
   docker inspect <container_name_or_id> | grep -i "networkmode"
   ```

   这应该显示 `host` 作为网络模式。

## 镜像相关命令补充

`docker commit` 的语法格式为：

```shell
docker commit [选项] <容器ID或容器名> [<仓库名>[:<标签>]]

我们可以用下面的命令将容器保存为镜像：
```

要知道，当我们运行一个容器的时候（如果不使用卷的话），我们做的任何文件修改都会被记录于容器存储层里。而 Docker 提供了一个 `docker commit` 命令，可以将容器的存储层保存下来成为镜像。换句话说，就是在原有镜像的基础上，再叠加上容器的存储层，并构成新的镜像。以后我们运行这个新镜像的时候，就会拥有原有容器最后的文件变化。

> 慎用 `docker commit`
>
> 使用 `docker commit` 命令虽然可以比较直观的帮助理解镜像分层存储的概念，但是实际环境中并不会这样使用。

`docker container ls -a` 命令查看容器的状态。

`docker container stop` 命令来终止一个运行中的容器。

`docker container start` 命令来重新启动处于终止状态的容器。

`docker container restart` 命令会将一个运行态的容器终止，然后再重新启动它。

## 数据管理

在容器中管理数据主要有两种方式：

- 数据卷（Volumes）
- 挂载主机目录 (Bind mounts)

![img](https://yeasy.gitbook.io/~gitbook/image?url=https%3A%2F%2F1881212762-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F-M5xTVjmK7ax94c8ZQcm%252Fuploads%252Fgit-blob-5950036bba1c30c0b1ab52a73a94b59bbdd5f57c%252Ftypes-of-mounts.png%3Falt%3Dmedia&width=768&dpr=4&quality=100&sign=fb819ed99aeae8422fcffe6597d87acda98625f3220b4187d11feb58447ab739)

`数据卷` 是一个可供一个或多个容器使用的特殊目录，它绕过 UnionFS，可以提供很多有用的特性：

- `数据卷` 可以在容器之间共享和重用
- 对 `数据卷` 的修改会立马生效
- 对 `数据卷` 的更新，不会影响镜像
- `数据卷` 默认会一直存在，即使容器被删除

> 注意：`数据卷` 的使用，类似于 Linux 下对目录或文件进行 mount，镜像中的被指定为挂载点的目录中的文件会复制到数据卷中（仅数据卷为空时会复制）。

```shell
docker volume --help

Commands:
  create      创建一个数据卷
  inspect     打印一个或多个数据卷的详细信息
  ls          列出所有数据卷
  prune       删除所有未使用的数据卷
  rm          删除一个或多个数据卷

# 例：
# 创建一个数据卷
docker volume create my-vol

# 查看所有的 数据卷
docker volume ls

# 在宿主机里查看指定 数据卷 的信息
docker volume inspect my-vol

# 删除数据卷
docker volume rm my-vol

# 挂载数据卷的容器：
# 在用 docker run 命令的时候，使用 --mount 标记来将 数据卷 挂载到容器里。
# 下面创建一个名为 web 的容器，并加载一个 数据卷 到容器的 /usr/share/nginx/html 目录
docker run -d -P \
    --name web \
    # -v my-vol:/usr/share/nginx/html \
    --mount source=my-vol,target=/usr/share/nginx/html \
    nginx:alpine

# 挂载一个主机目录作为数据卷
# 使用 --mount，加载主机的 /src/webapp 目录到容器的 /usr/share/nginx/html目录
docker run -d -P \
    --name web \
    # -v /src/webapp:/usr/share/nginx/html \
    --mount type=bind,source=/src/webapp,target=/usr/share/nginx/html \
    nginx:alpine
```

> tip:
>
> ```shell
> # 在宿主机里查看指定 数据卷 的信息
> docker volume inspect my-vol
>
> [
>     {
>         "Driver": "local",
>         "Labels": {},
>         "Mountpoint": "/var/lib/docker/volumes/my-vol/_data",
>         "Name": "my-vol",
>         "Options": {},
>         "Scope": "local"
>     }
> ]
> ```
>
> 注：每创建一个 volume，docker 会在 `/var/lib/docker/volumes/` 下创建一个子目录，默认情况下目录名是一串 UUID。如果指定了名称，则目录名是 volume 名称（例如上面的 my-vol）。volume 里的数据都存储在这个子目录的`_data`目录下。==**这个路径可以修改，遇到过不在 /var/lib/docker/volumes/ 下面的。**==
>
> **MountPoint** 宿主机上的路径为 `/var/lib/docker/volumes/wmy-vol/_data`，数据卷的名称为 my-vol。

> tip:
>
> ```shell
> # 删除数据卷
> docker volume rm my-vol
> ```
>
> `数据卷` 是被设计用来持久化数据的，它的生命周期独立于容器，Docker 不会在容器被删除后自动删除 `数据卷`，并且也不存在垃圾回收这样的机制来处理没有任何容器引用的 `数据卷`。
>
> 如果需要在删除容器的同时移除数据卷。可以在删除容器的时候使用 `docker rm -v` 这个命令。

> tip:
>
> ```shell
> # 在用 docker run 命令的时候，使用 --mount 标记来将 数据卷 挂载到容器里。
> # 下面创建一个名为 web 的容器，并加载一个 数据卷 到容器的 /usr/share/nginx/html 目录
> docker run -d -P \
>     --name web \
>     # -v my-vol:/usr/share/nginx/html \
>     --mount source=my-vol,target=/usr/share/nginx/html \
>     nginx:alpine
>
> # 挂载一个主机目录作为数据卷
> # 使用 --mount，加载主机的 /src/webapp 目录到容器的 /usr/share/nginx/html目录
> docker run -d -P \
>     --name web \
>     # -v /src/webapp:/usr/share/nginx/html \
>     --mount type=bind,source=/src/webapp,target=/usr/share/nginx/html \
>     nginx:alpine
> ```
>
> 挂载数据卷相关总结：
>
> > [Docker 基础知识 - 使用绑定挂载(bind mounts)管理应用程序数据](https://ittranslator.cn/backend/docker/2020/07/13/docker-storage-bind-mounts.html)
> >
> > [Docker 数据管理-volume/bind mount/tmpfs mount](https://blog.zhimma.com/2019/04/10/Docker%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86-volume-bind-mount-tmpfs-mount/)
>
> 1. 选择 `-v` 或者 `--mount` 标记
>
>    最初，`-v` 或 `--volume` 标记用于独立容器，`--mount` 标记用于集群服务。但是，从 Docker 17.06 开始，您也可以将 `--mount` 用于独立容器。
>
>    通常，`--mount` 标记表达更加明确和冗长。最大的区别是 `-v` 语法将所有选项组合在一个字段中，而 `--mount` 语法将选项分离。下面是每个标记的语法比较。
>
>    > 提示：新用户推荐使用 `--mount` 语法，有经验的用户可能更熟悉 `-v` or `--volume` 语法，但是更鼓励使用 `--mount` 语法，因为研究表明它更易于使用。
>
>    - `-v` 或 `--volume` : 由三个字段组成，以冒号(:)分隔。如`<卷名>:<容器路径>:<选项列表>`。字段必须按照正确的顺序排列，且每个字段的含义不够直观明显。
>      - 对于绑定挂载（bind mounts）, 第一个字段是主机上文件或目录的路径。
>      - 第二个字段是容器中文件或目录挂载的路径。
>      - 第三个字段是可选的，是一个逗号分隔的选项列表，比如 `ro`、`consistent`、 `delegated`、 `cached`、 `z` 和 `Z`。这些选项会在本文下面讨论。
>    - `--mount` ：由多个键-值对组成，以逗号分隔，每个键-值对由一个 `<key>=<value>` 元组组成。`--mount` 语法比 `-v` 或 `--volume` 更冗长，但是键的顺序并不重要，标记的值也更容易理解。
>      - 挂载的类型（`type`），可以是 `bind`、`volume` 或者 `tmpfs`。本主题讨论绑定挂载（bind mounts），因此类型（`type`）始终为绑定挂载（`bind`）。
>      - 挂载的源（`source`），对于绑定挂载，这是 Docker 守护进程主机上的文件或目录的路径。可以用 `source` 或者 `src` 来指定。
>      - 目标（`destination`），将容器中文件或目录挂载的路径作为其值。可以用 `destination`、`dst` 或者 `target` 来指定。
>      - `readonly` 选项（如果存在），则会将绑定挂载以[只读形式挂载到容器](https://ittranslator.cn/backend/docker/2020/07/13/docker-storage-bind-mounts.html#use-a-read-only-bind-mount)中。
>      - `bind-propagation` 选项（如果存在），则更改[绑定传播](https://ittranslator.cn/backend/docker/2020/07/13/docker-storage-bind-mounts.html#configure-bind-propagation)。 可能的值是 `rprivate`、 `private`、 `rshared`、 `shared`、 `rslave` 或 `slave` 之一。
>      - [`consistency`](https://ittranslator.cn/backend/docker/2020/07/13/docker-storage-bind-mounts.html#configure-mount-consistency-for-macos) 选项（如果存在）， 可能的值是 `consistent`、 `delegated` 或 `cached` 之一。 这个设置只适用于 Docker Desktop for Mac，在其他平台上被忽略。
>      - `--mount` 标记不支持用于修改 selinux 标签的 `z` 或 `Z`选项。
>
> 2. `-v` 和 `--mount` 行为之间的差异
>
> 由于 `-v` 和 `-volume` 标记长期以来一直是 Docker 的一部分，它们的行为无法改变。这意味着 `-v` 和 `-mount` 之间有一个不同的行为。
>
> 如果您使用 `-v` 或 `-volume` 来绑定挂载 Docker 主机上还不存在的文件或目录，则 `-v` 将为您创建它。它总是作为目录创建的。
>
> 如果使用 `--mount` 绑定挂载 Docker 主机上还不存在的文件或目录，Docker 不会自动为您创建它，而是产生一个错误。
>
> 3. Docker 挂载方式
>
>    Docker 提供了 3 种方法将数据从 Docker 宿主机挂载（mount）到容器：`volumes`，`bind mounts`和`tmpfs mounts`。一般来说，`volumes`总是最好的选择。
>
>    不管你选择哪种挂载方式，从容器中看都是一样的。数据在容器的文件系统中被展示为一个目录或者一个单独的文件。
>
>    一个简单区分`volumes`，`bind mounts`和`tmpfs mounts`不同点的方法是：**思考数据在宿主机上是如何存在的。**
>
>    - **Volumes**由 Docker 管理，存储在宿主机的某个地方（在 linux 上是`/var/lib/docker/volumes/`）。非 Docker 应用程序不能改动这一位置的数据。Volumes 是 Docker 最好的数据持久化方法。
>    - **Bind mounts**的数据可以存放在宿主机的任何地方。数据甚至可以是重要的系统文件或目录。非 Docker 应用程序可以改变这些数据。
>    - **tmpfs mounts**的数据只存储在宿主机的内存中，不会写入到宿主机的文件系统。

# docker 知识碎片

## debconf: unable to initialize frontend: Dialog

> [debconf: unable to initialize frontend: Dialog 问题解决](https://blog.csdn.net/weixin_44413445/article/details/137875391?spm=1001.2101.3001.6650.3&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EYuanLiJiHua%7EPosition-3-137875391-blog-111039589.235%5Ev43%5Epc_blog_bottom_relevance_base3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EYuanLiJiHua%7EPosition-3-137875391-blog-111039589.235%5Ev43%5Epc_blog_bottom_relevance_base3&utm_relevant_index=4)

文章讲述了在使用 debconf 时遇到初始化前端问题（Dialog 和 Readline 不支持）的解决方案，包括通过命令行设置非交互式模式和在 Dockerfile 中修改环境变量 DEBIAN_FRONTEND。还提到了在 CI/CD 流程中的应用实例。

法一：

```shell
echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
sudo apt-get install -y -q
```

由于用的 cicd，选择在 sh 文件中加上述内容解决问题

法二：
修改 Dockerfile，添加 DEBIAN_FRONTEND=noninteractive

参考
https://github.com/moby/moby/issues/27988

## Docker：如何关闭以--restart=always 启动的容器

```shell
docker update --restart=no <container-id>
docker stop <container-id>
```

## Error response from daemon: No such image

> [Docker 删除镜像失败](https://blog.csdn.net/maple0102/article/details/82690215)
>
> [docker tag Error response from daemon: No such image: lhzx-gateway:latest](https://blog.51cto.com/u_16175504/6945027)

1. 删除所有镜像、容器、网络和卷的方法：`docker system prune -a`
2. 可能是由于 Docker 守护进程出现了错误。在这种情况下，可以尝试重启 Docker 服务。`sudo systemctl restart docker`
