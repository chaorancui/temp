[toc]

# C++ 知识点总结

### C++函数传参
1. 非指针变量、class、struct：
   * 函数内修改值，不影响外部：传值(int)、传const引用(const int &)
   * 函数内修改值，影响外部：传指针(int *)、传非const引用(int &)
2. 指针变量：
   * 函数内修改指针指向，不影响外部：传指针(int *，对指针类型来说，就是传值)、传指向指针的const引用(const int *&)
   * 函数内修改指针指向，影响外部：传指针的指针(int **)、传向指针的非const引用(int *&)
3. 一维数组：
   * 函数内修改值，不影响外部：传指向数组的const引用(const int (&arr)[2])
   * 函数内修改值，影响外部：传指向数组的指针(int */int arr[2])、传指向数组的引用(int (&arr)[2])

### C++ 类定义中class+宏+类名的意义
https://vzhougm.gitee.io/2021/06/25/c&c++/C++%20%E7%B1%BB%E5%AE%9A%E4%B9%89%E4%B8%ADclass+%E5%AE%8F+%E7%B1%BB%E5%90%8D%E7%9A%84%E6%84%8F%E4%B9%89/

### 返回函数指针的函数
https://www.cnblogs.com/lifexy/p/14098103.html

### C++17 新特性之 std::optional（上）
https://zhuanlan.zhihu.com/p/64985296

## 《重构 改善既有代码的设计第二版》中文版
https://github.com/MwumLi/book-refactoring2


## c++ enum class compare
https://juejin.cn/s/c%2B%2B%20enum%20class%20compare

## 不能delete void指针
释放指针void*那里有问题，正确的做法应该做一个强制转换

## 类成员函数放在类声明中实现，则此函数默认是内联函数

## 空struct指针的用途C++
在C++中，空的结构体指针可以用于以下情况：

占位符
在一些代码中，我们可能需要一个占位符来表示某个变量或参数的位置，但是这个变量或参数当前并没有被定义或赋值。这时候，我们可以使用一个空的结构体指针来代替该变量或参数的位置，以便于后续代码的编写。

例如，下面的代码中，我们定义了一个空的结构体Dummy，并将其用作一个函数的参数占位符：

c++
Copy code
struct Dummy {};
void myFunction(Dummy* param1, int param2) {
  // ...
}

int main() {
  myFunction(nullptr, 42);
  return 0;
}
作为泛型指针
在C++中，有时候我们需要定义一个通用的指针类型，以便于在不同的上下文中使用。这时候，我们可以使用空的结构体指针来定义这个通用的指针类型。

例如，下面的代码中，我们定义了一个名为GenericPointer的类型，该类型是一个空的结构体指针：

c++
Copy code
struct GenericPointer {};
using MyPointer = GenericPointer*;
在这个例子中，我们使用了GenericPointer来定义了一个别名MyPointer，这个别名可以在不同的上下文中使用，以表示一个通用的指针类型。

作为哨兵值
有时候，我们需要定义一个特殊的值来表示某种状态或条件。在这种情况下，我们可以使用空的结构体指针来作为哨兵值。

例如，下面的代码中，我们定义了一个名为EndOfList的哨兵值，用于表示一个链表的末尾：

c++
Copy code
struct EndOfList {};
struct ListNode {
  int value;
  ListNode* next;
};

int main() {
  ListNode* head = new ListNode{1, new ListNode{2, new ListNode{3, new EndOfList}}};
  // ...
  return 0;
}
在这个例子中，我们使用了一个空的结构体指针EndOfList来表示链表的末尾。由于EndOfList是一个空的结构体指针，它不会占用任何内存空间，因此可以作为一个轻量级的哨兵值来使用。


## 为什么使用空类
空类在“泛型编程”中，空类（空结构）的用处非常广：
我们利用类型（通常是空类），来区别对待不同类对象的属性。
通过使用函数重载的方法，在参数中加入一个空类来作为区分不同的函数的方法，编译的时候直接选择，而不是在运行的时候选择，是非常提高效率的。
https://www.cnblogs.com/Allen-rg/p/7307116.html


