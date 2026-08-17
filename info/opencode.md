wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
推荐：curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash

# 要等一下来安装完成，出现提示

source ~/.bashrc

export NVM_NODEJS_ORG_MIRROR=https://npmmirror.com/mirrors/node/



nvm install --lts

验证 Node.js 和 npm
Node.js 安装完成后，你可以通过以下命令来验证安装是否成功，并查看具体的版本号。
bash

node -v  # 查看 Node.js 版本
npm -v   # 查看 npm 版本

设置全局镜像源
bash

npm config set registry https://registry.npmmirror.com


验证配置是否生效
bash

npm config get registry

npm install -g @openai/codex # codex
npm i -g opencode-ai # opencode
npm install -g ccswitch-tui

chsh -s /usr/bin/fish #将 Fish 设置为默认 Shell