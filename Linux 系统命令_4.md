[toc]

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
Usage: rsync [OPTION]... SRC [SRC]... DEST
  or   rsync [OPTION]... SRC [SRC]... [USER@]HOST:DEST
  or   rsync [OPTION]... SRC [SRC]... [USER@]HOST::DEST
  or   rsync [OPTION]... SRC [SRC]... rsync://[USER@]HOST[:PORT]/DEST
  or   rsync [OPTION]... [USER@]HOST:SRC [DEST]
  or   rsync [OPTION]... [USER@]HOST::SRC [DEST]
  or   rsync [OPTION]... rsync://[USER@]HOST[:PORT]/SRC [DEST]
The ':' usages connect via remote shell, while '::' & 'rsync://' usages connect
to an rsync daemon, and require SRC or DEST to start with a module name.
```

**常见选项：**

- `-a`: 归档模式，表示递归复制并保持文件的权限、时间戳等属性(已包含 `-r`)
- `-z`: 压缩文件数据，减少传输数据量，以减少传输时间
- `-r`: 递归复制整个目录
- `-u`: 仅复制源文件比目标文件新的文件
- `--delete`: 删除目标目录中源目录没有的文件
- `--exclude=PATTERN`: 匹配 PATTERN，排除文件或目录
- `--exclude-from=FIL`: 匹配 FILE 中的规则，排除文件或目录
- `--include=PATTERN`: 匹配 PATTERN，不进行 exclude
- `--include-from=FIL`: 匹配 FILE 中的规则，不进行 exclude
- `-l`: 保留符号链接
- `-t`: 保留时间戳
- `-p`: 保留文件权限
- `-g`: 保留文件的组信息
- `-o`: 保留文件的拥有者信息
- `-x`: 防止跨文件系统，限制同步到单一文件系统
- `-e`: 使用自定义远程 shell（可指定如 SSH 端口）进行传输
- `-v`: 显示详细输出
- `--partial`: 保留已传输的部分文件
- `--progress`: 显示传输进度
- `-P`: 等同于 --partial 和 --progress，在文件传输过程中显示进度，并保留已传输的部分文件。
- `-h`: 以易读的格式显示文件大小（例如 KB、MB、GB）
- `--dry-run`: 模拟同步过程，但不实际执行任何操作

**目录后加不加 `/`：**

| 情况                     | 拷贝结果                                                          |
| ------------------------ | ----------------------------------------------------------------- |
| 源目录末尾加 `/`         | 拷贝<font color=red>源目录中的内容</font>，而不复制源目录本身     |
| 源目录末尾不加 `/`       | 拷贝<font color=red>整个目录</font>（包括其本身）复制到目标目录中 |
| 目标目录末尾加或不加 `/` | 一般无实际区别，除非目标不存在                                    |

假设当前目录结构如下：

```bash
/home/user/
├── source/
│   ├── file1.txt
│   └── file2.txt
└── destination/
```

1. `rsync -av source/ destination/`

   - 拷贝的是 `source` **目录中的内容** 到 `destination` 目录中。
   - `destination` 目录最终变为：

     ```log
     /home/user/destination/
     ├── file1.txt
     └── file2.txt
     ```

2. `rsync -av source destination/`

   - 拷贝的是 `source` **整个目录（包括其名称）** 到 `destination`。
   - `destination` 目录最终变为：

     ```log
     /home/user/destination/source/
     ├── file1.txt
     └── file2.txt
     ```

3. `rsync -av source/ destination` vs `rsync -av source/ destination/`

   - 如果 `destination` 存在，它们效果是一样的；
   - 如果 `destination` 不存在：
     - `destination` 会被创建为新的目录；
     - 加 `/` 不影响拷贝内容，但更推荐用 `/` 表明是目录意图。

4. 常见错误理解

   - **误以为加不加 `/` 没区别**：实际上差异很大，会导致最终目录结构不同。
   - **目标目录是否存在影响结果**：若目标目录不存在，`rsync` 会根据源路径决定最终路径。

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

   `rsync` 默认使用 SSH 协议进行远程文件传输，可将文件从本地复制到远程服务器，或将远程服务器的文件同步到本地。如果你希望指定一个自定义的 SSH 端口，可以使用 `-e` 选项来设置 SSH 的命令。

   ```bash
   # 从本地复制到远程服务器：
   rsync -av /path/to/source/ user@remote_host:/path/to/destination/
   # 从远程服务器复制到本地：
   rsync -av user@remote_host:/path/to/source/ /path/to/destination/
   # 使用 SSH 自定义端口
   rsync -av -e 'ssh -p 2222' /path/to/source/ user@remote_host:/path/to/destination/
   ```

3. **增量备份**

   `rsync` 的一个重要功能是增量备份，它只会复制自上次同步以来发生变化的文件。这是通过记录每个文件的修改时间和大小来实现的。

   ```bash
   rsync -av --delete /path/to/source/ /path/to/destination/
   ```

   - `--delete`：删除目标目录中在源目录中不存在的文件。这通常用于保持目标目录与源目录的完全一致。

4. **排除/包含某些文件或目录**

   1. **排除指定文件或目录**
      使用 `--exclude` 选项，多个排除规则就写多次 `--exclude`。
      或使用 `--exclude-from` 选项，指定一个文件，该文件每行对应一个排除规则。

      ```bash
      rsync -av \
         --exclude '*.log' \
         --exclude '*.git' \
         source/ destination/
      ```

   2. **仅包含指定文件或目录**

      先使用 `--include`/`--include-from` 指定要同步的内容，最后用 `--exclude='*'` 排除其他所有内容。

      > :warning: 注意：`--include` 中路径是相对于 `source/` 的，不是绝对路径。
      > 如果想匹配 source/ 的内层目录的文件而不指定内层目录（如下面 `subdir`），需要加上 `--include='*/'`，这样就可以进入内层目录去找到你想要的 `*.xx/` 等文件。如果不加，rsync 会一上来就排除整个目录，连里面的文件都不会检查。

      ```bash
      rsync -av \
         --include='file1.txt' \
         --include='subdir/data.csv' \
         --exclude='*' \
         source/ destination/
      rsync -av \
         --include='*/' \
         --include='file1.txt' \
         --include='data.csv' \
         --exclude='*' \
         source/ destination/
      ```

   3. **--include 和 --exclude 解释**

      `--include` 本身**不会自动排除其他文件**。如果你只使用 `--include` 而不加 `--exclude='*'`，那么默认是「同步所有文件」，只是在你指定的 `--include` 文件上**优先匹配**，并不会阻止其他文件也被同步。因此若想「仅同步指定文件」，需加上写 `--exclude='*'`。

      `rsync` 的匹配规则是「顺序判断」的，流程大致如下：

      1. 遇到 `--include`：如果文件/路径匹配到，**标记为“保留”**。
      2. 遇到 `--exclude`：如果匹配到，**标记为“忽略”**。
      3. 如果什么都不匹配，默认是包含。

      > :pushpin: `--include` 是一个「白名单」，但 rsync 默认是「全允许」的。所以你必须配合 `--exclude='*'` 才能让 `--include` 生效为「只包含这些，其他都不要」。

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
   ssh-copy-id -p 22 -i /path/id_rsa_xxx.pub user@host

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

   > :page_with_curl: **Note**
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

5. **本地 SSH 连接配置**

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
   Host my-server-alias                # hostName的别名
     HostName xxx.xxx.xxx.xxx          # 远程服务器 IP 或域名
     Port xx                           # 默认是22，可以根据实际改
     User xxxxx                        # SSH 登录用户名
     IdentityFile ~/.ssh/xxxxxxxx      # 指定私钥路径

     # 跳过服务器指纹验证，建议仅用于脚本或临时场景
     StrictHostKeyChecking no
     UserKnownHostsFile /dev/null

     # 指定跳板机的用户名、主机地址、端口
     ProxyJump [user@]jump_host[:port]
     # 也可以把跳板机也定义成一个 Host 别名方便复用，然后
     ProxyJump my-server-alias
   ```

   > - 不要加 PreferredAuthentications publickey，否则连接远程服务器上 docker 时，会报错 **Connection refused**。<font color=red><b>被坑死了 -\_-!!!</b></font>

