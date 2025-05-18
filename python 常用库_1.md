[toc]

# python 常用库

## 使用 `pipdeptree` 检查依赖树

使用 `pipdeptree` 工具可以帮助你可视化和理解当前环境中的依赖关系，找出可能的冲突。

首先，安装 `pipdeptree`：

```shell
pip install pipdeptree
```

然后运行：

```shell
pipdeptree
```

这将显示所有已安装包及其依赖树，有助于你理解当前依赖关系，并手动解决冲突。

如：

```shell
NOTE: This warning isn't a failure warning.
------------------------------------------------------------------------
Warning!!! Possibly conflicting dependencies found:
* clikit==0.6.2
 - crashtest [required: >=0.3.0,<0.4.0, installed: 0.4.1]
------------------------------------------------------------------------
```

上面说明：`clikit` 版本为 `0.6.2`，它的依赖项 `crashtest` 要求的版本范围是 `>=0.3.0,<0.4.0`，但是已经安装的 `crashtest` 版本为 `0.4.1`，超出了这个范围。

你需要确保 `clikit` 和 `crashtest` 的版本是兼容的。需要**降级 `crashtest` 版本**，降级 `crashtest` 到 `0.3.x` 的版本，使其符合 `clikit` 的要求。

```shell
pip install crashtest==0.3.0
```

## OS 库

Python 的 `os` 模块提供了许多与操作系统交互的函数，可以用来管理文件和目录、执行命令、获取系统信息等。下面列举了一些常用的 `os` 模块函数及其功能：

### 系统信息和环境

1. **获取环境变量值**

   ```python
   value = os.getenv('PATH')
   ```

2. **设置环境变量**

   ```python
   os.environ['CUSTOM_VAR'] = 'value'
   ```

3. **获取操作系统名称**

   ```python
   os_name = os.name  # 返回 'posix' 或 'nt'，表示 Unix 或 Windows 系统
   ```

4. **获取系统平台信息**

   ```python
   platform = os.uname()  # 返回一个包含系统信息的元组，仅在 Unix 系统上可用
   ```

### 文件和目录操作

1. **获取当前工作目录**

   ```python
   import os

   cwd = os.getcwd()
   print("Current working directory:", cwd)
   ```

2. **改变当前工作目录**

   ```python
   os.chdir('/path/to/new/directory')
   ```

3. **创建单层目录**

   ```python
   # 注意提前判断路径为空的异常场景
   os.mkdir('/path/to/new/directory')
   ```

4. **递归创建多层目录**

   ```python
   # 注意提前判断路径为空的异常场景
   os.makedirs('/path/to/new/directory/with/multiple/levels', exist_ok=True)
   ```

5. **删除空目录**

   ```python
   os.rmdir('/path/to/empty/directory')
   ```

6. **递归删除目录及其内容**

   ```python
   import shutil

   shutil.rmtree('/path/to/directory/to/be/removed')
   ```

7. **重命名文件或目录**

   ```python
   os.rename('/path/to/old_name', '/path/to/new_name')
   ```

8. **删除文件**

   ```python
   os.remove('/path/to/file/to/be/deleted')
   os.unlink("file.txt")  # 删除文件
   ```

   `os.unlink(path, *, dir_fd=None)` 用于**删除指定路径的文件**，它的行为与 `os.remove()` 相同。

   - 如果**文件不存在**，调用 `os.unlink()` 会抛出 `FileNotFoundError`。
   - 如果 `path` 指向的是一个**目录**，会抛出 `IsADirectoryError`。删除目录应该使用 `os.rmdir()` 或 `shutil.rmtree()`。
   - 在 Linux 或 macOS 上，`os.unlink()` 也可以用于删除**符号链接**，但不会影响原始文件。

9. **复制文件**

   ```python
   import shutil

   shutil.copyfile('/path/to/source_file', '/path/to/destination_file')
   ```

10. **获取文件列表**

    ```python
    files = os.listdir('/path/to/directory')
    ```

### 文件和目录检查

1. **检查路径是否为文件或目录**

   - `os.path.isfile(path)`: 判断路径是否为文件。

   - `os.path.isdir(path)`: 判断路径是否为目录。

     ```python
     path_file = '/path/to/file.txt'
     path_directory = '/path/to/directory'

     is_file = os.path.isfile(path_file)
     is_directory = os.path.isdir(path_directory)

     print(f"{path_file} is a file:", is_file)
     print(f"{path_directory} is a directory:", is_directory)
     ```

