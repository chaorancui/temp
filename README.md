# -
无卵用的记录

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



    
    
---
```markdown
1、 识别无线信号连续覆盖区域

某天小王搭小黄的车从东莞一路到了深圳，期间接了一个电话，一路上电话都没有中断，小王在想这是为什么呢？基站的信号覆盖有这么远吗？实际上我们单个基站的信号覆盖并没有那么远，这中间可能切换了好几个基站了，但是对于打电话的人并不感知，这就得益于无线信号的连续覆盖和平滑切换。
为了简化处理我们假设所有基站的信号都是360度覆盖，覆盖半径都是300m（也即两个站点间距离小于等于600m，则认为是连续覆盖），同时我们假设基站所在坐标是平面的，已知输入一批基站坐标，请帮忙计算小王打着电话从坐标A移动到坐标B的过程，能否找到一条信号不中断的路线，如果存在这样的路径，则输出小王所需要经过的最少的信号连续覆盖的站点数量，否则输出-1。

解答要求
时间限制: 800ms, 内存限制: 100MB
输入
第一行为起始坐标A，
第二行为终点坐标B，
第三行为站点数量M，M的取值范围[1, 10000]；
接下来M行为每个站点的坐标，坐标取值范围[-100000, 100000]，输入坐标可能是乱序的，比如：
200 300
800 800
3
400 400
700 600
500 500

输出
如果不会中断输出沿途经过的连续覆盖区域的最少站点数量，如果会中断则输出-1，如上例子，起点(200 300)和终点（800，800），则最少经过的站点为：
400 400
700 600

最少2个站点，所以输出为：
2

样例1
复制输入：
200 300
800 800
3
400 400
500 500
700 600
复制输出：
2
解释：
起点(200 300)和终点（800，800），则最少经过的站点为：
400 400
700 600
则输出结果为2

样例2
复制输入：
200 300
800 800
1
500 500
复制输出：
-1
解释：
站点（500,500）无法覆盖起点和终点，所以输出结果为-1

样例3
复制输入：
400 400
800 800
1
600 600
复制输出：
1
解释：
站点（600,600）可以覆盖起点和终点，所以输出结果为1
    
```
    
    
```Java
// We have imported the necessary tool classes.
// If you need to import additional packages or classes, please import here.

public class Main {
    public static void main(String[] args) {
    // please define the JAVA input here. For example: Scanner s = new Scanner(System.in);
    // please finish the function body here.
    // please define the JAVA output here. For example: System.out.println(s.nextInt());
        Scanner scanner = new Scanner(System.in);
        String start = scanner.nextLine();
        String end = scanner.nextLine();
        int siteNum = Integer.parseInt(scanner.nextLine());
        String[] sites = new String[siteNum];
        for (int i = 0; i < siteNum; i++) {
            sites[i] = scanner.nextLine();
        }
        ShortestPathUtil shortestPathUtil = new ShortestPathUtil();
        System.out.println(shortestPathUtil.solve(start, end, sites));
    }
}

class ShortestPathUtil {
    private static final int ISD = 300;
    private final Queue<SiteInfo> opens = new ArrayDeque<>();

    int solve(String rawStart, String rawEnd, String[] rawSites) {
        int len = rawSites.length;
        SiteInfo[] siteInfos = new SiteInfo[len + 2];
        SiteInfo start = createPoint(rawStart, 0);
        start.distance = 0;
        start.isVisited = true;
        siteInfos[0] = start;
        int target = len + 1;
        SiteInfo end = createPoint(rawEnd, target);
        siteInfos[target] = end;
        for (int i = 0; i < len; i++) {
            siteInfos[i + 1] = createPoint(rawSites[i], i + 1);
        }

        opens.add(start);
        while (!opens.isEmpty()) {
            SiteInfo cur = opens.poll();
            List<Integer> neighbors = searchNeighbors(cur, siteInfos);
            for (int neighborId: neighbors) {
                if (neighborId == target) {
                    return cur.distance;
                }
                siteInfos[neighborId].isVisited = true;
                siteInfos[neighborId].distance = cur.distance + 1;
                opens.add(siteInfos[neighborId]);
            }
        }
        return -1;
    }

    private List<Integer> searchNeighbors(SiteInfo cur, SiteInfo[] siteInfos) {
        List<Integer> neighbors = new ArrayList<>();
        for (SiteInfo siteInfo : siteInfos) {
            if (siteInfo.isVisited) {
                continue;
            }
            int coverage = 0;
            if (cur.id != 0) {
                coverage += ISD;
            }
            if (siteInfo.id != siteInfos.length - 1) {
                coverage += ISD;
            }
            if (isNear(cur, siteInfo, coverage)) {
                neighbors.add(siteInfo.id);
            }
        }
        return neighbors;
    }

    private boolean isNear(SiteInfo a, SiteInfo b, int coverage) {
        return Math.pow(a.lon - b.lon, 2) + Math.pow(a.lat - b.lat, 2) <= Math.pow(coverage, 2);
    }

    private SiteInfo createPoint(String raw, int index) {
        String[] raws = raw.split(" ");
        return new SiteInfo(Integer.parseInt(raws[0]), Integer.parseInt(raws[1]), index);
    }
}

class SiteInfo {
    int lat;
    int lon;
    int id;
    boolean isVisited;
    int distance;

    public SiteInfo(int lat, int lon, int id) {
        this.lat = lat;
        this.lon = lon;
        this.id = id;
        this.isVisited = false;
        this.distance = -1;
    }
}
```


