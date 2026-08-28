# \t 类似 tab功能

%d 是int,%f是float 
a.b 是a位宽度，b位小数

#define name 量 #定义常量

ctrl+d 代表 EOF

# 作用域
在函数中，离开就消失，就会重新开始

# 外部变量
一直保存，函数对他的改变会保留

‘’是字符,对应ASCII数值，“”是字符串，有字母和\0

# ASCII
'0' is 48，'1' is 49 ，一段是连续的,'A' is 65 ,'a' is 97
%d is int, %c is char
%zu is size_t

# printf
printf 的第一个参数必须是 const char *（格式字符串），而你传了一个 int，只能打印string/char

# ASCII
标准 ASCII（7 位）范围是：0 ～ 127

类别	范围	是否可显示
控制字符（Control）	0 ～ 31，127	❌ 不可显示
可打印字符（Printable）	32 ～ 126	✅ 可显示

# 强制类型转换
（type_name）表达式
原来的数值不会改变，智慧生成一个指定类型的数值

# 前++和后++
++n,是先+1,后使用变量n
n++，是先使用变量n,后+1

# 赋值缩写
+ - * / % << >> &^| 等都可以使用
eg i+=2

或者
expr1 op= expr2 #都是表达式，不用括号
eg:x+1 *= y+3 is x+1 = (x+1) *(y+3)
eg:x=y+1 is x =x*(y+1)

0是八进制前缀，0x是十六进制前缀，一般是十进制，没有前缀

# 条件判断
expr1 ? expr2 : expr3

若expr1 is True 则返回expr2,否则expr3

# 数组int v[]=...
v 代表数组，v[] 代表数组初始化

# switch 使用
break使用：防止执行后面的case,没有break会按顺序执行
case 只是一个标志

switch(表达式){
    case value:语句;  # 可以多个case共用

    default:语句;
}

# 循环
while,for执行前会终止条件进行测试
do-while 执行后进行测试

创建空数组要指定大小，有初始化不用指定

for 后使用; 表示不进行处理

# float舍入
四舍五入，中间值就向偶数（末尾是0）

运算： 对齐统一指数，后二进制直接算，*2^n or *2^-n,就是位移操作（左右位移）


# 头文件 
// math_utils.h
#ifndef MATH_UTILS_H  //自己定义的符号
#define MATH_UTILS_H

int add(int a, int b);
int sub(int a, int b);  //对外的函数接口

#endif

编译：把所有的.c文件一起编译

# 静态变量 static
- 函数内的静态局部变量
作用域：仅在函数内部可见
生命周期：程序整个运行期间都存在
只初始化一次，函数调用结束后值不会消失

- 文件内的静态全局变量/函数
只在文件内使用，外部无法访问

# 初始化
使用“=” 来显示赋值，可以多个一起初始化

char pattern[] = "ould ";
字符串初始化等价：
char pattern[] = { 'o', 'u', 'l', 'd'};

# 条件编译

#ifdef DEBUG // 有定义就编译,之前要使用define定义
    printf("调试模式开启\n");


#endif //结束

# 防止重复
#ifndef MYLIB_H
#define MYLIB_H

void foo(void);
int bar(int x);

#endif

# 指针
& 取地址

char message[] = "hello" #定义字符数组
char *message = "hello" #定义指针

指针和数组在大多数表达式中是等价的，
p[i] 本质上就是 *(p + i)

# /0 数值最小是0

# %s 的工作方式不是“打印一个字符”，而是：
“从你给的地址开始，一个字节一个字节地打印，直到碰到 '\0' 才停下来。”**
所以：
%s 需要的不是字符串，而只是一个“起始地址”
char * 正好就是这个起始地址，指针就是一个起始位置

# %p 打印指针地址
 %x 打印十六进制

 # 单精度 float
双精度 double 精度更高
总位数​
32 位（4 字节）
64 位（8 字节）

# 多个 .c 文件共享同一个 .h 文件，就能保证接口一致。

用一个.h文件/多个.h文件都可以，没有太大区别，只是方便管理，编译不用管.h文件

# 多维数组
按行存储

二维数组：int a[][];
指针数组：char *b[]; //空的要指定大小，有初始化就不用指定大小

# 传入参数
int main(int argc, char *argv[])

argc
argument count，参数个数
argv
argument vector，参数数组（char * 指针数组） 都是字符str

第一个参数是程序名，实际参数是argc-1,argv[0] 是程序名本身,用空格来区分不同参数（空格是分割符号

# 结构体
定义 struct name {};
初始化 struct name 变量={}; //直接赋值

# sizeof 对象/表达式 或 sizeof(类型名)
# typedef 类型定义（可以自己组合来定义类型）
eg: typedef char* string; //定义string类型

# 位字段
struct 结构体名 {
    unsigned int 成员名 : 位数;
};
%u 表示unsigned 

# >< | 操作

# scanf("格式控制字符串", 地址列表);
和printf（）配对

# 函数声明
写在 main() 外面​ → 全局作用域 → 整个文件都能用
写在 main() 里面​ → 局部作用域 → 只有 main() 里能用

eg：    void filecopy(FILE *,FILE *);  //函数声明