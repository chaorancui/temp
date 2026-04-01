[toc]

# Conda 使用速查手册（Linux 版）

> 适用于：已安装 `Anaconda` / `Miniconda` / `Mambaforge`

## Conda 是什么

Conda 是一个：

- 包管理工具（类似 apt / pip）
- 虚拟环境管理工具（类似 venv / virtualenv）

Conda 的两个核心功能：

1. 创建独立 Python 环境
2. 在不同环境中安装不同依赖

例如：

```log
项目A → python3.8 + torch1.13
项目B → python3.10 + torch2.2
```

**conda 和 virtualenv 区别**：

| 特性       | conda | virtualenv |
| ---------- | ----- | ---------- |
| python管理 | 支持  | 不支持     |
| 非python包 | 支持  | 不支持     |
| 依赖解析   | 强    | 弱         |
| 速度       | 慢    | 快         |

## 环境管理

1. 查看已有环境

   ```bash
   conda env list
   # 或
   conda info --envs
   ```

   输出示例：

   ```log
   # conda environments:
   #
   base                  *  /home/user/anaconda3
   py38                     /home/user/anaconda3/envs/py38
   llm                      /home/user/anaconda3/envs/llm
   ```

   说明：
   - `*` 表示当前激活环境
   - `base` 是默认环境

2. 创建新环境

   创建指定 Python 版本环境

   ```bash
   conda create -n <env_name> python=3.10
   ```

   如：

   ```bash
   conda create -n video2blog python=3.10
   # 创建完成后：
   conda activate video2blog
   # 终端会变成：
   (video2blog) user@server
   # 说明已进入新环境
   ```

3. 退出当前环境

   ```bash
   conda deactivate
   ```

4. 删除环境

   ```bash
   conda remove -n myenv --all
   ```

   例如：

   ```bash
   conda remove -n video2blog --all
   ```

5. 重命名环境（没有直接命令）

   需要复制后删除：

   ```bash
   conda create -n newenv --clone oldenv
   conda remove -n oldenv --all
   ```

## 包管理

**conda 和 pip 可以混用**。**建议顺序**：

- 优先使用 `conda install`
- 找不到再用 `pip install`。

1. 查看已安装包

   ```bash
   conda list
   conda list -n myenv      # 指定环境
   ```

2. 安装包

   ```bash
   # 当前环境安装：
   conda install numpy
   conda install numpy pandas matplotlib    # 安装多个包

   # 指定环境安装：
   conda install -n myenv numpy
   ```

3. 安装指定版本

   ```bash
   conda install python=3.10
   conda install pytorch=2.2
   ```

4. 删除包

   ```bash
   conda remove numpy
   ```

5. 更新包

   ```bash
   conda update numpy

   # 更新所有包：
   conda update --all
   ```

## 环境导出与复现（重要）

1. 导出环境

   ```bash
   conda env export > environment.yml
   ```

2. 从文件创建环境

   ```bash
   conda env create -f environment.yml
   ```

3. 指定环境名创建

   ```bash
   conda env create -f environment.yml -n newenv
   ```

## 清理缓存（释放空间）

```bash
conda clean -a
# 或
conda clean --all
```

## 镜像源配置（强烈推荐）

默认源很慢，建议换清华源：

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free

conda config --set show_channel_urls yes
```

查看配置：

```bash
conda config --show
```

## 常用高级命令

1. 查看 conda 安装路径: `which conda` 或 `conda info | grep -i base`

2. 查看 conda 信息: `conda info`

3. 查看 conda 版本: `conda --version`

4. 更新 conda: `conda update conda`

5. 搜索包: `conda search pytorch`

6. 关闭自动进入 base 环境: `conda config --set auto_activate_base false`

7. 恢复自动进入 base: `conda config --set auto_activate_base true`

8. 查看环境路径: `which python` 或 `which pip`

9. 如果环境出问题：

   ```bash
   conda clean -a
   conda update conda
   ```

10. 进阶：mamba（更快）

    ```bash
    # 安装 mamba：
    conda install mamba -n base -c conda-forge
    # 使用：
    mamba install pytorch
    ```

## 推荐环境管理流程

推荐流程：

1. 创建项目环境

   ```bash
   conda create -n video2blog python=3.10
   ```

2. 进入环境

   ```bash
   conda activate video2blog
   ```

3. 安装依赖

   ```bash
   pip install -r requirements.txt
   ```

4. 开发

5. 导出环境

   ```bash
   conda env export > environment.yml
   ```

## 最常用命令速查表

1. 环境管理

   ```bash
   conda env list
   conda create -n env python=3.10
   conda activate env
   conda deactivate
   conda remove -n env --all
   ```

2. 包管理

   ```bash
   conda list
   conda install numpy
   conda remove numpy
   conda update numpy
   ```

3. 环境导出

   ```bash
   conda env export > environment.yml
   conda env create -f environment.yml
   ```

## 推荐的视频转博客项目环境

你可以这样创建：

```bash
conda create -n video2blog python=3.10
conda activate video2blog
```

安装常见依赖：

```bash
pip install

openai
whisper
ffmpeg-python
yt-dlp
transformers
torch
accelerate
sentencepiece
```