## C++11
https://www.apiref.com/cpp-zh/cpp/11.html
值初始化
https://www.apiref.com/cpp-zh/cpp/language/value_initialization.html
C++11特性之default/delete
　在未显式的定义类的特殊成员函数时，如果被调用，系统会自动隐式的创建该特殊成员函数，且隐式的创建方式比显式的创建方式执行效率高。
　只需在函数声明后加上=default;，就可将该函数声明为 defaulted 函数，编译器将为显式声明的 defaulted 函数自动生成函数体，以获得更高的执行效率。
　有些时候，我们需要禁用某些函数(=delete不仅可以禁用类内的特殊成员函数，也可以禁用一般函数)，此时就需要在该函数后面增加=delete；，则该函数将变的不可调用，比如不可复制等。


## extern声明变量或函数
https://blog.csdn.net/weixin_38145317/article/details/86496041






## 条件同时满足的写法

```C++
// a, b, c 同时为1时返回true；否则返回false
// 写法1
if (a && b && c) {
	return true;
}

// 写法2
if (!a) {
	return false;
}
if (!b) {
	return false;
}
if (!c) {
	return false;
}
return true;
```

这种好处是针对很长的条件判断，易读性较好。



## 回调函数(callback)

**一般来说**，只要参数是一个函数，那么这个函数就是回调。

很多初学者不明白 callback 的用法，因为 callback 有一点「反直觉」。

比如说我们用代码做一件事情，分为两步：step1( ) 和 step2( )。

符合人类直觉的代码是：

```
step1()
step2()
```

callback 的写法却是这样的：

```
step1(step2)
```

为什么要这样写？或者说在什么情况下应该用这个「反直觉」的写法？

一般（注意我说了一般），在 step1() 是一个异步任务的时候，就会使用 callback。



## 位域的使用

有些信息在存储时，并不需要占用一个完整的字节，而只需占几个或一个二进制位。例如在存放一个开关量时，只有 0 和 1 两种状态，用 1 位二进位即可。为了节省存储空间，并使处理简便，C 语言又提供了一种数据结构，称为"位域"或"位段"。

所谓"位域"是把一个字节中的二进位划分为几个不同的区域，并说明每个区域的位数。每个域有一个域名，允许在程序中按域名进行操作。这样就可以把几个不同的对象用一个字节的二进制位域来表示。

**典型的实例：**

- 用 1 位二进位存放一个开关量时，只有 0 和 1 两种状态。
- 读取外部文件格式——可以读取非标准的文件格式。例如：9 位的整数。



**位域定义：** 

位域定义与结构定义相仿，可采用先定义后说明，同时定义说明或者直接说明这三种方式。其形式为：

```
struct 位域结构名 
{
 位域列表
};

其中位域列表的形式为：
type [member_name] : width ;

struct packed_struct {
    unsigned int f1:1;
    unsigned int f2:1;
    unsigned int f3:1;
    unsigned int f4:1;
    unsigned int type:4;
    unsigned int my_int:9;
};
可以替换为：
struct packed_struct {
    unsigned int f1:1,
                 f2:1,
                 f3:1,
                 f4:1,
                 type:4;
    unsigned int my_int:9;
};
```



**对于位域的定义尚有以下几点说明：**

- 一个位域存储在同一个字节中，如一个字节所剩空间不够存放另一位域时，则会从下一单元起存放该位域。也可以有意使某位域从下一单元开始。例如：

  ```C++
  struct bs{
      unsigned a:4;
      unsigned  :4;    /* 空域 */
      unsigned b:4;    /* 从下一单元开始存放 */
      unsigned c:4;
  }; // 在这个位域定义中，a 占第一字节的 4 位，后 4 位填 0 表示不使用，b 从第二字节开始，占用 4 位，c 占用 4 位。
  ```

- 位域的宽度不能超过**它所依附的**数据类型的长度，成员变量都是有类型的，这个类型限制了成员变量的最大长度，**:** 后面的数字不能超过这个长度。

- 位域可以是无名位域，这时它只用来作填充或调整位置。无名的位域是不能使用的。例如：

  ```C++
  struct k{
      int a:1;
      int  :2;    /* 该 2 位不能使用 */
      int b:3;
      int c:2;
  };
  ```

从以上分析可以看出，位域在本质上就是一种结构类型，不过其成员是按二进位分配的。



**位域的使用：**

位域的使用和结构成员的使用相同，其一般形式为：

```
位域变量名.位域名
位域变量名指针->位域名
```

位域允许用各种格式输出。

