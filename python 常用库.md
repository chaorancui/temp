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

以下是使用 `logging` 模块的基本方法和常见用法：

### 基本用法

1. **导入模块**

   ```python
   import logging
   ```

2. **设置日志级别**

   `logging` 模块提供了多个日志级别，如 `DEBUG`、`INFO`、`WARNING`、`ERROR` 和 `CRITICAL`。通过设置不同的日志级别，可以控制记录的详细程度。

   ```python
   logging.basicConfig(**kwargs)
   ```

   **常用参数**

   - `filename`：指定日志输出到的文件名。如果不指定，日志将输出到控制台。
   - `filemode`：指定文件打开模式，默认是 `'a'`（追加模式）。常用模式还有 `'w'`（写模式，覆盖原有文件）。
   - `format`：指定日志记录的格式字符串。
   - `datefmt`：指定日期和时间的格式。
   - `level`：设置日志记录的最低严重级别。常见级别有 `logging.DEBUG`, `logging.INFO`, `logging.WARNING`, `logging.ERROR`, `logging.CRITICAL`。设置为 `DEBUG`，意味着所有级别的日志信息都会被记录。
   - `handlers`：指定一个处理器列表，用于自定义处理器（Python 3.3 及以上版本支持）。

3. **记录日志**

   使用不同级别的日志记录函数来记录不同级别的日志信息：

   ```python
   logging.debug('This is a debug message')
   logging.info('This is an info message')
   logging.warning('This is a warning message')
   logging.error('This is an error message')
   logging.critical('This is a critical message')
   ```

4. **输出格式**

   默认情况下，日志信息会按照一定的格式输出到控制台。可以通过设置 `format` 参数来自定义日志输出的格式。

   ```python
   logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
   ```

   上述格式中：

   - `%(asctime)s` 表示日志记录的时间
   - `%(levelname)s` 表示日志级别名称
   - `%(message)s` 表示日志消息

**示例**：

```python
import logging

# 设置日志级别和输出格式
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 记录不同级别的日志信息
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
```

运行上述示例，会输出类似以下内容的日志信息：

```log
2024-07-10 12:00:00,000 - DEBUG - This is a debug message
2024-07-10 12:00:00,001 - INFO - This is an info message
2024-07-10 12:00:00,002 - WARNING - This is a warning message
2024-07-10 12:00:00,003 - ERROR - This is an error message
2024-07-10 12:00:00,004 - CRITICAL - This is a critical message
```

### 高级用法

- **将日志记录到文件**

  可以通过设置 `filename` 参数将日志记录到文件中：

  ```python
  logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
  ```

- **添加处理程序**

  可以添加多个处理程序，比如同时输出到控制台和文件：

  ```python
  console_handler = logging.StreamHandler()
  file_handler = logging.FileHandler('app.log')
  handlers = [console_handler, file_handler]

  logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=handlers)
  ```

- **使用 Logger 对象**

  创建和配置 `Logger` 对象来进行更灵活的日志记录控制：

  ```python
  logger = logging.getLogger('my_app')
  logger.setLevel(logging.DEBUG)
  
  # 创建一个文件处理程序和一个控制台处理程序
  file_handler = logging.FileHandler('app.log')
  console_handler = logging.StreamHandler()
  
  # 设置日志格式
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  file_handler.setFormatter(formatter)
  console_handler.setFormatter(formatter)
  
  # 添加处理程序到 logger
  logger.addHandler(file_handler)
  logger.addHandler(console_handler)
  
  # 记录日志
  logger.debug('Debug message')
  logger.info('Info message')
  ```

通过这些方法，可以根据具体需求配置和管理日志记录，帮助开发人员更好地理解和调试程序运行过程中的各种情况和问题。

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
