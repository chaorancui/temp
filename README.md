# 无卵用的记录

```python
import struct
import operator
import numpy as np

''' 
BlockReduceMax：对每个block内所有元素求最大值。
BlockReduceMin：对每个block内所有元素求最小值。
BlockReduceSum：对每个block内所有元素求和。

构造样例：
BlockReduceMax 数据类型：fp16
BlockReduceMax 输入数据大小： 16 个 block
则BlockReduceMax 输出数据大小： 16
参数：
    分2次取完 = 16个block / 矢量计算单元每次读取连续的8个block
    src_size: 16 * 32 / sizeof(fp16) = 16 * 16 = 256
    dst_size: 16
    repeat: 2
    mask: 256 / sizeof(fp16) = 128，连续模式，单词迭代所有元素参与计算
    dstRepStride: 1，迭代间block连续写
    srcBlkStride: 1，单次迭代内block连续
    srcRepStride: 8，迭代间相同block地址步长8
'''



ONE_BLOCK_SIZE = 32 # 硬件每个 block 32B，固定的
RANDOM_SEED = 12306 # 随机种子的随机数组（为了确保结果的可重复性）


# 给定输入数据大小： 16 个 block， float16
# 则输出数据大小： 16
input_block_num = 16
element_byte_num = int(np.dtype(np.float16).itemsize)  # float16 数据类型占用的字节数，其余数据类型也按需修改
element_num_in_each_block = int(ONE_BLOCK_SIZE / element_byte_num)  # 每个 block 有多少个数据

src_size = int(input_block_num * element_num_in_each_block)
dst_size = int(input_block_num)


# 生成输入数据，，float16
np.random.seed(RANDOM_SEED)
srcData = np.random.random(src_size)
srcData = srcData.astype(np.float16)


# 一维数组中转换为二位数组，一维数组中每个block转换为二维数组中的一行
srcDataReshape = srcData.reshape(-1, element_num_in_each_block)


# 对每行（axis=1）数据进行计算，即求每个 block 内所有元素的函数计算结果
# ================ 多选一 BlockReducexxx ================
dstData = np.max(srcDataReshape, axis=1) # BlockReduceMax 输出结果
# dstData = np.min(srcDataReshape, axis=1) # BlockReducemin 输出结果
# dstData = np.sum(srcDataReshape, axis=1) # BlockReducesum 输出结果
# ================================


# 数据写入文件
srcData.tofile("input_data.bin")
dstData.tofile("golden_data.bin")


# 打印相关数据
print("\n================ float16 ================")
print("ONE_BLOCK_SIZE = 32B")
print("element_byte_num = ", element_byte_num)
print("element_num_in_each_block = ", element_num_in_each_block)

print("\n================ 输入输出维度 ================")
print("src_size = ", src_size, ", src_block_num = ", srcDataReshape.shape[0])
print("dst_size = ", dst_size)

print("\n================ 实际数据 ================")
print("srcData.shape = ", srcData.shape)
print("srcDataReshape.shape = ", srcDataReshape.shape)
print("dstData.shape = ", dstData.shape)
print("\n====src")
print(srcDataReshape)
print("\n====dst")
print(dstData)


def main():
    if len(sys.argv) < 2:
        print("params error! pelese input 1 param at least: conf_file")
        return -1

    conf_file = sys.argv[1]
    if not os.path.exists(conf_file):
        print("conf_file: %s not exist!!" % conf_file)
        exit(-1)

    print("conf_file: %s!" % conf_file)

    runner_type = "camodel"
    mode = "run"
    soc_version = soc_cfg.SocVersion.CharlottePro
    for i in range(2, len(sys.argv)):
        if "--runner_type=" in sys.argv[i]:
            runner_type = sys.argv[i].split("=")[-1]
        elif "--mode=" in sys.argv[i]:
            mode = sys.argv[i].split("=")[-1]
        elif "--soc_version=" in sys.argv[i]:
            soc_version = sys.argv[i].split("=")[-1]

    run_tick_by_yaml(conf_file, runner_type, mode, soc_version)
    exit(0)


if __name__ == '__main__':
    main()


mask参数使用逐bit模式，该模式的具体介绍请参考参数说明中的mask参数说明：
template <typename T, bool isSetMask = true> __aicore__ inline void BlockReduceMax(const LocalTensor<T>& dstLocal, const LocalTensor<T>& srcLocal,const int32_t repeat, const uint64_t mask[2], const int32_t dstRepStride, const int32_t srcBlkStride,const int32_t srcRepStride)

mask参数使用连续模式，该模式的具体介绍请参考参数说明中的mask参数说明：
template <typename T, bool isSetMask = true> __aicore__ inline void BlockReduceMax(const LocalTensor<T>& dstLocal, const LocalTensor<T>& srcLocal,const int32_t repeat, const int32_t maskCount, const int32_t dstRepStride, const int32_t srcBlkStride,const int32_t srcRepStride)
```

