# -
无卵用的记录

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



### 


// 相等IPV6地址数量
// we have defined the necessary header files here for this problem.
// If additional header files are needed in your program, please import here.
#include <algorithm>
#include <cctype>
#include <cmath>
#include <fstream>
// #include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

bool AllDigits(string str)
{
    bool flag = true;
    for (char c : str) {
        flag = flag && isdigit(c);
    }
    return flag;
}

int CountAlpha(string str)
{
    int ans = 0;
    for (char c : str) {
        ans = isalpha(c) ? ans + 1 : ans;
    }
    return ans;
}

bool Is4Char(string str)
{
    return str.size() == 4;
}

bool Is0Start(string str)
{
    return str.front() == '0';
}

bool IsZero(string str)
{
    return stoi(str) == 0;
}

// 计算每个片段的可能性
int calcPossibilitiesPerSeg(string str)
{
    if (IsZero(str)) {
        return 2;
    }

    if (Is4Char(str)) {
        if (!Is0Start(str)) {
            if (CountAlpha(str) == 0) {
                return 1; // 4字符 + 非0开头 + 无字母
            } else {
                return pow(2, CountAlpha(str)); // 4字符 + 非0开头 + 有字母
            }
        } else {
            if (CountAlpha(str) == 0) {
                return 2; // 4字符 + 0开头 + 无字母
            } else {
                return 2 * pow(2, CountAlpha(str)); // 4字符 + 0开头 + 有字母
            }
        }
    } else { // 少于4字符
        if (!Is0Start(str)) {
            if (CountAlpha(str) == 0) {
                return 2; // 少于4字符 + 非0开头 + 无字母
            } else {
                return 2 * pow(2, CountAlpha(str)); // 少于4字符 + 非0开头 + 有字母
            }
        } else {
            if (CountAlpha(str) == 0) {
                return 2 + 1; // 少于4字符 + 0开头 + 无字母
            } else {
                return 2 * pow(2, CountAlpha(str)) + 1; // 少于4字符 + 0开头 + 有字母
            }
        }
    }
}

// 用途：双指针计算连续的0
// 标记连续0段（大于1个）的位置，初始化为1，标记为0
// 8段最多3个连续0
vector<vector<int>> Continue0Pos(vector<int> vec)
{
    vector<vector<int>> ans;
    vector<int> tmp(8, 1); // 初始化为1，为0的段标记为0

    int left = 0;
    int right = left;
    int len = vec.size();
    while (left < len) {
        if (vec[left] == 0) {
            tmp[left] = 0;
            right = left + 1;
            while (right < len && vec[right] == 0) {
                tmp[right] = 0;
                right++;
            }
            if (count(tmp.begin(), tmp.end(), 0) > 1) { // 连续0（大于1个）
                ans.push_back(tmp);
            }
            tmp.assign(8, 1); // vector赋值全1
            left = right + 1;
        } else {
            left++;
        }
    }
    return ans;
}

int main()
{
    // please define the C++ input here. For example: int a,b; cin>>a>>b;;
    stringstream sstr;
    string str;
    string s;

    vector<string> ipv6Seg;
    getline(cin, str);
    sstr.str(str);
    while (getline(sstr, s, ':')) {
        ipv6Seg.push_back(s);
    }

    // please finish the function body here.
    vector<int> numPerSeg(8, 0);
    vector<int> equalZero(8, 0); // 标记0的位置
    // 1、单个段
    for (int i = 0; i < 8; i++) {
        str = ipv6Seg[i];
        numPerSeg[i] = calcPossibilitiesPerSeg(str);
        equalZero[i] = IsZero(str) ? 0 : 1;
    }
    int ans = 1;
    ans = accumulate(numPerSeg.begin(), numPerSeg.end(), ans, multiplies<int>());
    // 2、连续零(不小于2段)
    vector<vector<int>> subContinue0 = Continue0Pos(equalZero);

    int ansPartII = 1;
    // for (int i = 0; i < subContinue0.size(); i++) {
    //     for (int j = 0; j < 8; j++) {
    //         if (j == subContinue1[i])
    //     }
    // }

    // please define the C++ output here. For example:cout<<____<<endl;
    // cout << stoi(ipv6Seg[6], 0, 16) << endl;
    // cout << ans << endl;

    // string x = "0a0";
    // bool alldigits = AllDigits(x);
    // int alphanum = CountAlpha(x);
    // bool zerostart = Is0Start(x);
    // bool fourchar = Is4Char(x);
    // int cnt = calcPossibilities(x);


    // stringstream sstr;
    // string str("01100111");
    // string s;

    // vector<string> ipv6Seg;
    // // getline(cin, str);
    // sstr.str(str);
    // while (getline(sstr, s, '0')) {
    //     ipv6Seg.push_back(s);
    // }
    return 0;
}
  
  
  1050:0:0:1234:6789:3450:3333:3261
  5
  0:0:0000:0:0000:0:0000:0
  257
  a050:b000:c000:d234:a000:c450:c234:b269
  256
  0000:0000:1000:0:0:3450:0:0000
  109
  
    
    
    ---
    1、

识别无线信号连续覆盖区域


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
