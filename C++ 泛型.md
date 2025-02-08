# C++ 泛型

## SFINAE

SFINAE 是 "Substitution Failure Is Not An Error" 的缩写，它是 C++ 模板编程中的一个重要概念。

1. SFINAE 的定义

   SFINAE 是指在**模板参数替换**过程中，如果出现了**无效的代码，编译器不会报错**，而是**继续尝试**其他的重载或模板特化。这种机制允许我们**基于类型特性来选择不同的函数重载或模板特化**。

2. SFINAE 的原理

   当编译器遇到一个函数模板时，它会尝试用给定的模板参数来实例化这个模板。如果在这个过程中产生了无效的代码（例如，**使用了一个不存在的类型成员**），编译器不会立即报错，而是**简单地放弃这个模板，继续查找其他可能的匹配**。

3. SFINAE 的基本应用

   以下是一个简单的 SFINAE 示例：

   ```cpp
   #include <iostream>
   #include <type_traits>

   // 对于有 size_type 成员的类型
   template <typename T>
   typename T::size_type size(const T& container) {
       return container.size();
   }

   // 对于没有 size_type 成员的类型
   template <typename T>
   typename std::enable_if<!std::is_same<decltype(std::declval<T>().size()), void>::value, size_t>::type
   size(const T& container) {
       return container.size();
   }

   // 对于C风格数组
   template <typename T, std::size_t N>
   std::size_t size(const T (&)[N]) {
       return N;
   }

   int main() {
       std::vector<int> vec = {1, 2, 3};
       int arr[] = {1, 2, 3, 4};

       std::cout << "Vector size: " << size(vec) << std::endl;
       std::cout << "Array size: " << size(arr) << std::endl;

       return 0;
   }
   ```

   使用 `std::enable_if` 可以根据条件启用或禁用某个函数模板。

   ```cpp
   #include <iostream>
   #include <type_traits>

   template <typename T>
   typename std::enable_if<std::is_integral<T>::value, void>::type
   process(T value) {
       std::cout << "Processing integral type: " << value << std::endl;
   }

   template <typename T>
   typename std::enable_if<std::is_floating_point<T>::value, void>::type
   process(T value) {
       std::cout << "Processing floating-point type: " << value << std::endl;
   }

   int main() {
       process(42);       // 调用处理整数类型的函数模板
       process(3.14);     // 调用处理浮点类型的函数模板
       // process("hello"); // 编译错误，因为没有匹配的函数模板
       return 0;
   }
   ```

4. SFINAE 的高级应用

   a. 类型特征检查：

   ```cpp
   #include <iostream>
   #include <type_traits>

   // 检查类型是否有 push_back 方法
   template <typename T, typename = void>
   struct has_push_back : std::false_type {};

   template <typename T>
   struct has_push_back<T,
       std::void_t<decltype(std::declval<T>().push_back(std::declval<typename T::value_type>()))>
   > : std::true_type {};

   // 使用 SFINAE 选择正确的函数
   template <typename Container>
   std::enable_if_t<has_push_back<Container>::value>
   add_element(Container& c, const typename Container::value_type& value) {
       c.push_back(value);
       std::cout << "Element added using push_back" << std::endl;
   }

   template <typename Container>
   std::enable_if_t<!has_push_back<Container>::value>
   add_element(Container& c, const typename Container::value_type& value) {
       c.insert(value);
       std::cout << "Element added using insert" << std::endl;
   }

   int main() {
       std::vector<int> vec;
       std::set<int> set;

       add_element(vec, 1);
       add_element(set, 2);

       return 0;
   }
   ```

   b. 编译时多态性：

   ```cpp
   #include <iostream>
   #include <type_traits>

   // 基础案例
   template <typename T, typename = void>
   struct Printer {
       static void print(const T& value) {
           std::cout << "Generic print: " << value << std::endl;
       }
   };

   // 特化版本：对于有 to_string 方法的类型
   template <typename T>
   struct Printer<T, std::void_t<decltype(std::declval<T>().to_string())>> {
       static void print(const T& value) {
           std::cout << "Print using to_string: " << value.to_string() << std::endl;
       }
   };

   class CustomClass {
   public:
       std::string to_string() const { return "CustomClass"; }
   };

   int main() {
       Printer<int>::print(42);
       Printer<CustomClass>::print(CustomClass());
       return 0;
   }
   ```

5. SFINAE 的优点

   - 允许在编译时基于类型特性选择不同的实现。

   - 可以实现更灵活和通用的模板代码。

   - 能够在不修改现有代码的情况下扩展功能。

6. SFINAE 的局限性

   - 可能导致代码复杂性增加，难以理解和维护。

   - 编译错误信息可能变得难以解读。

   - 在某些情况下可能会增加编译时间。

7. C++20 中的改进

   C++20 引入了概念（Concepts）和约束（Constraints），这些新特性提供了一种更清晰、更直接的方式来表达模板参数的要求，在某些情况下可以替代 SFINAE。

   ```cpp
   #include <concepts>

   template <typename T>
   concept Printable = requires(T t) {
       { t.to_string() } -> std::convertible_to<std::string>;
   };

   template <Printable T>
   void print(const T& value) {
       std::cout << value.to_string() << std::endl;
   }

   template <typename T>
   void print(const T& value) requires (!Printable<T>) {
       std::cout << value << std::endl;
   }
   ```

总结：SFINAE 是 C++ 模板元编程中的一个强大工具，它允许我们基于类型特性进行编译时的代码选择。虽然它可能增加代码的复杂性，但在需要高度泛型和优化的场景中，SFINAE 仍然是一个非常有用的技术。

## SFINAE 的最佳实践

1. 使用类型特征和别名模板简化 SFINAE

   最佳实践：使用标准库的类型特征和自定义的别名模板来简化 SFINAE 表达式。

   ```cpp
   #include <type_traits>
   #include <iostream>

   // 别名模板简化SFINAE表达式
   template<typename T>
   using EnableIfIntegral = std::enable_if_t<std::is_integral_v<T>, int>;

   // 使用简化后的SFINAE
   template<typename T, EnableIfIntegral<T> = 0>
   void printNumber(T value) {
       std::cout << "Integral number: " << value << std::endl;
   }

   // 对于非整数类型
   template<typename T, std::enable_if_t<!std::is_integral_v<T>, int> = 0>
   void printNumber(T value) {
       std::cout << "Non-integral value" << std::endl;
   }

   int main() {
       printNumber(42);    // 输出：Integral number: 42
       printNumber(3.14);  // 输出：Non-integral value
       return 0;
   }
   ```

