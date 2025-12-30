[toc]

# Excel 配置及小技巧

## 写在前面

excel 直接打开 300M 的 CSV，打开不全，有时会少加载行。避免方法是使用【数据】$\Longrightarrow$【获取数据】$\Longrightarrow$【从文本/CSV】。

## 自定义快速访问工具栏

`自动换行`、`添加或删除筛选`、`冻结窗格`、`数据透视表`、`数据透视图`、`插入折线或面积图`、`分列`、`高级筛选`、`填充颜色`、`自动调整行高`、`自动调整列宽`、`切换窗口`

## 每列单独排序

一、整体简介：多列数据同时进行升序，如上图 A2:C11 有三列数值，用公式使三列数据升序排列。

二、工具、原料：

excel、数据表格、small 函数。

三、方法：

E2=SMALL(A$2:A$11,ROW(A1))数组公式向下向右复制。
四、注意事项：

【数组公式，公式输完后，光标放在公式编辑栏同时按下 CTRL+SHIFT+回车键，使数组公式生效】

## 填充数据

1. 多单元格填充一样数据

   选中多个单元格 $\Longrightarrow$ 输入内容 $\Longrightarrow$ Ctrl + Enter

2. 循环填充序列 1,2,3,4

   选中待循环的区域，按住 ctrl 下拉

3. 空单元格快速填充上一行单元格内容

   1. 第一步：选中需要填充的区域，Ctrl+G 键弹出【定位】，选中【空值】，【定位】
   2. 第二步：= ↑ 键
   3. 第三步：Ctrl + Enter 键

## 选中指定单元格

### 区域内固定值

选中区域，按 CTRL+F，输入要定位的文字或字符，单击全部查找，再按 CTRL+A，关闭对话框，OK。（定位到固定的文字或字符）

### `CTRL + G` 定位

按 CTRL + G，然后点击“定位条件”，在勾选对话框中的对应选项，确定即可。（定位到一类特定值，例如公式，或者文字，或者数字，或者空值等等）

**Ctrl+G 定位空值报未找到单元格**

1. 选定区域
2. 先用 Ctrl+H 替换单元格内容为 aaaaa
3. 再将 aaaaa 替换为空，就可以进行空值定位了

[【Excel 中的「定位」功能用法详解】](https://zhuanlan.zhihu.com/p/36979568)

## 用滚轮左右滚动

Ctrl + shift + 滚轮：水平滚动表格

## 定位快捷键

1. 快速定位到==表格部分内容的末尾==（只能定位到表格当前内容区域的末尾，若表格中有多个内容区域，则使用方法 2）
   快捷键：Ctrl + 方向下键

2. 快速定位到==整个表格的末尾==
   快捷键：Ctrl + end 键

3. 快速定位到==表格列尾==
   快捷键：Ctrl + 方向右键

4. 快速==选中表格内容区域==
   快速选中整个表格内容区域，首先定位到首个单元格，快捷键：Ctrl + Shift + end 键。
   快速选择表格部分内容区域，定位到需要选择内容区域的末尾行与列，快捷键：Ctrl + Shift + 方向左键（选中一行），然后 Ctrl + Shift + home 键。

5. 进入==单元格编辑模式==

   快捷键：F2

   执行“文件——选项”，打开“excel 选项”对话框，勾选“高级——允许直接在单元格内编辑”即可恢复设置。

## 切换快捷键

1. 同一个 Excel 文件中，不同 sheet 间相互切换:

   Ctrl+PgDn：切换到下一个 Sheet

   Ctrl+PgUp：切换到上一个 Sheet

2. 不同 Excel 文件间切换：

   Ctrl+F6：切换到下一个工作簿窗口

   Ctrl+Shift+F6：切换到上一个工作簿窗口

## 插入行列快捷键

1. 新插入行：

   - 上方插入：选中一行，右击==>插入
   - 上方插入：选中一行，【Ctrl】+【Shift】+【+】
   - 上方插入：选中一个单元格，【Alt】【i】【r】

2. 新插入列：

   - 左侧插入：选中一列，右击==>插入
   - 左侧插入：选中一列，【Ctrl】+【Shift】+【+】
   - 左方插入：选中一个单元格，【Alt】【h】【i】【c】

3. 重复上一步：【F4]
4. 删除行：

   - 删除当前行：选中一行，【Ctrl】【-】
   - 删除当前行：选中一个单元格，【Alt】【h】【d】【r】

5. 删除列：
   - 删除当前列：选中一列，【Ctrl】【-】
   - 删除当前列：选中一个单元格，【Alt】【h】【d】【c】

## 新增 sheet 快捷键

1. 在 Excel 中添加新 sheet

   ```markdown
   快捷键：Shift+F11
   ```

2. 在 Excel 中复制现有 sheet

   ```markdown
   快捷键：选中一个工作表，按住 Ctrl 或 ⌥ Opt 并拖动，
   ```

## 设置行高列宽

Excel 中，行高所使用单位为`磅`，列宽使用单位为`1/10英寸`。填写同样的值，列宽是比较大的。

```cpp
// 行高[厘米-->磅]：cm*28.3464=
// 列宽[厘米-->1/10英寸]：cm*3.937=

// 英制长度与米制长度换算的基本关系
1英寸=2.54厘米
1厘米=0.3937英寸


1厘米=1/2.54*72磅=28.3464磅

// 英制长度
1英里(mile)=1760码=1.6093千米
1码(yard)=3英尺=0.9144米
1英尺(foot)=12英寸=0.3048米【1米=3.28084英尺】
1英寸(inch)=72磅=2.5400厘米
1磅=1/72英寸=0.035277厘米


1尺=10寸
/*====================*/
1尺=1/3米=0.33333米=33.33厘米
1寸=0.1尺=3.33厘米
```

## 多单元格填充一样数据

选中多个单元格 $\Longrightarrow$ 输入内容 $\Longrightarrow$ Ctrl + Enter

## Ctrl + num 快捷键

- 【Ctrl + 1】：打开【设置单元格格式】窗口

- 【Ctrl + 5】：对文本应用删除线

- 【Ctrl+;（分号）】：插入当前日期

- 【Ctrl+Shift+;（分号）】：插入当前时间

  > - 若要插入当前日期和时间，请按 Ctrl+;（分号），然后按空格键，接着按 Ctrl+Shift+;（分号）。

