[toc]

# Linux 操作

## Terminal 中杀掉进程

在终端（terminal）中杀掉进程的方法主要有以下几种，取决于你知道进程的什么信息：

**一、已知进程名时杀掉进程**

使用 `pkill` 命令：

```bash
pkill <进程名>

# 例如：
pkill firefox
```

如果想更安全地匹配名字（避免误杀）：

```bash
pkill -f "完整命令行内容的一部分"
```

**二、已知进程 ID（PID）时杀掉进程**

使用 `kill` 命令：

```bash
kill <PID>

# 例如：
kill 12345
```

如果进程不响应（顽固），可以强制杀死：

```bash
kill -9 <PID>
```

**三、查找并杀掉进程（推荐组合）**

用 `ps` 或 `top` 查找 PID 后再杀掉进程：

```bash
ps aux | grep <关键字>

# 例如：
ps aux | grep python
```

找到 PID 后，使用 `kill` 或 `kill -9` 杀掉它。

也可以结合 `ps` 和 `awk`：

```bash
ps aux | grep <关键字> | grep -v grep | awk '{print $2}' | xargs kill
# 或强制杀掉：
ps aux | grep <关键字> | grep -v grep | awk '{print $2}' | xargs kill -9
```

**四、 使用 `htop`（更友好）**

安装并运行 `htop`：

```bash
sudo apt install htop    # Debian/Ubuntu
htop
```

然后用方向键选择进程，按 `F9`，选择 `SIGKILL` 杀掉。

**注意事项**

- 使用 `kill -9` 杀进程虽然暴力，但**不会给程序清理资源的机会**，慎用。
- `pkill` 默认会杀所有匹配名的进程，如果名字不唯一要小心。

## kill 命令

`kill` 通过 **发送信号** 给指定的进程（PID）来控制其行为，最常用于“杀掉进程”，但实际上它也可以发送其他信号（如暂停、继续、重新加载配置等）。

**常见语法：**

```bash
kill [选项] PID
```

- 默认发送 `SIGTERM`（15）信号，表示“请求终止”
- 强制终止用 `SIGKILL`（9）
- 查看信号列表：`kill -l`

**常用信号：**

| 信号名  | 数字 | 含义              | 说明                           |
| ------- | ---- | ----------------- | ------------------------------ |
| SIGTERM | 15   | 优雅地终止        | 默认行为，让进程有机会清理资源 |
| SIGKILL | 9    | 强制终止          | 无法被捕获或忽略，**直接终止** |
| SIGHUP  | 1    | 挂起/重新加载配置 | 常用于守护进程重读配置         |
| SIGSTOP | 19   | 暂停进程          | 类似 Ctrl+Z                    |
| SIGCONT | 18   | 恢复被暂停的进程  | 和 SIGSTOP 配合使用            |

**示例用法：**

```bash
kill 1234                  # 发送 SIGTERM，优雅终止
kill -9 1234               # 强制杀死进程
kill -SIGSTOP 1234         # 暂停进程
kill -SIGCONT 1234         # 恢复进程
```

**使用场景：**

- **已知 PID 的时候**最适合用 `kill`
- 用于**控制进程状态**（暂停、恢复）
- 用于**安全退出某些服务**（使用 SIGTERM 或 SIGHUP）

## pkill 命令

`pkill` 用于通过 **进程名或命令匹配**来终止进程，不需要知道 PID。`pkill` 允许通过进程名、用户、组或其他属性来查找和杀死进程，这使得它比 `kill` 更方便，尤其是在需要杀死多个同名进程时。

```bash
pkill [选项] <匹配条件>
```

- `选项`: `pkill` 有许多选项，用于指定匹配方式和发送的信号。
- `匹配条件`: 这是要匹配的进程名或属性，可以是精确的名称，也可以是使用正则表达式的模式。

**常用选项：**

| 选项     | 含义                                               |
| -------- | -------------------------------------------------- |
| `-f`     | 匹配完整命令行（包含参数）                         |
| `-<sig>` | 指定信号，如 `-9` 强制杀死进程（等价于 `kill -9`） |
| `-u`     | 指定用户杀掉进程                                   |
| `-t`     | 指定终端杀掉进程                                   |
| `-x`     | 完整匹配进程名                                     |
| `-n`     | 只向找到的最大(结束) 进程号发送信号                |
| `-o`     | 只向找到的最小(起始) 进程号发送信号                |

**示例用法：**

```bash
pkill firefox             # 杀掉所有名为 firefox 的进程
pkill -f "python myapp.py"  # 精确匹配命令行中包含“python myapp.py”的进程
pkill -9 python           # 强制杀掉所有 python 进程
pkill -u alice chrome     # 杀掉用户 alice 的 chrome
pkill -t pts/0            # 杀死终端 `pts/0` 的所有进程
```

**使用场景：**

- **根据进程名终止进程**：如 `pkill firefox` 杀死所有名为 `firefox` 的进程。

- **模糊匹配杀死进程**: `pkill` 支持模糊匹配，如 `pkill fire` 可能会杀死所有以 `fire` 开头的进程。

- **支持信号**: `pkill` 默认发送 `SIGTERM` 信号来终止进程，但您也可以使用 `-s` 选项发送其他信号，例如 `SIGKILL` (强制终止)。