6. 测试免密登录

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

### ssh 服务器指纹

服务器指纹（**SSH Fingerprint**）是在 SSH 连接中用于标识远程主机身份的“数字指纹”，它的作用类似于人的身份证，用来确认“你正在连接的是你想连接的那台服务器”。

> 服务器指纹是<font color=red>服务器的 SSH 公钥</font>经过摘要算法（如 SHA256）计算后的简短字符串，用于防止中间人攻击。

**它是怎么来的？**

- 当一台服务器启动 SSH 服务时，它会生成一对密钥对（公钥和私钥）。

- 公钥存储在服务器的 `/etc/ssh/ssh_host_*.pub` 中。

- **指纹**就是这个公钥经过哈希算法（MD5、SHA1、SHA256）计算出的摘要，例如：

  ```ruby
  SHA256:X3vUHT4ZBj3lRDb1K+F2G8HVzknD4Q7KpR4gzxZPbSg
  ```

可以用如下命令查看服务器的 SSH 指纹：

```bash
ssh-keygen -lf /etc/ssh/ssh_host_rsa_key.pub
```

**作用：**

1. **身份验证（防中间人攻击）**
   当你第一次连接某台服务器，SSH 客户端会显示指纹，让你确认这是不是你要连的机器。

2. **防止被假冒服务器欺骗**
   如果你连接到了一个伪装成目标主机的机器，它的公钥指纹会不同，SSH 就会提示你：

   > WARNING: POSSIBLE DNS SPOOFING DETECTED!