```markdown
200 300
800 800
3
400 400
500 500
700 600

2
```

```markdown
2100 0
9900 0
100
46600 31300
67100 88900
42900 50200
57900 83700
79400 94000
55400 40300
56100 57800
79800 37900
7200 0
91200 66700
70700 61700
73500 89000
33200 60400
28800 83000
25200 50900
85400 84500
43700 41200
5400 0
80100 79800
40800 88200
43000 54300
2400 0
60700 49200
40100 50800
70800 64700
7800 0
69300 58800
38900 34200
1200 0
89800 71400
60100 42700
94800 61900
9600 0
25900 60700
69000 53200
76200 37600
55900 25300
94000 26200
500 5100
80200 30000
8700 10200
58500 49900
84400 97200
52700 62300
88900 42600
60600 34200
39700 85400
74500 32900
3000 0
74700 62100
89300 84000
4200 2200
33000 79600
8400 0
38200 84700
5400 0
48800 68600
32900 28900
78100 50300
60700 52600
98400 46500
37700 32300
72400 83500
32800 25800
76900 40700
76400 38600
4200 0
6000 0
1700 2400
74600 99200
96300 73900
31900 60200
52900 54000
9300 1700
94000 32900
3600 0
31400 38000
57100 54900
85700 26100
47600 30500
85200 32000
98600 82400
63700 65400
47700 73900
76500 84100
91400 63500
68500 37500
82200 84300
50200 50900
38000 32900
4800 0
9000 0
91900 92900
95000 62000
48000 70800
6600 0
99300 35900
3000 0
67700 26100
63000 99700

13
```

```markdown
9300 0
23700 0
200
5400 0
7800 0
48800 68600
38200 84700
8400 0
48400 40700
14400 0
40100 50800
23400 0
80200 30000
25900 60700
99800 27500
46900 88900
70800 64700
8700 10200
92500 36200
5400 0
69300 58800
89800 71400
80200 30000
1200 0
18000 0
91200 66700
89800 71400
80100 79800
25200 50900
9600 0
43100 52000
18000 0
5400 0
38900 34200
13800 0
82300 85100
5400 0
14400 0
46900 44500
600 0
79400 94000
600 0
7800 0
40100 50800
65900 80500
7200 0
25900 60700
60100 42700
40800 88200
9600 0
13800 0
20000 0
5400 0
32900 28900
33200 60400
32900 28900
38200 84700
94800 61900
51200 32900
91200 66700
80200 30000
8400 0
89800 71400
82500 85100
40100 50800
79400 94000
48800 68600
38900 34200
94200 99500
9600 0
41300 86000
48800 68600
89800 71400
15000 0
20400 0
1200 0
60900 51000
70700 61700
94000 26200
72300 70800
1200 0
5400 0
56000 90700
18600 0
40800 88200
94000 26200
20000 0
59200 36500
21000 0
8400 0
19600 0
79800 37900
32900 28900
79400 94000
10800 0
56100 57800
16200 0
84100 80000
3000 0
69300 58800
79800 37900
12600 0
33200 35400
21600 0
7800 0
21600 0
33200 60400
20400 0
25200 50900
91200 66700
33200 60400
7200 0
13200 0
23400 0
19200 0
51400 31900
80100 79800
38200 84700
79400 94000
22200 0
21000 0
18600 0
27900 78800
9600 0
80200 30000
44300 85400
22800 0
69300 58800
8400 0
91600 35400
22200 0
57700 96700
8700 10200
11400 0
40100 50800
60700 49200
32900 28900
91200 66700
8700 10200
89300 84000
25200 50900
1200 0
12000 0
38900 34200
56100 57800
60100 97800
16200 0
9600 0
5400 0
60700 49200
16800 0
7200 0
69300 58800
79800 37900
10200 0
5400 0
94000 26200
17400 0
52500 84700
3000 0
16800 0
600 0
15600 0
19200 0
33200 60400
17400 0
38900 34200
52000 54200
7200 0
15600 0
81300 38500
25900 60700
19600 0
70100 95300
8700 10200
4200 2200
38600 89000
25200 50900
25900 60700
15000 0
94800 61900
22800 0
40100 50800
56100 57800
14300 8300
94800 61900
94800 61900
48800 68600
7000 6000
58700 77500
79800 37900
7800 0
36700 35800
80100 79800
4200 2200
80100 79800
94000 26200
56100 57800
60700 49200
600 0
6700 4900
38200 84700
60700 49200

25
```

