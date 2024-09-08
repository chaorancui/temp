[toc]

# `C++ 11/14/17/20 新特性总结`

## `C++11`

### 1. constexpr

`constexpr` 是 C++ 11 中新增加的用于**指示常量表达式**的关键字。在此之前（C++ 98/03 标准）只有 `const` 关键字，其在实际使用中经常会表现出**两种不同的语义**。举个例子：

总的来说在 C++ 11 标准中，`const` 用于为修饰的变量添加“只读”属性；而 `constexpr` 关键字则用于指明其后是一个常量（或者常量表达式），编译器在编译程序时可以顺带将其结果计算出来，而无需等到程序运行阶段，这样的优化极大地**提高了程序的执行效率**。

### 2. 自动推导 atuo 和 decltype

auto 和 decltype 是在 C++11 中引入的关键字，可以在**编译期**推导出变量或者表达式的类型，方便开发者编写代码。

#### **auto**

**概括：**

- `cv` 属性指的是 `const` 和 `volatile`。其中 `const` 区分顶层和底层。auto 推导中，**底层 const 会保留下来**。顶层 const 若需保留需在声明 auto 变量时明确指出，如 `const auto xxx`。
- 在声明的变量类型**不为指针或引用**的情况下，需**忽略**等号右边的引用类型和 `顶层cv` 属性，得到 atuo 占位符的类型，进而得到变量类型。
- 在声明的变量类型**为指针或引用**的情况下，需**保留**等号右边的引用和 `顶层cv` 属性，得到 atuo 占位符的类型，进而得到变量类型。
- auto 在一行定义多个变量时，各个变量的推导不能产生二义性。
- auto 推导表达式类型时会进行考虑隐式类型转换，如 `uint32_t + uint64_t` 推导的结果为 `uint64_t`。
- auto 定义的变量必须有初始值，即定义的同时就要初始化。

在 **《Effective Modern C++》** 这本书中，**Scott Meyers** 将 **auto** 的类型推导规则划分为了 3 种场景，并对每种场景依次介绍了其推导方式[1]：

##### 场景 1：声明的变量类型是引用或者指针，但不是转发引用

在这种场景下，按照以下方式推导：

1. 如果初始化表达式是引用类型，先忽略引用部分；
2. 将初始化表达式的类型作为**auto**占位的类型。

```c++
int x = 27;
const int cx = x;
const int &rx = x;

auto &a = x;  // a被推导为int&
auto &b = cx;  // b被推导为const int&
auto &c = rx;  // c被推导为const int&
auto d = &x; // d被推导为int *
auto e = &cx; // e被推导为cosnt int *
```

对变量 b 来说，其初始化表达式 cx 的类型是 const int，用 const int 替换 auto 占位符，得到 b 的类型是 const int&。

对变量 c 来说，其初始化表达式 rx 的类型是 const int&，这时要先应用步骤 1，把引用去掉，变为 const int，之后的推导和 b 一样。

场景 1 还有一个变体：当声明的变量是 **const** 引用或指针时，推导过程大致相同，但是这个时候，初始化表达式的 **const** 属性不再需要作为 **auto** 占位符的一部分：

```c++
int x = 27;
const int cx = x;
const int &rx = x;

const auto &a = x;  // a被推导为const int&
const auto &b = cx;  // b被推导为const int&
const auto &c = rx;  // c被推导为const int&
const auto d = &rx;  // d被推导为const int *const
```

这里的 b 和 c 在推导时，由于声明的类型已经带有 const，因此 auto 占位符只需要被替换为 int，得到 const int& 类型。

##### 场景 2：声明的变量类型是转发引用

在这种场景下，变量类型的推导大体遵循以下规则：

1. 如果初始化表达式的类型是左值，变量被推导为左值引用类型；
2. 如果初始化表达式的类型是右值，推导方式同场景 1。

```C++
int x = 27;
const int cx = x;
const int& rx = x;

auto&& a = x;  // a被推导为int&
auto&& b = cx;  // b被推导为const int&
auto&& c = rx;  // c被推导为const int&
auto&& d = 28;  // d被推导为int&&
```

注意转发引用的语法很像右值引用，很多同学会把 auto&& 误解为右值引用。但实际上从上面的例子可以看出，a、b、c 三个变量都不是右值引用，只有 d 因为初始化表达式是右值，所以成为了右值引用。

转发引用的推导背后还有引用折叠的原理，需要了解相关知识的，可以阅读《Effective Modern C++》的 Item24~Item28。

##### 场景 3：声明的变量类型既不是引用也不是指针

在这种场景下，按照以下方式推导：

1. 如果初始化表达式是引用类型，忽略引用部分（和场景 1 一样）；
2. 如果初始化表达式带有 const 或 volatile 属性，同样忽略。

```C++
int x = 27;
const int cx = x;
const int& rx = x;

auto a = x;  // a被推导为int
auto b = cx;  // b被推导为int
auto c = rx;  // c被推导为int
```

在这个场景下，推导出的类型不会是引用类型，它往往会导致非预期的拷贝（或者移动）。

##### 定义多个变量

要在一条语句中定义多个变量， 切记， 符号 `＆` 和 `＊` 只从属于某个声明符， 而非基本数据类型的一部分， 因此初始值必须是同一种类型：

```cpp
int* pl, p2;            // pl 是指向 int 的指针，p2是 int。基本数据类型是 int 而非 int＊

int i = 0;
const int ci = i;
auto k = ci, &l = i;    // k 是整数，l 是整型引用
auto &m = ci, *p = &ci; // m 是对整型常量的引用，p 是指向整型常量的指针
// 错误： i 的类型是 int，而 ＆ci 的类型是 const int
auto &n = i, *p2 = &ci;
```

#### **decltype**

希望从表达式的类型推断出要定义变量的类型，但是不想用该表达式的值初始化变量（auto 需要定义时初始化）。为了满足这一要求，C++11 新标准引入了第二种类型说明符 `decltype`，它的作用是选择并返回操作数的数据类型。在此过程中，编译器分析表达式并得到它的类型， 却不实际计算表达式的值（这和 **sizeof** 很像）。

**概括：**

- `decleartype` 表达式为**变量**，则结果为该变量的类型（包括顶层 const 和引用在内）。
- `decleartype` 表达式**本身有括号**，则结果固定为引用类型。
- `decltype(*p)` **解引用操作**的结果为引用类型。
- decltype 推导表达式类型时会进行考虑隐式类型转换，如 `uint32_t + uint64_t` 推导的结果为 `uint64_t`。

##### 推导变量

`decleartype` 使用的表达式是一个**变量**，则 `decltype` 返回该变量的类型（包括顶层 const 和引用在内）。

```cpp
const int ci = 0, &cj = ci;
decltype(ci) x = O; // x 的类型是 const int
decltype(cj) y = x; // y 的类型是 const int &, y 绑定到变量 x
decltype(cj) z; // 错误：z 是一个引用， 必须初始化
```

##### 推导表达式

如果 `decltype` 使用的表达式不是一个变量，则 `decltype` 返回**表达式结果对应的类型**。
如果表达式的内容是**解引用操作**，则 `decltype` 将得到引用类型。原因：解引用指针可以得到指针所指的对象，而且还能给这个对象赋值，因此，`decltype(*p)` 的结果类型就是引用类型而非变量本身类型。

```cpp
// decltype 的结果可以是引用类型
int i = 42, *p = &i, &r = i;
decltype(r + 0) b;  // 正确：加法的结果是 int，因此 b 是一个（未初始化的）int
decltype(*p) c;     // 错误：e 是 int &，必须初始化。
```

##### 表达式括号

如果变量名加上了一对括号， 则得到的类型与不加括号时会有不同。
如果 decltype 使用的是一个不加括号的变量，则得到的结果就是该变量的类型；
如果给变量加上了一层或多层括号，编译器就会把它当成是一个表达式。
变量是一种可以作为赋值语句左值的特殊表达式， 所以这样的 decltype 就会得到引用类型。

```cpp
// decltype 的表达式如果是加上了括号的变量，结果将是引用
decltype((i)) d;    // 错误：d 是 int &，必须初始化
decltype(i) e;      // 正确：e 是一个（未初始化的）int
```

> 切记：**decltype ((variable))（注意是双层括号）的结果永远是引用，而 decltype(variable)结果只有当 variable 本身就是一个引用时才是引用**。

##### 多用于模板

```C++
// decltype 应用场景：decltype 通常用于追踪返回类型『复合符号 -> decltype() 』
// 某些库用 decltype 来实现完美转发
template <typename T1, typename T2>
auto sum(T1 &t1, T2 &t2) -> decltype(t1 + t2)
{
    return t1 + t2;
}
```

### 3. Lambda 表达式

C++11 的一大亮点就是引入了 Lambda 表达式。利用 Lambda 表达式，可以方便的定义和创建匿名函数。

