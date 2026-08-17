# Latex使用
sudo apt update
sudo apt install texlive-full latexmk #辅助工具

pdflatex --version 

LaTeX Workshop 插件
在 VS Code 中，按 Ctrl+Shift+P 打开命令面板，输入 Preferences: Open User Settings (JSON) 并选择它，打开设置文件。

既然你安装了 texlive-full，为了省心，顺手把系统字体也装上，只需一行命令：

bash
sudo apt install fonts-arphic-ukai fonts-arphic-uming

latexmk -C   #清理
