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

![img](https://pic3.zhimg.com/80/v2-dac570abcf7e1776cc266a60c4b19e5e_720w.webp)

最后，让我们来看一下docker的底层实现。



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

**镜像**：可以理解为软件安装包，可以方便的进行传播和安装。

**容器**：软件安装后的状态，每个软件运行环境都是独立的、隔离的，称之为容器。

**仓库**：镜像集中存储、分发的服务，类似 Github 软件仓库。


