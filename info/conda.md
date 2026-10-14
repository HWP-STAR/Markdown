# conda env list 
查看环境

conda env remove -n <环境名称> # 删除

conda clean --all #清除缓存

pip install --upgrade matplotlib #升级

# 使用linux字体
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC'] 
plt.rcParams['axes.unicode_minus'] = False

# 新建环境，指定 Python 版本
conda create -n myproj python=3.10
 
 # 新建环境并顺手装包
conda create -n myproj python=3.10 numpy 

# 激活环境（激活后装的包只属于这个环境）
conda activate myproj

# 退出环境
conda deactivate

# 删除环境
conda remove -n myproj --all

# 克隆环境
conda create --name myproj_copy --clone myproj