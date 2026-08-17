# Docker使用

Docker 的使用流程可以概括为"安装 → 拉取镜像 → 运行容器 → 构建自己的镜像 → 多容器编排"

docker pull 仓库
docker run/stop/rm

Hub网站
https://hub.docker.com/

# 1. 拉取轻量版 Nginx 镜像
docker pull nginx:alpine

docker是一套打包完整运行环境，包含系统、依赖、程序三合一的只读模板
「操作系统 + 系统依赖 + 应用程序 + 配置」全部封存在一个文件包

# 直接进入容器终端，用完手动退出
docker run -it --rm nginx:alpine sh

sh 是进入终端
-it：交互式终端，可以敲命令
--rm：退出后自动删除容器，不残留

后台服务容器（-d 启动的网站）
默认持续运行，除非手动停止、重启服务器、删除容器。
bash
运行
# 手动停止
docker stop my-nginx
# 再次启动
docker start my-nginx
交互式 sh 容器（docker run -it sh）
输入 exit 退出终端，容器立刻停止；加了 --rm 会直接删掉容器。

## 镜像永久存在，容器是临时实例
CI/CD 自动化基石
代码提交 → 自动构建镜像 → 自动测试 → 自动部署，整个流水线高度标准化
ocker 基于 Linux 容器技术，不能直接运行 .exe 程序
