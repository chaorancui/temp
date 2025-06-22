[toc]

# 系统设备命令

## lspci 命令

`lspci` 是 Linux 下用于列出所有 PCI 总线设备（如显卡、声卡、网卡等）信息的命令。它能显示设备的多种信息，但**显示的内容取决于命令参数和系统数据库的完整性**。`lspci` 的识别信息来自 `/usr/share/misc/pci.ids` 数据库，推荐更新该数据库以识别更多设备 `sudo update-pciids`。

**一、一般默认信息（无参数 `lspci`）**

```bash
00:14.3 Network controller: Intel Corporation Cannon Lake PCH CNVi WiFi (rev 10)
```

包括：

- **总线地址**（如 `00:14.3`）
- **设备类型**（如 `Network controller`）
- **厂商和设备名称**（如 `Intel Corporation Cannon Lake PCH CNVi WiFi`）
- **修订版本**（如 `rev 10`）

**二、更详细的信息（`-v`、`-vv` 或 `-vvv`）**

```bash
lspci -vv
```

包括：

- **设备状态**（启用/禁用）
- **I/O 端口地址**
- **内存映射范围**
- **中断号（IRQ）**
- **内核驱动（使用哪个驱动）**
- **内核模块（可用模块）**
- **延迟（Latency）**
- **设备控制能力（例如 Message Signaled Interrupts）**
- **能力列表（Capabilities，如 PCIe Capabilities）**

**三、显示内核驱动信息（`-k`）**

```bash
lspci -k
```

包括：

- **内核使用的驱动程序**
- **已加载的内核模块**
- **可用的其他模块**

示例：

```log
Kernel driver in use: iwlwifi
Kernel modules: iwlwifi
```

**四、显示原始 ID 数字（`-n`、`-nn`）**

```bash
lspci -nn
```

显示厂商 ID 和设备 ID，例如：

```log
00:14.3 Network controller [0280]: Intel Corporation Cannon Lake PCH CNVi WiFi [8086:9df0] (rev 10)
```

- `8086`：Intel 的 PCI vendor ID
- `9df0`：设备 ID

**五、能力结构（`-vvv` + Capabilities）**

包括：

- **PCI Express 链路速度和宽度**
- **电源管理支持**
- **热插拔能力**
- **MSI / MSI-X 中断支持**
- **原子操作能力**

**六、实用组合命令推荐**