```C++
int main(){
    struct bs{
        unsigned a:1;
        unsigned b:3;
        unsigned c:4;
    } bit,*pbit;
    bit.a=1;    /* 给位域赋值（应注意赋值不能超过该位域的允许范围） */
    bit.b=7;    /* 给位域赋值（应注意赋值不能超过该位域的允许范围） */
    bit.c=15;    /* 给位域赋值（应注意赋值不能超过该位域的允许范围） */
    printf("%d,%d,%d\n",bit.a,bit.b,bit.c);    /* 以整型量格式输出三个域的内容 */
    pbit=&bit;    /* 把位域变量 bit 的地址送给指针变量 pbit */
    pbit->a=0;    /* 用指针方式给位域 a 重新赋值，赋为 0 */
    pbit->b&=3;    /* 使用了复合的位运算符 "&="，相当于：pbit->b=pbit->b&3，位域 b 中原有值为 7，与 3 作按位与运算的结果为 3（111&011=011，十进制值为 3） */
    pbit->c|=1;    /* 使用了复合位运算符"|="，相当于：pbit->c=pbit->c|1，其结果为 15 */
    printf("%d,%d,%d\n",pbit->a,pbit->b,pbit->c);    /* 用指针方式输出了这三个域的值 */
}
```

位域结构体中的变量不能取地址。

有符号数在机器中是以**补码**的形式存在的，其正负的判断有其规则。位域是以**原码**的形式来进行操作的，这中间有差异。而关于位域的正负数判断，也不是简单的首bit的0或1来决定，否则上面的结果就应该是-1 -2 -3或者1 2 3了。位域的实现，是编译器相关的。**建议是，使用位域不要使用正负这样的特性**——理论上来说，应该只关注定义的那几个bit的0或者1，是无符号的。可以使用无符号类型来定义位域，这样不会产生正负号这样的问题。



**存储说明：** 

类可以将其（非静态）数据成员定义为位域（bit-field），在一个位域中含有一定数量的二进制位。当一个程序需要向其他程序或硬件设备传递二进制数据时，通常会用到位域。

位域在内存中的布局是与机器有关的

位域的类型必须是整型或枚举类型，带符号类型中的位域的行为将因具体实现而定

取地址运算符（&）不能作用于位域，任何指针都无法指向类的位域



无论小端还是大端，先定义的位域占据低bit地址。

我们常用的x86结构是小端模式，而KEIL C51则为大端模式。 很多的ARM，DSP都为小端模式。 有些ARM处理器还可以由硬件来选择是大端模式还是小端模式。



**非const引用不应绑定到位域字段，**

由于指针不能指向位字段,因此非const引用不能绑定到位字段.

非常量引用不能绑定(bind)到位域，原因与指针不能指向位域的原因相同。

虽然没有指定引用是否占用存储空间，但很明显，在非平凡的情况下，它们被实现为伪装的指针，并且引用的这种实现是语言作者“有意”的。就像指针一样，引用必须指向一个可寻址的存储单元。不可能将非常量引用绑定(bind)到不可寻址的存储单元。由于非常量引用需要直接绑定(bind)，因此非常量引用不能绑定(bind)到位域。

产生可以指向位域的指针/引用的唯一方法是实现某种“ super 指针”，除了存储中的实际地址外，还包含某种位偏移量和位宽信息，以便告诉编写代码要修改哪些位。请注意，此附加信息必须存在于所有数据指针类型中，因为 C++ 中没有“位域指针/引用”这样的类型。这基本上等同于实现更高级别的存储寻址模型，与底层操作系统/硬件平台提供的寻址模型完全分离。出于纯粹的效率考虑，C++ 语言从未打算要求对底层平台进行这种抽象。

一种可行的方法是引入一个单独的指针/引用类别，例如“位域的指针/引用”，它具有比普通数据指针/引用更复杂的内部结构。这样的类型可以从普通的数据指针/引用类型转换，但反过来不行。但这似乎并不值得。

在实际情况下，当我必须处理打包成位和位序列的数据时，我通常更喜欢手动实现位域并避免语言级别的位域。位域的名称是一个编译时实体，不可能进行任何类型的运行时选择。当需要运行时选择时，更好的方法是声明一个普通的 `uint32_t`数据字段并手动管理其中的单个位和位组。这种手动“位域”的运行时选择很容易通过掩码和移位(两者都可以是运行时值)实现。基本上，这接近于上述“ super 指针”的手动实现。



> 参考资料
>
> C 位域：https://www.runoob.com/cprogramming/c-bit-fields.html
>
> 



## protected访问权限