```c++
// Lambda 表达式完整的声明格式如下：
[capture list] (params list) mutable exception -> return type { function body }

// 省略其中的某些成分来声明“不完整”的Lambda表达式,常见的有以下几种：
[capture list] (params list) -> return type {function body} // 不能修改捕获列表中的值
[capture list] (params list) {function body} // 省略了返回值类型，编译器推导（有 return 根据表达式来，无 return 为 viod）
[capture list] {function body} // 省略了参数列表，类似普通函数中的无参函数
```

**各项具体含义如下**

1. capture list：捕获外部变量列表
2. params list：形参列表
3. mutable 指示符：用来说用是否可以修改捕获的变量
4. exception：异常设定
5. return type：返回类型
6. function body：函数体

**捕获列表**

- []：默认**不捕获**任何变量；

- [=]：默认**以值捕获**所有变量；

- [&]：默认**以引用捕获**所有变量；

- [x]：仅以值捕获 x，其它变量不捕获，捕获多个变量用 "," 分隔；

- [&x]：仅以引用捕获 x，其它变量不捕获；

- [=, &x]：默认以值捕获所有变量，但是 x 是例外，通过引用捕获；

- [&, x]：默认以引用捕获所有变量，但是 x 是例外，通过值捕获；

- [this]：通过引用捕获当前对象（其实是复制指针）；

- [*this]：通过传值方式捕获当前对象；没有[&this]

  > C++11/14/17/20 的捕获行为有差异

**修改捕获变量**
在 Lambda 表达式中，如果以传值方式捕获外部变量，则函数体中不能修改该外部变量，否则会引发编译错误。那么有没有办法可以修改值捕获的外部变量呢？这是就需要使用 mutable 关键字，该关键字用以说明**表达式体内的代码可以修改值捕获的变量**。

**Lambda 表达式的参数**
Lambda 表达式的参数和普通函数的参数类似，但有区别。在 **Lambda 表达式中传递参数限制**如下：

1. 参数列表中不能有默认参数
2. 不支持可变参数
3. 所有参数必须有参数名

**捕获列表和参数列表**

在 C++的 Lambda 表达式中，捕获列表（capture list）和参数列表（parameter list）都是可选的部分，但它们的作用不同。

参数列表是用于定义 Lambda 表达式的形参的，这些形参可以在 Lambda 函数体中被使用。Lambda 表达式的形参列表和函数的参数列表一样，可以有默认值和可变参数等特性。

而捕获列表则用于在 Lambda 表达式内捕获外部作用域的变量，以供 Lambda 函数体中使用。这些变量可以是 Lambda 函数外部的局部变量、全局变量、静态变量等等。当 Lambda 表达式被定义时，**捕获列表会将这些变量复制到 Lambda 函数体内**，使 Lambda 函数能够在不同的上下文中执行而不受影响。

### 4. 强类型枚举

C++11 引入了语法为 `enum class` 的强类型枚举。 它们与整数类型不兼容，并且需要显式转换以获取其数值。 C++11 还引入了以 `enum name : type {}` 形式为弱类型枚举指定存储类的功能。

### 5. for_each

```cpp
int testA[] = {1,2,3,4,5};
for_each(testA,testA + sizeof(testA)/sizeof(testA[0]),[](int &e){  cout << e << endl;});

```

### 6. 基于范围的 for 循环

C++11 中引入了 for_each 循环的语言特性（自动确定循环范围），使用这个特性能够非常方便快捷的对**「普通数组 / STL 容器」**中的元素进行遍历，而不必再关心和计算他们的的界限。

```C++
int num[5] = {1, 2, 3, 4, 5};
for (auto x : num) {
   cout << x << endl;
}
```

上面`for`述句的第一部分定义被用来做范围迭代的变量，就像被声明在一般 for 循环的变量一样，其作用域仅只于循环的范围。而在":"之后的第二区块，代表将被迭代的范围。

这种 for 语句还可以用于**C 型数组**，**初始化列表**，和任何定义了`begin()`和`end()`来回返**首尾迭代器的类型**。

**基于范围 for 循环使用细节：**

```C++
/*  1.基于范围的FOR循环的遍历是只读的遍历，除非将变量变量的类型声明为引用类型。 */
std::vector<int> vec {1,2,3,4,5,6,7,8,9,10};
for (auto& n :vec) {
    n++; // vec 中每个元素自加1
}

/* 2.在遍历容器的时候，auto 自动推导的类型是容器的value_type类型，而不是迭代器，而 map 中的 value_type 是 std::pair，也就是说 val 的类型是 std::pair 类型的，因此需要使用 val.first,val.second 来访问数据。 */
std::map<string, int>  map = { { "a", 1 }, { "b", 2 }, { "c", 3 } };
for (auto &val : map) {
    cout << val.first << "->" << val.second << endl;
}

/* 3.用基于范围的for循环迭代时修改容器会导致代码崩溃 */
vector<int> vec = { 1, 2, 3, 4, 5, 6 };
for (auto &n : vec) {
    cout << n << endl;
    vec.push_back(7);
}

/* 4.如果冒号后面的表达式是一个函数调用时，函数仅会被调用一次。 */
set<int> ss = { 1, 2, 3, 4, 5, 6 };
const set<int>& getSet() {
 cout << "GetSet" << << ", ";
 return ss;
}
for (auto &n : getSet()) {
    cout << n << ", ";
} // 输出为：GetSet， 1， 2， 3， 4， 5， 6，
```

> 1. 基于范围的 for 循环和普通的 for 循环一样，在遍历的过程中如果修改容器，会造成迭代器失效，（有关迭代器失效的问题请参阅 C++ primer 这本书，写的很详细）
> 2. 注意：如果数组（集合）的大小（范围）在编译期间不能确定，那么不能够使用基于范围的 for 循环。

### 7. static_assert

C++11 中引入了 `static_assert` 这个关键字，用来做**编译期间的断言**，因此叫做静态断言。

语法： `static_assert(常量表达式，提示字符串)`;

如果“常量表达式”的值为真( true 或者非零值)，那么 static_assert 不做任何事情，否则会产生一条编译错误，错误位置就是该 static_assert 语句所在行，错误提示就是“提示字符串”。

static_assert 的特点：

- 使用范围：可以用在全局作用域，命名空间、类或函数的作用域中

- 常量表达式的结果必须是在编译时期可以计算的表达式，即必须是常量表达式

- 可检查模板参数

- 编译期间断言，不生成目标代码，不会产生任何运行期性能开销

对于**常量表达式、模板参数的检查**建议使用静态断言 static_assert 。

```c++
// 使用静态断言检查类型的大小。
static_assert(sizeof(int) == 4, "system is not supported.");

// 使用静态断言检查模板参数。
template <typename T>
void swap(T& a, T& b)
{
    static_assert(std::is_copy_constructible<T>::value, "Swap requires copy");
    static_assert(std::is_nothrow_copy_assignable<T>::value, "Swap requires nothrow assign");
    static_assert(std::is_nothrow_copy_constructible<T>::value, "Swap requires nothrow copy");
    auto c = b;
    b = a;
    a = c;
}
```

> 在 C++20 开始引入 `concepts` ，相比 `static_assert` ，其功能上更强大，提供了很好的诊断功能。

### 8. std::thread

C++11 增加了线程以及线程相关的类, 而之前并没有对并发编程提供语言级别的支持。

`std::thread 类`

使用 `std::thread` 类来创建线程, 我们需要提供的只是线程函数, 或者线程对象, 同时提供必要的参数。`std::thread` 表示单个执行的线程, 使用`thread` 类首先会构造一个线程对象, 然后开始执行线程函数。

```C++
#include <iostream>
#include <thread> //需要包含的头

using namespace std;

void func(int a, double b)  //有参数, 参数数量不限
{
    cout << a << ' ' << b << endl;
}

void func2() //无参数
{
    cout << "hello!\n";
}

int main()
{
    thread t1(func, 1, 2); //提供参数
    thread t2(func2);

    //可以使用 lambda表达式
    thread t3([](int a, double b){cout << a << ' ' << b << endl;}, 3, 4);

    cout << t1.get_id()  << "****" << endl;  //可以使用 get_id() 获取线程 id
    t1.join();
    t2.join();
    t3.join();

    return 0;
}
```

**使用 join()**
我们知道, 上例中如果主线程 (main) 先退出, 那些还未完成任务的线程将得不到执行机会, 因为 main 会在执行完调用 exit(), 然后整个进程就结束了, 那它的"子线程" (我们知道线程是平级的, 这里只是, 形象一点) 自然也就 over 了。
所以就像上例中, 线程对象调用 join() 函数, **join() 会阻塞当前线程**, 直到线程函数执行结束, 如果线程有返回值, 会被忽略。

**使用 detach()**
对比于 join(), 我们肯定有**不想阻塞当前线程的时候, 这时可以调用 detach(**), 这个函数会分离线程对象和线程函数, 让线程作为后台线程去执行, 当前线程也不会被阻塞了, 但是分离之后, 也不能再和线程发生联系了, 例如不能再调用 get_id() 来获取线程 id 了, 或者调用 join() 都是不行的, 同时也无法控制线程何时结束。程序终止后, 不会等待在后台执行的其余分离线程, 而是将他们挂起, 并且本地对象被破坏。