```bash
lspci -nnk         # 查看厂商/设备ID + 驱动
lspci -vvv         # 超详细版本
lspci -nn | grep -i eth     # 筛选网卡设备
lspci -nn | grep -i nvidia  # 筛选显卡设备
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

1. `iw`（现代工具，**替代 iwconfig**）：更全面地管理无线设备，支持查看频段、连接状态、功率等高级信息。
2. `ip`（现代工具，**替代 ifconfig**）：管理网络接口状态（启用、禁用）、分配 IP 地址等。
3. `nmcli`（NetworkManager 的命令行工具）：管理网络连接（包括 Wi-Fi 和以太网），常用于桌面 Linux 发行版（如 Ubuntu）
4. `wpa_supplicant`（低层连接工具，适用于嵌入式/无 GUI 系统）：管理 WPA/WPA2 连接，是 Wi-Fi 连接的底层工具。通常和配置文件搭配使用。
5. `rfkill`（软/硬件屏蔽无线模块）：启用或禁用无线功能（如 Wi-Fi、蓝牙）

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

## iw 命令

全称 `interface wireless`，支持现代内核（2.6.30+）中的 **nl80211** 驱动接口，适用于现代 Wi-Fi 功能，如 802.11n/ac/ax，管理接口、扫描网络、信道设置等，**已取代旧的 `iwconfig` 工具**。

**注**：

- `iw`：用于查看/管理无线网卡和**射频相关特性**（scan、channel、txpower 等），并不负责设置接口状态为 up/down，它关注的是 Wi-Fi 的无线功能。
- `ip link`：用于启用/禁用**网络接口本身**（包括无线和有线）

安装：

```bash
apt install iw
```

**一、基本语法结构**

```bash
iw [ options ] dev <interface> <command> [args]
```

**二、常用参数说明**

1. `dev`：指定接口名称（如 wlan0）

2. `phy`：指定物理无线设备（如 phy0）

3. `reg`：查看和设置无线国家/区域代码（影响频段可用性）

4. `help`：查看帮助文档

**三、常用命令分类详解**

1. 查看无线设备信息

   ```bash
   iw dev                  # 列出所有无线接口及状态
   iw phy                  # 列出所有物理无线设备
   iw list                 # 显示驱动和设备支持的功能（如 HT/VHT）
   ```

2. 扫描无线网络

   ```bash
   iw dev wlan0 scan
   ```

   - 会扫描所有可用 AP（Access Point），显示 SSID、信道、信号强度等。（要先保证设备启用 `ip link set wlan0 up`）

   示例输出：

   ```log
   SSID: MyWiFi
   signal: -45 dBm
   frequency: 2412 MHz
   ```

3. 查看连接状态

   ```bash
   iw dev wlan0 link
   ```

   - 查看当前连接的 Wi-Fi 信息，如连接的 AP、信号强度、速率等。

4. 断开连接

   ```bash
   iw dev wlan0 disconnect
   ```

   - 手动断开当前 Wi-Fi 连接。

5. 设置接口类型

   ```bash
   iw dev wlan0 set type managed     # 设置为客户端（常规连接路由器）
   iw dev wlan0 set type monitor     # 设置为监听模式（抓包等）
   iw dev wlan0 set type ibss        # 设置为 Ad-Hoc 模式
   ```

   > 注：改类型前需先关闭接口：`ip link set wlan0 down`

6. 设置信道

   ```bash
   iw dev wlan0 set channel 6        # 设置到信道6
   iw dev wlan0 set freq 2412        # 设置到2.4GHz频段的2412MHz
   ```

7. 设置国家代码（Region）

   ```bash
   iw reg get                        # 查看当前国家设置
   iw reg set US                    # 设置国家为美国（可能解锁更多信道）
   ```

8. 修改传输功率

   ```bash

   iw dev wlan0 set txpower fixed 2000    # 设置为20 dBm（= 100mW）
   ```

9. 帮助信息

   ```bash
   iw help
   iw dev help
   ```

**四、iw 输出太长怎么办**

结合 `grep`、`less`、`awk` 等使用：

```bash
iw dev wlan0 scan | grep SSID
iw dev wlan0 scan | less
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

## 有线网络与无线网络

- **有线网卡**是基于电信号传输的物理链路，不存在射频模块。
- **无线网卡**具备：

  - 天线 + 射频模块
  - 调制/解调 + 频段配置（2.4GHz / 5GHz）
  - 受限于无线法规与功率控制

**一、有线网卡与无线网卡的控制层级对比**

| 功能          | 有线网卡                      | 无线网卡                          |
| ------------- | ----------------------------- | --------------------------------- |
| `up/down`     | 支持，打开/关闭接口，允许连接 | 支持，打开/关闭接口，允许链路协商 |
| 自动检测连接  | 插线自动检测                  | 需手动连接 SSID                   |
| 射频/信道设置 | 无                            | 支持                              |
| 认证连接      | 无（即插即通）                | WPA/WPA2/WPA3 等                  |
| 加密/握手流程 | 无                            | 是                                |

**无线网络接口**（如 WIFI）既有 `up/down` 状态，也有 `connect/disconnect` 逻辑，因为其接口就绪后，需要手动指定 SSID 进行认证连接。
**有线网络接口**（如 Ethernet）也有 `up/down` 状态，但没有 `connect/disconnect` 逻辑，因为其接口就绪后，自动就可协商连接。

**二、`up/down` 含义**

| 状态   | 含义说明                               |
| ------ | -------------------------------------- |
| `up`   | 打开网卡，使其监听链路，尝试协商连接等 |
| `down` | 关闭网卡，不再进行任何链路侦测与通信   |

都通过 `ip link` 命令控制：

```bash
ip link set eno1 up
ip link set eno1 down
```

但从**用户空间或软件层面**来看，有线网卡**没有“connect”命令或过程**，而是：

- 插上网线 → 网卡自动检测链路（link negotiation）
- 链路协商成功 → 自动进入 `CONNECTED` 状态（自动完成）

**三、有线网络判断是否连接（链路状态）：**

```bash
cat /sys/class/net/eno1/carrier
```

- `1` 表示物理链路已连接（网线已插好）
- `0` 表示物理链路未连接（网线拔出或另一端未启用）

也可以用：

```bash
ethtool eno1 | grep "Link detected"
```

**四、配置差异**

