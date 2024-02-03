# C++ STL快速入门

C++ 对模板（Template）支持得很好，STL 就是借助模板把常用的[数据结构](http://data.biancheng.net/)及其算法都实现了一遍，并且做到了数据结构和算法的分离。例如，

* vector 的底层为顺序表（数组），

* list 的底层为双向链表，(列表)

* deque 的底层为循环队列，(双端队列)？？

* set 的底层为红黑树，

* hash_set 的底层为哈希表。

  

  树是set和map的基础，set和map内部实现是基于RB-Tree。(set和map的区别：set的key=value)

  而unordered_set和unordered_map内部实现是基于哈希表(hashtable)，unordered_set和unordered_map内部实现的公共接口大致相同。
  
  ​    map可借助iterator或reverse_iterator进行正序和反序遍历
  
  ​    正序：for(**auto** iter = roman.begin(); riter != roman.end(); iter++)
  
  ​    反序：for(**auto** riter = roman.rbegin(); riter != roman.rend(); riter++)
  
  ​    unordered_map只能根据键值进行操作，若对key值有操作顺序的要求，unordered_map要求自己另行实现
  
  ___
  
  vector默认初始化为0
  
  char默认初始化为'\0'
  
  vector<string>  rows(8);定义包含8个string的vector
  
  
  
---

  ## 数据结构操作复杂度

  ### 向量容器

  ​    查询单个元素：O(n)

  ​    插入/删除单个元素：

  

  向量——vector(顺序容器)
  向量容器的特性
  向量容器的常用方法
  向量容器的遍历
  string 字符串(顺序容器)
  string 字符串的声明
  string的常用方法
  string字符串的操作和遍历
  stack - 堆栈容器(顺序容器)
  stack 堆栈容器的声明
  stack 堆栈容器的常用方法
  stack 堆栈容器的操作和遍历
  queue - 队列容器(顺序容器)
  queue 队列容器的声明
  queue 队列容器的常用方法
  queue 队列容器的操作和遍历
  deque - 双端队列容器(顺序容器)
  deque 双端队列容器的声明
  deque 双端队列容器的常用方法
  deque 双端队列容器的操作和遍历
  set - 集合容器（有序关联容器）
  set 集合容器的声明
  set 集合容器的常用方法
  set集合容器的操作和遍历
  map - 映照容器（有序关联容器）
  map 映照容器的声明
  map 映照容器的常用方法
  map 映照容器的操作和遍历

  

  

## algorithm 库函数

```c++
#include<algorithm>
```

* 排序
  * sort(v.begin(), v.end());
    > 默认升序    // [](int x, int y) {return x >= y; } 
  
  * merge(v.begin(), v.end(), b.begin(), b.end(), s.begin());
    > 合并有序

  * reverse(v.begin(), v.end());       
    > 逆序

  * random_shuffle(v.begin(), v.end());
    > 随机排序

* 查找
  * find(v.begin(), v.end(), 9);
    > 查找指定元素 没有返回 end
  
  * find_if(v.begin(), v.end(), [](int x) {return x >= 3; });
    > 返回一系列有条件的元素迭代器，最后一个参数是c++11中 LAMBDA表达式（匿名函数）写法，自定义了具体条件

* 替换


* 计数

  

* 遍历
  * for_each(uni.begin(), uni.end(), [](int x) {cout << x << endl; });  

  * transform(str.begin(), str.end(), str.begin(), ::toupper);
    > // 遍历每一个元素，进行处理其中的数据


  