终端直接输入，自动弹出浏览器配置面板：
fish
fish_config

# 用vim编辑(配置文件)
vim ~/.config/fish/config.fish

cp -r 复制文件夹

fish_add_path 自带永久保存参数 -U（universal 全局变量），执行一次永久写入：
fish
fish_add_path -U $HOME/.opencode/bin

# 一般生效
source ~/.config/fish/config.fish