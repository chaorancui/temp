[toc]

## subprocess 模块

`subprocess` 模块是 Python 中用于执行外部命令和与之交互的强大工具。以下是 `subprocess` 模块的常见用法及其详细说明。

### run 函数说明

`subprocess.run()`

```python
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None, universal_newlines=None)
```

**参数说明：**

- **`args`**: 要执行的命令及其参数，可以是一个字符串或者一个列表。
- **`stdin`**: 指定输入流，默认为 `None`，表示不接受输入。
- **`input`**: 要传递给命令的输入数据。如果指定了 `input`，则 `stdin` 必须是 `PIPE`。
- **`stdout`**, **`stderr`**: 分别指定标准输出和标准错误的输出流，可以是 `subprocess.PIPE`、`subprocess.DEVNULL` 或者一个文件描述符。如果不指定，默认会将输出打印到控制台。
- **`capture_output`**: 如果设置为 `True`，则 `stdout` 和 `stderr` 将会捕获输出，并作为 `CompletedProcess` 对象的属性返回。如果同时设置了 `stdout` 或 `stderr`，则会引发 `ValueError`。
- **`shell`**: 如果为 `True`，则将通过系统 shell 执行命令。
- **`cwd`**: 指定命令的工作目录。
- **`timeout`**: 设置命令的超时时间（秒），超过此时间将引发 `TimeoutExpired` 异常。
- **`check`**: 如果为 `True`，且命令返回非零退出状态码，则引发 `CalledProcessError` 异常。
- **`encoding`**, **`errors`**: 控制 `input`、`stdout` 和 `stderr` 的编码和错误处理方式。
- **`text`**: Python 3.7+ 中的参数，如果为 `True`，则 `input`、`stdout` 和 `stderr` 将会是文本模式，而不是字节模式。在 Python 3.7+ 中，`text` 和 `universal_newlines` 是等价的，都用于指定输入输出为文本模式。
- **`env`**: 设置子进程的环境变量。
- **`universal_newlines`**: Python 3.6 中的参数，如果为 `True`，则 `input`、`stdout` 和 `stderr` 将会是文本模式，而不是字节模式。在 Python 3.7+ 推荐使用 `text` 参数代替。

**返回值：**

`subprocess.run()` 返回一个 `CompletedProcess` 对象，该对象包含执行命令的结果，如返回码、标准输出和标准错误等信息。

### 基本用法

**执行命令并等待其完成**

```python
import subprocess

# 执行命令并等待完成
result = subprocess.run(['ls', '-l'], capture_output=True, text=True)

# 输出结果
print(result.stdout)
```

- `capture_output=True`: 捕获标准输出和标准错误。
- `text=True`: 输出以文本而不是字节形式返回。

**获取返回状态**

可以获取命令的返回码，标准输出和标准错误。

```python
import subprocess

result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
print(f'Return code: {result.returncode}')
print(f'Stdout: {result.stdout.decode("utf-8")}')
print(f'Stderr: {result.stderr}')
```

在 Python 中，`result.stdout.decode("utf-8")` 是一个常见的操作，用于将**字节对象（bytes）转换为字符串（str）**，并指定使用 UTF-8 编码进行解码。这种操作通常在处理通过标准输出捕获的命令行输出时非常有用，特别是当输出包含非 ASCII 字符或者是 UTF-8 编码的文本时。

### 高级用法

#### `subprocess.Popen()`

`Popen` 提供了更强的控制，可以在进程运行时进行交互。

```python
import subprocess

# 启动一个进程
proc = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 等待命令完成并获取输出
stdout, stderr = proc.communicate()

print(f'Stdout: {stdout.decode()}')
print(f'Stderr: {stderr.decode()}')
```

#### 使用管道将一个命令的输出作为另一个命令的输入

```python
import subprocess

# 第一个命令
proc1 = subprocess.Popen(['echo', 'Hello World'], stdout=subprocess.PIPE)

# 第二个命令
proc2 = subprocess.Popen(['grep', 'Hello'], stdin=proc1.stdout, stdout=subprocess.PIPE)

# 获取输出
output = proc2.communicate()[0]
print(output.decode())
```

#### 异步执行

使用 `asyncio` 和 `subprocess` 可以异步运行命令。

```python
import asyncio
import subprocess

async def run_command(cmd):
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return stdout.decode(), stderr.decode()

async def main():
    stdout, stderr = await run_command(['ls', '-l'])
    print(stdout)
    print(stderr)

asyncio.run(main())
```

### 参数解释

