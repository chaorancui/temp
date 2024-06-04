# CCE-C培训认证课程（初级）

[toc]



![](https://ilearning.huawei.com/edx/assets/courseware/v1/7df76efb8a9de3816c669b7bb25eb1c8/asset-v1:HuaweiX+CNE052301001461+Self-paced+type@asset+block/CCE-C%E5%9F%B9%E8%AE%AD%E8%AE%A4%E8%AF%81%E8%AF%BE%E7%A8%8B_%E5%88%9D%E7%BA%A7_.png)

## 导引：并行编程思维





## 模块一：Davinci基本架构讲解





## 模块二：



































# Docker 学习

> [什么是Docker？看这一篇干货文章就够了！](https://zhuanlan.zhihu.com/p/187505981)

**目的**

为解决重复搭建开发/测试环境的问题，应运而生的技术。



**容器技术 vs 虚拟机**

虚拟机 clone 也可以解决问题，但虚拟机需要同步 clone 操作系统，内存浪费且启动慢。对于**仅部署应用程序**诉求来说，不是最优解。



**什么是容器**

容器一词的英文是container，其实container还有集装箱的意思，集装箱绝对是商业史上了不起的一项发明，大大降低了海洋贸易运输成本。让我们来看看集装箱的好处：

- 集装箱之间相互隔离
- 长期反复使用
- 快速装载和卸载
- 规格标准，在港口和船上都可以摆放

回到软件中的容器，其实容器和集装箱在概念上是很相似的。

与虚拟机通过操作系统实现隔离不同，容器技术**只隔离应用程序的运行时环境但容器之间可以共享同一个操作系统**，这里的运行时环境指的是程序运行依赖的各种库以及配置。

容器更加的**轻量级且占用的资源更少**，与操作系统动辄几G的内存占用相比，容器技术只需数M空间，因此我们可以在同样规格的硬件上**大量部署容器**，这是虚拟机所不能比拟的，而且不同于操作系统数分钟的启动时间容器几乎瞬时启动，容器技术为**打包服务栈**提供了一种更加高效的方式，So cool。

那么我们该怎么使用容器呢？这就要讲到docker了。

==注意，**容器是一种通用技术，docker只是其中的一种实现**。==



**什么是docker**

docker是一个用Go语言实现的开源项目，可以让我们方便的创建和使用容器，docker将程序以及程序所有的依赖都打包到docker container，这样你的程序可以在任何环境都会有一致的表现，这里程序运行的依赖也就是容器就好比集装箱，容器所处的操作系统环境就好比货船或港口，**程序的表现只和集装箱有关系(容器)，和集装箱放在哪个货船或者哪个港口(操作系统)没有关系**。

因此我们可以看到docker可以屏蔽环境差异，也就是说，只要你的程序打包到了docker中，那么无论运行在什么环境下程序的行为都是一致的，程序员再也无法施展表演才华了，**不会再有“在我的环境上可以运行”**，真正实现“build once, run everywhere”。

此外docker的另一个好处就是**快速部署**，这是当前互联网公司最常见的一个应用场景，一个原因在于容器启动速度非常快，另一个原因在于只要确保一个容器中的程序正确运行，那么你就能确信无论在生产环境部署多少都能正确运行。



**如何使用docker**

docker中有这样几个概念：

- dockerfile
- image
- container

实际上你可以简单的把image理解为可执行程序，container就是运行起来的进程。

那么写程序需要源代码，那么“写”image就需要dockerfile，dockerfile就是image的源代码，docker就是"编译器"。

因此我们只需要在dockerfile中指定需要哪些程序、依赖什么样的配置，之后把dockerfile交给“编译器”docker进行“编译”，也就是docker build命令，生成的可执行程序就是image，之后就可以运行这个image了，这就是docker run命令，image运行起来后就是docker container。

具体的使用方法就不再这里赘述了，大家可以参考docker的官方文档，那里有详细的讲解。



**docker是如何工作的**

实际上docker使用了常见的CS架构，也就是client-server模式，docker client负责处理用户输入的各种命令，比如`docker build`、`docker run`，真正工作的其实是 server，也就是 docker daemon，值得注意的是，docker client 和 docker daemon 可以运行在同一台机器上。

接下来我们用几个命令来讲解一下docker的工作流程：



**1，docker build**

当我们写完dockerfile交给docker“编译”时使用这个命令，那么client在接收到请求后转发给docker daemon，接着docker daemon根据dockerfile创建出“可执行程序”image。

![img](https://pic3.zhimg.com/80/v2-f16577a98471b4c4b5b1af1036882caa_720w.webp)



**2，docker run**

有了“可执行程序”image后就可以运行程序了，接下来使用命令docker run，docker daemon接收到该命令后找到具体的image，然后加载到内存开始执行，image执行起来就是所谓的container。

![img](https://pic4.zhimg.com/80/v2-672b29e2d53d2ab044269b026c6bc473_720w.webp)



**3，docker pull**

其实docker build和docker run是两个最核心的命令，会用这两个命令基本上docker就可以用起来了，剩下的就是一些补充。

那么docker pull是什么意思呢？

我们之前说过，docker中image的概念就类似于“可执行程序”，我们可以从哪里下载到别人写好的应用程序呢？很简单，那就是APP Store，即应用商店。与之类似，既然image也是一种“可执行程序”，那么有没有"Docker Image Store"呢？答案是肯定的，这就是Docker Hub，docker官方的“应用商店”，你可以在这里下载到别人编写好的image，这样你就不用自己编写dockerfile了。

docker registry 可以用来存放各种image，公共的可以供任何人下载image的仓库就是docker Hub。那么该怎么从Docker Hub中下载image呢，就是这里的docker pull命令了。

因此，这个命令的实现也很简单，那就是用户通过docker client发送命令，docker daemon接收到命令后向docker registry发送image下载请求，下载后存放在本地，这样我们就可以使用image了。



**docker的底层实现**

docker基于Linux内核提供这样几项功能实现的：

- **NameSpace**
  我们知道Linux中的PID、IPC、网络等资源是全局的，而NameSpace机制是一种资源隔离方案，在该机制下这些资源就不再是全局的了，而是属于某个特定的NameSpace，各个NameSpace下的资源互不干扰，这就使得每个NameSpace看上去就像一个独立的操作系统一样，但是只有NameSpace是不够。
- **Control groups**
  虽然有了NameSpace技术可以实现资源隔离，但进程还是可以不受控的访问系统资源，比如CPU、内存、磁盘、网络等，为了控制容器中进程对资源的访问，Docker采用control groups技术(也就是cgroup)，有了cgroup就可以控制容器中进程对系统资源的消耗了，比如你可以限制某个容器使用内存的上限、可以在哪些CPU上运行等等。

有了这两项技术，容器看起来就真的像是独立的操作系统了。

> 说明：
>
> “真正实现“build once, run everywhere””。这句话是错误的，实际上程序员依然有演戏的空间。因为容器只打包了用户空间的系统调用，执行系统调用的地方依然是宿主的kernel，所以当你docker run centos:6 bash执行这句话的时候，在新的内核上可能会发生段错误，而老的宿主机却不会。**真正要做到BORE，还是必使用同样的内核**，那样的话，和使用虚拟机就没差别了。总之不可能做到开发，测试，运维只要用同一个镜像就能表现完全一致，只要提供系统调用的内核版本不同，嗯，行为就绝对不能保证一致。



# **Docker 快速入门**

> [**Docker 快速入门**](https://docker.easydoc.net/doc/81170005/cCewZWoN/lTKfePfP)
>
> [Docker — 从入门到实践](https://yeasy.gitbook.io/docker_practice)

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

-  镜像（`Image`）：Docker 镜像是一个特殊的文件系统，除了提供[容器](https://cloud.tencent.com/product/tke?from_column=20065&from=20065)运行时所需的程序、库、资源、配置等文件外，还包含了一些为运行时准备的一些配置参数（如匿名卷、环境变量、用户等）。镜像不包含任何动态数据，其内容在构建之后也不会被改变。 
-  容器（`Container`）：镜像（`Image`）和容器（`Container`）的关系，就像是面向对象程序设计中的 `类` 和 `实例` 一样，镜像是静态的定义，容器是镜像运行时的实体。容器可以被创建、启动、停止、删除、暂停等。 
-  仓库（`Repository`）：仓库（`Repository`）类似Git的远程仓库，集中存放镜像文件。 

三者关系可以用下图表示：

![Docker](https://ask.qcloudimg.com/http-save/yehe-7565276/joa65awgh4.png)







# 震惊😱 超详细的 Docker 常用命令

> [震惊😱 超详细的 Docker 常用命令](https://juejin.cn/post/7245275769219203132)
>
> [一张脑图整理Docker常用命令](https://cloud.tencent.com/developer/article/1772136)

![Docker](https://ask.qcloudimg.com/http-save/yehe-7565276/6lldlbgfhn.png)



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

**搜索镜像**

```shell
# 从Docker Hub查找镜像
docker search [OPTIONS] TERM

--automated :只列出 automated build类型的镜像；
--no-trunc :显示完整的镜像描述；
-f <过滤条件>:列出收藏数不小于指定值的镜像。

# 例：
docker search -f stars=10 java # 从 Docker Hub 查找所有镜像名包含 java，并且收藏数大于 10 的镜像
```



**拉取镜像**

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



**使用`Dockerfile`构建镜像**

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



**查看本地镜像**

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



**删除本地镜像**

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



**导出镜像**

```bash
# 将指定镜像保存成 tar 归档文件
docker save [OPTIONS] IMAGE [IMAGE...]

-o :输出到的文件。

# 例：
docker save -o my_ubuntu_v3.tar runoob/ubuntu:v3
```



**导入镜像**

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

**创建容器**

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



**查看容器列表**

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
> STATUS: 容器状态。 状态有7种：
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
> 这些状态中，最重要和常见的是除了restarting（重启中）和removing（迁移中）之外的五个状态，下面基本上网络上大部分的容器生命周期图都只包含五个状态：created（已创建），running（运行中），paused（暂停），exited（停止），dead（死亡）。



**启动/停止/重启运行的容器**

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



**进入容器执行命令**(正在运行的容器才可以进入)

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
```



**查看容器信息**

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

![docker-inspect.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6fae54d11c904fc1973f73e7390ca6fb~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)



**容器与宿主机之间的数据拷贝**

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

