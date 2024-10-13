# python 安装配置

## 查看 python 版本

查看 python 版本：python --version

windows 查看安装 python 版本：py -0

查看 python 安装路径：where python

# pip 命令

pip 是 Python 包管理工具，该工具提供了对 Python 包的查找、下载、安装、卸载的功能。

```shell
pip --version	# 显示版本和路径，也可判断是否已经安装pip
pip --help		# 获取帮助
pip list		# 列出已安装的包
pip list -o		# 查看可升级的包
pip install -U pip	# 升级 pip
# 安装包
pip install SomePackage              # 最新版本
pip install SomePackage==1.0.4       # 指定版本
pip install 'SomePackage>=1.0.4'     # 最小版本

# 显示安装包信息
pip show xxx

# 升级包
pip install --upgrade xxx

# 删除包
pip uninstall xxx

# 搜索包
pip search xxx

# 软件源安装某个包（临时使用）
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple xxx		# 清华源
```

# python 虚拟环境

Python 版本更新比较快速，主要原因有：活跃的开发社区、适应技术变化、改进性能、修复安全漏洞等。尽管版本更新频繁，但主要版本（如 Python 2 到 Python 3）之间通常会有较长的过渡期。因此不同的机器上安装的 python 版本和依赖库版本不同。

考虑这种情况：你正在开发应用程序 A，使用你的系统安装的 Python 和你 pip install 安装的 packageX 的 1.0 版本到全局 Python 库。然后你切换到本地机器上的项目 B，并安装了相同的 packageX，但版本为 2.0，在 1.0 和 2.0 之间有一些突破性的变化。当你回去运行你的项目 A 时，你遇到了各种各样的错误，而且你的项目不能运行。这是你在用 Python 构建软件时可能遇到的情况。而为了解决这个问题，我们可以使用虚拟环境。

使用虚拟环境时可能会遇到`virtualenv`、`venv`、`pipenv`等名词，下面是他们的区别：

## virtualenv 虚拟环境

`virtualenv` 是目前最流行的 Python 虚拟环境配置工具。它不仅同时支持 Python2 和 Python3，而且可以为每个虚拟环境指定 Python 解释器，并选择不继承基础版本的包。

```shell
# 安装 virtualenv
pip install virtualenv

# 创建虚拟环境
virtualenv [虚拟环境名称]
# –no-site-packeages参数，意义在于不复制已经安装到系统Python环境中的所有第三方包从而得到一个“纯净”的运行环境。
virtualenv --no-site-packages [虚拟环境名称]

# 激活环境
cd venv
source ./bin/activate	# Linux
.\Scripts\activate.bat	# Windows

# 退出环境
deactivate					# Linux
.\Scripts\deactivate.bat	# Windows

# 删除环境
# 直接删除venv文件夹来删除环境

# 使用环境
# 进入环境后，一切操作和正常使用python一样 安装包使用pip install 包。
```

## venv

Python 从 3.3 版本开始，自带了一个虚拟环境 venv，在 PEP-405 中可以看到它的详细介绍。它实际是 virtualenv 的一个子集被整合到标准库的 venv 模块下，因此很多操作都和 virtualenv 类似，但是两者运行机制不同。因为是从 3.3 版本开始自带的，这个工具也仅仅支持 python 3.3 和以后版本。所以，要在 python2 上使用虚拟环境，依然要利用 virtualenv。

## pipenv

**pipenv 是 Python 官方推荐的包管理工具。** pipenv 是 Pipfile 主要倡导者、requests 作者 Kenneth Reitz 写的一个命令行工具，主要包含了 Pipfile、pip、click、requests 和 virtualenv，能够有效管理 Python 多个环境，各种第三方包及模块。

```shell
# 安装 pipenv
pip install pipenv

# 创建虚拟环境
# pipenv以是基于项目的，首先新建项目文件夹
cd myproject
pipenv install  # 使用本地默认版本的python
pipenv --two  # 使用当前系统中的Python2 创建环境
pipenv --three  # 使用当前系统中的Python3 创建环境
pipenv --python 3.6  # 指定使用Python3.6创建环境


# 激活环境
pipenv shell

# 退出环境
exit

# 删除环境
pipenv --rm

# 使用环境
# 不要使用pip安装库，而要使用pipenv install命令
pipenv install xxx
pipenv install requests  # 或者直接安装库
```

## conda

conda 可以直接创建不同 python 版本的虚拟环境。前面讲的 virtualenv 只是指定创建不同 python 版本的虚拟环境，前提是你的电脑上已经安装了不同版本的 python，与 conda 相比没有 conda 灵活。
