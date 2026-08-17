# python学习（CS61A）
命令	功能
python3 -m doctest lab00.py	自动运行注释内的单元测试，自动校验结果，用于代码自测
python3 -i lab00.py	运行脚本，然后进入交互环境，手动调用函数调试代码


doctest 统一书写规范
>>> 后面必须空格再写代码；
多行输入用 ... （省略号后也要空格）；
输出单独占一行，紧贴代码下方。

加 --local 参数本地离线运行，跳过邮箱认证
解锁 WWPD 问答题目（带 -u 解锁）

交互环境会把返回值展示出来，单独一行输出 'hello'，带引号。就是有什么，显示什么
脚本运行，只会显示print内容，没有‘’
只要使用print,‘’中的内容会识别为str,打印
在交互环境中，if return 被赋值，则不会输出，else 没有赋值，会输出

# 运算
%10 获取最后一位数字
//10  减少一个位数

# 阶乘
使用递归
n * f(n-1)

# 其他
可以在函数内部定义一个函数，可以实现更高level的功能

## lambda expressions
lambda <parameters>: <return expression>

and or 运算：
为什么不统一返回 True/False，而是返回原值？
Python 设计者希望 and/or 不只是 “判断真假”，还能传递数值，实现简洁的简写语法。

## python中的数值 对应 bool
数字里只有 0 是假值；
正数、负数全部都是真值（True）。

and 是两个都是True
or 是其中一个是True就可以

# function
参数是括号，从左到右传入的
函数中定义函数，可以使用多个括号
当有return时，会退出循环

/ 返回float
// 返回int

python中使用j表示复数单位
[]*n:是复制n份的意思

from math import sqrt # 要导入，pow,abs都不用
s[:-n] 就是减去最后n个元素的切片

split() 实际上是字符串（str）
字符串（str）：拥有 split()、upper()、replace() 等方法。
列表（list）：拥有 append()、pop()

# str处理
split() 返回一个list

str 和 list 都是使用[index]来索引
list.index() 获取元素索引

>>> x,y=[1,2]
>>> x
1
>>> y
2

#字典
dict.values() 查看value
dict.keys() 查看key

any(iterable)
功能：判断可迭代对象中是否至少有一个元素为 True。

# 可迭代对象and迭代器
可迭代对象 (Iterable)：list,tuple, dict, str, set
迭代器：iter(list)  有next()函数，一个一个取值，迭代器 - 只能遍历一次

只有一次，用一次，少一次

# tree
一般要for 和递归遍历
 def print_tree(t):
...     print(label(t))
...     for child in branches(t):
...             print_tree(child)

# 生成器 使用next（）或for循环
使用 yield 关键字代替 return

惰性求值（Lazy Evaluation）：按需生成，节省内存

保持状态：每次 yield 后暂停，下次继续

== 是对不同对象的判断
is 是判断是不是指向同一个东西（不是副本）

# lsit
append() 加1个
extend（） 加多个
insert(a,b) 是把b插入到a位置

# dist
使用dist[key]来操作value

# python内置函数  要使用list（）转化为list才能查看
map(func,obj)
filter(func,obj)
sorted() 默认是升序，要降序 reverse=True,可以处理数字和str


enumerate(list) - 枚举 ，返回 (idx,value)
zip(list1,list2) - 打包,一一配对，就是笛卡尔积

# 总结
map 映射逐个变，
filter 过滤条件选。
reduce 归约成单个，
any/all 布尔判断。
sum 求和 max 最大，
min 最小 sorted 排序。
enumerate 带索引，
zip 打包成元组。


有运算符号的print,使用str

# 面向对象编程
 __init__ 定义各种属性
 method 定义各种操作

 yield from partition_gen(n, m-1)	✅ 正确。把生成器里面的每一个元素依次 yield 出去。

 在 Python 中，只要一个函数体内包含了 yield 关键字，它就不再是一个普通的函数，而是变成了一个生成器函数（Generator Function）。

 yield和return 几乎一样，略有不同
 list遍历 [next(iter) for _ in range(n)]

 没括号，一个类，也可以调用
 有括号，一个实例

 # 定义在 __init__() 内部 ，是实例变量，单独的一个实例属性
 # 定义在类体中，是类变量，所有共享

 类继承，直接修改对应部分即可覆盖（重写）

 return self 可以实现链式调用，如果没有，就只能一次调用
 eg.calc.add(5).subtract(2).multiply(3).value

字典构建和list构建类似

# 类如果要初始化父类的__init__()
使用super().__init__()，先初始化，再重写

assert 条件, 错误信息	断言（Assertion）：如果条件为 False，程序抛出 AssertionError 并显示错误信息
当条件不成立，才报错

# 继承
使用 super(). fun_name 可以调用父类的函数（在重写函数时候有用）

使用递归处理Link