2. **检查路径是否存在**

   - `os.path.exists(path)`: 判断路径是否存在。

     ```python
     path = '/path/to/file_or_directory'

     if os.path.exists(path):
         print(f"{path} exists!")
     else:
         print(f"{path} does not exist!")
     ```

3. **获取路径的属性**

   - `os.path.getsize(path)`: 返回指定路径文件的大小（字节数）。

   - `os.path.getmtime(path)`: 返回指定路径文件的最后修改时间（时间戳）。

   - `os.path.getctime(path)`: 返回指定路径文件的创建时间（时间戳）。

     ```python
     import time

     path = '/path/to/file.txt'

     size = os.path.getsize(path)
     last_modified = os.path.getmtime(path)
     creation_time = os.path.getctime(path)

     print(f"Size of {path}: {size} bytes")
     print(f"Last modified: {time.ctime(last_modified)}")
     print(f"Created on: {time.ctime(creation_time)}")
     ```

4. **判断路径是否是绝对路径**

   - `os.path.isabs(path)`: 判断路径是否为绝对路径。

     ```python
     path_absolute = '/absolute/path/to/file.txt'
     path_relative = 'relative/path/to/file.txt'

     is_absolute = os.path.isabs(path_absolute)
     is_relative = os.path.isabs(path_relative)

     print(f"{path_absolute} is absolute:", is_absolute)
     print(f"{path_relative} is absolute:", is_relative)
     ```

### 文件路径操作

1. **连接路径**

   - `os.path.join(path1, path2, ...)`: 将多个路径组合成一个路径。**根据操作系统的不同，使用正确的路径分隔符**。

     ```python
     import os

     path = os.path.join('/path/to', 'directory', 'file.txt')
     print(path)  # 输出: /path/to/directory/file.txt
     ```

     > 特殊情况:
     >
     > 1. 如果任意一个参数是一个绝对路径，那么它之前的所有参数都会被忽略，并从这个绝对路径开始构建：
     >
     >    ```python
     >    import os
     >
     >    # 示例路径片段
     >    path1 = "/home/user"
     >    path2 = "/etc"
     >    path3 = "file.txt"
     >
     >    # 使用 os.path.join 连接路径
     >    full_path = os.path.join(path1, path2, path3)
     >    print(full_path) # /etc/file.txt, 因为 path2 是一个绝对路径，所有之前的路径片段都会被忽略。
     >    ```
     >
     > 2. 如果某个路径片段是空字符串，`os.path.join` 会自动忽略它：
     >
     >    ```python
     >    import os
     >
     >    # 示例路径片段
     >    path1 = "/home/user"
     >    path2 = ""
     >    path3 = "documents"
     >    path4 = "file.txt"
     >
     >    # 使用 os.path.join 连接路径
     >    full_path = os.path.join(path1, path2, path3, path4)
     >    print(full_path) # /home/user/documents/file.txt
     >    ```

2. **获取绝对路径**

   - `os.path.abspath(path)`: 返回指定路径的绝对路径。

     ```python
     abs_path = os.path.abspath('relative/path/to/file.txt')
     print(abs_path)  # 输出绝对路径
     ```

3. **获取绝对路径，而不是符号链接路径**

   假设有一个符号链接指向某个文件或目录，可以使用 `realpath` 来获取实际路径：

   ```python
   import os

   # 假设 'symlink_path' 是一个符号链接的路径
   symlink_path = '/path/to/symlink'
   actual_path = os.path.realpath(symlink_path)
   print(actual_path)
   ```

   `realpath` 也可以用来将相对路径转换为绝对路径：

   ```python
   import os

   relative_path = './some/relative/path'
   absolute_path = os.path.realpath(relative_path)
   print(absolute_path)
   ```

   > **区别总结**
   >
   > - **`realpath`**：返回指定路径的真实路径，解析所有符号链接后的绝对路径。
   > - **`abspath`**：返回指定路径的绝对路径，仅仅是将给定的路径规范化成绝对路径形式。
   >
   > 如果你需要解析符号链接并获取其真实路径，应该使用`os.path.realpath`。
   >
   > 如果只需要将路径规范化成绝对路径，而不考虑符号链接的影响，则可以使用`os.path.abspath`。

