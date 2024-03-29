[toc]

# `C++ 11/14/17/20 新特性总结`

## `C++11`

### 1. constexpr

`constexpr` 是 C++ 11 中新增加的用于**指示常量表达式**的关键字。在此之前（C++ 98/03标准）只有 `const` 关键字，其在实际使用中经常会表现出**两种不同的语义**。举个例子：







总的来说在 C++ 11 标准中，`const` 用于为修饰的变量添加“只读”属性；而 `constexpr` 关键字则用于指明其后是一个常量（或者常量表达式），编译器在编译程序时可以顺带将其结果计算出来，而无需等到程序运行阶段，这样的优化极大地**提高了程序的执行效率**。

### 2. 自动推导 atuo 和 decltype

auto 和 decltype 是在 C++11 中新增的类型推导方法，它可以让程序员不再需要手工编写变量的类型。

#### **auto**

在 **《Effective Modern C++》** 这本书中，**Scott Meyers** 将 **auto** 的类型推导规则划分为了3种场景，并对每种场景依次介绍了其推导方式[1]：

##### 场景1：声明的变量类型是引用或者指针，但不是转发引用

在这种场景下，按照以下方式推导：

1. 如果初始化表达式是引用类型，先忽略引用部分；
2. 将初始化表达式的类型作为**auto**占位的类型。

```c++
int x = 27;
const int cx = x;
const int& rx = x;
 
auto& a = x;  // a被推导为int&
auto& b = cx;  // b被推导为const int&
auto& c = rx;  // c被推导为const int&
```

对变量 b 来说，其初始化表达式 cx 的类型是 const int，用 const int 替换 auto 占位符，得到 b 的类型是 const int&。

对变量 c 来说，其初始化表达式 rx 的类型是 const int&，这时要先应用步骤1，把引用去掉，变为 const int，之后的推导和 b 一样。

场景1还有一个变体：当声明的变量是 **const** 引用或指针时，推导过程大致相同，但是这个时候，初始化表达式的 **const** 属性不再需要作为 **auto** 占位符的一部分：

```c++
int x = 27;
const int cx = x;
const int& rx = x; 

const auto& a = x;  // a被推导为const int&
const auto& b = cx;  // b被推导为const int&
const auto& c = rx;  // c被推导为const int&
```

这里的 b 和 c 在推导时，由于声明的类型已经带有 const，因此 auto 占位符只需要被替换为 int，得到 const int& 类型。

##### 场景2：声明的变量类型是转发引用

在这种场景下，变量类型的推导大体遵循以下规则：

1. 如果初始化表达式的类型是左值，变量被推导为左值引用类型；
2. 如果初始化表达式的类型是右值，推导方式同场景1。

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

转发引用的推导背后还有引用折叠的原理，需要了解相关知识的，可以阅读《Effective Modern C++》的Item24~Item28。

##### 场景3：声明的变量类型既不是引用也不是指针

在这种场景下，按照以下方式推导：

1. 如果初始化表达式是引用类型，忽略引用部分（和场景1一样）；
2. 如果初始化表达式带有const或volatile属性，同样忽略。

```C++
int x = 27;
const int cx = x;
const int& rx = x;
 
auto a = x;  // a被推导为int
auto b = cx;  // b被推导为int
auto c = rx;  // c被推导为int
```

在这个场景下，推导出的类型不会是引用类型，它往往会导致非预期的拷贝（或者移动）。

#### **decltype**

**decltype** 的推导规则比**auto**要简单得多： 它几乎总是得到其内部表达式的原始类型。

需要注意的是，**decltype** 并不对其内部的表达式真正求值（这和 **sizeof** 很像），因此 **decltype(Foo())** 不会真的去调用 **Foo()**，只是推导出 **Foo** 的返回值类型 **const A&**。

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
3. mutable指示符：用来说用是否可以修改捕获的变量
4. exception：异常设定
5. return type：返回类型
6. function body：函数体

**捕获列表** 

- []：默认**不捕获**任何变量；

- [=]：默认**以值捕获**所有变量；

- [&]：默认**以引用捕获**所有变量；

- [x]：仅以值捕获x，其它变量不捕获，捕获多个变量用 "," 分隔；

- [&x]：仅以引用捕获x，其它变量不捕获；

- [=, &x]：默认以值捕获所有变量，但是x是例外，通过引用捕获；

- [&, x]：默认以引用捕获所有变量，但是x是例外，通过值捕获；

- [this]：通过引用捕获当前对象（其实是复制指针）；