> Java 包(package)
>
> 为了更好地组织类，Java 提供了包机制，用于区别类名的命名空间。
>
> 包的作用
>
> - 1、把功能相似或相关的类或接口组织在同一个包中，方便类的查找和使用。
> - 2、如同文件夹一样，包也采用了树形目录的存储方式。同一个包中的类名字是不同的，不同的包中的类的名字是可以相同的，当同时调用两个不同包中相同类名的类时，应该加上包名加以区别。因此，包可以避免名字冲突。
> - 3、包也限定了访问权限，拥有包访问权限的类才能访问某个包中的类。
>
> Java 使用包（package）这种机制是为了防止命名冲突，访问控制，提供搜索和定位类（class）、接口、枚举（enumerations）和注释（annotation）等。



当父类与子类位于同一包中时，不管是子类对象还是父类对象都可以访问protected，但是它们的意义是不一样的；对于子类对象，之所以可以访问是因为：子类从父类继承了protected成员，理所当然可以访问；父类对象（在子类中创建的）之所以可以访问是因为protected提供了包访问极限！


  当父类与子类位于不同包中时，protected成员就只能通过子类对象来访问（因为protected对于子类是可见的），而父类对象不再可以访问！不过，可以访问static 成员（因为protected的包访问极限已失去作用）



## inline函数

内联函数：告知编译器在进行有内联标识的函数调用时将函数体部分在调用处展开。这样做可以消除函数传参（堆栈调用）的负担，提高了函数的调用效率。

而且inlining的函数并不存在，因为已经被展开了。


如果需要定义一个内联函数，需要在函数体定义的地方使用inline关键字标识，写在函数声明处是没有意义的。原因是一个函数要inline，编译器必须见过它的实现，否则编译器无米之炊无法inline。

```C++
int func(int);  //函数声明
 
inline int func(int a)  //函数定义
{ 
    return ++a;
}
```

1. 在C++类的实现过程中，如果想要将成员函数设置成inline内联函数的话，需要在类的头文件.h中定义这个函数，不能在相应的.cpp文件中定义。
2. 在类内部定义的成员函数默认设置成内联函数。
3. inline内联关键字只是给编译器一个建议，有些函数即使有inline标识，也不会被设置成内联函数。
4. 有些函数即使没有inline标识，编译器在优化时也有可能将这个函数作为内联函数来处理。

## 整数的位操作：按位与&、或|、异或^、取反~

**机器数：**一个数在计算机中的二进制表示形式, 叫做这个数的机器数。**机器数是带符号的**，在计算机用一个数的最高位存放符号, 正数为0, 负数为1。比如，十进制中的数 +3 ，计算机字长为8位，转换成二进制就是00000011。如果是 -3 ，就是 10000011 。这里的 00000011 和 10000011 就是机器数。

**真值：**因为第一位是符号位，所以机器数的形式值就不等于真正的数值。例如上面的有符号数 10000011，其最高位1代表负，其真正数值是 -3 而不是形式值131（10000011转换成十进制等于131）。所以，为区别起见，将**带符号位的机器数对应的真正数值称为机器数的真值**。例：0000 0001的真值 = +000 0001 = +1，1000 0001的真值 = –000 0001 = –1

正数：原码 = 反码 = 补码

负数：原码、反码为原码除符号为按位取反、补码为反码加1

整数在计算机中是**以补码的方式存储**。

这些操作都是按**补码**来操作的，输出为8进制或16进制时也是输出的补码，输出为10进制时才转换为机器数真值。

```C++
// -88&100 负数参与按位且，分析步骤
     1111 1111 1010 1000 // -88补码
    &0000 0000 0110 0100 // 100补码
     -------------------
     0000 0000 0010 0000 // 转成十进制结果为：32， 即-88&100 = 32
```

## 结构体初始化的四种方法

### 定义
```c++
struct InitMember
{
    int first；
    double second；
    char* third；
    float four;
};
```


### 方法一：定义时赋值
```c++
struct InitMember test = {-10,3.141590，"method one"，0.25}；
```

需要注意对应的顺序，不能错位。

### 方法二：定义后逐个赋值

```c++
struct InitMember test；

test.first = -10;
test.second = 3.141590;
test.third = "method two";
test.four = 0.25;

```

因为是逐个确定的赋值，无所谓顺序啦。

### 方法三：定义时乱序赋值（C风格）

这种方法类似于第一种方法和第二种方法的结合体，既能初始化时赋值，也可以不考虑顺序；

