# C++ 泛型

## 模板

### C++模板的偏特化与全特化

> [C++模板的偏特化与全特化](https://harttle.land/2015/10/03/cpp-template.html)

模板机制为C++提供了泛型编程的方式，在减少代码冗余的同时仍然可以提供类型安全。 特化必须在同一命名空间下进行，可以特化类模板也可以特化函数模板，**但类模板可以偏特化和全特化，而函数模板只能全特化**。 模板实例化时会优先匹配"模板参数"最相符的那个特化版本。

> C++的模板机制被证明是图灵完备的，即可以通过[模板元编程（template meta programming）](https://harttle.land/2015/09/16/effective-cpp-48.html)的方式在编译期做任何计算。

#### 模板的声明

类模板和函数模板的声明方式是一样的，在类定义/模板定义之前声明模板参数列表。例如：

```c++
// 类模板
template <class T1, class T2>
class A{
    T1 data1;
    T2 data2;
};

// 函数模板
template <class T>
T max(const T lhs, const T rhs){   
    return lhs > rhs ? lhs : rhs;
}
```

#### 全特化

通过[全特化](http://en.cppreference.com/w/cpp/language/template_specialization)一个模板，可以对一个特定参数集合自定义当前模板，类模板和函数模板都可以全特化。 **全特化的模板参数列表应当是空的，并且应当给出"模板实参"列表**：

```c++
// 全特化类模板
template <>
class A<int, double>{
    int data1;
    double data2;
};

// 函数模板
template <>
int max(const int lhs, const int rhs){   
    return lhs > rhs ? lhs : rhs;
}
```

注意类模板的全特化时在类名后给出了"模板实参"，但函数模板的函数名后没有给出"模板实参"。 这是因为编译器根据`int max(const int, const int)`的函数签名可以推导出来它是`T max(const T, const T)`的特化。

#### 特化的歧义

上述函数模板不需指定"模板实参"是因为编译器可以通过函数签名来推导，但有时这一过程是有歧义的：

```c++
template <class T>
void f(){ T d; }

template <>
void f(){ int d; }
```

此时编译器不知道`f()`是从`f<T>()`特化来的，编译时会有错误：

```
error: no function template matches function template specialization 'f'
```

这时我们便需要显式指定"模板实参"：

```c++
template <class T>
void f(){ T d; }

template <>
void f<int>(){ int d; }
```

#### 偏特化

类似于全特化，偏特化也是为了给自定义一个参数集合的模板，但偏特化后的模板需要进一步的实例化才能形成确定的签名。 值得注意的是函数模板不允许偏特化，这一点在[Effective C++: Item 25](https://harttle.land/2015/08/23/effective-cpp-25.html)中有更详细的讨论。 偏特化也是以`template`来声明的，需要给出剩余的"模板形参"和必要的"模板实参"。例如：

```c++
template <class T2>
class A<int, T2>{
    ...
};
```

函数模板是不允许偏特化的，下面的声明会编译错：

```c++
template <class T1, class T2>
void f(){}

template <class T2>
void f<int, T2>(){}
```

但函数允许重载，声明另一个函数模板即可替代偏特化的需要：

```c++
template <class T2>
void f(){}              // 注意：这里没有"模板实参"
```

多数情况下函数模板重载就可以完成函数偏特化的需要，一个例外便是`std`命名空间。 `std`是一个特殊的命名空间，用户可以特化其中的模板，但不允许添加模板（**其实任何内容都是禁止添加的**）。 因此在`std`中添加重载函数是不允许的，在[Effective C++: Item 25](https://harttle.land/2015/08/23/effective-cpp-25.html)中给出了一个更详细的案例。



### C++ 中让人头晕的 typedef & typename

> [C++ 中让人头晕的 typedef & typename](https://www.luozhiyun.com/archives/742)

用过 C++ 的同学对 typename 和 typedef 相信并不是很陌生，但是当我看到下面这段代码的时候仍然无法理解：

```c++
typedef typename std::vector<T>::size_type size_type;
```

按理来说 typedef 一般不是用来定义一种类型的别名，如下：

```
typedef int SpeedType;
```

定义了一个 int 的别名是 SpeedType，那么我就可以这样用：

```c++
int main(void)
{
    SpeedType s = 10;
    printf("speed is %d m/s",s);
    return 0;
}
```

但是 typedef 后面接 typename 表示什么意思呢？typename 不是用来定义模板参数的吗？下面我们分别归纳一下 typedef & typename 的用法。

#### typedef

为特定含义的类型取别名，而不只是简单的宏替换，有编译时类型检查。

* 用作同时声明指针型的多个对象

```c++
// pa、pb两个变量都声明为字符串，但是这样只能成功声明了一个
char* pa, pb;  
cout << typeid(pa).name() << endl; //Pc
cout << typeid(pb).name() << endl; //c

// 成功声明两个字符串指针
typedef char* PCHAR; 
PCHAR pa, pb; // 可行
cout << typeid(pa).name() << endl; //Pc
cout << typeid(pb).name() << endl; //Pc
```

* 为结构体取别名

```c++
// 在声明变量的时候，需要带上struct，即像下面这样使用：
typedef struct info
{
    char name[128];
    int length;
}Info;

Info var;
```

* 用来定义与平台无关的类型

```c++
// 比如定义一个叫 REAL 的浮点类型，在目标平台一上，让它表示最高精度的类型为：
typedef long double REAL;
// 在不支持 long double 的平台二上，改为：
typedef double REAL;
```

当跨平台时，只要改下 typedef 本身就行，不用对其他源码做任何修改。

#### typename

typename关键字用于引入一个模板参数，这个关键字用于指出模板声明（或定义）中的非独立名称（dependent names）**是类型名，而非变量名**：

```c++
template <typename T>
const T& max(const T& x, const T& y)
{
  if (y < x) {
    return x;
  }
  return y;
}
```

typename 在这里的意思表明 T 是一个类型。如果没有它的话，在某些情况下会出现模棱两可的情况，比如下面这种情况：

```c++
template <class T>
void foo() {
    T::iterator * iter;
    // ...
}
```

作者想定义一个指针`iter`，它指向的类型是包含在类作用域`T`中的`iterator`。可能存在这样一个包含`iterator`类型的结构：

```c++
struct ContainsAType {
    struct iterator { /*...*/ }; 
};
```

那么 `foo<ContainsAType>();` 这样用的是时候确实可以知道 `iter`是一个`ContainsAType::iterator`类型的指针。但是`T::iterator`实际上可以是以下三种中的任何一种类型：

- 静态数据成员
- 静态成员函数
- 嵌套类型

所以如果是下面这样的情况：

```c++
struct ContainsAnotherType {
    static int iterator;
    // ... 
};
```

那 `T::iterator * iter;`被编译器实例化为`ContainsAnotherType::iterator * iter;`，变成了一个静态数据成员乘以 iter ，这样编译器会找不到另一个变量 `iter` 的定义 。所以为了避免这样的歧义，我们加上 typename，表示 `T::iterator` 一定要是个类型才行。

```c++
template <class T>
void foo() {
    typename T::iterator * iter;
    // ... 
}
```

我们回到一开始的例子，对于 `vector::size_type`，我们可以知道：

```c++
template <class T,class Alloc=alloc>
class vector{
public:
    //...
    typedef size_t size_type;
    //...
};
```

`vector::size_type`是`vector`的嵌套类型定义，其实际等价于 `size_t`类型。

```
typedef typename std::vector<T>::size_type size_type;
```

那么这个例子的真是面目是，`typedef`创建了存在类型的别名，而`typename`告诉编译器`std::vector<T>::size_type`是一个类型而不是一个成员。





 

# C++ 元模版编程

> [【C++ 泛型编程 进阶篇】：用std::integral_constant和std::is_*系列深入理解模板元编程](https://blog.csdn.net/qq_21438461/article/details/131179100)

用std::integral\_constant和std::is\_\*系列深入理解模板元编程



一、模板元编程与类型特性 (Template Metaprogramming and Type Traits)
-------------------------------------------------------

### 1.1 模板元编程简介 (Introduction to Template Metaprogramming)

模板元编程（Template Metaprogramming）是一种 C++ [编程技术](https://so.csdn.net/so/search?q=%E7%BC%96%E7%A8%8B%E6%8A%80%E6%9C%AF&spm=1001.2101.3001.7020)，其主要手段是利用模板（template）来实现在编译时（compile-time）执行计算。这种方法的优点是，通过在编译阶段完成部分工作，可以提高运行时（runtime）的效率。

这类似于厨师在开店前就已经切好了蔬菜和肉，这样客人点菜的时候就可以更快地烹饪和上菜，而不用等待食材准备的时间。

在模板元编程中，我们常常使用类型（type）来表示值（value），并通过模板特化（template specialization）或者[模板函数](https://so.csdn.net/so/search?q=%E6%A8%A1%E6%9D%BF%E5%87%BD%E6%95%B0&spm=1001.2101.3001.7020)的重载（overloading）来实现不同的操作。这就好比我们通过不同的切菜方法（如切丁、切片、切丝）来处理不同的食材，达到我们想要的烹饪效果。

比如说，我们可以定义一个模板类 `Factorial<3>`，然后通过特化这个模板，使得 `Factorial<3>::value` 在编译时就等于6。这是一个非常简单的模板元编程的例子，但是你可以想象，这种技术在实现更复杂的编译时计算或者类型检查时可能会非常有用。

总的来说，模板元编程是一种强大的 C++ 编程技术，它可以让我们在编译时完成更多的工作，提高程序的运行效率，增强代码的可读性和可维护性。在接下来的章节中，我们将会详细介绍模板元编程中一些重要的类型特性工具，如 `std::integral_constant`、`std::is_same` 等，并探索如何利用它们进行更高级的模板元编程。

### 1.2 类型特性的必要性 (The Necessity of Type Traits)

类型特性（Type Traits）在模板元编程中发挥了重要的作用，可以说它们是模板元编程的基础工具。那么，为什么我们需要类型特性呢？

首先，类型特性可以帮助我们获取类型的各种信息。这些信息包括但不限于：这个类型是否是整型？是否是指针？两个类型是否相同？等等。正如我们在购物时需要通过产品的标签来了解产品的信息，类型特性就像是类型的“标签”，为我们提供了大量关于类型的信息。

其次，类型特性可以让我们根据类型的信息来选择不同的实现。这是一种基于类型信息的分支选择机制。就像购物时，你可能会根据商品的价格、质量、口碑等因素来选择最适合自己的商品，编程时我们也可以根据类型特性来选择最合适的代码实现。

例如，我们可以根据 `std::is_integral` 来判断一个类型是否为整型，然后根据这个信息选择不同的实现。这样，我们可以为整型和非整型分别提供最优化的实现，而不必写出一种对所有类型都适用但效率不高的通用实现。

最后，类型特性可以帮助我们写出更安全的代码。通过检查类型特性，我们可以在编译时就捕获到一些可能的错误，而不必等到运行时才发现问题。这可以大大提高代码的可靠性。

综上，类型特性是模板元编程的重要工具，它们的存在使得我们可以在编译时获取类型的信息，根据这些信息选择最合适的代码实现，以及提高代码的可靠性。在接下来的章节中，我们将详细探讨如何使用和特化类型特性，以及如何利用类型特性来实现更复杂的模板元编程。

### 1.3 C++标准库中的类型特性 (Type Traits in the C++ Standard Library)

C++标准库提供了一套丰富的类型特性工具，主要包含在 `<type_traits>` 头文件中。这些工具可以帮助我们在编译时获取大量有关类型的信息。

让我们以购物清单的方式来了解一些常见的类型特性工具：

1.  `std::is_same<T1, T2>`：判断 `T1` 和 `T2` 是否为同一类型，就如同我们比较两个商品是否是同一个品牌、同一个型号的产品。

2.  `std::is_integral<T>`：判断 `T` 是否为整型，这就像我们识别商品是否是某一类别的，例如，判断一件商品是否属于日常用品。

3.  `std::is_pointer<T>`：判断 `T` 是否为指针类型，类似于我们区分一种商品是否属于电子产品。

4.  `std::is_base_of<Base, Derived>`：判断 `Base` 是否为 `Derived` 的基类，就像我们查看一个商品是否是另一个商品的配件或者相关产品。

5.  `std::is_constructible<T, Args...>`：判断类型 `T` 是否可以用 `Args...` 来构造，这就像我们看一件家具是否可以通过提供的零件来组装。

除了以上这些，C++标准库还提供了更多其他的类型特性，如 `std::is_array`、`std::is_enum`、`std::is_function` 等等。使用这些类型特性，我们可以获取更多关于类型的信息，帮助我们在编译时进行决策，实现类型安全的模板元编程。

在后续的章节中，我们将详细探讨一些特定的类型特性，如 `std::integral_constant`，并且深入了解如何利用这些工具实现更高级的模板元编程技巧。

好的，让我们来详细介绍第二章第一节的内容。

二、std::integral\_constant解析
---------------------------

### 2.1 std::integral\_constant的设计与实现

std::integral\_constant是C++标准库中定义的一个模板类。它的主要作用是将整数值作为类型的一部分进行编译。从字面上理解，它是一个"积分常数"，用于编译期间的常数表达。现在，让我们仔细看看它的声明和实现。

std::integral\_constant的声明如下：

```cpp
template< class T, T v >
struct integral_constant {
    static constexpr T value = v;
    typedef T value_type;
    typedef integral_constant type; 
    constexpr operator value_type() const noexcept { return value; }
    constexpr value_type operator()() const noexcept { return value; }
};
```

我们可以看到，这个模板类接受两个参数，一个类型T和一个该类型的值v。它提供了一个静态的常量成员value，该成员的值就是传入的v。

其中，`typedef T value_type;`和`typedef integral_constant type;`分别用来定义value的类型以及integral\_constant本身的类型。

然后，它还提供了两个转换函数，一个是`constexpr operator value_type() const noexcept`，可以将std::integral\_constant对象隐式转换为T类型的值；另一个是`constexpr value_type operator()() const noexcept`，可以将std::integral\_constant对象当作函数来调用，并返回其内部保存的常量。

通过这样的设计，std::integral\_constant能够让我们在编译期间就能确定某些值，从而提高代码的效率。同时，因为它包含了值类型的信息，我们还可以根据这个信息进行编程，提高代码的灵活性。

下面，我们来看一个std::integral\_constant的使用示例：

```cpp
typedef std::integral_constant<int, 2> two_t;
two_t two;
std::cout << two() << std::endl;  // 输出: 2
```

在这个例子中，我们定义了一个std::integral\_constant的别名two\_t，然后创建了一个two\_t类型的对象two。在打印two对象时，由于std::integral\_constant重载了函数调用运算符，我们可以直接像调用函数那样调用two对象，从而输出其内部保存的值。

### 2.2 std::integral\_constant在模板元编程中的应用

我们已经知道了`std::integral_constant`是如何设计和实现的，那么，它在模板元编程中又是如何被应用的呢？

模板元编程，简单来说，就是利用C++模板在编译期生成并运行代码的技术。在模板元编程中，常数和类型通常被紧密地结合在一起。`std::integral_constant`就是这样一个工具，可以将常数作为类型的一部分在编译期进行操作。

让我们来看一个例子。假设我们想在编译期计算阶乘，那么可以使用`std::integral_constant`来实现：

```cpp
template<int N>
struct factorial : std::integral_constant<int, N * factorial<N - 1>::value> {};

template<>
struct factorial<0> : std::integral_constant<int, 1> {};
```

在这个例子中，我们首先定义了一个模板类`factorial`，继承自`std::integral_constant<int, N * factorial<N - 1>::value>`。这样，`factorial<N>`的`value`就等于`N * factorial<N - 1>::value`，即N的阶乘。然后，我们对N=0的情况进行特化，使得`factorial<0>::value`等于1。这样，我们就可以在编译期计算阶乘了。

> 这里涉及2个知识点,可以查看这两篇文章:
>
> > *   模版继承:[【C++ 泛型编程 入门篇】全面掌握C++元模板中的模板继承:模板继承深入指南和教程](https://liucjy.blog.csdn.net/article/details/131342657)
> > *   结构体模板:[【C++ 泛型编程 入门篇】C++ 元编程 :模板结构体的的使用教程](https://liucjy.blog.csdn.net/article/details/131179530)

然后，我们可以像这样使用上述定义：

```cpp
constexpr int val = factorial<5>::value;
std::cout << val << std::endl;  // 输出: 120
```

在这个例子中，`factorial<5>::value`在编译期就已经计算出来了，所以我们可以将它赋值给`constexpr`变量`val`。

这就是`std::integral_constant`在模板元编程中的一个应用。它让我们可以在编译期做更多的事情，使得代码更高效，更灵活。

### 2.3 std::integral\_constant的高级应用

我们可以在元编程和类型特征（type traits）中看到`std::integral_constant`的实际应用。以下是一个例子：

假设你正在编写一个函数，需要对整型和非整型数据进行不同的处理。你可以创建两个模板函数，一个用于处理整型，一个用于处理非整型。`std::integral_constant`和`std::is_integral`可以帮助你实现这一点。

```cpp
#include <iostream>
#include <type_traits>

// 处理整型数据
template <typename T>
typename std::enable_if<std::is_integral<T>::value>::type
process(T t) {
    std::cout << t << " is an integral number." << std::endl;
}

// 处理非整型数据
template <typename T>
typename std::enable_if<!std::is_integral<T>::value>::type
process(T t) {
    std::cout << t << " is not an integral number." << std::endl;
}

int main() {
    process(10);       // 输出: 10 is an integral number.
    process(3.14);     // 输出: 3.14 is not an integral number.
    process("hello");  // 输出: hello is not an integral number.
}
```

在这个例子中，我们使用`std::is_integral`来判断给定的类型是否为整型。`std::is_integral<T>::value`返回一个`std::integral_constant`实例，表示`T`是否为整型。这个`std::integral_constant`实例在编译时确定，因此我们可以基于它的值来选择合适的模板函数。

### 2.4 std::integral\_constant的特化版本: std::true\_type和std::false\_type

std::integral\_constant 的两个最常用的特化版本是 `std::true_type` 和 `std::false_type`。它们是 `std::integral_constant<bool, value>` 的特化版本，其中 `std::true_type` 是 `std::integral_constant<bool, true>`，`std::false_type` 是 `std::integral_constant<bool, false>`。

这两种类型的主要用途是表示编译期的布尔值。在模板元编程中，它们常被用来代表一种编译期的"是"和"否"，从而允许我们进行编译期的条件判断。同时，由于它们都是类型，因此也可以作为类型标签来使用，帮助我们在模板元编程中传递信息。

1. **std::false\_type 和 std::true\_type 的定义**：

   它们都是简单地继承自 `std::integral_constant`。其定义如下：

   ```cpp
   template<class T, T v>
   struct integral_constant {
       static constexpr T value = v;
       using value_type = T;
       using type = integral_constant;
       constexpr operator value_type() const noexcept { return value; }
       constexpr value_type operator()() const noexcept { return value; }
   };
   
   using false_type = integral_constant<bool, false>;
   using true_type = integral_constant<bool, true>;
   ```

2. **为什么继承它就可以总是返回 false**：

   当你继承自 `std::false_type`，你实际上是继承自一个已经特化的 `integral_constant`，它的 `value` 成员已经被设置为 `false`。因此，任何继承自 `std::false_type` 的类型都将有一个静态常量成员 `value`，其值为 `false`。

   同理，继承自 `std::true_type` 的类型将有一个值为 `true` 的静态常量成员 `value`。

3. **用途**：

   `std::false_type` 和 `std::true_type` 主要用于在编译时为类型提供一种简单的 `true` 或 `false` 标签。这在模板特化、SFINAE（Substitution Failure Is Not An Error）技巧和其他模板编程技术中非常有用。

例如，你可能看到如下的类型特性：

```cpp
template <typename T>
struct is_pointer : std::false_type {};

template <typename T>
struct is_pointer<T*> : std::true_type {};
```

上面的代码定义了一个 `is_pointer` 类型特性，它用于在编译时判断一个类型是否为指针。对于大多数类型，它返回 `false`（因为大多数类型不是指针），但对于指针类型，它返回 `true`。这是通过模板特化实现的。

实际上，对于某些简单的场景，你确实可以直接返回 `true` 或 `false` 而不必使用 `std::true_type` 或 `std::false_type`。但在模板编程中，使用这些类型具有特定的优势和原因：

1.  **元编程的一致性**：在模板元编程中，很多类型特性都返回一个类型而不是一个值。`std::true_type` 和 `std::false_type` 为我们提供了一种统一的方式来表示编译时的布尔值。

2.  **更多的信息**：`std::true_type` 和 `std::false_type` 不仅仅是布尔值。它们还有其他成员，例如 `value_type` 和 `type`，这些成员在复杂的模板操作中可能会派上用场。

3.  **可扩展性**：使用 `std::true_type` 和 `std::false_type` 允许你在未来为你的类型特性添加更多的信息或功能，而不仅仅是一个布尔值。

4.  **与标准库的互操作性**：许多标准库模板（例如 `std::enable_if`）期望其模板参数是一个有 `value` 成员的类型。直接使用 `std::true_type` 和 `std::false_type` 可以确保与这些标准库模板的兼容性。

5.  **语义清晰性**：使用类型特性表示编译时的信息可以使代码的意图更加明确。例如，`is_pointer<T>::value` 比一个简单的函数或变量更清楚地表示其是一个关于类型 `T` 是否为指针的编译时信息。

然而，如果你的目标只是简单地返回一个编译时的 `true` 或 `false` 值，并且不需要上述的其他优势，那么直接返回布尔值当然是可以的。选择哪种方法取决于你的具体需求和你想要的代码的复杂性级别。

* * *

例如，我们可以使用 `std::true_type` 和 `std::false_type` 来实现一个编译期的 `is_integral` 判断，这个判断会告诉我们一个类型是否是整型：

```cpp
template <typename T>
struct is_integral : std::false_type {};

template <>
struct is_integral<int> : std::true_type {};

template <>
struct is_integral<long> : std::true_type {};

// 其他整型特化...
```

在这个例子中，我们首先定义了一个模板 `is_integral`，并让它默认继承自 `std::false_type`。然后，我们对所有整型进行特化，让它们继承自 `std::true_type`。这样，我们就可以使用 `is_integral<T>::value` 来判断 `T` 是否是整型，如果 `T` 是整型，那么 `is_integral<T>::value` 就是 `true`，否则就是 `false`。  
在使用 `std::true_type` 和 `std::false_type` 时，一种常见的模式是定义一个名为 `type` 的内部类型，然后让 `type` 成为 `std::true_type` 或 `std::false_type`：

```cpp
template <typename T>
struct is_integral {
    typedef std::false_type type;
};

template <>
struct is_integral<int> {
    typedef std::true_type type;
};

template <>
struct is_integral<long> {
    typedef std::true_type type;
};
```

这种模式的优点是，我们可以使用 `typename is_integral<T>::type` 来获得一个代表 `T` 是否为整数的类型标签，而不仅仅是一个布尔值。这样，我们就可以在模板元编程中使用类型推导和特化来进行更复杂的操作。

例如，我们可以使用 `typename is_integral<T>::type` 来选择不同的函数实现：

```cpp
template <typename T>
void print(const T& val, std::true_type) {
    std::cout << "Integral: " << val << std::endl;
}

template <typename T>
void print(const T& val, std::false_type) {
    std::cout << "Not integral: " << val << std::endl;
}

template <typename T>
void print(const T& val) {
    print(val, typename is_integral<T>::type());
}
```

在这个例子中，我们定义了两个 `print` 函数，一个接受 `std::true_type`，另一个接受 `std::false_type`。然后，我们定义了一个 `print` 函数模板，它会根据 `T` 是否为整型来选择正确的 `print` 函数。

这样，我们就可以根据类型的特性在编译期选择不同的函数实现，从而实现编译期的多态。这只是 `std::true_type` 和 `std::false_type` 的应用之一，它们在模板元编程中的应用是非常广泛的。

### 2.5 什么时候需要继承 std::true\_type和std::false\_type 提供默认行为

模板编程中，有时候会有疑问，如何正确的选取编程手段。什么情况下默认行为需要继承它们。  
查看下面例子：

```cpp
template<typename Mapper>
struct MapperTraits;

template<typename Mapper>
struct MapperTraits : std::false_type {};

```

当你定义一个模板如`template<typename Mapper> struct MapperTraits;`而不提供任何默认实现，它实际上是一个不完整的模板。如果你尝试为一个没有特化的类型实例化它，编译器会产生一个错误，因为它找不到该模板的定义。

另一方面，如果你提供一个默认实现，如继承自`std::false_type`：

```cpp
template<typename Mapper>
struct MapperTraits : std::false_type {};
```

那么，对于任何没有特化的类型，编译器都可以成功地实例化这个模板，并继承自`std::false_type`。

这两种方法的主要区别在于它们如何处理未特化的类型：

1.  **不完整的模板**：会导致编译错误。
2.  **提供默认实现**：会成功编译，并为未特化的类型提供默认行为。

选择哪种方法取决于你的需求：

*   如果你想确保每种类型都有一个明确的特化，并且不希望有任何默认行为，那么使用不完整的模板是有意义的。

*   如果你想为那些没有特化的类型提供一个默认行为，那么提供一个默认实现是合适的。

在某些情况下，继承自`std::false_type`或`std::true_type`是有意义的，因为它们提供了一个编译时的布尔值，你可以使用这个值来进行编译时的条件检查。但如果你不需要这种行为，那么只提供一个默认实现就足够了。

*   当你继承自`std::false_type`或`std::true_type`时，你通常是为了在编译时进行条件判断。这样，你可以使用这些类型特征来决定某些编译时的行为，例如选择特定的函数重载或模板特化。这种方法提供了一种默认行为，即使对于那些没有明确特化的类型。

*   当你选择不提供默认实现（即不完整的模板）时，你的意图是确保每个类型都有一个明确的特化。这样，如果某个类型没有特化，编译器会产生一个错误，从而强制开发者为该类型提供一个特化。

这两种方法都有其用途，选择哪种方法取决于你的具体需求和你想要的代码行为。

*   当你为模板提供一个默认实现（例如继承自`std::false_type`或其他任何默认行为），你实际上为模板提供了一个完整的定义。这意味着，对于那些没有特化的类型，这个默认实现会被使用。

*   当你只声明模板而不提供任何定义（即不完整的模板），你实际上只为模板提供了一个声明。这意味着，如果你尝试为一个没有特化的类型实例化这个模板，编译器会产生一个错误，因为它找不到该模板的定义。

所以，前者提供了一个完整的默认定义，而后者只是一个声明，没有定义，因此会导致编译错误。

三、std::is\__类系列剖析 (Unveiling the std::is\__ Class Series)
---------------------------------------------------------

### 3.1 std::is\_same: 识别相同类型 (Recognizing Identical Types with std::is\_same)

在编程的过程中，我们有时候需要判断两种类型是否完全相同，这时候就需要用到std::is\_same。它是一个模板类，可以帮助我们在编译时判断两种类型是否一致。那么它是如何做到的呢？我们来一起探究一下。

std::is\_same的定义非常简单。一般来说，我们可以在的头文件中找到它。它是这样定义的：

```cpp
template<class T, class U>
struct is_same : std::false_type {};
```

当我们使用std::is\_same<T, U>::value时，如果T和U是不同的类型，那么结果就是false。但是如果T和U是同一种类型，我们期望得到的结果是true。这是如何实现的呢？

这就要借助模板特化的技术了。在模板特化中，我们可以为模板类定义特定的行为。对于std::is\_same，它的特化版本如下：

```cpp
template<class T>
struct is_same<T, T> : std::true_type {};
```

这个特化版本告诉我们，当两个模板参数完全相同时，is\_same返回的结果是std::true\_type，也就是true。

有了这个工具，我们就可以在编译时期对类型进行判断了。例如，我们可以使用static\_assert来检查类型：

```cpp
static_assert(std::is_same<int, int>::value, "Types are not the same");
```

如果类型相同，那么这个断言就会通过。如果类型不同，那么就会在编译期间发出错误。

std::is\_same不仅可以用于基础类型，也可以用于用户定义的类型。例如，我们定义了一个类A，然后我们可以使用std::is\_same<A, A>::value来判断A类的类型。

std::is\_same在泛型编程中非常有用，特别是在模板函数的重载中。有时，我们需要根据模板参数的类型来选择不同的函数实现。这时，std::is\_same就可以帮助我们做出正确的选择。

以上就是std::is\_same的核心内容，通过它我们可以在编译时刻就确定两个类型是否相同，为我们的编程提供了极大的便利。

### 3.2 std::is\_integral: 鉴别整型类型 (Identifying Integral Types with std::is\_integral)

在C++中，整型类型（integral types）包括了bool类型、字符类型和整数类型。那么，如何在编译时判断一个类型是否为整型类型呢？答案就是使用std::is\_integral。

std::is\_integral 是一个模板类，作用是在编译期确定传入的类型参数是否为整型。它在 <type\_traits> 头文件中定义，其基础定义如下：

```cpp
template< class T >
struct is_integral;
```

为了适应所有整型类型，C++ 标准库对其进行了完全特化。完全特化是一种模板特化的技术，即为模板提供特定类型参数的特定实现。例如，int类型的特化版本如下：

```cpp
template<>
struct is_integral<int> : std::true_type {};
```

这样，当我们使用 std::is\_integral::value 时，会得到 true。

实际上，std::is\_integral不仅仅对 int 进行了特化，还对 bool、char、wchar\_t、char16\_t、char32\_t，以及它们的有无符号形式、各种长度的整数类型进行了特化。

使用 std::is\_integral 可以在编译时期进行类型检查，例如：

```cpp
static_assert(std::is_integral<int>::value, "Not an integral type");
```

这行代码会在编译时检查int是否为整型，如果是，则编译可以通过；如果不是，则会报错。

std::is\_integral在模板元编程中有很多应用，它可以在编译时判断模板参数是否为整型，从而对不同类型进行不同的处理。这在泛型编程和模板特化中非常有用。

下面是一个简单的示例，展示了如何使用 std::is\_integral 来对整型和非整型参数进行不同处理：

```cpp
template <typename T>
void func(T t) {
    if constexpr (std::is_integral<T>::value) {
        std::cout << "Integral type\n";
    } else {
        std::cout << "Non-integral type\n";
    }
}
```

以上就是 std::is\_integral 的核心内容，希望能对你理解并应用它有所帮助。

### 3.3 std::is\_pointer: 探寻指针类型 (Exploring Pointer Types with std::is\_pointer)

在C++编程中，指针类型（pointer types）是非常重要的一类数据类型，而在模板元编程中，如何在编译时判断一个类型是否为指针类型呢？C++标准库提供了std::is\_pointer，它帮助我们在编译期就可以得知某个类型是否为指针类型。

`std::is_pointer`仅用于检查类型是否为原始指针类型，即形如`T*`的类型，其中`T`可以是任何非函数类型。对于智能指针类型，如`std::shared_ptr<T>`或`std::unique_ptr<T>`，`std::is_pointer`将返回`false`。

如果你想检查一个类型是否是某种特定的智能指针（如`std::shared_ptr<T>`），你需要写自己的类型特征或使用第三方库。这需要更复杂的模板元编程技术，例如模板特化和SFINAE（替换失败不是错误）。

然而，在日常编程中，我们通常不需要这种复杂性。如果我们需要特别处理指针或智能指针，我们通常会重载函数，或者使用模板并假设它们有某些特性（例如`operator*`和`operator->`）。

std::is\_pointer是一个模板类，它接收一个类型参数，并提供一个布尔常量，如果提供的类型是一个指针类型，则值为true，否则值为false。其基本定义如下：

```cpp
template< class T >
struct is_pointer;
```

和std::is\_same以及std::is\_integral类似，std::is\_pointer也利用了模板的特化技术。其特化的版本如下：

```cpp
template< class T >
struct is_pointer<T*> : std::true_type {};
```

这意味着当我们使用std::is\_pointer<T\*>::value时，如果T\*是一个指针类型，那么结果就是true。

例如，下面的代码展示了如何使用std::is\_pointer：

```cpp
int main() {
    int* p = nullptr;
    std::cout << std::boolalpha << std::is_pointer<decltype(p)>::value;  // 输出：true
}
```

我们可以看到，std::is\_pointer成功地在编译期判断出decltype§是一个指针类型。

std::is\_pointer对于泛型编程来说非常有用，例如在模板函数的重载中。有时，我们需要根据模板参数的类型来选择不同的函数实现，这时std::is\_pointer就能帮助我们做出正确的选择。

例如，下面的代码展示了如何在模板函数中使用std::is\_pointer来进行不同的处理：

```cpp
template <typename T>
void process(T t) {
    if constexpr (std::is_pointer<T>::value) {
        std::cout << "Processing pointer type\n";
    } else {
        std::cout << "Processing non-pointer type\n";
    }
}
```

以上就是std::is\_pointer的核心内容，借助它我们可以在编译时期就判断出某个类型是否为指针类型，从而使我们的编程更加灵活和准确。  
然而`std::is_pointer`并不能区分指针所指向的类型是`int`、`char`还是某个类的类型。它只能判断一个类型是否是指针类型。如果你需要获取指针所指向的类型，你可以使用`std::remove_pointer`这个模板，它可以把一个指针类型转换为它所指向的类型。

例如，如果你有一个`int*`类型，你可以使用`std::remove_pointer`获取`int`类型：

```cpp
typedef std::remove_pointer<int*>::type Type;  // Type 是 int
```

然后，你可以使用`std::is_same`来检查`Type`是否为`int`，`char`或者某个类的类型：

```cpp
bool is_int = std::is_same<Type, int>::value;  // is_int 为 true
bool is_char = std::is_same<Type, char>::value;  // is_char 为 false
```

上述代码中，`std::is_same<T1, T2>::value`会在`T1`和`T2`类型完全相同时返回`true`，否则返回`false`。这样你就可以根据指针所指向的具体类型进行不同的操作了。

四、类型特性类特化 (Specializing Type Traits Classes)
--------------------------------------------

### 4.1 为何要进行类型特性类的特化 (Why Specialize Type Traits Classes)

在我们深入到“为何要进行类型特性类的特化”（Why Specialize Type Traits Classes）的主题之前，先让我们想象一个场景。你正在为一家美食杂志担任摄影师，你需要拍摄各种各样的食物，从热狗到鱼子酱，从蔬菜沙拉到焦糖布丁。每一种食物都需要不同的照明，不同的角度，甚至不同的镜头来捕捉它们最诱人的一面。

编程世界中的情形也是如此。在C++编程中，我们经常会遇到各种各样的数据类型，每一种数据类型都有其特性和行为。如果我们想要编写适应多种数据类型的代码，就需要了解并处理每种数据类型的特性和行为。这就像我们需要知道如何拍摄每种食物一样。

这就是我们要进行类型特性类的特化（Specialize Type Traits Classes）的原因。通过特化类型特性类，我们可以为每种数据类型定义其特性和行为。这使我们能够编写更通用，更灵活的代码。

#### 类型特性类的特化的基本含义

首先，我们需要理解类型特性类的特化（Specializing Type Traits Classes）的基本含义。在C++编程中，"特化"是一个非常重要的概念。它的核心思想是：对于一个模板，我们可以为某些特定的模板参数提供特定的实现。这就是所谓的“特化”。

特化类型特性类（Specializing Type Traits Classes）实际上就是这个概念的应用。我们可以为某些特定的类型提供特定的类型特性类。这样，我们就可以根据每种类型的特性和行为来调整我们的代码。

以std::is\_pointer为例，这个类型特性类用于检测一个类型是否为指针类型。在C++标准库中，std::is\_pointer的基本实现是返回false。但是，当类型T是一个指针类型时，std::is\_pointer被特化为返回true。通过这种方式，我们可以为不同的类型提供不同的行为。

#### 类型特性类特化的应用

类型特性类的特化（Specializing Type Traits Classes）在实际编程中有很多应用。一种常见的用法是在模板函数或模板类中使用它来调整行为。

假设我们有一个模板函数，它接受一个参数并打印该参数。对于大多数类型，我们可以直接使用std::cout来打印。但是，如果参数是一个指针，我们可能希望打印指针的地址，而不是指针指向的值。在这种情况下，我们就可以使用std::is\_pointer来检测参数是否为指针，然后根据结果来调整我们的打印行为。

如果没有类型特性类的特化，我们可能需要为每种可能的类型写一个单独的函数，这显然是不现实的。通过使用类型特性类的特化，我们可以写出更通用，更灵活的代码。

总结一下，类型特性类的特化（Specializing Type Traits Classes）是模板元编程（Template Metaprogramming）中的一种重要技术。通过使用它，我们可以为每种数据类型定义其特性和行为，从而编写出更通用，更灵活的代码。在接下来的章节中，我们将详细介绍如何进行类型特性类的特化，并探讨其在实战中的应用。

### 4.2 如何特化类型特性类 (How to Specialize Type Traits Classes)

在了解了类型特性类特化的基本含义和应用后，接下来我们将详细介绍如何进行类型特性类的特化。特化类型特性类可以看作是一种定制化的过程，类似于定制一件衣服，我们需要根据自己的需求来确定衣服的颜色，样式等特性。类似地，特化类型特性类就是要根据特定类型的特性和行为，定制该类型的类型特性类。

#### 类型特性类特化的基本语法

在C++中，特化类型特性类的基本语法如下：

```cpp
template<>
struct TypeName<TargetType> {
  // 重新定义或者添加成员
};
```

其中，`TypeName`是类型特性类的名称，`TargetType`是需要特化的类型。在大括号内部，我们可以重新定义或者添加类型特性类的成员。

例如，我们可以特化std::is\_integral类，使其能够识别我们自定义的整型类型：

```cpp
struct MyInt {};

template<>
struct std::is_integral<MyInt> : std::true_type {};
```

在这个例子中，我们首先定义了一个名为MyInt的结构体，然后我们特化了std::is\_integral类，使其能够识别MyInt类型为整型类型。我们做的实际上就是将std::is\_integral的基类设为std::true\_type，这样std::is\_integral::value就会返回true。

#### 类型特性类特化的注意事项

当我们特化类型特性类时，需要注意一些事项：

1.  在C++标准库中，大多数类型特性类的基本实现都是继承自std::false\_type或std::true\_type。因此，当我们特化这些类型特性类时，通常会将其基类设为std::false\_type或std::true\_type，来指定::value的值。

2.  类型特性类的特化应当尽可能地减少。不必要的特化会使代码复杂化，并可能导致错误。

3.  特化类型特性类并不会改变原有类型特性类的行为，它只会为特定的类型添加或修改特性。

在接下来的章节中，我们将详细介绍类型特性类特化在实际编程中的应用。

### 4.3 特化类型特性类的实战应用 (Practical Applications of Specialized Type Traits Classes)

在了解了如何特化类型特性类后，我们将探讨其在实际编程中的应用。理论知识的掌握当然重要，但我们更需要知道如何将理论知识应用到实际编程中，就像我们知道每个棋子的走法，但真正重要的是知道如何将它们组合在一起赢得棋局。

#### 类型特性类特化在泛型编程中的应用

在C++的泛型编程中，类型特性类的特化有着广泛的应用。我们可以使用特化的类型特性类来调整模板函数或模板类的行为，以适应不同的类型。

例如，我们可能有一个模板函数，该函数对于大多数类型，都需要进行一些特定的处理。但是，对于某些特殊类型，我们可能需要进行不同的处理。在这种情况下，我们就可以通过特化类型特性类，来实现这种行为的调整。

以下是一个例子，展示了如何利用特化的std::is\_integral来调整模板函数的行为：

```cpp
template <typename T>
void print(const T& value) {
    if constexpr (std::is_integral_v<T>) {
        std::cout << "integral: " << value << "\n";
    } else {
        std::cout << "non-integral: " << value << "\n";
    }
}
```

在这个例子中，如果T是整型类型（包括我们之前特化的MyInt类型），print函数将打印"integral"，否则，将打印"non-integral"。

#### 类型特性类特化在性能优化中的应用

类型特性类的特化也常常用于性能优化。我们可以特化某些类型特性类，来选择性地为特定的类型启用某些性能优化。

例如，对于某些数据结构，如数组，如果元素类型是平凡的（Trivial），我们可以使用更高效的内存操作函数，如std::memcpy，来提高性能。我们可以通过特化std::is\_trivial来实现这种优化。

以下是一个例子，展示了如何利用特化的std::is\_trivial来优化复制数组的函数：

```cpp
template <typename T>
void copy_array(T* dest, const T* src, size_t count) {
    if constexpr (std::is_trivial_v<T>) {
        std::memcpy(dest, src, count * sizeof(T));
    } else {
        for (size_t i = 0; i < count; ++i) {
            dest[i] = src[i];
        }
    }
}
```

在这个例子中，如果T是平凡的，copy\_array函数将使用std::memcpy进行复制，否则，将使用循环进行复制。

通过类型特性类的特化，我们不仅可以使代码更通用，更灵活，还可以根据类型的特性进行性能优化。在未来的编程过程中，你会发现类型特性类的特化是一种强大的工具，它可以帮助你解决许多复杂的问题。

五、案例研究：类型特性在实际编程中的应用 (Case Study: Applying Type Traits in Practical Programming)
--------------------------------------------------------------------------------

### 5.1 面向泛型编程的类型特性应用 (Applying Type Traits for Generic Programming)

类型特性(type traits)在面向泛型编程(generic programming)中有着重要的作用。让我们从一个简单的例子开始，理解一下在这种情况下如何运用类型特性。

假设我们有一个函数，需要对给定的数值进行递增（increment）。我们可能会写出这样的函数：

```cpp
template <typename T>
void increment(T& value) {
    ++value;
}
```

这个函数对大多数的数据类型，如`int`, `float`, `double`等都可以正常工作。但是如果我们尝试将一个`std::string`对象作为参数传递，这个函数就会编译失败，因为`std::string`类型没有定义`++`操作符。

这种情况下，类型特性就派上了用场。我们可以使用`std::is_integral`类型特性来检查T是否是整型，如果是，则执行`++`操作，否则抛出异常。这样，我们就能在编译期间就发现问题，避免了运行时错误。

```cpp
template <typename T>
void increment(T& value) {
    static_assert(std::is_integral<T>::value, "Can only increment integral types");
    ++value;
}
```

这样，如果我们尝试对一个`std::string`类型的对象进行递增操作，编译器就会给出一个错误提示，让我们知道这是不被允许的。

此外，我们也可以使用类型特性来调整函数的行为，以适应不同的数据类型。例如，我们可能希望对于浮点数，增加的值是0.1，而对于整型，增加的值是1。

```cpp
template <typename T>
void increment(T& value) {
    if constexpr (std::is_integral_v<T>) {
        ++value;
    } else if constexpr (std::is_floating_point_v<T>) {
        value += 0.1;
    } else {
        static_assert(always_false_v<T>, "Can only increment integral or floating point types");
    }
}
```

在上述代码中，我们使用了`std::is_integral_v`和`std::is_floating_point_v`类型特性来检查T是否为整型或浮点型。对于不满足这些条件的类型，我们使用了`static_assert`来在编译期间产生错误。

我们也可以看到，这里使用了`if constexpr`来实现编译时分支。这是C++17引入的新特性，它可以确保只有满足条件的分支会被实例化，进一步增强了泛型编程的灵活性。

至此，我们可以看到类型特性在面向泛型编程中的重要作用，它们可以帮助我们在编译期间发现潜在的问题，并灵活地调整函数的行为以适应不同的数据类型。

### 5.2 在元编程中优雅地使用类型特性 (Elegantly Using Type Traits in Metaprogramming)

元编程(metaprogramming)是一种编程技巧，允许程序在编译期间生成或操作其它程序。类型特性(type traits)在元编程中扮演着关键角色，它们可以帮助我们在编译期间获取类型的信息，并据此调整代码的行为。下面，我们将展示如何在元编程中优雅地使用类型特性。

假设我们正在编写一个模板函数，这个函数需要实现两个功能：对于基本类型，我们需要直接打印这个值；对于容器类型，我们需要逐个打印出容器中的元素。为此，我们可以使用`std::is_same`和`std::is_integral`来识别出基本类型，再使用`std::is_class`来识别出类类型。

我们的模板函数可能如下所示：

```cpp
template <typename T>
void print(const T& t) {
    if constexpr (std::is_same_v<T, std::string> || 
                  std::is_integral_v<T> || 
                  std::is_floating_point_v<T>) {
        std::cout << t << '\n';
    } else if constexpr (std::is_class_v<T>) {
        for (const auto& elem : t) {
            std::cout << elem << ' ';
        }
        std::cout << '\n';
    } else {
        static_assert(always_false_v<T>, "Unsupported type");
    }
}
```

在这个函数中，我们使用了`std::is_same`，`std::is_integral`和`std::is_class`来在编译期间确定T的类型。对于字符串、整数和浮点数类型，我们直接打印出该值；对于类类型，我们假定它是一个容器，遍历其元素并打印；对于其它类型，我们使用`static_assert`在编译期间产生错误。这样，我们就能在编译期间发现问题，并根据不同的类型来调整函数的行为。

这个例子展示了类型特性在元编程中的威力。通过使用类型特性，我们可以在编译期间获取类型的信息，并据此生成不同的代码，从而使得我们的程序更加灵活、强大。

### 5.3 从类型特性到概念 (Concepts): C++20的新探索 (From Type Traits to Concepts: New Exploration in C++20)

C++20引入了一个新的特性：概念(concepts)。概念是对模板参数所需特性的明确声明，它能够更加清晰、更加精准地表达我们对模板参数的要求。不过，即使有了概念，类型特性(type traits)仍然会发挥它们在编译期间获取类型信息的重要作用。下面，我们将探讨一下如何结合使用概念和类型特性。

考虑以下这个例子：我们要编写一个模板函数，这个函数需要一个迭代器(iterator)作为参数。在C++20之前，我们可能会这样定义这个函数：

```cpp
template <typename Iter>
void foo(Iter iter) {
    // ...
}
```

然而，这样的定义对`Iter`的要求并不明确，任何类型的参数都可以传递给这个函数，编译器并不能提供足够的类型检查。

在C++20中，我们可以使用概念来更好地定义这个函数：

```cpp
template <std::input_or_output_iterator Iter>
void foo(Iter iter) {
    // ...
}
```

这里，`std::input_or_output_iterator`是一个概念，它要求`Iter`必须是输入迭代器或输出迭代器。如果我们尝试传递一个不满足这个要求的参数，编译器会给出错误提示。

然而，概念并不能完全取代类型特性。类型特性可以提供更多的类型信息，例如，我们可以使用`std::iterator_traits`来获取迭代器指向的类型：

```cpp
template <std::input_or_output_iterator Iter>
void foo(Iter iter) {
    using ValueType = typename std::iterator_traits<Iter>::value_type;
    // ...
}
```

在这个函数中，我们使用`std::iterator_traits`来获取迭代器`Iter`指向的类型，并将其别名为`ValueType`。这样，我们就能在函数内部使用这个类型。

从这个例子中，我们可以看到，概念和类型特性在C++编程中各有其用。概念提供了一种明确、简洁的方式来表达我们对模板参数的要求，而类型特性则可以提供更多的类型信息。结合使用它们，可以让我们的程序更加强大、更加灵活。



