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


# 安装
第一步：清理旧版本（如果有）
sudo apt remove -y docker docker-engine docker.io containerd runc
sudo rm -rf /var/lib/docker /var/lib/containerd

第二步：安装依赖包
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

第三步：添加阿里云 Docker GPG 密钥
sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

第四步：添加阿里云 Docker 软件源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

第五步：更新软件源缓存并安装 Docker
sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

第六步：启动并验证
sudo systemctl start docker
sudo systemctl enable docker
docker --version
sudo docker run hello-world

第七步：配置免 sudo 使用 Docker（可选）
sudo usermod -aG docker $USER
newgrp docker

第一步：编辑配置文件
sudo mkdir -p /etc/docker
sudo vim /etc/docker/daemon.json

{
  "registry-mirrors": [
    "https://docker.xuanyuan.me",
    "https://docker.1ms.run",
    "https://docker.m.daocloud.io",
    "https://registry-1.docker.io"
  ]
}

第三步：重载配置并重启 Docker 服务
sudo systemctl daemon-reload
sudo systemctl restart docker

第四步：验证配置是否生效
docker info | grep -A 3 "Registry Mirrors"


# 使用
docker pull 拉取的是「镜像（Image）」

docker images

docker run -it 名字 bash
exit

⚠️ 注意：
容器关了，装的软件就没了
想长期保存，要用 镜像 / 挂载

docker run -it ubuntu bash        # 进容器
exit                              # 退出
docker ps                         # 看运行中的
docker ps -a                      # 看所有
docker rm 容器名                  # 删除容器

这里其实出现了两个概念: “镜像” 和 “容器”. 你可以把它们理解为: 前者是一个硬盘, 里面装好了操作系统, 但它是静态的, 你不能直接拿它来运行. 后者是一台电脑, 里面安装了硬盘, 就能运行对应的操作系统

docker run -it --rm maxxing/compiler-dev bash
 #用完就删除

使用了 -it 参数, 这个参数会开启容器的 stdin 以便我们输入 (-i), 同时 Docker 会为容器分配一个终端 (-t).

# docker run -it --rm -v /home本地路径:/root/compiler maxxing/compiler-dev bash

在许多情况下, 我们需要让 Docker 容器访问宿主系统中的文件