- `args`: 要执行的命令及其参数，可以是列表或字符串。
- `stdout`: 标准输出的处理方式，如 `subprocess.PIPE`、`subprocess.DEVNULL`。
- `stderr`: 标准错误的处理方式，如 `subprocess.PIPE`、`subprocess.DEVNULL`。
- `stdin`: 标准输入的处理方式，如 `subprocess.PIPE`。
- `shell`: 如果为 `True`，将通过 shell 执行命令。

### 使用 `shell=True`

虽然 `shell=True` 可以让你直接传递命令字符串，但使用时要注意安全问题，特别是在处理用户输入时。

```python
import subprocess

# 使用 shell=True 运行命令
result = subprocess.run('ls -l | grep py', shell=True, capture_output=True, text=True)
print(result.stdout)
```

### 处理超时

可以设置超时，如果命令在指定时间内未完成，将会引发 `subprocess.TimeoutExpired` 异常。

```python
import subprocess

try:
    result = subprocess.run(['sleep', '10'], timeout=5)
except subprocess.TimeoutExpired:
    print('Process timed out')
```

### 实际使用示例

#### 简单命令执行

```python
import subprocess

result = subprocess.run(['echo', 'Hello World'], capture_output=True, text=True)
print(result.stdout)  # 输出: Hello World
```

#### 捕获错误输出

```python
import subprocess

result = subprocess.run(['ls', '/nonexistentpath'], capture_output=True, text=True)
print(f'Return code: {result.returncode}')
print(f'Stdout: {result.stdout}')
print(f'Stderr: {result.stderr}')
```

#### 交互式命令

```python
import subprocess

proc = subprocess.Popen(['cat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
stdout, stderr = proc.communicate(input='Hello\nWorld\n')
print(stdout)
```

### 总结

`subprocess` 模块提供了灵活而强大的方法来执行和管理外部命令。对于简单的命令执行，`subprocess.run` 是最方便的，而对于更复杂的交互需求，可以使用 `subprocess.Popen`。在使用 `shell=True` 时，要特别注意安全问题。通过了解这些用法，可以有效地在 Python 程序中集成外部命令。

## stat 模块

Python 中的 `stat` 模块用于在处理文件和目录时访问**文件状态信息**和**文件类型信息**。它提供了许多常量和函数来检查和操作文件的状态信息，这在处理文件系统相关的操作时非常有用。

### 常用常量

`stat` 模块中定义了一些常量来表示不同的文件类型和模式：

- 文件**类型常量**：

  - `stat.S_IFMT`：文件类型的位掩码
  - `stat.S_IFDIR`：目录
  - `stat.S_IFCHR`：字符设备
  - `stat.S_IFBLK`：块设备
  - `stat.S_IFREG`：常规文件
  - `stat.S_IFIFO`：FIFO 管道
  - `stat.S_IFLNK`：符号链接
  - `stat.S_IFSOCK`：套接字

- 文件**模式常量**（权限位）：

  - `stat.S_IRUSR`：用户读权限
  - `stat.S_IWUSR`：用户写权限
  - `stat.S_IXUSR`：用户执行权限
  - `stat.S_IRGRP`：组读权限
  - `stat.S_IWGRP`：组写权限
  - `stat.S_IXGRP`：组执行权限
  - `stat.S_IROTH`：其他用户读权限
  - `stat.S_IWOTH`：其他用户写权限
  - `stat.S_IXOTH`：其他用户执行权限
  - `stat.S_IRWXU` 是 `stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR` 的组合，用于表示所有者对文件的全部权限（读、写和执行）。
  - `stat.S_IRWXG` 和 `stat.S_IRWXO` 同理。

  ```python
  S_ISUID = 0o4000  # set UID bit
  S_ISGID = 0o2000  # set GID bit
  S_ENFMT = S_ISGID # file locking enforcement
  S_ISVTX = 0o1000  # sticky bit
  S_IREAD = 0o0400  # Unix V7 synonym for S_IRUSR
  S_IWRITE = 0o0200 # Unix V7 synonym for S_IWUSR
  S_IEXEC = 0o0100  # Unix V7 synonym for S_IXUSR
  S_IRWXU = 0o0700  # mask for owner permissions
  S_IRUSR = 0o0400  # read by owner
  S_IWUSR = 0o0200  # write by owner
  S_IXUSR = 0o0100  # execute by owner
  S_IRWXG = 0o0070  # mask for group permissions
  S_IRGRP = 0o0040  # read by group
  S_IWGRP = 0o0020  # write by group
  S_IXGRP = 0o0010  # execute by group
  S_IRWXO = 0o0007  # mask for others (not in group) permissions
  S_IROTH = 0o0004  # read by others
  S_IWOTH = 0o0002  # write by others
  S_IXOTH = 0o0001  # execute by others
  ```