2. 使用 void_t 进行类型检测

   最佳实践：使用 `std::void_t` 来检测类型是否具有特定的成员或操作。

   ```cpp
   #include <type_traits>
   #include <iostream>

   // 检测是否有 size() 方法
   template<typename, typename = void>
   struct has_size : std::false_type {};

   template<typename T>
   struct has_size<T, std::void_t<decltype(std::declval<T>().size())>> : std::true_type {};

   // 使用 SFINAE 选择正确的函数
   template<typename Container, std::enable_if_t<has_size<Container>::value, int> = 0>
   void printSize(const Container& c) {
       std::cout << "Container size: " << c.size() << std::endl;
   }

   template<typename T, std::enable_if_t<!has_size<T>::value, int> = 0>
   void printSize(const T&) {
       std::cout << "No size() method available" << std::endl;
   }

   int main() {
       std::vector<int> vec{1, 2, 3};
       printSize(vec);  // 输出：Container size: 3

       int x = 10;
       printSize(x);    // 输出：No size() method available

       return 0;
   }
   ```

3. 使用 decltype 和 declval 进行更复杂的类型检测

   最佳实践：对于更复杂的类型检测，结合使用 `decltype` 和 `std::declval`。

   ```cpp
   #include <type_traits>
   #include <iostream>

   // 检测是否可以调用 begin() 和 end()
   template<typename T, typename = void>
   struct is_iterable : std::false_type {};

   template<typename T>
   struct is_iterable<T, std::void_t<
       decltype(std::begin(std::declval<T>())),
       decltype(std::end(std::declval<T>()))
   >> : std::true_type {};

   // 使用 SFINAE 选择正确的函数
   template<typename Container, std::enable_if_t<is_iterable<Container>::value, int> = 0>
   void printFirstElement(const Container& c) {
       auto it = std::begin(c);
       if (it != std::end(c)) {
           std::cout << "First element: " << *it << std::endl;
       } else {
           std::cout << "Container is empty" << std::endl;
       }
   }

   template<typename T, std::enable_if_t<!is_iterable<T>::value, int> = 0>
   void printFirstElement(const T&) {
       std::cout << "Not an iterable type" << std::endl;
   }

   int main() {
       std::vector<int> vec{1, 2, 3};
       printFirstElement(vec);  // 输出：First element: 1

       int x = 10;
       printFirstElement(x);    // 输出：Not an iterable type

       return 0;
   }
   ```

4. 使用 constexpr if (C++17) 简化代码

   最佳实践：在 C++17 及以后的版本中，考虑使用 `if constexpr` 来替代某些 SFINAE 用法，以提高代码可读性。

   ```cpp
   #include <type_traits>
   #include <iostream>

   template<typename T>
   void processValue(const T& value) {
       if constexpr (std::is_integral_v<T>) {
           std::cout << "Processing integral value: " << value << std::endl;
       } else if constexpr (std::is_floating_point_v<T>) {
           std::cout << "Processing floating point value: " << value << std::endl;
       } else {
           std::cout << "Processing other type" << std::endl;
       }
   }

   int main() {
       processValue(42);    // 输出：Processing integral value: 42
       processValue(3.14);  // 输出：Processing floating point value: 3.14
       processValue("Hello"); // 输出：Processing other type
       return 0;
   }
   ```

5. 使用概念 (Concepts, C++20) 进一步简化和明确约束

   最佳实践：在 C++20 中，使用概念来替代复杂的 SFINAE 表达式，提高代码的可读性和表达能力。

   ```cpp
   #include <concepts>
   #include <iostream>

   template<typename T>
   concept Numeric = std::integral<T> || std::floating_point<T>;

   template<typename T>
   concept Printable = requires(T t) {
       { std::cout << t } -> std::same_as<std::ostream&>;
   };

   template<Numeric T>
   void process(T value) {
       std::cout << "Processing numeric value: " << value << std::endl;
   }

   template<Printable T>
   void process(T value) {
       std::cout << "Processing printable value: ";
       std::cout << value << std::endl;
   }

   int main() {
       process(42);     // 输出：Processing numeric value: 42
       process(3.14);   // 输出：Processing numeric value: 3.14
       process("Hello"); // 输出：Processing printable value: Hello
       return 0;
   }
   ```

总结最佳实践：

1. 使用类型特征和别名模板简化 SFINAE 表达式。
2. 利用 `std::void_t` 进行类型特性检测。
3. 对于复杂检测，结合使用 `decltype` 和 `std::declval`。
4. 在 C++17 中，考虑使用 `if constexpr` 替代某些 SFINAE 用法。
5. 在 C++20 中，优先考虑使用概念（Concepts）来表达类型约束。
6. 保持代码简洁和可读，适当添加注释解释复杂的 SFINAE 逻辑。
7. 将复杂的 SFINAE 逻辑封装在单独的类型特征或概念中。
8. 在使用 SFINAE 时，始终考虑编译时间和代码可维护性的平衡。

这些最佳实践可以帮助您更有效地使用 SFINAE，同时保持代码的清晰度和可维护性。随着 C++标准的发展，一些 SFINAE 的使用场景可能会被更现代的特性所取代，但理解 SFINAE 仍然对于理解模板元编程和泛型编程非常重要。

## 模板的实例化

### 模板实例化的过程

模板实例化过程大致可以分为以下几个步骤：

1. **模板的声明和定义**：

   - 当编译器在编译过程中遇到了模板的定义（例如，模板类或模板函数的实现）时，**模板的声明和定义（如模板类、模板函数）会在编译器的符号表中进行记录**。但并不会生成实际的代码。模板定义必须是可见的，才能在后续实例化阶段使用。

     例如，一个模板函数的定义可能是这样的：

     ```cpp
     template<typename T>
     void foo(T x) {
         std::cout << x << std::endl;
     }
     ```

2. **模板实例化的触发**：

   - 当你在某个地方实际使用模板（即实例化模板时，提供了具体的类型或参数），模板实例化才会发生。即编译器根据模板定义生成具体的代码。例如：

     ```cpp
     int main() {
         foo(42);  // 这里触发了模板 foo<int> 的实例化
         foo(3.14); // 这里触发了模板 foo<double> 的实例化
         return 0;
     }
     ```

3. **模板实例化的过程**：

   - **查找模板定义**：编译器首先会检查模板定义是否已可见。如果模板定义不在当前翻译单元中，编译器会报错。
   - **生成代码**：编译器根据模板定义和给定的模板参数生成具体的类或函数代码。模板实例化会产生特定类型的代码。例如，`foo<int>` 会生成一个接受 `int` 类型参数的 `foo` 函数，而 `foo<double>` 会生成一个接受 `double` 类型参数的 `foo` 函数。