- 无线：

  ```bash
  ip link set wlo1 up             # 开启接口（供电、驱动）
  iw dev wlo1 scan                # 扫描可用 Wi-Fi（需要 up）
  wpa_supplicant ...             # 执行连接（connect）
  ```

- 有线：

  ```bash
  ip link set eno1 up            # 插网线自动协商 link
  dhclient eno1                  # 获取 IP 即可（不需要 connect）
  ```

## 无线网络的启用与连接

理解**网络接口的 `up/down`** 与 **Wi-Fi 的 `connect/disconnect`** 是理解 Linux 无线网络配置的基础。

**一、网络接口的 `up` / `down`（由 `ip link` 控制）**

含义：

- `up` ： 打开网卡，使其监听链路，尝试协商连接等
- `down` ： 关闭网卡，不再进行任何链路侦测与通信

控制命令：

```bash
ip link set wlo1 up      # 启用接口
ip link set wlo1 down    # 禁用接口
```

效果：

- `up`：网卡开始工作，能参与扫描、连接等操作
- `down`：网卡彻底关闭，不能连接、不能扫描，所有配置失效

二、**Wi-Fi 的 `connect` / `disconnect`（由 `wpa_supplicant` 或 `nmcli` 控制）**

含义：

- **`connect`**：尝试加入一个 Wi-Fi 网络（例如连接某个 SSID）
- **`disconnect`**：断开当前的 Wi-Fi 网络连接（但接口仍然是 up）

控制命令示例：

1. 使用 `wpa_cli`：

   ```bash
   wpa_cli -i wlo1 disconnect   # 断开 Wi-Fi
   wpa_cli -i wlo1 reconnect    # 重连上次 Wi-Fi
   ```

2. 使用 `nmcli`：

   ```bash
   nmcli device wifi connect "MyWiFi" password "mypass"
   nmcli device disconnect wlo1
   ```

**三、举个例子帮助理解**

| 项目                | `up/down`                        | `connect/disconnect`                 |
| ------------------- | -------------------------------- | ------------------------------------ |
| 控制范围            | 网卡接口                         | 无线连接                             |
| 控制方式            | `ip link`, `ifconfig`            | `wpa_cli`, `wpa_supplicant`, `nmcli` |
| 是否涉及 Wi-Fi 连接 | ❌ 不涉及连接                    | ✅ 直接控制 Wi-Fi 是否连接           |
| 典型影响            | 关闭/打开接口、禁用驱动          | 接口仍然工作，仅断开 Wi-Fi           |
| 执行优先级          | 必须先 `up` 接口，才能连接 Wi-Fi | 连接前提是接口已经 `up`              |

WIFI 状态：

| 状态 | 接口是否 UP | 是否连接 Wi-Fi | 能否联网 | 举例描述                     |
| ---- | ----------- | -------------- | -------- | ---------------------------- |
| A    | DOWN        | 无             | 否       | 网卡未启用，设备处于断电状态 |
| B    | UP          | 无             | 否       | 网卡开启，但没有连接 Wi-Fi   |
| C    | UP          | 已连接         | 是       | 正常联网中                   |
| D    | UP          | 已断开         | 否       | 断开了 Wi-Fi，但网卡仍在工作 |

**四、推荐使用顺序（命令行连接 Wi-Fi 的完整流程）**

1. 启动网卡接口（电源上电）：

   ```bash
   ip link set wlo1 up
   ```

2. 用 `iw` 扫描可用 Wi-Fi（可选）：

   ```bash
   iw dev wlo1 scan | grep SSID
   ```

3. 连接 Wi-Fi：

   ```bash
   wpa_supplicant -B -i wlo1 -c /etc/wpa_supplicant.conf
   ```

4. 获取 IP 地址：

   ```bash
   dhclient wlo1
   ```

为什么要获取 IP：

`wpa_supplicant` 只负责**建立 Wi-Fi 连接**（认证和加密），**它本身不负责获取 IP 地址**。
要让系统能够联网，**你还需要一个 DHCP 客户端**（如 `dhclient`、`dhcpcd`、`systemd-networkd`）去向路由器请求 IP 地址。

即 `wpa_supplicant` 做的事情：

- 扫描无线网络
- 连接到 SSID（WPA2/WPA3 加密握手）
- 验证密码
- 保持连接稳定

但它**不包含 DHCP 客户端功能**，也不会自动触发 IP 配置。