### 常用函数

- `stat.filemode(mode)`：将文件模式转换为字符串表示形式。
- `stat.S_ISDIR(mode)`：如果文件是目录，则返回 True。
- `stat.S_ISCHR(mode)`：如果文件是字符设备，则返回 True。
- `stat.S_ISBLK(mode)`：如果文件是块设备，则返回 True。
- `stat.S_ISREG(mode)`：如果文件是常规文件，则返回 True。
- `stat.S_ISFIFO(mode)`：如果文件是 FIFO 管道，则返回 True。
- `stat.S_ISLNK(mode)`：如果文件是符号链接，则返回 True。
- `stat.S_ISSOCK(mode)`：如果文件是套接字，则返回 True。

### 示例

#### 获取文件状态信息

可以使用 `os.stat()` 或 `os.lstat()` 获取文件状态信息：

```python
import os
import stat

# 获取文件状态
file_stat = os.stat('example.txt')

# 打印文件模式
print(f"File mode: {file_stat.st_mode}")

# 打印文件大小
print(f"File size: {file_stat.st_size} bytes")

# 打印文件的最后访问时间
print(f"Last accessed: {file_stat.st_atime}")

# 打印文件的最后修改时间
print(f"Last modified: {file_stat.st_mtime}")

# 打印文件的创建时间
print(f"Creation time: {file_stat.st_ctime}")
```

#### 检查文件类型

使用 `stat` 模块的函数来检查文件类型：

```python
import os
import stat

# 获取文件状态
file_stat = os.stat('example.txt')

# 检查是否为目录
if stat.S_ISDIR(file_stat.st_mode):
    print("This is a directory.")
else:
    print("This is not a directory.")

# 检查是否为常规文件
if stat.S_ISREG(file_stat.st_mode):
    print("This is a regular file.")
else:
    print("This is not a regular file.")
```

#### 转换文件模式为字符串表示

```python
import os
import stat

# 获取文件状态
file_stat = os.stat('example.txt')

# 将文件模式转换为字符串表示
mode_string = stat.filemode(file_stat.st_mode)
print(f"File mode string: {mode_string}")
```

**总结**：

`stat` 模块在处理文件和目录的状态信息时非常有用。通过结合使用 `os` 模块和 `stat` 模块，可以方便地获取文件的详细信息并执行各种检查。无论是查看文件权限、确定文件类型还是获取文件的时间戳信息，`stat` 模块都提供了便捷的方法来实现这些操作。

## logging 模块

在 Python 中，`logging` 是一个标准库模块，用于记录程序运行时的日志信息。通过合理使用 `logging` 模块，可以帮助开发者更好地理解程序运行过程中的状态和问题，从而更轻松地进行调试和故障排查。

### 用法介绍

1. **基础用法：**

   ```python
   import logging

   # 设置基本配置
   logging.basicConfig(
       level=logging.INFO,  # 日志级别
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 日志格式
       filename='app.log'  # 日志文件
   )

   # 使用日志
   logging.debug('调试信息')
   logging.info('一般信息')
   logging.warning('警告信息')
   logging.error('错误信息')
   logging.critical('严重错误信息')
   ```

   上述格式中：

   - `%(asctime)s` 表示日志记录的时间
   - `%(levelname)s` 表示日志级别名称
   - `%(message)s` 表示日志消息

   format 宽度及对齐:

   `logging` 中，`Formatter` 支持 **标准的 Python 字符串格式化语法**，也就是说你可以在格式化字符串里指定 **最小宽度、对齐方式**，类似 Python 的 f-string 或 `%` 格式化。

   | 对齐方式 | 格式示例            | 说明                   |
   | -------- | ------------------- | ---------------------- |
   | 左对齐   | `%-20s` 或 `{:<20}` | 字符串占 20 位，左对齐 |
   | 右对齐   | `%20s` 或 `{:>20}`  | 字符串占 20 位，右对齐 |
   | 居中     | `{:^20}`            | 字符串居中，占 20 位   |

