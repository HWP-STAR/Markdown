# cuda toolkit 使用
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
source ~/.bashrc

nvcc --version
使用nvcc编译.cu文件

2️⃣ 直接测试 nvcc 的原始路径
/usr/local/cuda/bin/nvcc --version
如果环境没有，可使用绝对路径

# 1. 将CUDA二进制程序目录加入系统PATH，终端能直接调用nvcc等命令
export PATH=/usr/local/cuda-12.5/bin:$PATH

# 2. 将CUDA运行库目录加入动态链接库路径，程序运行时能找到cuda库文件，资源库
export LD_LIBRARY_PATH=/usr/local/cuda-12.5/lib64:$LD_LIBRARY_PATH

# 3. 定义CUDA_HOME环境变量，很多编译脚本、框架(PyTorch/TensorRT)会读取这个变量
export CUDA_HOME=/usr/local/cuda-12.5

/usr/local/cuda/bin
原因有两个：
1️⃣ 统一入口，切换版本不用改 PATH

目录	类型	作用
cuda-13.3	真实目录​	13.3 版本的全部文件（编译器、库、头文件）
cuda-13	大版本目录​	13.x 系列的统一入口
cuda	符号链接​	当前"默认激活"的 CUDA 版本

echo $PATH 查看路径
fish和bash语法不同，一般换bash
正确的 PATH 配置（照抄即可）
编辑 ~/.bashrc：
# CUDA
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda
然后：
source ~/.bashrc
验证：
nvcc --version

.cu文件和.c文件类似
nvcc编译，gcc编译