```bash
# 连接WIFI
sudo wpa_supplicant -B -i wlo1 -c /etc/wpa_supplicant.conf

# 查看IP结果为空
ip a show wlo1
# 输出类似：inet <none>

# 获取IP
sudo dhclient wlo1

# 查看IP正常，才说明具备联网能力
ip a show wlo1
# 输出累死：inet 192.168.1.101/24 brd 192.168.1.255 scope global dynamic wlo1
```

**五、无线连接工具对比**

| 工具             | 类型                  | 推荐场景                       | 是否图形界面      | 是否需配置文件      | 是否适合脚本化 | 控制粒度   |
| ---------------- | --------------------- | ------------------------------ | ----------------- | ------------------- | -------------- | ---------- |
| `wpa_supplicant` | **底层守护进程**      | 所有 Linux 无线网络的底层基础  | 无                | 需要                | 可嵌入系统启动 | ⭐⭐⭐⭐⭐ |
| `wpa_cli`        | 命令行控制工具        | 手动调试、连接、故障排查       | 无                | 依赖 wpa_supplicant | 非交互适用     | ⭐⭐⭐⭐   |
| `nmcli`          | NetworkManager 的前端 | 桌面用户、系统集成、自动化管理 | （有 GUI 可配合） | （内部管理）        | 非常适合       | ⭐⭐⭐     |

1. 安装：

   `wpa_cli` 和 `wpa_supplicant` 这两个是绑定在一起的，通常属于同一个软件包：**`wpasupplicant`**

   ```bash
   sudo apt install wpasupplicant
   ```

   安装结果包括：

   - `/sbin/wpa_supplicant`：无线认证守护进程
   - `/sbin/wpa_cli`：命令行控制工具
   - `/etc/wpa_supplicant/wpa_supplicant.conf`：配置文件（你需手动写）

   `nmcli` 是 `NetworkManager` 的一部分，安装包名为：**`network-manager`**

   ```bash
   sudo apt install network-manager
   ```

   > 注意事项：
   >
   > - 某些服务器或 minimal 系统默认禁用 `NetworkManager`，你可能需要手动启用服务：
   >
   > ```bash
   > sudo systemctl enable NetworkManager
   > sudo systemctl start NetworkManager
   > ```
   >
   > - 在嵌入式或服务器上，NetworkManager 有时会与 `ifupdown`、`netplan` 冲突，谨慎使用。

2. `wpa_supplicant`：无线网络的内核级别大管家

   `wpa_supplicant` 是 Linux 无线连接的**核心守护进程**，负责：

   - 认证（WPA2/WPA3）
   - 密钥协商（EAP/PSK）
   - 自动重连、漫游支持

   ```bash
   wpa_supplicant -B -i wlo1 -c /etc/wpa_supplicant.conf
   ```

   其中配置文件示例如：

   ```log
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1

   network={
       ssid="HomeWiFi"
       psk="homepassword"
       priority=10
   }

   network={
       ssid="WorkWiFi"
       psk="workpassword"
       priority=5
   }
   ```

   > priority 越大，优先级越高。你也可以不给 priority，手动选择哪个启用。

   特点：

   - 所有连接命令都通过它处理
   - 适合嵌入式系统、init 脚本启动
   - 非常稳定、可高度定制
   - **不适合日常手工使用**

3. `wpa_cli`：对 `wpa_supplicant` 的交互控制工具

   `wpa_cli` 是一个控制 `wpa_supplicant` 的命令行接口工具，可以用来：

   - 交互控制连接、断开、扫描
   - 添加/移除网络
   - 获取连接状态
   - 适合调试或简易脚本

   ```bash
   wpa_cli -i wlo1
   # 当前连接状态、SSID、信号强度
   > status
   # 查看已配置网络
   > list_networks
   # 扫描网络和显示结果
   > scan
   > scan_results
   # 添加新 Wi-Fi 网络
   > add_network        # 会返回一个网络编号
   > set_network 0 ssid "你的WiFi名称"
   > set_network 0 psk "你的WiFi密码"
   > enable_network 0    # 允许被自动连接，会根据 signal/priority 等自动决定是否连它
   > save_config
   > select_network 0    # 立即切换连接
   > status
   # 删除网络
   > remove_network
   ```

   也可以非交互模式：

   ```bash
   wpa_cli -i wlo1 scan
   wpa_cli -i wlo1 status
   ```

   特点：

   - 需要 `wpa_supplicant` 已启动
   - 非常底层，适合高手调试或开发环境
   - 一般不推荐初学者直接使用