2. **创建自定义 logger，将日志同时输出到控制台和文件**

   ```python
   import logging

   # 创建logger
   logger = logging.getLogger('my_app')
   logger.setLevel(logging.DEBUG)

   # 创建文件处理器
   file_handler = logging.FileHandler('app.log')
   file_handler.setLevel(logging.INFO)

   # 创建控制台处理器
   console_handler = logging.StreamHandler()
   console_handler.setLevel(logging.DEBUG)

   # 创建格式器
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   file_handler.setFormatter(formatter)
   console_handler.setFormatter(formatter)

   # 添加处理器到logger
   logger.addHandler(file_handler)
   logger.addHandler(console_handler)

   # 使用logger
   logger.debug('This is a debug message')
   logger.info('This is an info message')
   logger.warning('This is a warning message')
   ```

3. **在实际项目中的完整示例：**

   ```python
   import logging
   import logging.handlers
   import os

   def setup_logger(name, log_file, level=logging.INFO):
       """创建一个logger"""

       # 创建logger目录
       log_dir = os.path.dirname(log_file)
       if not os.path.exists(log_dir):
           os.makedirs(log_dir)

       # 创建logger
       logger = logging.getLogger(name)
       logger.setLevel(level)

       # 创建TimedRotatingFileHandler
       file_handler = logging.handlers.TimedRotatingFileHandler(
           log_file,
           when='midnight',  # 每天午夜切换文件
           interval=1,       # 间隔为1天
           backupCount=30    # 保留30天的日志
       )
       file_handler.setLevel(level)

       # 创建StreamHandler
       console_handler = logging.StreamHandler()
       console_handler.setLevel(level)

       # 创建formatter
       formatter = logging.Formatter(
           '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
       )

       # 设置formatter
       file_handler.setFormatter(formatter)
       console_handler.setFormatter(formatter)

       # 添加handlers
       logger.addHandler(file_handler)
       logger.addHandler(console_handler)

       return logger

   # 使用示例
   class UserService:
       def __init__(self):
           self.logger = setup_logger(
               'user_service',
               'logs/user_service.log',
               logging.DEBUG
           )

       def create_user(self, username):
           try:
               self.logger.info(f'开始创建用户: {username}')
               # 业务逻辑
               if not username:
                   raise ValueError('用户名不能为空')
               # 更多业务逻辑...
               self.logger.info(f'用户创建成功: {username}')
           except Exception as e:
               self.logger.error(f'创建用户失败: {str(e)}', exc_info=True)
               raise

   # 使用服务
   if __name__ == '__main__':
       service = UserService()
       try:
           service.create_user('')
       except Exception:
           pass
       service.create_user('alice')
   ```

4. **使用配置文件：**

   ```python
   # logging_config.py
   import logging.config
   import yaml

   # 配置文件示例 (logging_config.yaml)
   config = """
   version: 1
   formatters:
     simple:
       format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
     detailed:
       format: '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'

   handlers:
     console:
       class: logging.StreamHandler
       level: DEBUG
       formatter: simple
       stream: ext://sys.stdout

     file:
       class: logging.handlers.TimedRotatingFileHandler
       level: INFO
       formatter: detailed
       filename: logs/app.log
       when: midnight
       interval: 1
       backupCount: 30
       encoding: utf8

   loggers:
     my_app:
       level: DEBUG
       handlers: [console, file]
       propagate: no

   root:
     level: INFO
     handlers: [console]
   """

   # 加载配置
   def setup_logging():
       config_dict = yaml.safe_load(config)
       logging.config.dictConfig(config_dict)

   # 使用示例
   if __name__ == '__main__':
       setup_logging()
       logger = logging.getLogger('my_app')

       logger.debug('调试信息')
       logger.info('一般信息')
       logger.warning('警告信息')
   ```

**主要注意点**：

1. 日志级别（从低到高）：

   - DEBUG: 详细调试信息
   - INFO: 一般信息
   - WARNING: 警告信息
   - ERROR: 错误信息
   - CRITICAL: 严重错误信息

2. 最佳实践：

   - 每个模块使用独立的 logger
   - 使用适当的日志级别
   - 配置日志轮转避免文件过大
   - 包含足够的上下文信息
   - 在异常处理中使用 exc_info=True 记录堆栈信息

3. 性能考虑：

   - 使用 lazy logging: `logger.debug('User %s logged in', username)` 而不是 `logger.debug(f'User {username} logged in')`
   - 适当设置日志级别，避免过多日志
   - 考虑使用异步日志处理器处理大量日志

Python 的 `logging` 模块提供了多种 **handlers** 用于将日志输出到不同的目的地。`handlers` 允许你将日志信息输出到控制台、文件、远程服务器等，而不是直接在代码中使用简单的打印语句。相比直接使用 `print()` 或手动写入文件，使用 `logging` 模块的好处在于它提供了更丰富的功能，如日志级别、格式化、日志轮转、输出到多个目的地等。