4. **实例化时的特殊处理**：

   - **显式实例化**：可以显式实例化一个模板，即强制编译器为某个特定的模板参数生成代码。这样做的好处是，实例化代码将只在显式实例化的地方生成，而不必在每个使用该模板的地方生成。

     ```cpp
     template class MyClass<int>;  // 显式实例化 MyClass<int>
     ```

   - **内联实例化**：对于函数模板而言，编译器通常会进行内联处理，即将模板实例化的代码直接插入到调用的地方。

   - **实例化的延迟**：C++ 支持“延迟实例化”（Lazy Instantiation），即模板代码会在首次实例化时才会被生成。也就是说，模板的定义本身不生成任何代码，只有在模板被使用时，编译器才会根据给定的类型生成具体的代码。

5. **错误处理**：

   - 如果模板参数的类型不满足模板定义中的要求，编译器会报错。例如，模板函数要求参数类型是某个特定类型的类，而实例化时传入了不符合要求的类型，编译器会产生错误。

**如果模板在实例化时无法找到对应的模板定义，编译器会报错**。这是因为模板实例化依赖于模板的定义，编译器需要知道模板的具体实现才能生成特定类型或函数的代码。为了避免这种错误，**模板的定义通常需要在头文件中完全提供，而不仅仅是声明**。通常你会将模板函数或类的定义和声明放在同一个头文件中，以便在编译时确保模板的完整定义是可见的。

**模板定义不可见，错误示例**：

```cpp
// ==== 1、错误示例 ==== //
// foo.h
template<typename T>
void foo(T a);  // 这里只是声明，没有定义

// main.cpp
#include "foo.h"

int main() {
    foo(42);  // 编译时实例化 foo<int>
    return 0;
}

/*
 * 在这种情况下，foo 函数的定义在头文件中没有提供，只有声明。当 main.cpp 中调用 foo(42) 时，编译器试图实例化 foo<int>，
 * 但它没有找到 foo 的定义，因此会报错，通常是类似于：
 * undefined reference to `foo<int>`, 或者
 * error: no matching function for call to ‘foo<int>(int)’.
 */


// ==== 2、正确示例 ==== //
// foo.h
template<typename T>
void foo(T a) {  // 这里是定义，而不仅是声明
    // 函数的具体实现
    std::cout << a << std::endl;
}

// main.cpp
#include "foo.h"

int main() {
    foo(42);  // 编译时实例化 foo<int>
    return 0;
}

/*
 * 这样，在 main.cpp 中调用 foo(42) 时，编译器就能找到模板的定义并进行实例化，生成特定类型（例如 foo<int>）的代码。
 */
```

### 显式与隐式实例化

模板实例化有两种常见的方式：**隐式实例化**和**显式实例化**。

1. **隐式实例化**：

   - 这是模板实例化的默认方式。当模板在代码中**首次被使用时**（如调用模板函数或创建模板类对象），**编译器自动进行实例化**。

     ```cpp
     template<typename T>
     void foo(T x) {
         std::cout << x << std::endl;
     }

     int main() {
         foo(42);    // 隐式实例化 foo<int>
         foo(3.14);  // 隐式实例化 foo<double>
         return 0;
     }
     ```

     在这里，`foo<int>` 和 `foo<double>` 会在编译时被实例化。

2. **显式实例化**：

   - 显式实例化是通过在源代码中**明确地告诉编译器生成特定类型的模板代码**。显式实例化通常在 `.cpp` 文件中使用，并且可以避免不必要的实例化，减少代码膨胀。
   - 显式实例化**只会影响那些明确指定的模板类型，并不会影响其他类型**。其他类型仍然会根据其首次使用的情况**触发隐式实例化**。

     ```cpp
     // 声明
     template<typename T>
     void foo(T x);

     // 显式实例化
     template void foo<int>(int);
     template void foo<double>(double);

     int main() {
         foo(42);    // 不会再实例化模板，只调用已经显式实例化的代码
         foo(3.14);  // 同上
         foo(2.5f);  // 对于 float，会触发隐式实例化，因为未显式指定
         return 0;
     }
     ```

     这种方式常用于头文件中定义模板的接口，但将模板的实现放在 `.cpp` 文件中，以避免每个使用模板的源文件都进行实例化。

### 模板实例化的特殊情况

- **默认模板参数**：当模板有默认参数时，实例化时可以省略该参数。

  ```cpp
  template<typename T = int>
  void foo(T x) {
      std::cout << x << std::endl;
  }

  int main() {
      foo(42);  // 会实例化 foo<int>
      foo(3.14);  // 会实例化 foo<double>
      return 0;
  }
  ```

- **模板的特化**：C++ 允许模板的特化，即为某些特定类型定义不同的实现。模板特化分为**完全特化**和**偏特化**。

  - **完全特化**：为某个特定类型提供一个完全不同的实现。

    ```cpp
    template<>
    void foo<int>(int x) {
        std::cout << "Specialized for int: " << x << std::endl;
    }
    ```

  - **偏特化**：为模板参数的某些类型特定提供一个实现。

    ```cpp
    template<typename T>
    class MyClass<T*> {  // 偏特化：针对指针类型
    public:
        T* ptr;
        MyClass(T* p) : ptr(p) {}
    };
    ```

### 总结

- 如果模板在实例化时找不到定义，编译器就无法生成相应的代码并会报错。因此，模板定义必须在实例化之前是可见的。**通常，模板的定义应放在头文件中，并确保定义和声明一致，以便在任何地方都能正确实例化**。
- 显式实例化只是告诉编译器为特定的类型生成代码，**其他未显式实例化的类型会在首次使用时触发隐式实例化**。

## 模板的两阶段翻译

> 英文名为 Two-phase translation，中文也可翻译成两阶段检查或两阶段编译。

C++ 中的 Two-Phase Translation（两阶段翻译）是模板编译的一个核心机制，特别是在标准 C++（如 C++98）中首次引入。它规定模板的实例化分为两个阶段，模板定义阶段和模板实例化阶段，以确保编译器能够正确解析模板代码。

> 如果模板在实例化时无法找到对应的模板定义，编译器会报错。这是因为模板实例化依赖于模板的定义，编译器需要知道模板的具体实现才能生成特定类型或函数的代码。

1. **第一阶段**（模板定义时）：
   - 检查模板的基本语法
   - 检查与模板参数无关的静态断言
   - 进行名称查找（name lookup）和函数重载解析
2. **第二阶段**（模板实例化时）：
   - 检查依赖于模板参数的代码
   - 类型检查
   - 进行最终的代码生成

详细展开：