4. `nmcli`：NetworkManager 的 CLI 接口

   `nmcli` 是 `NetworkManager` 的命令行控制工具。是现代桌面 Linux（如 Ubuntu、Fedora）默认无线网络控制方式。

   优点：

   - 易用：无需手写配置文件
   - 统一管理有线、无线、VPN
   - 支持自动连接、保存配置
   - 适合桌面用户、运维自动化脚本

   连接 Wi-Fi：

   ```bash
   nmcli device wifi list
   nmcli device wifi connect "MyWiFi" password "mypassword"
   ```

   列出当前设备状态：

   ```bash
   nmcli device status
   ```

   断开连接：

   ```bash
   nmcli device disconnect wlo1
   ```

   设置自动重连：

   ```bash
   nmcli connection modify MyWiFi connection.autoconnect yes
   ```

**总结推荐**

| 使用场景                     | 推荐工具                      | 原因                           |
| ---------------------------- | ----------------------------- | ------------------------------ |
| **系统级嵌入式**（如路由器） | `wpa_supplicant` + `wpa_cli`  | 稳定性高，精细控制             |
| **Linux 桌面/服务器管理**    | `nmcli`                       | 易用，自动化程度高，配置持久化 |
| **无线调试、低级控制**       | `wpa_cli`                     | 可直接与 `wpa_supplicant` 对话 |
| **无 NetworkManager 系统**   | `wpa_supplicant` + `dhclient` | 传统纯命令行方案               |

**建议入门优先顺序：**

如果你是服务器或软路由用户：

1. 使用 `wpa_supplicant` 搭配配置文件连接
2. 用 `wpa_cli` 查看状态、扫描等
3. 若使用桌面系统或带 NetworkManager，直接用 `nmcli` 最简单

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

## OpenWrt DNS 分析

在 OpenWRT 中安装了 **OpenClash** 后，DNS 解析通常会被接管（因为代理规则和分流依赖 DNS 解析）。如果你发现终端无法解析域名、DNS 被污染、或者浏览器和终端行为不一致，很可能是 DNS 配置不当。

一、查看 OpenClash 是否安装和运行

```bash
# 查看是否安装：
opkg list-installed | grep openclash
# 查看是否在运行：看到 `openclash` 的守护进程或 `clash` 主进程，说明在运行。
ps | grep openclash
```

二、排查 OpenClash 的 DNS 配置

OpenClash 的 DNS 配置是在其 YAML 配置文件中，影响所有客户端的 DNS 解析行为。

```bash
# OpenClash 的配置文件一般在：
/etc/openclash/config/
# 可以用以下命令查看当前使用的配置文件：
uci get openclash.config.config_path
# 或者直接在openclash的配置文件中找对应项
cat /etc/config/openclash | grep config_path
# 输出上面yaml配置文件中的内容：
cat /etc/openclash/config/xxxx.yaml
```

三、关键 DNS 配置字段说明（YAML）

在 Clash 核心配置中，DNS 配置字段类似如下：

```yaml
dns:
  enable: true
  listen: 0.0.0.0:53
  ipv6: false
  enhanced-mode: fake-ip # 或 redir-host
  nameserver:
    - 1.1.1.1
    - 8.8.8.8
  fallback:
    - https://dns.google/dns-query
    - https://cloudflare-dns.com/dns-query
  fallback-filter:
    geoip: true
    ipcidr:
      - 240.0.0.0/4
  fake-ip-filter:
    - "*.lan"
    - "localhost"
```

各字段说明：

- `enable` ： 是否启用 Clash 内建 DNS（建议为 `true`）
- `listen` ： 本地监听端口（通常为 `53`，以接管系统 DNS），其他配置如 `127.0.0.1:5450` 则 DNS 监听在本地 127.0.0.1 的 5450 端口
- `enhanced-mode` ： `fake-ip` 模式能更好地分流（推荐）
- `nameserver` ： 主 DNS，用于解析常规域名（如国内网站）
- `fallback` ： 被识别为“国外域名”时，用于安全 DNS（DoH）
- `fake-ip-filter` ： 不使用 fake-ip 的域名白名单（避免局域网问题）

四、确认 dnsmasq 是否正确配合 OpenClash

OpenWRT 系统默认使用 dnsmasq 作为 DNS 服务，OpenClash 会修改其配置，以实现 DNS 接管。