### 高级用法

1. **将日志记录到文件**

   可以通过设置 `filename` 参数将日志记录到文件中：

   ```python
   logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
   ```

2. **添加处理程序**

   可以添加多个处理程序，比如同时输出到控制台和文件：

   ```python
   console_handler = logging.StreamHandler()
   file_handler = logging.FileHandler('app.log')
   handlers = [console_handler, file_handler]

   logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=handlers)
   ```

### 常用 `handlers`

1. **StreamHandler**

   - 将日志输出到流（通常是控制台）。
   - 适用于开发调试时，实时查看日志。

   ```python
   import logging

   logger = logging.getLogger('my_logger')
   handler = logging.StreamHandler()  # 输出到控制台
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   handler.setFormatter(formatter)
   logger.addHandler(handler)

   logger.setLevel(logging.DEBUG)
   logger.debug('This is a debug message')
   ```

2. **FileHandler**

   - 将日志输出到文件。
   - 适用于生产环境中记录日志。

   ```python
   handler = logging.FileHandler('my_log.log')  # 输出到文件
   handler.setFormatter(formatter)
   logger.addHandler(handler)

   logger.setLevel(logging.INFO)
   logger.info('This is an info message')
   ```

3. **RotatingFileHandler**

   - 将日志输出到文件并在文件大小达到一定阈值时自动进行文件轮换。
   - 适用于日志文件会随着时间增长而变得很大的情况。

   ```python
   handler = logging.handlers.RotatingFileHandler(
       'my_rotating_log.log', maxBytes=2000, backupCount=5
   )  # 设置最大文件大小和备份数量
   handler.setFormatter(formatter)
   logger.addHandler(handler)

   logger.setLevel(logging.DEBUG)
   for i in range(1000):
       logger.debug(f'Debug message {i}')
   ```

4. **TimedRotatingFileHandler**

   - 将日志输出到文件并根据时间周期进行日志轮换（如每天、每小时等）。
   - 适用于按时间进行日志文件管理的场景。

   ```python
   from logging.handlers import TimedRotatingFileHandler

   handler = TimedRotatingFileHandler(
       'timed_log.log', when='midnight', interval=1, backupCount=7
   )  # 每天午夜轮换日志，保留7天的日志
   handler.setFormatter(formatter)
   logger.addHandler(handler)

   logger.setLevel(logging.INFO)
   logger.info('This is a timed log message')
   ```

5. **SocketHandler**

   - 将日志发送到远程的日志服务器，通过网络连接。
   - 适用于集中化日志管理的场景。

   ```python
   handler = logging.handlers.SocketHandler('localhost', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
   handler.setFormatter(formatter)
   logger.addHandler(handler)

   logger.setLevel(logging.ERROR)
   logger.error('This is an error message sent to a remote server')
   ```

6. **SMTPHandler**

   - 将日志通过电子邮件发送。
   - 适用于在特定错误发生时需要立即通知相关人员的情况。

   ```python
   from logging.handlers import SMTPHandler

   mail_handler = SMTPHandler(
       mailhost='smtp.example.com',
       fromaddr='your_email@example.com',
       toaddrs=['recipient@example.com'],
       subject='Error Log'
   )
   mail_handler.setFormatter(formatter)
   logger.addHandler(mail_handler)

   logger.setLevel(logging.ERROR)
   logger.error('This is an error message sent by email')
   ```

**使用 `handlers` 的优势**

- **日志级别控制**：通过 `handlers`，你可以对不同的输出目标设置不同的日志级别。例如，你可以将控制台输出限制为 `DEBUG`，而将文件输出限制为 `INFO` 或更高的级别。
- **灵活的输出目标**：`handlers` 使得你可以轻松地将日志输出到多个不同的地方，比如控制台、文件、邮件、网络服务器等。
- **日志轮换**：使用 `RotatingFileHandler` 或 `TimedRotatingFileHandler`，你可以设置日志文件的大小或时间，自动进行轮换并保存备份。这对于长期运行的应用程序非常有用，避免日志文件过大。
- **格式化日志**：通过设置 `Formatter`，你可以控制日志的输出格式，包括时间戳、日志级别、消息内容等，使日志更加可读和结构化。
- **日志集中管理**：`SocketHandler` 和其他类似的 `handlers` 可以将日志信息集中到一个服务器上，便于多台机器或应用程序的日志汇总，便于监控和分析。