4. **获取路径的目录名和文件名**

   - `os.path.dirname(path)`: 返回路径的目录名（不包括文件名）。<span style="color: blue; font-weight: bold;">注意目录名可能为空，创建文件夹要处理此异常场景。</span>

   - `os.path.basename(path)`: 返回路径的基本名称（即文件名或目录名，不包括目录路径）。

     ```python
     path = '/path/to/directory/file.txt'
     dirname = os.path.dirname(path)
     basename = os.path.basename(path)
     print("Directory:", dirname)  # 输出: /path/to/directory
     print("Filename:", basename)  # 输出: file.txt
     ```

5. **分割路径**

   - `os.path.split(path)`: 分割路径为目录名和文件名，返回元组 `(dirname, basename)`。

     ```python
     path = '/path/to/directory/file.txt'
     dirname, basename = os.path.split(path)
     print("Directory:", dirname)  # 输出: /path/to/directory
     print("Filename:", basename)  # 输出: file.txt
     ```

6. **分割文件名和扩展名**

   - `os.path.splitext(path)`: 分割文件名和扩展名，返回元组 `(filename, extension)`。

     ```python
     path = '/path/to/file.txt'
     filename, extension = os.path.splitext(path)
     print("Filename:", filename)    # 输出: /path/to/file
     print("Extension:", extension)  # 输出: .txt
     ```

### 其他常用函数

1. **执行系统命令**

   ```python
   os.system('command')
   ```

   > :star:**注意：**推荐使用 `subprocess` 模块代替 `os.system` 进行更为灵活和安全的命令执行。

2. **获取文件或目录的最后修改时间**

   ```python
   import time

   timestamp = os.path.getmtime('/path/to/file_or_directory')
   last_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
   ```

3. **获取文件或目录的权限模式**

   ```python
   mode = os.stat('/path/to/file_or_directory').st_mode
   ```

4. **判断路径是否为链接文件**

   - `os.path.islink(path)`: 判断路径是否为符号链接。

     ```python
     path_link = '/path/to/symlink'

     is_link = os.path.islink(path_link)

     print(f"{path_link} is a symbolic link:", is_link)
     ```

5. **规范化路径**

   - `os.path.normpath(path)`: 规范化路径，解析路径中的符号链接和相对路径，返回规范化的绝对路径。

     ```python
     path = '/path/to/../file.txt'

     normalized_path = os.path.normpath(path)

     print(f"Original path: {path}") # 输出："/path/to/../file.txt"
     print(f"Normalized path: {normalized_path}") # 输出："/path/file.txt"
     ```

6. **检查路径是否相同**

   - `os.path.samefile(path1, path2)`: 判断两个路径是否指向同一个文件或目录。

     ```python
     path1 = '/path/to/file1.txt'
     path2 = '/path/to/file2.txt'

     is_same = os.path.samefile(path1, path2)

     print(f"{path1} and {path2} point to the same file:", is_same)
     ```

### 常用脚本

1. 文件夹中查找特定文件
   在 Python 中查找文件夹中以 `.bin` 结尾的文件可以使用 `os` 模块。代码示例如下：

   ```shell
   import os

   # 设置要查找的文件夹路径
   folder_path = "/path/to/your/folder"

   # 查找文件夹中以 ".bin" 结尾的文件
   files = [f for f in os.listdir(folder_path) if f.endswith('.bin')]

   # 打印找到的文件列表
   for file in files:
       print(file)
   ```

   其中：

   - `folder_path` 是你要查找的文件夹路径。
   - `os.listdir(folder_path)` 列出文件夹中的所有文件。
   - `f.endswith('.bin')` 用于过滤以 `.bin` 结尾的文件。

2. 创建输出文件目录
   Python 命令参数中经常会同时指定输入文件路径和输出文件路径，而输出文件路径有时候可能不存在，需要新创建。代码示例如下：

   ```shell
   import os

   output_file = "example.txt"  # 替换为你的实际文件路径

   directory = os.path.dirname(output_file)
   if not directory: # 如果 directory 为空，设置为当前目录
       directory = "."

   os.makedirs(directory, exist_ok=True) # directory 为空，此命令会报错
   ```

## 打开文件

### open() 函数

`open()` 函数是 Python 内置的函数，用于以高级别的方式打开文件，返回一个文件对象，支持读取、写入和其他文件操作。

