[toc]

# Linux 系统

# 字体

## 查看已安装字体

1. 最标准的方法：`fc-list`

   大多数 Ubuntu Server 系统都预装了 `fontconfig` 工具包。你可以直接运行：

   ```bash
   fc-list
   ```

   **常用进阶用法：**
   - **只看字体名称（去重）：** `fc-list : family`
   - **查看特定的字体（如等宽字体）：** `fc-list :spacing=100` （100 通常代表 Monospace 等宽）
   - **搜索特定字体（如是否存在 "Ubuntu" 字样）：** `fc-list | grep -i "ubuntu"`

2. 如果 `fc-list` 命令不存在

   如果在执行时提示 `command not found`，说明系统没有安装 `fontconfig`。如果没有 `root` 权限，你无法通过 `apt install` 安装它，但你可以直接查看系统存放字体的**物理目录**：
   - **系统级字体目录：** `ls -R /usr/share/fonts/`
   - **用户级字体目录（你自己的）：** `ls -R ~/.local/share/fonts/` 或 `ls -R ~/.fonts/`

## 安装字体

两种方法（用户目录 vs 系统目录）的对比：

- **用户目录**：无需 root 权限，仅当前用户可用
- **系统目录**：需要 root 权限，所有用户共享

**一、安装到系统目录（需要 root 权限，所有用户共享）**

1. **安装到系统字体目录**

   ```bash
   # 将字体复制到系统字体目录
   sudo cp /path/to/your/font.ttf /usr/share/fonts/truetype/
   ```

   或者为了更好的组织，可以创建子目录：

   ```bash
   # 创建自定义字体目录
   sudo mkdir -p /usr/share/fonts/truetype/custom

   # 复制字体文件
   sudo cp /path/to/your/fonts/* /usr/share/fonts/truetype/custom/

   # 设置正确的权限
   sudo chmod 644 /usr/share/fonts/truetype/custom/*
   ```

2. **更新字体缓存**

   ```bash
   # 更新系统字体缓存
   sudo fc-cache -fv
   ```

3. **验证安装**

   ```bash
   # 列出所有字体，查找你安装的字体
   fc-list | grep "字体名称"

   # 或者查看字体详细信息
   fc-list : file family style
   ```

**补充：**

1. 常用系统字体目录：
   - `/usr/share/fonts/truetype/` - TrueType 字体
   - `/usr/share/fonts/opentype/` - OpenType 字体
   - `/usr/local/share/fonts/` - 本地安装的字体

2. 对于一些常见字体，更推荐使用包管理器：

   ```bash
   # 安装常用中文字体
   sudo apt install fonts-noto-cjk fonts-noto-cjk-extra

   # 安装文泉驿字体
   sudo apt install fonts-wqy-microhei fonts-wqy-zenhei

   # 安装思源字体
   sudo apt install fonts-source-han-sans fonts-source-han-serif
   ```

   这种方法的优点是系统会自动处理字体配置和更新。

**二、安装到用户目录（无需 root 权限，仅当前用户可用）**

1. **创建用户字体目录**（如果不存在）：

   ```bash
   mkdir -p ~/.local/share/fonts
   ```

2. **将字体文件复制到该目录**：

   ```bash
   cp /path/to/your/font.ttf ~/.local/share/fonts/
   ```

   或者如果你有多个字体文件：

   bash

   ```bash
   cp /path/to/your/fonts/* ~/.local/share/fonts/
   ```

3. **更新字体缓存**：

   ```bash
   fc-cache -fv ~/.local/share/fonts
   ```

4. **验证字体是否安装成功**：

   ```bash
   fc-list | grep "字体名称"
   ```