- [*this]：通过传值方式捕获当前对象；没有[&this]

  > C++11/14/17/20 的捕获行为有差异

**修改捕获变量** 
在Lambda表达式中，如果以传值方式捕获外部变量，则函数体中不能修改该外部变量，否则会引发编译错误。那么有没有办法可以修改值捕获的外部变量呢？这是就需要使用mutable关键字，该关键字用以说明**表达式体内的代码可以修改值捕获的变量**。

**Lambda 表达式的参数** 
Lambda 表达式的参数和普通函数的参数类似，但有区别。在 **Lambda 表达式中传递参数限制**如下：

1. 参数列表中不能有默认参数
2. 不支持可变参数
3. 所有参数必须有参数名



### 4. 强类型枚举

C++11 引入了语法为 `enum class` 的强类型枚举。 它们与整数类型不兼容，并且需要显式转换以获取其数值。 C++11 还引入了以 `enum name : type {}` 形式为弱类型枚举指定存储类的功能。 



### 5. for_each





### 6. 基于范围的 for 循环

C++11 中引入了 for_each 循环的语言特性（自动确定循环范围），使用这个特性能够非常方便快捷的对**「普通数组 / STL 容器」**中的元素进行遍历，而不必再关心和计算他们的的界限。

```C++
int num[5] = {1, 2, 3, 4, 5};    
for (auto x : num) {
   cout << x << endl; 
}
```

上面`for`述句的第一部分定义被用来做范围迭代的变量，就像被声明在一般for循环的变量一样，其作用域仅只于循环的范围。而在":"之后的第二区块，代表将被迭代的范围。

这种for语句还可以用于**C型数组**，**初始化列表**，和任何定义了`begin()`和`end()`来回返**首尾迭代器的类型**。

**基于范围for循环使用细节：** 

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

> 1. 基于范围的for循环和普通的for循环一样，在遍历的过程中如果修改容器，会造成迭代器失效，（有关迭代器失效的问题请参阅C++ primer这本书，写的很详细）
> 2. 注意：如果数组（集合）的大小（范围）在编译期间不能确定，那么不能够使用基于范围的 for 循环。



### 7. static_assert

C++11 中引入了 `static_assert` 这个关键字，用来做**编译期间的断言**，因此叫做静态断言。

语法： `static_assert(常量表达式，提示字符串)`; 

如果“常量表达式”的值为真( true 或者非零值)，那么 static_assert 不做任何事情，否则会产生一条编译错误，错误位置就是该 static_assert 语句所在行，错误提示就是“提示字符串”。

static_assert 的特点：

* 使用范围：可以用在全局作用域，命名空间、类或函数的作用域中

* 常量表达式的结果必须是在编译时期可以计算的表达式，即必须是常量表达式

* 可检查模板参数

* 编译期间断言，不生成目标代码，不会产生任何运行期性能开销

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

**使用join()** 
我们知道, 上例中如果主线程 (main) 先退出, 那些还未完成任务的线程将得不到执行机会, 因为 main 会在执行完调用 exit(), 然后整个进程就结束了, 那它的"子线程" (我们知道线程是平级的, 这里只是, 形象一点) 自然也就 over 了。
所以就像上例中, 线程对象调用 join() 函数, **join() 会阻塞当前线程**, 直到线程函数执行结束, 如果线程有返回值, 会被忽略。

**使用 detach()** 
对比于 join(), 我们肯定有**不想阻塞当前线程的时候, 这时可以调用 detach(**), 这个函数会分离线程对象和线程函数, 让线程作为后台线程去执行, 当前线程也不会被阻塞了, 但是分离之后, 也不能再和线程发生联系了, 例如不能再调用 get_id() 来获取线程 id 了, 或者调用 join() 都是不行的, 同时也无法控制线程何时结束。程序终止后, 不会等待在后台执行的其余分离线程, 而是将他们挂起, 并且本地对象被破坏。

**警惕作用域**  

`std::thread` 出了作用域之后就会被析构, 这时如果线程函数还没有执行完就会发生错误, 因此, 要注意**保证线程函数的生命周期在线程变量之内**。

**线程不能复制** 

**`std::thread` 不能复制, 但是可以移动**
也就是说, 不能对线程进行复制构造, 复制赋值, 但是可以移动构造, 移动赋值



> 使用C++11进行多线程开发 (std::thread)：https://blog.csdn.net/weixin_36888577/article/details/82891531



### 9. alignof alignas 说明符