### python
https://pythonhowto.readthedocs.io/zh-cn/latest/module.html

### shell 学习
https://shellscript.readthedocs.io/zh-cn/latest/1-syntax/2-datatype/index.html

https://github.com/chaorancui/temp/blob/main/README.md

https://linuxstory.gitbook.io/advanced-bash-scripting-guide-in-chinese


### chrome 黑暗模式插件
Night Eye

### Guitar Pro 中文官网 
https://www.guitarpro.cc/xinwen/gp-rgfyh.html

### Xenomai (学习笔记)
https://blog.csdn.net/pwl999/article/details/109412539

### 什么是实时操作系统（RTOS）
https://zhuanlan.zhihu.com/p/86861756

### 继承与多态public private
https://shaofengjiang.cn/programming-course/lec9-inheritance.pdf

### 【C++】override和final关键字
https://blog.csdn.net/weixin_41838721/article/details/125232736?spm=1001.2014.3001.5502

### 面试经典问题，谈谈你对OOA,OOD,OOP的理解
https://lovojava.github.io/2017/06/19/20170619/

### 纯虚函数设置为public、protected和private的区别
https://blog.csdn.net/CLZHIT/article/details/105936620

### c++虚函数和纯虚函数以及static关键字
https://blog.csdn.net/weixin_44302602/article/details/112298053

### book-refactoring2
《重构 改善既有代码的设计第二版》中文版
https://book-refactoring2.ifmicro.com
电子书: pdf, epub, mobi


### IQ信号的学习
https://blog.csdn.net/goodnessg/article/details/123706807?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-9-123706807-blog-85958872.235^v40^pc_relevant_3m_sort_dl_base4&spm=1001.2101.3001.4242.6&utm_relevant_index=10


### 天地图key
702f9a64c89bc4c93c57338a0d5da2e6

### c++11增加的变参数模板，今天总算整明白了
https://www.helloworld.net/p/7580029278

### C++函数传参的时候，右引（T&&）和常引（const T&）接收的参数有什么不同，分别该什么时候用？
https://www.zhihu.com/question/437590377

### C++函数定义中占位参数（没有参数名）的作用
https://blog.csdn.net/LIsmooth/article/details/127210379

### C++ 为什么要让 struct 可以定义成员函数？
https://www.zhihu.com/question/49072961

### 如何离线安装 Oh My Zsh
https://blog.csdn.net/u012814856/article/details/100668640

Windows 系统中配置终端 Oh-My-Zsh 教程:https://dreamhomes.top/posts/202201092010/

Git-Zsh on Windows安装与配置:https://amagi.yukisaki.io/article/96e5adc4-1212-4260-8399-4dfd3964dc3b/

Zsh / Oh-my-zsh on Windows Git Bash:https://gist.github.com/fworks/af4c896c9de47d827d4caa6fd7154b6b

主题powerlevel10k：https://github.com/romkatv/powerlevel10k#oh-my-zsh

Linux查看及测试网络：https://blog.csdn.net/FP202530/article/details/125362831?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-1-125362831-blog-79207806.pc_relevant_3mothn_strategy_and_data_recovery&spm=1001.2101.3001.4242.2&utm_relevant_index=2

### zsh 编译下载
https://zsh.sourceforge.io/Arc/source.html
```shell
# 进入源码目录
cd zsh-5.8

# 执行配置
./configure   # 默认安装在：/usr/local/bin/zsh

# 编译和安装
make && make install

# 添加信息
vim /etc/shells
# 在最后一行加上：/usr/local/bin/zsh

./Util/preconfig
./configure
make && make install
```



### C++成员函数修饰词的意义和使用（&， &&， const， override）
https://blog.csdn.net/qls315/article/details/106849340

### C++-[override]关键字使用详解
https://blog.csdn.net/qq_42542471/article/details/124659190?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-124659190-blog-79122136.pc_relevant_recovery_v2&spm=1001.2101.3001.4242.1&utm_relevant_index=1