1. 查看 dnsmasq 配置中是否重定向了 DNS 请求：

```bash
cat /etc/config/dhcp
```

你应该能看到类似配置：

```log
config dnsmasq
    option noresolv '1'
    option port '0'
```

说明：

- `noresolv 1` → 不使用 `/etc/resolv.conf`
- `port 0` → 停止监听 53 端口，**将 DNS 功能交给 OpenClash**

如果这两个没有设置，dnsmasq 仍然在监听 53 端口，可能与 OpenClash 冲突！

五、排查 DNS 不通的现象

1. 使用 dig/nslookup 进行测试（建议安装工具包）：

```bash
opkg update
opkg install bind-dig
```

然后执行：

```bash
dig www.google.com @127.0.0.1
dig www.google.com @8.8.8.8
```

分析返回的 IP 是否正确，以及响应时间。

---

## ✅ 六、常见问题排查建议

| 问题                 | 原因                                    | 解决方案                                      |
| -------------------- | --------------------------------------- | --------------------------------------------- |
| DNS 被污染           | fallback 配置错误或未启用 DoH           | 设置 `fallback` 为 https 类型 DNS             |
| OpenClash 没接管 DNS | `/etc/config/dhcp` 中 `port` 未设为 `0` | 设置 `port 0`、重启 dnsmasq                   |
| fake-ip 模式失效     | clash 配置错误、设备缓存污染            | 切换为 `redir-host` 试试，或清理设备 DNS 缓存 |
| 有网但不能解析域名   | dnsmasq 与 OpenClash 冲突               | 禁用 dnsmasq 监听 53，重启 OpenClash          |

---

## ✅ 七、实用命令小结

```bash
# 查看 OpenClash 使用的配置文件名
uci get openclash.config.config_path

# 查看 Clash DNS 状态
cat /etc/openclash/config/*.yaml | grep -A10 '^dns:'

# 测试 DNS
dig www.google.com @127.0.0.1

# 重启相关服务
/etc/init.d/openclash restart
/etc/init.d/dnsmasq restart
```

## 我的 openclash DNS 配置分析

我的 openclash dns 配置项 `listen: 127.0.0.1:5450`：表示 DNS 监听在本地 127.0.0.1 的 5450 端口（⚠️） |

可能出现的问题

### 问题 1：系统/终端没有指向 `127.0.0.1:5450`，导致未走 Clash DNS

你设置了 Clash 的 DNS 监听端口是 `127.0.0.1:5450`，那么：

- 如果 OpenWRT 本身（或上游 dnsmasq）没有转发到该端口
- 或你终端（如 Windows/curl/ping）使用的是默认 53 端口
- → 就会**绕过 Clash 的干净 DNS**，导致 DNS 污染/错误。

---

## ✅ 解决方法

### ✅ 方法一：让 OpenWRT 系统 DNS 请求转发到 openclash 的 5450 端口

编辑 `/etc/config/dhcp`，加入/修改以下内容：

```bash
config dnsmasq
    option noresolv '1'
    option port '53'
    list server '127.0.0.1#5450'
```

含义：

- 禁用系统默认的 `/etc/resolv.conf`
- 使用 Clash DNS（本地 127.0.0.1:5450）作为唯一 DNS 上游

然后重启 dnsmasq：

```bash
/etc/init.d/dnsmasq restart
```

### ✅ 方法二：让 Windows 客户端显式用 OpenClash DNS（推荐）

如果你终端是 Windows：

- 打开“网络连接” → 当前网络属性 → IPv4 设置
- 设置 DNS 为 OpenWRT 的 LAN 地址（如 192.168.1.1）
- 保证 OpenWRT 会将请求转发到 Clash 的 DNS

---

## ✅ 方法三（可选）：改为监听 0.0.0.0:53，彻底接管

你也可以直接让 Clash 接管 DNS 53 端口，这样所有设备直接用它：

```yaml
dns:
  enable: true
  listen: 0.0.0.0:53
```

然后 **关闭 dnsmasq 的 53 端口监听**：

```bash
uci set dhcp.@dnsmasq[0].port='0'
uci commit dhcp
/etc/init.d/dnsmasq restart
```

⚠️ 这样操作风险较高，容易影响 OpenWRT 本地域名解析（例如 luci 网页访问），建议谨慎。

---

## 🔎 测试方法