1. 定义阶段检查
   在这个阶段，编译器检查模板的整体结构，但**不涉及依赖于模板参数**的部分。主要检查内容包括：

   - 语法正确性：
     - 模板的语法结构是否正确。
     - 括号匹配、分号位置等检查。
   - 非依赖名称的正确性：
     - 不依赖于模板参数的名称检查。
     - 非模板函数、全局变量等的检查。
     - 不依赖于模板参数的 **静态断言**（static assertions）
   - 模板参数的声明是否正确
   - 不依赖于模板参数的基本语义检查

2. 实例化阶段检查
   当模板被实例化时，**依赖于模板参数**的部分被检查。这个阶段包括：

   - 依赖名称的检查：
     解析并检查在第一阶段被标记为依赖的名称。
   - 类型检查：
     对实例化后的代码进行完整的类型检查。
   - 语义分析：
     进行全面的语义分析，包括重载解析、访问控制等。
   - 特化和偏特化的检查：
     检查是否存在适用的特化或偏特化版本。
   - 进行最终的代码生成。

3. 示例

   ```cpp
   template <typename T>
   class MyClass {
   public:
       void func() {
           T::static_method();     // (1)
           int x = sizeof(T);      // (2)
           helper(42);             // (3)
           undeclared_var = 10;    // (4)
       }

   private:
       T member;                   // (5)
   };

   void helper(int) { /* ... */ }
   ```

   第一阶段（定义检查）：

   - (1) 和 (2) 被标记为依赖表达式，不进行检查。
   - (3) helper 函数被识别并检查其存在性。
   - (4) undeclared_var 不被检查，因为它可能是 T 的静态成员。
   - (5) member 的声明被检查语法正确性。

   第二阶段（实例化检查，例如 MyClass<int>）：

   - (1) 检查 int 是否有 static_method。
   - (2) 验证 sizeof(int) 的使用是否正确。
   - (3) 解析 helper(42) 调用，检查参数类型是否匹配。
   - (4) 检查 undeclared_var，如果 int 没有这个静态成员，报错。
   - (5) 检查 int member 的合法性。

4. 编译器实现的差异
   不同的编译器可能会在两个阶段之间的边界上有略微不同的行为。一些编译器可能会尝试在第一阶段做更多的检查，而其他编译器可能会推迟更多的检查到第二阶段。

## 宏展开和模板编译

- 在预处理阶段，所有的宏都会被展开，无论它们是否出现在模板的上下文中。因此，**宏的展开总是在模板编译之前**进行。
- 在**模板实例化时，宏已被展开**，模板代码本身已经被预处理过。如果模板代码中含有宏定义，它们也会在实例化时被再次处理，但这时已经是宏展开后的内容。

## 模板零碎知识

### 在类代码内简化模板类名的使用

> C++ Primer 第五版 ch16.1.2

当我们使用一个类模板类型时必须提供模板实参，但这一规则有一个例外。在**类模板自己的作用域中**，我们可以直接使用模板名而不提供实参。

```cpp
template <typename T>
class BlobPtr {
public:
    BlobPtr(): curr(0) {}
    BlobPtr(Blob<T> &a, size_t sz = O):wptr(a.data), curr(sz) {}
    T& operator*() const {
        auto p = check(curr, "dereference past end");
        return（*p）[curr];//（*p)为本对象指向的 vector
    }
    // 递增和递减
    BlobPtr& operator++();// 前置运算符
    BlobPtr& operator--();
private:
    //若检查成功，check 返回一个指向 vector 的 shared_ptr
    std::shared_ptr<std::vector<T>>
        check(std::si.ze_t, const std::string&) const;
    //保存一个 weak_ptr，表示底层vector 可能被销毁
    std::weak_ptr<std::vector<T>> wptr;
    std::size_tcurr；//数组中的当前位置
};
```

`BlobPtr` 的前置递增和递减成员返回 `BlobPtr&`，而不是 `BlobPtr<T>&`。

当我们处于一个类模板的作用域中时，编译器处理模板自身引用时就好像我们已经提供了与模板参数匹配的实参一样。即，就好像我们这样编写代码一样：

```cpp
BlobPtr<T>& operator++();
BlobPtr<T>& operator--();
```

在 C++中，类内部确实可以省略模板形参。这是因为类内部的成员和类型定义可以隐式地引用外层模板参数。**在模板类内部使用该类本身的名称时，编译器会隐式地将其解释为当前模板实例**。

### 模板类型别名

> C++ Primer 第五版 ch16.1.2

```cpp
template<typename T> using twin = pair<T, T>;
twin<string> authors;// authors 是一个pair<string,String>
```

在这段代码中，我们将 twin 定义为成员类型相同的 pair 的别名。这样，twin 的用户只需指定一次类型。

当我们定义一个模板类型别名时，可以固定一个或多个模板参数：

```cpp
template <typename T> using partNo = pair<T, unsigned>;
partNo<string> books;// books是一个pair<string，unsigned>
partNo<Vehicle> cars;// cars 是一个pair<Vehicle，unsigned>
partNo<Student> kids;// kids 是-个 pair<Student， unsigned>
```

这段代码中我们将 partNo 定义为一族类型的别名，这族类型是 second 成员为 unsigned 的 pair。partNo 的用户需要指出 pair 的 first 成员的类型，但不能指定 second 成员的类型。

### `A.template B<T>()`

#### 分析

`A.template B<T>();` 是模板语法的一部分，特别是在需要**显式地告诉编译器你正在使用一个模板成员函数**时。

1. 整体结构:

   - `A` 是一个对象或指针
   - `B` 是一个模板成员函数
   - `T` 是模板参数

2. `.template` 关键字:

   - 这是 C++中的一个特殊语法
   - 用于明确指出 `B` 是一个模板成员函数

3. **使用场景**:

   - 主要在模板代码中使用
   - 特别是当 `T` 依赖于外部模板参数时

4. 为什么需要 `.template`:

   - **在某些情况下，编译器可能无法确定 `B` 是否为模板**
   - 使用 `.template` 消除歧义，明确告诉编译器 `B` 是模板

5. 示例场景:

   ```cpp
   #include <iostream>

   template <typename T>
   class A {
   public:
       template <typename U>
       void B() {
           std::cout << "Template member function B<U> called with U = " << typeid(U).name() << std::endl;
       }
   };

   template <typename T>
   void example(A<T>& a) {
       a.template B<int>();  // 这里必须使用 template 关键字
   }

   int main() {
       A<double> a;
       example(a);
       return 0;
   }
   ```

   在这个例子中，`example` 函数中调用 `B<int>()` 时使用了 `template` 关键字，表示这是一个模板函数调用。程序输出将会是：

   ```log
   Template member function B<U> called with U = i
   ```

