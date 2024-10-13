[toc]

# Linux 命令

## Linux terminal 终端快捷键汇

1. 常用快捷键

ctrl+左右键: 在单词之间跳转
ctrl+a: 跳到本行的行首
ctrl+e: 跳到页尾
Ctrl+u：删除当前光标前面的文字 （还有剪切功能）
ctrl+k：删除当前光标后面的文字(还有剪切功能)
Ctrl+L：进行清屏操作
Ctrl+y: 粘贴Ctrl+u或ctrl+k剪切的内容
Ctrl+w: 删除光标前面的单词的字符
Alt – d ：由光标位置开始，往右删除单词。往行尾删

2. 移动光标

Ctrl – a ：移到行首
Ctrl – e ：移到行尾
Ctrl – b ：往回(左)移动一个字符
Ctrl – f ：往后(右)移动一个字符
Alt – b ：往回(左)移动一个单词
Alt – f ：往后(右)移动一个单词
Ctrl – xx ：在命令行尾和光标之间移动
M-b ：往回(左)移动一个单词
M-f ：往后(右)移动一个单词

3. 编辑命令

Ctrl – h ：删除光标左方位置的字符
Ctrl – d ：删除光标右方位置的字符（注意：当前命令行没有任何字符时，会注销系统或结束终端）
Ctrl – w ：由光标位置开始，往左删除单词。往行首删
Alt – d ：由光标位置开始，往右删除单词。往行尾删
M – d ：由光标位置开始，删除单词，直到该单词结束。
Ctrl – k ：由光标所在位置开始，删除右方所有的字符，直到该行结束。
Ctrl – u ：由光标所在位置开始，删除左方所有的字符，直到该行开始。
Ctrl – y ：粘贴之前删除的内容到光标后。
ctrl – t ：交换光标处和之前两个字符的位置。
Alt + . ：使用上一条命令的最后一个参数。
Ctrl – _ ：回复之前的状态。撤销操作。
Ctrl -a + Ctrl -k 或 Ctrl -e + Ctrl -u 或 Ctrl -k + Ctrl -u 组合可删除整行。

3. Bang(!)命令

!! ：执行上一条命令。
!wget ：执行最近的以wget开头的命令。
!wget:p ：仅打印最近的以wget开头的命令，不执行。
!$ ：上一条命令的最后一个参数， 与 Alt - . 和 $_ 相同。
!* ：上一条命令的所有参数
!*:p ：打印上一条命令是所有参数，也即 !*的内容。
^abc ：删除上一条命令中的abc。
!-n ：执行前n条命令，执行上一条命令： !-1， 执行前5条命令的格式是： !-5 查找历史命令
Ctrl – p ：显示当前命令的上一条历史命令
Ctrl – n ：显示当前命令的下一条历史命令
Ctrl – r ：搜索历史命令，随着输入会显示历史命令中的一条匹配命令，Enter键执行匹配命令；ESC键在命令行显示而不执行匹配命令。
Ctrl – g ：从历史搜索模式（Ctrl – r）退出。

4. 控制命令

Ctrl – l ：清除屏幕，然后，在最上面重新显示目前光标所在的这一行的内容。
Ctrl – o ：执行当前命令，并选择上一条命令。
Ctrl – s ：阻止屏幕输出
Ctrl – q ：允许屏幕输出
Ctrl – c ：终止命令
Ctrl – z ：挂起命令


-----------------------------------
©著作权归作者所有：来自51CTO博客作者Linux学习记录的原创作品，请联系作者获取转载授权，否则将追究法律责任
Linux terminal 终端快捷键汇总
https://blog.51cto.com/u_12148962/5622453





## ***\*find 命令和 grep 命令区别\****

### **grep 命令**

- grep 的作用是**在文件中**提取和匹配符合条件的字符串行。命令格式如下

```bash
grep [选项] "搜索内容" 文件名
```





find 也是搜索命令，那么 find 命令和 grep 命令有什么区别呢？
find 命令
find 命令用于在系统中搜索符合条件的文件名，如果需要模糊查询，则使用通配符进行匹配，通配符是完全匹配（find 命令可以通过-regex 选项，把匹配规则转为正则表达式规则，但是不建议如此）。
grep 命令
grep 命令用于在文件中搜索符合条件的字符串，如果需要模糊查询，则使用正则表达式进行匹配，正则表达式是包含匹配。