**警惕作用域**

`std::thread` 出了作用域之后就会被析构, 这时如果线程函数还没有执行完就会发生错误, 因此, 要注意**保证线程函数的生命周期在线程变量之内**。

**线程不能复制**

**`std::thread` 不能复制, 但是可以移动**
也就是说, 不能对线程进行复制构造, 复制赋值, 但是可以移动构造, 移动赋值

> 使用 C++11 进行多线程开发 (std::thread)：<https://blog.csdn.net/weixin_36888577/article/details/82891531>

### 9. alignof & alignas 说明符

> [alignof 运算符(C++11 起)](https://zh.cppreference.com/w/cpp/language/alignof)

查询类型的对齐要求。

语法：

```C++
alignof(类型标识)
```

[返回 std::size_t](https://en.cppreference.com/w/cpp/types/size_t)类型的值。

解释

返回由[类型标识](https://zh.cppreference.com/w/cpp/language/type#.E7.B1.BB.E5.9E.8B.E7.9A.84.E5.91.BD.E5.90.8D)所指示的类型的任何实例所要求的[对齐](https://zh.cppreference.com/w/cpp/language/object#.E5.AF.B9.E9.BD.90)字节数，该类型可以是[完整](https://zh.cppreference.com/w/cpp/language/type#.E4.B8.8D.E5.AE.8C.E6.95.B4.E7.B1.BB.E5.9E.8B)对象类型、元素类型完整的数组类型或者到这些类型之一的引用类型。

如果类型是引用类型，那么运算符返回*被引用*类型的对齐要求；如果类型是数组类型，那么返回元素类型的对齐要求。

> [alignas 说明符 (C++11 起)](https://www.apiref.com/cpp-zh/cpp/language/alignas.html)
>
> [alignas 用法](https://juejin.cn/s/alignas%E7%94%A8%E6%B3%95)

`alignas` 是一个 C++11 中的关键字，用于指定变量、结构体、联合体、类等对象的对齐方式。它可以用来控制数据的内存对齐，以优化内存的访问速度。

`alignas` 的使用方法如下：

```scss
alignas(n) type variable;
```

其中，`n` 是对齐要求的字节数，必须是 2 的幂次方，`type` 是变量的数据类型，`variable` 是变量名。

`alignas` 的作用是让变量在内存中按照指定的对齐方式分配内存。例如：

```scss
alignas(16) int a; // 按照 16 字节对齐
alignas(32) char b; // 按照 32 字节对齐
```

在这个例子中，变量 `a` 按照 16 字节对齐，变量 `b` 按照 32 字节对齐。

需要注意的是，如果指定的对齐值比默认对齐值更小，则指定的对齐值会被忽略。例如：

```c
struct alignas(4) A {
  char c;
  int i;
};

sizeof(A) // 结果为 8，而不是 6
```

在这个例子中，`A` 结构体的对齐方式为 4 字节，但是由于默认对齐值是 8 字节，所以实际上 `A` 结构体的大小是 8 字节。

总之，`alignas` 可以用来控制数据的内存对齐方式，以优化内存访问速度。但是需要注意，如果指定的对齐值比默认对齐值更小，则指定的对齐值会被忽略。

### 10.tuple

## `C++ 14`

### 1. std::make_unique<T>()

从 C++14 开始，有一个库函数 make_unique<T>() 可用于创建 unique_ptr 对象。该函数分配一个类型为 T 的对象，然后返回一个拥有该对象的独占指针。例如，来看下面的代码：

```c++
unique_ptr<int> uptr(new int); // 可以弃用此代码
unique_ptr<int> uptr = make_unique<int>(); // 改为使用此代码
```

### std::enable_if_t

> [C++ SFINAE 简介和 std::enable_if_t 的简单使用](https://blog.csdn.net/wangx_x/article/details/122867422)
>
> [c++模板元编程 std::enable_if 详解](https://blog.csdn.net/SWX230162/article/details/124587261?spm=1001.2101.3001.6650.3&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-3-124587261-blog-84667071.235%5Ev43%5Epc_blog_bottom_relevance_base3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-3-124587261-blog-84667071.235%5Ev43%5Epc_blog_bottom_relevance_base3&utm_relevant_index=4)

先引入一个很重要的概念：`SFINAE`，这是英文 Substitution failure is not an error 的缩写，意思是**匹配失败不是错误**。这句话的意思是：我们使用模板函数时编译器会根据传入的参数来推导适配最合适的模板函数，在某些情况下，推导过程会发现某一个或者某几个模板函数推导起来其实是无法编译通过的，但只要有一个可以正确推导并编译出来，则那些推导得到的可能产生编译错误的模板函数就并不会引发编译错误，即匹配失败不是错误。

现在开始描述下 `std::enable_if` 的使用方式吧，`std::enable_if` 顾名思义，满足条件时类型有效。作为选择类型的小工具，其广泛的应用在 C++ 的模板元编程（meta programming）中。基本实现方式大约为：

```cpp
template<bool B, class T = void>
struct enable_if {};

template<class T>
struct enable_if<true, T> { typedef T type; };
```

一个是**普通版本的模板类定义**，一个**偏特化版本的模板类定义**。
主要在于第一个参数是否为 true，当第一个**模板参数为 false 的时候并不会定义 type**，只有在第一模板参数为 true 的时候才会定义 type。

```cpp
typename std::enable_if<true, int>::type t; // 正确，type等同于int
typename std::enable_if<true>::type; // 可以通过编译，没有实际用处，推导的模板是偏特化版本，第一模板参数是true，第二模板参数是通常版本中定义的默认类型即void，但是一般也用不上它。
typename std::enable_if<false>::type; // 无法通过编译，type类型没有定义
typename std::enable_if<false, int>::type t2; // 同上
```

网上扒过来了一个用于偏特化的小例子：

```cpp
template <typename T>
typename std::enable_if<std::is_trivial<T>::value>::type SFINAE_test(T value)
{
    std::cout<<"T is trival"<<std::endl;
}

template <typename T>
typename std::enable_if<!std::is_trivial<T>::value>::type SFINAE_test(T value)
{
    std::cout<<"T is none trival"<<std::endl;
}
```

下面是一个用于校验函数模板参数类型的小例子：

```cpp
template <typename T>
typename std::enable_if<std::is_integral<T>::value, bool>::type
is_odd(T t) {
  return bool(t%2);
}

template <typename T, typename = typename std::enable_if<std::is_integral<T>::value>::type>
bool is_even(T t) {
  return !is_odd(t);
}
```

到这里对于 `enable_if_t` 就更通俗易懂了：

```cpp
template <bool _Test, class _Ty = void>
using enable_if_t = typename enable_if<_Test, _Ty>::type;
```

**使用场景**
**类型偏特化**
在使用模板编程的时候，可以使用 enbale_if 的特性根据模板参数的不同特性进行不同的类型选择。

```cpp
template<class T, class Enable = void>
class Test {
public:
 Test() {
  std::cout << "normal template" << std::endl;
 }
};

template<class T>
class Test<T, typename std::enable_if<std::is_floating_point<T>::value>::type> {
public:
 Test() {
  std::cout << "is_floating_point" << std::endl;
 }
};
int main() {
 auto a1 = std::make_shared<Test<int>>();
   auto a2 = std::make_shared<Test<float>>();
   return 0;
}
```

执行结果：

```shell
normal template
is_floating_point
```

**控制函数返回值**
通过函数的返回值，在不同的条件下，选择不同的模板。

```cpp
template <typename T>
typename std::enable_if<std::is_integral<T>::value,bool>::type
GetValue (T i) {
 cout << "is integral" << endl;
 return i>0;
}
template <typename T>
typename std::enable_if<!std::is_integral<T>::value,bool>::type
GetValue (T i) {
 cout << "is not integral" << endl;
 return i>0;
}

int main()
 int i = 1;
 float f = 2.0;
 std::cout << i << " GetValue : " << GetValue(i) << std::endl;
 std::cout << f << " GetValue : " << GetValue(f) << std::endl;
 return 0;
}
```

执行结果：

```shell
1 GetValue : is integral
1
2 GetValue : is not integral
```

函数参数场景
通过函数的参数，在不同的条件下，选择不同的模板。

```cpp
template <typename T,
          typename std::enable_if<std::is_integral<T>::value, int>::type = 0>
void TestFunc(T msg) {
 std::cout << "is integral" << std::endl;
}

template <typename T,
          typename std::enable_if<!std::is_integral<T>::value, int>::type = 0>
void TestFunc(T msg) {
 std::cout << "is not integral" << std::endl;
}
```

执行结果：

```shell
is integral
is not integral
```

另外这块的详细使用场景也可以看下百度 apollo cyber 代码中 message 部分的封装，也是大量使用了 std::enable_if。

## `C++ 17`

> [std::optional](https://zh.cppreference.com/w/cpp/utility/optional)
>
> [C++语法糖(std::optional)详解以及示例代码](https://zhuanlan.zhihu.com/p/627806230)
>
> [C++17 之 std::optional 全方位详解](https://blog.csdn.net/hhdshg/article/details/103433781)

### 1. std::optional

类模板 `std::optional` 管理一个*可选*的所含值，即**既可以存在也可以不存在的值**。

一种常见的 `optional` 使用情况是作为可能失败的函数的返回值。与如 [std::pair](http://zh.cppreference.com/w/cpp/utility/pair)<T, bool> 等其他手段相比，`optional` 可以很好地处理构造开销高昂的对象，并更加可读，因为它明确表达了意图。

当一个 `optional<T>` 类型的对象被[按语境转换到 bool](https://zh.cppreference.com/w/cpp/language/implicit_conversion) 时，若对象*含值*则转换返回 true，若它*不含值*则返回 false。

```C++
#include <iostream>
#include <optional>

std::optional<int> divide(int a, int b) {
    if (b == 0) {
        return std::nullopt;
    } else {
        return a / b;
    }
}

int main() {
    auto result1 = divide(10, 2);
    if (result1.has_value()) {
        std::cout << "Result 1: " << result1.value() << std::endl;
    } else {
        std::cout << "Result 1: division by zero" << std::endl;
    }

    auto result2 = divide(10, 0);
    if (result2.has_value()) {
        std::cout << "Result 2: " << result2.value() << std::endl;
    } else {
        std::cout << "Result 2: division by zero" << std::endl;
    }

    return 0;
}
```

如果分母为零，则返回一个 std::nullopt，表示结果不存在。否则，返回一个包含除法结果的 std::optional<int>类型的对象。

### 2. [[maybe_unused]]

提示编译器修饰的内容可能暂时没有使用，避免产生警告。

这个属性可以出现在以下实体的声明中。

- [class / struct / union](https://runebook.dev/zh-CN/docs/cpp/language/classes)： `struct [[maybe_unused]] S;` ，
- [typedef](https://runebook.dev/zh-CN/docs/cpp/language/typedef)，包括[别名声明](https://runebook.dev/zh-CN/docs/cpp/language/type_alias)所声明的那些： `[[maybe_unused]] typedef S* PS;` ， `using PS [[maybe_unused]] = S*;` ，
- 变量，包括[静态数据成员](https://runebook.dev/zh-CN/docs/cpp/language/static)： `[[maybe_unused]] int x;` ，
- [非静态数据成员](https://runebook.dev/zh-CN/docs/cpp/language/data_members)： `union U { [[maybe_unused]] int n; };` ，
- [函数](https://runebook.dev/zh-CN/docs/cpp/language/function)： `[[maybe_unused]] void f();` ，
- [枚举](https://runebook.dev/zh-CN/docs/cpp/language/enum)： `enum [[maybe_unused]] E {};` ，
- 枚举器： `enum { A [[maybe_unused]], B [[maybe_unused]] = 42 };` 。

如果编译器对未使用的实体发出警告,那么对于任何被声明为 maybe_unused 的实体,该警告将被抑制。

```C++
[[maybe_unused]] void f([[maybe_unused]] bool thing1,
                        [[maybe_unused]] bool thing2)
{
   [[maybe_unused]] bool b = thing1 && thing2;
   assert(b); // in release mode, assert is compiled out, and b is unused
              // no warning because it is declared [[maybe_unused]]
} // parameters thing1 and thing2 are not used, no warning
```

许多 C/C++ 编译器能帮我们找出「未使用变量」，并产生警告信息，然而，在一些情況下，这些「未使用变量」并不是真的沒用。举例来说，有時候使用这些变量的代码被 `#ifdef` 与 `#endif` 包起來，在特定状态下才会发生作用。例如：

```C++
#include <iostream>

int test(int a, int b, int c) {
    int result = a + b;

#ifdef ENABLE_FEATURE_C
    result += c;
#endif
    return result;
}

int main() {
    std::cout << test(1, 2, 3) << std::endl;
}
```

编译后会产生警告信息。

如果想要关闭警告信息，我们能加上 `[[maybe_unused]]` 属性：

```C++
int test(int a, int b, [[maybe_unused]] int c) {  // Modified
```

> [C++ 17 fallthrough、nodiscard、maybe_unused 屬性](https://zh-blog.logan.tw/2020/07/19/cxx-17-fallthrough-nodiscard-maybe-unused-attribute/)

### 3.标准库头文件 <memory_resource>

> [C++17 的 多态内存分配器 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/359409607)
>
> [标准库头文件 - C++中文 - API 参考文档 (apiref.com)](https://www.apiref.com/cpp-zh/cpp/header/memory_resource.html)

C++ 17 引入了一系列新的内存管理工具, 定义在 header `<memory_resources>` 之中. 其中的东西都在 namespace `std::pmr` 下. pmr 的意思是 polymorphic memory resources.多态的内存分配器。

```c++
class memory_resource;

template<class Tp> class polymorphic_allocator; // Tp 是需要被分配的类型

memory_resource* new_delete_resource() noexcept;
memory_resource* null_memory_resource() noexcept;
memory_resource* set_default_resource(memory_resource* r) noexcept;
memory_resource* get_default_resource() noexcept;

struct pool_options;
class synchronized_pool_resource;
class unsynchronized_pool_resource;
class monotonic_buffer_resource;
```

简单描述一下是做什么的.

1. `memory_resource` 是一个抽象类, 定义了各种接口. 你可以在上面 `allocate` 和 `deallocate`. 可以理解成资源池子, 需要的时候问它要一块资源.
2. 而 `synchronized_pool_resource` , `unsynchronized_pool_resource` , `monotonic_buffer_resource` 就继承了上面这个抽象类, 是三种不同的内存资源.
3. `polymorphic_allocator` 是一个分配器. 可以在指定的内存资源上进行分配. 如果没有给出指定的资源, 那么就会用 `get_default_resource()` 得到一个默认资源.
4. `new_delete_resource()` 会返回一个使用全局 `new` 和全局 `delete` 的 `memory resource*`.
5. `null_memory_resource()` 会返回一个啥也不干的 `memory resource*`.

所以 PMR 使用起来很简单, 创建一个 `memory_resource` , 然后用 `polymorphic_allocator` 在上面进行分配就行了.

### if constexpr

`constexpr if` 是 C++17 引入的一种**条件编译机制**，使得编译器在编译时根据条件选择执行特定的代码分支，而不生成不必要的代码。这在模板编程中非常有用，因为它允许在编译时根据模板参数的特性来选择不同的代码路径，从而避免运行时开销和错误。

`if constexpr` 是 C++17 引入的一种**条件编译机制**，主要用于模板编程中。它的特点是：**条件判断发生在编译期，而不是运行时**。

如果条件为 `true`，编译器会保留 `if` 分支中的代码并忽略 `else` 分支；如果条件为 `false`，则相反。

未被选中的分支不会被编译，因此即使该分支中有语法错误或调用了不适用于某个模板参数的代码，编译器也不会报错。

**基本语法**

```cpp
if constexpr (condition) {
    // 当 condition 为 true 时执行此部分
} else {
    // 当 condition 为 false 时执行此部分
}
```

- `condition` 必须是一个编译时常量表达式（`constexpr`）。

- 只有 `condition` 为 `true` 时，对应的 `if` 分支代码才会被编译，`else` 分支的代码会被完全忽略，反之亦然。
- 不满足条件的代码分支完全不会参与编译，因此即使该分支中的代码存在语法错误或其他问题，也不会影响编译。

**例子**

以下是一个简单的示例，展示了 `constexpr if` 如何用于根据类型选择不同的操作：

```cpp
#include <iostream>
#include <type_traits>

template <typename T>
void print_type_info(T t) {
    if constexpr (std::is_integral_v<T>) {
        std::cout << t << " is an integral type.\n";
    } else if constexpr (std::is_floating_point_v<T>) {
        std::cout << t << " is a floating-point type.\n";
    } else {
        std::cout << t << " is of some other type.\n";
    }
}

int main() {
    print_type_info(42);          // 输出: 42 is an integral type.
    print_type_info(3.14);        // 输出: 3.14 is a floating-point type.
    print_type_info("Hello");     // 输出: Hello is of some other type.
    return 0;
}
```

在上面的例子中：

- `std::is_integral_v<T>` 和 `std::is_floating_point_v<T>` 都是编译时常量表达式，用来判断 `T` 是否为整数类型或浮点类型。
- 通过 `constexpr if`，编译器根据传入参数的类型选择对应的分支代码进行编译和执行。例如，当传入 `42` 时，编译器会选择第一个分支（整数类型）进行编译，而其他分支则被忽略。

**优势**

- **提高编译时优化**：由于不满足条件的代码分支不会被编译，`constexpr if` 可以大大减少编译时和运行时的开销。
- **代码安全性**：可以避免因为未使用的代码分支而引入潜在的错误或未定义行为。
- **提升模板的可读性和可维护性**：通过 `constexpr if`，可以在模板中实现更灵活的类型处理逻辑。

**使用限制**

1. **只能在函数或方法内部使用**

   `if constexpr` 只能出现在函数体内部，包括普通函数、成员函数、lambda 表达式等。这是因为 `if constexpr` 的主要目的是在编译时根据条件选择代码路径，而这些代码路径只能在函数执行期间实际使用。

2. **不能在类的成员变量初始化或全局作用域中使用**

   由于 `if constexpr` 需要在编译时评估，因此它不能直接用于全局作用域，也不能用于类的成员变量初始化表达式中。

   **错误示例：**

   ```cpp
   class MyClass {
       int x = if constexpr (true) { return 1; } else { return 2; };  // 错误：不能在类成员变量初始化时使用
   };
   ```

3. **不能用于模板参数列表中**

   `if constexpr` 不能直接用于模板参数列表或在模板参数列表中使用。

   **错误示例：**

   ```cpp
   template <typename T, if constexpr (std::is_integral<T>::value)>  // 错误：不能在模板参数列表中使用
   void func() {
       // ...
   }
   ```

4. **可以用于函数内部的模板代码**

   `if constexpr` 经常用于模板函数中，以根据模板参数的特性选择不同的代码路径。这是 `if constexpr` 最常见的用途之一。

   **正确示例：**

   ```cpp
   template <typename T>
   void process(T value) {
       if constexpr (std::is_integral_v<T>) {
           std::cout << value << " is an integral type.\n";
       } else {
           std::cout << value << " is not an integral type.\n";
       }
   }
   ```

5. **可以用于 lambda 表达式中**

   `if constexpr` 也可以在 lambda 表达式的主体中使用。

   **正确示例：**

   ```cpp
   auto lambda = [](auto value) {
       if constexpr (std::is_integral_v<decltype(value)>) {
           std::cout << value << " is an integral type.\n";
       } else {
           std::cout << value << " is not an integral type.\n";
       }
   };
   ```

6. **不能用于类成员变量的直接初始化**

   由于 `if constexpr` 是编译时条件，因此它不能用于直接初始化类的成员变量，而应当在构造函数或成员函数内使用。

   **错误示例：**

   ```cpp
   class MyClass {
       int x = if constexpr (true) { return 1; } else { return 0; };  // 错误
   };
   ```

   **正确示例：**

   ```cpp
   class MyClass {
       int x;
   public:
       MyClass() {
           if constexpr (true) {
               x = 1;
           } else {
               x = 0;
           }
       }
   };
   ```

总结

- `if constexpr` 只能用于函数体内部（包括普通函数、成员函数、lambda 表达式）。
- 不能用于全局作用域或类成员变量的直接初始化。
- 不能用于模板参数列表中。

## `C++ 20`

## 开发准则支持库(GSL)

(GSL:Guidelines support library)

C++ 的语法特性实在是太多了，因此实践过程中许多人只选择了 C++ 的一部分语言特性进行开发，从而约定了最佳实践（用什么、怎么用、要不要用）。其中一个著名的规范就是 CCG （C++ Core Guidelines）。为了在开发过程中更好地遵守 CCG 的最佳实践，可以使用 GSL（The Guideline Support Library） 库。

Philosophy.4: Ideally, a program should be statically type safe

- narrowing conversions – minimize their use and use `narrow` or `narrow_cast` (from the GSL) where they are necessary

```c++
int z = gsl::narrow_cast<int>(7.9);  // OK: you asked for it
```

在转化的类型可以容纳时，narrow_cast 可以正常运行，如果 narrow_cast 转化后的值与原值不同时，会抛出 runtime_error 的异常。

## c++ 标准库头文件

> [C++ 标准库](https://zh.cppreference.com/w/cpp/standard_library)
>
> [C++ 标准库头文件](https://c-cpp.com/cpp/header.html)

### [<type_traits>](https://zh.cppreference.com/w/cpp/header/type_traits) C++11

- [underlying_type](https://zh.cppreference.com/w/cpp/types/underlying_type)(C++11)：获取给定枚举类型的底层整数类型
- 1
- 1
- 1
- 1
- 1
- 1
-

# 零碎知识

## 整形提升和寻常算数转换

**整型提升**：

整型提升是 C 程序设计语言中的一项规定：在**表达式计算**时，各种整形首先要提升为 int 类型，如果 int 类型不足以表示则要提升为 unsigned int 类型；然后执行表达式的运算。

一些数据类型（比如 char，short int）比 int 占用更少的字节数，对它们执行操作时，这些数据类型会自动提升为 int 或 unsigned int。

**寻常算术转换**：

许多操作数类型为算术类型的双目运算符会引发转换，并以类似的方式产生结果类型。它的目的的产生一个普通类型，同时也是运算结果的类型。这个模式成为“寻常算术转换”。

如果其中一个操作数类型是 long double，那么另一个操作数也被转换为 long double。其次如果一个操作数的类型是 double，那么另一个操作数也被转换为 double，再次，如果其中一个操作数的类型是 float，那么另一个操作数也被转换为 float。否则两个操作数进行整形升级，执行下面的规则：

如果其中一个操作数的类型是 unsigned long int，那么另一个操作数也被转换成 unsigned long int。其次，如果其中一个操作数类型是 long int，而另一个操作数的类型是 unsigned int，如果 long int 能够完整表示 unsigned int 的所有值，那么 unsigned int 类型操作数操作数被转换为 long int，如果 long int 不能完整表示 unsigned int 的所有值，那么两个操作数都被转换为 unsigned long int。再次，如果一个操作数的类型是 long int，那么另一个操作数被转换为 long int。再再次，如果一个操作数的类型是是 unsigned int，那么另一个操作数被转换为 unsigned int。如果所有以上情况都不属于，那么两个操作数都为 int。

采用通俗语言大意如下：**当执行算术运算时，操作数的类型如果不同，就会发生转换。数据类型一般朝着浮点精度更高、长度更长的方向转换，整型数如果转换为 signed 不会丢失信息，就转换为 signed，否则转换为 unsigned**。

整型提升的意义在于：表达式的整型运算要在 CPU 的相应运算器件内执行，CPU 内整型运算器(ALU)的操作数的字节长度一般就是 int 的字节长度，同时也是 CPU 的通用寄存器的长度。因此，即使两个 char 类型的相加，在 CPU 执行时实际上也要先转换为 CPU 内整型操作数的标准长度。通用 CPU（general-purpose CPU）是难以直接实现两个 8 比特字节直接相加运算（虽然机器指令中可能有这种字节相加指令）。所以，表达式中各种长度可能小于 int 长度的整型值，都必须先转换为 int 或 unsigned int，然后才能送入 CPU 去执行运算。

例如：对精度低于 int 类型的无符号整数进行**位运算**时，编译器会进行整数提升，再对提升后的整数进行位运算，因此要特别注意对于这类无符号整数的位运算，避免出现非预期的结果。

## 命名空间

命名空间(namespace)为防止名字冲突提供了更加可控的机制。命名空间分割了全局命名空间，其中每个命名空间是一个作用域。通过在某个命名空间中定义库的名字，库的作者以及用户可以避免全局名字固有的限制。

命名空间定义：一个命名空间的定义包含两部分：首先是关键字 namespace，随后是命名空间的名字。在命名空间名字后面是一系列由花括号括起来的声明和定义。**只要能出现在全局作用域中的声明就能置于命名空间内**，主要包括：**类、变量(及其初始化操作)、函数(及其定义)、模板和其它命名空间**。命名空间结束后无须分号，这一点与块类似。和其它名字一样，**命名空间的名字也必须在定义它的作用域内保持唯一**。**命名空间既可以定义在全局作用域内，也可以定义在其它命名空间中，但是不能定义在函数或类的内部**。命名空间作用域后面无须分号。

- **每个命名空间都是一个作用域**：命名空间中的每个名字都必须表示该空间内的唯一实体。定义在某个命名空间中的名字可以被该命名**空间内的其它成员直接访问**，也可以被这些成员**内嵌作用域中的任何单位访问**。位于该**命名空间之外**的代码则必须**明确指出**所用的名字属于哪个命名空间。
- **命名空间可以是不连续的**：直观理解是：同一个命名空间出现在多个文件中，但他们仍组成一个命名空间。命名空间可以定义在几个不同的部分，这一点与其它作用域不太一样。命名空间的定义可以不连续的特性使得我们可以**将几个独立的接口和实现文件组成一个命名空间**。此时，命名空间的组织方式类似于我们管理自定义类及函数的方式：命名空间的一部分成员的作用是定义类，以及声明作为类接口的函数及对象，则这些成员应该置于头文件中，这些头文件将被包含在使用了这些成员的文件中。命名空间成员的定义部分则置于另外的源文件中。

- **内联命名空间**：C++11 新标准引入了一种新的嵌套命名空间，称为内联命名空间(inline namespace)。和普通的嵌套命名空间不同，**内联命名空间中的名字可以被外层命名空间直接使用**。也就是说，我们无须在内联命名空间的名字前添加表示该命名空间的前缀，通过外层命名空间的名字就可以直接访问它。定义内联命名空间的方式是在关键字 namespace 前添加关键字 inline。关键字 inline 必须出现在命名空间第一次定义的地方，后续再打开命名空间的时候可以写 inline，也可以不写。当应用程序的代码在一次发布和另一次发布之间发生了改变时，常常会用到内联命名空间。
- **未命名的命名空间**(unnamed namespace)：是指关键字 namespace 后紧跟花括号括起来的一系列声明语句。未命名的命名空间中定义的变量拥有静态生命周期：它们在第一次使用前创建，并且直到程序结束才销毁。
- **using 声明**：一条 using 声明(usingdeclaration)语句一次只引入命名空间的一个成员。它使得我们可以清楚地知道程序中所用的到底是哪个名字。
- **using 指示**(usingdirective)：和 using 声明类似的地方是，我们可以使用命名空间名字的简写形式；和 using 声明不同的地方是，我们无法控制哪些名字是可见的，因为所有名字都是可见的。using 指示以关键字 using 开始，后面是关键字 namespace 以及命名空间的名字。
- **避免 using 指示**：using 指示一次性注入某个命名空间的所有名字，这种用法看似简单实则充满了风险：只使用一条语句就突然将命名空间中所有成员的名字变得可见了。如果应用程序使用了多个不同的库，而这些库中的名字通过 using 指示变得可见，则全局命名空间污染的问题将重新出现。

> [C++/C++11 中命名空间(namespace)的使用](https://www.huaweicloud.com/articles/12620834.html)

## 初始化方式

### 就地初始化

在 C++11 之前，只能对**结构体或类的静态常量成员**进行就地初始化，其他的不行。

```c++
class C {
private:
 static const int a=10; // yes
 int a=10;    // no
}
```

在 C++11 中，**结构体或类的数据成员**在声明时**可以直接赋予一个默认值**，初始化的方式有两种：“等号=” 和 “大括号列表初始化”。

```c++
class C {
private:
    int a=7;  // C++11 only
    int b{7}; // or int b={7}; C++11 only
    int c(7); // error，小括号初始化方式不能用于就地初始化。
};
```

### 就地初始化与初始化列表的先后顺序

C++11 支持了就地初始化非静态数据成员的同时，初始化列表的方式也被保留下来，也就是说既可以使用就地初始化，也可以使用初始化列表来完成数据成员的初始化工作。当二者同时使用时并不冲突，**初始化列表发生在就地初始化之后**，即最终的初始化结果以初始化列表为准。

在 C++11 中，对象初始化拥有多种语法选择：圆括号，等号，花括号：

```C++
int x(0); //用圆括号初始化
int y = 0; //用"="初始化
int z{0}; //用花括号初始化
int z = { 0 };  //用"="和花括号初始化，C++通常把它和“只使用花括号”的情况同样对待。
```

C++ 中指定初始化值的三种方式中，只有花括号能用在每个地方。

花括号初始化有一个新奇的特性，它**阻止在 built-in 类型中的隐式收缩转换**（narrowing conversation）。如果表达式的值不能保证被初始化对象表现出来，代码将无法通过编译。用圆括号和”=“初始化不会检查收缩转换（narrowing conversation）。

```c++
double x, y, z;
...
int sum1{ x + y + z }; //编译错误！double 的和不能表现为 int
int sum2(x + y + z); //可以（表达式的值被截断为 int）
int sum3 = x + y + z; //同上
```

花括号初始化的另外一个值得一谈的特性是它能避免 C++最令人恼火的解析。

初始化经常使用括号，或者是使用大括号，或者是复赋值操作。因为这个原因，c++11 提出了统一初始化，意味着使用这初始化列表，

一个初始化列表强制使用赋值操作， 也就是意味着每个变量都是一个默认的初始化值，被初始化为 0（NULL 或者是 nullptr）。如下：

```c++
int i; //这是一个未定义的行为
int i{}； //i调用默认的构造函数为i赋值为0
int *p； //这是一个未定义的行为
int *p{} ;// p被初始化为一个nullptr
```

### 缩窄转换

C++11 中的列表初始化禁止缩窄转换，关于缩窄转换的规则如下：

```c++
1. 从浮点数转换为整数
vector<int> tmp1 {1.0, 2, 3}; // 从 "double" 到 "int" 进行收缩转换无效

2. 从取值范围大的浮点数转换为取值范围小的浮点数（在编译期可以计算并且不会溢出的表达式除外）
double a = 1.0;
vector<float> tmp2 {1.0f, a, 5}; // 从 "double" 到 "float" 进行收缩转换无效

3. 从整数转换为浮点数（在编译期可以计算并且转换之后值不变的表达式除外）
int b = 1;
vector<float> tmp3 {1.0f, b, 5}; // 从 "int" 到 "float" 进行收缩转换无效

4. 从取值范围大的整数转换为取值范围小的整数（在编译期可以计算并且不会溢出的表达式除外）
int c = 1;
vector<short> tmp3 {1, c, 5}; // 从 "int" 到 "short" 进行收缩转换无效
```

> 如在列表初始化中出现缩窄转换，编译无法通过。

---

## 顶层 const 和 底层 const 理解

首先，const 是一个限定符，被它修饰的变量的值不能改变。

对于**一般的变量**来说，其实**没有**顶层 const 和底层 const 的区别，而只有像**指针**这类复合类型的基本变量，才有这样的区别。

1. 顶层 const：指的是 const 修饰的**变量本身**是一个常量，无法修改，指的是指针，就是 \* 号的右边

2. 底层 const：指的是 const 修饰的变量**所指向的对象**是一个常量，指的是所指变量，就是 \* 号的左边

```c++
int a = 10;
int* const b1 = &a; // 顶层 const，b1 本身是一个常量
const int* b2 = &a; // 底层 const，b2 本身可变，所指向的对象是常量
const int b3 = 20; // 顶层 const，b3 是常量不可变
const int* const b4 = &a; // 前一个 const 为底层，后一个为顶层，b4 不可变
const int& b5 = a; // 用于声明引用变量，都是底层 const
```

区分作用：

1. 执行对象拷贝时有限制，常量的底层 const 不能赋值给非常量的底层 const
2. 使用命名的强制类型转换函数 const_cast 时，只能改变运算对象的底层 const

Tips:

1. 用于声明引用的 const 都是**底层 const**。

2. const 成员函数本质上是修饰 this 指针，成员变量引用会被看成常量指针的。

3. **const 的引用(reference to const)**对于引用对象本身是否是一个常量没有做出限定，因此对象也可能是个非常量，允许通过其他途径改变它的值。

4. **指向常量的指针**也没有规定其所指的对象必须是一个常量，所谓指向常量**仅仅要求不能通过该指针修改所指向对象的值**，而**没有规定所指对象的值不能通过其他途径改变**。

5. 可以定义**指向指针的引用**：

   ```c++
   int *&x;
   ```

   作用：指针的引用就是指针的别名，可以用这个别名全局地修改指针，类比变量的引用。否则就需要用指针的指针。

> [Difference between const int*, const int * const, and int const \*](https://www.geeksforgeeks.org/difference-between-const-int-const-int-const-and-int-const/)
>
> ![](https://media.geeksforgeeks.org/wp-content/cdn-uploads/PointersWithConstants-1024x535.png)

## 左值引用和右值引用

右值引用完成两个功能：

1. 实现 move 语义
2. 完美转发

## new 方法

stl_placement_new

## 类型转换

[C++标准转换运算符 reinterpret_cast](https://www.cnblogs.com/ider/archive/2011/07/30/cpp_cast_operator_part3.html)

reinterpret_cast 运算符是用来处理无关类型之间的转换；它会产生一个新的值，这个值会有与原始参数（expressoin）有完全相同的比特位。

所以总结来说：reinterpret_cast 用在任意指针（或引用）类型之间的转换；以及指针与足够大的整数类型之间的转换；从整数类型（包括枚举类型）到指针类型，无视大小。

（所谓"足够大的整数类型",取决于操作系统的参数，如果是 32 位的操作系统，就需要整形（int）以上的；如果是 64 位的操作系统，则至少需要长整形（long）。具体大小可以通过 sizeof 运算符来查看）。

## 变量声明

> 参考：《C++ Pirmer 第五版》ch2

### 基本数据类型和声明符

一条声明语句由**一个基本数据类型**(base type)和紧随其后的**一组声明符**(declarator)组成。每个声明符命名了一个变量并指定该变量为与基本数据类型有关的某种类型（ch2.3.3）。

```cpp
int ival = 1024;
int &refVal = ival; // 引用：refVal 指向 ival (是ival的另一个名宇）
int *pi = ＆ival;   // 指针：pi 存放变量 ival 的地址，或者说 pi 是指向变量 ival 的指针
int **ppi = &pi;    // 指向指针的指针：ppi 指向一个 int 型的指针
int *&r = pi;       // 指向指针的引用：r 是个对指针 pi 的引用
```

> - 很多程序员容易迷惑于基本数据类型和类型修饰符的关系，其实后者不过是**声明符的一部分**罢了。
> - 面对一条比较复杂的指针或引用的声明语句时，**从右向左阅读**有助于弄清楚它的真实含义。

### 别名声明

如下类型别名声明（ch2.5.1）：

```cpp
typedef char *pstring;   // 类型 pstring，实际上是类型 char＊ 的别名
const pstring cstr = 0;  // cstr 是指向 char 的常量指针
const pstring *ps;       // ps 是一个指针， 它的对象是指向 char 的常量指针

const char *cstr = 0; // 是对 const pstring cstr = 0; 的错误理解。
```

上述两条声明语句的基本数据类型都是 const pstring, 和过去一样， const 是对给定类型的修饰。pstring 实际上是指向 char 的指针，因此 const pstring 就是指向 char 的常量指针， 而非指向常量字符的指针。

分析类型别名的声明语句时，人们往往会错误地尝试把类型别名替换成它本来的样子，**这种理解是错误的**。

声明语句中用到 pstring 时，其基本数据类型是指针。可是用 char＊ 重写了声明语句后， 数据类型就变成了 char, ＊成为了声明符的一部分。这样改写的结果是，const char 成了基本数据类型。前后两种声明含义截然不同， 前者声明了一个指向 char 的常量指针，改写后的形式则声明了一个指向 constchar 的指针。

### 定义多个变量

要在一条语句中定义多个变量， 切记， 符号 `＆` 和 `＊` 只从属于某个声明符， 而非基本数据类型的一部分， 因此初始值必须是同一种类型：

```cpp
int* pl, p2;            // pl 是指向 int 的指针，p2是 int。基本数据类型是 int 而非 int＊

int i = 0;
const int ci = i;
auto k = ci, &l = i;    // k 是整数，l 是整型引用
auto &m = ci, *p = &ci; // m 是对整型常量的引用，p 是指向整型常量的指针
// 错误： i 的类型是 int，而 ＆ci 的类型是 const int
auto &n = i, *p2 = &ci;
```

## C++ 说明符和限定符

> [C++ 说明符和限定符](https://zhuanlan.zhihu.com/p/645909785)

在 C++中，说明符（Specifier）和限定符（Qualifier）用于修饰数据类型、函数、变量等，以改变其行为或提供额外的信息。它们是编程语言中的关键字或关键字组合。下面是一些常见的 C++ 说明符和限定符：

数据类型说明符：

1. 基本内置类型：
   C++ 定义了一套包括算术类型(arithmetic type)和空类型(void)在内的基本数据类型。其中算术类型包含了字符、整型数、布尔值和浮点数。

   - 算数类型
     算术类型分为两类：整型（含字符和布尔类型）和浮点型。C++ 标准规定了尺寸的最小值，同时允许编译器赋予这些类型更大的尺寸。
     - bool: 布尔类型，用于声明布尔值（true 或 false）变量。
     - char: 字符类型，用于声明单个字符变量。
     - int 等: 整数类型，用于声明整数变量。
     - float: 单精度浮点数类型，类似于 double 但存储空间较小。
     - double: 双精度浮点数类型，用于声明带有小数点的浮点数变量。
   - 空类型
     - void: 空类型，用于表示没有返回值的函数或空指针。

2. 复合类型
   复合类型(compound type)是指基于其他类型定义的类型。C++ 语言有几种复合类型，其中两种为：引用和指针，它们的声明需要用到类型修饰符 `*` 和 `&`。

存储类说明符：

- auto: 自动类型推断，编译器根据初始化表达式自动推断变量的类型。
- static: 静态存储类，使得局部变量在程序生命周期内保持其值，且只初始化一次。
- extern: 外部存储类，用于声明全局变量，并表示该变量在其他文件中定义。
- register: 寄存器存储类，用于请求将变量存储在寄存器中，以便更快地访问。
- mutable: 用于修饰类的成员变量，允许在 const 成员函数中修改这些变量。

限定符：

- const: 用于声明常量，表示该变量的值在初始化后不能被修改。

- volatile: 用于声明易变的变量，告诉编译器不要进行优化，因为变量的值可能会在意料之外的情况下改变（如中断）。

- restrict（C99 标准新增）：用于告知编译器，该指针是访问对象的唯一且初始的方式，从而进行优化。

  在保证多个指针所指向的区域无交叠的前提下，可以将这些指针加上 restrict 限定符，用于指导编译器做出更激进的优化。

访问限定符：

- public: 在类中指定公共成员，可以在类的内部和外部访问。
- private: 在类中指定私有成员，只能在类的内部访问。
- protected: 在类中指定受保护成员，可以在类的内部和派生类中访问。

这些说明符和限定符提供了更多的灵活性和控制，帮助开发者在 C++中编写更有效、安全和可维护的代码。

在 C++11 中引入了 thread_local 关键字，它是一个存储类说明符，用于声明线程局部存储的变量。这使得变量的值在每个线程中都有一份独立的副本，而不是像普通变量那样在所有线程之间共享。

非类型描述符放在类型描述符的左边，更符合阅读习惯。

```c++
int static i; // 不符合
void virtual Fun(); // 不符合

static int i; // 符合：static 放在 int 左边
virtual void Fun(); // 符合：virtual 放在 void 左边
```

> 不限制多个非类型描述符的书写顺序，可参考如下顺序书写：
>
> - friend / typedef /存储类型说明符（ static 、extern 、thread_local 、mutable
>   等）/ virtual
> - inline
> - constexpr
> - explicit 说明符

## restrict 关键字

restrict 关键字是 C 语言中的一种类型限定符（Type Qualifiers），只用于限定指针，该关键字用于告诉编译器，所有修改该指针指向内容的操作，**全部是基于该指针的，即不存在其他修改操作的途径**，消除 pointer aliasing（指针别名），从而帮助编译器**生成更优的机器码**。在保证多个指针所指向的区域无交叠的前提下，可以将这些指针加上 restrict 限定符，用于指导编译器做出更激进的优化。

需要特别**注意**的是，如果指针指向同一块区域而错误的加上了 restrict 限定符，则结果是未定义的。

这个指针有两个作用，一个是告诉编译器，编译器一旦获得了这个信息，那么就可以放心大胆地对这个进行优化。另一个作用是告诉程序员，这段内存只能通过这个指针访问。

- 作用一： 告诉编译器，编译器可以根据这个大胆做优化

```cpp
int add(int *a, int *b){
  *a = 10;
  *b = 12;
  return *a + *b;
}
```

在这个函数中，有的同学就说了，直接返回 22 不就好了，这么想的同学就**忽略了 a==b 的可能**，如果 a 和 b 指向同一个地址，那么这个函数将返回 24。实际上，编译器就是这个想要把额外操作去掉的“同学”，如果我们能清晰的告诉他，a 和 b 在本函数中不管怎么移动都永远不可能指向相同的地址，那么，处理这个函数时，*a +*b 可以直接使用两立即数相加，不需要再从地址中读取值，就能优化代码执行的效率。**因此，在没有指明 a 不可能等于 b 的情况下，编译器能做到的最大优化就是，b 指向地址的值一定是 12，但 a 的值必须从地址中读取**。

```cpp
int add(int __restrict *a, int __restrict *b){
  *a = 10;
  *b = 12;
  return *a + *b;
}
```

- 作用二：告诉程序员，这段内存需要满足 restrict 规则

C 库中有两个函数可以从一个位置把字节复制到另一个位置。在 C99 标准下，它们的原型如下：

```cpp
void * memcpy（void * restrict s1, const void * restrict s2, size_t n);
void * memmove(void * s1, const void * s2, size_t n);
```

这两个函数均从 s2 指向的位置复制 n 字节数据到 s1 指向的位置，且均返回 s1 的值。两者之间的差别由关键字 restrict 造成，即 **memcpy 函数内部可以假定两个内存区域没有重叠，但是需要使用者来保证**，如果没有按照规则，则内部的实现如果没有考虑重叠的情况，就可能出问题。**memmove() 函数则不做这个假定**，因此，复制过程类似于首先将所有字节复制到一个临时缓冲区，然后再复制到最终目的地。同样，编译器并不会对这个做检测，你告诉编译器什么，编译器就相信什么了。

```cpp
void test()
{
    char *ptr = (char*)malloc(10);
    char *tmp = ptr + 3;
    memset(ptr, '\0', 10);
    snprintf(ptr, 10, "%s", "HelloWorld");
    memcpy(tmp, ptr, 5);
}
```

如上面的代码，tmp 初始指向字符 "I"，按照本意，我们是想把从 ptr 开始的 5 个字符 "Hello" 复制到从 tmp 开始的地址上。那么如果 memcpy 没有考虑地址重叠的话，它会从 ptr 开始把字符一个一个拷贝到 tmp 地址上。那么你就会发现，当把第一个字符 "H" 拷贝到 tmp 指向 "I" 的位置的时候，被拷贝的 5 个字符已经变成“HelHo"了，也就是改 dst 的同时，也改到了 src 了。那这样起来肯定会违背我们的本意，但是这个不是 memcpy 的锅，人家已经通过 restrict 告诉你 s2 这块地址只有限定在只能通过 s2 指针来访问才能保证没问题，是你自己没按照函数规则来。

这也告诉我们，**在设计 memcpy 的时候，需要考虑内存重叠的情况**。解决办法如下，当修改 dst 也有可能改到 src 的情况下，可以把 src 和 dst 均加上要拷贝的 size，然后从尾巴开始逐一字符拷贝，这样就不会有重叠了。

## POD 数据类型

> [**对 POD 定义的修正**](https://zh.wikipedia.org/wiki/C%2B%2B11)

在**C++03**中，一个类（class）或结构（struct）要想被作为[POD](<https://zh.wikipedia.org/wiki/POD_(程序设计)>)，必须遵守几条规则。符合这种定义的类别**能够产生与 C 兼容的对象内存布局（object layout），而且可以被静态初始化**。但 C++03 标准严格限制了何种类型与 C 兼容或可以被静态初始化的，尽管并不存在技术原因导致编译器无法处理。如果创建一个 C++03 POD 类型，然后为其添加一个非虚成员函数，这个类型就不再是 POD 类型了，从而无法被静态初始化，也不再与 C 兼容，尽管其内存布局并没有发生变化。

**C++11**通过把 POD 概念划分成两个概念：**_平凡的（trivial）_**和**标准布局*（standard-layout）***，**放宽**了关于 POD 的定义。

### Trivial 类型

根据 C++标准，一个类型 T 是 Trivial 的，如果它满足以下所有条件：

a) 是一个标量类型（scalar type），或
b) 是一个 trivial 类，满足：

- 有一个 trivial 默认构造函数
- 有 trivial 复制构造函数和移动构造函数
- 有 trivial 复制赋值运算符和移动赋值运算符
- 有一个 trivial 析构函数
- 所有非静态数据成员都是 trivial 类型

其中：

- Trivial 默认构造函数：要么是隐式定义的，要么是用户提供的并且等同于隐式定义的（使用 = default，或者空函数体什么都不做）
- Trivial 复制/移动构造函数：要么是隐式定义的，要么是用户提供的并且等同于隐式定义的
- Trivial 复制/移动赋值运算符：要么是隐式定义的，要么是用户提供的并且等同于隐式定义的
- Trivial 析构函数：非虚的，并且基类的析构函数也是 trivial 的

如果一个类或结构体满足上述所有条件，那么它就是一个平凡的类型。**平凡类型可以通过简单的内存复制操作来创建或销毁**（例如，通过 `memcpy` 或 `memset`），这在某些情况下能提高性能。

### Standard-layout 类型

一个类型 T 是 Standard-layout 的，如果它满足以下所有条件：

a) 是一个标量类型，或
b) 是一个 standard-layout 类，满足：

- **所有非静态数据成员都具有相同的访问控制（public、protected 或 private）**

  解释：这确保了所有成员在内存中的连续性，没有因为不同的访问级别而导致的潜在填充或重排。

  ```cpp
  struct Good {
      int a;
      double b;
      char c;
  }; // 全部是public，符合条件

  class Bad {
  public:
      int a;
  private:
      double b; // 不同的访问说明符，不符合条件
  };
  ```

- **没有虚函数和虚基类**

  解释：虚函数和虚基类会引入虚函数表指针（vptr）或虚基类表指针，这会改变对象的内存布局。

  ```cpp
  struct Good {
      void foo() {}
  }; // 没有虚函数，符合条件

  struct Bad {
      virtual void foo() {} // 虚函数，不符合条件
  };
  ```

- **所有非静态数据成员，包括在其所有基类中的，都是 standard-layout 类型**

  解释：这确保了整个类的内存布局是可预测的，因为所有成员都遵循 standard-layout 规则

  ```cpp
  struct StandardLayoutMember {};

  struct Good {
      int a;
      StandardLayoutMember b;
  }; // 所有成员都是standard-layout，符合条件

  struct NonStandardLayoutMember {
      virtual void foo() {}
  };

  struct Bad {
      int a;
      NonStandardLayoutMember b; // 成员不是standard-layout，不符合条件
  };
  ```

- **类中第一个非静态数据成员的类型与其任何基类的类型都不同**

  解释：这防止了由于基类和第一个成员类型相同可能导致的歧义或复杂性。// 例如：`struct A:B { B b; int c; }`不符合要求

  ```cpp
  struct Base {};

  struct Good : Base {
      int first; // 第一个成员类型与基类不同，符合条件
  };

  struct Bad : Base {
      Base first; // 第一个成员类型与基类相同，不符合条件
  };
  ```

- **没有两个基类有<font color=red>相同类型</font>的非静态数据成员**

  解释：这避免了多重继承时可能出现的成员重叠问题。// 例如两个基类都有 int 类型成员，不符合条件

  ```cpp
  struct Base1 { int x; };
  struct Base2 { double y; };

  struct Good : Base1, Base2 {}; // 基类成员类型不同，符合条件

  struct Base3 { int z; };
  struct Bad : Base1, Base3 {}; // 两个基类都有int类型成员，不符合条件
  ```

- **没有基类与第一个定义非静态数据成员的类共享公共初始序列**

  解释：这避免了因共享初始序列而可能导致的内存布局复杂性。

  ```cpp
  struct Base { int x; };
  struct Good : Base { double y; }; // 符合条件

  struct Derived : Base { int y; }; // 不符合条件，与Base共享初始序列
  ```

  > 共享公共初始序列（Common Initial Sequence）指的是在继承关系中，基类和派生类**开始部分**的非静态数据成员序列相同的情况。
  >
  > 关键点：
  >
  > - 只考虑非静态数据成员。
  > - 成员的顺序和类型必须完全匹配。
  > - 这个序列从第一个成员开始，直到遇到不同类型的成员或其中一个类型的成员结束
  >
  > 这条规则主要影响那些需要精确控制内存布局的场景，比如：**与 C 语言接口交互**、**序列化和反序列化**、**底层系统编程**、**某些性能敏感的应用**

- **最多只有一个类（包括所有基类）有<font color=red>非静态</font>数据成员**

  解释：这简化了内存布局，确保所有数据成员都在一个连续的内存块中。

  ```cpp
  struct Base {};
  struct Good : Base { int x; double y; }; // 只有一个类有非静态成员，符合条件

  struct Base2 { int z; };
  struct Bad : Base2 { double w; }; // 基类和派生类都有非静态成员，不符合条件
  ```

- **一个类不能同时满足以下所有条件：**

  - **继承自一个只有静态成员的类**
  - **继承自至少一个非空的类**
  - **自身拥有非静态数据成员**

  解释：这条规则防止了可能导致内存布局复杂化的特殊继承情况。特别是，它防止了在继承层次中混合使用空基类优化（Empty Base Optimization，EBO）和非空基类，同时还添加自己的成员，这可能会导致意外的内存布局。

  ```cpp
  struct StaticOnly { static int x; };
  struct Good1 : StaticOnly { int y; }; // 符合条件
  struct Good2 { int z; };

  struct Bad : StaticOnly, Good2 { double w; }; // 不符合条件，1继承自只有静态成员的类，2继承自一个非空类，3自身有非静态数据成员
  ```

### POD (Plain Old Data) 类型

在 C++11 之前，POD 是一个统一的概念。但在 C++11 及以后，POD 的概念被分解为两个独立的概念：trivial 和 standard-layout。

一个类型是 POD，当且仅当它**同时满足以下两个条件**：

- 是一个 trivial 类型
- 是一个 standard-layout 类型

C++标准库提供了 type traits 来检查这些属性：

```cpp
#include <type_traits>

static_assert(std::is_trivial<TrivialType>::value, "Not trivial");
static_assert(std::is_standard_layout<StandardLayoutType>::value, "Not standard layout");
std::is_pod<T>::value  // C++20前
```

注意：`std::is_pod` 在 C++20 中被废弃，因为 Trivial 和 Standard-layout 的概念已经足够精确地描述了 POD 的特性。

### 总结

- **Trivial** 类型强调的是类型行为的简单性和高效性。
- **Standard-layout** 类型强调的是类型的内存布局与 C 语言的兼容性。

这两个属性并不是互斥的，一个类型可以同时是 Trivial 和 Standard-layout 类型。

## 经典宏用法收集

```cpp
#define max(a,b)    (((a) > (b)) ? (a) : (b))

#define min(a,b)    (((a) < (b)) ? (a) : (b))

#define ARRAY_SIZE(array) (sizeof(array)/sizeof(array[0]))

#define offset_of(type, member)    ((VOS_UINT32)(&((type *)0)->member))

#define abs(a, b) (((a) > (b))? ((a) - (b)) : ((b) - (a)))
```

## c++ 给无名形参提供默认值

> <https://blog.csdn.net/zhangzhangkeji/article/details/132005953>

如上图，若函数的形参不在函数体里使用，可以不提供形参名，而且可以给此形参提供默认值。也能编译通过。
在看 vs2019 上的源码时，也出现了这种写法。应用 SFINAE（substitute false is not an error）原则，若没推断出形参类型，也不报错，若推断出形参类型，则为其提供默认值。

google：c++模板 无名参数默认赋值

[C++模板 匿名类型参数](https://www.jianshu.com/p/3deec1ac6430)