https://shenjun4cplusplus.github.io/cplusplushtml/%E7%AC%AC3%E7%AB%A0%20%E5%A4%84%E7%90%86%E6%95%B0%E6%8D%AE/3_4_1%20%E8%BF%90%E7%AE%97%E7%AC%A6%E4%BC%98%E5%85%88%E7%BA%A7%E5%92%8C%E7%BB%93%E5%90%88%E6%80%A7.html

https://docs.microsoft.com/zh-cn/cpp/cpp/cpp-built-in-operators-precedence-and-associativity?view=msvc-170


```c++
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

class StorageSystem {
 public:
  StorageSystem(int coldstoregeNum, int coldStoregePirce, int normalStorageNum,
                int normalStoragePirce, int delay) {
    coldSotregeNum_ = coldstoregeNum;
    coldStoregePirce_ = coldStoregePirce;
    normalStorageNum_ = normalStorageNum;
    normalStoragePirce_ = normalStoragePirce;
    delay_ = delay;
  }

  int Store(int date, int storageId, int storageType, int storageDays) {
    Query(date);
    if ((storageType == 0 && coldSotregeNum_ <= 0) ||
        (storageType == 1 && (coldSotregeNum_ + normalStorageNum_ <= 0))) {
      return -1;
    }

    if (storageType == 0) {
      sys[storageId] = {date, storageType, storageDays};
      coldSotregeNum_--;
      return storageDays * coldStoregePirce_;
    }

    if (normalStorageNum_ <= 0) {
      sys[storageId] = {date, 0, storageDays};
      coldSotregeNum_--;
      return storageDays * coldStoregePirce_;
    } else {
      sys[storageId] = {date, 1, storageDays};
      normalStorageNum_--;
      return storageDays * normalStoragePirce_;
    }
  }

  int Retrieve(int date, int storageId) {
    int ret = 0;
    Query(date);
    if (sys.count(storageId) == 0) {
      return -1;
    }
    int beyond = date - (sys[storageId].date + sys[storageId].storageDays);
    if (beyond <= delay_) {
      get[storageId] = sys[storageId];
    }
    if (0 < beyond && beyond <= delay_) {
      int price = sys[storageId].storageType == 0 ? coldStoregePirce_ : normalStoragePirce_;
      ret = beyond * price;
    }
    if (sys[storageId].storageType == 0) {
      coldSotregeNum_++;
    } else {
      normalStorageNum_++;
    }
    sys.erase(storageId);
    return ret;
  }

  vector<int> Query(int date) {
    for (auto it = sys.begin(); it != sys.end();) {
      int beyond = date - (it->second.date + it->second.storageDays);
      if (beyond > delay_) {
        del[it->first] = it->second;
        if (it->second.storageType == 0) {
          coldSotregeNum_++;
        } else {
          normalStorageNum_++;
        }
        it = sys.erase(it);
      } else {
        it++;
      }
    }

    int g = get.size();
    int in = sys.size();
    int d = del.size();
    return {g, in, d};
  }

 private:
  struct crit {
    int date;
    int storageType;
    int storageDays;
  };

  unordered_map<int, crit> sys;
  unordered_map<int, crit> del;
  unordered_map<int, crit> get;
  int coldSotregeNum_{0};
  int coldStoregePirce_{0};
  int normalStorageNum_{0};
  int normalStoragePirce_{0};
  int delay_{0};
};

int main() {
  return 0;
}

```