### **通配符与正则表达式的区别**

 **\*通配符：用于匹配文件名，完全匹配\***

| 通配符 | 作用                                                         |
| ------ | ------------------------------------------------------------ |
| ？     | 匹配一个任意字符                                             |
| *      | 匹配 0 个或任意多个任意字符，也就是可以匹配任何内容          |
| []     | 匹配中括号中任意一个字符。例如，[abc]代表一定匹配一个字符，或者是 a，或者是 b，或者是 c |
| [-]    | 匹配中括号中任意一个字符，-代表一个范围。例如，[a-z]代表匹配一个小写字母 |
| [^]    | 逻辑非，表示匹配不是中括号内的一个字符。例如，  `[^0-9]`代表匹配一个不是数字的字符 |

**\*正则表达式：用于匹配字符串，包含匹配\***

| 正则符 | 作用                                                         |
| ------ | ------------------------------------------------------------ |
| ？     | 匹配一个任意字符                                             |
| *      | 匹配 0 个或任意多个任意字符，也就是可以匹配任何内容          |
| []     | 匹配中括号中任意一个字符。例如，[abc]代表一定匹配一个字符，或者是 a，或者是 b，或者是 c |
| [-]    | 匹配中括号中任意一个字符，-代表一个范围。例如，[a-z]代表匹配一个小写字母 |
| [^]    | 逻辑非，表示匹配不是中括号内的一个字符。例如，  `[^0-9]`代表匹配一个不是数字的字符 |
| ^      | 匹配行首                                                     |
| $      | 匹配行尾                                                     |

