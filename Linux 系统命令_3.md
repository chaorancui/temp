[toc]

# 系统设备命令

## lspci 命令

**lspci** 是一个用来显示系统中所有 PCI 总线设备或连接到该总线上的所有设备的工具。

```bash
lspci [options]
```

- **-v**

  使得 _lspci_ 以冗余模式显示所有设备的详细信息。

- **-vv**

  使得 _lspci_ 以过冗余模式显示更详细的信息 (事实上是 PCI 设备能给出的所有东西)。这些数据的确切意义没有在此手册页中解释，如果你想知道更多，请参照 **/usr/include/linux/pci.h** 或者 PCI 规范。

- **-t**

  以树形方式显示包含所有总线、桥、设备和它们的连接的图表。

```shell
# 实例
# 查看网卡生产商，型号
lspci | grep -i net
```

## lsusb 命令

> lsusb 查看当前有哪些 usb 设备。注意：插在 usb 口上的外接设备一定能通过 lsusb 显示出来，但是不一定能通过 lspci 显示出来，即使这个设备的驱动已经安装了。

`lsusb` 是 Linux 系统中一个非常常用的命令，用于列出连接到系统上的 USB（通用串行总线）设备的信息。这个命令主要用于调试和查看 USB 设备的状态，是排查 USB 设备识别问题的利器。

**基本用法**：

```bash
lsusb
```

这条命令会列出当前系统识别到的所有 USB 设备，每个设备一行。输出示例如下：

```log
Bus 002 Device 003: ID 046d:c52b Logitech, Inc. Unifying Receiver
Bus 001 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
```

字段解释：

- `Bus 002`: USB 总线编号
- `Device 003`: USB 设备号（在该总线上的编号）
- `ID 046d:c52b`: USB 设备的厂商 ID（Vendor ID）和产品 ID（Product ID）
- `Logitech, Inc. Unifying Receiver`: 设备厂商和设备名称（如能识别）

---

**常用选项**：

| 选项                    | 说明                                                                |
| ----------------------- | ------------------------------------------------------------------- |
| `-v`                    | 显示详细信息（verbose），会输出每个设备的详细描述。需要 root 权限。 |
| `-t`                    | 以树状结构显示设备之间的拓扑关系。                                  |
| `-s [bus]:[dev]`        | 只查看指定的 Bus 和 Device 编号的设备信息。                         |
| `-d [vendor]:[product]` | 只查看指定 Vendor ID 和 Product ID 的设备。                         |
| `-V`                    | 显示 `lsusb` 版本信息。                                             |

**示例**：

1. 查看详细信息（root 权限推荐）

   ```bash
   sudo lsusb -v
   ```

2. 查看树状结构

   ```bash
   lsusb -t
   ```

3. 查看指定设备的详细信息

   ```bash
   lsusb -s 002:003 -v
   ```

**补充说明**：

- `lsusb` 本质上是 `usbutils` 软件包的一部分，在大多数 Linux 发行版中可以通过以下命令安装：

  ```bash
  # Debian/Ubuntu
  sudo apt install usbutils
  # RedHat/CentOS/Fedora
  sudo dnf install usbutils
  # Arch
  sudo pacman -S usbutils
  ```

- 如果你插了设备，但 `lsusb` 里看不到，可能需要检查：
  - 是否物理连接没问题
  - 是否内核支持对应驱动
  - `dmesg` 中是否有设备识别失败的提示

## lshw 命令

`lshw`（**List Hardware**）是 Linux 下一个非常强大的**硬件信息查看工具**，可以详细列出系统中主板、CPU、内存、网卡、磁盘、总线等的硬件型号、序列号、速度、驱动、厂商、固件版本等等。相比 `lscpu`、`lsblk` 等专用工具，`lshw` 更像是一个全能硬件侦探。

**安装方式**：

```bash
# Debian/Ubuntu
sudo apt install lshw
# Arch Linux
sudo yum install lshw
# Arch Linux
sudo yum install lshw
```

**常用选项总结**：

| 选项            | 说明                                            |
| --------------- | ----------------------------------------------- |
| `-short`        | 简洁模式，快速查看硬件                          |
| `-class [类型]` | 只列出指定类别（如 cpu、memory、disk、network） |
| `-C [类型]`     | 同 `-class`，大小写敏感更宽容                   |
| `-sanitize`     | 屏蔽序列号、MAC 等敏感信息                      |
| `-json`         | 以 JSON 格式输出                                |
| `-html`         | 输出为 HTML 格式（适合做报告）                  |
| `-quiet`        | 静默模式，隐藏错误或警告信息                    |

---

**示例用法**：

1. 查看 CPU 信息

   ```bash
   sudo lshw -class cpu

   # 输出示例：
     *-cpu
          description: CPU
          product: Intel(R) Core(TM) i7-9700K CPU @ 3.60GHz
          vendor: Intel Corp.
          physical id: 3
          bus info: cpu@0
          width: 64 bits
   ```

2. 简洁模式查看硬件总览

   ```bash
   sudo lshw -short

   # 示例输出：
   H/W path       Device      Class          Description
   =====================================================
   /0/0                        memory         64KiB BIOS
   /0/4                        processor      Intel Core i7
   /0/100/1f.2    /dev/sda     disk           512GB SSD
   /0/100/1f.3                 multimedia     Audio device
   ```

3. 查看内存信息

   ```bash
   sudo lshw -class memory
   ```

   可以看到物理内存槽数量、已插入的内存条型号、容量等。

4. 导出为 HTML 或 JSON

   ```bash
   sudo lshw -html > hardware.html
   sudo lshw -json > hardware.json
   ```

   适合文档记录或做硬件审计报告。

**能查看的硬件类型**：

你可以用 `lshw -class [类型]` 查看：

- `cpu` – 处理器
- `memory` – 内存
- `disk` – 磁盘设备（HDD、SSD、NVMe）
- `network` – 网卡
- `storage` – 控制器（如 SATA/NVMe 控制器）
- `display` – 显卡
- `bus` – 总线（如 PCIe、USB 控制器）
- `battery` – 电池（笔记本）
- `system` – 主机名、厂商、BIOS

  **注意事项**：

- **必须加 `sudo`** 才能看到最完整的信息，否则很多设备会显示不全。
- 某些设备（比如 NVMe）可能不会被完全识别，需要搭配 `lsblk` / `nvme list`。
- 如果你觉得 `lshw` 输出太多，可以搭配 `less` 或 `grep` 过滤。

**vs 其他工具对比**：