```python
open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
```

**参数说明：**

- **`file`**: 要打开的文件名或路径。
- **`mode`**: 打开文件的模式，可以是以下几种之一：
  - `'r'`: 只读模式（默认）。
  - `'w'`: 写入模式，如果文件存在则截断文件（清空文件内容），如果文件不存在则创建。
  - `'x'`: 独占创建模式，如果文件已存在则抛出 `FileExistsError` 异常。
  - `'a'`: 追加模式，如果文件存在，数据将被写入到文件末尾。
  - `'b'`: 以二进制模式打开文件。
  - `'t'` 或 `'r'`: 文本模式（默认）。
  - `'+'`: 更新（读取和写入）模式。
- **`buffering`**: 设置缓冲策略。0 表示不缓冲（直接写入磁盘），1 表示行缓冲（只在换行时刷新缓冲区），大于 1 表示缓冲区大小（以字节为单位）。
- **`encoding`** 和 **`errors`**: 如果文件模式包括 `'t'` 或 `'r'`，则可以指定文件编码和错误处理方式。
- **`newline`**: 控制换行符的行为。`None`（默认）表示使用系统默认的换行符；`''` 表示禁用换行符转换；`'\n'` 表示将换行符转换为 `\n`。
- **`closefd`**: 当设置为 `False` 时，传入的 `file` 参数可以是一个文件描述符而不是文件名。
- **`opener`**: 用于打开文件的自定义函数（通常用于特定文件对象的打开方式）。

**返回值：**

`open()` 函数返回一个文件对象，可以通过该对象进行读取、写入或者其他文件操作。

**示例**

1. 读取文件

   ```python
   # 以只读模式打开文件
   with open('example.txt', 'r') as file:
       content = file.read()
       print(content)
   ```

2. 写入文件

   ```python
   # 以写入模式打开文件（如果文件不存在则创建，存在则覆盖）
   with open('example.txt', 'w') as file:
       file.write('Hello, World!')
   ```

3. 追加到文件末尾

   ```python
   # 以追加模式打开文件，将数据追加到文件末尾
   with open('example.txt', 'a') as file:
       file.write('\nThis is a new line.')
   ```

4. 二进制模式读取文件

   ```python
   # 以二进制模式读取文件
   with open('image.jpg', 'rb') as file:
       image_data = file.read()
       # 对二进制数据进行处理
   ```

**注意事项**

- 在使用 `open()` 函数打开文件时，建议使用 `with` 语句（上下文管理器），以确保文件在使用完毕后会被正确关闭，从而释放系统资源。
- 对于文本文件，默认情况下使用系统默认的文本编码进行读写，但可以通过 `encoding` 参数显式指定编码，例如 `encoding='utf-8'`。
- 在处理文件时，要注意文件的打开模式和操作方式，避免意外覆盖或损坏文件内容。

### os.open() 函数

`os.open()` 函数属于 `os` 模块，用于通过底层的操作系统调用打开文件，返回一个文件描述符（integer）。

```python
os.open(file, flags, mode=0o777)
```

**参数**

- **`file`**：要打开的文件的路径（字符串）。
- **`flags`**：文件打开标志（整数），可以使用多个标志按位或组合。
- **`mode`**（可选）：文件模式（整数），在创建文件时指定文件权限。默认是 `0o777`（八进制）。

**常用标志**

标志用于指定文件的打开方式和权限，常用标志包括：

- `os.O_RDONLY`：只读模式。
- `os.O_WRONLY`：只写模式。
- `os.O_RDWR`：读写模式。
- `os.O_CREAT`：如果文件不存在则创建。
- `os.O_EXCL`：与 `os.O_CREAT` 一起使用，如果文件已存在则抛出异常。
- `os.O_TRUNC`：打开文件时截断文件（清空文件内容）。
- `os.O_APPEND`：以追加模式打开文件。
- `os.O_NONBLOCK`：非阻塞模式。

**示例**

示例 1：打开文件并读取内容

```python
import os

# 使用 os.O_RDONLY 以只读模式打开文件
fd = os.open('example.txt', os.O_RDONLY)

# 读取文件内容（假设文件大小小于100字节）
content = os.read(fd, 100)
print("Read content:")
print(content.decode('utf-8'))

# 关闭文件描述符
os.close(fd)
```

示例 2：打开文件并写入内容

