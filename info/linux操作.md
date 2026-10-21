# 文件查找
1. find（全盘 / 目录精准搜索，最常用）
bash
运行
# 在根目录全盘搜索文件名包含xxx
find / -name "xxx" 2>/dev/null

# 在当前目录递归查找，大小写不敏感
find . -iname "filename"

# 只查找普通文件，排除文件夹
find /home -type f -name "*.log"
2>/dev/null 屏蔽权限不足的报错。

3. grep 查找文件内容（按文本内容搜文件）
bash
运行
# 在当前目录所有文件里搜索包含"关键词"的文件
grep -r "关键词" .

# 只列出文件名，不显示匹配行
grep -rl "关键词" .

# 解压
sudo apt update
sudo apt install unrar

unrar x 文件名.rar //直接就可以看到文件夹

一般压缩包，系统都可以解压，不用命令行

网盘登陆后可以直接下载，不用客户端

unzip 文件名.zip -d 目标目录  # 单个zip
unzip '*.zip' -d /target/ # 多个zip


# 删除软件

dpkg -l | grep -i 关键词 # 查看包名

sudo apt remove --purge app_nme
 sudo apt autoremove --purge # 清理依赖

# apt使用
sudo apt clean：清理已下载的安装包缓存。
sudo apt autoclean：清理过期的软件包缓存。
sudo apt autoremove：删除因安装其他软件而自动安装，但现在已不再需要的孤立依赖包。


使用 sudo apt install ./新版软件包名称.deb 命令不会删除原来的软件，而是会直接进行覆盖升级

ctrl+h 查看隐藏文件

# 使用 ncdu 工具。安装（sudo apt install ncdu）

ncdu 目录

使用d来删除
按大小排序：在界面中按下 s 键，所有文件和目录会按大小降序排列，最大的文件会直接置顶，方便你快速揪出“空间杀手”。
查看详细信息：选中某个文件后按下 i 键，可以查看该文件的详细信息（如具体路径、占用空间大小等）。
退出工具：分析或清理完毕后，按下 q 键即可退出 ncdu。

只读模式防误删：如果你只是想排查磁盘占用，担心自己手滑误删，可以在启动时加上 -r 参数（例如 ncdu -r /）。这会开启只读模式，彻底禁用删除功能，非常适合敏感数据分析场景。

# 缓存
./cache/中的东西可以清除

pip cache purge
conda clean --all
# 对于huggingface模型
官方 CLI 工具（推荐）：
首先确保安装了工具：pip install huggingface_hub[cli]。

然后可以使用以下命令查看缓存占用情况：huggingface-cli scan-cache。
进行交互式删除：huggingface-cli delete-cache（或者在新版本中使用 hf cache delete）。

手动清理：
如果你想直接清空所有 HuggingFace 缓存，可以执行：rm -rf ~/.cache/huggingface/hub/*。

rm -rf ~/.cache/* #清理

# 查看
ncdu  #好用
df -h #查看系统
du -h #查看当前目录

# 硬盘划分
sudo apt install gparted

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


# 下载加速

aria2c -c -s8 -x8 https://ghproxy.net/https://github.com/
多线下载(要使用zip连接，不要使用.git)

# 假设当前可用域名为 https://ghproxy.link（以该页跳转后拿到的为准）
git clone https://ghproxy.link/https://github.com/Zheng-Chong/CatVTON.git

https://ghfast.top

# 软连接（快捷方式）
ln -s "/home/my_llm/.local/share/Steam/steamapps/common/Skyrim Special Edition" ~/skyrimse

# 传输文件到服务器
## 安装
apt install -y rsync
rsync --version
rsync -avzP -e "ssh -p 12221" \
  /本地路径/largefile.zip \
  root@172.31.233.169:/服务器指定路径/

eg:
rsync -avzP -e "ssh -p 12221" \
  ./dataset/ \
  root@172.31.233.169:/mnt/d/HuangWeipeng/dataset # 显示指定目录