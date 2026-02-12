# shell 编程

## 参数默认值处理

默认值操作符：`:-`、`:=`、`:+`、`:?`

```bash
# :- 如果变量未设置或为空，则使用默认值
echo ${var:-default}   # var未设置，输出: default
var=""; echo ${var:-default}  # var为空，输出: default
var="value"; echo ${var:-default}  # var有值，输出: value

# := 如果变量未设置或为空，则设置默认值并返回
echo ${var:=default}   # 设置var为default并输出

# :? 如果变量未设置或为空，则显示错误信息并退出（生产脚本常用）
MODEL_PATH=${MODEL_PATH:?MODEL_PATH must be set}

# :+ 如果变量设置且非空，则使用替代值
var="value"
echo ${var:+replaced}  # 输出: replaced
```

## 字符串大小写操作

只在 **Bash 4.0+** 支持，**不是 POSIX sh**，在 `dash / ash / busybox sh` 中不可用。

```bash
# 全部转小写：`,,`
var=${var,,}
mode=DEBUG
echo "${mode^^}"   # debug

# 全部转大写：`^^`
var=${var^^}
mode=debug
echo "${mode^^}"   # DEBUG

# 仅首字母转小写：`,`（单个）
var=${var,}
Var=TRUE
echo "${Var,}"     # tRUE

# 仅首字母转大写：`^`
var=${var^}
mode=debug
echo "${mode^}"    # Debug

# 对特定字符集转换（进阶）
var=${var,,[A-Z]}
var=${var^^[a-z]}
str="AbC123"
echo "${str,,[A-Z]}"   # abc123
```

> **脚本内部字符串处理，优先用 Bash 参数展开**

示例：

```bash
GDB=${GDB:-false}
GDB=${GDB,,}

case "$GDB" in
  true|1|yes|on) ENABLE_GDB=true ;;
  *)             ENABLE_GDB=false ;;
esac
```

这已经是 Shell 脚本处理布尔开关的“工业级模板”。

## 参数展开删除替换

**Shell 参数展开操作符的介绍**：

1. 基本的参数展开：`${}`

   ```bash
   var="hello"
   echo ${var}        # 等同于 $var
   echo ${var}world   # 拼接字符串，输出: helloworld
   ```

2. 长度获取：`#`

   ```bash
   str="hello"
   echo ${#str}      # 输出字符串长度: 5

   array=(1 2 3 4 5)
   echo ${#array[@]} # 输出数组长度: 5
   ```

3. 从开头删除匹配模式：`#` 和 `##`

   ```bash
   ${var#pattern}   # 从结尾删除 最短 匹配
   ${var##pattern}  # 从结尾删除 最长 匹配

   path="/usr/local/bin/python"
   # #  从开头删除最短匹配
   echo ${path#*/}      # 输出: usr/local/bin/python
   # ## 从开头删除最长匹配
   echo ${path##*/}     # 输出: python

   # 实际应用：提取文件名
   filename="script.test.sh"
   echo ${filename#*.}  # 输出: test.sh
   echo ${filename##*.} # 输出: sh
   ```

   使用 **Bash 参数展开（parameter expansion）删除替换**，注意：
   - `pattern` 使用的是 **shell 通配符（glob）**
     - `*` 任意字符串
     - `?` 单个字符
     - `[abc]` 字符集合
   - **不是正则**
   - **不是普通文本**

4. 从结尾删除匹配模式：`%` 和 `%%`

   ```bash
   ${var%pattern}   # 从结尾删除 最短 匹配
   ${var%%pattern}  # 从结尾删除 最长 匹配

   path="/usr/local/bin/python"
   # %  从结尾删除最短匹配
   echo ${path%/*}      # 输出: /usr/local/bin
   # %% 从结尾删除最长匹配
   echo ${path%%/*}     # 输出: (空)

   # 实际应用：删除文件扩展名
   filename="script.test.sh"
   echo ${filename%.*}  # 输出: script.test
   echo ${filename%%.*} # 输出: script
   ```