在 OpenWRT 或终端执行：

```bash
# 测试是否真的走到了 Clash 的 DNS
dig www.google.com @127.0.0.1 -p 5450

# 或使用 dig 默认测试，看是否返回污染 IP（如 198.18.x.x）
dig www.google.com

# 或在 Windows 中执行：
nslookup www.google.com 192.168.1.1
```

---

## ✅ 建议配置方式（稳妥方案）

```
yaml复制编辑dns:
  enable: true
  listen: 127.0.0.1:5450
  enhanced-mode: fake-ip
  default-nameserver:
    - 1.1.1.1
    - 8.8.8.8
  nameserver:
    - https://dns.google/dns-query
    - https://cloudflare-dns.com/dns-query
  fake-ip-filter:
    - '*.lan'
    - 'localhost'
```

并在 `/etc/config/dhcp` 配置中：

```
bash复制编辑option noresolv '1'
list server '127.0.0.1#5450'
```

这样你浏览器、终端、系统都走了 clash 的加密 DNS，**防污染 + 能分流**，所有访问行为一致。

---

如果你贴出 `/etc/config/dhcp` 我可以一起帮你检查下是不是已经正确接入 Clash DNS。



`/etc/config/dhcp` 配置说明

你贴出的 `/etc/config/dhcp` 配置说明：

------

### ✅ 当前 dnsmasq 配置重点如下：

```
bash复制编辑option noresolv '1'
list server '127.0.0.1#7874'
```

表示：

* 系统 **禁用了默认的 `/etc/resolv.conf`**，即不会使用运营商 DNS（✅）
* 所有 DNS 请求都会被转发到 **127.0.0.1:7874**

------

### ⚠️ 但你的 Clash 配置中监听的端口是：

```
yaml


复制编辑
listen: 127.0.0.1:5450
```

也就是说：

> **dnsmasq 转发给了 7874，而 Clash 实际监听的是 5450 → 这不匹配！**

所以终端或设备通过 OpenWRT 解析域名时，dnsmasq 把请求发到了 7874，而 Clash 根本不监听这个端口，结果是 DNS 请求被吃掉或失败，终端无法解析域名。

------

## ✅ 解决方案：统一端口配置

你有两个选项：

------

### ✅ 方案 1：**改 dnsmasq 指向 5450**

这是最简单、推荐的改法，因为 clash.yaml 中就是监听 `127.0.0.1:5450`：

```
bash复制编辑# 修改 dnsmasq 转发端口
uci set dhcp.@dnsmasq[0].server='127.0.0.1#5450'
uci commit dhcp
/etc/init.d/dnsmasq restart
```

------

### ✅ 方案 2：**改 Clash 配置，监听 7874**

如果你更希望保留 dnsmasq 指向 7874，那就把 Clash 配置改成：

```
yaml复制编辑dns:
  enable: true
  listen: 127.0.0.1:7874
```

然后保存配置、重启 OpenClash：

```
bash


复制编辑
/etc/init.d/openclash restart
```

------

## ✅ 检查是否生效

### 1. 用 dig 检查是否正确走了 Clash：

```
bash


复制编辑
dig www.google.com @127.0.0.1 -p 5450  # 如果你使用的是 5450
```

或者：

```
bash


复制编辑
dig www.google.com
```

看是否解析到真实的 Google IP，而不是污染 IP（如 `198.18.x.x`）

------

### 2. curl 测试是否成功连接：

```
bash


复制编辑
curl https://www.google.com
```

如果之前 curl 失败但浏览器能打开，此修改后 curl 应该也成功。

------

## 🔄 总结

| 项目               | 状态          | 建议                             |
| ------------------ | ------------- | -------------------------------- |
| Clash DNS 监听端口 | 5450          | ✅ 保留                           |
| dnsmasq 转发端口   | 7874 ❌ 不一致 | 改为 `5450` 一致 ✅               |
| 是否使用加密 DNS   | 有 DoH/tls ✅  | 保持                             |
| fake-ip 模式       | 没显示配置    | 可考虑开启增强分流               |
| 浏览器能解析       | 因自带 DoH ✅  | 终端靠系统 DNS，需要修好转发路径 |



------

如你愿意，我可以提供一份优化后的 clash.yaml DNS 片段 + `/etc/config/dhcp` 一致匹配的示例配置。是否需要？





帮我整理一下上述openwrt设置dns的方式，默认使用什么，是怎样运作的？安装了openwrt后又是怎样使用和运作的