**总结**

- **优势**：
  - 提供多种日志输出方式（控制台、文件、网络等）。
  - 支持日志级别控制。
  - 提供日志轮换功能，避免日志文件过大。
  - 支持格式化输出，使日志易于阅读和分析。
  - 可以集中管理多个日志来源，适用于分布式应用。
- **如何使用**：
  - 创建适当的 `Handler`（如 `StreamHandler`, `FileHandler` 等）。
  - 配置日志格式（`Formatter`）。
  - 将 `Handler` 添加到 `Logger`。
  - 可以使用多个 `Handler` 将日志输出到不同的目标（如控制台和文件）。

### 缓冲区

同时使用 `logging` 和 `print()`，会出现**输出交错顺序不稳定**，这是 Python I/O 缓冲机制导致的常见问题。下面详细分析原因和解决方案。

一、为什么输出顺序可能混乱

1. **缓冲区机制不同**

   - `print()` 默认写入 **`sys.stdout`**，默认是 **行缓冲**（line-buffered），在终端上通常每行立即刷新，但如果重定向到文件或管道，可能变为全缓冲（buffered）。
   - `logging` 默认使用 **`StreamHandler`** 写入 **`sys.stderr`**，也是缓冲的，但和 `stdout` 的缓冲区独立。

   > 也就是说，你的 `print()` 写在 `stdout`，`logging` 写在 `stderr`，两个缓冲区不同步，所以打印顺序看起来乱。

2. **多线程或异步写入**

   - 如果程序里有多线程或异步处理，每个线程写 `stdout`/`stderr` 的顺序也可能不一致。

二、如何保证输出顺序正常

1. 统一输出到 **stdout**

   ```python
   import logging
   import sys

   logging.basicConfig(
       stream=sys.stdout,   # 原来是 stderr，改为 stdout
       level=logging.DEBUG,  # 日志级别 DEBUG/INFO/WARNING/ERROR/CRITICAL
       format='%(asctime)s - %(name)s - %(levelname)-7s - %(message)s'  # 日志格式
   )
   ```

   - 这样 `logging` 和 `print` 都写到同一个缓冲区。
   - 注意仍需确保刷新。

2. 在 `print` 中加 `flush=True`

   ```python
   print("some info", flush=True)
   ```

   - 强制立即刷新 `stdout`，防止和 `logging` 的输出错位。

3. 在 `logging` 里使用 `flush`

   `StreamHandler` 默认会在每条消息后 flush，但如果自定义 Handler，确保：

   ```python
   handler = logging.StreamHandler(sys.stdout)
   handler.flush = True
   ```

4. 全部使用 `logging`，不要混用 `print`

   - 如果你把所有输出都改为 `logging.info/warning/debug`，默认输出顺序会更稳定。
   - 可以自定义不同日志级别显示不同颜色或者前缀替代 print。

5. 强制同步

   ```python
   import sys
   sys.stdout.flush()
   sys.stderr.flush()
   ```

   - 在关键点手动刷新 stdout/stderr，保证两者顺序正确。

**总结**：

- `print()` 写 `stdout`，`logging` 默认写 `stderr` → 两个缓冲区独立 → 输出顺序可能混乱。
- 解决办法：
  1. 统一输出到同一个流（stdout 或 stderr）
  2. 强制 flush（`flush=True` 或 `sys.stdout.flush()`）
  3. 尽量只用 `logging`，不要混用 `print`

## struct 模块

Python 中的 `struct` 模块用于在**字节串和 Python 原生数据类型之间进行转换**。这个模块非常有用，尤其是在处理二进制数据或与 C 语言的结构进行交互时。

### 常用函数

- `struct.pack(fmt, v1, v2, ...)`：将 Python 值打包成二进制数据。
- `struct.unpack(fmt, buffer)`：从二进制数据中解包出 Python 值。
- `struct.calcsize(fmt)`：计算格式字符串表示的结构的大小。

### 格式字符串

格式字符串（`fmt`）用于指定要打包或解包的数据的类型和顺序。常见的格式字符包括：

- `c`：char（1 字节）
- `b`：signed char（1 字节）
- `B`：unsigned char（1 字节）
- `h`：short（2 字节）
- `H`：unsigned short（2 字节）
- `i`：int（4 字节）
- `I`：unsigned int（4 字节）
- `f`：float（4 字节）
- `d`：double（8 字节）
- `s`：char[]（字符串）
- `p`：pascal string
- `P`：void \*（指针）

### 示例

#### 打包和解包整数

