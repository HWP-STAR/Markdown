# 查看看内核版本

cat /etc/os-release

# cmake使用

cmake -B build //创建
cmake --build build  //编译，在 `build` 目录里执行编译，生成可执行文件、库文件

等价：`cd build && make`（Linux/macOS）

./build/hello

# 生成可执行文件
add_executable(hello main.cpp)

# 告诉 CMake：去这两个目录里找 CMakeLists.txt，继续解析它们
add_subdirectory(lib)
add_subdirectory(app)

**add_subdirectory 管“工程结构”
add_executable 管“具体生成什么目标”**

**CMake 本身：大小写不敏感！**
`project()` 和 `PROJECT()` 完全等价，`message()` 和 `MESSAGE()` 一样能跑。
没有语法层面的缩进要求！

# opencv
它支持 C++、Python、Java​ 等语言，在 Ubuntu / Linux、Windows、macOS、Android、iOS​ 上都能使用，是计算机视觉领域最主流的基础库之一。

# Pop!_OS 上其实是一个打包层面的自动化策略
sudo apt update && sudo apt full-upgrade/upgrade #更新
