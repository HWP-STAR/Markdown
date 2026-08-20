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