```python
import struct

# 打包数据
packed_data = struct.pack('i', 42)
print(f'Packed Data: {packed_data}') # Packed Data: b'*\x00\x00\x00'

# 解包数据
unpacked_data = struct.unpack('i', packed_data)
print(f'Unpacked Data: {unpacked_data[0]}') # Unpacked Data: 42
```

#### 打包和解包多个值

```python
# 打包数据
packed_data = struct.pack('i4sh', 42, b'test', 7)
print(f'Packed Data: {packed_data}') # Packed Data: b'*\x00\x00\x00test\x07\x00'

# 解包数据
unpacked_data = struct.unpack('i4sh', packed_data)
print(f'Unpacked Data: {unpacked_data}') # Unpacked Data: (42, b'test', 7)
```

#### 计算结构大小

```python
size = struct.calcsize('i4sh')
print(f'Structure Size: {size} bytes') # Structure Size: 10 bytes
```

**示例解释**：

1. **打包和解包整数**：我们使用 `struct.pack('i', 42)` 将整数 42 打包成二进制数据，并使用 `struct.unpack('i', packed_data)` 将其解包回整数。
2. **打包和解包多个值**：我们将一个整数、一个字符串和一个短整数打包在一起，并解包成原始值。
3. **计算结构大小**：我们计算格式字符串 `'i4sh'` 表示的结构在字节中的大小。

### 进阶用法

#### 处理字节序

默认情况下，`struct` 按照本地字节序处理数据。你可以在格式字符串前添加字符来指定字节序：

- `@`：原生字节序（默认）
- `<`：小端字节序
- `>`：大端字节序
- `=`：标准字节序（与本地字节序相同）
- `!`：网络字节序（大端）

```python
# 小端字节序
packed_data = struct.pack('<i', 42)
print(f'Small Endian Packed Data: {packed_data}')

# 大端字节序
packed_data = struct.pack('>i', 42)
print(f'Big Endian Packed Data: {packed_data}')
```

#### 处理浮点数

```python
# 打包浮点数
packed_data = struct.pack('f', 3.14)
print(f'Packed Float Data: {packed_data}')

# 解包浮点数
unpacked_data = struct.unpack('f', packed_data)
print(f'Unpacked Float Data: {unpacked_data[0]}')
```

**总结**：

`struct` 模块提供了一种高效的方法来处理二进制数据。通过指定格式字符串，你可以灵活地在 Python 值和二进制数据之间进行转换。这在**处理网络协议、文件格式或其他低级别数据处理任务时**非常有用。

## operator 模块

Python 中的 `operator` 模块提供了**一系列函数来对应 Python 内置运算符**。这些函数可以用于代替传统的运算符进行操作，尤其**在需要将运算符作为函数传递**的情况下非常有用，比如在 `map()`, `filter()`, `sorted()` 等函数中使用。

### 常用函数

以下是 `operator` 模块中一些常用的函数：

#### 算术运算符函数

- `operator.add(a, b)`：返回 `a + b`
- `operator.sub(a, b)`：返回 `a - b`
- `operator.mul(a, b)`：返回 `a * b`
- `operator.truediv(a, b)`：返回 `a / b`
- `operator.floordiv(a, b)`：返回 `a // b`
- `operator.mod(a, b)`：返回 `a % b`
- `operator.pow(a, b)`：返回 `a ** b`

#### 比较运算符函数

- `operator.eq(a, b)`：返回 `a == b`
- `operator.ne(a, b)`：返回 `a != b`
- `operator.gt(a, b)`：返回 `a > b`
- `operator.ge(a, b)`：返回 `a >= b`
- `operator.lt(a, b)`：返回 `a < b`
- `operator.le(a, b)`：返回 `a <= b`

#### 逻辑运算符函数

- `operator.and_(a, b)`：返回 `a & b`
- `operator.or_(a, b)`：返回 `a | b`
- `operator.xor(a, b)`：返回 `a ^ b`
- `operator.not_(a)`：返回 `not a`

#### 序列运算符函数

- `operator.concat(a, b)`：返回连接 `a` 和 `b`
- `operator.contains(a, b)`：返回 `b in a`
- `operator.itemgetter(*items)`：返回一个函数，该函数获取给定位置上的元素
- `operator.attrgetter(*attrs)`：返回一个函数，该函数获取给定属性的值
- `operator.methodcaller(name, *args, **kwargs)`：返回一个函数，该函数调用给定的方法

### 示例

#### 算术运算符函数