```c++
struct InitMember test = {
    .second = 3.141590,
    .third = "method three",
    .first = -10,
    .four = 0.25
};
```

这种方法在Linux内核（kernel）中经常使用，在音视频编解码库FFmpeg中也大量频繁使用，还是很不错的一种方式。

### 方法四：定义时乱序赋值（C++风格）

这种方法和前一种类似，网上称之为C++风格，类似于key-value键值对的方式，同样不考虑顺序。

```c++
struct InitMember test = {
    second：3.141590,
    third："method three",
    first：-10,
    four：0.25
};
```

## __builtin_expect 说明

### 引言

> 这个指令是 gcc 引入的，作用是**允许程序员将最有可能执行的分支告诉编译器**。这个指令的写法为：`__builtin_expect(EXP, N)`。
> 意思是：EXP==N 的概率很大。

一般的使用方法是将`__builtin_expect`指令封装为`likely`和`unlikely`宏。这两个宏的写法如下.

```c++
#define likely(x) __builtin_expect(!!(x), 1) //x很可能为真       
#define unlikely(x) __builtin_expect(!!(x), 0) //x很可能为假
```

`!!(x)` 的作用是把(x)转变成"布尔值"：无论(x)的值是多少，`!(x)` 得到的是 `true` 或 `false`, `!!(x)` 就得到了原值的"布尔值"。

### 内核中的 likely() 与 unlikely()

首先要明确：

```c++
if(likely(value))  //等价于 if(value)
if(unlikely(value))  //也等价于 if(value)
```