第一题：DiskSystem AC

实现一个磁盘系统的增、删、整理

初始化一个大小为capacity容量的磁盘

增：给定一个文件fileid和大小，若磁盘能存放，将其存放在磁盘中，可以不连续，返回最后一个存放数据的位置索引。若空间不够，返回-1

删：删除指定fileId的文件，若无这个文件，返回-1

整理：将磁盘文件按大小依次存放在磁盘中，返回文件个数

-Java 代码
查看代码
01
import java.util.Map;
02
import java.util.TreeMap;
03
 
04
class DiskSystem {
05
    // 这里使用一个数组作为磁盘容器，并使用一个int值记录剩下的磁盘容量
06
    private int[] disk;
07
    private int lastSize;
08
    // 初始化，按照给定的大小建立数组，并初始化剩余容量
09
    public DiskSystem(int capacity) {
10
        this.disk = new int[capacity];
11
        this.lastSize = capacity;
12
    }
13
 
14
    public int add(int fileId, int fileSize) {
15
        // 看剩余容量是否满足增加文件，若不满足，返回-1。建立剩余容量的好处就在于可以少遍历几次数组
16
        int lastfile = fileSize;
17
        if (this.lastSize < fileSize) {
18
            return -1;
19
        }
20
        for (int i = 0; i < this.disk.length; i++) {
21
      // 遍历数组，为0的空间放置文件，同时减小剩余空间、文件大小，当文件大小为0，返回当前索引。
22
            if (this.disk[i] == 0) {
23
                this.disk[i] = fileId;
24
                lastfile -= 1;
25
                this.lastSize -= 1;
26
            }
27
            if (lastfile == 0) {
28
                return i;
29
            }
30
        }
31
        return -1;
32
    }
33
 
34
    public int remove(int fileId) {                
35
    // 先记录当前剩余位置，遍历一边数组，符合给fileId的置0，磁盘剩余容量+1。判断遍历后的磁盘剩余容量是否相等。 
36
        // 若相同，则不存在fileId，返回-1;若不同，返回当前磁盘剩余容量。
37
        int beforeRemoveSize = this.lastSize;
38
        for (int i = 0; i < this.disk.length; i++) {
39
            if (this.disk[i] == fileId) {
40
                this.disk[i] = 0;
41
                this.lastSize += 1;
42
            }
43
        }
44
        if (this.lastSize > beforeRemoveSize) {
45
            return this.lastSize;
46
        } else {
47
            return -1;
48
        }
49
    }
50
 
51
    public int defrag() { 
52
        // 整理空间，遍历数组，使用treeMap，记录文件个数，treeMap保证了文件按大小顺序排列，数组为0时跳过。
53
        Map<Integer, Integer> treemap = getFiles();
54
        int index = 0;
55
        int files = 0;
56
        for (Map.Entry<Integer, Integer> treeEntry : treemap.entrySet()) {
57
            // 遍历treeMap，将值填到数组中。
58
            files += 1;
59
            for (int i = 0; i < treeEntry.getValue(); i++) {
60
                this.disk[index] = treeEntry.getKey();
61
                index += 1;
62
            }
63
        }
64
        // 剩余数组，置0，有很多测试用例通过但是提交报错的可能就少这一步。
65
        for (int i = index; i < this.disk.length; i++) {
66
            this.disk[i] = 0;
67
        }
68
        return files;
69
    }
70
 
71
    public Map<Integer, Integer> getFiles() {
72
        TreeMap<Integer, Integer> map = new TreeMap<>();
73
        for (int i : this.disk) {
74
            if (i == 0) {
75
                continue;
76
            }
77
            if (map.containsKey(i)) {
78
                int curNum = map.get(i);
79
                map.put(i, curNum + 1);
80
            } else {
81
                map.put(i, 1);
82
            }
83
        }
84
        return map;
85
    }



第二题：操作系统文件拷贝
输入：

TargetDir []string：目标文件路径
DstDirLine int：被拷贝到第几行文件夹下
SrcDir []string：需要拷贝的文件夹
输出：
[]string：拷贝完后的文件路径，并且文件要以字典序排序
题目描述得很复杂，但是其实就是把一个目录拷贝到另外一个目录下面，满足三个条件：

同一层级不能有相同命名的文件夹，如果目标路径有和原路径相同的文件夹，则需要合并子文件
如果目标路径有，但是原路径没有，则保留目标路径的文件夹
如果目标路径没有，但是原路径有，则创建新的文件夹
注意：SrcDir的根目录不会被拷贝
例一：
TargetDir :

HOME
  log
    config
  license
    lib32
    lib64
  usr
  pkg
DstDirLine: 1
SrcDir:

bin
  games
  license
    lib32
    libx86
  usr
    pwd
如上图，被拷贝到第一行文件夹下，也就是HOME下，最后输出如下

HOME
  games
  license
    lib32
    lib64
    libx86
  log
    config
  pkg
  usr
    pwd
代码：

type treeNode struct {
	name     string
	level    int
	children []*treeNode
}
 
func copyDir(targetDir []string, dstDirLine int, srcDir []string) []string {
	res := make([]string, 0)
	targetTree, dstTree := buildTree(targetDir, dstDirLine)
	srcTree, _ := buildTree(srcDir, 0)
	if dstDirLine == 1 {
		combineTree(targetTree, srcTree)
	} else {
		combineTree(dstTree, srcTree)
	}
	res = printRes(targetTree, 0, res)
	return res
}
 
func combineTree(dst, src *treeNode) {
	if src == nil {
		return
	}
	if len(dst.children) == 0 {
		for _, node := range src.children {
			dst.children = append(dst.children, node)
		}
		sortChildren(dst.children)
		return
	}
	nameNodeMap := make(map[string]*treeNode)
	for _, node := range dst.children {
		nameNodeMap[node.name] = node
	}
	for _, node := range src.children {
		if oriNode, ok := nameNodeMap[node.name]; ok {
			combineTree(oriNode, node)
		} else {
			dst.children = append(dst.children, node)
		}
	}
	sortChildren(dst.children)
}
 
func printRes(targetTree *treeNode, indent int, res []string) []string {
	res = append(res, strings.Repeat(" ", indent*2) + targetTree.name)
	sortChildren(targetTree.children)
	for _, node := range targetTree.children {
		res = printRes(node, indent + 1, res)
	}
	return res
}
 
func sortChildren(children []*treeNode) {
	sort.Slice(children, func(i, j int) bool {
		return children[i].name < children[j].name
	})
}




请设计一个仓库管理系统，实现如下功能：

StorageSystem(int coldStorageNum, int coldStoragePrice, int normalStorageNum, int normalStoragePrice, int delay) -初始化仓库信息。

仓库有冷藏和常温两种类型的储藏室，初始化其对应的数量和每天租赁价格；

若客户租赁过期且超出delay天后，依旧未提取货物，该储物区将被清空；

Store(int date, int storageId, int storageType, int storageDays) -在日期date为存单storageId租赁storageType类型的一个储藏室，并存放物品storageDays天。

若有空间则存储成功，则需预付storageDays的费用（按照实际储藏室类型进行计算：天数*每日租赁价格），返回该费用；