###### ChatGPT 说：

当然可以。下面我会系统性地帮你梳理 **OpenWRT 默认 DNS 设置方式**、**工作机制**，以及 **安装 OpenClash 后如何改变其 DNS 流程**。

------

## 🧠 一、OpenWRT 默认 DNS 设置机制（无 OpenClash 时）

### ✅ 默认使用组件：

| 组件                  | 作用                                                     |
| --------------------- | -------------------------------------------------------- |
| `dnsmasq`             | 负责提供 DHCP 和 DNS 缓存服务，是默认的本地 DNS 服务器   |
| `/etc/resolv.conf`    | 系统 DNS 上游配置文件，一般由 WAN 接口自动获取运营商 DNS |
| `/etc/config/network` | 设置网络接口时，也可指定 `dns` 字段来自定义 DNS          |



------

### 📌 默认 DNS 流程如下：

```
bash复制编辑客户端（PC等）
    ↓
  DHCP 获取 IP 和 DNS（通常是 192.168.1.1）
    ↓
OpenWRT 的 dnsmasq 接收请求（监听 53 端口）
    ↓
dnsmasq 转发 DNS 请求到 `/etc/resolv.conf` 指定的上游 DNS
    ↓
如无污染 → 正常解析
如被污染（如访问 Google）→ 返回错误或 198.18.x.x
```

------

## 🧠 二、安装 OpenClash 后 DNS 机制发生的变化

> OpenClash 是通过劫持网络流量和 DNS 流量，实现分流代理的。

### 🧰 OpenClash 的 DNS 设置项（关键）：

```
yaml复制编辑dns:
  enable: true
  listen: 127.0.0.1:5450
  nameserver:
    - https://1.1.1.1/dns-query
```

------

### 📌 如果未配合 dnsmasq 设置，默认仍然是这样：

```
markdown复制编辑客户端
  ↓
DNS → 192.168.1.1
  ↓
dnsmasq（监听 53）→ 运营商 DNS
    ⚠️ 这里绕过了 Clash，自然会污染
```

------

### ✅ 正确的配合方式（你的目标）：

要让 dnsmasq 把 DNS 请求转发给 OpenClash 的 `127.0.0.1:5450`，如下设置：

```
bash复制编辑option noresolv '1'
list server '127.0.0.1#5450'
```

这意味着：

```
复制编辑客户端
  ↓
DNS → 192.168.1.1
  ↓
dnsmasq
  ↓
转发到 Clash 的本地 DNS → 通过加密 DNS 查询 → 返回正确解析
```

------

## ✅ 总结：OpenWRT DNS 运作机制对比表

| 场景                              | 监听端口                       | 上游 DNS                     | 是否污染         |
| --------------------------------- | ------------------------------ | ---------------------------- | ---------------- |
| 默认 dnsmasq（无 Clash）          | 53                             | `/etc/resolv.conf`（运营商） | ✅可能污染        |
| 加装 Clash（未配置 dnsmasq 转发） | Clash 5450，dnsmasq 仍查运营商 | Clash未接入                  | ❌Clash DNS未生效 |
| 配置 dnsmasq → Clash              | dnsmasq 53 → Clash 5450        | Clash 通过 DoH、TLS 查询     | ✅无污染          |



------

## ✅ 建议最佳实践（你的系统）

1. **OpenClash 设置 DNS：**

```
yaml复制编辑dns:
  enable: true
  listen: 127.0.0.1:5450
  ipv6: false
  nameserver:
    - https://1.1.1.1/dns-query
    - https://dns.google/dns-query
```

1. **/etc/config/dhcp 中 dnsmasq 设置为：**

```
bash复制编辑option noresolv '1'
list server '127.0.0.1#5450'
```

1. **客户端 DNS 设置为网关 IP（如 192.168.1.1）**
   * DHCP 自动下发即可
   * curl、终端都走统一的 DNS 流程

------

## 🛠 可选优化：加入 fake-ip 模式（避免污染与分流问题）

```
yaml复制编辑dns:
  enable: true
  listen: 127.0.0.1:5450
  enhanced-mode: fake-ip
  fake-ip-filter:
    - '*.lan'
    - 'localhost'
```

------

如你希望，我还可以给你整理一张完整的 **Clash DNS 数据流图** 或自动检测脚本，帮你快速验证设置是否成功。是否需要？
