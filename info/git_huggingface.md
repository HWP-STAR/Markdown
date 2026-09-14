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

# 远程有改变，拉取合并后push

# 1. 拉取远程代码并变基
git pull --rebase origin master
# 2. 如果遇到冲突，解决冲突后执行：
# git add <冲突文件>
# git rebase --continue
# 3. 重新推送
git push origin master


git remote add origin git@github.com:HWP-STAR/miniGPT.git
git branch -M main
git push -u origin main

1. 查看本地所有分支（你电脑上的）
bash
运行
git branch
看远程仓库的分支（GitHub/GitLab/ 码云 上的）
bash
运行
git branch -r  or -a


# 1. 切到主分支
git checkout main

# 2. 新建并切换到你的功能分支
git checkout -b feature/login

# 3. 写代码后提交
git add .
git commit -m "完成登录功能"

# 4. 第一次推送到远程（必须加 -u）
git push -u origin feature/login

# 5. 要合并时：切回主分支 → 合并 → 推送
git checkout main
git merge feature/login
git push


# 注释用 #
# 忽略文件夹（末尾加 /）
node_modules/
dist/
build/
__pycache__/
logs/

# 忽略文件
.env
*.log
*.tmp
.DS_Store
Thumbs.db

# 忽略所有目录下的某种文件
*.swp
*.swo

# 排除（不忽略）某个文件
# !important.log

git reset HEAD -- FILE_name

# 把仓库复位到某个提交的状态: git reset 提交的哈希值.
从当前提交新建分支并切换: git checkout -b 分支名.
切换到分支: git checkout 分支名.
删除分支: git branch -D 分支名.
