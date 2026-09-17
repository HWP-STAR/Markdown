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

# 提交记录
# 导出单行日志到commit-log.txt
git log --oneline > commit-log.txt

commit message格式

<type>(<scope>): <subject>
type(必须)

用于说明git commit的类别，只允许使用下面的标识。

feat：新功能（feature）。

fix/to：修复bug，可以是QA发现的BUG，也可以是研发自己发现的BUG。

fix：产生diff并自动修复此问题。适合于一次提交直接修复问题
to：只产生diff不自动修复此问题。适合于多次提交。最终修复问题提交时使用fix
docs：文档（documentation）。

style：格式（不影响代码运行的变动）。

refactor：重构（即不是新增功能，也不是修改bug的代码变动）。

perf：优化相关，比如提升性能、体验。

test：增加测试。

chore：构建过程或辅助工具的变动。

revert：回滚到上一个版本。

merge：代码合并。

sync：同步主线或分支的Bug。

scope(可选)

scope用于说明 commit 影响的范围，比如数据层、控制层、视图层等等，视项目不同而不同。

例如在Angular，可以是location，browser，compile，compile，rootScope， ngHref，ngClick，ngView等。如果你的修改影响了不止一个scope，你可以使用*代替。

subject(必须)

subject是commit目的的简短描述，不超过50个字符。