# 下载lean
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh

 source ~/.profile 使环境变量生效

 elan --version
lean --version

# elan 是 Lean 的版本管理工具
先从镜像装 glean
https://mirror.sjtu.edu.cn/
https://s3.jcloud.sjtu.edu.cn/899a892efef34b1b944a19981040f55b-oss01/elan/mirror_clone_list.html

elan：Lean 的版本管理器（类似 Rust 的 rustup）。它会根据项目里的 lean-toolchain 文件自动下载/切换 Lean 4 版本。
glean：国内镜像适配工具，用来通过 SJTUG 镜像安装 elan 或 lean，解决 GitHub 访问慢的问题

mkdir -p ~/.local/bin
mv glean ~/.local/bin/
chmod +x ~/.local/bin/glean

glean -update
glean -install elan -version latest

elan show
lean --version  # 类似python
lake --version # 类似npm

# lake 是 Lean 4（形式化数学/定理证明语言）的构建工具
lake new my_project #创建项目

# Mathlib
在项目根目录下的 lakefile.lean 文件中
require mathlib from git
  "https://mirror.sjtu.edu.cn/git/lean4-packages/mathlib4"

  # 学习
  elan --version
lake --version
lean --version