| 工具                     | 功能强度 | 覆盖范围   | 输出风格     | 是否图形 |
| ------------------------ | -------- | ---------- | ------------ | -------- |
| `lshw`                   | ⭐⭐⭐⭐ | 全面       | 树状/表格    | ❌       |
| `lscpu`                  | ⭐       | 仅 CPU     | 表格         | ❌       |
| `lsblk`                  | ⭐⭐     | 存储设备   | 树状         | ❌       |
| `hwinfo`                 | ⭐⭐⭐⭐ | 全面       | 超详细       | ❌       |
| `inxi`                   | ⭐⭐⭐⭐ | 综合、简洁 | 表格         | ❌       |
| `neofetch`/`screenfetch` | ⭐       | 炫酷简要   | 终端艺术风格 | ❌       |

> `lshw` 就是 Linux 下的“全套硬件扫描神器”，用来查主板、CPU、内存、磁盘、网卡等都非常靠谱，适合做系统评估、排查硬件、制作硬件清单。

# 系统信息命令

## dmesg 命令

[dmesg 命令](https://www.runoob.com/linux/linux-comm-dmesg.html)

Linux dmesg（英文全称：display message）命令用于显示开机信息。

kernel 会将开机信息存储在 ring buffer 中。您若是开机时来不及查看信息，可利用 dmesg 来查看。开机信息亦保存在 /var/log 目录中，名称为 dmesg 的文件里。

```bash
dmesg [-cn][-s <缓冲区大小>]
```

- -c 　显示信息后，清除 ring buffer 中的内容。
- -s<缓冲区大小> 　预设置为 8196，刚好等于 ring buffer 的大小。
- -n 　设置记录信息的层级。

```bash
# 实例
# 显示开机信息
dmesg |less
```

# 系统服务命令

## systemctl 命令

`systemctl` 是 Linux 系统中用于与 **systemd** 系统和服务管理器交互的命令行工具。`systemd` 是现代 Linux 发行版（如 Ubuntu、CentOS、Debian 和 Fedora 等）中用于初始化系统和管理系统服务的核心组件。通过 `systemctl`，你可以管理和控制系统的服务、守护进程、系统状态等。

**列出所有 service**：

```shell
systemctl list-units --type=service
systemctl --type=service
```

**常用命令**，ssh 服务为例：

```bash
# 开机自动启动ssh命令
sudo systemctl enable ssh

# 关闭ssh开机自动启动命令
sudo systemctl disable ssh

# 单次开启ssh
sudo systemctl start ssh

# 单次关闭ssh
sudo systemctl stop ssh

# 设置好后重启系统
reboot

#查看ssh是否启动，看到Active: active (running)即表示成功
sudo systemctl status ssh
```

**其他命令**：

```bash
# 重新加载服务配置，某些服务（例如 Nginx、Apache）支持在不完全重启服务的情况下重新加载配置
sudo systemctl reload <service_name>

# 查看日志
# 查看特定服务的日志输出，通常通过 journalctl 配合 systemctl 使用
sudo journalctl -u <service_name>
```

## systemd 服务

`systemd` 是现代 Linux 系统中用来管理系统启动、服务管理、进程监控等任务的初始化系统和系统管理器。它是许多主流 Linux 发行版（如 Ubuntu、Fedora、Debian、CentOS 等）的默认系统和服务管理工具。

在传统的 Unix 系统中，使用的是老式的 SysVinit 系统来启动服务和管理进程，而 `systemd` 是一个现代化的替代方案，它解决了许多传统初始化系统的问题，提供了更高效、更强大的功能。

### 启动过程

`systemd` 在 Linux 系统启动时首先启动，并接管系统的初始化过程，取代了传统的 SysVinit。它通过 **并行化** 启动服务和处理任务，从而加速了系统的启动过程。与传统的线性启动方式不同，`systemd` 可以同时启动多个服务，提高了系统的启动效率。

### 主要组件和功能

1. Unit（单元）

   `systemd` 通过 **unit**（单元）管理系统的各类服务、挂载点、套接字等。每个单元有不同的类型，用于表示不同的任务或资源。例如：

   - **service unit**（服务单元）：用于管理后台服务进程（例如 HTTP 服务、数据库服务等）。
   - **mount unit**（挂载单元）：用于挂载文件系统。
   - **socket unit**（套接字单元）：用于处理网络通信或文件 I/O 等任务。
   - **target unit**（目标单元）：用于定义系统的运行级别，类似于传统的运行级别概念（例如，图形界面模式、多用户模式等）。

2. 并行启动

   传统的系统初始化使用串行启动，即服务依赖于前一个服务的启动，而 `systemd` 支持 **并行启动**，可以在没有相互依赖的情况下同时启动多个服务，显著提高了启动速度。

3. 依赖关系

   `systemd` 允许服务之间建立依赖关系，确保服务按照特定的顺序启动或停止。例如，一个 Web 服务器可能依赖于数据库服务，`systemd` 会确保数据库服务在 Web 服务器启动之前完成启动。

4. 日志管理（Journal）

   `systemd` 内置了日志系统，称为 **journal**，它能够收集和存储系统和服务的日志消息。与传统的日志文件不同，`journal` 将日志存储在二进制文件中，能够提供更强的查询功能。通过 `journalctl` 命令，用户可以轻松查看和分析系统日志。

5. 并发和依赖控制

   `systemd` 允许服务的启动、停止和重启依赖于其他服务的状态。例如，一个网络服务的启动可能依赖于网络接口的激活，`systemd` 会自动处理这些依赖关系。

6. 服务监控和自动重启

   `systemd` 提供了 **服务监控** 功能，可以检测服务是否崩溃或停止运行。如果服务失败，`systemd` 可以自动重启服务，确保系统的稳定性和可靠性。

7. 控制系统资源

   `systemd` 可以控制和管理服务的资源使用，例如，限制内存、CPU、磁盘 I/O 等资源的使用，从而避免某些服务占用过多资源导致系统不稳定。

8. **与传统 SysVinit 的对比**

   | 特性         | SysVinit                 | systemd                                |
   | ------------ | ------------------------ | -------------------------------------- |
   | 启动方式     | 串行启动                 | 并行启动                               |
   | 服务管理     | 基于脚本（/etc/init.d/） | 基于 unit 文件（/etc/systemd/system/） |
   | 服务依赖管理 | 不支持自动管理依赖关系   | 支持服务依赖自动管理                   |
   | 系统日志     | 单独的日志文件           | 集成的日志系统（journal）              |
   | 服务重启     | 手动配置                 | 支持自动重启服务                       |

### 常见命令和操作

使用 `systemd` 时，常用的命令包括：

- **启动服务**：`sudo systemctl start <service_name>`
- **停止服务**：`sudo systemctl stop <service_name>`
- **查看服务状态**：`sudo systemctl status <service_name>`
- **重启服务**：`sudo systemctl restart <service_name>`
- **启用服务（开机启动）**：`sudo systemctl enable <service_name>`
- **禁用服务（禁止开机启动）**：`sudo systemctl disable <service_name>`
- **查看日志**：`sudo journalctl -u <service_name>`

### systemd 的优势

- **快速启动**：并行化的服务启动显著缩短了系统启动时间。
- **精确的依赖管理**：服务可以按需自动启动和停止，避免不必要的依赖。
- **日志集成**：内置日志管理功能，简化了日志的存储和查看。
- **容错性**：支持自动重启崩溃的服务，确保系统稳定运行。
- **资源控制**：更好地控制每个服务的资源使用，防止某个服务影响整个系统的稳定性。

总结来说，`systemd` 是一个功能强大、灵活且高效的系统和服务管理工具，它提升了系统启动、服务管理、资源分配和日志管理的能力，逐步成为现代 Linux 系统的标准初始化系统。

# 网络命令

## ip 命令

Linux 下 [ip](https://www.runoob.com/linux/linux-comm-ip.html) 命令与 [ifconfig](https://www.runoob.com/linux/linux-comm-ifconfig.html) 命令类似，但比 ifconfig 命令更加强大，主要功能是用于显示或设置网络设备。

ip 命令是 Linux 加强版的的网络配置工具，用于代替 ifconfig 命令。

```shell
ip [ OPTIONS ] OBJECT { COMMAND | help }
```

OBJECT 为常用对象，值可以是以下几种：

```shell
OBJECT={ link | addr | addrlabel | route | rule | neigh | ntable | tunnel | maddr | mroute | mrule | monitor | xfrm | token }
```

常用对象的取值含义如下：

- link：网络设备
- address：设备上的协议（IP 或 IPv6）地址
- addrlabel：协议地址选择的标签配置
- route：路由表条目
- rule：路由策略数据库中的规则

OPTIONS 为常用选项，值可以是以下几种：

```shell
OPTIONS={ -V[ersion] | -s[tatistics] | -d[etails] | -r[esolve] | -h[uman-readable] | -iec | -f[amily] { inet | inet6 | ipx | dnet | link } | -o[neline] | -t[imestamp] | -b[atch] [filename] | -rc[vbuf] [size] }
```

常用选项的取值含义如下：

- -V：显示命令的版本信息；
- -s：输出更详细的信息；
- -f：强制使用指定的协议族；
- -4：指定使用的网络层协议是 IPv4 协议；
- -6：指定使用的网络层协议是 IPv6 协议；
- -0：输出信息每条记录输出一行，即使内容较多也不换行显示；
- -r：显示主机时，不使用 IP 地址，而使用主机的域名。

```shell
# 实例
ip link show         # 显示网络接口信息
ip link list         # 用 ip 命令显示网络设备的运行状态：
ip -s link list      # 显示更加详细的设备信息：
ip addr show         # 显示网卡IP信息
ip route list        # 显示核心路由表：
ip link | grep -E '^[0-9]' | awk -F: '{print $2}'  # 获取主机所有网络接口：
```

## ifconfig 命令

[ifconfig 命令](https://www.runoob.com/linux/linux-comm-ifconfig.html)

需要安装如下工具：

```shell
apt install net-tools
```

配置和显示 Linux 系统网卡的网络参数。用 ifconfig 命令配置的网卡信息，在网卡重启后机器重启后，配置就不存在。要想将上述的配置信息永远的存的电脑里，那就要修改网卡的配置文件了。

```shell
ifconfig [网络设备][down up -allmulti -arp -promisc][add<地址>][del<地址>][<hw<网络设备类型><硬件地址>][io_addr<I/O地址>][irq<IRQ地址>][media<网络媒介类型>][mem_start<内存地址>][metric<数目>][mtu<字节>][netmask<子网掩码>][tunnel<地址>][-broadcast<地址>][-pointopoint<地址>][IP地址]
```

**参数说明**：

- add<地址> 设置网络设备 IPv6 的 IP 地址。
- del<地址> 删除网络设备 IPv6 的 IP 地址。
- down 关闭指定的网络设备。
- <hw<网络设备类型><硬件地址> 设置网络设备的类型与硬件地址。
- io_addr<I/O 地址> 设置网络设备的 I/O 地址。
- irq<IRQ 地址> 设置网络设备的 IRQ。
- media<网络媒介类型> 设置网络设备的媒介类型。
- mem_start<内存地址> 设置网络设备在主内存所占用的起始地址。
- metric<数目> 指定在计算数据包的转送次数时，所要加上的数目。
- mtu<字节> 设置网络设备的 MTU。
- netmask<子网掩码> 设置网络设备的子网掩码。
- tunnel<地址> 建立 IPv4 与 IPv6 之间的隧道通信地址。
- up 启动指定的网络设备。
- -broadcast<地址> 将要送往指定地址的数据包当成广播数据包来处理。
- -pointopoint<地址> 与指定地址的网络设备建立直接连线，此模式具有保密功能。
- -promisc 关闭或启动指定网络设备的 promiscuous 模式。
- [IP 地址] 指定网络设备的 IP 地址。
- [网络设备] 指定网络设备的名称。

```shell
# 实例
ifconfig   #处于激活状态的网络接口
ifconfig -a  #所有配置的网络接口，不论其是否激活
ifconfig eth0  #显示eth0的网卡信息

# 显示网络设备信息（激活状态的）：
[root@localhost ~]# ifconfig
eth0      Link encap:Ethernet  HWaddr 00:16:3E:00:1E:51
          inet addr:10.160.7.81  Bcast:10.160.15.255  Mask:255.255.240.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:61430830 errors:0 dropped:0 overruns:0 frame:0
          TX packets:88534 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:3607197869 (3.3 GiB)  TX bytes:6115042 (5.8 MiB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:56103 errors:0 dropped:0 overruns:0 frame:0
          TX packets:56103 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:5079451 (4.8 MiB)  TX bytes:5079451 (4.8 MiB)
```

说明：

**eth0** 表示第一块网卡，其中`HWaddr`表示网卡的物理地址，可以看到目前这个网卡的物理地址(MAC 地址）是`00:16:3E:00:1E:51`。

**inet addr** 用来表示网卡的 IP 地址，此网卡的 IP 地址是`10.160.7.81`，广播地址`Bcast:10.160.15.255`，掩码地址`Mask:255.255.240.0`。

**lo** 是表示主机的回坏地址，这个一般是用来测试一个网络程序，但又不想让局域网或外网的用户能够查看，只能在此台主机上运行和查看所用的网络接口。比如把 httpd 服务器的指定到回坏地址，在浏览器输入 127.0.0.1 就能看到你所架 WEB 网站了。但只是您能看得到，局域网的其它主机或用户无从知道。

- 第一行：连接类型：Ethernet（以太网）HWaddr（硬件 mac 地址）。
- 第二行：网卡的 IP 地址、子网、掩码。
- 第三行：UP（代表网卡开启状态）RUNNING（代表网卡的网线被接上）MULTICAST（支持组播）MTU:1500（最大传输单元）：1500 字节。
- 第四、五行：接收、发送数据包情况统计。
- 第七行：接收、发送数据字节数统计信息。

**启动关闭指定网卡：**

```shell
ifconfig eth0 up
ifconfig eth0 down
```

`ifconfig eth0 up`为启动网卡 eth0，`ifconfig eth0 down`为关闭网卡 eth0。ssh 登陆 linux 服务器操作要小心，关闭了就不能开启了，除非你有多网卡。

**为网卡配置和删除 IPv6 地址：**

```shell
ifconfig eth0 add 33ffe:3240:800:1005::2/64    #为网卡eth0配置IPv6地址
ifconfig eth0 del 33ffe:3240:800:1005::2/64    #为网卡eth0删除IPv6地址
```

**用 ifconfig 修改 MAC 地址：**

```shell
ifconfig eth0 hw ether 00:AA:BB:CC:dd:EE
```

**配置 IP 地址：**

```shell
[root@localhost ~]# ifconfig eth0 192.168.2.10
[root@localhost ~]# ifconfig eth0 192.168.2.10 netmask 255.255.255.0
[root@localhost ~]# ifconfig eth0 192.168.2.10 netmask 255.255.255.0 broadcast 192.168.2.255
```

## iwconfig 命令

需要安装如下工具：

```shell
sudo apt install wireless-tools
```

iwconfig 系统配置无线网络设备或显示无线网络设备信息。iwconfig 命令类似于 ifconfig 命令，但是他配置对象是无线网卡，它对网络设备进行无线操作，如设置无线通信频段

```shell
iwconfig [interface]
```

- auto 自动模式
- essid 设置 ESSID
- nwid 设置网络 ID
- freq 设置无线网络通信频段
- chanel 设置无线网络通信频段
- sens 设置无线网络设备的感知阀值
- mode 设置无线网络设备的通信设备
- ap 强迫无线网卡向给定地址的接入点注册
- nick<名字> 为网卡设定别名
- rate<速率> 设定无线网卡的速率
- rts<阀值> 在传输数据包之前增加一次握手，确信信道在正常的
- power 无线网卡的功率设置

```shell
# 实例
iwconfig    # 显示无线网络配置
```

## wpa_supplicant 工具

wpa_supplicant 工具集，包括 wpa_supplicant*、*wpa_passphrase、wpa_cli

## dig

`dig`（Domain Information Groper）是一个用于查询 DNS（域名系统）信息的命令行工具。在 Linux 和其他 Unix-like 系统中，`dig` 是最常用的 DNS 查询工具之一。它可以用于查询域名的各种信息，如 IP 地址、MX 记录、NS 记录等。

`dig` 提供了比传统的 `nslookup` 更强大和灵活的功能，支持更多的查询选项、查询类型以及更详细的输出。

1. **基本语法**

   ```bash
   dig [@server] [name] [type] [options]
   ```

   - `@server`：指定要查询的 DNS 服务器。默认情况下，`dig` 会查询系统配置的 DNS 服务器。
   - `name`：要查询的域名。
   - `type`：查询类型（例如，A、MX、NS 等）。如果不指定，默认查询 A 记录。
   - `options`：一些附加选项，用于修改查询的行为或输出。

2. **常见查询类型**

   以下是 `dig` 支持的一些常见查询类型：

   - **A**：查询 IPv4 地址（默认查询类型）。
   - **AAAA**：查询 IPv6 地址。
   - **MX**：查询邮件交换记录（Mail Exchange）。
   - **NS**：查询域名服务器记录（Name Server）。
   - **CNAME**：查询别名记录（Canonical Name）。
   - **SOA**：查询授权记录（Start of Authority）。
   - **PTR**：查询反向 DNS 查找记录。
   - **TXT**：查询文本记录，常用于域名验证或 SPF 配置。

3. **常用选项**

   - `+short`：仅显示简洁的输出（例如，只显示 IP 地址）。
   - `+trace`：显示 DNS 查询的完整跟踪路径，查看从根服务器到目标服务器的所有查询过程。
   - `+all`：显示所有相关信息，包括查询的每个步骤和每个 DNS 记录。
   - `+noall +answer`：仅显示答案部分，过滤掉不相关的信息。
   - `+ndots=<num>`：指定域名解析时要求的最小点数，默认是 1。

4. **基本用法**

   1. 查询 A/MX/NS/CNAME/TXT/PTR/SOA 记录

      ```bash
      dig example.com      # 查询某个域名的 A 记录（IPv4 地址），默认情况下，dig 会查询 A 记录
      dig example.com MX   # 查询域名的 MX 记录（邮件交换服务器）
      dig example.com NS   # 查询域名的 NS 记录（域名服务器）
      dig www.example.com CNAME  # 查询域名的 CNAME 记录（别名记录）
      dig example.com TXT        # 查询域名的 TXT 记录（文本记录）
      dig example.com A MX NS    # 可以在同一个命令中查询多个记录， 这将同时查询 A、MX 和 NS 记录。
      dig -x 8.8.8.8       # 反向查询某个 IP 地址对应的域名，这将查询 IP 地址 8.8.8.8 对应的域名
      dig example.com SOA  # 查询一个域名的授权记录（SOA）
      ```

   2. 查询指定的 DNS 服务器

      如果你想要指定某个 DNS 服务器来执行查询，可以使用 `@` 来指定：

      ```bash
      dig @8.8.8.8 example.com
      ```

      这会使用 Google 的公共 DNS 服务器 `8.8.8.8` 来查询 `example.com` 的 A 记录。

   3. 选项使用

      ```bash
      # +trace：使用 `+trace` 查看从根 DNS 服务器到目标服务器的查询路径，这会显示详细的查询过程，包括所有递归查询
      dig +trace example.com
      # +short：如果你只关心简洁的输出，可以使用 `+short` 选项，这只会输出 IP 地址或其他查询的简洁结果
      dig example.com +short
      # +noall +answer：如果你只想查看答案部分，可以使用 `+noall +answer`，这会过滤掉其他部分，仅显示查询的答案
      dig example.com +noall +answer
      ```

5. **输出示例**

   以查询 `example.com` 的 A 记录为例，执行 `dig example.com` 后的输出通常包括以下几部分：

   - **QUESTION SECTION**：显示查询的目标域名和查询类型。
   - **ANSWER SECTION**：显示查询的结果（例如，`example.com` 的 IP 地址）。
   - **AUTHORITY SECTION**：显示负责该域名的授权 DNS 服务器。
   - **ADDITIONAL SECTION**：可能会显示额外的相关信息。

6. **常见用途**

- **检查域名是否解析正常**：使用 `dig` 可以快速确认某个域名是否能够正确解析为 IP 地址。
- **诊断 DNS 问题**：当出现 DNS 问题时，`dig` 可帮助分析域名解析过程，确认 DNS 配置是否正确。
- **了解 DNS 记录**：你可以通过 `dig` 查询各类 DNS 记录，获取域名的详细配置信息。

**总结**：

`dig` 是一个非常强大的 DNS 查询工具，适用于从简单的域名解析查询到复杂的 DNS 配置分析。通过灵活的查询类型和选项，它可以帮助你全面了解 DNS 配置、调试 DNS 问题并进行网络故障排查。

# 程序分析命令

## ldd

(list dynamic dependencies)

# 网络协议命令

## curl 命令

> [curl 的用法指南](https://www.ruanyifeng.com/blog/2019/09/curl-reference.html)
>
> [curl 命令详解](https://handerfly.github.io/linux/2019/05/26/curl%E5%91%BD%E4%BB%A4%E8%AF%A6%E8%A7%A3/)
>
> [Linux curl 命令详解](https://www.cnblogs.com/duhuo/p/5695256.html)

`curl` 命令是一个功能强大的网络工具，它的名字就是客户端（client）的 URL 工具的意思。它能够通过 http、ftp 等方式下载文件，也能够上传文件，同时支持 HTTPS 等众多协议，还支持 POST、cookies、认证、从指定偏移处下载部分文件、用户代理字符串、限速、文件大小、进度条等特征。其实 curl 远不止前面所说的那些功能，大家可以通过 man curl 阅读手册页获取更多的信息。

类似的工具还有 wget。

常用参数 curl 命令参数很多，这里只列出 shell 脚本中经常用到过的那些。

```shell
-a/--append 上传文件时，附加到目标文件

-A:随意指定自己这次访问所宣称的自己的浏览器信息

-b/--cookie <name=string/file> cookie字符串或文件读取位置，使用option来把上次的cookie信息追加到http request里面去。

-c/--cookie-jar <file> 操作结束后把cookie写入到这个文件中

-C/--continue-at <offset>  断点续转

-d/--data <data>   HTTP POST方式传送数据

    --data-ascii <data> 以ascii的方式post数据
     --data-binary <data> 以二进制的方式post数据
     --negotiate 使用HTTP身份验证
     --digest 使用数字身份验证
     --disable-eprt 禁止使用EPRT或LPRT
     --disable-epsv 禁止使用EPSV
-D/--dump-header <file> 把header信息写入到该文件中

     --egd-file <file>  为随机数据(SSL)设置EGD socket路径

     --tcp-nodelay     使用TCP_NODELAY选项

-e/--referer <URL>  指定引用地址

-F/--form <name=content>   模拟http表单提交数据

     --form-string <name=string> 模拟http表单提交数据

-G/--get    以get的方式来发送数据

-H/--header <header> 指定请求头参数

    --ignore-content-length  忽略的HTTP头信息的长度

-i/--include     输出时包括protocol头信息

-I/--head 仅返回头部信息，使用HEAD请求

-k/--insecure  允许不使用证书到SSL站点

-K/--config    指定的配置文件读取

-l/--list-only   列出ftp目录下的文件名称

    --limit-rate <rate> 设置传输速度

     --local-port<NUM>  强制使用本地端口号

-m/--max-time <seconds> 指定处理的最大时长

     --max-redirs <num>    设置最大读取的目录数

     --max-filesize <bytes>  设置最大下载的文件总量

-o/--output <file>   指定输出文件名称

-O/--remote-name  把输出写到该文件中，保留远程文件的文件名



-v/--verbose  小写的v参数，用于打印更多信息，包括发送的请求信息，这在调试脚本是特别有用。

-s/--slient 减少输出的信息，比如进度

--connect-timeout <seconds> 指定尝试连接的最大时长

-x/--proxy <proxyhost[:port]> 指定代理服务器地址和端口，端口默认为1080


-u/--user <user[:password]>设置服务器的用户和密码

-r/--range <range>检索来自HTTP/1.1或FTP服务器字节范围

   --range-file 读取（SSL）的随机文件

-R/--remote-time   在本地生成文件时，保留远程文件时间

    --retry <num>   指定重试次数

    --retry-delay <seconds>   传输出现问题时，设置重试间隔时间

    --retry-max-time <seconds>  传输出现问题时，设置最大重试时间

-s/--silent  静默模式。不输出任何东西

-S/--show-error  显示错误

    --socks4 <host[:port]> 用socks4代理给定主机和端口

    --socks5 <host[:port]> 用socks5代理给定主机和端口

    --stderr <file>

-x/--proxy <host[:port]> 在给定的端口上使用HTTP代理

-X/--request <command> 指定什么命令。curl默认的HTTP动词是GET，使用-X参数可以支持其他动词。

-T/--upload-file <file> 指定上传文件路径
```

## wget 命令

## scp 命令

> [Docs » 工具参考篇 » 18. scp 跨机远程拷贝](https://linuxtools-rst.readthedocs.io/zh-cn/latest/tool/scp.html)
> 帮助文档：`man scp`

scp 是 secure copy 的简写，用于在 Linux 下进行远程拷贝文件的命令，和它类似的命令有 cp，不过 cp 只是在本机进行拷贝不能跨服务器，而且 scp 传输是加密的。当你服务器硬盘变为只读 read only system 时，用 scp 可以帮你把文件移出来。

> :page_with_curl: **注解：**
> 类似的工具有 rsync；scp 消耗资源少，不会提高多少系统负荷，在这一点上，rsync 就远远不及它了。rsync 比 scp 会快一点，但当小文件多的情况下，rsync 会导致硬盘 I/O 非常高，而 scp 基本不影响系统正常使用。

**命令格式**：

```bash
scp [参数] [原路径] [目标路径]
```

**命令参数**：

- `-1` 强制 scp 命令使用协议 ssh1
- `-2` 强制 scp 命令使用协议 ssh2
- `-4` 强制 scp 命令只使用 IPv4 寻址
- `-6` 强制 scp 命令只使用 IPv6 寻址
- `-B` 使用批处理模式（传输过程中不询问传输口令或短语）
- `-C` 允许压缩。（将-C 标志传递给 ssh，从而打开压缩功能）
- `-p` 留原文件的修改时间，访问时间和访问权限。
- `-q` 不显示传输进度条。
- `-r` 递归复制整个目录。
- `-v` 详细方式显示输出。scp 和 ssh(1)会显示出整个过程的调试信息。这些信息用于调试连接，验证和配置问题。
- `-c` cipher 以 cipher 将数据传输进行加密，这个选项将直接传递给 ssh。
- `-F` ssh_config 指定一个替代的 ssh 配置文件，此参数直接传递给 ssh。
- `-i` identity_file 从指定文件中读取传输时使用的密钥文件，此参数直接传递给 ssh。
- `-l` limit 限定用户所能使用的带宽，以 Kbit/s 为单位。
- `-o` ssh_option 如果习惯于使用 ssh_config(5)中的参数传递方式，
- `-P` port 注意是大写的 P, port 是指定数据传输用到的端口号
- `-S` program 指定加密传输时所使用的程序。此程序必须能够理解 ssh(1)的选项。

**使用示例**：

1. **从本地拷贝文件到远程服务器**：

   ```bash
   scp /path/to/local/file username@remote_host:/path/to/remote/directory
   scp /path/to/local/file remote_host:/path/to/remote/directory

   # 例如，把本地的 `file.txt` 拷贝到远程服务器的 `/home/user/` 目录：
   scp file.txt user@192.168.1.10:/home/user/
   ```

   指定了用户名，命令执行后需要输入用户密码；如果不指定用户名，命令执行后需要输入用户名和密码；

2. **从远程服务器拷贝文件到本地**：

   ```bash
   scp username@remote_host:/path/to/remote/file /path/to/local/directory

   # 例如，从远程服务器的 `/home/user/` 目录下载 `file.txt` 到本地：
   scp user@192.168.1.10:/home/user/file.txt /path/to/local/directory
   ```

3. **递归拷贝目录**： 使用 `-r` 选项，可以拷贝整个目录：

   ```bash
   scp -r /path/to/local/directory username@remote_host:/path/to/remote/directory
   ```

4. **指定端口号**： 如果远程服务器的 SSH 服务运行在非标准端口（例如 10086），你可以通过 `-P` 选项指定端口：

   ```bash
   scp -P 10086 file.txt user@192.168.1.10:/home/user/
   ```

5. **使用 SSH 密钥文件**： 如果你需要使用 SSH 密钥进行认证，可以使用 `-i` 选项指定密钥文件：

   ```bash
   scp -i /path/to/private_key file.txt user@192.168.1.10:/home/user/
   ```

6. **显示详细信息**： 使用 `-v` 选项来查看详细的传输过程：

   ```bash
   scp -v file.txt user@192.168.1.10:/home/user/
   ```

7. **启用压缩**： 使用 `-C` 选项来启用压缩，以加快大文件的传输速度：

   ```bash
   scp -C largefile.zip user@192.168.1.10:/home/user/
   ```

`scp` 是一个非常方便且安全的工具，适用于快速传输文件。如果你有需要使用 SSH 协议进行文件传输的场景，`scp` 可以高效地帮助你完成工作。

## rsync 命令

`rsync` 是一个强大的文件同步和传输工具，通常用于在本地或远程主机之间同步文件和目录。它的主要优势是**支持增量备份和高效的数据传输**，能够只传输已更改的部分数据，而不必每次都传输完整的文件。

**基本语法：**

```bash
rsync [选项] 源路径 目标路径
```

> - 源目录后不加斜杠 `/`：将<font color=red>整个目录</font>（包括其名称）复制到目标目录中。
> - 源目录后加斜杠 `/`：将<font color=red>源目录中的内容</font>复制到目标目录，而不复制源目录本身。

**常见用法：**

1. **本地文件同步**

   将本地文件或目录同步到另一个本地目录。

   ```bash
   rsync -av /path/to/source/ /path/to/destination/
   ```

   - `-a`：归档模式，表示递归复制文件并保持文件的权限、时间戳等属性。
   - `-v`：显示详细输出。

   例如，将 `/home/user/source/` 目录中的内容同步到 `/home/user/destination/` 目录：

   ```bash
   rsync -av /home/user/source/ /home/user/destination/
   ```

2. **远程同步**

   `rsync` 还可以通过 SSH 连接到远程服务器，将文件从本地复制到远程服务器，或将远程服务器的文件同步到本地。

   - 从本地复制到远程服务器：

   ```bash
   rsync -av /path/to/source/ user@remote_host:/path/to/destination/
   ```

   - 从远程服务器复制到本地：

   ```bash
   rsync -av user@remote_host:/path/to/source/ /path/to/destination/
   ```

   其中：

   - `user`：远程服务器的用户名。
   - `remote_host`：远程主机的 IP 地址或域名。

3. **增量备份**

   `rsync` 的一个重要功能是增量备份，它只会复制自上次同步以来发生变化的文件。这是通过记录每个文件的修改时间和大小来实现的。

   ```bash
   rsync -av --delete /path/to/source/ /path/to/destination/
   ```

   - `--delete`：删除目标目录中在源目录中不存在的文件。这通常用于保持目标目录与源目录的完全一致。

4. **排除某些文件或目录**

   如果你希望同步时排除某些文件或目录，可以使用 `--exclude` 选项。

   ```bash
   rsync -av --exclude 'pattern' /path/to/source/ /path/to/destination/
   ```

   例如，要排除 `.git/` 目录：

   ```bash
   rsync -av --exclude '.git/' /path/to/source/ /path/to/destination/
   ```

   你还可以使用 `--exclude-from` 选项，指定一个文件，**该文件列出了多个排除模式**。

   ```bash
   rsync -av --exclude-from 'exclude_list.txt' /path/to/source/ /path/to/destination/
   ```

5. **同步指定文件**

   如果只想同步特定文件，可以指定文件路径。例如，将某个文件从本地同步到远程服务器：

   ```bash
   rsync -av /path/to/local/file.txt user@remote_host:/path/to/remote/destination/
   ```

6. **使用 SSH 进行加密传输**

   `rsync` 默认使用 SSH 协议进行远程文件传输。如果你希望指定一个自定义的 SSH 端口，可以使用 `-e` 选项来设置 SSH 的命令。

   ```bash
   rsync -av -e 'ssh -p 2222' /path/to/source/ user@remote_host:/path/to/destination/
   ```

**常见选项：**

| 选项             | 描述                                                                             |
| ---------------- | -------------------------------------------------------------------------------- |
| `-a`             | 归档模式，表示递归复制并保持文件的权限、时间戳等属性                             |
| `-v`             | 显示详细输出                                                                     |
| `-z`             | 压缩文件数据，减少传输数据量                                                     |
| `-r`             | 递归复制整个目录                                                                 |
| `-u`             | 仅复制源文件比目标文件新的文件                                                   |
| `-l`             | 保留符号链接                                                                     |
| `-t`             | 保留时间戳                                                                       |
| `-p`             | 保留文件权限                                                                     |
| `-P`             | 启用 --partial 和 --progress，在文件传输过程中显示进度，并保留已传输的部分文件。 |
| `-g`             | 保留文件的组信息                                                                 |
| `-o`             | 保留文件的拥有者信息                                                             |
| `-x`             | 防止跨文件系统，限制同步到单一文件系统                                           |
| `--delete`       | 删除目标目录中源目录没有的文件                                                   |
| `--exclude`      | 排除匹配的文件或目录                                                             |
| `--exclude-from` | 从指定文件中读取排除规则                                                         |
| `--progress`     | 显示传输进度                                                                     |
| `-e`             | 使用自定义远程 shell（例如 SSH）进行传输                                         |
| `-h`             | 以易读的格式显示文件大小（例如 KB、MB、GB）                                      |
| `--dry-run`      | 模拟同步过程，但不实际执行任何操作                                               |

**高级用法：**

1. **限制带宽使用**

   如果你希望限制 `rsync` 使用的带宽，可以使用 `--bwlimit` 选项。例如，限制带宽为 1MB/s：

   ```bash
   rsync -av --bwlimit=1024 /path/to/source/ user@remote_host:/path/to/destination/
   ```

2. **比较文件**

   使用 `--itemize-changes` 选项可以显示文件同步时的变化：

   ```bash
   rsync -av --itemize-changes /path/to/source/ /path/to/destination/
   ```

   该命令会输出详细的文件变化信息，类似于：

   ```shell
   >f+++++++++ file1
   >f+++++++++ file2
   ```

3. **使用 `rsync` 进行镜像同步**

   如果你想将一个目录完全复制到另一个位置，并删除目标位置中不再存在的文件，可以使用以下命令：

   ```bash
   rsync -av --delete /path/to/source/ /path/to/destination/
   ```

4. **只同步文件的元数据**

   如果你只关心文件的时间戳和权限等元数据，不需要同步文件内容，可以使用 `-c`（--checksum）选项，通过比较文件校验和来确定是否需要同步文件。

   ```bash
   rsync -avc /path/to/source/ /path/to/destination/
   ```

**例子：**

1. **将本地目录 `/data/` 同步到远程服务器：**

   ```bash
   rsync -avz /data/ user@remote_host:/backup/
   ```

   - `-z`：启用数据压缩，以减少传输时间。

2. **从远程服务器同步目录并排除 `.log` 文件：**

   ```bash
   rsync -av --exclude='*.log' user@remote_host:/data/ /backup/
   ```

3. **使用 SSH 自定义端口进行同步：**

   ```bash
   rsync -av -e 'ssh -p 2222' /data/ user@remote_host:/backup/
   ```

4. **在本地和远程服务器之间进行增量备份：**

   ```bash
   rsync -av --delete /data/ user@remote_host:/backup/
   ```

5. **模拟执行而不实际同步：**

   ```bash
   rsync -av --dry-run /data/ user@remote_host:/backup/
   ```

**总结：**

`rsync` 是一个非常高效、灵活的工具，适用于文件同步、备份和远程传输。它能够处理本地和远程文件的增量同步，并通过多种选项提供高效的数据传输、压缩、排除和文件比较等功能。通过合理配置和选择选项，`rsync` 可以极大地简化和加速大规模数据的同步任务。

## ssh-keygen

> [ssh-keygen](http://linux.51yip.com/search/ssh-keygen)

ssh-keygen 用于为 ssh(1)生成、管理和转换认证密钥，包括 RSA 和 DSA 两种密钥。**密钥类型可以用 -t 选项指定**。如果没有指定则默认生成用于 SSH-2 的 RSA 密钥。

通常，这个程序产生一个密钥对，并要求**指定一个文件存放私钥**，同时将公钥存放在附加了".pub"后缀的同名文件中。

程序同时要求输入一个密语字符串(passphrase)，空表示没有密语(主机密钥的密语必须为空)。

密语和口令(password)非常相似，但是密语可以是一句话，里面有单词、标点符号、数字、空格或任何你想要的字符。好的密语要 30 个以上的字符，难以猜出，由大小写字母、数字、非字母混合组成。密语可以用 -p 选项修改。丢失的密语不可恢复。如果丢失或忘记了密语，用户必须产生新的密钥，然后把相应的公钥分发到其他机器上去。

RSA1 的密钥文件中有一个**"注释"字段**，可以方便用户标识这个密钥，指出密钥的用途或其他有用的信息。创建密钥的时候，注释域初始化为"user@host"，以后可以用 -c 选项修改。

```shell
 -C comment 提供一个新注释
 -f filename 指定密钥文件名。(要输入完整路劲，否则在当前路径下生成)
-P passphrase 提供(旧)密语。
-t type  指定要创建的密钥类型。可以使用："rsa1"(SSH-1) "rsa"(SSH-2) "dsa"(SSH-2)

ssh-keygen -t rsa -C "user@host" -f "id_rsa_user@host"
```

## ssh 命令

> 参考：
>
> ```shell
> man ssh
> ```

Linux 一般作为服务器使用，而服务器一般放在机房，你不可能在机房操作你的 Linux 服务器。

这时我们就需要远程登录到 Linux 服务器来管理维护系统。

Linux 系统中是通过 ssh 服务实现的远程登录功能，默认 ssh 服务端口号为 22。

SSH 为 Secure Shell 的缩写，由 IETF 的网络工作小组（Network Working Group）所制定。

SSH 为建立在应用层和传输层基础上的安全协议。

```shell
ssh [-46AaCfGgKkMNnqsTtVvXxYy] [-B bind_interface]
    [-b bind_address] [-c cipher_spec] [-D [bind_address:]port]
    [-E log_file] [-e escape_char] [-F configfile] [-I pkcs11]
    [-i identity_file] [-J [user@]host[:port]] [-L address]
    [-l login_name] [-m mac_spec] [-O ctl_cmd] [-o option] [-p port]
    [-Q query_option] [-R address] [-S ctl_path] [-W host:port]
    [-w local_tun[:remote_tun]] destination [command [argument ...]]
```

ssh connects and logs into the specified destination, which may be specified as either `[user@]hostname` or a URI of the form
`ssh://[user@]hostname[:port]`. The user must prove their identity to the remote machine using one of several methods (see below).

常用登录命令：

```shell
ssh -p 22 my@127.0.0.1
# 输入密码：
```

**-p** 后面是端口

**my** 是服务器用户名

**127.0.0.1** 是服务器 ip

回车输入密码即可登录

### ssh 免密登录

参考链接：

1. [设置 SSH 通过秘钥登录](https://www.runoob.com/w3cnote/set-ssh-login-key.html)
2. [ssh 免密登录配置方法及配置](https://blog.csdn.net/weixin_44966641/article/details/123955997) ----主要
3. [VSCode——SSH 免密登录](https://blog.csdn.net/qq_45779334/article/details/129308235?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ECtr-2-129308235-blog-123031276.235%5Ev43%5Epc_blog_bottom_relevance_base3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ECtr-2-129308235-blog-123031276.235%5Ev43%5Epc_blog_bottom_relevance_base3&utm_relevant_index=4) ----主要
4. [连接远程服务器总是要输入密码（rsa 验证无用）](https://www.cnblogs.com/coldchair/p/18760176)
5. [git/ssh 捋不清的几个问题](https://www.barretlee.com/blog/2014/03/11/cb-problems-in-git-when-ssh/)
6. [解决使用两台主机的 VSCode 远程连接同一个服务器账户出现的配置冲突问题](https://blog.csdn.net/holyball/article/details/130109637)

配置流程：

1. **生成秘钥对**

   在本地机器上生成公钥、私钥：（一路回车默认即可）

   ```shell
   # 自行查阅命令参数，-t 秘钥类型；-C 注释；-f 生成文件名；
   # 最好先进入 `~/.ssh` 目录，这样文件直接生成在这个目录下。
   ssh-keygen -t rsa -C "xxx" -f "path/id_rsa_xxx"
   ```

   可以在 `~/.ssh` 目录下看到两个秘钥文件，即我们刚生成的私钥 `iid_rsa_xxx` 和公钥 `iid_rsa_xxx.pub`（具体名称取决于你的命名）。

2. **上传公钥到服务器**

   在本地机器上生成秘钥对之后，需要将公钥 `iid_rsa_xxx.pub` 中的内容放到对应服务器上的 `~/.ssh/authorized_keys` 文件中，此步有 2 种方式：

   ```shell
   # 1.通过 ssh-copy-id 命令，命令有点类似 scp，需要输入密码
   ssh-copy-id -i /path/id_rsa_xxx.pub user@host

   # 2.手动将直接将公钥文件内容拷贝到服务器的 ~/.ssh/authorized_keys 文件中，没有文件则创建文件
   ```

3. **文件权限配置**

   - ssh 密钥登录时，用户的 `~/.ssh` 目录及其内部文件（如 `authorized_keys`）的权限设置必须严格（安全性考虑），**否则 SSH 认证会失败**。
   - 用户 Home 目录的权限过于宽松**也会导致 SSH 无法正常使用密钥认证**。该目录权限应该为 `755（drwxr-xr-x）`。

   ```shell
   # 设置 `～/.ssh` 和 `~/.ssh/authorized_keys` 权限
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys

   # 用户 Home 目录权限为755
   chmod 755 xxx/xxx
   ```

   > :page*with_curl: **Note**
   > 如果权限设置不对，在配对秘钥的时候会无法打开 authorized_keys 文件从而导致秘钥配对失败。而 ssh 此时没有放弃连接，依然会尝试询问用户密码。最终产生的结果就是用户配置了公钥却仍然需要输入密码的问题。导致费了很大功夫才找到问题 `-*-!!!`。
   >
   > :warning: 设置 ssh 路径下的权限，以及 Home 目录权限（重要！）---- 本人未设置
   >
   > [vscode 在 remote SSH 免密远程登录](https://blog.csdn.net/weixin_42907822/article/details/125237307)

4. **修改 SSH 服务器的配置文件**

确保 SSH 配置文件 `/etc/ssh/sshd_config` 允许公钥认证。你需要检查以下设置：

```shell
# /etc/ssh/sshd_config 文件中
PubkeyAuthentication yes # 把#号去掉（默认在39行附近），这样公钥验证才生效。
```

重启远程服务器的 ssh 服务

```shell
service ssh start
```

5.  **本地 SSH 连接配置**

SSH 使用 `~/.ssh/config` 文件来配置 SSH 连接。在文件中新增一份如下配置：

```shell
Host xxx-xxx
  HostName xxx.xxx.xxx.xxx
  Port 22
  User root
  IdentityFile ~/.ssh/id_rsa_xxx
```

如果这个文件没有正确配置，或者你没有在该文件中指定正确的 SSH 密钥，可能会导致无法识别密钥，从而要求输入密码。

:book: **补充**
**ssh config 配置文件的基本格式**

```shell
Host      # hostName的别名
  HostName  # 是目标主机的主机名，也就是平时我们使用ssh后面跟的地址名称。
  Port   # 指定的端口号。
  User   # 指定的登陆用户名。
  IdentifyFile # 指定的私钥地址。
  ProxyJump ProxyJump user@jump_host:port # 跳板机的用户名、主机地址、端口
```

> - 不要加 PreferredAuthentications publickey，否则连接远程服务器上 docker 时，会报错 **Connection refused**。<font color=red><b>被坑死了 -\_-!!!</b></font>

6.  测试免密登录

### ssh 远程连接 docker

> [设置 SSH 远程连接 docker 容器](https://www.cnblogs.com/luochunxi/p/16699704.html)

```shell
# 1.创建容器，默认是root用户，需自定义<>中内容
# `host` 模式 `-p` 选项不需要，因为 `host` 模式下容器直接使用宿主机的网络栈，端口是共享的。
docker run -d \
    -it \
    --privileged \
    -h <hostname> \
    --restart always \
    --network host \
    --name <dockername> \
    -v /data/<path>:/data/<path> \
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
    --name <dockername> \
    -v /data/<path>:/data/<path> \
    IMAGE \
    /bin/bash

# 2.进入容器
docker exec -it <docker_name> bash

# 3.设置密码，修改容器的root密码
passwd
密码设置为：123456

# 4.安装 ssh
apt-get update
apt-get install openssh-server -y

# 5.查看 ssh 是否启动
ps -e | grep ssh # 有sshd,说明ssh服务已经启动。如果没有启动，输入`service ssh start`启动服务

# 6.修改配置，
# 打开配置文件`/etc/ssh/sshd_config`
PermitRootLogin yes  # 原文件为`PermitRootLogin without-password`，需要改成左边，没有就新增
Port 22  # 可能原文件为`#Port 22`，即默认放开 22 端口给 ssh 用。
Port xxx # 如果 docker run 用的是 host 模式，这里直接指定一个合法端口给 ssh 用就可以，如 10086，宿主机和 docker 都是用这个端口，注意不要冲突。如果 docker run 命令中为 bridge 模式（默认）且用 -p <host_port>:<container_port>的<container_port>为22，此处`Port 22`；若<container_port>为其他值如10086，则此处需要改成`Port 10086`。放开多个端口需同时添加多条`Port xxx`。

# 7.启动 ssh，重启用`service ssh restart`
service ssh start
# 开机自动启动ssh命令
sudo systemctl enable ssh

# 8.ssh远程登录上述创建的容器
# 注意这里要用 root 用户登录
ssh root@xx.xx.xx.xx -p <port>
```

> NOTE：
>
> 一定要检查 `~/.ssh/config` 文件，不要添加 PreferredAuthentications publickey，否则连接远程服务器上 docker 时，会报错 **Connection refused**。
>
> `<font color=red>`被坑死了 -\_\_-!!!`</font>`
>
> ```shell
> # 上面步骤修改配置文件`/etc/ssh/sshd_config`时，部分 wiki 说要放开下面配置，实测未放开也可以，未深究
> PasswordAuthentication yes
> ```

### ssh 启动报错

如果 ssh 启动报错：

```shell
Badly formatted port number
```

说明 `/etc/ssh/sshd_config` 中端口号有问题，改正默认值 22，然后重启 ssh 服务即可。如

```shell
# 打开文件 /etc/ssh/sshd_config，将 Port 改成22
Port 22

# 重启 ssh 服务
service ssh start
```