```python
import os

# 使用 os.O_WRONLY | os.O_CREAT 打开文件，如果文件不存在则创建
fd = os.open('example.txt', os.O_WRONLY | os.O_CREAT)

# 写入内容到文件
os.write(fd, b'Hello, World!\n')

# 关闭文件描述符
os.close(fd)
```

示例 3：以读写模式打开文件并进行操作

```python
import os

# 使用 os.O_RDWR 打开文件，以读写模式
fd = os.open('example.txt', os.O_RDWR)

# 读取文件内容
content = os.read(fd, 100)
print("Read content:")
print(content.decode('utf-8'))

# 将文件指针移到文件末尾
os.lseek(fd, 0, os.SEEK_END)

# 写入新内容到文件末尾
os.write(fd, b'Additional line.\n')

# 将文件指针移到文件开头
os.lseek(fd, 0, os.SEEK_SET)

# 读取新的文件内容
new_content = os.read(fd, 100)
print("New content:")
print(new_content.decode('utf-8'))

# 关闭文件描述符
os.close(fd)
```

**注意事项**

1. **文件描述符**：`os.open()` 返回一个整数文件描述符，与文件对象不同，需要使用 `os.read()` 和 `os.write()` 进行读写操作。
2. **关闭文件**：使用 `os.close(fd)` 关闭文件描述符，释放系统资源。
3. **权限管理**：在创建文件时，可以通过 `mode` 参数指定文件权限，例如 `0o644` 表示用户可读写，组和其他用户只读。

通过使用 `os.open()`，可以实现对文件的更底层控制，适用于需要精细控制文件打开方式和权限的场景。

### os.fdopen() 函数

在 Python 中，`fdopen()` 函数用于将一个已有的文件描述符（file descriptor）**包装成一个 Python 文件对象**。这样你就可以使用 **Python 的高级文件操作接口**（如读取、写入和关闭文件）来操作已经通过底层系统调用打开的文件。

```python
fdopen(fd, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True)
```

**参数说明：**

- **`fd`**: 要包装的文件描述符（整数）。这个文件描述符通常是**通过底层文件操作系统调用（如 `os.open()`）返回的**。
- **`mode`**: 打开文件的模式，与 `open()` 函数的模式参数相同：
  - `'r'`: 只读模式。
  - `'w'`: 写入模式。
  - `'x'`: 独占创建模式。
  - `'a'`: 追加模式。
  - `'b'`: 二进制模式。
  - `'t'` 或 `'r'`: 文本模式。
  - `'+'`: 更新模式（读取和写入）。
- **`buffering`**: 缓冲策略，与 `open()` 函数的 `buffering` 参数相同。
- **`encoding`** 和 **`errors`**: 如果文件模式包括 `'t'` 或 `'r'`，则可以指定文件编码和错误处理方式，与 `open()` 函数的相应参数相同。
- **`newline`**: 控制换行符的行为，与 `open()` 函数的 `newline` 参数相同。
- **`closefd`**: 如果为 `True`，则在关闭文件对象时也关闭文件描述符 `fd`。

**返回值：**

`fdopen()` 函数返回一个文件对象，可以像常规的文件对象一样进行读取、写入或其他文件操作。

**示例**

以下示例展示了如何使用 `os.open()` 打开文件，然后使用 `os.fdopen()` 将文件描述符转换为文件对象，并进行文件操作。

**示例 1：打开文件并读取内容**

```python
import os

# 使用 os.open() 打开文件，并获取文件描述符 fd
fd = os.open('example.txt', os.O_RDONLY)

# 使用 os.fdopen() 将文件描述符 fd 包装成文件对象
with os.fdopen(fd, 'r') as file:
    content = file.read()
    print("Read content:")
    print(content)

# 文件对象在 with 语句结束时自动关闭
```

**示例 2：打开文件并写入内容**

```python
import os

# 使用 os.open() 打开文件，并获取文件描述符 fd
fd = os.open('example.txt', os.O_WRONLY | os.O_CREAT | os.O_TRUNC)

# 使用 os.fdopen() 将文件描述符 fd 包装成文件对象
with os.fdopen(fd, 'w') as file:
    file.write('Hello, World!\n')

# 文件对象在 with 语句结束时自动关闭
```

**示例 3：以读写模式打开文件并进行操作**