6. 不使用 `.template` 的情况:

   - 当上下文明确时，可以省略
   - 例如: `A.B<int>();`

7. 编译器行为:

   - 遇到 `.template` 时,编译器会将后面的 `B` 视为模板
   - 这有助于解析复杂的模板表达式

8. 可读性考虑:

   - 虽然有时可以省略,但使用 `.template` 可以提高代码可读性
   - 明确指出这是一个模板调用

这种语法主要用于复杂的模板编程场景，特别是在**处理嵌套模板或依赖型名称**时。它帮助编译器正确解析和编译模板代码。

#### 会造成歧义的示例

示例 1：

```cpp
#include <iostream>

template <typename T>
class A {
public:
    void B() {
        std::cout << "Non-template member function B called." << std::endl;
    }

    template <typename U>
    void B(U value) {
        std::cout << "Template member function B<U> called with value: " << value << std::endl;
    }
};

template <typename T>
void example(A<T>& a) {
    a.B();          // 调用非模板成员函数
    a.template B<int>(42);  // 调用模板成员函数
    // a.B<int>(42);   // 编译器无法解析这行代码，导致错误
}

int main() {
    A<double> a;
    example(a);
    return 0;
}
```

可能的歧义，在 `example` 函数中：

- `a.B();` 将调用 `A` 类的非模板成员函数 `B()`。
- `a.template B<int>(42);` 调用了 `A` 类的模板成员函数 `B<U>`，我们必须使用 `template` 关键字来显式地告诉编译器这是一个模板成员函数调用，否则编译器可能无法正确解析 `B<int>`。

如果不使用 `template` 关键字，编译器可能会认为 `B<int>` 是一种不完整的类型或者尝试调用一个非模板成员函数，这将导致**编译错误**：`error: expected primary-expression before 'int'`，表示**编译器期望在 `int` 之前有一个有效的表达式**，但找不到。

## 模板嵌套

## C++模板的偏特化与全特化