        当常温储藏室空间不足时，可使用空闲的冷藏储藏室存储；反之不可以；

        date为【租赁起始日期】，日期超过date + storageDays时开始过期

若无空间则不做任何处理，并返回 -1.
系统保证storageId参数全局唯一，storageType为0表示冷藏，1表示常温。

Retrieve(int date, int storageId) -在日期date，客户取出存单storageId（存单一定存在且未被提取）对应的物品：

若存单过期时，则取出物品，并返回0；

若存单过期但未超出delay天，则取出物品，并返回需要补交的费用（实际延迟天数*每日价格），实际延迟天数=date - （租赁起始日期 + storageDays）；

若存单过期且已超出delay天（日期超过 租赁起始日期 + storageDays + delay）时，则物品已被清空，则取出失败，并返回 -1.

Query(int date) -请返回截止日期date时3种状态的存单数量序列，依次为：物品已成功取出，物品未取仍在仓库中，物品被清空的存单数量。

注意：保证函数store、retrieve、query的日期date参数按输入顺序非严格递增；

示例1：

输入：

["StorageSystem", "store", "retrieve", "query"]

[[2,2,1,1,2], [0,1,0,2], [3.1], [3]]

输出[null, 4, 2, [1, 0, 0]]




class StorageSystem {

public:

    StorageSystem(int coldStorageNum, int coldStoragePrice, int normalStorageNum, 

                                int normalStoragePrice, int delay)

    {

       

    }



    int Store(int date, int storageId, int storageType, int storageDays)

    {

        

    }



    int Retrieve(int date, int storageId)

    {

        

    }



    vector<int> Query(int date)

    {

       

    }

};


分析：
涉及题，首先得选好数据结构，由题意storageId全局唯一，且需要在函数调用中添加、查找、删除，可以使用时间复杂度为O（1）的哈希表<stroageId, 物品信息>来表示仓库，物品信息可自定义结构体表示。如下代码是提交已通过代码，可作参考。




class StorageSystem {

public:

    StorageSystem(int coldStorageNum, int coldStoragePrice, int normalStorageNum, 

                                int normalStoragePrice, int delay)

    {

        this->coldStorageNum = coldStorageNum;

        this->coldStoragePrice = coldStoragePrice;

        this->normalStorageNum = normalStorageNum;

        this->normalStoragePrice = normalStoragePrice;

        this->delay = delay;

    }



    int Store(int date, int storageId, int storageType, int storageDays)

    {

        Query(date);

        if ((storageType == 0 && coldStorageNum <= 0) || 

            (storageType == 1 && (coldStorageNum + normalStorageNum <= 0))) {

            return -1;

        }

        if (storageType == 0) {

            sys[storageId] = {date, storageType, storageDays};

            coldStorageNum--;

            return storageDays * coldStoragePrice;

        }

        if (normalStorageNum <= 0) {

            sys[storageId] = {date, 0, storageDays};

            coldStorageNum--;

            return storageDays * coldStoragePrice;

        } else {

            sys[storageId] = {date, 1, storageDays};

            normalStorageNum--;

            return storageDays * normalStoragePrice;

        }

    }



    int Retrieve(int date, int storageId)

    {

        int ret = 0;

        Query(date);

        if (sys.count(storageId) == 0) {

            return -1;

        }

        int beyond = date - (sys[storageId].date + sys[storageId].storageDays);

        if (beyond <= delay) {

            get[storageId] = sys[storageId];

        }

        if (0 < beyond && beyond <= delay) {

            int price = sys[storageId].storageType == 0 ? coldStoragePrice : normalStoragePrice;

            ret = beyond * price;

        }

        if (sys[storageId].storageType == 0) {

            coldStorageNum++;

        } else {

            normalStorageNum++;

        }

        sys.erase(storageId);

        return ret;

    }



    vector<int> Query(int date)

    {

        for (auto it = sys.begin(); it != sys.end();) {

            int beyond = date - (it->second.date + it->second.storageDays);

            if (beyond > delay) {

                del[it->first] = it->second;

                if (it->second.storageType == 0) {

                    coldStorageNum++;

                } else {

                    normalStorageNum++;

                }

                it = sys.erase(it);

            } else {

                it++;

            }

        }

        int g = get.size();

        int in = sys.size();

        int d = del.size();

        return {g, in, d};

    }



private:

    unordered_map<int, crit> sys;

    unordered_map<int, crit> del;

    unordered_map<int, crit> get;

    int coldStorageNum {0};

    int coldStoragePrice {0};

    int normalStorageNum {0};

    int normalStoragePrice {0};

    int delay {0};

};



class RateLimitSystem1 {
public:
    explicit RateLimitSystem1(int tokenLimit)
    {
        maxCardNum = tokenLimit;
        this->rateSystem = vector<tuple<int, int, int>>(1000);
    }

    bool AddRule(int ruleId, int time, int interval, int number)
    {
        if (system.count(ruleId)) {
            return false;
        } else {
            rateSystem[ruleId] = { time, interval, number };
            system[ruleId] = 1;
            UpdateCardNum(time);
            return true;
        }
    }

