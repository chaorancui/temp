[toc]

# C++ 知识点总结

> [C 语言的各种标准](https://shaoguangleo.github.io/2013/05/06/c-standard/)

> [_C++ FAQ LITE_ — Frequently Asked Questions](https://www.sunistudio.com/cppfaq/index.html)

## 类的拷贝控制

1. 拷贝构造:

   第一个参数必须是自身类型的引用（ch13.1.1，否则为调用拷贝构造，必须拷贝实参，为拷贝实参，又要调用拷贝构造，无限循环），通常加 const。拷贝构造函数通常不应该是 explicit 的（ch13.1.1），考虑加 explicit。

2. 拷贝赋值运算符：

   本质为 operator=的重载函数，入参通常是 const 引用，为了与内置类型赋值运算符（=）一致，返回值通常是指向其左侧运算符对象的引用。

   赋值运算符通常**组合**了**析构函数**和**构造函数**的操作（ch13.2.1）。必须正确处理自赋值。

3. 三/五法则（ch13.1.4)：

   一个基本原则：如果这个类需要一个析构函数（指的是需要自定义析构函数，如 delete 动态内存）， 我们几乎可以肯定它也需要一个拷贝构造函数和一个拷贝赋值运算符。

   第二个基本原则：如一个类需要一个拷贝构造函数， 几乎可以肯定它也需要个拷贝赋值运算符。反之亦然。

4. 移动赋值运算符：

   类似拷贝构造函数， 移动构造函数的第一个参数是该类类型的一个引用，且是右值引用。**通常无 const**。

5. 拷贝构造、拷贝赋值：不应该抛出异常???

   > [C++ 构造函数抛出异常注意事项](https://blog.csdn.net/K346K346/article/details/50144947)

   从语法上来说，构造函数可以抛出异常。但从逻辑上和风险控制上，构造函数中尽量不要抛出异常。万不得已，一定要注意防止内存泄露。

6. 移动构造、移动赋值：不应该抛出异常

   搞清楚为什么需要 noexcept 能帮助我们深入理解标准库是如何与我们自定义的类型交互的。我们需要指出一个移动操作不抛出异常，这是因为两个相互关联的事实：**首先，虽然移动操作通常不抛出异常， 但抛出异常也是允许的**；**其次， 标准库容器能对异常发生时其自身的行为提供保陷**。例如，vector 保证， 如果我们调用 push_back 时发生异常，vector 自身不会发生改变。

   现在让我们思考 push—back 内部发生了什么。类似对应的 StrVec 操作（参见 13.5 节， 第 466 页）， 对一个 vector 调用 push_back 可能要求为 vector 重新分配内存空间。当重新分配 vector 的内存时， vector 将元素从旧空间移动到新内存中， 就像我们在 reallocate 中所做的那样（参见 13.5 节， 第 469 页）。
   如我们刚刚看到的那样， 移动一个对象通常会改变它的值。如果重新分配过程使用了移动构造函数， 且在移动了部分而不是全部元素后抛出了一个异常， 就会产生问题。旧空间中的移动源元素已经被改变了， 而新空间中未构造的元素可能尚不存在。在此情况下，vector 将不能满足自身保持不变的要求。
   另一方面， 如果 vector 使用了拷贝构造函数且发生了异常， 它可以很容易地满足要求。在此情况下， 当在新内存中构造元素时， 旧元素保持不变。如果此时发生了异常，vector 可以释放新分配的（但还未成功构造的）内存并返回。vector 原有的元素仍然存在。
   为了避免这种潜在问题， 除非 vector 知道元素类型的移动构造函数不会抛出异常，否则在重新分配内存的过程中， 它就必须使用拷贝构造函数而不是移动构造函数。**如果希望在 vector 重新分配内存这类情况下对我们自定义类型的对象进行移动而不是拷贝，就**
   **必须显式地告诉标准库我们的移动构造函数可以安全使用**。我们通过将移动构造函数（及移动赋值运算符）标记为 noexcept 来做到这一点。

7. 拷贝赋值运算符、移动赋值运算符：必须正确处理自赋值：

   ```C++
   StrVec &StrVec::operator=(StrVec &&rhs) noexcept {
       // 直接检测自赋值
       if (this != &rhs) {
           free(); // 释放已有元素
           elements = rhs.elements; // 从rhs接节资源
           first_free = rhs.first_free;
           cap = rhs.cap;
           // 将rhs置于可析构状态
           rhs.elements = rhs.first_free = rhs.cap = nullptr;
       }
       return *this;
   }
   ```

8. 移动赋值运算符：

   **在移动操作之后， 移后源对象必须保持有效的、可析构的状态，但是用户不能对其值进行任何假设。**

   当我们编写一个移动操作时， 必须确保移后源对象进入一个可析构的状态。我们的 StrVec 的移动操作满足这一要求， 这是通过将移后源对象的指针成员置为 nullptr 来实现的。

   除了将移后源对象置为析构安全的状态之外， 移动操作还必须保证对象仍然是有效的。一般来说， 对象有效就是指可以安全地为其赋予新值或者可以安全地使用而不依赖其当前值。另一方面， 移动操作对移后源对象中留下的值没有任何要求。

9. 合成的移动操作：

   **定义了一个移动构造函数或移动赋值运算符的类必须也定义自己的拷贝操作。否则， 这些成员默认地被定义为删除的。**

   与拷贝操作不同， 编译器根本不会为某些类合成移动操作。特别是， 如果一个类定义了自己的拷贝构造函数、拷贝赋值运算符或者析构函数， 编译器就不会为它合成移动构造函数和移动赋值运算符了。

   只有当一个类没有定义任何自己版本的拷贝控制成员，且类的每个非 static 数据成员都可以移动时， 编译器才会为它合成移动构造函数或移动赋值运算符。

   如果我们显式地要求编译器生成＝ default 的（参见 7.1.4 节， 第 237 页）移动操作， 且编译器不能移动所有成员， 则编译器会将移动操作定义为删除的函数。（有成员不可移动、类无析构函数被定义为删除或不可访问、类成员是 const 的或是引用）

   如果类定义了一个移动构造函数和/或一个移动赋值运算符， 则该类的合成拷贝构造函数和拷贝赋值运算符会被定义为删除的。

10. 右值引用和成员函数

    **区分移动和拷贝的重载函数通常有一个版本接受一个 const T&， 而另一个版本接受一个 T&＆。**

    如果一个成员函数**同时提供拷贝和移动版本**，它**也能从中受益**。这种允许移动的成员函数通常使用与拷贝／移动构造函数和赋值运算符相同的参数模式 ---- 一个版本接受一个指向**const 的左值引用**， 第二个版本接受一个指向**非 const 的右值引用**。

    例如， 定义了 push_back 的标准库容器提供两个版本： 一个版本有一个右值引用参数， 而另一个版本有一个 const 左值引用。假定 x 是元素类型， 那么这些容器就会定义以下两个 push_back 版本：

    ```C++
    void push_back(const X&); // 拷贝： 绑定到任意类型的X
    void push_back(X&&); // 移动： 只能绑定到类型X的可修改的右值
    ```

    我们可以将能转换为类型 x 的任何对象传递给第一个版本的 push_back。此版本从其参数拷贝数据。对于第二个版本， 我们只可以传递给它非 con 江的右值。此版本对千非 const 的右值是精确匹配（也是更好的匹配）的， 因此当我们传递一个可修改的右值（参见 13.6.2 节， 第 477 页）时， 编译器会选择运行这个版本。此版本会从其参数窃取数据。

    一般来说， 我们不需要为函数操作定义接受一个 const X&＆或是一个（普通的）X&参数的版本。**当我们希望从实参＂窃取“ 数据时， 通常传递一个右值引用。为了达到这一目的， 实参不能是 const 的**。类似的， 从一个对象进行拷贝的操作不应该改变该对象。因此， 通常不需要定义一个接受一个（普通的）X＆参数的版本。

    ```C++
    sl + s2 = "wow'";
    ```

    此处我们对两个 string 的连接结果 ---- 一个右值， 进行了赋值。在旧标准中， 我们没有办法阻止这种使用方式。为了**维持向后兼容性， 新标准库类仍然允许向右值赋值**。但是， 我们可能**希望在自己的类中阻止这种用法**。在此情况下， 我们希望强制左侧运算对象（即， this 指向的对象）是一个左值。

    我们指出 this 的左值／右值屈性的方式与定义 const 成员函数相同（参见 7.1.2 节，第 231 页）， 即， 在参数列表后放置一个引用限定符(reference qualifier):

    ```c++
    class Foo {
    public:
        Foo &operator=(const Foo &) &; // 只能向可修改的左值赋值
        // Foo 的其他参数
    };

    Foo &Foo::operator=(const Foo &rhs) &{
        // 执行将rhs 赋子本对象所需的工作
        return *this;
    }
    ```

    **引用限定符可以是&或&&**，分别指出 this 可以指向一个左值或右值。类似 const 限定符，**引用限定符只能用千（非 static)成员函数， 且必须同时出现在函数的声明和定义中**。

    一个函数可以同时用 const 和引用限定。在此情况下，引用限定符必须跟随在 const 限定符之后：

    ```c++
    class Foo {
    public:
        Foo someMem() & const; // 错误： const 限定符必须在前
        Foo anotherMem() const &; // 正确： const 限定符在前
    };
    ```

    就像一个成员函数可以根据是否有 const 来区分其重载版本一样（参见 7.3.2 节， 第 247 页）， 引用限定符也可以区分重载版本。而且， 我们可以综合引用限定符和 const 来区分一个成员函数的重载版本。

    ```C++
    class Foo {
    public:
        Foo sorted() &&; // 可用于可改变的右值
        Foo sorted() const &; // 可用于任何类型的Foo
        Foo sorted() const; // 错误： 必须加上引用限定符
        // Foo的其他成员的定义
    private:
        vector<int> data;
    };

    // 本对象为右值， 因此可以原址排序
    Foo Foo::sorted() &&{
        sort(data.begin(), data.end());
        return *this;
    }

    // 本对象是const 或是一个左值， 哪种情况我们都不能对其进行原址排序
    Foo Foo::sorted() const &{
        Foo ret(*this); // 拷贝一个副本
        sort(ret.data.begin(), ret．data.end()); // 排序副本
        return ret; // 返回副本
    }
    ```

    当我们对一个右值执行 sorted 时， 它可以安全地直接对 data 成员进行排序。对象是一个右值， 意味着没有其他用户， 因此我们可以改变对象。当对一个 const 右值或一个左值执行 sorted 时， 我们不能改变对象， 因此就需要在排序前拷贝 data。
    编译器会根据调用 sorted 的对象的左值／右值属性来确定使用哪个 sorted 版本：

    ```c++
    retVal().sorted(); // retVal()是一个右值， 调用Foo: : sorted() &&
    retFoo().sorted(); // retFoo()是一个左值， 调用Foo: : sorted() const &
    ```

    **如果一个成员函数有引用限定符，则具有相同参数列表的所有版本都必须有引用限定符。**

    如果我们定义两个或两个以上具有相同名字和相同参数列表的成员函数， 就必须对所有函数都加上引用限定符， 或者所有都不加：

11. 举例

    ```C++
    class Foo {
    public:
        Foo(const char *buffer, size_t size) { Init(buffer, size); }

        Foo(const Foo &other) { Init(other.buf, other.size); }

        Foo &operator=(const Foo &other) {
            Foo tmp(other);
            Swap(tmp);
            return *this;
        }

        Foo(Foo &&other) noexcept: buf(std::move(other.buf)), size(std::move(other.size)) {
            other.buf = nullptr;
            other.size = 0;
        }

        Foo &operator=(Foo &&other) noexcept {
            Foo tmp(std::move(other));
            Swap(tmp);
            return *this;
        }

        ~Foo() { delete[] buf; }

        void Swap(Foo &other) noexcept {
            using std::swap;
            swap(buf, other.buf);
            swap(size, other.size);
        }

    private:
        void Init(const char *buffer, size_t size) {
            this->buf = new char[size];
            memcpy(this->buf, buffer, size);
            this->size = size;
        }

        char *buf;
        size_t size;
    };
    ```

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

有符号数在机器中是以**补码**的形式存在的，其正负的判断有其规则。位域是以**原码**的形式来进行操作的，这中间有差异。而关于位域的正负数判断，也不是简单的首 bit 的 0 或 1 来决定，否则上面的结果就应该是-1 -2 -3 或者 1 2 3 了。位域的实现，是编译器相关的。**建议是，使用位域不要使用正负这样的特性**——理论上来说，应该只关注定义的那几个 bit 的 0 或者 1，是无符号的。可以使用无符号类型来定义位域，这样不会产生正负号这样的问题。

**存储说明：**

类可以将其（非静态）数据成员定义为位域（bit-field），在一个位域中含有一定数量的二进制位。当一个程序需要向其他程序或硬件设备传递二进制数据时，通常会用到位域。

位域在内存中的布局是与机器有关的

位域的类型必须是整型或枚举类型，带符号类型中的位域的行为将因具体实现而定

取地址运算符（&）不能作用于位域，任何指针都无法指向类的位域

无论小端还是大端，先定义的位域占据低 bit 地址。

我们常用的 x86 结构是小端模式，而 KEIL C51 则为大端模式。 很多的 ARM，DSP 都为小端模式。 有些 ARM 处理器还可以由硬件来选择是大端模式还是小端模式。

**非 const 引用不应绑定到位域字段，**

由于指针不能指向位字段,因此非 const 引用不能绑定到位字段.

非常量引用不能绑定(bind)到位域，原因与指针不能指向位域的原因相同。

虽然没有指定引用是否占用存储空间，但很明显，在非平凡的情况下，它们被实现为伪装的指针，并且引用的这种实现是语言作者“有意”的。就像指针一样，引用必须指向一个可寻址的存储单元。不可能将非常量引用绑定(bind)到不可寻址的存储单元。由于非常量引用需要直接绑定(bind)，因此非常量引用不能绑定(bind)到位域。

产生可以指向位域的指针/引用的唯一方法是实现某种“ super 指针”，除了存储中的实际地址外，还包含某种位偏移量和位宽信息，以便告诉编写代码要修改哪些位。请注意，此附加信息必须存在于所有数据指针类型中，因为 C++ 中没有“位域指针/引用”这样的类型。这基本上等同于实现更高级别的存储寻址模型，与底层操作系统/硬件平台提供的寻址模型完全分离。出于纯粹的效率考虑，C++ 语言从未打算要求对底层平台进行这种抽象。

一种可行的方法是引入一个单独的指针/引用类别，例如“位域的指针/引用”，它具有比普通数据指针/引用更复杂的内部结构。这样的类型可以从普通的数据指针/引用类型转换，但反过来不行。但这似乎并不值得。

在实际情况下，当我必须处理打包成位和位序列的数据时，我通常更喜欢手动实现位域并避免语言级别的位域。位域的名称是一个编译时实体，不可能进行任何类型的运行时选择。当需要运行时选择时，更好的方法是声明一个普通的 `uint32_t`数据字段并手动管理其中的单个位和位组。这种手动“位域”的运行时选择很容易通过掩码和移位(两者都可以是运行时值)实现。基本上，这接近于上述“ super 指针”的手动实现。

> 参考资料
>
> C 位域：<https://www.runoob.com/cprogramming/c-bit-fields.html>

## protected 访问权限

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

当父类与子类位于同一包中时，不管是子类对象还是父类对象都可以访问 protected，但是它们的意义是不一样的；对于子类对象，之所以可以访问是因为：子类从父类继承了 protected 成员，理所当然可以访问；父类对象（在子类中创建的）之所以可以访问是因为 protected 提供了包访问极限！

当父类与子类位于不同包中时，protected 成员就只能通过子类对象来访问（因为 protected 对于子类是可见的），而父类对象不再可以访问！不过，可以访问 static 成员（因为 protected 的包访问极限已失去作用）

**公有（public）、私有（private）和保护（protected）成员**

- 公有成员：类内和类外都可访问。
- 私有成员：类内可访问，类外不可访问。友元可访问。什么是友元，下面会介绍。
- 保护成员：不涉及继承，和私有成员没什么区别。涉及继承，保护成员在派生类（即子类）中是可访问的。 private 成员只能被本类成员（类内）和友元访问，不能被派生类访问；

> [C++ protected 继承和 private 继承是不是没用的废物？](https://www.zhihu.com/question/425852397/answer/1528656579)

## inline 函数

内联函数：告知编译器在进行有内联标识的函数调用时将函数体部分在调用处展开。这样做可以消除函数传参（堆栈调用）的负担，提高了函数的调用效率。

而且 inlining 的函数并不存在，因为已经被展开了。

如果需要定义一个内联函数，需要在函数体定义的地方使用 inline 关键字标识，写在函数声明处是没有意义的。原因是一个函数要 inline，编译器必须见过它的实现，否则编译器无米之炊无法 inline。

```C++
int func(int);  //函数声明

inline int func(int a)  //函数定义
{
    return ++a;
}
```

1. 在 C++类的实现过程中，如果想要将成员函数设置成 inline 内联函数的话，需要在类的头文件.h 中定义这个函数，不能在相应的.cpp 文件中定义。
2. 在类内部定义的成员函数默认设置成内联函数。
3. inline 内联关键字只是给编译器一个建议，有些函数即使有 inline 标识，也不会被设置成内联函数。
4. 有些函数即使没有 inline 标识，编译器在优化时也有可能将这个函数作为内联函数来处理。

关键字 inline **必须与函数定义体放在一起才能使函数成为内联，仅将 inline 放在函数声明前面不起任何作用**。 所以说，inline 是一种“用于实现的关键字”，而不是一种“用于声明的关键字”。 一般地，用户可以阅读函数的声明，但是看不到函数的定义。

> [[9] 内联函数](https://www.sunistudio.com/cppfaq/inline-functions.html)

## 结构体初始化的四种方法

如果没什么要求，可以直接**定义结构体变量后逐个成员赋值**。

C 语言中结构体初始化方式和 C++ 中不同。对如下结构体：

```C
struct InitMember
{
    int first；
    double second；
    char* third；
    float four;
};
```

### C 语言结构体初始化

#### 方法一：按顺序初始化（聚合初始化）

这种方式按结构体成员的**声明顺序**来进行初始化，必须确保提供的初始化值与结构体成员的顺序匹配，**不能错位**。

```C
struct InitMember test = {-10,3.141590，"method one"，0.25}；
```

#### 方法二：指定成员初始化（**C99 Designated Initializers**）

从 C99 开始，C 语言支持使用指定成员初始化器（Designated Initializers），你可以指定**某些字段的值**而**不必按顺序**提供所有成员的初始化值。这允许你更灵活地初始化结构体，并且可以跳过某些成员的初始化（未初始化的成员将使用默认值）。

```C
struct InitMember test = {
    .second = 3.141590,
    .third = "method three",
    .first = -10,
    .four = 0.25
};
```

这种方法在 Linux 内核（kernel）中经常使用，在音视频编解码库 FFmpeg 中也大量频繁使用，还是很不错的一种方式。

#### 方法三：嵌套结构体初始化

如果结构体包含其他结构体作为成员，可以通过嵌套的方式初始化。

```cpp
struct Inner {
    int inner_member;
};

struct Outer {
    struct Inner inner_struct;
    int outer_member;
};

struct Outer test = { { 10 }, 20 };  // 内层结构体 `inner_struct` 的初始化值为 10，外层成员 `outer_member` 为 20
```

> 此外还可以：
>
> 1. 部分初始化
>    在 C 语言中，如果只对部分成员进行初始化，未初始化的成员将自动被初始化为 0（对于数值类型）或 NULL（对于指针类型）。
>
>    ```C
>    struct InitMember test = { -10, 3.141590 };  // 剩下的成员将被初始化为 0 或 NULL
>    ```
>
> 2. 默认初始化
>    C 没有直接提供默认初始化功能，因此，如果你声明了结构体变量而不显式进行初始化，成员值会是随机的。
>    使用 {0} 初始化所有成员为 0 的一种方式，所有未初始化的成员都默认值为 0（对于数值类型）或 NULL（对于指针类型）。
>
>    ```C
>    struct InitMember test = {0};  // 初始化所有成员为 0 或 NULL
>    ```

### C++ 语言结构体初始化

#### 方法一：按顺序初始化（聚合初始化）---- 同 C 语言

#### 方法二：指定成员初始化（**C++20 Designated Initializers**）---- C++ 20 后才支持

**从 C++20 开始**，C++ 才引入了类 C99 风格的 designated initializers，允许按成员名称初始化结构体成员，而不必按顺序提供所有成员的值。

#### 方法三：构造函数初始化

C++ 中的结构体可以有构造函数，因此可以通过构造函数来初始化成员。即使结构体默认情况下不提供构造函数，你也可以为其定义构造函数。

```c++
struct InitMember {
    int first;
    double second;
    const char* third;
    float four;

    // 定义构造函数
    InitMember(int f, double s, const char* t, float fr)
        : first(f), second(s), third(t), four(fr) {}
};

InitMember test = InitMember(-10, 3.141590, "method three", 0.25);
```

#### 方法四：默认成员初始化（C++11 引入）

从 C++11 开始，C++ 支持在定义结构体时为成员提供默认初始值。这使得你可以在不显式提供所有成员值的情况下初始化结构体。

```cpp
struct InitMember {
    int first = 0;
    double second = 3.14159;
    const char* third = "default";
    float four = 0.25;
};

InitMember test;  // 结构体的成员将使用默认值进行初始化
```

#### 方法五：列表初始化（C++11 引入）

C++11 引入了列表初始化（initializer list），可以直接用花括号初始化结构体成员，无需显式调用构造函数。

```cpp
struct InitMember {
    int first;
    double second;
    const char* third;
    float four;
};

InitMember test{ -10, 3.141590, "method three", 0.25 };
```

这种方式与传统的聚合初始化类似，但列表初始化语法支持更多类型的对象，并且**是 C++11 之后强烈推荐的初始化方式**。

#### 方法六：嵌套结构体初始化

同 C 语言，只不过不再需要加上 struct 关键字。

```cpp
Outer test = { { 10 }, 20 };  // 无需像 C 语言一样，前面再加 struct
```

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

[c 语言中的#号和##号的作用](https://blog.csdn.net/zxx2096/article/details/81206935?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2-81206935-blog-82853634.pc_relevant_multi_platform_whitelistv2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2-81206935-blog-82853634.pc_relevant_multi_platform_whitelistv2&utm_relevant_index=3)

## 条件编译指令

C++ 中的条件编译指令是预处理器指令，用于根据某些条件在编译时有选择地包含或排除代码片段。这些指令允许在不同的平台、配置或编译选项下编译不同的代码。常见的条件编译指令包括 #if、#ifdef、#ifndef、#else、#elif 和 #endif。

### 主要的条件编译指令

```cpp
#if: 如果条件为真,编译后面的代码
#ifdef: 如果宏已定义,编译后面的代码
#ifndef: 如果宏未定义,编译后面的代码
#undef: 取消宏定义，后面也可在重新定义
#elif: else if 的作用
#else: else 的作用
#endif: 结束条件编译块
defined()：预处理器中的一个特殊运算符，用于检查某个宏是否已被定义。
```

> :bulb: 注意：`#ifdef` 与 `#if defined()` 等价，同理，`#ifndef` 与 `#if !defined()` 等价。

```cpp
#ifdef DEBUG
// 等同于
#if defined(DEBUG)

#ifndef DEBUG
// 等同于
#if !defined(DEBUG)
```

使用示例：

```cpp
#define DEBUG

#ifdef DEBUG
    std::cout << "Debug mode is on" << std::endl;
#else
    std::cout << "Debug mode is off" << std::endl;
#endif

#if defined(_WIN32) || defined(_WIN64)
    std::cout << "Running on Windows" << std::endl;
#elif defined(__linux__)
    std::cout << "Running on Linux" << std::endl;
#elif defined(__APPLE__)
    std::cout << "Running on macOS" << std::endl;
#else
    std::cout << "Unknown operating system" << std::endl;
#endif

// 重新定义宏
#define MAX 100
// 使用 MAX
#undef MAX
#define MAX 200
// 此后 MAX 的值变为 200
```

### `#if` 一次判断多个条件

使用逻辑运算符，且逻辑运算符可以和 `defined() 运算符`混合使用。
C++ 预处理器支持以下逻辑运算符：

- && (与)
- || (或)
- ! (非)

```cpp
#if defined(__cplusplus) && __cplusplus >= 201703L && !defined(LEGACY_MODE)
    // 这段代码只在 C++17 或更高版本，且未定义 LEGACY_MODE 时编译
    std::cout << "Using C++17 features" << std::endl;
#endif
```

### 使用注意事项

1. 嵌套使用: 条件编译指令可以嵌套,但要注意配对和缩进,以提高可读性。
2. 避免过度使用: 过多的条件编译可能导致代码难以维护和理解。
3. 注意跨平台兼容性: 使用标准的宏定义来检测平台,如 WIN32, linux, APPLE 等。
4. 保持一致性: 在项目中保持条件编译的一致使用风格。
5. 注释说明: 对于复杂的条件编译,添加注释说明其用途和条件。
6. 测试覆盖: 确保测试涵盖了所有条件编译的分支。
7. 版本控制: 使用版本控制系统时,注意不同分支间条件编译的一致性。
8. 优先使用 #if defined() 而非 #ifdef: 前者更灵活,可以组合多个条件。
9. 使用 #pragma once 或头文件保护: 防止头文件重复包含。
10. 注意宏定义的位置: 确保在使用条件编译指令之前已定义相关宏。

## struct 和 union 内存对齐

> [`union` 与 `struct` 内存分配](https://jiehust.github.io/c/c++/2015/01/21/Struct-and-Union/)
>
> [为什么要内存对齐](https://blog.csdn.net/lgouc/article/details/8235471)

### `#pragma pack（n）`

`#pragma pack(n)` 是一个编译器指令，用于控制结构体、类和联合体的内存对齐方式。这个指令在需要精确控制数据布局的场景中非常有用，比如在与硬件直接交互、网络协议实现或者跨平台数据交换时。

1. 基本语法

   ```cpp
   #pragma pack(push, n)  // 保存当前对齐方式并设置新的对齐值
   // 结构体定义
   #pragma pack(pop)      // 恢复之前的对齐方式
   ```

   或使用

   ```cpp
   #pragma pack(n)  // 保存当前对齐方式并设置新的对齐值
   // 结构体定义
   #pragma pack()      // 恢复之前的对齐方式
   ```

   其中 `n` 是一个表示字节对齐值的整数，通常是 1, 2, 4, 8 或 16。

   若存在多个#pragma pack (n)，遵从向上对齐原则，即某个结构体定义上方最近的一个#pragma pack(n)

2. 作用

   `#pragma pack(n)` 指定了结构体成员的最大对齐字节数。具体来说：

   - 如果成员的大小小于 n，则按照成员自身的大小对齐。
   - 如果成员的大小大于或等于 n，则按照 n 字节对齐。
   - 整个结构体的大小将是 n 的倍数。

   示例： 让我们通过一个例子来说明 `#pragma pack` 的效果：

   ```cpp
   #include <iostream>

   // 默认对齐
   struct DefaultAligned {
       char a;    // 1 byte
       int b;     // 4 bytes
       short c;   // 2 bytes
   };

   // 使用 #pragma pack(1)
   #pragma pack(push, 1)
   struct PackedStruct {
       char a;    // 1 byte
       int b;     // 4 bytes
       short c;   // 2 bytes
   };
   #pragma pack(pop)

   int main() {
       std::cout << "Size of DefaultAligned: " << sizeof(DefaultAligned) << std::endl;
       std::cout << "Size of PackedStruct: " << sizeof(PackedStruct) << std::endl;
       return 0;
   }
   ```

   输出可能如下：

   ```
   Size of DefaultAligned: 12
   Size of PackedStruct: 7
   ```

3. 解释

   - `DefaultAligned`: 在大多数系统上，默认对齐会导致 `int` 类型对齐到 4 字节边界，所以在 `char a` 之后会有 3 字节的填充，总大小为 12 字节。
   - `PackedStruct`: 使用 `#pragma pack(1)` 后，所有成员紧密排列，没有填充，总大小就是所有成员大小的和，即 7 字节。

4. 注意事项

   a) 性能影响：过小的对齐值可能导致性能下降，因为某些处理器访问未对齐的数据会更慢。

   b) 可移植性：不同编译器对 `#pragma pack` 的支持可能有所不同，使用时需要考虑跨平台兼容性。

   c) 数据交换：在进行网络通信或文件 I/O 时，使用 `#pragma pack` 可以确保数据结构的紧凑表示。

   d) 潜在风险：改变对齐可能导致某些类型的未定义行为，特别是在处理指针时。

5. 替代方案

   C++11 引入了 `alignas` 说明符，它提供了一种更标准的方式来指定对齐：

   ```cpp
   struct alignas(1) ModernPacked {
       char a;
       int b;
       short c;
   };
   ```

6. 实际应用

   - 网络协议实现
   - 二进制文件格式定义
   - 与特定硬件接口交互
   - 跨平台数据序列化

7. 结论

   `#pragma pack(n)` 是一个强大的工具，可以精确控制数据结构的内存布局。然而，它应该谨慎使用，因为它可能影响性能和可移植性。在大多数情况下，让编译器处理对齐是更好的选择，只有在确实需要特定内存布局时才使用 `#pragma pack`。

   在使用时，务必理解其影响，并考虑到可能的跨平台问题。对于现代 C++ 编程，考虑使用 `alignas` 作为更可移植的替代方案。

### `union` 内存分配

联合体，顾名思义，整个数据联合为一个整体，故其所有成员共享同一块内存区域。分配内存时，按照其数据成员中，占用内存最大的成员来分配最终内存大小。

```C
union data{
    int a;    // int 占用内存最大的 4 byte
    short b;  // 2 byte
    char c;   // 1 byte
}
```

`data` 所占的空间等于其最大的成员所占的空间，即 `int` 为 `4byte`。对 `union` 型的成员的存取都是相对于该联合体基地址的偏移量为 0 处开始， 也就是*联合体的访问不论对哪个变量的存取都是从 `union` 的首地址位置开始*。成员 `a`, `b`, `c` 共享这 `4byte` 内存。其各成员所占用情况，如下图所示：

| `Address` | `0x03` | `0x02` | `0x01` | `0x00` |
| :-------: | :----: | :----: | :----: | :----: |
|  `int a`  | `yes`  | `yes`  | `yes`  | `yes`  |
| `short b` |  `no`  |  `no`  | `yes`  | `yes`  |
| `char c`  |  `no`  |  `no`  |  `no`  | `yes`  |

而其各成员的值，因计算机存储模式有关。因此，大端（Big endian）和小端（Little endian）存储模式将会直接影响 `union` 内成员的值。

> - 大端模式：字数据的高字节存储在低地址中，而字数据的低字节则存放在高地址中
> - 小端模式：字数据的高字节存储在高地址中，而字数据的低字节则存放在低地址中

若令联合体成员 `a = 4278190081` 16 进制表示为 `0xff 00 00 01`， - 大端模式下，其内存中值的情况如下：

| `Address` | `0x03` | `0x02` | `0x01` | `0x00` |   `真实值`   |
| :-------: | :----: | :----: | :----: | :----: | :----------: |
|  `int a`  | `0x01` | `0x00` | `0x00` | `0xff` | `0xff000001` |
| `short b` |  `no`  |  `no`  | `yes`  | `yes`  |   `0xff00`   |
| `char c`  |  `no`  |  `no`  |  `no`  | `yes`  |    `0xff`    |

- 小端模式下，其内存中值的情况如下：

| `Address` | `0x03` | `0x02` | `0x01` | `0x00` |   `真实值`   |
| :-------: | :----: | :----: | :----: | :----: | :----------: |
|  `int a`  | `0xff` | `0x00` | `0x00` | `0x01` | `0xff000001` |
| `short b` |  `no`  |  `no`  | `yes`  | `yes`  |   `0x0001`   |
| `char c`  |  `no`  |  `no`  |  `no`  | `yes`  |    `0x01`    |

由此可以看出，大端小端模式对联合体成员值的影响，反过来思考，则可以通过联合体成员值的不同，来判断存储模式为大端模式还是小端模式。

### `struct` 内存分配

结构体是由一系列具有相同类型或不同类型的数据构成的数据集合，其各成员拥有各自独立的空间。其内存分配满足一下四个原则：

- 最大的基本类型为其成员以及其成员的成员中，所占内存最大的基本类型。该基本类型的大小作为结构体内存分配的最小单元\(w\)
- 内存的分配顺序与其成员的申明顺序相同
- 若成员为基本类型，则存放的起始地址相对于结构的起始地址的偏移量必须为该变量的类型所占用的字节数的倍数
- 若该成员不是基本类型，则存放在起始地址相对于结构的起始地址的偏移量必须为\(w\)的倍数。该成员内部成员**独立**遵循此四条原则

对于基本类型，[CSDN 解释](http://msdn.microsoft.com/zh-cn/library/cc953fe1.aspx)如下：

> - C++ 中的基础类型分为三个类别：整数、浮动和 void。 整数类型能够处理整数。 浮动类型能够指定具有小数部分的值。

个人认为基础类型应该包括指针类型。由上可知，数组、结构体以及类等并非基本类型，当其嵌入在结构体中是，应当注意其成员中的基本类型。

#### 仅含有基本类型

```C
struct data1{
    int a;
    char b;
    short c;
};

struct data2{
    char b;
    int a;
    short c;
};
```

- 规则 1：在 `data1` 中，占内存最大的基本类型为 `int` ，故\(w=4\)。
- 规则 2：先分配 `int a`，分配最小单元为\(w=4\) byte， `a` 占用所分配的第 0-3 字节。再分配 `char b`, 已无剩余空间，于是再分配最小单元数 `4byte`。`b` 占第 4 个字节。还剩第 5-7 字节
- 规则 3：再分配 `short c`，地址偏移量需满足 2 的倍数，第 5 字节不满足，则 `b` 占用所分配的第 6、7 个字节。

若将其成员申明顺序变换一下，如 `data2`，则按照上述原则，内存分配如下图所示。

![Drawing](https://jiehust.github.io/assets/img/mem.jpg)

#### 含有非基本类型

```C
struct data1{
    int a;      // 最大基本类型,则最小分配单元为4byte   | 0 [a ][a ][  ][  ] 3
    char b[5];  // 非基本类型,其成员类型为char,占1byte  | 4 [b0][b1][b2][b3] 7
    short c;    //                                   | 8 [b4][  ][c ][c ] 11
};

struct data2{
    short s;
    data1 d;  // 非基本类型，data1成员中最大基本类型为 int, 则最小分配单元为4 byte
    char c;
};
```

仍然按照上述四条原则来分析:

- `data1` 占 `12byte`。
- `data2` 中，`data1` 子成员中最大基本类型为 `int`，`data2` 自身的基本类型成员最大为 `short`，故最终最小分配单元为 `4byte`，则先为 `s` 分配 `4byte`，`s` 占第 0-1 个字节。当分配 `data1 d` 时，根据第四条原则，第 2-3 字节不满足， `d` 从第 4 个字节开始分配，其子成员在 `data1` 内部独立满足上述四条规则。占用第 4-15 个字节，共 `12byte`，最终为`char c`分配 `4byte`。`data2` 共占 `20byte`

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

举例：修改调用函数中的 x 和 y，会直接影响到主函数中的 a 和 b 的值。因为他们是引用关系。

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

## C++函数传参

1. 非指针变量、class、struct：
   - 函数内修改值，不影响外部：传值(`int`)、传 const 引用(`const int &`)
   - 函数内修改值，影响外部：传指针(`int *`)、传非 const 引用(`int &`)
2. 指针变量：
   - 函数内修改指针指向，不影响外部：传指针(`int *`，对指针类型来说，就是传值)、传指向指针的 const 引用(`const int *&`)
   - 函数内修改指针指向，影响外部：传指针的指针(`int **`)、传向指针的非 const 引用(`int *&`)
3. 一维数组：
   - 函数内修改值，不影响外部：传指向数组的 const 引用(`const int (&arr)[2]`)
   - 函数内修改值，影响外部：传指向数组的指针(`int * 或 int arr[2]`)、传指向数组的引用(`int (&arr)[2]`)

> 这里 `int (&ref)[2]` 表示：
>
> - ref 是一个对数组的引用，数组的类型是 int[2]（长度为 2 的整型数组）。
> - ref 引用的数组大小是编译时确定的，因此**引用的数组大小必须匹配**。

## typedef 使用

在编程中使用 typedef 目的一般有两个，一个是给变量一个易记且意义明确的新名字，另一个是简化一些比较复杂的类型声明。

### 用途 1

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

### 用途 2

用在旧的 C 的代码中（具体多旧没有查），声明 struct 新对象时，必须要带上 struct，即形式为： `struct 结构名 对象名`，使用 typedef 可以少写一个 struct。如：

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

而在 C++中，在 C++中，typedef 的这种用途二不是很大，因为 C++ 中可以直接写：`结构名 对象名`，即：

```c++
tagPOINT1 p1;
```

### 用途 3

用 typedef 来定义与平台无关的类型。当跨平台时，只要改下 typedef 本身就行，不用对其他源码做任何修改。标准库就广泛使用了这个技巧，比如 size_t。

```c++
// 比如定义一个叫 REAL 的浮点类型，在目标平台一上，让它表示最高精度的类型为：
typedef long double REAL;

// 在不支持 long double 的平台二上，改为：
typedef double REAL;

// 在连 double 都不支持的平台三上，改为：
typedef float REAL;
```

### 用途 4

为复杂的声明定义一个新的简单的别名。方法是：在原来的声明里逐步用别名替换一部分复杂声明，如此循环，把带变量名的部分留到最后替换，得到的就是原声明的最简化版。举例：

1. 复杂声明 1：

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

2. 复杂声明 2：

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

网络博客 typedef 用法中提到一个复杂的声明：

```C++
doube()() (e)[9]; // 这个声明在gcc下编译时不通过的。按照作者的本意，应该这样声明：double(*(*pa)[9])();
```

例子：

```c++
typedef double (*pFun)(); // 定义函数指针pFun
typedef double (*(*e)[2])();

double Fun1()
{
    cout << "Fun1" << endl;
    return 1;
};

double Fun2()
{
    cout << "Fun2" << endl;
    return 2;
};

int main()
{
    pFun array[2] = {Fun1, Fun2};
    array[0](); // 执行Fun1
    array[1](); // 执行Fun2

    e MyE = &array;               // 将array的首地址赋给MyE
    cout << sizeof(MyE) << endl;  // 既然是指针，长度自然为4（32位机上）
    cout << sizeof(*MyE) << endl; // （两个指针）长度为8（32位机上）

    (*MyE[0])(); // 执行Fun1，注意优先级，其实就是 (*(MyE[0]))();

    (*MyE)[0](); // 执行Fun1
    (*MyE)[1](); // 执行Fun2

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
> 首先找到变量名 func，外面有一对圆括号，而且左边是一个*号，这说明 func 是一个指针；然后跳出这个圆括号，先看右边，又遇到圆括号，这说明 (*func)是一个函数，所以 func 是一个指向这类函数的指针，即函数指针，这类函数具有 int\*类型的形参，返回值类型是 int。
>
> ```c++
> int (*func[5])(int *);
> ```
>
> func 右边是一个[]运算符，说明 func 是具有 5 个元素的数组；func 的左边有一个*，说明 func 的元素是指针（注意这里的*不是修饰 func，而是修饰 func[5]的，原因是[]运算符优先级比*高，func 先跟[]结合）。跳出这个括号，看右边，又遇到圆括号，说明 func 数组的元素是函数类型的指 针，它指向的函数具有 int*类型的形参，返回值类型为 int。
>
> 也可以记住 2 个模式：
>
> ```c++
> type (*)(....)函数指针
> type (*)[]数组指针
> ```

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

## 整数的位操作：&、|、^、~

**机器数：**一个数在计算机中的二进制表示形式, 叫做这个数的机器数。**机器数是带符号的**，在计算机用一个数的最高位存放符号, 正数为 0, 负数为 1。比如，十进制中的数 +3 ，计算机字长为 8 位，转换成二进制就是 00000011。如果是 -3 ，就是 10000011 。这里的 00000011 和 10000011 就是机器数。

**真值：**因为第一位是符号位，所以机器数的形式值就不等于真正的数值。例如上面的有符号数 10000011，其最高位 1 代表负，其真正数值是 -3 而不是形式值 131（10000011 转换成十进制等于 131）。所以，为区别起见，将**带符号位的机器数对应的真正数值称为机器数的真值**。例：0000 0001 的真值 = +000 0001 = +1，1000 0001 的真值 = –000 0001 = –1

正数：原码 = 反码 = 补码

负数：原码、反码为原码除符号为按位取反、补码为反码加 1

整数在计算机中是**以补码的方式存储**。

这些操作都是按**补码**来操作的，输出为 8 进制或 16 进制时也是输出的补码，输出为 10 进制时才转换为机器数真值。

```C++
// -88&100 负数参与按位且，分析步骤
     1111 1111 1010 1000 // -88补码
    &0000 0000 0110 0100 // 100补码
     -------------------
     0000 0000 0010 0000 // 转成十进制结果为：32， 即-88&100 = 32
```

## 空 struct 指针的用途 C++

在 C++中，空的结构体指针可以用于以下情况：

- 占位符
  在一些代码中，我们可能需要一个占位符来表示某个变量或参数的位置，但是这个变量或参数当前并没有被定义或赋值。这时候，我们可以使用一个空的结构体指针来代替该变量或参数的位置，以便于后续代码的编写。

  例如，下面的代码中，我们定义了一个空的结构体 Dummy，并将其用作一个函数的参数占位符:

  ```c++
  struct Dummy {};
  void myFunction(Dummy* param1, int param2) {
    // ...
  }

  int main() {
    myFunction(nullptr, 42);
    return 0;
  }
  ```

- 作为泛型指针
  在 C++中，有时候我们需要定义一个通用的指针类型，以便于在不同的上下文中使用。这时候，我们可以使用空的结构体指针来定义这个通用的指针类型。

  例如，下面的代码中，我们定义了一个名为 GenericPointer 的类型，该类型是一个空的结构体指针：

  ```c++
  struct GenericPointer {};
  using MyPointer = GenericPointer*;
  ```

  在这个例子中，我们使用了 GenericPointer 来定义了一个别名 MyPointer，这个别名可以在不同的上下文中使用，以表示一个通用的指针类型。

- 作为哨兵值
  有时候，我们需要定义一个特殊的值来表示某种状态或条件。在这种情况下，我们可以使用空的结构体指针来作为哨兵值。

  例如，下面的代码中，我们定义了一个名为 EndOfList 的哨兵值，用于表示一个链表的末尾：

  ```c++
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
  ```

  在这个例子中，我们使用了一个空的结构体指针 EndOfList 来表示链表的末尾。由于 EndOfList 是一个空的结构体指针，它不会占用任何内存空间，因此可以作为一个轻量级的哨兵值来使用。

## 为什么使用空类

> [C/C++中，空数组、空类、类中空数组的解析及其作用](https://www.cnblogs.com/Allen-rg/p/7307116.html)

空类在“泛型编程”中，空类（空结构）的用处非常广：

我们利用类型（通常是空类），来区别对待不同类对象的属性。

通过使用函数重载的方法，在参数中加入一个空类来作为区分不同的函数的方法，编译的时候直接选择，而不是在运行的时候选择，是非常提高效率的。

要知道，不同的空类，是不同的。他们代表着不同的类型(虽然他们结构一样）。在 STL 中，使用空类区分不同类型的标志，从而在编译的时候来对不同的类进行有针对性的优化是非常常见的。

```c++
template<typename A>
void fun(A a) {
    typedef typename trait<A>::type T;
    _fun(A a, *(new T()));
}

template<typename A>
void _fun(A a, int) {
    // ......
}

template<typename A>
void _fun(A b, float) {
    // ......
}
```

当然，空类应该还有其他的用处。我们所有知道和理解的就是：空类是 C++ 中一个有用的机制，不同名称的空类代表着不同的类型。

<font color=red>空类在编译的时候会被编译器自动的加入一个 char 成员，不为别的，只是为了，让它被实例后的对象占有空间，从而可以区分。</font>

## mutable 关键字

mutable 是 C++中的一个关键字,主要用于修饰类的成员变量。它的主要作用是允许在 const 成员函数中修改被 mutable 修饰的成员变量。这打破了 const 成员函数不能修改类成员的一般规则。

以下是 mutable 关键字的几个要点:

1. 用途:

   - 允许在 const 成员函数中修改特定的成员变量。
   - 通常用于那些不影响对象逻辑状态的成员变量。

2. 语法:
   在声明成员变量时,在类型前加上 mutable 关键字。

   ```cpp
   class MyClass {
   private:
       mutable int counter;
   };
   ```

3. 常见应用场景:

   - 缓存机制：允许缓存的值在 const 对象中修改。
   - 线程同步：允许在 const 成员函数中修改同步机制（如锁、条件变量）。
   - 计数器：记录函数调用或对象访问次数。
   - 惰性初始化：延迟初始化不影响对象核心状态。

   1. 缓存机制

      这是 mutable 最常见的使用场景之一。当一个 const 成员函数需要进行密集计算时，可以缓存计算的结果，以提高程序性能。在这种情况下，缓存结果的变量通常不被认为是对象的核心逻辑状态。因此，可以将缓存变量声明为 mutable，以便在 const 对象中更新缓存值。

      ```cpp
      class BigData {
      private:
          mutable std::optional<int> cachedResult;
          std::vector<int> data;

      public:
          int computeResult() const {
              if (!cachedResult) {
                  // 假设这是一个耗时的计算
                  int result = 0;
                  for (const auto& item : data) {
                      result += std::pow(item, 2);
                  }
                  cachedResult = result;
              }
              return *cachedResult;
          }
      };
      ```

   2. 线程同步

      在 const 成员函数中,我们可能需要使用互斥锁来保证线程安全。这时可以将互斥锁声明为 mutable，以便在 const 成员函数中修改它们。锁的状态通常不属于对象的逻辑状态，因此这种设计是合理的。

      ```cpp
      class ThreadSafeCounter {
      private:
          mutable std::mutex mtx;
          int value;

      public:
          int getValue() const {
              std::lock_guard<std::mutex> lock(mtx);
              return value;
          }

          void increment() {
              std::lock_guard<std::mutex> lock(mtx);
              ++value;
          }
      };
      ```

   3. 统计或调试信息

      当我们想在 const 成员函数中更新一些不影响对象逻辑状态的统计信息时,可以使用 mutable。

      ```cpp
      class DataAnalyzer {
      private:
          mutable int accessCount = 0;
          std::vector<double> data;

      public:
          double getAverage() const {
              ++accessCount;  // 更新访问计数
              if (data.empty()) return 0.0;
              return std::accumulate(data.begin(), data.end(), 0.0) / data.size();
          }

          int getAccessCount() const {
              return accessCount;
          }
      };
      ```

   4. 惰性初始化

      在某些情况下，可能希望延迟初始化某个成员变量，直到它第一次被需要时再进行初始化。由于这种初始化不应影响对象的逻辑一致性，因此可以使用 mutable 来允许在 const 成员函数中完成初始化。

      ```cpp
      class LazyInitialization {
      private:
          mutable std::unique_ptr<ExpensiveObject> expensiveObject;

      public:
          const ExpensiveObject& getObject() const {
              if (!expensiveObject) {
                  expensiveObject = std::make_unique<ExpensiveObject>();
              }
              return *expensiveObject;
          }
      };
      ```

   5. 实现逻辑上的常量性

      有时,我们可能需要修改对象的某些内部状态,但这种修改在逻辑上不改变对象的值。

      ```cpp
      class String {
      private:
          char* str;
          mutable size_t hash_value;
          mutable bool hash_computed = false;

      public:
          size_t getHash() const {
              if (!hash_computed) {
                  hash_value = std::hash<std::string_view>()(str);
                  hash_computed = true;
              }
              return hash_value;
          }
      };
      ```

4. 注意事项:
   - 不要过度使用 mutable,它可能破坏 const 的语义。
   - 只将真正需要在 const 环境中修改的成员声明为 mutable。
5. 线程安全:
   mutable 成员在多线程环境中可能需要额外的同步机制。

# 小整理

## 类 class

**根据类型兼容原则，在指针和引用语义下，子类同时也可被视作是父类**。

## 二叉数组

找节点的子节点和父节点可以利用简单的算术计算它们在数组中的索引值

设某个节点索引值为 index,则节点的左子节点索引为:

2\*index+1

右子节点索引为:

2\*index+2

父节点索引为:

(index-1)/2

### 【C++断言机制】深入理解 C/C++ 中静态断言 static_assert 与断言 assert

<https://blog.csdn.net/qq_21438461/article/details/132293042>

### C/C++ for 循环的几种用法

<https://blog.csdn.net/cpp_learner/article/details/117395735?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-117395735-blog-54602752.235^v40^pc_relevant_3m_sort_dl_base4&spm=1001.2101.3001.4242.1&utm_relevant_index=1>

### C++ 类定义中 class+宏+类名的意义

<https://vzhougm.gitee.io/2021/06/25/c&c++/C++%20%E7%B1%BB%E5%AE%9A%E4%B9%89%E4%B8%ADclass+%E5%AE%8F+%E7%B1%BB%E5%90%8D%E7%9A%84%E6%84%8F%E4%B9%89/>

### 返回函数指针的函数

<https://www.cnblogs.com/lifexy/p/14098103.html>

## 《重构 改善既有代码的设计第二版》中文版

<https://github.com/MwumLi/book-refactoring2>

## c++ enum class compare

<https://juejin.cn/s/c%2B%2B%20enum%20class%20compare>

## 不能 delete void 指针

释放指针 void\*那里有问题，正确的做法应该做一个强制转换

## C++11

<https://www.apiref.com/cpp-zh/cpp/11.html>
值初始化
<https://www.apiref.com/cpp-zh/cpp/language/value_initialization.html>
C++11 特性之 default/delete
　在未显式的定义类的特殊成员函数时，如果被调用，系统会自动隐式的创建该特殊成员函数，且隐式的创建方式比显式的创建方式执行效率高。
　只需在函数声明后加上=default;，就可将该函数声明为 defaulted 函数，编译器将为显式声明的 defaulted 函数自动生成函数体，以获得更高的执行效率。
　有些时候，我们需要禁用某些函数(=delete 不仅可以禁用类内的特殊成员函数，也可以禁用一般函数)，此时就需要在该函数后面增加=delete；，则该函数将变的不可调用，比如不可复制等。

## extern 声明变量或函数

<https://blog.csdn.net/weixin_38145317/article/details/86496041>

## 裸数组

C /C++中，裸数组是个什么概念
ChatGPT 说：
ChatGPT
在 C/C++ 中，“裸数组”通常指的是原生数组或静态数组，即通过简单的语法声明的数组，不是通过容器类或智能指针管理的。这类数组是最基础的内存存储结构，提供最低级别的管理和控制。

裸数组的特点：
固定大小：裸数组在声明时必须指定大小，数组的大小是编译时常量，不能在运行时动态调整。

```cpp
int arr[10];  // 大小为10的整型数组，不能改变大小
```

不进行边界检查：访问裸数组的元素时，编译器不会检查是否越界，程序员需要自己确保访问安全。

```cpp
arr[11] = 5;  // 如果超出数组的边界，可能导致未定义行为
```

不自带内存管理：裸数组不进行任何自动化的内存管理，例如内存分配、释放或重新分配。数组元素的生命周期是由它们的存储类型（如局部变量、全局变量）决定的。

指针兼容性：裸数组可以被隐式转换为指向其第一个元素的指针。这是 C/C++ 中使用数组的核心特性。

```cpp
int* ptr = arr;  // arr 被转换为指向其第一个元素的指针
```

没有额外的功能：裸数组只提供最基本的功能，即元素存储和访问。相比之下，C++ 的标准容器如 std::vector 提供了更丰富的功能（如动态大小调整、边界检查等）。

裸数组的例子：

```cpp
int arr[5] = {1, 2, 3, 4, 5};  // 声明并初始化一个大小为5的数组
for(int i = 0; i < 5; ++i) {
    std::cout << arr[i] << std::endl;  // 输出数组元素
}
```

裸数组与现代 C++ 容器的对比：
在现代 C++ 中，裸数组的使用逐渐被更安全、更功能丰富的容器（如 std::vector 或 std::array）替代。裸数组虽然性能高且语法简单，但由于缺乏内存安全保障，容易引发诸如越界访问、内存泄漏等问题。因此，推荐在现代 C++ 代码中尽量使用标准库提供的容器类。

裸数组常见的问题：
内存泄漏（特别是与动态分配结合时）：

```cpp
int* arr = new int[10];
// 如果忘记调用 delete[] arr; 会导致内存泄漏
```

越界访问：

```cpp
arr[10] = 1;  // 如果数组大小为 10，则访问 arr[10] 会导致未定义行为
```

总之，裸数组是 C/C++ 中最基本的数组形式，但它的使用可能带来隐患，尤其是在涉及到复杂内存管理时。

## 整形存储指针

用整形存储指针是一种不常见但有特定用途的技术，这种技术通常用于低级编程、系统编程和性能优化的场景。**使用指针时 `reinterpret_cast` 转换成对应类型指针**，以下是一些常见的场景和原因：

### 1. **位操作和标志位**

在某些情况下，程序需要在指针的基础上存储额外的信息。例如，使用指针的低位来存储标志位。这在内存对齐的系统中特别有用，因为指针的低位通常是零，可以用来存储其他信息，而不会影响指针的实际地址。

```cpp
uintptr_t ptr_with_flags = reinterpret_cast<uintptr_t>(ptr) | flag;
```

### 2. **内存管理和垃圾回收**

内存管理系统和垃圾回收器有时会使用整形操作来操作和管理内存块。将**指针转换为整数可以方便地进行地址计算、内存对齐和其他低级操作**。

```cpp
uintptr_t addr = reinterpret_cast<uintptr_t>(ptr);
```

### 3. **序列化和反序列化**

在某些情况下，需要将指针序列化（如保存到文件或发送到网络）。由于指针是地址，在不同的程序运行期间可能会变化，所以通常将指针转换为整形来序列化，然后在反序列化时恢复。

```cpp
uintptr_t serialized_ptr = reinterpret_cast<uintptr_t>(ptr);
// 序列化后的数据
```

### 4. **性能优化**

某些高性能计算或嵌入式系统中，为了减少存储和计算开销，开发者可能会选择将指针转换为整形来进行特定的优化操作。这种方法可以绕过某些语言和硬件的限制。

```cpp
uintptr_t int_ptr = reinterpret_cast<uintptr_t>(ptr);
```

### 5. **调试和日志记录**

在调试和日志记录过程中，开发者可能需要记录指针的值。将指针转换为整形可以更容易地进行比较、打印和分析。

```cpp
uintptr_t int_ptr = reinterpret_cast<uintptr_t>(ptr);
std::cout << "Pointer value: " << int_ptr << std::endl;
```

### 6. **跨语言接口**

在与某些低级语言（如 C 和汇编）进行接口编程时，可能需要将指针转换为整形，以便在不同语言之间传递数据。

```cpp
uintptr_t addr = reinterpret_cast<uintptr_t>(ptr);
// 传递到其他语言的接口
```

### 安全性和注意事项

使用整形存储指针时需要非常小心，因为不正确的操作可能导致严重的错误和安全漏洞。常见的注意事项包括：

1. **类型安全**：避免无意的类型转换和错误使用。
2. **地址对齐**：确保指针的地址对齐要求，以避免未定义行为。
3. **平台依赖性**：指针大小和整形大小在不同平台上可能不同，注意可移植性问题。

总结来说，用整形存储指针是一种强大的技术，但应谨慎使用，并确保代码的可维护性和安全性。

# 标准库/编译器函数

根据 ANSI-C 标准，在标识符中，**两个下划线 `__` 保留给编译器内部使用，单个下划线 `_` 通常用于标准库函数的名称**（例如“ \_main”和“ \_exit”）。

## `__builtin_expect` 与 `likely(x)`

**`__builtin_expect`**：
这个指令是 **gcc 引入**的，作用是**允许程序员将最有可能执行的分支告诉编译器**。
写法为：`__builtin_expect(EXP, N)`，意思是：EXP==N 的概率很大。

一般的使用方法是将`__builtin_expect`指令封装为`likely`和`unlikely`宏。这两个宏的写法如下.

```c++
#define likely(x) __builtin_expect(!!(x), 1) //x很可能为真
#define unlikely(x) __builtin_expect(!!(x), 0) //x很可能为假
```

`!!(x)` 的作用是把(x)转变成"布尔值"：无论(x)的值是多少，`!(x)` 得到的是 `true` 或 `false`, `!!(x)` 就得到了原值的"布尔值"。

**likely() 与 unlikely()**：

首先要明确：

```c++
if(likely(value))  //等价于 if(value)
if(unlikely(value))  //也等价于 if(value)
```

`__builtin_expect()` 是 GCC (version >= 2.96）提供给程序员使用的，目的是将“分支转移”的信息提供给编译器，这样编译器可以对代码进行优化，以减少指令跳转带来的性能下降。
`__builtin_expect((x),1)` 表示 x 的值为真的可能性更大；
`__builtin_expect((x),0)` 表示 x 的值为假的可能性更大。
也就是说，使用`likely()`，执行 if 后面的语句的机会更大，使用 `unlikely()`，执行 else 后面的语句的机会更大。通过这种方式，编译器在编译过程中，会将可能性更大的代码紧跟着起面的代码，从而减少指令跳转带来的性能上的下降。

**例子**：

```c++
int x, y;
 if(unlikely(x > 0))
    y = 1;
else
    y = -1;
```

上面的代码中 gcc 编译的指令会预先读取 y = -1 这条指令，这适合 x 的值大于 0 的概率比较小的情况。如果 x 的值在大部分情况下是大于 0 的，就应该用 likely(x > 0)，这样编译出的指令是预先读取 y = 1 这条指令了。这样系统在运行时就会减少重新取指了。

## 导入导出库

### windows

可以使用两种方法将公共符号导入应用程序或从 DLL 导出函数：

- 生成 DLL 时使用模块定义 (.def) 文件
- 在主应用程序的函数定义中使用关键字 **`__declspec(dllimport)`** 或 **`__declspec(dllexport)`**

1. **使用 .def 文件**

   模块定义 (.def) 文件是文本文件，其中包含一个或多个描述 DLL 的各种特性的模块语句。 如果没有使用 **`__declspec(dllimport)`** 或 **`__declspec(dllexport)`** 来导出 DLL 的函数，则 DLL 需要 .def 文件。

   可以使用 .def 文件[导入到应用程序中](https://learn.microsoft.com/zh-cn/cpp/build/importing-using-def-files?view=msvc-170)或[从 DLL 导出](https://learn.microsoft.com/zh-cn/cpp/build/exporting-from-a-dll-using-def-files?view=msvc-170)。

2. **使用 `__declspec`**

   **Microsoft 专用**

   **`dllexport`** 和 **`dllimport`** 存储类特性是 C 和 C++ 语言的 **Microsoft 专用扩展**。 可以使用它们从 DLL 中导出或向其中导入数据、函数、类或类成员函数。

   > **`__declspec( dllimport )`** _`declarator`_ > **`__declspec( dllexport )`** _`declarator`_

   > [使用 \_\_declspec(dllexport) 从 DLL 导出](https://learn.microsoft.com/zh-cn/cpp/build/exporting-from-a-dll-using-declspec-dllexport?view=msvc-170)

### Unix/Linux

`__attribute__((visibility("default")))` 是 GCC（GNU Compiler Collection）和 Clang 编译器支持的属性，主要用于控制符号的可见性在共享库（shared libraries）中的行为。它在 Unix-like 系统（如 Linux、macOS）上使用，类似于 Windows 平台上的 \_\_declspec(dllexport)。
在没有特殊指定的情况下，现代编译器通常默认将所有符号设置为隐藏（hidden）。这意味着这些符号只在库内部可见，不能被外部代码直接访问。

**使用 visibility("default") 可以覆盖默认的隐藏行为，使得被标记的符号可以被外部代码访问**。这等同于将符号导出。

除了 "default"，还有其他可见性选项如 "hidden"（隐藏）、"internal"（内部）等。

### 跨平台解决方案

为了编写跨平台代码，开发者通常会定义类似这样的宏：

```cpp
#if defined(_WIN32) || defined(_WIN64)
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT __attribute__((visibility("default")))
#endif
```

这样，可以在代码中统一使用 EXPORT 关键字，在不同平台上编译时会自动选择合适的导出方法。

## 右值引用

右值引用（T&&）能在不构造对象的情况下“模拟”创建某个类型的对象，原因在于右值引用的语法允许我们声明一个引用，它指向的对象可以是临时的、未命名的对象，而不需要实际创建该对象。这个特性被 std::declval 所利用，使得我们可以在编译时“模拟”出某个类型的对象而不触发实际的构造函数调用。

原理

1. 右值引用不需要实际对象存在
   在 C++ 中，引用是一种绑定到现有对象的别名。右值引用专门用于绑定到临时对象（右值），而这些对象往往是短期存在、无命名的。重要的是，右值引用只是一个引用，它不需要对象实际存在，只需要编译器知道它将会引用什么类型的对象。

   例如，当你写出这样的代码时：

   ```cpp
   int&& r = 42;
   ```

   42 是一个临时对象（右值），而 r 是一个绑定到这个临时对象的右值引用。你可以通过 r 来访问 42，但你并没有手动创建一个持久的 int 对象。

   std::declval<T>() 使用的原理类似。它返回的是一个 T&&，但并不会真正创建一个 T 类型的对象。因此，编译器可以假装存在一个 T 类型的右值对象供我们使用，而实际上在运行时并没有这样的对象。

2. 右值引用允许访问类型的成员和操作
   由于右值引用只是在编译时告诉编译器要引用的类型是什么，我们可以使用右值引用来访问该类型的成员函数或运算符，而无需实际创建一个对象。这在模板元编程中尤其有用，因为我们可能只关心某个类型是否支持某个操作，而不想真的创建一个对象进行实际的操作。

   例如：

   ```cpp
   #include <utility> // for std::declval

   struct Foo {
   int getValue() { return 42; }
   };

   template <typename T>
   auto test() -> decltype(std::declval<T>().getValue()) {
   return 0;
   }

   int main() {
   test<Foo>(); // 没有创建 Foo 对象，但可以检查 getValue 函数
   }
   ```

   在这个例子中，std::declval<T>() 返回一个 T 的右值引用，通过它我们可以检查 T 是否有 getValue() 函数，但 Foo 对象本身从未真正被创建。

3. 避免实际构造对象的限制
   有些类型的对象可能无法实际构造，或者在编译时我们还不知道该类型是否有默认构造函数。右值引用允许我们绕过这些限制，进行类型检查和推导：

类型没有默认构造函数：某些类型无法直接构造（如有私有构造函数、删除默认构造函数等），但我们仍然可以通过右值引用访问它的成员函数或检查某些操作是否合法。

抽象类：抽象类不能实例化，但我们可以通过右值引用来模拟一个抽象类的对象，进而进行类型推导。

类的私有成员或受限访问：某些类可能有私有的构造函数或成员，无法在普通代码中直接构造对象。通过右值引用的模拟，我们可以在不实际构造对象的情况下，检查该类的某些特性。

为什么右值引用可以模拟？
右值引用之所以可以“模拟”对象的存在，主要有以下几点原因：

引用不需要实际创建对象：引用（包括右值引用和左值引用）只是类型的一种别名，它不需要实际的存储空间或者对象来引用。因此，右值引用不需要实际的对象存在，只需要类型本身就可以。

右值引用适合“临时对象”：右值引用通常用于绑定到临时对象，而这些对象可能在表达式计算后立刻消亡。这种短暂的存在让右值引用能够灵活地进行类型推导，而无需考虑对象的生命周期。

编译时推导：在模板元编程或 SFINAE 中，我们仅仅关心编译时的类型属性，而不需要实际执行代码。在这种上下文中，右值引用只需告诉编译器我们打算使用的类型是 T，而编译器会检查类型及其成员函数是否合法，而不需要实际创建对象。

总结
右值引用允许我们在不实际构造对象的情况下，推导类型属性和成员函数合法性。
std::declval 通过返回类型的右值引用（T&&），让编译器能够在模板元编程中“模拟”对象的存在，进而进行类型推导、SFINAE 检查等操作。
右值引用的这种特性非常有助于元编程，因为它避免了不必要的构造开销，并能处理无法实际构造的类型。

## enable_shared_from_this

std::enable_shared_from_this<T>：当一个类继承自 std::enable_shared_from_this<T>（T 是类本身），这个类的对象就可以通过 shared_from_this() 函数生成一个指向自身的 std::shared_ptr。

在使用 std::shared_ptr 时，直接通过 this 来创建一个新的共享指针是危险的，因为这可能会导致管理同一个对象的多个共享指针，而它们彼此之间并不知道对方的存在，最终可能导致对象被提前析构或析构多次。
std::enable_shared_from_this 提供了一种机制，允许类对象在创建时将自己与 shared_ptr 关联起来，从而保证即使在类的成员函数中调用 shared_from_this()，也可以获取正确的、引用计数一致的 std::shared_ptr。