### C++ 直接初始化和拷贝初始化
https://blog.csdn.net/twdlll/article/details/78302349

### extern "C"：实现C++和C的混合编程
http://c.biancheng.net/view/8064.html

### 加载符号表：Linux下__attribute__((visibility ("default")))的使用
https://blog.csdn.net/fengbingchun/article/details/78898623

### C++ Primer英文第五版
chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://zhjwpku.com/assets/pdf/books/C++.Primer.5th.Edition_2013.pdf

### C++Primer第五版 习题答案
https://github.com/smzztx/CppPrimer_5th_cn

### 回调函数基本介绍和基本使用场景
https://blog.csdn.net/u014337397/article/details/80328277

### 设计模式网站
https://refactoringguru.cn/design-patterns

### vscode
https://www.thisfaner.com/p/vs-code-tips/

### C++点点滴滴（上）
https://azurery.github.io/2019/03/09/C++%E7%82%B9%E7%82%B9%E6%BB%B4%E6%BB%B4%EF%BC%88%E4%B8%8A%EF%BC%89/

### C++中的POD类型
https://cloud.tencent.com/developer/article/1814242
https://blog.csdn.net/Jxianxu/article/details/80524526

### [C++]五花八门的C++初始化规则
https://segmentfault.com/a/1190000039844285

### c++算术运算时数据类型提升带来的问题
https://www.programminghunter.com/article/2113391637/

### c++ cout 不能正常打印uint8_t
https://blog.csdn.net/carbon06/article/details/80856436

### 回调函数
https://www.runoob.com/w3cnote/c-callback-function.html

### 共享内存实现原理
https://www.jianshu.com/p/37b4cd5a25fd

### Linux下的共享内存
https://www.jianshu.com/p/962b03a7b400

### Bing搜索:Linux 下共享内存API

### linux ftok（）函数
https://www.cnblogs.com/joeblackzqq/archive/2011/05/31/2065161.html

### 进程间通信——共享内存（Shared Memory）
https://blog.csdn.net/ypt523/article/details/79958188

### 宋宝华：世上最好的共享内存(Linux共享内存最透彻的一篇)上集
https://blog.csdn.net/21cnbao/article/details/102994278?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.pc_relevant_is_cache&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.pc_relevant_is_cache

### =============================================
### PCL PCD（点云数据point clouds）文件格式
https://blog.csdn.net/hjwang1/article/details/52384903

### PCL点云数据格式，可用的PointT类型
https://blog.csdn.net/u013925378/article/details/83537844

### PCL学习（4.5）——点云对象的两种定义方式的区别与转换
https://blog.csdn.net/qq_30815237/article/details/86509741

### PCL点云的创建、访问与转换
https://www.cnblogs.com/hsy1941/p/11980775.html

### pcl小知识（十三）——两种读取和写入pcd点云文件的方法（根目录与指定目录）
https://blog.csdn.net/liukunrs/article/details/80769145


### =============================================
### PCL滤波--参数化模型投影点云---三维点云投影到二维平面
https://blog.csdn.net/Asabc12345/article/details/107045410

### PCL 根据参数模型将点云数据映射到指定的几何模型
https://blog.csdn.net/zhaoxr233/article/details/91997302?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param

### =============================================
### PCL实时显示点云流？？？？


### =============================================
### 点云数据滤波处理(PCL实现）（理论及头文件）
https://www.jianshu.com/p/a1c6cd7d411b

### 常见点云滤波算法(理论)
https://www.jianshu.com/p/5a1731d6226c

### PCL_几种点云滤波方法(代码)
https://blog.csdn.net/zhan_zhan1/article/details/103991733?utm_medium=distribute.pc_relevant.none-task-blog-searchFromBaidu-3.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-searchFromBaidu-3.control

### PCL点云滤波去噪
https://blog.csdn.net/qq_30815237/article/details/86294496?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.control

### PCL—低层次视觉—点云滤波（基于点云频率）
https://www.cnblogs.com/ironstark/p/5010771.html

### =============================================
### PCL ——最小包围盒(画出了最小包围盒并求出顶点坐标)(PCA)
https://blog.csdn.net/u013541523/article/details/82982522

### 3D点云目标识别和抓取
https://www.cnblogs.com/BellaVita/p/9979185.html

### 点云处理---最小矩形包围盒
https://blog.csdn.net/xuyi1218037/article/details/84298615

### [算法][包围盒]球，AABB，OBB
https://www.cnblogs.com/lyggqm/p/5386174.html