    bool RemoveRule(int ruleId, int time)
    {
        if (!system.count(ruleId)) {
            return false;
        } else {
            UpdateCardNum(time);
            system.erase(ruleId);
            return true;
        }
    }

    bool TransferData(int time, int size)
    {
        UpdateCardNum(time);
        if (curCardNum < size) {
            return false;
        }
        curCardNum = curCardNum - size;
        return true;
    }
    void UpdateCardNum(int curTime)
    {
        for (int tempTime = lastOrderTime; tempTime <= curTime; tempTime++) {
            for (auto item : system) {
                int id = item.first;
                auto [time, interval, number] = rateSystem[id];
                if (tempTime < time) {
                    continue;
                }
                if ((tempTime - time) % interval == 0) {        // 设计精妙的地方在这里，时间步长为1往后扫描！！！
                    curCardNum = std::min(curCardNum + number, maxCardNum);
                }
            }
        }
        lastOrderTime = curTime + 1;
    }
    int QueryToken(int curTime)
    {
        UpdateCardNum(curTime);
        return curCardNum;
    }

private:
    int maxCardNum{0};
    int curCardNum{0};
    int lastOrderTime{0};
    vector<tuple<int, int, int> > rateSystem;   //此处的tuple可以用struct替代
    map<int, int> system;
};

```C++
#include <iostream>
#include <string>
#include <vector>
#include <utility>
#include <algorithm>
#include <map>
using namespace std;


class RateLimitSystem {
public:
    int tokenLimit_;
    int tokenNumber_;
    int time_; // 用于保存每次操作的时间
    struct Rule_ {
        int time;
        int interval;
        int number;
    };
    map<int, Rule_> tokenMap_;

    explicit RateLimitSystem(int tokenLimit)
    {
        tokenLimit_ = tokenLimit;
        tokenNumber_ = 0;
        time_ = 0;
    }

    bool AddRule(int ruleId, int time, int interval, int number)
    {
        Rule_ rule = { time, interval, number };
        auto result = tokenMap_.insert(pair<int, Rule_>(ruleId, rule));
        bool flag = result.second;
        updateTokenNumber(time);
        time_ = time + 1;
        return flag;
    }

    bool RemoveRule(int ruleId, int time)
    {
        updateTokenNumber(time);
        bool flag = false;
        if (tokenMap_.find(ruleId) != tokenMap_.end()) {
            tokenMap_.erase(ruleId);
            flag = true;
        }

        time_ = time + 1;
        return flag;
    }

    bool TransferData(int time, int size)
    {
        updateTokenNumber(time);
        bool flag = false;
        if (tokenNumber_ >= size) {
            tokenNumber_ -= size;
            flag = true;
        }
        time_ = time + 1;
        return flag;
    }

    int QueryToken(int time)
    {
        updateTokenNumber(time);
        time_ = time + 1;
        return tokenNumber_;
    }

    void updateTokenNumber(int time)
    {
        for (auto iter = tokenMap_.begin(); iter != tokenMap_.end(); ++iter) { // 每一种规则令牌计数
            for (int i = iter->second.time; i <= time; i += iter->second.interval) { // 规则i令牌计算
                if (i < time_) {
                    continue;
                }
                if (tokenNumber_ + iter->second.number <= tokenLimit_) {
                    tokenNumber_ += iter->second.number;
                } else {
                    tokenNumber_ = tokenLimit_;
                }
            }
        }
    }
};


int main()
{
    RateLimitSystem sol(8);
    cout << sol.AddRule(0, 0, 1, 3) << endl;
    cout << sol.AddRule(1, 2, 2, 1) << endl;
    cout << sol.TransferData(3, 12) << endl;
    cout << sol.RemoveRule(3, 4) << endl;
    cout << sol.RemoveRule(0, 5) << endl;
    cout << sol.TransferData(6, 8) << endl;
    cout << sol.QueryToken(7) << endl;
    cout << sol.RemoveRule(1, 8) << endl;
    cout << sol.QueryToken(9) << endl;
    cout << sol.AddRule(0, 10, 2, 2) << endl;
    cout << sol.QueryToken(12) << endl;
    cout << sol.AddRule(0, 13, 2, 2) << endl;
    cout << sol.TransferData(14, 8) << endl;


    cout << 10 << endl;

    return 0;
}
```