3. **后续连接时自动校验**
   第一次连接确认后，指纹被保存在你本地的 `~/.ssh/known_hosts` 文件中。下次连接时自动校验是否一致，如果变了，SSH 会警告你可能遭遇了攻击。

举个中间人攻击的例子：

1. 你连接服务器 A，结果网络中有人劫持了你的连接。
2. 他伪装成 A 给你发送了自己的公钥。
3. 如果你没有验证指纹并照样输入密码，你的密码就被泄露了！

**总结：**

| 项目         | 说明                               |
| ------------ | ---------------------------------- |
| 本质         | 服务器 SSH 公钥的哈希摘要          |
| 作用         | 确认远程主机身份，防止中间人攻击   |
| 首次连接     | 用户确认指纹，保存到 known_hosts   |
| 指纹变更警告 | 可能是服务器换密钥或遭遇攻击       |
| 推荐做法     | 第一次连接时比对确认，之后自动校验 |

**跳过指纹验证：**

在 vscode 的 ssh config 配置文件中，可以通过下面配置跳过指纹验证

```bash
# 跳过服务器指纹验证，建议仅用于脚本或临时场景
StrictHostKeyChecking no
UserKnownHostsFile /dev/null
```

### ssh 命令行指定跳板机

1. **`-J`（ProxyJump，推荐）**

   ```bash
   ssh -J jumpuser@jump.xx.xx.xx:52000 \
       workuser@target.xx.xx.xx
   ```

   对应 rsync：

   ```bash
   sshpass -p xxxx \
   rsync -avzP \
   -e "ssh -J <jumpuser>@<jumpip>:<jumpport>" \
   <src_path> \
   <workuser>@<workip>:<dst_path>
   ```

   - 语义清晰
   - 推荐程度仅次于 ssh config
   - 无法在一条命令里用 sshpass 同时为 jumpuser 和 workuser 指定两个不同的密码。是 OpenSSH 的设计限制问题。
   - 经尝试，无法用 sshpass 指定 workuser 密码。因为 sshpass 无法区分是 jumpuser 在要密码还是 workuser 在要密码。

2. **`ProxyCommand + -W`（底层但通用）**

   ```bash
   # 不带 sshpass
   ssh -o ProxyCommand="ssh -p <jumpport> <jumpuser>@<jumpip> -W %h:%p" \
     -p <workport> <workuser>@<workip>
   # 带 sshpass
   sshpass -p <wordpassword> ssh -o ProxyCommand="sshpass -p <jumppassword> ssh -p <jumpport> <jumpuser>@<jumpip> -W %h:%p" \
     -p <workport> <workuser>@<workip>
   ```

   rsync 写法：

   ```bash
   # 不带 sshpass
   rsync -avzP \
     -e 'ssh -p <workport> -o ProxyCommand="ssh -p <jumpport> <jumpuser>@<jumpip> -W %h:%p"' \
     <src_dir> \
     <workuser>@<workip>:<dst_dir>
   # 带 sshpass
   sshpass -p <wordpassword> \
     rsync -avzP \
     -e 'ssh -p <workport> -o ProxyCommand="sshpass -p <jumppassword> ssh -p <jumpport> <jumpuser>@<jumpip> -W %h:%p"' \
     <src_dir> \
     <workuser>@<workip>:<dst_dir>
   ```

   - 所有 OpenSSH 版本可用
   - `%h:%p` 在 **ProxyCommand 内合法**

   > rsync 命令中，目的主机的端口号用 `-e 'ssh -p <port>'` 指定。
   > scp 命令中，目的主机的端口号用 `-P <port>` 指定。

### ssh config 指定跳板机

**ssh config 配置文件的基本格式**

```shell
Host my-server-alias                # hostName的别名
  HostName xxx.xxx.xxx.xxx          # 远程服务器 IP 或域名
  Port xx                           # 默认是22，可以根据实际改
  User xxxxx                        # SSH 登录用户名
  IdentityFile ~/.ssh/xxxxxxxx      # 指定私钥路径

  # 跳过服务器指纹验证，建议仅用于脚本或临时场景
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null

  # 指定跳板机的用户名、主机地址、端口
  ProxyJump [user@]jump_host[:port]
  # 也可以把跳板机也定义成一个 Host 别名方便复用，然后
  ProxyJump my-server-alias
```