> [C++模板的偏特化与全特化](https://harttle.land/2015/10/03/cpp-template.html)

模板机制为 C++提供了泛型编程的方式，在减少代码冗余的同时仍然可以提供类型安全。 特化必须在同一命名空间下进行，可以特化类模板也可以特化函数模板，**但类模板可以偏特化和全特化，而函数模板只能全特化**。 模板实例化时会优先匹配"模板参数"最相符的那个特化版本。

> C++的模板机制被证明是图灵完备的，即可以通过[模板元编程（template meta programming）](https://harttle.land/2015/09/16/effective-cpp-48.html)的方式在编译期做任何计算。

#### 模板的声明

类模板和函数模板的声明方式是一样的，在类定义/模板定义之前声明模板参数列表。例如：

```cpp
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

```cpp
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

```cpp
template <class T>
void f(){ T d; }

template <>
void f(){ int d; }
```

此时编译器不知道`f()`是从`f<T>()`特化来的，编译时会有错误：

```log
error: no function template matches function template specialization 'f'
```

这时我们便需要显式指定"模板实参"：

```cpp
template <class T>
void f(){ T d; }

template <>
void f<int>(){ int d; }
```

#### 偏特化

类似于全特化，偏特化也是为了给自定义一个参数集合的模板，但偏特化后的模板需要进一步的实例化才能形成确定的签名。 **值得注意的是函数模板不允许偏特化**，这一点在[Effective C++: Item 25](https://harttle.land/2015/08/23/effective-cpp-25.html)中有更详细的讨论。 偏特化也是以`template`来声明的，需要给出剩余的"模板形参"和必要的"模板实参"。例如：

```cpp
template <class T2>
class A<int, T2>{
    ...
};
```

函数模板是不允许偏特化的，下面的声明会编译错：

```cpp
template <class T1, class T2>
void f(){}

template <class T2>
void f<int, T2>(){}
```

但函数允许重载，声明另一个函数模板即可替代偏特化的需要：

```cpp
template <class T2>
void f(){}              // 注意：这里没有"模板实参"
```

多数情况下函数模板重载就可以完成函数偏特化的需要，一个例外便是`std`命名空间。 `std`是一个特殊的命名空间，用户可以特化其中的模板，但不允许添加模板（**其实任何内容都是禁止添加的**）。 因此在`std`中添加重载函数是不允许的，在[Effective C++: Item 25](https://harttle.land/2015/08/23/effective-cpp-25.html)中给出了一个更详细的案例。

## C++ 中 typedef & typename

> [C++ 中让人头晕的 typedef & typename](https://www.luozhiyun.com/archives/742)

用过 C++ 的同学对 typename 和 typedef 相信并不是很陌生，但是当我看到下面这段代码的时候仍然无法理解：

```cpp
typedef typename std::vector<T>::size_type size_type;
```

按理来说 typedef 一般不是用来定义一种类型的别名，如下：

```cpp
typedef int SpeedType;
```

定义了一个 int 的别名是 SpeedType，那么我就可以这样用：

```cpp
int main(void)
{
    SpeedType s = 10;
    printf("speed is %d m/s",s);
    return 0;
}
```

但是 typedef 后面接 typename 表示什么意思呢？typename 不是用来定义模板参数的吗？下面我们分别归纳一下 typedef & typename 的用法。

### typedef

为特定含义的类型取别名，而不只是简单的宏替换，有编译时类型检查。

- 用作同时声明指针型的多个对象

```cpp
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

- 为结构体取别名

```cpp
// 在声明变量的时候，需要带上struct，即像下面这样使用：
typedef struct info
{
    char name[128];
    int length;
}Info;

Info var;
```

- 用来定义与平台无关的类型

```cpp
// 比如定义一个叫 REAL 的浮点类型，在目标平台一上，让它表示最高精度的类型为：
typedef long double REAL;
// 在不支持 long double 的平台二上，改为：
typedef double REAL;
```

当跨平台时，只要改下 typedef 本身就行，不用对其他源码做任何修改。

### typename

typename 关键字用于引入一个模板参数，这个关键字用于指出模板声明（或定义）中的非独立名称（dependent names）**是类型名，而不是一个静态成员变量或其他非类型成员**：

这是因为：

- 当使用依赖于模板参数的嵌套类型时（称为依赖类型/dependent type），需要使用 typename 关键字
- 编译器在不使用 typename 的情况下，默认认为 :: 后的标识符是一个静态成员

举例说明：

```cpp
// 示例1：需要typename的情况
template <typename T>
struct Outer {
    typedef int Type;  // 嵌套类型定义
};

template <typename T>
void foo() {
    typename Outer<T>::Type x;  // 必须使用typename，因为Type依赖于模板参数T
}

// 示例2：不需要typename的情况
struct Simple {
    typedef int Type;
};

void bar() {
    Simple::Type x;  // 不需要typename，因为Simple不是模板
}

// 示例3：如果不使用typename，编译器可可能误以为 Type 是静态成员
static int Type;  // 而不是类型别名或嵌套类型
```

如果没有它的话，在某些情况下会**出现模棱两可**的情况，比如下面这种情况：

```cpp
template <class T>
void foo() {
    T::iterator * iter;
    // ...
}
```

作者想定义一个指针`iter`，它指向的类型是包含在类作用域`T`中的`iterator`。可能存在这样一个包含`iterator`类型的结构：

```cpp
struct ContainsAType {
    struct iterator { /*...*/ };
};
```

那么 `foo<ContainsAType>();` 这样用的是时候确实可以知道 `iter`是一个`ContainsAType::iterator`类型的指针。但是`T::iterator`实际上可以是以下三种中的任何一种类型：

- 静态数据成员
- 静态成员函数
- 嵌套类型

所以如果是下面这样的情况：

```cpp
struct ContainsAnotherType {
    static int iterator;
    // ...
};
```

那 `T::iterator * iter;`被编译器实例化为`ContainsAnotherType::iterator * iter;`，变成了一个静态数据成员乘以 iter ，这样编译器会找不到另一个变量 `iter` 的定义 。所以为了避免这样的歧义，我们加上 typename，表示 `T::iterator` 一定要是个类型才行。

```cpp
template <class T>
void foo() {
    typename T::iterator * iter;
    // ...
}
```

我们回到一开始的例子，对于 `vector::size_type`，我们可以知道：

```cpp
template <class T,class Alloc=alloc>
class vector{
public:
    //...
    typedef size_t size_type;
    //...
};
```

`vector::size_type`是`vector`的嵌套类型定义，其实际等价于 `size_t`类型。

```cpp
typedef typename std::vector<T>::size_type size_type;
```

那么这个例子的真是面目是，`typedef`创建了存在类型的别名，而`typename`告诉编译器`std::vector<T>::size_type`是一个类型而不是一个成员。

## if constexpr 和 static_assert(false) 的组合

C++ 模板中，不能同时使用 `if constexpr` 和 `static_assert(false)`，会编译报错。

`if constexpr` 是 C++17 引入的一个特性，用于在编译时进行条件分支。它的主要目的是根据模板参数或其他编译时常量来选择性地编译代码块。
`static_assert` 是一个编译时断言，用于在编译期间检查条件是否为真。如果条件为假，编译器会产生一个错误。

同时使用 `if constexpr` 和 `static_assert(false)` 时，会出现编译错误。例如：

```cpp
template <typename T>
void func() {
    if constexpr (std::is_integral_v<T>) {
        // 整数类型的代码
    } else {
        static_assert(false, "Not supported for this type");  // 在第一阶段就会失败
    }
}
```

这段代码的问题在于，即使 if constexpr 的条件为真（即 T 是整数类型），static_assert(false) 仍然会被实例化和检查，导致编译错误。

这与 C++ 模板的两阶段编译（Two-Phase Translation）特性有关：

1. **第一阶段**（模板定义时）：
   - 检查模板的基本语法
   - 检查与模板参数无关的静态断言
   - 进行名称查找（name lookup）和函数重载解析
2. **第二阶段**（模板实例化时）：
   - 检查依赖于模板参数的代码
   - 类型检查
   - 进行最终的代码生成

关键点在于：`static_assert(false)` 是非依赖性表达式（non-dependent expression），它在第一阶段就会被求值。而 `if constexpr` 的分支消除发生在第二阶段。
**分支消除是第二阶段最优先进行的操作，这保证了被消除分支中的代码不会参与后续的编译过程。(来自 Claude-3.5-Sonnet)**

上面的例子，即使我们用整数类型调用 `func<int>()`：

1. 在第一阶段，编译器看到 `static_assert(false)` 时就会报错，因为这是个非依赖表达式。
2. `if constexpr` 的**分支消除要等到第二阶段才会发生，这时已经太晚了**。

而这个版本就没问题：

```cpp
template<typename T>
void func() {
    if constexpr (std::is_integral_v<T>) {
        // 整数类型的处理
    } else {
        static_assert(std::is_integral_v<T>, "error");  // 依赖于T，第二阶段才求值
    }
}
```

因为 `std::is_integral_v<T>` 是依赖性表达式，它的求值会推迟到第二阶段，这时 `if constexpr` 的分支消除已经发生。

这就是为什么我们需要使用依赖于模板参数的表达式来做静态断言，比如：

- `static_assert(std::is_integral_v<T>)`
- `static_assert(always_false<T>::value)`

而不能直接使用 `static_assert(false)`。

## 函数模板**重载**中使用省略号（...）

在函数模板重载中使用省略号（...）的目的是提供一种**通用的、低优先级的模板匹配方式**。可以理解为**回退机制**。
这是一种常见的 SFINAE（Substitution Failure Is Not An Error）技术，用于在编译时进行类型特征检测。

1. 省略号（`...`）的作用
   在 C++ 中，省略号有两个主要用途：

   - 表示**可变参数函数**，允许函数接受任意数量的参数。
   - 在模板中作为**通用参数匹配器**，作为一种"捕获所有"的机制，用于匹配任何类型和数量的参数。

   **重载优先级： 在函数重载解析中，更具体的重载版本会优先于更通用的版本**。使用 `...` 的版本被认为是最不具体的，因此具有最低的优先级。因此在 SFINAE 中，`...` 通常用作"后备"或"默认"选项。如果其他更具体的重载由于替换失败而被排除，那么带有 `...` 的版本将会被选中。

   例子：

   ```cpp
   /*
    * 1. 通过 decltype 和逗号表达式返回 std::true_type 来确认 T 是否具备 getValue() 方法。
    * 2. 下面的 has_getValue 实现属于函数模板重载，因此函数签名要不同，不能都用 typename T 和 has_getValue()。
    *    可以通过不同的函数入参区分。
    */
   // 2-1. 使用 int 参数版本，调用时用 has_getValue<T>(0)。也可用 double/string 等参数版本，对应调用时做修改即可。
   template <typename T>
   auto has_getValue(int) -> decltype(std::declval<T>().getValue(), std::true_type{});

   // 2-2. 使用 ... 参数版本作为回退，它也可以匹配无参数的调用，因此上面不能没有参数
   template <typename T>
   std::false_type has_getValue(...);
   ```

   第一个重载使用 int 参数，更具体。第二个重载使用 ...，可以匹配任何参数，因此更通用。

2. 工作原理：
   当编译器尝试实例化 `has_getValue<T>(0)` 时，它首先尝试匹配第一个重载。
   如果 T 类型有 getValue() 方法，第一个重载成功匹配，返回 std::true_type。
   如果 T 类型没有 getValue() 方法，第一个重载的 SFINAE 失败（因为 decltype 表达式无效）。
   SFINAE 失败后，编译器不会报错，而是继续尝试下一个重载。
   第二个重载（...版本）总是可以匹配，所以它作为"回退"选项，返回 std::false_type。

3. 常见用法：

   1. 检查类是否有特定的**成员函数**：

      ```cpp
      template <typename T>
      auto has_print(int) -> decltype(std::declval<T>().print(), std::true_type{});

      template <typename T>
      std::false_type has_print(...);
      ```

   2. 检查类是否有特定的**成员类型**：

      ```cpp
      template <typename T>
      auto has_value_type(int) -> typename std::enable_if<sizeof(typename T::value_type) >= 0, std::true_type>::type;

      template <typename T>
      std::false_type has_value_type(...);
      ```

4. 优点：

   - 这种技术允许我们在**编译时检查类型特征**，而不会导致编译错误。
   - 它提供了一种**优雅的方式**来处理"类型不满足某种条件"的情况。
   - 回退版本确保了即使第一个版本失败，我们仍然有一个有效的函数可以调用。

5. 注意事项：
   - 使用 `...` 的重载应该放在其他重载之后，因为它会匹配任何东西。
   - 过度使用这种技术可能会使代码难以理解和维护。
   - C++20 引入了概念（Concepts），提供了一种更清晰、更强大的方式来实现类似的功能。

通过使用这种"回退"机制，我们可以创建强大而灵活的模板代码，能够适应各种不同的类型，同时保持**类型安全**和**编译时检查**的优势。这是 C++ 模板元编程中一个非常有用和常用的技巧，特别是在实现类型特征（type traits）和条件编译时。

# 技巧

## 用于校验的模板无需实现函数体

假如想检查一个类是否具有特定的成员函数。

```cpp
#include <type_traits>
#include <utility>

struct Foo {
    int getValue() { return 42; }
};

struct Bar {};

// 1. 通过 decltype 和逗号表达式返回 std::true_type 来确认 T 是否具备 getValue() 方法。
// 2. 下面的 has_getValue 实现属于函数模板重载，因此函数签名要不同，不能都用 typename T 和 has_getValue()。
// 2-1. 使用 int 参数版本检查是否有 getValue() 方法
template <typename T>
auto has_getValue(int) -> decltype(std::declval<T>().getValue(), std::true_type{}) {
    return std::true_type{};
}
// 2-2. 使用 ... 参数版本作为回退
template <typename T>
std::false_type has_getValue(...) {
    return std::false_type{};
}

int main() {
    static_assert(has_getValue<Foo>(0)::value, "Foo has getValue");
    static_assert(!has_getValue<Bar>(0)::value, "Bar doesn't have getValue");
}

```

将 has_getValue 函数模板改为函数声明，不提供实现。这是因为我们只需要它的返回类型，而不需要实际的函数体。

```cpp
#include <type_traits>
#include <utility>

struct Foo {
    int getValue() { return 42; }
};

struct Bar {};

// 通过 decltype 和逗号表达式返回 std::true_type 来确认 T 是否具备 getValue() 方法。
template <typename T>
auto has_getValue(int) -> decltype(std::declval<T>().getValue(), std::true_type{});

template <typename T>
std::false_type has_getValue(...);

// 定义一个 trait 来封装 has_getValue 的结果
template <typename T>
struct has_getValue_trait : decltype(has_getValue<T>(0)) {};

int main() {
    static_assert(has_getValue_trait<Foo>::value, "Foo has getValue");
    static_assert(!has_getValue_trait<Bar>::value, "Bar doesn't have getValue");
}
```

## 可变参数

> [C++学习之可变参数的函数与模板](https://songlee24.github.io/2014/07/22/cpp-changeable-parameter/)

```cpp
return_type function_name(parameter_list, ...);
```

使用 `<cstdarg>` 头文件中的宏来处理可变参数。
只能出现在形参列表的最后一个位置.
需要显式指定参数数量或使用某种约定来确定参数数量。
类型不安全，容易出错。
在现代 C++ 中，通常推荐使用更安全的替代方案，如可变参数模板。

## 模板模板参数

### 介绍与对比

在 C++ 中，模板参数通常有三种类型：**类型参数**、**非类型参数** 和 **模板参数**。其中，模板参数作为参数有两种形式：**模板作为参数** 和 **模板本身作为参数**。它们的区别主要体现在它们如何在模板中使用以及它们所代表的具体含义。

- 接受已经实例化的模板作为参数，叫做**模板参数（Template Parameter）**。
- 接受模板本身作为参数，叫做**模板模板参数（Template Template Parameter）**。

1. **模板作为参数（Template as a Parameter）**：

   “模板作为参数”指的是将一个**已经实例化的模板类型作为参数**传递给另一个模板。在这种情况下，传递的是模板的实例化类型，而不是模板的模板定义本身。

   例子：

   ```cpp
   #include <iostream>

   // 定义一个模板结构体 MyType，接受类型 T 并存储一个 T 类型的值
   template <typename T>
   struct MyType {
       T value;
   };

   // 定义一个函数模板 printValue，接受 MyType<T> 类型的对象，并打印其值
   template <typename T>
   void printValue(MyType<T> obj) {
       std::cout << obj.value << std::endl;
   }

   int main() {
       // 创建一个 MyType<int> 类型的对象，初始化值为 42
       MyType<int> obj = {42};

       // 调用 printValue 函数打印 obj 的值
       printValue(obj);  // 这里传递的是 MyType<int> 类型的对象

       return 0;
   }
   ```

   **代码解析**：

   - `MyType` 是一个模板结构体，接受一个类型 `T`。
   - `printValue` 是一个模板函数，接受一个 `MyType<T>` 类型的对象 `obj`。
   - `MyType<int>` 是模板 `MyType` 被实例化后的类型（`MyType<int>` 是一种类型），它被作为 `printValue` 函数的参数传递。也就是说，`printValue` 的参数是 `MyType<int>` 类型的对象，而不是模板本身。

2. **模板本身作为参数（Template Itself as a Parameter）**：

   “模板本身作为参数”指的是将模板的模板定义作为参数传递给另一个模板。在这种情况下，传递的是模板的定义，而不是已经实例化后的类型。

   **例子**：

   ```cpp
   #include <iostream>

   // 定义一个模板模板 MyType，用于根据传递的类型定义一个类型成员 value
   template <typename T>
   struct MyType {
       T value;
   };

   // 定义一个模板函数 printValue，接受一个模板 MyType，并打印其 value 成员
   template <template <typename> class TEMPL, typename T>
   void printValue(TEMPL<T> obj) {
       std::cout << obj.value << std::endl;
   }

   int main() {
       // 创建一个 MyType<int> 类型的对象，并初始化其 value 成员为 42
       MyType<int> obj = {42};

       // 调用 printValue 函数，传递 MyType 作为模板模板参数
       printValue<MyType>(obj);  // 传递模板类型 MyType 和模板实例化类型 int

       return 0;
   }
   ```

   **代码解析**：

   - `MyType` 仍然是一个模板，接受一个类型 `T`。
   - `printValue` 是一个接受模板模板参数 `TEMPL` 和类型 `T` 的模板函数。**`TEMPL` 是一个模板，它接受一个类型参数并定义一个类型（例如 `MyType` 模板）**。该函数接收 `TEMPL<T>` 类型的对象。
   - `printValue` 函数接受了一个模板模板参数 `TEMPL`，并且我们通过传递 `MyType` 模板以及类型 `T` 来实现更灵活的调用。
   - 通过 `MyType<int>` 类型的 `obj` 对象，推导 `printValue<MyType>` 对象的类型。

3. **区别**：

   1. **传递的内容不同**：
      - **模板作为参数**：传递的是一个已经实例化的模板类型（如 `MyType<int>`）。
      - **模板本身作为参数**：传递的是一个模板定义（如 `MyPolicy`），可以用于进一步实例化或操作。
   2. **使用方式不同**：
      - **模板作为参数**：你直接传递模板实例化后的类型（如 `MyType<int>`）作为参数传递给函数或类模板。
      - **模板本身作为参数**：你传递一个模板的模板定义（如 `TEMPL`）作为参数传递给另一个模板，允许你在模板中进一步实例化或操作它。
   3. **语法差异**：
      - **模板作为参数**：传递的是模板实例化后的类型，通常用于普通模板函数或类中作为参数。
      - **模板本身作为参数**：传递的是模板模板类型，通常用于那些能够根据传递的模板类型进行行为调整的更高级的模板设计。

   这两者的区别在于传递的是模板实例化后的类型还是模板定义本身。在模板编程中，模板本身作为参数提供了更大的灵活性，能够让你根据不同的模板定义来控制模板的行为。

4. **模板模板参数的使用场景**：

   1. **泛型容器和算法**：通过将模板模板参数用于容器类型（如 `std::vector`、`std::list` 等），可以实现更加通用和灵活的算法或数据结构。
   2. **嵌套模板的传递**：当一个模板类或函数内部需要使用其他模板类或函数时，模板模板参数提供了一种简洁的传递方式。
   3. **库设计**：比如在设计通用库时，可以使用模板模板参数来支持不同类型的容器和策略模式。
   4. **优化和定制化**：通过模板模板参数，用户可以灵活定制所使用的容器或算法模板，从而针对不同的需求进行优化。
   5. **策略模式**：我们可以传入不同的 `Policy` 模板来影响 `Navigator` 类的行为。例如，传入一个不同的 `Policy` 模板来决定 `Controller` 类型，达到一个策略模板，用于处理基本类型的矩阵乘法，另一个策略模板用于处理复杂类型或多线程环境下的矩阵乘法的目的。

      ```cpp
      template <typename IMPL>
      struct BasicPolicy {
          using Controller = int;  // 基础的控制类型
      };

      template <typename IMPL>
      struct AdvancedPolicy {
          using Controller = double;  // 更复杂的控制类型
      };

      template <typename A_TYPE, typename B_TYPE, typename C_TYPE, template <typename ...> class POLICY = BasicPolicy>
      class Navigator {
      public:
          using Controller = typename POLICY<Navigator<A_TYPE, B_TYPE, C_TYPE>>::Controller;

          void compute() {
              Controller c;
              // 根据 c 的类型执行不同的逻辑
          }
      };

      // 使用不同的策略
      Navigator<int, int, int, BasicPolicy> basicNavigator;   // 使用 BasicPolicy，Controller 为 int
      Navigator<int, int, int, AdvancedPolicy> advancedNavigator;  // 使用 AdvancedPolicy，Controller 为 double
      ```

使用模板模板参数的场景

1. **策略模式**：我们可以传入不同的 `Policy` 模板来影响 `Navigator` 类的行为。例如，传入一个不同的 `Policy` 模板来决定 `Controller` 类型。

   ```cpp
   template <typename IMPL>
   struct PolicySpecialized {
       using Controller = double;  // 更复杂的类型
   };

   Navigator<int, float, double, PolicySpecialized> Navigator;  // 使用 PolicySpecialized
   ```

### 进阶记录

1. 标准写法
   使用模板模板参数时（如 `template <typename> class POLICY`），`typename` 后无需添加具体类型名称如 `T1`。因为其中的 `typename` 并不是定义一个类型名字，而是定义一个**类型参数的占位符**。具体来说，`template <typename> class POLICY` 是一个模板模板参数，它表示一个模板类型，而该模板模板参数接受一个类型参数（例如 `T1`）。
   但 `typename` 后加上具体类型名，功能也是等价的。
   - `template <typename> class POLICY = MyPolicy` 是模板模板参数的标准写法。
   - `template <typename T1> class POLICY = MyPolicy` 也能工作，但在语法上它看起来更像是一个普通的模板类定义。
2. 可变参数模板 `typename...` 在模板模板参数中的应用
   `typename...` 也可以用于模板模板参数中，允许你**传递一个任意数量的类型参数给模板**。

   ```cpp
   template <typename... Ts>
   struct MyPolicy {
       // 模板接受多个类型参数
       using Controller = std::tuple<Ts...>;
   };

   template <typename T, template <typename...> class POLICY = MyPolicy>
   class Navigator {
   public:
       using Controller = typename POLICY<T>::Controller;
   };
   ```

   在这个例子中，`MyPolicy` 接受多个类型参数（`typename... Ts`），并将这些类型打包成一个 `std::tuple` 类型。`Navigator` 类模板的模板模板参数 `POLICY` 就是一个可以接受多个类型参数的模板。

   - `POLICY` 是一个接受多个类型参数的模板模板参数。
   - `POLICY<T>` 会被实例化成一个具体的类型，在这个例子中是 `MyPolicy<T>`，它的 `Controller` 成员是一个包含所有类型的元组（`std::tuple<Ts...>`）。

## 检查类是否有特定的**成员函数**，有几种方式
