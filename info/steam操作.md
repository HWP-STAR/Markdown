# 潜渊症
f3 控制台
enablecheats # 开启作弊

# 作弊代码 cheat code
开发者调试

# （387290 是《Ori and the Blind Forest: Definitive Edition》的 Steam AppID
~/.steam/steam/steamapps/compatdata/387290/pfx/

C:\temp\moonDebugPC.txt

# 奥日2
~/.steam/steam/steamapps/compatdata/1057090/pfx

drive_c/moon/wispsDebug.txt

# 模拟win
~/.local/share/Steam/steamapps/compatdata/
2600176545 是动漫共和国


# holocure
~/.local/share/Steam/steamapps/compatdata/2420510/pfx/drive_c/users/steamuser/AppData/Local/HoloCure/

# mod
nexusmods.com

# steam c盘
~/.local/share/Steam/steamapps/compatdata/
各种数字id

# deepseek
位置
C:\users\steamuser\AppData\Local\Programs\DeepSeek Harness\DeepSeek Harness.exe

从库中移除，steam会自动删除c盘文件夹


# 让 glxgears 用独显跑
DRI_PRIME=1 glxgears

# Steam 游戏启动项里
DRI_PRIME=1 %command%

# 桌面环境仍走核显，只有这个程序吃独显
DRI_PRIME=1 blender

DRI_PRIME=1 minecraft-launcher

DRI_PRIME=1 %command% #command是一个展位符号
Steam 里某游戏「启动选项」填 DRI_PRIME=1 %command%

在 Ubuntu 等发行版中，默认不自带该命令，但可以手动创建。在 /usr/local/bin/ 下新建一个名为 prime-run 的文件，写入以下内容：
bash

编辑



#!/bin/bash
__NV_PRIME_RENDER_OFFLOAD=1 __VK_LAYER_NV_optimus=NVIDIA_only __GLX_VENDOR_LIBRARY_NAME=nvidia "$@"

sudo chmod +x /usr/local/bin/prime-run

prime-run <你想运行的程序>  //要注意$PATH中是否有/usr/local/bin/


## 显卡查看

glxinfo 是一个查询 OpenGL / GLX 渲染能力的命令行工具
sudo apt install mesa-utils

prime-run glxinfo | grep "OpenGL renderer" //验证是否生效

在 Steam 游戏的启动选项中，也可以设置为：



glxgears          # 集显运行
prime-run glxgears  # 独显运行，帧率会明显更高


# steam安装其他exe
安装完成后修改路径
使用proton 

"C:\users\steamuser\AppData\Local\Programs\动漫共和国概念版/dmghg.exe"

"Z:\home\my_llm\Downloads\压缩包\动漫共和国概念版-1.4.4\动漫共和国概念版\dmghg.exe"

steam linux runtime ：兼容给原生linux游戏
steam Proton ： 兼容给win游戏

# 小键盘有些游戏不能识别，一般使用主键盘

# 渲染有问题
启动选项
-vulkan

# 动漫
使用proton experimental 

"C:\users\steamuser\AppData\Local\Programs\动漫共和国概念版/dmghg.exe"

steam linux runtime ：兼容给原生linux游戏
steam Proton ： 兼容给win游戏

# MC
爱发电官网
龙腾猫跃 PCL

# 老滚5
版本：1.6.1170.0
1.6.1170 是“2024 年的旧稳定版”；1.7.104 是“2026-08 之后 Steam 默认给你装的新版”。

开梯子速度很快，N网下载
/home/my_llm/.local/share/Steam/steamapps/common/Skyrim Special Edition/

## mod管理器
vertex
mo2

"C:\Modding\MO2\ModOrganizer.exe"

指定的文件夹必须是游戏的“根目录”（里面要包含游戏的真实 .exe 启动文件，比如 SkyrimSE.exe、Fallout4.exe）。

# 装游戏
是在~/.local/share/Steam中

Steam\steamapps\common\游戏名

# 存档
Steam\userdata\SteamID\AppID\
每个 Steam 账号有自己唯一的 SteamID
832002909 是我原来账号的存档

# 硬盘
主要影响加载游戏到内存
游戏运行在内存，基本没有影响，实际不是

## 流式加载（Streaming）
开放世界游戏不会把整个地图一次性塞进内存，而是边跑边加载

着色器编译/读取，速度有影响
帧率（FPS）是 CPU+GPU 的产出速率，硬盘不直接参与每一帧的计算