- **支持其他属性**: 除了进程名，`pkill` 还可以根据用户、组、终端等属性来匹配和杀死进程。

## `kill` vs `pkill`

| 项   | `kill`               | `pkill`                      |
| ---- | -------------------- | ---------------------------- |
| 依据 | PID（数字）          | 进程名、命令行内容等         |
| 优点 | 精确控制，适合脚本化 | 快捷模糊匹配，适合人手操作   |
| 缺点 | 需要先查 PID         | 可能误杀进程（需小心匹配）   |
| 场景 | 已知 PID、写脚本     | 杀掉一类进程、快速命令行处理 |
| 示例 | `kill -9 1234`       | `pkill -9 python`            |

## read 命令

在 Linux 的 Shell 脚本编程中，`read` 是一个非常实用的内置命令。它主要用于**从标准输入（键盘）或文件描述符中读取一行文本**，并将内容赋值给一个或多个变量。

```bash
read: read [-ers] [-a array] [-d delim] [-i text] [-n nchars] [-N nchars] [-p prompt] [-t timeout] [-u fd] [name ...]
    Read a line from the standard input and split it into fields.

    Reads a single line from the standard input, or from file descriptor FD
    if the -u option is supplied.  The line is split into fields as with word
    splitting, and the first word is assigned to the first NAME, the second
    word to the second NAME, and so on, with any leftover words assigned to
    the last NAME.  Only the characters found in $IFS are recognized as word
    delimiters.

    If no NAMEs are supplied, the line read is stored in the REPLY variable.
```

常见参数汇总：

- `-p`: 显示提示信息
- `-s`: 静默模式（不回显输入内容）
- `-n`: 读取指定的 N 个字符后立即返回
- `-t`: 设置超时秒数
- `-r`: 原始模式（不转义反斜杠 `\`）
- `-a`: 将读入的数据赋值给数组

注意：

- 如果不指定变量名，读取到的内容会默认存储在环境变量 `$REPLY` 中。

### 常见用法

```bash
# 最简单的用法，程序会停下来等待用户输入并按回车。
read name

# 使用 `-p` 添加提示语
read -p "请输入年龄: " age

# 使用 `-s` 隐藏输入（用于密码）
read -sp "请输入密码: " password

# 使用 `-n` 或 `-N` 限制字符数（读取固定数量的字符后自动结束，无需按回车。常用于“Yes/No”的选择。）
read -n 1 -p "是否继续? (y/n): " answer

# 使用 `-t` 设置超时时间，防止程序死等。
if ! read -rp "10 秒内输入 continue，否则退出: " -t 10 input; then
   echo "超时，退出"
   exit 1
fi

# 使用 `-a` 读取到数组（将输入的一行内容按照分隔符拆分并存入数组。）
read -a colors -p "输入三种颜色（空格隔开）: "
echo "第二种颜色是: ${colors[1]}"
```

### 进阶：如何处理文件内容

`read` 常与 `while` 循环配合使用，用于**逐行读取文件**。这是运维脚本中最常见的场景之一。

```bash
cat file.txt | while read line
do
    echo "正在处理行内容: $line"
done
```

_注：在处理包含特殊字符或反斜杠的文件时，建议使用 `read -r`，它能防止反斜杠被转义。_

### 输入控制脚本执行

这是 `read` 的标准用法之一，而且在工程脚本里非常常见。核心思路是：**循环读取 → 校验输入 → 不满足就继续阻塞**。

1. 最规范、可读性最强（强烈推荐）

   ```bash
   while true; do
       read -rp ">>> 输入 continue / c 继续: " input
       case "$input" in
           continue|c)
               break
               ;;
           *)
               echo "请输入 continue 或 c"
               ;;
       esac
   done
   ```

   **优点**
   - 语义清晰
   - 易扩展（以后加 `quit` / `help` 很方便）
   - 工程脚本最常见写法

2. 严格模式兼容（`set -u` 安全）

   如果脚本最开始设置了 `set -euo pipefail`，推荐用这种：

   ```bash
   while true; do
       read -rp ">>> 输入 continue 继续执行: " input || continue
       input=${input,,}   # 转小写（bash >= 4）
       [ "$input" = "continue" ] && break
       echo "请输入 continue"
   done
   ```

   `read || continue` 可以避免 **EOF / Ctrl+D** 导致脚本退出。

3. 支持超时（自动继续 / 自动退出）

   ```bash
   # 超时继续
   if read -rp "10 秒内输入 continue 继续（超时自动继续）: " -t 10 input; then
       [ "$input" != "continue" ] && echo "输入错误，继续执行"
   fi
   # 超时退出
   if ! read -rp "10 秒内输入 continue，否则退出: " -t 10 input; then
       echo "超时，退出"
       exit 1
   fi
   ```

4. **生产级暂停点函数模板**

   ```bash
   pause_until_continue() {
       while true; do
           read -rp ">>> 输入 continue 继续执行: " input || continue
           [ "${input,,}" = "continue" ] && break
           echo "请输入 continue"
       done
   }
   ```

   直接在脚本中：

   ```bash
   pause_until_continue
   run_cmd
   ```
