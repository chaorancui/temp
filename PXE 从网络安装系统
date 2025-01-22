# PXE 从网络安装系统

参考资料：
[1]. [从零开始：搭建 PXE 远程批量安装服务器](https://asterfusion.com/a20240424-pxe/?srsltid=AfmBOorqWNykCeAY6kI0SmUZASD2hvsAfRplOzGzCj_qgWz91xSlcXA_)
[2]. [自动化批量安装系统：PXE 服务器搭建](https://blog.gpx.moe/2023/02/09/pxe-server/)
[3]. [一步步搭建 PXE 网络装机](https://yunfwe.github.io/2018/06/03/2018/%E4%B8%80%E6%AD%A5%E6%AD%A5%E6%90%AD%E5%BB%BAPXE%E7%BD%91%E7%BB%9C%E8%A3%85%E6%9C%BA/)
[4]. [dnsmasq 部署 pxe 服务器脚本](https://developer.aliyun.com/article/529076)
[5]. [使用dnsmasq从网络PXE引导安装Arch/Debian/Suse Linux系统](https://blog.csdn.net/weixin_43869959/article/details/90146987?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7Ebaidujs_baidulandingword%7ECtr-2-90146987-blog-136810938.235%5Ev43%5Epc_blog_bottom_relevance_base5&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7Ebaidujs_baidulandingword%7ECtr-2-90146987-blog-136810938.235%5Ev43%5Epc_blog_bottom_relevance_base5&utm_relevant_index=3)
[ubuntu安装dnsmasq 做dns服务器](https://blog.csdn.net/weixin_42833423/article/details/141815079?spm=1001.2101.3001.6650.8&utm_medium=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~Rate-8-141815079-blog-136810938.235%5Ev43%5Epc_blog_bottom_relevance_base5&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~Rate-8-141815079-blog-136810938.235%5Ev43%5Epc_blog_bottom_relevance_base5&utm_relevant_index=13)
[在centos7上部署pxe服务器](https://zhuanlan.zhihu.com/p/623516185)
[https://www.myfreax.com/how-to-install-nginx-on-ubuntu-22-04/](https://www.myfreax.com/how-to-install-nginx-on-ubuntu-22-04/)
[PXE网络安装系统之基于dnsmasq的环境搭建](https://lemubei.com/p/pxe%E7%BD%91%E7%BB%9C%E5%AE%89%E8%A3%85%E7%B3%BB%E7%BB%9F%E4%B9%8B%E5%9F%BA%E4%BA%8Ednsmasq%E7%9A%84%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA/)
[JimmyXu的小站](https://xujimmy.com/2019/07/21/pxe-install-os.html)


## PXE 介绍

在大规模服务器部署时，面对成百上千台服务器，通过手动插入光盘或者 USE 驱动器来安装操作系统无比繁琐，让大量工程师在现场挨个安装系统也不切实际，PXE 的出现使得网络远程批量自动安装和配置操作系统成为现实。

### 什么是 PXE

PXE（Pre-boot Execution Environment，预启动执行环境）是由 Intel 设计的协议，它允许计算机通过网络启动。这个协议工作在 Client/Server 模式下，允许客户机通过网络从远程服务器下载引导镜像，并加载安装文件或整个操作系统。

相比其他工具，PXE 更好地解决了以下问题：

- 自动化：PXE 允许自动安装和配置操作系统，减少了手动操作的工作量。
- 远程实现：通过网络远程安装操作系统，无需物理介质，方便管理远程服务器。
- 规模化：特别适用于大规模服务器部署，可以同时装配多台服务器。。

### PXE 工作原理和配置

工作原理

1. PXE 启动：当终端进入网卡启动时，会发送一个特殊的 PXE 启动请求到本地网络上的 DHCP 服务器。
2. DHCP 服务：DHCP 服务器收到 PXE 启动请求后，会向计算机发送 DHCP 响应，DHCP 响应包含了计算的网络配置信息，以及 PXE 引导服务器的 IP 地址——TFTP Server（Trivial File Transfer Protocol）。
3. TFTP 传输：计算机收到 DHCP 响应后，会使用 TFTP 从 Server 下载引导文件——pxelinux.0 或者 bootx64.efi。
4. 加载引导文件：计算机加载并执行从 TFTP 下载的引导文件。引导文件通常是一个小型的 Linux 内核，能够连接到 PXE 服务器并获取操作系统镜像。
5. 获取配置信息：引导文件连接到 PXE 服务器后，会通过 TFTP 发送请求以获取更多的配置信息。
6. 获取操作系统镜像：PXE 服务器根据计算机的请求，将系统镜像发送给计算机。
7. 操作系统加载：一旦操作系统映像文件下载完成，计算机会加载并执行该映像文件。此时，计算机将完全从网络上运行操作系统，而无需本地硬盘上的安装。

![](https://asterfusion.com/wp-content/uploads/2024/04/%E5%85%AC%E4%BC%97%E5%8F%B7%E6%96%87%E7%AB%A0-%E3%80%8APXE%E3%80%8B-%E9%85%8D%E5%9B%BE2-20240424.jpeg)

注意：虽然 PXE 很好用，但启动时也需要满足以下条件

1. 网卡支持 PXE，目前新出的网卡基本都支持，同时需要完成 BIOS 的启动项配置。
2. 传统启动模式（Legacy）下，PXE 客户端会请求 pxelinux.0；UEFI 启动会请求 bootx64.efi。
3. 也可以采用 nfsboot 方式，该流程采用的是 ISO 镜像下载再安装的方式。

## Linux 下搭建 PXE 服务器

PXE 对运行环境没有什么需求，只需能提供 tftp, dhcp, http 等服务的系统即可。这里使用 Linux 环境来搭建 PXE 服务。

### dnsmasq + Nginx

使用 dnsmasq 这个小巧玲珑的软件提供 tftp 和 dhcp 服务，使用 Nginx 来提供 http 服务。

#### 安装配置 dnsmasq

> 参考链接：
>
> 1. [ubuntu22.04 安装 dnsmasq 最详细易懂](https://blog.csdn.net/zwjzone/article/details/137114806)
> 2. [ubuntu 安装 dnsmasq 做 dns 服务器](https://blog.csdn.net/weixin_42833423/article/details/141815079?spm=1001.2101.3001.6650.8&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-8-141815079-blog-136810938.235%5Ev43%5Epc_blog_bottom_relevance_base5&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-8-141815079-blog-136810938.235%5Ev43%5Epc_blog_bottom_relevance_base5&utm_relevant_index=13)
> 3.

**一、安装**

> ubuntu 22 版本默认自带 dnsmasq，要么直接使用，要么关闭自带的 dns 服务后再启用自己安装 dnsmasq 软件包，否则就会产生冲突。
> Ubuntu 22.04 默认使用 systemd-resolved 管理自带的 dns，可用如下命令禁用：
>
> ```bash
> systemctl stop systemd-resolved
> systemctl disable systemd-resolved
> ```

最好在 root 账户下操作：

```bash
sudo -i
```

可以首先从 Linux 发行版的官方仓库中找找有没有 dnsmasq 的软件包，如果没有可以下载编译。

1. 直接安装

   ```bash
   sudo apt update
   sudo apt install dnsmasq
   ```

2. 编译安装

   > 注意：可以更新到最新版本，截止 2025/01/20 最新版本为 2.90.

   ```bash
   cd /usr/local/src/
   wget http://www.thekelleys.org.uk/dnsmasq/dnsmasq-2.90.tar.xz
   tar xf dnsmasq-2.90.tar.xz
   cd dnsmasq-2.90 && make
   cp src/dnsmasq /usr/local/bin/
   ```

   只需要将 dnsmasq 的二进制文件放到系统环境变量就可以了，接下来给它提供一个配置文件来告诉它要启动哪些服务。源码目录下有一个官方提供的配置文件模板，不过我们并不需要这么多的配置。

**二、配置**

```bash
mkdir -p /data/pxeboot          # PXE启动所需要的文件就都放到这里了
cd /data/pxeboot
vim dnsmasq.conf
```

然后写入以下内容：

```bash
## disable dns，用不着可以关闭
port=0

## enable dhcp
dhcp-range=192.168.4.10,192.168.4.200,12h # DHCP 地址范围
dhcp-option=3,192.168.4.254 # 默认网关
dhcp-option=option:dns-server,114.114.114.114,119.29.29.29 # 114/腾讯

# dhcp-boot=pxelinux.0 # bios 引导
# dhcp-boot=grubx64.efi # efi 引导
dhcp-boot=undionly.kpxe

## 指定某个特定网卡监听，不配置监听所有
# interface=ens8u2u4u1

## enable tftp
enable-tftp
tftp-root=/data/pxeboot
```

分析：

- `port=0`：此配置项禁用 DNS 服务。默认情况下，`dnsmasq` 会监听 53 端口来提供 DNS 服务。通过设置 `port=0`，`dnsmasq` 将不启动 DNS 功能。
- `dhcp-range=192.168.4.10,192.168.4.200,12h`：指定 DHCP 服务分配的 IP 地址范围。这里是从 `192.168.4.10` 到 `192.168.4.200`，并且租期为 12 小时。客户端会从这个范围内获取 IP 地址。
- `dhcp-option=3,192.168.4.254`：设置 DHCP 选项 3（即默认网关）。客户端将收到 `192.168.4.254` 作为默认网关，意味着所有发送到非本地网络的流量都会通过该网关转发。
- `dhcp-option=option:dns-server,114.114.114.114,119.29.29.29`：设置 DHCP 选项 6（即 DNS 服务器）。在客户端获得 IP 地址的同时，它们也会得到 `114.114.114.114` 和 `119.29.29.29` 作为 DNS 服务器地址。这里提供的是两个公共 DNS 服务器：一个是 114DNS（由中国电信提供），另一个是腾讯的 DNS。
- `dhcp-boot=undionly.kpxe`：这是配置 PXE 引导的部分。`undionly.kpxe` 是一个用于 PXE 启动的文件，通常用于网络启动。PXE 是一种通过网络引导操作系统的方式，这里使用的是 `undionly.kpxe` 文件，它是适用于没有 UEFI 支持的 BIOS 系统。如果你使用的是 UEFI 系统，可能会使用 `grubx64.efi` 文件。
- `interface=ens8u2u4u1`：如果需要指定 `dnsmasq` **只在某个特定的网络接口上监听**，可以取消注释并设置此项。这里的 `ens8u2u4u1` 是一个网络接口的名称（可用 `lshw -C network` 或 `ifconfig` 查看），代表 `dnsmasq` 只会在此接口上工作。由于这一行被注释掉，`dnsmasq` 将监听所有网络接口。
- `enable-tftp`：启用 TFTP（Trivial File Transfer Protocol）服务。TFTP 是一个简单的文件传输协议，通常用于网络启动（PXE 启动）。当客户端请求启动文件时，`dnsmasq` 将通过 TFTP 传输相应的文件。
- `tftp-root=/data/pxeboot`：指定 TFTP 服务的根目录，即网络启动文件存放的位置。在这个配置中，`dnsmasq` 会从 `/data/pxeboot` 目录提供文件（如 `undionly.kpxe` 或其他 PXE 启动所需的文件）。

一定要注意，dhcp-range 给客户端分配的 IP 地址池一定要是自己网段的。根据前面讲解的 PXE 启动的原理，可能大家会比较好奇，为什么这里 dhcp 推送的是 undionly.kpxe 这个文件呢？这个会在下面讲到，接下来就可以先启动 dnsmasq 了。

#### 安装配置 Nginx

参考链接：

1. [在 Ubuntu 22.04 上安装和配置 Nginx 的完整指南](https://blog.csdn.net/u011715638/article/details/138670319)
2.

Nginx 是一款高性能的开源 Web 服务器软件，它可以用于反向代理、负载均衡、静态文件服务等。

**一、安装**

```bash
# 1.更新系统包列表
sudo apt update
# 2.安装Nginx
sudo apt install nginx
```

**二、配置**

1. 检查 Nginx 状态

   ```bash
   sudo systemctl status nginx
   ```

   如果没有启动，可以手动启动 Nginx，命令命令如下：

   ```bash
   # 启动Nginx
   sudo systemctl start nginx
   # 停止Nginx
   sudo systemctl stop nginx
   # 重启Nginx
   sudo systemctl restart nginx
   # 重新加载配置（不中断服务）
   sudo systemctl reload nginx
   # 设置开机自启
   sudo systemctl enable nginx
   # 禁止开机自启
   sudo systemctl disable nginx
   ```

2. 防火墙配置

   如果你启用了 UFW 防火墙，需要允许 HTTP 和 HTTPS 流量。执行以下命令：

   ```bash
   sudo ufw status # 检查防火墙状态
   # 若显示inactive表示没有启用。启用命令：sudo ufw enable
   # 若显示active表示启用。禁用命令：sudo ufw disable

   # 若 UFW 开启
   sudo ufw allow 'Nginx Full'
   # 这将允许 HTTP（80 端口）和 HTTPS（443 端口）流量。
   ```

   检查防火墙规则，确保它们已应用：

   ```bash
   sudo ufw status
   ```

3. 基本 Nginx 配置

   主要配置文件位置：

   ```bash
   /etc/nginx/                  # Nginx主配置目录
   /etc/nginx/nginx.conf       # 主配置文件
   /etc/nginx/sites-available/ # 可用站点配置
   /etc/nginx/sites-enabled/  # 已启用站点配置
   /var/log/nginx/           # 日志文件目录
   /var/www/html/           # 默认网站根目录
   ```

   通常，您可以将您的站点配置文件放在 sites-available 目录中，并通过创建符号链接到 sites-enabled 目录来启用它们。

   ```bash
   sudo vim /etc/nginx/sites-available/my_site
   # 添加内容并保存文件
   sudo ln -s /etc/nginx/sites-available/my_site /etc/nginx/sites-enabled/
   ```

   > [自动化批量安装系统：PXE 服务器搭建](https://blog.gpx.moe/2023/02/09/pxe-server/)

4. 测试 Nginx 配置

   在重新加载 Nginx 配置之前，您可以使用以下命令检查配置是否存在语法错误：

   ```bash
   sudo nginx -t
   ```

   如果没有错误，您会看到类似于以下的输出：

   nginx: configuration file /etc/nginx/nginx.conf test is successful

5. 重新加载 Nginx

   一旦配置文件通过了语法检查，您可以通过以下命令重新加载 Nginx 以应用新的配置：

   ```bash
   sudo systemctl reload nginx
   ```

6. 访问 Nginx 欢迎页面

   ```bash
   curl -v http://<Server-IP-Address>:<port>
   ```

   或者打开浏览器，访问 `http://{Your-Server-IP-Address}:{port}`。

## Windows 下搭建 PXE 服务器

参考链接：

1. [windows tftpd64 软件的 TFTP service 使用](https://blog.csdn.net/m0_46141595/article/details/137144085)
2. [Windows系统下搭建PXE Server](https://blog.csdn.net/u010438035/article/details/134590199)
3. 

## 各种服务常用端口

1. HTTP 服务：`80/tcp`，其余还有 `8080/3128/8081/9080` 等
2. HTTPS（securely transferring web pages）服务：`443/tcp 443/udp`
3. FTP（文件传输）协议代理服务器常用端口号：`21/tcp`
4. Telnet（远程登录）协议代理服务器常用端口：`23/tcp`
5. SSH（安全登录）、SCP（文件传输）、端口重定向：`22/tcp`
6. TFTP（Trivial File Transfer Protocol）服务：`69/udp`
7. SOCKS 服务：`1080`
8. SMTP Simple Mail Transfer Protocol (E-mail）：`25/tcp`
9. POP3 Post Office Protocol (E-mail) ：`110/tcp`
10. TOMCAT 服务：`8080`