> [Linux grep 命令和通配符](https://blog.csdn.net/baidu_41388533/article/details/107610827)



## [shell 中| && || () {} 用法以及shell的逻辑与或非](https://www.cnblogs.com/aaronLinux/p/8340281.html)

### && 运算符:

格式



```undefined
command1  && command2
```

&&左边的命令（命令1）返回真(即返回0，成功被执行）后，&&右边的命令（命令2）才能够被执行；换句话说，“如果这个命令执行成功&&那么执行这个命令”。
 语法格式如下：



```undefined
command1 && command2 && command3 ...
```

1. 命令之间使用 && 连接，实现逻辑与的功能。

2. 只有在 && 左边的命令返回真（命令返回值 $? == 0），&& 右边的命令才会被执行。

3. 只要有一个命令返回假（命令返回值 $? == 1），后面的命令就不会被执行。

4. 示例1中，cp命令首先从root的家目录复制文件文件anaconda-ks.cfg到 /data目录下；执行成功后，使用 rm 命令删除源文件；如果删除成功则输出提示信息"SUCCESS"。

   ![img](https:////upload-images.jianshu.io/upload_images/3269979-0030f07de707cdf9.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/956/format/webp)

   示例1.jpg

### || 运算符:

格式



```ruby
command1 || command2
```

||则与&&相反。如果||左边的命令（command1）未执行成功，那么就执行||右边的命令（command2）；或者换句话说，“如果这个命令执行失败了||那么就执行这个命令。

1. 命令之间使用 || 连接，实现逻辑或的功能。

2. 只有在 || 左边的命令返回假（命令返回值 $? == 1），|| 右边的命令才会被执行。这和 c 语言中的逻辑或语法功能相同，即实现短路逻辑或操作。

3. 只要有一个命令返回真（命令返回值 $? == 0），后面的命令就不会被执行。

4. 示例2中，如果 dir目录不存在，将输出提示信息 fail 。

   ![img](https:////upload-images.jianshu.io/upload_images/3269979-14f9f3cf35f2ac05.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/570/format/webp)

   示例2.jpg

5. 示例3中，如果 dir 目录存在，将输出 success 提示信息；否则输出 fail 提示信息。

   ![img](https:////upload-images.jianshu.io/upload_images/3269979-c495d95cc835f354.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/737/format/webp)

   示例3.jpg

   6.下面是一个shell脚本中常用的||组合示例



```bash
echo $BASH |grep -q 'bash' || { exec bash "$0" "$@" || exit 1; }    系统调用exec是以新的进程去代替原来的进程，但进程的PID保持不变。因此，可以这样认为，exec系统调用并没有创建新的进程，只是替换了原来进程上下文的内容。原进程的代码段，数据段，堆栈段被新的进程所代替。
```

### () 运算符:

如果希望把几个命令合在一起执行，shell提供了两种方法。既可以在当前shell也可以在子shell中执行一组命令。
 格式:



```undefined
(command1;command2;command3....)               多个命令之间用;分隔
```

1. 一条命令需要独占一个物理行，如果需要将多条命令放在同一行，命令之间使用命令分隔符（;）分隔。执行的效果等同于多个独立的命令单独执行的效果。

2. () 表示在当前 shell 中将多个命令作为一个整体执行。需要注意的是，使用 () 括起来的命令在执行前面都不会切换当前工作目录，也就是说命令组合都是在当前工作目录下被执行的，尽管命令中有切换目录的命令。

3. 命令组合常和命令执行控制结合起来使用。

4. 示例4中，如果目录dir不存在，则执行命令组合。

   ![img](https:////upload-images.jianshu.io/upload_images/3269979-b2bbf7d1d82d20ba.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/1157/format/webp)

   示例4.jpg

### {} 运算符:

如果使用{}来代替()，那么相应的命令将在子shell而不是当前shell中作为一个整体被执行，只有在{}中所有命令的输出作为一个整体被重定向时，其中的命令才被放到子shell中执行，否则在当前shell执行。
 它的一般形式为：



```undefined
{ command1;command2;command3… }      注意：在使用{}时，{}与命令之间必须使用一个空格
```

1. 示例5中，使用{}则在子shell中执行了打印操作

   ![img](https:////upload-images.jianshu.io/upload_images/3269979-1702732ef384c16d.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/1134/format/webp)

   示例5.jpg



### shell的逻辑与或非

  逻辑非 !        条件表达式的相反

if [ ! 表达式 ]

if [ ! -d $num ]     如果不存在目录$num

 

  逻辑与 –a        条件表达式的并列

if [ 表达式1 –a 表达式2 ]

 

  逻辑或 -o        条件表达式的或

if [ 表达式1 –o 表达式2 ]

-   表达式与前面的= != -d –f –x -ne -eq -lt等合用

-   逻辑符号就正常的接其他表达式，没有任何括号（ ），就是并列

if [ -z "$JHHOME" -a -d $HOME/$num ]

-   注意逻辑与-a与逻辑或-o很容易和其他字符串或文件的运算符号搞混了



## install命令详解

install命令与cp命令类似，均可以将文件或目录拷贝到指定的路径；但是install命令可以控制目标文件的属性。

##### 命令格式：

```css
       install [OPTION]... [-T] SOURCE DEST
       install [OPTION]... SOURCE... DIRECTORY
       install [OPTION]... -t DIRECTORY SOURCE...
       install [OPTION]... -d DIRECTORY...
```

前三个格式会将指定的source 复制到Dest地址或者将多个source复制到已存在的目标目录，同时设定相应的权限模式或者属主，属组等信息；第四个格式会创建给定的目录路径。

##### 常用选项：

```csharp
-g，--group=Group：指定目标文件的属组；
-o，--owner=user：指定目标文件的属主；
-m，--mode=mode：指定目标文件的权限模式；
-S：设置目标文件的后缀；
-D：创建指定文件路径中不存在的目录；
```

##### 使用实例：

复制source文件到指定的文件路径：

```ruby
[root@localhost ~]# install /etc/passwd /tmp/passwd.bak
[root@localhost ~]# cat /tmp/passwd.bak | head -5
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
```

复制多个source文件到对应的目录路径：

```csharp
[root@localhost ~]# mkdir /tmp/test
[root@localhost ~]# install -t /tmp/test/ /etc/passwd /home/charlie/autocreate 
[root@localhost ~]# ll /tmp/test/
总用量 8
-rwxr-xr-x. 1 root root   12 2月   9 17:00 autocreate
-rwxr-xr-x. 1 root root 3595 2月   9 17:00 passwd
```



##  ip 命令

Linux 下 [ip](https://www.runoob.com/linux/linux-comm-ip.html) 命令与 [ifconfig](https://www.runoob.com/linux/linux-comm-ifconfig.html) 命令类似，但比 ifconfig 命令更加强大，主要功能是用于显示或设置网络设备。

ip 命令是 Linux 加强版的的网络配置工具，用于代替 ifconfig 命令。

语法

```
ip [ OPTIONS ] OBJECT { COMMAND | help }
```

OBJECT 为常用对象，值可以是以下几种：

```
OBJECT={ link | addr | addrlabel | route | rule | neigh | ntable | tunnel | maddr | mroute | mrule | monitor | xfrm | token }
```

常用对象的取值含义如下：

- link：网络设备
- address：设备上的协议（IP或IPv6）地址
- addrlabel：协议地址选择的标签配置
- route：路由表条目
- rule：路由策略数据库中的规则

OPTIONS 为常用选项，值可以是以下几种：

```
OPTIONS={ -V[ersion] | -s[tatistics] | -d[etails] | -r[esolve] | -h[uman-readable] | -iec | -f[amily] { inet | inet6 | ipx | dnet | link } | -o[neline] | -t[imestamp] | -b[atch] [filename] | -rc[vbuf] [size] }
```

常用选项的取值含义如下：

- -V：显示命令的版本信息；
- -s：输出更详细的信息；
- -f：强制使用指定的协议族；
- -4：指定使用的网络层协议是IPv4协议；
- -6：指定使用的网络层协议是IPv6协议；
- -0：输出信息每条记录输出一行，即使内容较多也不换行显示；
- -r：显示主机时，不使用IP地址，而使用主机的域名。

```
# 实例
ip link show                    # 显示网络接口信息
ip link list    				# 用 ip 命令显示网络设备的运行状态：
ip -s link list					# 显示更加详细的设备信息：
ip addr show     				# 显示网卡IP信息
ip route list 					# 显示核心路由表：
ip link | grep -E '^[0-9]' | awk -F: '{print $2}'	# 获取主机所有网络接口：
```



# lspci 命令

**lspci** 是一个用来显示系统中所有 PCI 总线设备或连接到该总线上的所有设备的工具。

```bash
lspci [options]
```

- **-v**

  使得 *lspci* 以冗余模式显示所有设备的详细信息。

- **-vv**

  使得 *lspci* 以过冗余模式显示更详细的信息 (事实上是 PCI 设备能给出的所有东西)。这些数据的确切意义没有在此手册页中解释，如果你想知道更多，请参照 **/usr/include/linux/pci.h** 或者 PCI 规范。

- **-t**

  以树形方式显示包含所有总线、桥、设备和它们的连接的图表。


```shell
# 实例
# 查看网卡生产商，型号
lspci | grep -i net
```



# [ifconfig 命令](https://www.runoob.com/linux/linux-comm-ifconfig.html)

apt install net-tools

配置和显示 Linux 系统网卡的网络参数。用ifconfig命令配置的网卡信息，在网卡重启后机器重启后，配置就不存在。要想将上述的配置信息永远的存的电脑里，那就要修改网卡的配置文件了。

```shell
ifconfig [网络设备][down up -allmulti -arp -promisc][add<地址>][del<地址>][<hw<网络设备类型><硬件地址>][io_addr<I/O地址>][irq<IRQ地址>][media<网络媒介类型>][mem_start<内存地址>][metric<数目>][mtu<字节>][netmask<子网掩码>][tunnel<地址>][-broadcast<地址>][-pointopoint<地址>][IP地址]
```

**参数说明**：

- add<地址> 设置网络设备IPv6的IP地址。
- del<地址> 删除网络设备IPv6的IP地址。
- down 关闭指定的网络设备。
- <hw<网络设备类型><硬件地址> 设置网络设备的类型与硬件地址。
- io_addr<I/O地址> 设置网络设备的I/O地址。
- irq<IRQ地址> 设置网络设备的IRQ。
- media<网络媒介类型> 设置网络设备的媒介类型。
- mem_start<内存地址> 设置网络设备在主内存所占用的起始地址。
- metric<数目> 指定在计算数据包的转送次数时，所要加上的数目。
- mtu<字节> 设置网络设备的MTU。
- netmask<子网掩码> 设置网络设备的子网掩码。
- tunnel<地址> 建立IPv4与IPv6之间的隧道通信地址。
- up 启动指定的网络设备。
- -broadcast<地址> 将要送往指定地址的数据包当成广播数据包来处理。
- -pointopoint<地址> 与指定地址的网络设备建立直接连线，此模式具有保密功能。
- -promisc 关闭或启动指定网络设备的promiscuous模式。
- [IP地址] 指定网络设备的IP地址。
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

**eth0** 表示第一块网卡，其中`HWaddr`表示网卡的物理地址，可以看到目前这个网卡的物理地址(MAC地址）是`00:16:3E:00:1E:51`。

**inet addr** 用来表示网卡的IP地址，此网卡的IP地址是`10.160.7.81`，广播地址`Bcast:10.160.15.255`，掩码地址`Mask:255.255.240.0`。

**lo** 是表示主机的回坏地址，这个一般是用来测试一个网络程序，但又不想让局域网或外网的用户能够查看，只能在此台主机上运行和查看所用的网络接口。比如把 httpd服务器的指定到回坏地址，在浏览器输入127.0.0.1就能看到你所架WEB网站了。但只是您能看得到，局域网的其它主机或用户无从知道。

- 第一行：连接类型：Ethernet（以太网）HWaddr（硬件mac地址）。
- 第二行：网卡的IP地址、子网、掩码。
- 第三行：UP（代表网卡开启状态）RUNNING（代表网卡的网线被接上）MULTICAST（支持组播）MTU:1500（最大传输单元）：1500字节。
- 第四、五行：接收、发送数据包情况统计。
- 第七行：接收、发送数据字节数统计信息。

**启动关闭指定网卡：**

```shell
ifconfig eth0 up
ifconfig eth0 down
```

`ifconfig eth0 up`为启动网卡eth0，`ifconfig eth0 down`为关闭网卡eth0。ssh登陆linux服务器操作要小心，关闭了就不能开启了，除非你有多网卡。

**为网卡配置和删除IPv6地址：**

```shell
ifconfig eth0 add 33ffe:3240:800:1005::2/64    #为网卡eth0配置IPv6地址
ifconfig eth0 del 33ffe:3240:800:1005::2/64    #为网卡eth0删除IPv6地址
```

**用ifconfig修改MAC地址：**

```shell
ifconfig eth0 hw ether 00:AA:BB:CC:dd:EE
```

**配置IP地址：**

```shell
[root@localhost ~]# ifconfig eth0 192.168.2.10
[root@localhost ~]# ifconfig eth0 192.168.2.10 netmask 255.255.255.0
[root@localhost ~]# ifconfig eth0 192.168.2.10 netmask 255.255.255.0 broadcast 192.168.2.255
```



# iwconfig 命令

iwconfig  系统配置无线网络设备或显示无线网络设备信息。iwconfig 命令类似于ifconfig命令，但是他配置对象是无线网卡，它对网络设备进行无线操作，如设置无线通信频段

```shell
iwconfig [interface]
```

* auto 自动模式
* essid 设置ESSID
* nwid 设置网络ID
* freq 设置无线网络通信频段
* chanel 设置无线网络通信频段
* sens 设置无线网络设备的感知阀值
* mode 设置无线网络设备的通信设备
* ap 强迫无线网卡向给定地址的接入点注册
* nick<名字> 为网卡设定别名
* rate<速率> 设定无线网卡的速率
* rts<阀值> 在传输数据包之前增加一次握手，确信信道在正常的
* power 无线网卡的功率设置

```shell
# 实例
iwconfig		# 显示无线网络配置
```

> 若提示找不到命令：`sudo apt install wireless-tools`





# [dmesg 命令](https://www.runoob.com/linux/linux-comm-dmesg.html) 

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



# 网络命令



wpa_supplicant工具集，包括wpa_supplicant*、*wpa_passphrase、wpa_cli



# ldd(list dynamic dependencies)



### systemctl命令列出所有服务

列出所有service

```shell
systemctl list-units --type=service
systemctl --type=service
```