5. 替换模式：`/` 和 `//`

   ```bash
   text="hello hello world"
   # / 替换第一次匹配
   echo ${text/hello/hi}   # 输出: hi hello world
   # // 替换所有匹配
   echo ${text//hello/hi}  # 输出: hi hi world

   # 实际应用：替换路径分隔符
   path="C:\Windows\System32"
   echo ${path//\\/\/}    # 输出: C:/Windows/System32
   ```

6. 子字符串提取：`:offset` 和 `:offset:length`

   ```bash
   str="Hello World"
   echo ${str:6}      # 输出: World
   echo ${str:0:5}    # 输出: Hello
   echo ${str: -5}    # 输出: World (注意空格)
   echo ${str: -5:2}  # 输出: Wo
   ```

**典型使用场景**：

1. 文件路径处理

   ```bash
   # 提取文件目录
   full_path="/home/user/docs/file.txt"
   dir=${full_path%/*}         # 输出: /home/user/docs

   # 提取文件名
   filename=${full_path##*/}   # 输出: file.txt

   # 提取不带扩展名的文件名
   name=${filename%.*}         # 输出: file

   # 提取扩展名
   ext=${filename##*.}         # 输出: txt
   ```

2. URL 处理

   ```bash
   url="https://example.com/path/to/page.html"
   # 提取域名
   domain=${url#*//}
   domain=${domain%%/*}       # 输出: example.com

   # 提取路径
   path=${url##*/}           # 输出: page.html
   ```

3. 批量重命名

   ```bash
   # 将所有.txt文件重命名为.md文件
   for file in *.txt; do
       mv "$file" "${file%.txt}.md"
   done
   ```

4. 环境变量处理

   ```bash
   # 添加路径到PATH，避免重复
   export PATH="${PATH:+$PATH:}/new/path"

   # 设置默认值
   TIMEOUT=${TIMEOUT:-30}
   ```

5. 字符串处理

   ```bash
   # 移除字符串中的所有空格
   str="hello world"
   echo ${str// /}      # 输出: helloworld

   # 将字符串中的下划线替换为空格
   var="hello_world_test"
   echo ${var//_/ }     # 输出: hello world test
   ```

## 引用变量：`$VAR` 和 `${VAR}`

在Shell脚本中，`$var` 和 `${var}` 的**核心功能是一样的**，都是获取变量的值。但 `${var}` 提供了更多的灵活性和安全性：

**一、主要区别**

1. **边界明确性**（最常见的使用场景）

   ```bash
   var="hello"

   # 错误：Shell会认为变量名是 var_world
   echo "$var_world"     # 输出：（空）

   # 正确：明确变量边界
   echo "${var}_world"   # 输出：hello_world
   ```

2. **数组访问**

   ```bash
   arr=(a b c d)

   echo "$arr"      # 输出：a （只输出第一个元素）
   echo "${arr[2]}" # 输出：c （访问指定索引）
   echo "${arr[@]}" # 输出：a b c d （所有元素）
   ```

3. **字符串操作**（只能用 `${}`）

   ```bash
   file="document.txt"

   # 字符串截取
   echo "${file:0:3}"        # 输出：doc

   # 删除后缀
   echo "${file%.txt}"       # 输出：document

   # 删除前缀
   path="/usr/local/bin"
   echo "${path##*/}"        # 输出：bin

   # 替换
   echo "${file/txt/pdf}"    # 输出：document.pdf

   # 默认值
   echo "${undefined:-default}"  # 输出：default
   ```

4. **可读性和维护性**

   ```bash
   # 不够清晰
   name="John"
   echo "Hello $name123"    # 会查找变量 name123

   # 清晰明确
   echo "Hello ${name}123"  # 输出：Hello John123
   ```

**二、什么时候必须用 `${}`**

1. **变量名后紧跟字母、数字或下划线**

   ```bash
      echo "${var}text"
   ```

2. **使用数组**

   ```bash
      echo "${array[0]}"
   ```

3. **进行参数扩展/字符串操作**

   ```bash
      echo "${var:-default}"
      echo "${var#prefix}"
   ```

最佳实践

虽然简单情况下 `$var` 可以工作，但**推荐始终使用 `${var}`**，因为：

