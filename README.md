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

int calcPossibilities(string str)
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

vector<vector<int>> Continue1Num(vector<int> vec)
{
    vector<vector<int>> ans;
    vector<int> tmp;

    int left = 0;
    int right = left;
    int len = vec.size();
    while (left < len) {
        if (vec[left] == 1) {
            tmp.push_back(left);
            right = left + 1;
            while (right < len && vec[right] == 1) {
                tmp.push_back(right);
                right++;
            }
            if (tmp.size() > 1) {
                ans.push_back(tmp);
            }
            tmp.clear();
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
    vector<int> equalZero(8, 0);
    // 对每个段进行判断，有几种可能
    for (int i = 0; i < 8; i++) {
        str = ipv6Seg[i];
        numPerSeg[i] = calcPossibilities(str);
        equalZero[i] = IsZero(str) ? 1 : 0;
    }
    int ans = 1;
    ans = accumulate(numPerSeg.begin(), numPerSeg.end(), ans, multiplies<int>());
    vector<vector<int>> subContinue1 = Continue1Num(equalZero);
    int ansPartII = 1;
    for (int i = 0; i < subContinue1.size(); i++) {
        for (int j = 0; j < 8; j++) {
            if (j == subContinue1[i])
        }
    }

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
  