> [alignof 运算符(C++11 起)](https://zh.cppreference.com/w/cpp/language/alignof)

查询类型的对齐要求。

语法：

```C++
alignof(类型标识)		
```

[返回std::size_t](https://en.cppreference.com/w/cpp/types/size_t)类型的值。

解释

返回由[类型标识](https://zh.cppreference.com/w/cpp/language/type#.E7.B1.BB.E5.9E.8B.E7.9A.84.E5.91.BD.E5.90.8D)所指示的类型的任何实例所要求的[对齐](https://zh.cppreference.com/w/cpp/language/object#.E5.AF.B9.E9.BD.90)字节数，该类型可以是[完整](https://zh.cppreference.com/w/cpp/language/type#.E4.B8.8D.E5.AE.8C.E6.95.B4.E7.B1.BB.E5.9E.8B)对象类型、元素类型完整的数组类型或者到这些类型之一的引用类型。

如果类型是引用类型，那么运算符返回*被引用*类型的对齐要求；如果类型是数组类型，那么返回元素类型的对齐要求。





> [alignas 说明符 (C++11 起)](https://www.apiref.com/cpp-zh/cpp/language/alignas.html)
>
> [alignas用法](https://juejin.cn/s/alignas%E7%94%A8%E6%B3%95)

`alignas` 是一个 C++11 中的关键字，用于指定变量、结构体、联合体、类等对象的对齐方式。它可以用来控制数据的内存对齐，以优化内存的访问速度。

`alignas` 的使用方法如下：

```scss
scss
复制代码alignas(n) type variable;
```

其中，`n` 是对齐要求的字节数，必须是 2 的幂次方，`type` 是变量的数据类型，`variable` 是变量名。

`alignas` 的作用是让变量在内存中按照指定的对齐方式分配内存。例如：

```scss
scss复制代码alignas(16) int a; // 按照 16 字节对齐
alignas(32) char b; // 按照 32 字节对齐
```

在这个例子中，变量 `a` 按照 16 字节对齐，变量 `b` 按照 32 字节对齐。

需要注意的是，如果指定的对齐值比默认对齐值更小，则指定的对齐值会被忽略。例如：

```c
c复制代码struct alignas(4) A {
  char c;
  int i;
};

sizeof(A) // 结果为 8，而不是 6
```

在这个例子中，`A` 结构体的对齐方式为 4 字节，但是由于默认对齐值是 8 字节，所以实际上 `A` 结构体的大小是 8 字节。

总之，`alignas` 可以用来控制数据的内存对齐方式，以优化内存访问速度。但是需要注意，如果指定的对齐值比默认对齐值更小，则指定的对齐值会被忽略。



## `C++ 14`

### 1. std::make_unique<T>()

从 C++14 开始，有一个库函数 make_unique<T>() 可用于创建 unique_ptr 对象。该函数分配一个类型为 T 的对象，然后返回一个拥有该对象的独占指针。例如，来看下面的代码：

```c++
unique_ptr<int> uptr(new int);	// 可以弃用此代码
unique_ptr<int> uptr = make_unique<int>();	// 改为使用此代码
```





## `C++ 17`

### 1. std::optional

有时我们会用一个值来表示一种“没有什么意义”的状态，这就是C++17的std::optional的用处。



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

如果编译器对未使用的实体发出警告,那么对于任何被声明为maybe_unused的实体,该警告将被抑制。

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
> [标准库头文件  - C++中文 - API参考文档 (apiref.com)](https://www.apiref.com/cpp-zh/cpp/header/memory_resource.html)

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





## `C++ 20`









## 开发准则支持库(GSL)

(GSL:Guidelines support library)

C++ 的语法特性实在是太多了，因此实践过程中许多人只选择了 C++ 的一部分语言特性进行开发，从而约定了最佳实践（用什么、怎么用、要不要用）。其中一个著名的规范就是CCG （C++ Core Guidelines）。为了在开发过程中更好地遵守 CCG 的最佳实践，可以使用 GSL（The Guideline Support Library） 库。

Philosophy.4: Ideally, a program should be statically type safe

- narrowing conversions – minimize their use and use `narrow` or `narrow_cast` (from the GSL) where they are necessary

```c++
int z = gsl::narrow_cast<int>(7.9);  // OK: you asked for it
```

在转化的类型可以容纳时，narrow_cast可以正常运行，如果narrow_cast转化后的值与原值不同时，会抛出runtime_error的异常。











# 零碎知识

## 1. 整形提升和寻常算数转换

**整型提升**：

整型提升是 C 程序设计语言中的一项规定：在**表达式计算**时，各种整形首先要提升为 int 类型，如果 int 类型不足以表示则要提升为 unsigned int 类型；然后执行表达式的运算。

一些数据类型（比如char，short int）比int占用更少的字节数，对它们执行操作时，这些数据类型会自动提升为int或unsigned int。

**寻常算术转换**：

许多操作数类型为算术类型的双目运算符会引发转换，并以类似的方式产生结果类型。它的目的的产生一个普通类型，同时也是运算结果的类型。这个模式成为“寻常算术转换”。

 如果其中一个操作数类型是long double，那么另一个操作数也被转换为long double。其次如果一个操作数的类型是double，那么另一个操作数也被转换为double，再次，如果其中一个操作数的类型是float，那么另一个操作数也被转换为float。否则两个操作数进行整形升级，执行下面的规则：

如果其中一个操作数的类型是unsigned long int，那么另一个操作数也被转换成unsigned long int。其次，如果其中一个操作数类型是long int，而另一个操作数的类型是unsigned int，如果long int能够完整表示unsigned int的所有值，那么unsigned int 类型操作数操作数被转换为long int，如果long int 不能完整表示unsigned int的所有值，那么两个操作数都被转换为unsigned long int。再次，如果一个操作数的类型是long int，那么另一个操作数被转换为long int。再再次，如果一个操作数的类型是是unsigned int，那么另一个操作数被转换为unsigned int。如果所有以上情况都不属于，那么两个操作数都为int。

采用通俗语言大意如下：**当执行算术运算时，操作数的类型如果不同，就会发生转换。数据类型一般朝着浮点精度更高、长度更长的方向转换，整型数如果转换为signed不会丢失信息，就转换为signed，否则转换为unsigned**。

整型提升的意义在于：表达式的整型运算要在 CPU 的相应运算器件内执行，CPU 内整型运算器(ALU)的操作数的字节长度一般就是 int 的字节长度，同时也是 CPU 的通用寄存器的长度。因此，即使两个 char 类型的相加，在 CPU 执行时实际上也要先转换为 CPU 内整型操作数的标准长度。通用 CPU（general-purpose CPU）是难以直接实现两个8比特字节直接相加运算（虽然机器指令中可能有这种字节相加指令）。所以，表达式中各种长度可能小于 int 长度的整型值，都必须先转换为 int 或 unsigned int，然后才能送入 CPU 去执行运算。

例如：对精度低于int类型的无符号整数进行**位运算**时，编译器会进行整数提升，再对提升后的整数进行位运算，因此要特别注意对于这类无符号整数的位运算，避免出现非预期的结果。

## 2. 命名空间

命名空间(namespace)为防止名字冲突提供了更加可控的机制。命名空间分割了全局命名空间，其中每个命名空间是一个作用域。通过在某个命名空间中定义库的名字，库的作者以及用户可以避免全局名字固有的限制。

命名空间定义：一个命名空间的定义包含两部分：首先是关键字 namespace，随后是命名空间的名字。在命名空间名字后面是一系列由花括号括起来的声明和定义。**只要能出现在全局作用域中的声明就能置于命名空间内**，主要包括：**类、变量(及其初始化操作)、函数(及其定义)、模板和其它命名空间**。命名空间结束后无须分号，这一点与块类似。和其它名字一样，**命名空间的名字也必须在定义它的作用域内保持唯一**。**命名空间既可以定义在全局作用域内，也可以定义在其它命名空间中，但是不能定义在函数或类的内部**。命名空间作用域后面无须分号。

* **每个命名空间都是一个作用域**：命名空间中的每个名字都必须表示该空间内的唯一实体。定义在某个命名空间中的名字可以被该命名**空间内的其它成员直接访问**，也可以被这些成员**内嵌作用域中的任何单位访问**。位于该**命名空间之外**的代码则必须**明确指出**所用的名字属于哪个命名空间。
* **命名空间可以是不连续的**：直观理解是：同一个命名空间出现在多个文件中，但他们仍组成一个命名空间。命名空间可以定义在几个不同的部分，这一点与其它作用域不太一样。命名空间的定义可以不连续的特性使得我们可以**将几个独立的接口和实现文件组成一个命名空间**。此时，命名空间的组织方式类似于我们管理自定义类及函数的方式：命名空间的一部分成员的作用是定义类，以及声明作为类接口的函数及对象，则这些成员应该置于头文件中，这些头文件将被包含在使用了这些成员的文件中。命名空间成员的定义部分则置于另外的源文件中。

* **内联命名空间**：C++11新标准引入了一种新的嵌套命名空间，称为内联命名空间(inline namespace)。和普通的嵌套命名空间不同，**内联命名空间中的名字可以被外层命名空间直接使用**。也就是说，我们无须在内联命名空间的名字前添加表示该命名空间的前缀，通过外层命名空间的名字就可以直接访问它。定义内联命名空间的方式是在关键字namespace前添加关键字inline。关键字inline必须出现在命名空间第一次定义的地方，后续再打开命名空间的时候可以写inline，也可以不写。当应用程序的代码在一次发布和另一次发布之间发生了改变时，常常会用到内联命名空间。
* **未命名的命名空间**(unnamed namespace)：是指关键字namespace后紧跟花括号括起来的一系列声明语句。未命名的命名空间中定义的变量拥有静态生命周期：它们在第一次使用前创建，并且直到程序结束才销毁。
* **using声明**：一条using声明(usingdeclaration)语句一次只引入命名空间的一个成员。它使得我们可以清楚地知道程序中所用的到底是哪个名字。
* **using指示**(usingdirective)：和using声明类似的地方是，我们可以使用命名空间名字的简写形式；和using声明不同的地方是，我们无法控制哪些名字是可见的，因为所有名字都是可见的。using指示以关键字using开始，后面是关键字namespace以及命名空间的名字。
* **避免using指示**：using指示一次性注入某个命名空间的所有名字，这种用法看似简单实则充满了风险：只使用一条语句就突然将命名空间中所有成员的名字变得可见了。如果应用程序使用了多个不同的库，而这些库中的名字通过using指示变得可见，则全局命名空间污染的问题将重新出现。

> [C++/C++11中命名空间(namespace)的使用](https://www.huaweicloud.com/articles/12620834.html) 

## 3. 初始化方式

#### 就地初始化

在 C++11 之前，只能对**结构体或类的静态常量成员**进行就地初始化，其他的不行。

```c++
class C {
private:
	static const int a=10;	// yes
	int a=10;				// no
}
```

在 C++11 中，**结构体或类的数据成员**在声明时**可以直接赋予一个默认值**，初始化的方式有两种：“等号=” 和 “大括号列表初始化”。

```c++
class C {
private:  
    int a=7; 	// C++11 only
    int b{7};	// or int b={7}; C++11 only
    int c(7);	// error，小括号初始化方式不能用于就地初始化。
};  
```

#### 就地初始化与初始化列表的先后顺序

C++11 支持了就地初始化非静态数据成员的同时，初始化列表的方式也被保留下来，也就是说既可以使用就地初始化，也可以使用初始化列表来完成数据成员的初始化工作。当二者同时使用时并不冲突，**初始化列表发生在就地初始化之后**，即最终的初始化结果以初始化列表为准。



在C++11中，对象初始化拥有多种语法选择：圆括号，等号，花括号：

```C++
int x(0);	//用圆括号初始化
int y = 0;	//用"="初始化
int z{0};	//用花括号初始化
int z = { 0 }; 	//用"="和花括号初始化，C++通常把它和“只使用花括号”的情况同样对待。
```

C++ 中指定初始化值的三种方式中，只有花括号能用在每个地方。

花括号初始化有一个新奇的特性，它**阻止在built-in类型中的隐式收缩转换**（narrowing conversation）。如果表达式的值不能保证被初始化对象表现出来，代码将无法通过编译。用圆括号和”=“初始化不会检查收缩转换（narrowing conversation）。

```c++
double x, y, z;
...
int sum1{ x + y + z };	//编译错误！double 的和不能表现为 int
int sum2(x + y + z);	//可以（表达式的值被截断为 int）
int sum3 = x + y + z;	//同上
```

花括号初始化的另外一个值得一谈的特性是它能避免C++最令人恼火的解析。


初始化经常使用括号，或者是使用大括号，或者是复赋值操作。因为这个原因，c++11提出了统一初始化，意味着使用这初始化列表，

一个初始化列表强制使用赋值操作， 也就是意味着每个变量都是一个默认的初始化值，被初始化为0（NULL 或者是 nullptr）。如下：

```c++
int i; //这是一个未定义的行为
int i{}； //i调用默认的构造函数为i赋值为0
int *p； //这是一个未定义的行为
int *p{} ;// p被初始化为一个nullptr
```



#### 缩窄转换

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

****



## 4. 顶层const 和 底层 const 理解

首先，const是一个限定符，被它修饰的变量的值不能改变。

对于**一般的变量**来说，其实**没有**顶层const和底层const的区别，而只有像**指针**这类复合类型的基本变量，才有这样的区别。

1. 顶层const：指的是 const 修饰的**变量本身**是一个常量，无法修改，指的是指针，就是 * 号的右边

2. 底层const：指的是 const 修饰的变量**所指向的对象**是一个常量，指的是所指变量，就是 * 号的左边

```c++
int a = 10;
int* const b1 = &a;	// 顶层 const，b1 本身是一个常量
const int* b2 = &a;	// 底层 const，b2 本身可变，所指向的对象是常量
const int b3 = 20;	// 顶层 const，b3 是常量不可变
const int* const b4 = &a;	// 前一个 const 为底层，后一个为顶层，b4 不可变
const int& b5 = a;	// 用于声明引用变量，都是底层 const
```

区分作用：

1. 执行对象拷贝时有限制，常量的底层 const 不能赋值给非常量的底层 const

2. 使用命名的强制类型转换函数 const_cast 时，只能改变运算对象的底层 const



const 成员函数本质上是修饰 this 指针，成员变量引用会被看成常量指针的。



## 5. 左值引用和右值引用

右值引用完成两个功能：

1. 实现 move 语义
2. 完美转发







## 6. new 方法

stl_placement_new



## 7. 类型转换

[C++标准转换运算符reinterpret_cast](https://www.cnblogs.com/ider/archive/2011/07/30/cpp_cast_operator_part3.html)

reinterpret_cast运算符是用来处理无关类型之间的转换；它会产生一个新的值，这个值会有与原始参数（expressoin）有完全相同的比特位。

所以总结来说：reinterpret_cast用在任意指针（或引用）类型之间的转换；以及指针与足够大的整数类型之间的转换；从整数类型（包括枚举类型）到指针类型，无视大小。

（所谓"足够大的整数类型",取决于操作系统的参数，如果是32位的操作系统，就需要整形（int）以上的；如果是64位的操作系统，则至少需要长整形（long）。具体大小可以通过sizeof运算符来查看）。



## 8.C++ 说明符和限定符

> [C++ 说明符和限定符](https://zhuanlan.zhihu.com/p/645909785)

在C++中，说明符（Specifier）和限定符（Qualifier）用于修饰数据类型、函数、变量等，以改变其行为或提供额外的信息。它们是编程语言中的关键字或关键字组合。下面是一些常见的C++说明符和限定符：

1. 数据类型说明符：

- int: 整数类型，用于声明整数变量。
- double: 双精度浮点数类型，用于声明带有小数点的浮点数变量。
- float: 单精度浮点数类型，类似于double但存储空间较小。
- char: 字符类型，用于声明单个字符变量。
- bool: 布尔类型，用于声明布尔值（true或false）变量。
- void: 空类型，用于表示没有返回值的函数或空指针。

存储类说明符：

- auto: 自动类型推断，编译器根据初始化表达式自动推断变量的类型。
- static: 静态存储类，使得局部变量在程序生命周期内保持其值，且只初始化一次。
- extern: 外部存储类，用于声明全局变量，并表示该变量在其他文件中定义。
- register: 寄存器存储类，用于请求将变量存储在寄存器中，以便更快地访问。
- mutable: 用于修饰类的成员变量，允许在const成员函数中修改这些变量。

限定符：

- const: 用于声明常量，表示该变量的值在初始化后不能被修改。
- volatile: 用于声明易变的变量，告诉编译器不要进行优化，因为变量的值可能会在意料之外的情况下改变（如中断）。
- restrict（C99标准新增）：用于告知编译器，该指针是访问对象的唯一且初始的方式，从而进行优化。
  在保证多个指针所指向的区域无交叠的前提下，可以将这些指针加上restrict限定符，用于指导编译器做出更激进的优化。

访问限定符：

- public: 在类中指定公共成员，可以在类的内部和外部访问。
- private: 在类中指定私有成员，只能在类的内部访问。
- protected: 在类中指定受保护成员，可以在类的内部和派生类中访问。

这些说明符和限定符提供了更多的灵活性和控制，帮助开发者在C++中编写更有效、安全和可维护的代码。



在C++11中引入了 thread_local 关键字，它是一个存储类说明符，用于声明线程局部存储的变量。这使得变量的值在每个线程中都有一份独立的副本，而不是像普通变量那样在所有线程之间共享。