```python
import operator

a = 10
b = 5

print(operator.add(a, b))       # 输出: 15
print(operator.sub(a, b))       # 输出: 5
print(operator.mul(a, b))       # 输出: 50
print(operator.truediv(a, b))   # 输出: 2.0
print(operator.floordiv(a, b))  # 输出: 2
print(operator.mod(a, b))       # 输出: 0
print(operator.pow(a, b))       # 输出: 100000
```

#### 比较运算符函数

```python
print(operator.eq(a, b))  # 输出: False
print(operator.ne(a, b))  # 输出: True
print(operator.gt(a, b))  # 输出: True
print(operator.ge(a, b))  # 输出: True
print(operator.lt(a, b))  # 输出: False
print(operator.le(a, b))  # 输出: False
```

#### 序列运算符函数

```python
lst = [1, 2, 3, 4, 5]

# 检查元素是否在列表中
print(operator.contains(lst, 3))  # 输出: True

# 获取指定位置的元素
itemgetter = operator.itemgetter(1, 3)
print(itemgetter(lst))  # 输出: (2, 4)

# 获取对象的属性
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person('Alice', 30)
attrgetter = operator.attrgetter('name', 'age')
print(attrgetter(person))  # 输出: ('Alice', 30)

# 调用对象的方法
methodcaller = operator.methodcaller('upper')
print(methodcaller('hello'))  # 输出: 'HELLO'
```

### 实际应用示例

#### 在排序中使用 `itemgetter`

```python
from operator import itemgetter

students = [
    {'name': 'John', 'age': 25, 'grade': 'B'},
    {'name': 'Jane', 'age': 22, 'grade': 'A'},
    {'name': 'Dave', 'age': 23, 'grade': 'C'}
]

# 按年龄排序
sorted_students = sorted(students, key=itemgetter('age'))
print(sorted_students)
```

#### 在 `map` 和 `filter` 中使用 `operator` 函数

```python
from operator import add, mul
numbers = [1, 2, 3, 4, 5]

# 使用 map 进行加法操作
result = list(map(add, numbers, [10, 10, 10, 10, 10]))
print(result)  # 输出: [11, 12, 13, 14, 15]

# 使用 filter 进行乘法操作
result = list(filter(lambda x: operator.gt(x, 10), map(mul, numbers, [2, 2, 2, 2, 2])))
print(result)  # 输出: [12, 14]
```

### 总结

`operator` 模块提供了一组函数来代替内置运算符，使得**在需要将运算符作为函数传递**的情况下更加方便和灵活。这对于函数式编程风格的 Python 代码特别有用。

## xlrd 和 xlwt

### xlrd

xlrd 是一个从 Excel 文件读取数据和格式化信息的库，支持.xls 以及.xlsx 文件。

<http://xlrd.readthedocs.io/en/latest/>

- xlrd 支持.xls，.xlsx 文件的读.
- 通过设置 on_demand 变量使 open_workbook()函数只加载那些需要的 sheet，从而节省时间和内存(该方法对.xlsx 文件无效)。
- xlrd.Book 对象有一个 unload_sheet 方法，它将从内存中卸载工作表，由工作表索引或工作表名称指定(该方法对.xlsx 文件无效)

### xlwt

xlwt 是一个用于将数据和格式化信息写入旧 Excel 文件的库(如.xls)。

<https://xlwt.readthedocs.io/en/latest/>

- xlwt 支持.xls 文件写。

## XML

读取 xml：

```python
 root = ElementTree.parse(r"/Users/..../Documents/111.xml")
 root = ElementTree.fromstring(text)
```

遍历：

for node in root.iter():
print type(node)
元素标签名 node.tag
元素标签属性名称、属性值 node.attrib
获取元素属性对应的值 node.attrib.get('id','NULL') # 不存在则取默认值 NULL，不指定默认值不存在时报错
元素属性二元组 node.attrib.items()
元素属性列表 node.attrib.keys()
该结点的所有子节点中选择符合元素名称的第一个子节点 node.find('xxx')
该结点的所有子节点中选择符合元素名称的所有子节点 node.findall('xxx')
所有子节点以列表形式给出 node.getchildren()
遍历所有子树 node.iter()

[`xml.etree.ElementTree`](https://docs.python.org/3.6/library/xml.etree.elementtree.html#module-xml.etree.ElementTree)— 元素树 XML API

python ElementTree：<https://blog.csdn.net/weixin_43956958/article/details/121986040?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-1-121986040-blog-79852724.pc_relevant_recovery_v2&spm=1001.2101.3001.4242.2&utm_relevant_index=2>