```python
import os

# 使用 os.open() 打开文件，并获取文件描述符 fd
fd = os.open('example.txt', os.O_RDWR)

# 使用 os.fdopen() 将文件描述符 fd 包装成文件对象
with os.fdopen(fd, 'r+') as file:
    # 读取文件内容
    content = file.read()
    print("Read content:")
    print(content)

    # 将文件指针移到文件末尾
    file.seek(0, os.SEEK_END)

    # 写入新内容到文件末尾
    file.write('Additional line.\n')

    # 将文件指针移到文件开头
    file.seek(0)

    # 读取新的文件内容
    new_content = file.read()
    print("New content:")
    print(new_content)

# 文件对象在 with 语句结束时自动关闭
```

**注意事项**

1. **文件描述符**：`os.open()` 返回一个整数文件描述符，`os.fdopen()` 将其包装为高级文件对象。
2. **关闭文件**：`os.fdopen()` 返回的文件对象在关闭时（例如在 `with` 语句结束时）会自动关闭底层文件描述符，除非 `closefd` 参数设置为 `False`。
3. **高级接口**：使用 `os.fdopen()` 后，可以使用 Python 提供的高级文件操作方法，例如 `read()`、`write()`、`seek()` 等。

通过 `os.fdopen()`，可以将底层的文件描述符转换为高级文件对象，从而更方便地进行文件操作。

### open()、os.open()、os.fdopen() 区别

- **灵活性**：

  - `open()` 函数提供了更高级别的接口，适合大多数文件操作需求，并且更易于使用和理解。
  - `os.open()` 函数提供了更底层的接口，适合需要更细粒度控制或者特定系统调用的场景。

- **返回值**：

  - `open()` 返回文件对象，支持高级别的文件操作方法。
  - `os.open()` 返回文件描述符，需要额外使用 `os` 模块提供的函数来进行文件操作。
  - `os.fdopen()` 返回文件对象，支持高级别的文件操作方法。

- **用法建议**：

  - **`open()`**：高级文件操作接口，适合大多数文件操作需求，返回文件对象，支持简单的文件读写和上下文管理。
  - **`os.open()`**：底层文件操作接口，提供更细粒度的控制，返回文件描述符，适合需要特殊文件打开模式或底层控制的场景。
  - **`os.fdopen()`**：将文件描述符转换为文件对象，结合了 `os.open()` 的底层控制和 `open()` 的高级接口，适合需要从底层控制切换到高级文件操作的场景。

> :star:**推荐：**1、直接使用 open()；2、用 os.open() 创建/打开文件描述符，再用 os.fdopen() 转换成文件对象，这样就可以用 with...as 管理文件资源，避免直接使用 os.open() 时忘记调用 os.os.close(fd)。

## 高级文件操作接口

在 Python 中，高级文件操作接口主要指使用**内置的 `open()` 函数以及与其相关的方法**来进行文件的读写操作。这些接口提供了更高层次和易用的文件操作方式，适用于大多数日常文件处理需求。

### 基本文件操作函数

1. **`open()`**

   - 打开文件并返回文件对象。

   ```python
   file = open('example.txt', 'r')
   ```

2. **`close()`**

   - 关闭文件对象。

   ```python
   file.close()
   ```

### 文件对象的方法

这些方法是文件对象所提供的，用于读写和管理文件。

**读操作**

1. **`read(size=-1)`**

   - 读取文件内容，可以指定读取的字节数。

   ```python
   content = file.read()
   ```

2. **`readline(size=-1)`**

   - 读取一行内容，可以指定最大读取的字节数。

   ```python
   line = file.readline()
   ```

3. **`readlines(hint=-1)`**

   - 读取所有行并返回列表，可以指定最大读取的字节数。

   ```python
   lines = file.readlines()
   ```

**写操作**

1. **`write(string)`**

   - 写入字符串到文件。

   ```python
   file.write('Hello, World!\n')
   ```

2. **`writelines(lines)`**

   - 写入字符串列表到文件。

   ```python
   file.writelines(['Line 1\n', 'Line 2\n'])
   ```

**文件指针操作**

1. **`seek(offset, whence=0)`**

   - 移动文件指针。

   ```python
   file.seek(0)
   ```

2. **`tell()`**

   - 获取文件指针当前位置。

   ```python
   position = file.tell()
   ```

**缓冲区操作**