- 更清晰、更安全
- 避免歧义
- 便于后续添加字符串操作
- 代码风格更统一

## 数组

[Bash 脚本进阶指南 - 27.数组](https://linuxstory.gitbook.io/advanced-bash-scripting-guide-in-chinese/zheng-wen/part5/27_arrays)

**一、定义使用数组**

新版本的 Bash 支持一维数组。 数组元素可以使用符号**variable[xx]** 来初始化。另外，脚本可以使用**declare -a variable**语句来指定一个数组。 如果想引用一个数组元素（也就是取值），可以使用大括号，访问形式为 ${element[xx]} 。

```bash
# -----------------------------------------------------------------
# 一种给数组变量赋值的方法...
#  数组成员不一定非得是相邻或连续的。
#  数组的部分成员可以不被初始化。
#  数组中允许空缺元素。
area[11]=23
area[13]=37
area[51]=UFOs

echo -n "area[11] = "
echo ${area[11]}    #  需要{大括号}。

echo -n "area[43] = "
echo ${area[43]}    # 没被初始化的数组成员打印为空值（null变量）。
echo "(area[43] unassigned)"


# -----------------------------------------------------------------
# 另一种给数组变量赋值的方法...
# array=( element1 element2 ... elementN )
# 从0开始计算数组下标（也就是，数组的第一个元素为[0],而不是[1]).
area2=( zero one two )
# 或
area2=(
  zero
  one
  two
)

echo -n "area2[0] = "
echo ${area2[0]}


# -----------------------------------------------------------------
# 另外一种给数组元素赋值的方法...
# array_name=([xx]=XXX [yy]=YYY ...)
area3=([17]=seventeen [24]=twenty-four)

echo -n "area3[17] = "
echo ${area3[17]}

exit 0
```

**二、数组操作**

```bash
#!/bin/bash

IFS=";"

array=(zero one two three four five)
# 数组元素 0   1   2    3     4    5

echo "--------------获取数组第0个元素"
echo ${array[0]} #  位置0(#0)元素
echo ${array:0}  #  位置0(#0)元素

echo "--------------获取数组的长度"
echo ${#array[*]} # 6 数组中的元素个数。
echo ${#array[@]} # 6 数组中的元素个数.

echo "--------------获取数组第0个元素的长度"
echo ${#array[0]} # 4 第一个数组元素的长度。
echo ${#array}    # 4 第一个数组元素的长度。(另一种表示形式)

echo "--------------数组切片"
# "${COMMON_ARGS[@]}" 和 "${COMMON_ARGS[*]}" 必须加引号
echo "${array[@]}" # 数组所有元素, one two three four five five
echo "${array[*]}" # 数组所有元素，受 IFS 影响, zero;one;two;three;four;five

echo "${array[@]:0}" # one two three four five five
#                ^     所有元素

echo "${array[@]:1}" # two three four five five
#                ^     element[0]后边的所有元素.

echo "${array[@]:1:2}" # two three
#                  ^     只提取element[0]后边的两个元素.

exit
```

> 注：大部分标准[字符串操作](https://linuxstory.gitbook.io/advanced-bash-scripting-guide-in-chinese/zheng-wen/part3/10_manipulating_variables/10_1_manipulating_strings) 都可以用于数组中。

**三、`"${COMMON_ARGS[@]}"` 和 `${COMMON_ARGS[*]}` 的区别（非常关键）**

**`${array_name[@]}`** 和 **`${array_name[*]}`** 的关系非常类似于 [`$@ 和 $*`](http://tldp.org/LDP/abs/html/internalvariables.html#APPREF)。这种数组用法非常广泛。

| 写法                  | 展开结果                 |
| --------------------- | ------------------------ |
| `"${COMMON_ARGS[@]}"` | **多个独立参数（正确）** |
| `"${COMMON_ARGS[*]}"` | 一个参数（全部拼在一起） |

示例：

```bash
COMMON_ARGS=(a b c)

echo "${COMMON_ARGS[@]}"   # a b c
echo "${COMMON_ARGS[*]}"   # a b c（一个整体）
```

在命令行参数中：

- **99% 场景必须用 `[@]`**
- `[*]` 基本只用于日志打印

## `$*` 和 `$@`

- `$*`

  所有位置参数（字符串语义），所有参数视为一个单词。

  > :point_right: "`$*`" <font color=red>must be</font> quoted.

- `$@`

  所有位置参数（数组语义），参数列表中的每个参数都被视为一个独立的单词。

  > :point_right: Of course, "`$@`" <font color=red>should be</font> quoted.

**Example 9-6. \*arglist\*: Listing arguments with $\* and $@**

```bash
#!/bin/bash
# arglist.sh
# Invoke this script with several arguments, such as "one two three" ...

E_BADARGS=85

if [ ! -n "$1" ]
then
  echo "Usage: `basename $0` argument1 argument2 etc."
  exit $E_BADARGS
fi

echo

index=1          # Initialize count.

echo "Listing args with \"\$*\":"
for arg in "$*"  # Doesn't work properly if "$*" isn't quoted.
do
  echo "Arg #$index = $arg"
  let "index+=1"
done             # $* sees all arguments as single word.
echo "Entire arg list seen as single word."
# "$*" 输出：
# Arg #1 = one two three

echo

index=1          # Reset count.
                 # What happens if you forget to do this?

echo "Listing args with \"\$@\":"
for arg in "$@"
do
  echo "Arg #$index = $arg"
  let "index+=1"
done             # $@ sees arguments as separate words.
echo "Arg list seen as separate words."
# "$@" 输出：
# Arg #1 = one
# Arg #2 = two
# Arg #3 = three

echo

index=1          # Reset count.

echo "Listing args with \$* (unquoted):"
for arg in $*
do
  echo "Arg #$index = $arg"
  let "index+=1"
done             # Unquoted $* sees arguments as separate words.
echo "Arg list seen as separate words."
# $* 输出：
# Arg #1 = one
# Arg #2 = two
# Arg #3 = three

exit 0
```

在执行 **shift** 操作后，`$@` 会保留剩余的命令行参数，而之前的 `$1` 参数则丢失了。

```bash
#!/bin/bash
# Invoke with ./scriptname 1 2 3 4 5

echo "$@"    # 1 2 3 4 5
shift
echo "$@"    # 2 3 4 5
shift
echo "$@"    # 3 4 5

# Each "shift" loses parameter $1.
# "$@" then contains the remaining parameters.
```

`$@` 这个特殊参数常被用作过滤输入到 shell 脚本中的工具。使用 `**cat "$@"**` 这种结构，可以接受从 `stdin` 或从作为参数传递给脚本的文件中获取的输入。参见 [Example 16-24](https://tldp.org/LDP/abs/html/textproc.html#ROT13) 和 [Example 16-25](https://tldp.org/LDP/abs/html/textproc.html#CRYPTOQUOTE)。

> :warning:
>
> - `$*` 和 `$@` 参数有时会根据 [$IFS](https://tldp.org/LDP/abs/html/internalvariables.html#IFSREF) 的设置表现出不一致且令人困惑的行为。
> - `$@` 和 `$*` 参数的区别仅在于双引号内使用时的表现不同。

[Example 9-7](https://tldp.org/LDP/abs/html/internalvariables.html#APPREF). Inconsistent `$\*` and `$@` behavior

```bash
# ./test.sh "First one" "second" "third:one" "" "Fifth: :one"

## == IFS unchanged
IFS unchanged, using "$*"
1: [First one second third:one  Fifth: :one]
---
IFS unchanged, using "$@"
1: [First one]
2: [second]
3: [third:one]
4: []
5: [Fifth: :one]
---
IFS unchanged, using $*
1: [First]
2: [one]
3: [second]
4: [third:one]
5: [Fifth:]
6: [:one]
---
IFS unchanged, using $@
1: [First]
2: [one]
3: [second]
4: [third:one]
5: [Fifth:]
6: [:one]
---

## == IFS=":"
IFS=":", using "$*"
1: [First one:second:third:one::Fifth: :one]
---
IFS=":", using "$@"
1: [First one]
2: [second]
3: [third:one]
4: []
5: [Fifth: :one]
```

## shift 命令