`__builtin_expect()` 是 GCC (version >= 2.96）提供给程序员使用的，目的是将“分支转移”的信息提供给编译器，这样编译器可以对代码进行优化，以减少指令跳转带来的性能下降。
 `__builtin_expect((x),1)` 表示 x 的值为真的可能性更大；
 `__builtin_expect((x),0)` 表示 x 的值为假的可能性更大。
 也就是说，使用`likely()`，执行 if 后面的语句的机会更大，使用 `unlikely()`，执行 else 后面的语句的机会更大。通过这种方式，编译器在编译过程中，会将可能性更大的代码紧跟着起面的代码，从而减少指令跳转带来的性能上的下降。

### 例子

```c++
int x, y;
 if(unlikely(x > 0))
    y = 1; 
else 
    y = -1;
```

上面的代码中 gcc 编译的指令会预先读取 y = -1 这条指令，这适合 x 的值大于 0 的概率比较小的情况。如果 x 的值在大部分情况下是大于 0 的，就应该用 likely(x > 0)，这样编译出的指令是预先读取 y = 1 这条指令了。这样系统在运行时就会减少重新取指了。

## C/C++中 `#` 和 `##` 的用法

C/C++ 宏定义中的 # 的用法分为两种：`#` 和 `##`

==**`#` 表示将宏定义中的参数变成字符串**==

==**`##` 表示将宏定义中的参数变成字符串连在一起**==

```c++
#include <iostream>

#define STR(a)       #a
#define FUNC(a, b)   a##b
 
int main()
{
    using namespace std;
 
    int a = 1, b = 2;
    string ab("Hello");
 
    cout << STR(a) << endl;
    cout << FUNC(a, b) << endl;
 
    return 0;
} 
```

> 输出：
>
> a
> Hello
>
> 解释：
>
> \#a：将 a 转为了字符串，所以输出的不是 1，而是 a
>
> a##b：将输入的参数 a、b 连接为字符串 ab，而变量 ab 为字符串类型，值为 Hello，所以输出的是 Hello

==**需要注意的是有 # 或者 ## 的地方，不会将参数展开了**==，例如：

```c++
#include <iostream>
 
#define PI           3.14
#define STR(a)       #a
#define F(t,f)       t##f
 
int main()
{
    using namespace std;
 
    int P = 5, I = 6;
    cout << STR(PI) << endl;
    cout << F(5, 6) << endl;
    cout << F(P, I) << endl;
 
    return 0;
}
```

> 输出：
>
> PI
> 56
> 3.14
>
> 解释：
>
> 没有将 PI 解释，直接将 PI 转为字符串了
>
> 56 输出正常与下面的输出对比，P 和 I 没有转义，而是直接输出 PI，因为 PI 为 3.14，所以输出的是 3.14

**解决方法：加一层中间转换层**

```c++
#include <iostream>
 
#define PI           3.14
 
#define _STR(a)      #a
#define STR(a)       _STR(a)
 
#define _F(t,f)       t##f
#define F(t,f)       _F(t,f)
 
int main()
{
    using namespace std;
 
    int P = 5, I = 6;
    cout << STR(PI) << endl;
    cout << F(5, 6) << endl;
    cout << F(P, I) << endl;
 
    return 0;
}
```

> 输出：
>
> 3.14
> 56
> 3.14

[C/C++语言中的#和##的作用](https://blog.csdn.net/michaelhit/article/details/82853634?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_title~default-0-82853634-blog-44133701.pc_relevant_multi_platform_whitelistv2&spm=1001.2101.3001.4242.1&utm_relevant_index=1)

[c语言中的#号和##号的作用](https://blog.csdn.net/zxx2096/article/details/81206935?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2-81206935-blog-82853634.pc_relevant_multi_platform_whitelistv2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2-81206935-blog-82853634.pc_relevant_multi_platform_whitelistv2&utm_relevant_index=3)

## struct 和 union 内存对齐

计算规则

首先需要介绍**有效对齐值**：每个平台上的编译器都有默认对齐系数 n,可以通过 `#pragma pack(n)` 来指定。有效对齐值就等与该对齐系数和结构体中最长的数据类型的长度两者最小的那一个值，即 `min(有效对齐值, 结构体中最长的数据类型的长度)` 比如对齐系数是8,而结构体中最长的是int,4个字节,那么有效对齐值为4。



内存对齐：

　　在 32 位系统下，gcc 的对齐方式为 1,2,4，默认为 4 字节对齐。 
　　在 64 为系统下，gcc 的对齐方式为 1,2,4,8，默认为 8 字节对齐



\#pragma pack （）是用来控制[字节对齐](https://so.csdn.net/so/search?q=字节对齐&spm=1001.2101.3001.7020)的，一般头文件中没有的话是默认值，即以结构体中的最大元素所占字节对齐；

若存在多个#pragma pack (n),遵从向上对齐原则，即某个结构体定义上方最近的一个#pragma pack（）



## C++函数参数为指针

1. 函数入参为 `**`， 通过这种调用可以修改指针对象值。

```c++
void my_malloc(void** p, int size)  
{  
    *p = malloc(sizeof(int)*size);
}
int main（）
{
    int *a;
    my_malloc(&a ， 10);
    return 1;
}
```

2. 函数参数中 `*&` 和 `**&` 符合分别代表什么呢？例如：

```C++
int *&p;
int **&p;
// 其实这两个*& 和 **&是表示引用，*&表示指针的引用，**&表示指针的指针的引用。
```

举例：修改调用函数中的x和y，会直接影响到主函数中的a和b的值。因为他们是引用关系。

```c++
void foo(int*& x, int**& y) {
    // modifying x or y here will modify a or b in main
}

int main() {
    int val = 42;
    int *a  = &val;
    int **b = &a;

	foo(a, b);
	return 0;
}
```
3. 指针传值和指针传引用的区别：

```c++
/* 再说一点和标题不想关的，还是上篇文章提到的问题，这里再给个实例： */
void pass_by_value(int* p)
{
    //Allocate memory for int and store the address in p
    p = new int;
}

void pass_by_reference(int*& p)
{
    p = new int;
}

int main()
{
    int* p1 = NULL;
    int* p2 = NULL;

pass_by_value(p1); //p1 will still be NULL after this call
pass_by_reference(p2); //p2 's value is changed to point to the newly allocate memory
 
return 0;
```



## typedef 使用

在编程中使用typedef目的一般有两个，一个是给变量一个易记且意义明确的新名字，另一个是简化一些比较复杂的类型声明。

### 用途1

定义一种类型的别名，==而不只是简单的宏替换==。可以用作同时声明指针型的多个对象。

```C++
typedef char* PCHAR; // 一般用大写
PCHAR pa, pb; // 可行，同时声明了两个指向字符变量的指针
char *pa, *pb; // 也可行，但相对来说没有用typedef的形式直观，尤其在需要大量指针的地方，typedef的方式更省事。

typedef char TA[5];//定义数组类型
typedef char *TB[5];//定义指针数组类型,PA定义的变量为含5个char*指针元素的数组(指针数组类型)
typedef char *(TC[5]);//指针数组类型，因为[]的结合优先级最高，所以加不加()没啥区别，TC等价于TB
typedef char (*TD)[5];//数组指针类型
```

### 用途2

用在旧的C的代码中（具体多旧没有查），声明struct新对象时，必须要带上struct，即形式为： `struct 结构名 对象名`，使用 typedef 可以少写一个 struct。如：

```C++
struct tagPOINT1  
{  
    int x;  
    int y;  
};  
struct tagPOINT1 p1; 

typedef struct tagPOINT  
{  
    int x;  
    int y;  
}POINT;  
POINT p1; // 这样就比原来的方式少写了一个struct，比较省事，尤其在大量使用的时候 
```

而在C++中，在C++中，typedef的这种用途二不是很大，因为 C++ 中可以直接写：`结构名 对象名`，即：

```c++
tagPOINT1 p1;
```

### 用途3

用typedef来定义与平台无关的类型。当跨平台时，只要改下 typedef 本身就行，不用对其他源码做任何修改。标准库就广泛使用了这个技巧，比如size_t。

```c++
// 比如定义一个叫 REAL 的浮点类型，在目标平台一上，让它表示最高精度的类型为：
typedef long double REAL;

// 在不支持 long double 的平台二上，改为：
typedef double REAL;

// 在连 double 都不支持的平台三上，改为：
typedef float REAL;
```

### 用途4

为复杂的声明定义一个新的简单的别名。方法是：在原来的声明里逐步用别名替换一部分复杂声明，如此循环，把带变量名的部分留到最后替换，得到的就是原声明的最简化版。举例：

1. 复杂声明1：

```c++
void (*b[10]) (void (*)()); // 数组，数组内存放函数指针
// 首先*b[10]为指针数组，它里面的十个元素全是指针。到底是什么指针呢，是一个返回类型为空，形参为空的函数指针。

// 用typedef进行简化： 
typedef void (pFunParam *)(); // 1：首先声明后面的函数指针
typedef void (*pFunx)(pFunParam); // 2：接着声明前面的指针数组

// 原声明的最简化版：
typedef void (*pFun[10]) (void (*)());
pFun b[10];
```

2. 复杂声明2：

```c++
double(*(*pa)[9])(); // 指针，指向数组，数组内存放函数指针
// pa是一个指向9维数组的指针，数组内为函数指针，该函数指针形参为空，返回类型为double。

// 用typedef进行简化： 
typedef double(*pFunParam)(); //1：首先声明一个函数指针 
typedef pFunParam (*pFun)[9]; //2：接着声明一个新类型 

// 原声明的最简化版：
typedef double(*(*pa)[9])();
pa x;
```

网络博客typedef用法中提到一个复杂的声明：

```C++
doube()() (e)[9]; // 这个声明在gcc下编译时不通过的。按照作者的本意，应该这样声明：double(*(*pa)[9])();
```

例子：

```c++
typedef double (*pFun)();//定义函数指针pFun
typedef double (*(*e)[2])();

double Fun1()
{
	cout<<"Fun1"<<endl;
	return 1;
};

double Fun2()
{
	cout<<"Fun2"<<endl;
	return 2;
};

int main()
{	
	pFun array[2]= {Fun1, Fun2};
	array[0]();//执行Fun1
	array[1]();//执行Fun2

	e MyE = &array;//将array的首地址赋给MyE
	cout<<sizeof(MyE)<<endl;//既然是指针，长度自然为4（32位机上）
	cout<<sizeof(*MyE)<<endl;//（两个指针）长度为8（32位机上）
	
	(*MyE[0])();//执行Fun1，注意优先级，其实就是 (*(MyE[0]))();

	(*MyE)[0]();//执行Fun1
	(*MyE)[1]();//执行Fun2

	return 0;
}
```



> ==理解复杂声明可用的“右左法则”==：
>
> 从变量名看起，先往右，再往左，碰到一个圆括号就调转阅读的方向；括号内分析完就跳出括号，还是按先右后左的顺序，如此循环，直到整个声明分析完。举例：
>
> ```c++
> int (*func)(int *p);
> ```
>
> 首先找到变量名func，外面有一对圆括号，而且左边是一个*号，这说明func是一个指针；然后跳出这个圆括号，先看右边，又遇到圆括号，这说明 (*func)是一个函数，所以func是一个指向这类函数的指针，即函数指针，这类函数具有int*类型的形参，返回值类型是int。
>
> ```c++
> int (*func[5])(int *);
> ```
>
> func 右边是一个[]运算符，说明func是具有5个元素的数组；func的左边有一个*，说明func的元素是指针（注意这里的*不是修饰func，而是修饰 func[5]的，原因是[]运算符优先级比*高，func先跟[]结合）。跳出这个括号，看右边，又遇到圆括号，说明func数组的元素是函数类型的指 针，它指向的函数具有int*类型的形参，返回值类型为int。
>
> 也可以记住2个模式：
>
> ```c++
> type (*)(....)函数指针 
> type (*)[]数组指针
> ```





# Vscode

### 查看反汇编代码

运行程序后，在监视变量中添加：

```bash
-exec disassemble /m main
# 或
-exec disassemble /m
```

然后在**<font color=red>调试控制台</font>**就可以看到汇编代码了。





# 模板编程

## 代码案例

app/l3/ceusm/include/common/ccb/ceusml_tblmng.h:46

index 类

## 用户数收编

CEUSML_PrepareRrmData：app/l3/ceusm/src/ue_procedure/ue_data_allocator/ceusml_ue_ccb_manager.cpp

app/l3/ceusm/include/ue_procedure/comm/counter/ceusml_counter_mng.h



## 结构体写法

  NrduCeusmReducedMimoCfg reducedMimoCfg = {

​    .reducedUeMimoLayersFr1Dl = UINT8_MAX,

​    .reducedUeMimoLayersFr1Ul = UINT8_MAX,

  };



## 多重继承，多态怎么回事

class CeusmlL1PoolResPucchMng : public Wsf::EzTimerHandler, public CeusmlL1PoolResMngBase {

app/l3/ceusm/include/l1_cap_mng/l1_res_pool_spec_mng/ceusml_l1_pool_res_pucch_mng.h



## 表链接函数、注册函数

该组函数有未使用参数的原因有3：
1. 函数回调，由于函数指针类型的限制，导致有些回调函数的入参可能不会被用到
2. 表驱动函数调用，原因同上
3. 成员函数的删除（func（）=delete）的情况下，工具误报

允许表链接函数、注册函数这两类为了拉齐统一接口存在函数接口未使用场景，无业务影响，建议屏蔽。

```c++
static bool CEUSML_IsNeedReAllocAckResForPreemptFeature(const CeusmlGlobalUeInfoData &globalUeInfo,

  const CeusmlCellData &cellData, const CeusmlAckResReqPara &ackResReqPara,

  const CeusmlPucchAckCellRes &cellPucchAckRes)

constexpr CeusmlAckInheritRule g_ceusmlAckInheritRule[CEUSML_ACK_RES_RECONFIG_CAUSE_BUTT] = {
    { CEUSML_ACK_RES_RECONFIG_CAUSE_NEW_RES, CEUSML_IsNeedAllocUePucchAckRes },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_LNR_OLD_RB, CEUSML_IsNeedReAllocAckResForAgingPrbIndex },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_RB_REDUCED, CEUSML_IsNeedReAllocAckResForRbReduced },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_NARROW_BWP2, CEUSML_IsNeedReAllocAckResForNarrowBwp2 },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_CA_OR_DL_BIG_PACKET, CEUSML_IsNeedReAllocAckResForPreemptFeature },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_PRIOR_SHORT_DELAY, CEUSML_IsNeedReAllocAckResForShortDelayUser },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_SU, CEUSML_IsNeedReAllocPucchAckResForSu },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_FDD, CEUSML_IsNeedReAllocAckForFdd },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_HYPER_SSB, CEUSML_IsNeedReAllocAckForHyperSsbUe },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_SRS_SWITCH, CEUSML_IsNeedReAllocAckForSrsSwitchUser },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_FORMAT2_RB_CHANGE, CEUSML_IsNeedReAllocAckForFormat2RbChange },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_MIDDLE_POINT_USER, CEUSML_IsNeedReAllocAckForMiddlePointUser },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_FREQ_RES_ADAPTIVE, CEUSML_IsNeedReAllocAckResForFreqResAdaptive },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_SR_SYMBOL_CHANGE, CEUSML_IsNeedReAllocAckResForSrSymbolChange },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_PREEMPT_ENHANCE, CEUSML_IsNeedReAllocAckResForPucchPreemptEnhance },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_SCS_CA_SU_SWITCH, CEUSML_IsNeedReAllocAckForScsCaSuChange },
    { CEUSML_ACK_RES_RECONFIG_CAUSE_REDCAP_BWP_CHANGE, CEUSML_IsNeedReAllocAckForRedCapBwpChange }
};
  
```