1. `flush()`

   - 刷新文件的写缓冲区。

   ```python
   python
   复制代码
   file.flush()
   ```

**上下文管理**

1. `__enter__()` 和 `__exit__()`

   - 使文件对象支持上下文管理协议，使用 `with` 语句自动管理文件的打开和关闭。

   ```python
   with open('example.txt', 'r') as file:
       content = file.read()
   ```

**示例**

读取二进制文件

```python
with open('example.bin', 'rb') as file:
    binary_data = file.read()
    print(binary_data)
```

写入二进制文件

```python
with open('example.bin', 'wb') as file:
    file.write(b'\x00\xFF\x00\xFF')
```

逐行读取大文件

```python
def process_large_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            process_line(line)

def process_line(line):
    print(line, end='')

process_large_file('large_file.txt')
```

通过这些高级文件操作函数和方法，可以方便地实现各种复杂的文件处理任务，适用于不同的应用场景。

### 高级文件处理函数

**`shutil` 模块**

`shutil` 模块的全称是 "shell utilities"。这个模块提供了许多高级的文件操作和目录管理功能，使得处理文件和目录的操作变得更加方便和高效。`shutil` 模块包含了**复制、移动、删除文件和目录，以及管理文件权限和符号链接等**操作。

**文件操作**

1. **`shutil.copy(src, dst)`**

   - 复制文件内容和权限，从源路径 `src` 到目标路径 `dst`。

   ```python
   import shutil
   shutil.copy('source.txt', 'destination.txt')
   ```

2. **`shutil.copy2(src, dst)`**

   - 复制文件内容、权限以及元数据（如时间戳）。

   ```python
   shutil.copy2('source.txt', 'destination.txt')
   ```

3. **`shutil.copyfile(src, dst)`**

   - 仅复制文件内容，不复制文件权限和元数据。

   ```python
   shutil.copyfile('source.txt', 'destination.txt')
   ```

4. **`shutil.move(src, dst)`**

   - 移动文件或目录到目标位置 `dst`。

   ```python
   shutil.move('source.txt', 'destination_folder/')
   ```

5. **`shutil.rmtree(path)`**

   - 递归删除目录树。

   ```python
   shutil.rmtree('directory_to_delete')
   ```

**目录操作**

1. **`shutil.copytree(src, dst)`**

   - 递归复制目录树，从源目录 `src` 到目标目录 `dst`。

   ```python
   shutil.copytree('source_folder', 'destination_folder')
   ```

2. **`shutil.rmtree(path)`**

   - 递归删除目录树。

   ```python
   shutil.rmtree('directory_to_delete')
   ```

3. **`shutil.make_archive(base_name, format, root_dir=None)`**

   - 创建压缩包并返回其路径。`base_name` 是压缩包的名字，`format` 是压缩包的格式（如 `'zip'`、`'tar'`），`root_dir` 是要压缩的目录。

   ```python
   shutil.make_archive('archive_name', 'zip', 'directory_to_compress')
   ```

4. **`shutil.unpack_archive(filename, extract_dir=None, format=None)`**

   - 解压缩文件到目标目录。`filename` 是压缩包的名字，`extract_dir` 是解压缩到的目录，`format` 是压缩包的格式。

   ```python
   shutil.unpack_archive('archive_name.zip', 'extracted_directory')
   ```

**文件权限操作**

1. `shutil.chown(path, user=None, group=None)`

   - 修改文件或目录的所有者。

   ```python
   shutil.chown('example.txt', user='username', group='groupname')
   ```

示例

复制文件并保留元数据

```python
import shutil

shutil.copy2('source.txt', 'destination.txt')
```

递归复制目录

```python
shutil.copytree('source_folder', 'destination_folder')
```

移动文件到另一个目录

```python
shutil.move('source.txt', 'destination_folder/source.txt')
```

递归删除目录

```python
shutil.rmtree('directory_to_delete')
```

创建和解压缩文件

```python
# 创建 zip 压缩包
shutil.make_archive('archive_name', 'zip', 'directory_to_compress')

# 解压缩文件
shutil.unpack_archive('archive_name.zip', 'extracted_directory')
```

修改文件权限

```python
shutil.chown('example.txt', user='username', group='groupname')
```

`shutil` 模块提供了一个简单而强大的接口，用于执行许多常见的文件和目录操作，这使得在 Python 中进行文件管理变得非常方便。

