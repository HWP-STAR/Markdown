# git使用
1. 先查看当前远程（你现在是 SSH 地址）
bash
运行
git remote -v
2. 修改 origin 远程地址为 HTTPS 格式
Gitee HTTPS 地址格式：
https://gitee.com/hwp-star/learning_-c.git
执行命令替换：
bash
运行
git remote set-url origin https://gitee.com/hwp-star/learning_-c.git


将git clone https://huggingface.co/lambdalabs/sd-image-variations-diffusers
换为
git clone https://hf-mirror.com/lambdalabs/sd-image-variations-diffusers

就是使用hf-mirror.com  不可用


pip install huggingface-hub
--upgrade  # pip 强制升级

# bash/zsh
export HF_ENDPOINT=https://hf-mirror.com

huggingface-cli download \
  lambdalabs/sd-image-variations-diffusers \
  --local-dir ./sd-image-variations-diffusers \
  --resume-download \
  --local-dir-use-symlinks False

# 等价替换
  lambdalabs/sd-image-variations-diffusers：仓库地址（用户名 / 模型名）
--local-dir ./sd-image-variations-diffusers：下载到本地这个文件夹，等价于 git clone 创建的目录
--resume-download：断点续传，网络中断下次执行继续下（git clone 没有这个能力）
--local-dir-use-symlinks False：不生成软链接，全部下载实体文件，和 git clone 拿到的文件结构完全一致，代码可以直接加载使用


# git 使用
git rm --cached 文件名 # 取消追踪

vim .gitignore
# 或者 nano .gitignore，忽略文件
文件夹/
**/file_name # 忽略任意目录下的该文件

git remote add origin # 添加仓库
git push -u origin main #推送main分支

# 使用ssh仓库
ssh-keygen -t ed25519 -C "你的邮箱" # 生成
cat ~/.ssh/id_ed25519.pub # 复制上传公钥


git remote add origin 仓库 # 添加
git remote set-url origin 仓库 # 修改remote仓库
git remote -v #查看