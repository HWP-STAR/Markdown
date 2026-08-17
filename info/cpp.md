# C++学习
STL中的内容：
1. 容器（存放数据）
//容器
#include <vector>
#include <string>
#include <map>
#include <set>
#include <queue>
#include <stack>
2.算法
//算法
#include <algorithm>

3. 迭代器（容器的指针）
4. 函数对象 & 内存分配器

# 语法
int 等声明变量会分配一个新存储地址，不可以重复声明，可以赋值


operator	meaning
!	Boolean "not"
&&	Boolean "and"
||	Boolean "or"

## cpp函数
data_type func_name (parameter){
    statment;
}
返回是一个value,不会打印输出，自己调用才行

cpp编译是从到后，函数要么先声明，要么先定义（在main（）前）

所有变量要有type（int,double,bool等）

return-type fn-name(args){
    //code here
}

所有cpp程序开始
int main(){

    // code
    return 0;
}

g++ -g (保留debug信息)

gdb ./文件 #start debug

 sumOfDigitsOf 函数入口停下：

gdb
(gdb) break sumOfDigitsOf

再次运行（这次会停住）
gdb
(gdb) run

- next（n）："跳过" 函数调用，不进去看细节

- step（s）："钻进去" 函数调用，看内部执行

使用string #include <string>
str 必须使用“”，不能‘’

cout 输出
cin >> text 输入（不能读取空格） getline(cin,text) 可以读取空格


isalpha() 是 C / C++ 标准库 <cctype> 里的字符判断函数，作用：判断一个字符是不是英文字母（a-z、A-Z）。
string.size() / vector.size() / sizeof() 返回值原生就是 size_t，就是无符号的int（>=0）

type:string,double,void 使用（）强制转换类型

# struct 定义结构体（存数据）

• #include <string> → std::string
• #include <utility> → std::pair
• #include <iostream> → std::cout,std::endl

都是使用stl（标准库
using 用法
// 给 vector<string> 起别名 StringVec
using StringVec = std::vector<std::string>;）

auto使用
使用 auto 定义变量时必须立刻初始化，否则编译器无法推导类型；

# &引用 = 变量的别名（alias）
在函数中可以修改外部的变量

能写 &变量 取地址 → 左值
不能取地址、临时一瞬 → 右值

stringstream 自动以空格分隔
#include <sstream>
#include <string>

size_t 是无符号整数类型（unsigned）
# 初始化赋值
一般使用{},用不用= 都可以，{} 统一叫「初始化列表 initializer_list」
（）一般有强制转换的意义
[]是index
cpp
 C++ 容器区分不靠括号，靠左边的类型
vector<int>   v = {1,2,3};   // 动态数组
list<int>     l = {1,2,3};   // 双向链表
tuple<int,int> t = {1,2};    // 元组
map<string,int> m = {{"a",1}};//字典

# vector
push_back() 添加元素
pop_back() 只删掉最后一个，不能拿到被删掉的值！

# map 
升序排序

for(const auto& elem:container) 遍历元素
for(init;condition;操作) 遍历元素

迭代器 c.begin(),c.end(),使用*it(揭开),++it（移动）

# 遍历元素
for (const auto& elem : container) 只读访问元素
&
使用引用，不产生拷贝

++it 指向同一个(不会复制)
it++ a copy of the old value

# 指针
int* 代表指针
&是 address操作

# 在 C++ 中，struct 和 class 的唯一本质区别是：默认访问权限和默认继承方式不同
struct默认public
class默认private

# 编译
g++ main.cpp utils.cpp -o app
只要cpp文件编译即可
不用处理Header File (.h)，只要在cpp文件中导入就可以

# h文件
**.h 文件用来“声明”类（告诉别人这个类长什么样），这里只有 声明
构造函数 没有函数体 {},定义好class声明

.cpp 文件用来“实现”类（真正写代码逻辑）**

编译只要.cpp文件就可以，其他不用处理

# virtual double area() const = 0;
virtual —— 多态的关键
= 0 —— 纯虚函数的标志
double area() const ————关键部分

# h文件
#ifndef SHAPE_H （自己定义的符号）
#define SHAPE_H
————————————
#endif

# cpp比较严格
不能对同一个定义两次
cpp 不是 python

# lambda
[capture](parameters) -> return_type { 
    // 函数体 
}

[]中有 = 不可以修改 & 引用，可以修改

# Move Semantics
左值：有名字的变量，存在很久

右值：临时的值，用完就消失

#  unique_ptr
自动管理内存，离开作用域就会自动释放（就是离开函数体）