-

## 数据透视表

> [Excel 数据透视表最全干货都在这里了（合集，值得转发收藏）](https://www.jianshu.com/p/23c8984f7cc7)

### 添加新的数据列

原因:

追加新数据列之前,就已经创建了一个数据透视表,而该数据透视表没有执行更新,导致之后创建的数据透视表也无法正常显示新追加的数据列.

解决办法:
新创建数据透视表之后,右键点击透视表,选择"刷新"

### 数据透视表存放位置

1. 新工作表：

   在弹出的「创建数据透视表」工具中选择「新工作表」，单击「确定」按钮。

   > 透视表可以直接在一个 sheet 中复制，复制后的表也可以重新筛选，便于生成多个图。

2. 现有工作表：

   在弹出的「创建数据透视表」工具中选择「现有工作表」，填写在现有工作表中的位置`「Sheet2!$A$1」`（此位置不能有数据），单击「确定」按钮。

### 删除数据透视表

1. 在数据透视表中的任意位置选择一个单元格以在功能区上显示“**数据透视表工具**”。
   ![选择整个数据透视表](https://support.content.office.net/zh-cn/media/a0a68d18-84bb-4efa-bee0-7060f4a5dc9f.png)
2. 单击“**分析**”>“**选择**”，然后选择“**整个数据透视表**”。
3. 按 Delete。

## 表格行列转置

1. 复制要转置的数据
2. 在空白的单元格内点击「右键」 $\Longrightarrow$ 「选择性粘贴」 $\Longrightarrow$ 「选择性粘贴」 $\Longrightarrow$ 勾选「转置 」

## 隐藏行列快捷键

1. Ctrl+9 隐藏单元格或者区域所在的行

2. Ctrl+Shift+9 取消隐藏单元格或者区域的行

3. Ctrl+0 隐藏单元格或者区域所在的列

4. Ctrl+Shift+0 取消隐藏单元格或者区域所在的列

运行 Excel 程序后，按 F1 键，在“搜索”中输入“快捷键”，即可显示 Excel 中的所有的快捷键。

> [Excel 快捷键 Ctrl+Shift+0 不能取消隐藏列设置方法](https://zhuanlan.zhihu.com/p/369384028)

## 不复制隐藏部分

1. 选择你要复制的区域「Ctrl+A」
2. 「Alt+；」意思是选中可见部分。或者在「查找和选择 $\Longrightarrow$ 定位条件 $\Longrightarrow$ 可见单元格」
3. 「Ctrl+C」 复制粘贴到新的工作表或者工作簿，就可以了

## 整行/整列快速选中

1. 整行快速选中

   按 Shift + Space，即可选中单元格所在整行

2. 整列快速选中（不管用 `-_-`，快捷键可能被操作系统占用了 ）

   按 Ctrl + Space，即可选中单元格所在整列

## 单元格内容合并/拆分

内容拆分至多个单元格 / 内容合并至一个单元格

### 文本合并

[文本合并](https://support.microsoft.com/zh-cn/office/%E5%B0%86%E4%B8%A4%E4%B8%AA%E6%88%96%E6%9B%B4%E5%A4%9A%E4%B8%AA%E5%8D%95%E5%85%83%E6%A0%BC%E7%9A%84%E6%96%87%E6%9C%AC%E5%90%88%E5%B9%B6%E5%88%B0%E4%B8%80%E4%B8%AA%E5%8D%95%E5%85%83%E6%A0%BC-81ba0946-ce78-42ed-b3c3-21340eb164a6)

**一、CONCAT 函数合并**

1. 选择要放置合并后数据的单元格。
2. 键入“**=CONCAT(**”。
3. 首先选择要合并的单元格。
   使用逗号分隔要合并的单元格，使用引号添加空格、逗号或其他文本。
4. 在公式末尾添加括号，然后按 Enter。 示例公式可能是“**=CONCAT(A2, " Family")**”。

**二、`&` 号合并**

1. 选择要放置合并后数据的单元格。
2. 键入“=”，然后选择要合并的第一个单元格。
3. 键入“**&**”，然后使用引号（中间有一个空格）。
4. 选择要合并的下一个单元格，然后按 Enter。 示例公式可能是“**=A2&" "&B2**”。

**三、TEXTJOIN 函数**

`TEXTJOIN` 是 Excel 2016 和更高版本中引入的一个非常强大的函数，用于将多个文本项按指定分隔符连接成一个单一的文本字符串。它提供了比传统的 `&` 运算符或 `CONCATENATE` 函数更灵活的功能，特别适用于处理多个单元格的内容和需要添加分隔符的场景。

**1. `TEXTJOIN` 函数的语法**

```excel
TEXTJOIN(delimiter, ignore_empty, text1, [text2], ...)
```

参数解释：

1. **`delimiter`（分隔符）**：
   - 这是你希望插入到每个文本项之间的字符或字符串（例如空格、逗号、分号等）。
   - 如果不希望在文本项之间插入任何分隔符，可以使用空字符串 `""`。
2. **`ignore_empty`（是否忽略空单元格）**：
   - 这是一个布尔值（`TRUE` 或 `FALSE`）。
     - `TRUE`：忽略空白单元格，不会在结果中插入额外的分隔符。
     - `FALSE`：空白单元格会被视为有效项并会插入分隔符（如果分隔符存在的话）。
3. **`text1, text2, ...`（要连接的文本）**：
   - 这是你想要连接的一个或多个文本项。可以是单元格、文本字符串，或者是数组。

**2. 示例**

1. 简单的连接文本

   如果你有以下数据：

   | A     | B     | C     |
   | ----- | ----- | ----- |
   | Hello | World | Excel |

   使用 `TEXTJOIN` 连接这些文本，并在每个文本项之间加入空格：

   ```excel
   =TEXTJOIN(" ", TRUE, A1, B1, C1)

   结果：`Hello World Excel`
   - 分隔符是一个空格。
   - 由于 `ignore_empty` 参数是 `TRUE`，如果某个单元格为空，它会被忽略，不会插入额外的空格。
   ```

2. 使用其他分隔符

   假设你有以下数据：

   | A    | B   | C   |
   | ---- | --- | --- |
   | John | Doe | 25  |

   你想连接这些文本并用逗号和空格 `", "` 分隔它们：

   ```excel
   =TEXTJOIN(", ", TRUE, A1, B1, C1)

   结果：`John, Doe, 25`

   - 使用 `", "` 作为分隔符。
   - `ignore_empty` 是 `TRUE`，所以即使某个单元格为空，它也不会插入额外的逗号。
   ```

3. 忽略空白单元格

   如果你希望忽略空白单元格，例如：

   | A     | B   | C      |
   | ----- | --- | ------ |
   | Apple |     | Orange |

   你可以这样使用：

   ```excel
   =TEXTJOIN(", ", TRUE, A1, B1, C1)

   结果：`Apple, Orange`
   - 由于B1是空白的，并且 `ignore_empty` 为 `TRUE`，`TEXTJOIN` 会自动跳过它。
   ```

4. 不忽略空白单元格

   如果你希望在空白单元格之间插入分隔符，可以设置 `ignore_empty` 为 `FALSE`：

   ```excel
   =TEXTJOIN(", ", FALSE, A1, B1, C1)

   结果：`Apple, , Orange`
   - 即使B1是空的，`TEXTJOIN` 也会插入分隔符。
   ```

5. 连接大范围的单元格

你可以使用 `TEXTJOIN` 来连接一个范围内的所有单元格，例如：

```excel
=TEXTJOIN(", ", TRUE, A1:A5)

- 这会将 A1 到 A5 范围内的所有非空单元格连接起来，且使用逗号和空格作为分隔符。
```

**3. `TEXTJOIN` 的优点**

- **处理空单元格更灵活**：你可以选择是否忽略空单元格。
- **支持范围引用**：可以直接处理多个单元格范围，而不需要逐个列出单元格。
- **易于使用分隔符**：直接在公式中指定分隔符，操作更简洁。
- **支持数组**：可以连接一个数组或多个不同区域的内容。

`TEXTJOIN` 是一个功能非常强大的文本连接函数，尤其适用于需要处理多个文本单元格并添加分隔符的场景。它的灵活性和简洁性使得在数据处理和报告生成时非常有用。

### 分列

[分列](https://support.microsoft.com/zh-cn/office/%E6%8B%86%E5%88%86%E5%8D%95%E5%85%83%E6%A0%BC-f1804d0c-e180-4ed0-a2ae-973a0b7c6a23)

1. 选择要拆分其内容的一个单元格或多个单元格。

   > **重要:** 拆分内容时，它们会覆盖右侧的下一个单元格中的内容，因此请务必在该处`留有空白区域`。

2. 在“**数据**”选项卡上的“**数据工具**”组中，单击“**`分列`**”。 随即将打开“**文本分列向导**”。

3. 如果未选择“**分隔符号**”，请选择此选项，然后单击“**下一步**”。

4. 选择分隔符号以定义要拆分单元格内容的位置。 “**数据预览**”部分显示内容的显示外观。 单击“**下一步**”。

5. 在“**列数据格式**”区域中，为新的列选择数据格式。 默认情况下，这些列的数据格式与原始单元格一样。 单击“**完成**”。

### 分行

1. 选中`数据区域`，然后点击**数据-从表格**按钮，弹出**创建表**-默认勾选表包含标题，点击确定，进入 power query 编辑器。
2. 在 power query 编辑器里面，选中数据，点击<kbd>转换</kbd>选项卡，在<kbd>文本列</kbd>功能区，点击<kbd>拆分列-按分隔符拆分</kbd>。
3. 然后点击**高级选项**，选择**“拆分为行”**，最后点击**确定**，即可完成拆分到行。
4. 点击“开始”选项卡，接着点击“关闭并上载”即可完成上传数据。

> 多列数据都要分行，power query 里面先转置，再分列，在转置。

## 数值和文本互转

[Excel 数值转文本](https://zhuanlan.zhihu.com/p/92360029)

### 数值转文本

数字前加上一个`半角单引号（'）`则该数字在单元格中的存储格式会自己转为“文本格式”。在 Excel 中，`分列功能`不仅仅可以根据需求把单列数据分成多列，还可以修改数据格式。

1. 选中数据
2. 单击【`分列`】-【下一步】-【下一步】-【`文本`】
3. 确定后，就可以发现数据格式变为文本啦

> [TEXT](https://support.microsoft.com/zh-cn/office/text-%E5%87%BD%E6%95%B0-20d5ac4d-7b94-49fd-bb38-93d29371225c?ns=excel&version=19&syslcid=2052&uilcid=2052&appver=zxl190&helpid=xlmain11.chm60096&ui=zh-cn&rs=zh-cn&ad=cn) 函数太难用

### 文本转数值

1. 使用乘法运算符：`=A1*1`

## 多个表格合并

先新建一个表格，在【数据】选项下点击【新建查询】-【从文件】-【从文件夹】,选择表格所在文件夹，点击【确定】。

点击右下角选项【组合】下拉小三角，选中【合并并转载数据】；在弹出窗口的下选择【Sheet 1】，点击【确定】，简单几步，就搞定了。

1. 先新建一个表格或 sheet，在【数据】选项下点击【获取数据】-【自文件】-【从工作簿】，选择要合并表格的文件，会弹出**“导航器”**窗口，点击【选择多项】并选择要合并的 sheet（可用 shift 多选），点击右下【转换数据】。

2. 弹出的**“Power Query 编辑器”**中，在**【主页】**选项卡的**【组合】**组中单击**【追加查询-下拉箭头】**功能，选择**【将查询追加为新查询】**。
3. 在弹出的**“追加”**窗口中，选择**【三个或更多表】**，把表添加到右侧要追加的表（可用 shift 多选），然后点击**【确定】**，在点击左上角**【关闭并上载】**。
4. 这样会回到 excel 窗口，右侧会出现**“查询&连接”**侧边框，点击新追加的查询结果即为合并后的结果。

> 会

## 绝对引用中$

```bash
一般情况下默认使用相对引用，不加$符号。使用绝对引用意味着不希望复制公式时公式中的行列变化。

$A$1是绝对引用，$A$1在复制公式时，行列均不会变化；
$A1、A$1是混合引用，$A1在复制公式时列不会变化，行会变化；A$1在复制公式时行不会变化，列会变化。

具体情况举例说明：
1、相对引用，复制公式时地址跟着发生变化，如C1单元格有公式：=A1+B1
当将公式复制到C2单元格时变为：=A2+B2
当将公式复制到D1单元格时变为：=B1+C1

2、绝对引用，复制公式时地址不会跟着发生变化，如C1单元格有公式：=$A$1+$B$1
当将公式复制到C2单元格时仍为：=$A$1+$B$1
当将公式复制到D1单元格时仍为：=$A$1+$B$1

3、混合引用，及锁定公式中的行或列。如C1单元格有公式：=$A1+B$1
当将公式复制到C2单元格时变为：=$A2+B$1
当将公式复制到D1单元格时变为：=$A1+C$1
锁定行同理。
```

> 注：输入或选择单元格地址后，按 `F4` 可以切换相对引用、绝对引用、混合引用。

## 数据行列转换

EXCEL 中一列（行）转多行多列或多行多列转一列（行）

<https://zhuanlan.zhihu.com/p/68901540>

## 常用函数

> https://support.microsoft.com/zh-cn/office/bitrshift-%E5%87%BD%E6%95%B0-274d6996-f42c-4743-abdb-4ff95351222c

### 数值计算

1. 相应范围或数组的个数之和

   **SUMPRODUCT**函数返回相应范围或数组的个数之和。 默认操作是乘法，但也可以执行加减除运算。

   若要使用默认操作 (乘法) ：

   ```vb
   =SUMPRODUCT (array1， [array2]， [array3]， ...)
   ```

   | 参数                             | 说明                                                |
   | :------------------------------- | :-------------------------------------------------- |
   | **array1** 必需                  | 其相应元素需要进行相乘并求和的第一个数组参数。      |
   | **[array2]， [array3],...** 可选 | 2 到 255 个数组参数，其相应元素需要进行相乘并求和。 |

   **执行其他算术运算**：像往常一样使用 SUMPRODUCT，但请将分隔数组参数的逗号替换为所需的算术运算符 (`*、/、+、-`) 。 执行所有操作后，结果将像往常一样进行求和。

### 进制转换

1. 十进制转十六进制

   DEC2HEX(number, [places])

   DEC2HEX 函数语法具有下列参数：

   - **Number** 必需。 要转换的十进制整数。 如果数字为负数，则忽略 places，且 DEC2HEX 返回 10 个字符的（40 位）十六进制数，其中最高位为符号位。 其余 39 位是数量位。 负数由二进制补码记数法表示。
   - **Places** 可选。 要使用的字符数。 如果省略 places，则 DEC2HEX 使用必要的最小字符数。 Places 可用于在返回的值前置 0（零）。

2. 将十六进制数转换为十进制数

   HEX2DEC(number)

   HEX2DEC 函数语法具有下列参数：

   - **Number** 必需。 要转换的十六进制数。 Number 不能包含超过 10 个字符（40 位）。 Number 的最高位为符号位。 其余 39 位是数量位。 负数由二进制补码记数法表示。

   | =HEX2DEC("A5")         | 将十六进制数 A5 转换为十进制数         | 165  |
   | ---------------------- | -------------------------------------- | ---- |
   | =HEX2DEC("FFFFFFFF5B") | 将十六进制数 FFFFFFFF5B 转换为十进制数 | -165 |

### 位操作

1. 按位与

   BITAND( number1, number2)

   BITAND 函数语法具有下列参数。

   - **Number1** 必需。 必须为十进制格式且大于等于 0。
   - **Number2** 必需。 必须为十进制格式且大于等于 0。

   | =BITAND(13,25) | 比较 13 和 25 的二进制表示形式。 | 9   | 13 的二进制表示形式是 1101，25 的二进制表示形式是 11001。 他们的二进制数字在最右端和从右侧开始第四个位置相匹配。 此结果将作为 (2^0)+ (2^3) 或 9 返回。 |
   | -------------- | -------------------------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |

2. 右移位

   BITRSHIFT(number, shift_amount)

   BITRSHIFT 函数语法具有下列参数。

   - **Number** 必需。 必须是大于或等于 0 的整数。
   - **Shift_amount** 必需。 必须是整数。

   | =BITRSHIFT(13,2) | 通过删除以二进制表示的数字最右边指定的位数，使数字右移相应位数。 返回的数值以十进制表示。 | 3   | 13 以二进制表示为 1101。 删除最右边的两位数将得到 11，即十进制值 3。 |
   | ---------------- | ----------------------------------------------------------------------------------------- | --- | -------------------------------------------------------------------- |

> 1、提取高 16bit：
>
> ```vb
> =BITRSHIFT(BITAND(OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-1), HEX2DEC("FFFF0000")),16)
> 或
> =BITRSHIFT(BITAND(L6496, HEX2DEC("FFFF0000")),16)
> ```

### 字符串

1. 字符子串 `LEFT`

   LEFT 从文本字符串的第一个字符开始返回指定个数的字符。

   LEFTB 基于所指定的字节数返回文本字符串中的第一个或前几个字符。

   LEFT(text, [num_chars])

   LEFTB(text, [num_bytes])

   该函数语法具有下列参数：

   - **文本** 必需。 包含要提取的字符的文本字符串。
   - **num_chars** 可选。 指定要由 LEFT 提取的字符的数量。
   - **Num_bytes** 可选。 按字节指定要由 LEFTB 提取的字符的数量。

2. 字符子串 `MID`

   MID 返回文本字符串中从指定位置开始的特定数目的字符，该数目由用户指定。

   MIDB 根据您指定的字节数，返回文本字符串中从指定位置开始的特定数目的字符。

   MID(text, start_num, num_chars)

   MIDB(text, start_num, num_bytes)

   MID 和 MIDB 函数语法具有下列参数：

   - **文本** 必需。 包含要提取字符的文本字符串。
   - **start_num** 必需。 文本中要提取的第一个字符的位置。 文本中第一个字符的 start_num 为 1，以此类推。
   - **num_chars** MID 必需。 指定希望 MID 从文本中返回字符的个数。
   - **Num_bytes** MIDB 必需。 指定希望 MIDB 从文本中返回字符的个数（字节数）。

3. 连接字符串 `CONCAT`

   CONCAT(text1, [text2],…)

   text1 (必需的)要联接的文本项。 字符串或字符串数组，如单元格区域。

   [text2， ...] (可选)要联接的其他文本项。 文本项最多可以有 253 个文本参数。 每个参数可以是一个字符串或字符串数组，如单元格区域。

   例如，=CONCAT("明"," ","天"," ","将"," ","有"," ","日"," ","出。 ") 将返回**明天将有日出。**

   **提示:** 若要在要合并的文本之间包含分隔符 (（例如间距或放大器 **(&**) ) ，以及删除不希望显示在组合文本结果中的空参数，可以使用 [TEXTJOIN 函数](https://support.microsoft.com/zh-cn/office/textjoin-函数-357b449a-ec91-49d0-80c3-0e8fc845691c)。

4. 格式化为文本 `TEXT`

   TEXT 函数会将数字转换为文本，这可能使其在以后的计算中难以引用。 最好将原始值保存在一个单元格中，然后在另一单元格中使用 TEXT 函数。 随后如果需要构建其他公式，请始终引用原始值，而不是 TEXT 函数结果。

   TEXT 函数最简单的形式表示：

   - **=TEXT(Value you want to format, "Format code you want to apply")**

   下面是一些常用示例，可将其直接复制到 Excel 自行进行试验。 请注意引号内的格式代码。

   | **公式**                        | **说明**                                                                                        |
   | ------------------------------- | ----------------------------------------------------------------------------------------------- |
   | =TEXT(1234.567,**"$#,##0.00"**) | 货币带有 1 个千位分隔符和 2 个小数，如 $1,234.57。 请注意，Excel 将该值四舍五入到小数点后两位。 |
   | = TEXT(TODAY()，**"MM/DD/YY"**) | 目前日期采用 YY/MM/DD 格式，如 12/03/14                                                         |
   | =TEXT(TODAY(),**"DDDD"**)       | 一周中的当天，如周日                                                                            |

   **注意:** 虽然可使用 TEXT 函数更改格式，但这不是唯一的方法。 你可以通过按 **CTRL+1** （或在 Mac 上按 ![MAC Command 按钮图标的图像](https://support.content.office.net/zh-cn/media/b7f18703-a23f-4d8c-81e4-4488ea64c049.png)**+1**)来更改不带公式的格式，然后在**设置单元格** > **数字**对话框中选择所需的格式。

5. 文本字符串替换 `SUBSTITUTE`

   如果需要在某一文本字符串中替换指定的文本，请使用函数 SUBSTITUTE；如果需要在某一文本字符串中替换特定位置处的任意文本，请使用函数 REPLACE。

   SUBSTITUTE(text, old_text, new_text, [instance_num])

   SUBSTITUTE 函数语法具有下列参数：

   - **text** 必需。 需要替换其中字符的文本，或对含有文本（需要替换其中字符）的单元格的引用。
   - **old_text** 必需。 需要替换的文本。
   - **new_text** 必需。 用于替换 old_text 的文本。
   - **Instance_num** 可选。 指定要将第几个 old_text 替换为 new_text。 如果指定了 instance_num，则只有满足要求的 old_text 被替换。 否则，文本中出现的所有 old_text 都会更改为 new_text。

   | **公式**                                     | **描述（结果）**                        | **结果**         |
   | -------------------------------------------- | --------------------------------------- | ---------------- |
   | =SUBSTITUTE("销售数据", "销售", "成本")      | 将“销售”替换为“成本”（成本数据）        | 成本数据         |
   | =SUBSTITUTE("2008 年第 1 季度", "1", "2", 1) | 将第一个 1 替换为 2（2008 年第 2 季度） | 2008 年第 2 季度 |
   | =SUBSTITUTE("2011 年第 1 季度", "1", "2", 2) | 将第二个 1 替换为 2（2012 年第 1 季度） | 2012 年第 1 季度 |

   ```vb
   // 统计 左侧单元格 字符串中 "_" 字符的个数
   =(LEN(OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-1)) - LEN(SUBSTITUTE(OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-1),"_",""))) / LEN("_")
      =(LEN(B480)-LEN(SUBSTITUTE(B480,C480,"")))/LEN(C480)

   // 拼接左侧两列字符串
   =CONCAT(OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-2),"-",OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-1))

   // 隔行填写1
   =IF(MOD(ROW(),2),1,0)
   ```

6. 文本搜索提取 `MID + FIND`

   在 A1 中查找 B1 字段直至后面的`,`:

   ```vb
   =MID($A$1,
        FIND(B1&" ",$A$1)+LEN(B1)+1,
        IFERROR(
          FIND(",", $A$1, FIND(B1&" ",$A$1))
          - FIND(B1&" ",$A$1) - LEN(B1) - 1,
          LEN($A$1)
        )
   )
   ```

### 匹配函数

在 Excel 中，用于**根据某个值查找对应数据**的函数主要有两个：`VLOOKUP` 和 `XLOOKUP`（后者在 Excel 365/2021 可用）。它们的适用场景和用法如下：

**一、VLOOKUP（老牌函数，兼容性好）**

1. **语法：**

   ```excel
   VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
   ```

   - `lookup_value`：要查找的值
   - `table_array`：查找的表格区域。<u>**请记住，查阅值应该始终位于所在区域的第一列，这样 VLOOKUP 才能正常工作。**</u>
   - `col_index_num`：返回结果所在列序号（从 table_array 的第一列开始算）
   - `range_lookup`（可选）：
     - `TRUE` 或省略 → 近似匹配（必须按升序排序）
     - `FALSE` → 精确匹配（推荐）

   > 如果要返回特定的文本而不是＃N/A 值，则可以应用以下公式：
   > `= IFERROR（VLOOKUP（D2，A2：B10,2，FALSE），“具体文字“）`

2. **示例：**

   | A 列 | B 列 |
   | ---- | ---- |
   | 101  | 苹果 |
   | 102  | 香蕉 |
   | 103  | 梨   |

   公式：查找 102 对应的水果名称

   ```excel
   =VLOOKUP(102, A1:B3, 2, FALSE)
   ```

   结果：`香蕉`

3. VLOOKUP 的限制

   1. **只能向右查找**：lookup_value 必须在 table_array 的第一列
   2. **插入/删除列容易出错**：col_index_num 是固定数字
   3. **性能不如 XLOOKUP**

**二、XLOOKUP（新函数，Excel 365 / 2021 可用）**

1. **语法：**

   ```excel
   XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])
   ```

   - `lookup_value`：要查找的值
   - `lookup_array`：查找的列/行
   - `return_array`：返回结果的列/行
   - `[if_not_found]`（可选）：找不到时显示内容
   - `[match_mode]`（可选）：
     - 0 → 精确匹配（默认）
     - -1 → 精确匹配或小于
     - 1 → 精确匹配或大于
     - 2 → 通配符匹配
   - `[search_mode]`（可选）：
     - 1 → 从首到尾（默认）
     - -1 → 从尾到首

2. **示例：**同上表，查找 102 对应的水果

   ```excel
   =XLOOKUP(102, A1:A3, B1:B3, "未找到")
   ```

   结果：`香蕉`

3. **XLOOKUP 的优点**

   1. **可以向左或向右查找** → 不再受列位置限制
   2. **可自定义未找到提示**
   3. **支持精确/近似/通配符匹配**
   4. **语法更直观，可维护性好**

**三、总结建议**

| 场景                          | 推荐函数          |
| ----------------------------- | ----------------- |
| Excel 2016 / 2019 / LTSC 2021 | VLOOKUP           |
| Excel 365 / 2021（更新版）    | XLOOKUP（更灵活） |
| 需要向左查找                  | XLOOKUP           |
| 需要找不到显示提示            | XLOOKUP           |
| 简单查找、兼容旧版本          | VLOOKUP           |

- 如果使用 **VLOOKUP**，可以结合 `MATCH` 动态获取列号，减少硬编码
- 如果使用 **XLOOKUP**，可以直接用列范围或整个表格列引用，更稳健

### 查找函数

1. 查找 FIND

   函数 FIND 和 FINDB 用于在第二个文本串中定位第一个文本串，并返回第一个文本串的起始位置的值，该值从第二个文本串的第一个字符算起。

   （这些函数可能并不适用于所有语言。FIND 适用于使用单字节字符集 (SBCS) 的语言，而 FINDB 适用于使用双字节字符集 (DBCS) 的语言。 支持 DBCS 的语言包括日语、中文（简体）、中文（繁体）以及朝鲜语）

   FIND(find_text, within_text, [start_num])

   FINDB(find_text, within_text, [start_num])

   FIND 和 FINDB 函数语法具有下列参数：

   - **find_text** 必需。 要查找的文本。
   - **within_text** 必需。 包含要查找文本的文本。
   - **start_num** 可选。 指定开始进行查找的字符。 within_text 中的首字符是编号为 1 的字符。 如果省略 start_num，则假定其值为 1。

   > - FIND 和 FINDB ==区分大小写==，并且==不允许使用通配符==。 如果您不希望执行区分大小写的搜索或使用通配符，则可以使用 SEARCH 和 SEARCHB 函数。

   | **数据**        |                                                 |          |
   | --------------- | ----------------------------------------------- | -------- |
   | Miriam McGovern |                                                 |          |
   | **公式**        | **说明**                                        | **结果** |
   | =FIND("M",A2)   | 单元格 A2 中第一个“M”的位置                     | 1        |
   | =FIND("m",A2)   | 单元格 A2 中第一个“M”的位置                     | 6        |
   | =FIND("M",A2,3) | 从单元格 A2 的第三个字符开始查找第一个“M”的位置 | 8        |

2. 查找 SEARCH

   SEARCH 和 SEARCHB 函数可在第二个文本字符串中查找第一个文本字符串，并返回第一个文本字符串的起始位置的编号，该编号从第二个文本字符串的第一个字符算起。

   > - **SEARCH** 和 **SEARCHB** 函数==不区分大小写==。 如果要执行区分大小写的搜索，可以使用 **FIND** 和 **FINDB** 函数。
   > - 可以在 **find_text** 参数中==可以使用通配符== （问号 (`?`) 和星号 (`*`)） 。 问号匹配任意单个字符；星号匹配任意一串字符。 如果要查找实际的问号或星号，请在字符前键入波形符 (`~`)。

### 计数函数

1. COUNTIF 函数

   COUNTIF 是一个[统计函数](https://support.microsoft.com/zh-cn/office/统计函数-参考-624dac86-a375-4435-bc25-76d659719ffd)，用于统计满足某个条件的单元格的数量；

   COUNTIF 的最简形式为：

   - =COUNTIF(要检查哪些区域? 要查找哪些内容?)

   例如：

   - =COUNTIF(A2:A5,"London")
   - =COUNTIF(A2:A5,A4)

关于 Excel 去重计数的方法，比较准确又高效的方法，就是在直接在单元格 C1 中输入公式“=SUMPRODUCT(1/COUNTIF(A1：A10，A1：A10))”，公式的含义就是统计 A1:A10 单元格区域有 A1 至 A10 单元格数据的个数。

> 1. 去重计数
>
>    比较准确又高效的方法，就是在直接在单元格中输入下面公式，公式的含义就是统计 A1:A10 单元格区域有 A1 至 A10 单元格数据的个数。
>
>    ```vb
>    =SUMPRODUCT(1/COUNTIF(A1：A10，A1：A10))
>    ```
>
> 2. x

### 日期和时间函数

> [日期和时间函数（参考）](https://support.microsoft.com/zh-cn/office/%E6%97%A5%E6%9C%9F%E5%92%8C%E6%97%B6%E9%97%B4%E5%87%BD%E6%95%B0-%E5%8F%82%E8%80%83-fd1b5961-c1ae-4677-be58-074152f97b81)

1. HOUR 函数

   HOUR(serial_number)

   HOUR 函数语法具有下列参数：

   - **Serial_number** 必需。 时间值，其中包含要查找的小时数。 时间值有多种输入方式：带引号的文本字符串（例如 "6:45 PM"）、十进制数（例如 0.78125 表示 6:45 PM）或其他公式或函数的结果（例如 TIMEVALUE("6:45 PM")）。

   | **时间**       |                             |          |
   | -------------- | --------------------------- | -------- |
   | 2011-7-18 7:45 | A3 单元格内容               |          |
   | **公式**       | **说明**                    | **结果** |
   | =HOUR(A3)      | 返回日期/时间值的小时部分。 | 7        |

2. MINUTE 函数 ：MINUTE(serial_number)

3. SECOND 函数：SECOND(serial_number)

4. YEAR 函数：YEAR(serial_number)

5. MONTH 函数：MONTH(serial_number)

6. DAY 函数：DAY(serial_number)

7. TEXT 分离日期和时间：=TEXT(A2,"yyyy/m/dd")，或者=TEXT(A2,"hh:mm:ss")

> 1、提取时间
>
> ```c++
> // 1、获取小时：
> =HOUR(OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-1))
> // 2、获取分钟：
> =MINUTE(OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-2))
> // 3、拼接日期和时间
> =CONCAT(TEXT(OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-2), "YYYY-MM-DD"), " ",
> TEXT(OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-1), "hh:mm:ss"))
> ```
>
> 2、格式化单元格
>
> ==单元格格式==应该设置成`**常规**`才能正确显示，否则单元格格式为`时间`则显示 0:00:00。
>
> 方法 1：按 `CTRL + 1`，然后选择“**常规**”。
>
> 方法 2：在“**开始**”选项卡的下拉列表中选择“**数字**”，选择所需格式。

### 其他

- 使用 IF 检查单元格是否为空白：`ISBLANK(D2)`

  ```vb
  =IF(NOT(ISBLANK(O2)),
      O2,
      IF(AND(NOT(ISBLANK(G2)), G2>=28),
          G2,
          "")
      )
  ```

- 将 IF 函数与 AND、OR 以及 NOT 函数配合使用

  ```vb
   IF(AND())、IF(OR()) 和 IF(NOT())
  ```

- 计算父级百分比下不止一个的

  ```vb
  //第一版
  =IF(AND(
          OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-1)=1,
          OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),1,-1)=1),
      0,
      1)
  //2-一父多子，1-子级，0-一父一子
  =IF(AND(
          OR(OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-1) = 1,OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-1) = ""),
          OR(OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),1,-1) = 1,OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),1,-1) = "")),
      0,
      IF(AND(
              OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),0,-1) = 1,
              OFFSET(INDIRECT(ADDRESS(ROW(), COLUMN())),1,-1) < 1),
              2,
              1)
      )
  ```

## 图表

### 折线图横坐标

1. 图表上右击“**选择数据**”。
2. 在打开的选择数据对话框中的**水平(分类)轴标签**，点击“**编辑**”。
3. 选中新的单元格内容，即可发现原本显示的数字变成新输入的内容了。

### 折线图新增折线

1. 图表上右击“**选择数据**”。
2. 在打开的选择数据对话框中的**图例项(系列)**，点击“**添加**”。
3. 系列名称选**要添加列的首行**的名称，系列值选**要添加列中除首行外**的具体值（删掉原有的={1}）。
4. 选中新的单元格内容，即可发现原本显示的数字变成新输入的内容了。

### 散点图添加拟合曲线

1. 选择数据**绘制散点图**。
2. 选中散点图后，右侧有几个快捷按钮，点击**”加号“**，里面选择**”趋势线“**。
3. **双击**添加后的趋势线就可以进入**“设置趋势线格式”**侧边栏，选择需要拟合的方式如线性、多项式等。

### 散点图修改点大小

图案——数据标记——选“自定义”——“大小”调成 2 磅或更小——确定

散点图中，【选中点】-->【右键】【“设置数据系列格式"】，在弹出的对话框中选择”数据标记选项“，把大小后面的数值调整就可以了。

## 筛选

使用通配符：即问号 (?) 和星号 (\*)。 `问号匹配任何单个字符。 星号匹配任何字符序列`。 如果要查找实际的问号或星号，则在字符前键入代字号 (~)。

### 高级条件筛选

1. 准备**列表区域，如 A1:D6**，**条件区域，如 F1:G2**。

   条件区域即为要筛选的数据：内容根据自己需求写，其格式数据仿照下面例子准备。**条件区域也可以放在其他 sheet 中**。

   |     |  A   |  B   |  C   |  D   | E   |  F   |  G   |
   | :-: | :--: | :--: | :--: | :--: | --- | :--: | :--: |
   |  1  | 班级 | 语文 | 数学 | 英语 |     | 班级 | 英语 |
   |  2  | 1 班 | 125  | 150  | 121  |     | 1 班 | 150  |
   |  3  | 1 班 | 120  | 148  | 124  |     |      |      |
   |  4  | 1 班 | 137  | 130  | 150  |     |      |      |
   |  5  | 1 班 | 115  | 147  | 136  |     |      |      |
   |  6  | 2 班 | 145  | 116  | 128  |     |      |      |

2. 在**“数据”**选项卡的**“排序和筛选”**组中单击**“高级”**按钮。

3. 在**“高级筛选”**界面中，**“列表区域”**文本框中需要**输入选择区域的单元格地址**，在**“条件区域”**文本框中输入筛选条件所在的单元格区域地址。**可再文本框中单击后，直接利用鼠标**在表格中选择区域。

   > 注：
   >
   > 1. “方式”中**“将筛选结果赋值到其他位置”**，需要操作“复制到”框框，且**只能复制到正在活动的 sheet**，意味着此时要在**想要复制到的 sheet 中**打开“高级筛选”界面。
   > 2. **“条件区域”**：不要选择整列，否则结果是没有筛选。

4. 点击**“高级筛选”**中的**“确定”**，需要的数据就被筛选出来了。

> 取消高级筛选：
>
> 在**“开始”**选项卡的**“编辑”**组中单击**“排序和筛选”**功能，在弹出框里选择**“清除”**选项即可。

### 筛选条件

4、通配符筛选。`???`

5、关键字+通配符筛选。`李?`

> ```wiki
> 提示: 可以在 Excel 搜索条件中使用 通配符 - 问号 （？）、星号 （*）、字号 （~）。
> - 使用问号 （？） 查找任意单个字符，例如，s？t 可找到"sat"和"set"。
> - 使用星号 （*） 查找任意多个字符(不匹配0个)，例如，sd 可找到"sad"和"started"。
> - 使用字号 （~） 后跟 ？、*或 ~ 查找问号、星号或其他代字 -例如 fy91~？ 找到"fy91？"。
> ```
>
> 假如列中包含`11_11_11_11`、`11_11`、`11`、`117_117_117_117`、`117_117`、`117`，如果想用高级筛选`11_11_11_11`、`11_11`、`11`，可以使用条件：`'=11*11`和`'=11`。

6、指定数据范围筛选。`300`

> 除了“大于>”之外，还有“等于=”、“不等于<>”、“大于或等于>=”、“小于<”、“小于或等于<=”等多种方式。

7、高级条件

筛选"销量"＞ 200 且＜ 300 和＞ 350 且＜ 400

| 销量 | 销量 |     |     |
| ---- | ---- | --- | --- |
| >200 | <300 |     |     |
| >350 | <400 |     |     |

> [Excel 筛选与高级筛选的 15 个应用技巧解读！](https://zhuanlan.zhihu.com/p/194389852)
>
> [玩转 Excel 数据透视表筛选，看这一篇就够了！](https://www.sohu.com/a/141945734_695443)

## 宏

> Microsoft 文档：[Office VBA 参考](https://learn.microsoft.com/zh-cn/office/vba/api/overview/)
>
> [Excel VBA 编程教程](https://www.w3cschool.cn/excelvba/)
>
> [Excel VBA：单元格对象](https://blog.csdn.net/qq_36551226/article/details/106833877?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-106833877-blog-106648689.235^v39^pc_relevant_3m_sort_dl_base4&spm=1001.2101.3001.4242.1&utm_relevant_index=1)
>
> [VBA 中日期和时间相关的计算](https://blog.51cto.com/alun51cto/2425920)

### 运行宏的方法

1. 菜单栏【开发工具】-> 【查看宏】 -> 【点击要执行的宏】

2. 快速打开宏对话框：Alt+F8 -> 【点击要执行的宏】

3. 自定义菜单栏运行宏

   方法：？？

4. 通过工作表里面的按钮运行宏

   方法：？？

5. ？？

### 参考宏

1. 首行\_换行筛选冻结

   ```vb
   Sub 首行_换行筛选冻结()
   '
   ' 首行_换行筛选冻结 宏
   '

   '
       Rows("1:1").Select
       With Selection
           .WrapText = True
       End With
       Selection.AutoFilter
       With ActiveWindow
           .SplitColumn = 0
           .SplitRow = 1
       End With
       ActiveWindow.FreezePanes = True
       Range("A1").Select
   End Sub
   ```

2. 首列\_文本时间插入

   ```vb
   Sub 首列_文本时间插入()
   '
   ' 首列_文本时间插入 宏
   '

   '
       Columns("A:A").Select
       Selection.Insert Shift:=xlToRight, CopyOrigin:=xlFormatFromLeftOrAbove
       Range("A1").Select
       ActiveCell.FormulaR1C1 = "时间"
       ' A2单元格公式填充
       Range("A2").Select
       ActiveCell.FormulaR1C1 = "=TEXT(RC[1],""HH:MM:SS"")"
       ' A2-Axx公式填充
       curSheetColumn = ActiveSheet.UsedRange.Rows.Count
       Set SourceRange = ActiveSheet.Range("A2")
       Set fillRange = ActiveSheet.Range(Cells(2, 1), Cells(curSheetColumn, 1))
       SourceRange.AutoFill Destination:=fillRange
       Range("A2:A110508").Select
       Range("A1").Select
   End Sub
   ```

3. 创建透视表\_490

   ```vb
   Sub 创建透视表_490()
   '
   ' 创建透视表_490 宏
   '

   '
       ' 生成透视表名字、透视表sheet名字
       Dim timeStamp As Date
       Dim tableName As String, sheetName As String
       timeStamp = Now()
       tableName = Month(timeStamp) & "_" & Day(timeStamp) & "T" & _
           Hour(timeStamp) & "_" & Minute(timeStamp) & "_" & Second(timeStamp)
       sheetName = "Sheet" & tableName

       ' 生成透视区域、透视表位置
       Dim sourceData As String, tableDest As String
       sourceData = ActiveSheet.Name & "!" & ActiveSheet.UsedRange.Address(ReferenceStyle:=xlR1C1)
       tableDest = sheetName & "!" & "R3C1"

       ' 新建sheet页，创建透视表
       Sheets.Add.Name = sheetName
       ActiveWorkbook.PivotCaches.Create(SourceType:=xlDatabase, sourceData:= _
           sourceData, Version:=7).CreatePivotTable _
           tableDestination:=tableDest, tableName:=tableName, DefaultVersion:=7

       ' 选中透视页，增加透视字段
       Sheets(sheetName).Select

       Dim pt As PivotTable
       Dim pf As PivotField
       Dim dataField As PivotField

       Set pt = ActiveSheet.PivotTables(tableName)
       ' 检查透视表是否存在
       If Not pt Is Nothing Then
           ' 添加字段到透视表的行区域
           Set pf = pt.PivotFields("bit08AirSlotNoInFrm") ' 替换为你实际的字段名称
           With pf
               .Orientation = xlRowField
               .Position = 1
           End With

           ' 添加字段到透视表的列区域
           Set pf = pt.PivotFields("totalReNum") ' 替换为你实际的字段名称
           With pf
               .Orientation = xlColumnField
               .Position = 1
           End With

           ' 添加同一字段到透视表的值区域，并设置为求和
           Set pf = pt.PivotFields("totalReNum") ' 替换为你实际的字段名称
           pf.Orientation = xlDataField
           pf.Function = xlSum
           pf.Name = "求和项:totalReNum"
       Else
           MsgBox "透视表未找到！", vbExclamation
       End If

   End Sub

   ```

## 其他

1. [方方格子](https://dumuzhou.org/1553.html) excel 超好用插件

2. [教程：创建 Excel 任务窗格加载项](https://docs.microsoft.com/zh-cn/office/dev/add-ins/tutorials/excel-tutorial)

3. [Kutools For Excel 26.10](https://www.extendoffice.com/product/kutools-for-excel.html)

4. [Office Tab 14.50](https://www.extendoffice.com/product/office-tab.html)

5. [吾爱破解](https://www.52pojie.cn/thread-1220396-1-1.html)

## 解析工具操作

REQ：

caServingCellNum：WU 列
