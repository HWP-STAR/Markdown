

# 标准方法
帮我跑通项目，进行简单的demo演示，网络不好就使用镜像服务（如：使用镜像
- PyPI/uv：清华源 https://pypi.tuna.tsinghua.edu.cn/simple
- npm：https://registry.npmmirror.com
- HuggingFace：https://hf-mirror.com
- GitHub 大 wheel：https://gh-proxy.com/），自己使用虚拟环境，下载各种东西尽量在当前目录（系统盘空间不够），下载模型权重使用huggingface_hub cli，完成后告诉我结果，

告诉我具体进度，还要多久完成，然后继续

cd /你的/当前目录
mkdir -p .conda_pkgs .pip_cache .tmp

export CONDA_PKGS_DIRS="$PWD/.conda_pkgs"
export PIP_CACHE_DIR="$PWD/.pip_cache"
export TMPDIR="$PWD/.tmp"
mkdir -p "$TMPDIR"

conda create --prefix "$PWD/venv" python=3.10.13 -y #指定python，这会在当前目录生成 ./venv

conda activate "$PWD/venv"
# 提示符变成 (./venv) 或 (/你的/当前目录/venv) 即成功 

# bash/zsh
export HF_ENDPOINT=https://hf-mirror.com

# hugging缓存在./，默认在系统盘
mkdir ./hf_cache
export HF_HOME=./hf_cache
export HF_HUB_CACHE=./hf_cache
# 想永久生效就写进 ~/.bashrc

# 假设当前可用域名为 https://ghproxy.link（以该页跳转后拿到的为准）
git clone https://ghproxy.link/https://github.com/Zheng-Chong/CatVTON.git

https://ghfast.top



pip install huggingface-hub
--upgrade  # pip 强制升级

# bash/zsh
export HF_ENDPOINT=https://hf-mirror.com

huggingface-cli download \
  lambdalabs/sd-image-variations-diffusers \
  --local-dir ./sd-image-variations-diffusers \
  --resume-download \
  --local-dir-use-symlinks False








CUDA_VISIBLE_DEVICES=0 python3 turbo_inference/bidirectional_inference_vivid.py --config_path configs/wan_bidirectional_dmd_from_scratch.yaml --checkpoint_folder ./weights/MagicTryOn_Turbo/model.pt  --output_folder result/tryon,帮我分析该命令，然后帮我跑通（解决各种报错），完成后告诉我你的操作(重点阅读README,我只要跑通Turbo部分，不要管MagicTryOn_14B_V1，我已经激活conda虚拟环境)，不要使用数据集，只要使用./datasets中的内容进行demo演示，帮我分析该项目结构,我只要跑通Turbo部分，不要管MagicTryOn_14B_V1，我已经激活conda虚拟环境和下载好Turbo权重，只要使用./datasets中的内容进行demo演示，具体该怎么做，你现在的工作进度如何，告诉我具体境况

我已经下载好了1.3B权重和Turbo权重，使用使用Turbo模型对./datasets中的内容进行demo演示，如果配置文件不合适，可以自己创建合适的配置文件来完成demo演示，完成后告诉我你的操作，你现在的进度是什么，flash_attn库是否正常，各种依赖是否正常，还要那些做什么，告诉我进度，然后继续完成，仔细阅读requirement.txt,分析各种依赖的关系，不要随意升级版本，寻找合适的解决方法
torch 2.2.0+cu121

# 检查 Python 版本
python --version

# 检查 PyTorch 和 CUDA
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"

# 检查 Flash Attention
python -c "import flash_attn; print(flash_attn.__version__)"

# 列出所有已安装的包
pip list | grep -E "torch|flash|diffusers|transformers|opencv|decord"

# 恢复当前目录所有已跟踪文件
git restore .
git reset --hard HEAD


# 使用 ghproxy 代理
https://ghproxy.com/https://github.com/Dao-AILab/flash-attention/releases/download/v2.7.3/flash_attn-2.7.3+cu12torch2.2cxx11abiFALSE-cp312-cp312-linux_x86_64.whl

aria2c -c -s8 -x8 https://ghproxy.net/https://github.com//Dao-AILab/flash-attention/releases/download/v2.7.3/flash_attn-2.7.3+cu12torch2.2cxx11abiFALSE-cp310-cp310-linux_x86_64.whl

flash_attn-2.7.3+cu12torch2.2cxx11abiFALSE-cp312-cp312-linux_x86_64.whl


最终运行命令
CUDA_VISIBLE_DEVICES=0 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True TOKENIZERS_PARALLELISM=false python3 turbo_inference/bidirectional_inference_vivid.py \
  --config_path configs/wan_turbo_demo_1_3b.yaml \
  --checkpoint_folder ./weights/MagicTryOn_Turbo/model.pt \
  --output_folder result/tryon \
  --output_name turbo_demo.mp4

CUDA_VISIBLE_DEVICES=0 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True TOKENIZERS_PARALLELISM=false python3 turbo_inference/bidirectional_inference_vivid.py --config_path configs/wan_turbo_demo_1_3b.yaml --checkpoint_folder ./weights/MagicTryOn_Turbo/model.pt --output_folder result/tryon --cloth_image datasets/garment/vivo/vivo_garment/00003.png --cloth_line_image datasets/garment/vivo/vivo_garment_anilines/00003.png --output_name turbo_demo_vivo_00002.mp4


当前脚本是一次性把视频 latent 放进模型里跑，帧数越长，显存和时间越高。
如果你要更长视频，建议先试：
--video_length 41
再试：
--video_length 61

如果你想更高清，比如接近原视频比例，可以试：
--height 960 --width 720
或者：
--height 1024 --width 768
但注意高度和宽度最好能被 8 整除。

--height 960 --width 720 --video_length 41

5. 修改输入视频/服装
不用改配置，直接命令行传：
--person_video path/to/video.mp4
--masked_video path/to/agnostic.mp4
--mask_video path/to/mask.mp4
--pose_video path/to/densepose.mp4
--cloth_image path/to/cloth.png
--cloth_line_image path/to/cloth_line.png
--cloth_caption_json path/to/caption.json
--output_name your_output.mp4

4. 修改去噪步数
当前是 4 步：
denoising_step_list:
- 1000
- 757
- 522
- 0
想更快可以减少，比如 3 步：
denoising_step_list:
- 1000
- 522
- 0
想尝试更细可以增加，比如：
denoising_step_list:
- 1000
- 850
- 700
- 522
- 300
- 0


CUDA_VISIBLE_DEVICES=0 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True TOKENIZERS_PARALLELISM=false python3 inference/video_tryon/predict_video_tryon_customize.py --video_length 21 --output_folder result/tryon_14b --output_name magictryon_14b_demo.mp4


1. 命令: CUDA_VISIBLE_DEVICES=0 python3 run_14b_demo.py（我写的脚本）
2. 推理时间: 20步推理，21帧 @ 640×480，约92秒（~4.6秒/步）


CUDA_VISIBLE_DEVICES=0 venv/bin/python -u run_1_3b_turbo_demo.py \
  --config_path configs/wan_turbo_video_demo_1_3b.yaml

  CUDA_VISIBLE_DEVICES=0 venv/bin/python -u run_1_3b_turbo_demo.py \
  --config_path configs/wan_turbo_video_demo_1_3b.yaml \
  --video_length 9 \
  --output_name turbo_1_3b_demo_9f.mp4




- 文本提示词 prompt  
run_1_3b_turbo_demo.py:127-128
- masked_video：人物视频的遮挡/agnostic 版  
run_1_3b_turbo_demo.py:151-161
- mask_video：二值 mask  
run_1_3b_turbo_demo.py:151-161
- pose_video：姿态/密集姿态视频  
run_1_3b_turbo_demo.py:151-161
- cloth_image：服装图
- cloth_line_image：服装线稿图
- clip_image：服装图再送进 CLIP 编码
- noise：随机噪声，作为扩散生成起

只能用 0 ~ N-1 帧作为条件输入
不能直接指定 20 ~ 20+N 帧

CUDA_VISIBLE_DEVICES=0 venv/bin/python -u benchmark_1_3b_14b_demo.py --config_path configs/wan_benchmark_1_3b_14b.yaml --models 14b --frames 1,3,6,9,24,48

 CUDA_VISIBLE_DEVICES=0 venv/bin/python -u benchmark_1_3b_14b_demo.py --config_path configs/wan_benchmark_1_3b_14b.yaml --models 14b --frames 6,9,24,48

CUDA_VISIBLE_DEVICES=0 venv/bin/python -u benchmark_1_3b_14b_demo.py \
  --config_path configs/wan_benchmark_1_3b_14b.yaml \
  --models 1_3b \
  --frames 1,3,6,9,24,48 \
  --start_frame 60


 

python run_1_3b_turbo_demo.py \
  --num_denoising_steps 4 \
  --benchmark_lengths 1,3,6,9,30,60 \
  --output_prefix turbo_benchmark

python3 run_1_3b_turbo_demo.py --num_denoising_steps 4 --benchmark_lengths 1,3,6,9,30


# input
1. 人物视频
2. 人物 agnostic 视频
3. 人物 mask 视频
4. 人物 densepose 视频
5. 衣服图片
6. 衣服线稿/边缘图
7. 衣服 caption 文本
输入	作用
person_video	原始人物视频
masked_video / agnostic	把要替换衣服区域抹掉后的人物视频
mask_video	指示哪里需要换衣服
pose_video / densepose	人体姿态/身体结构条件
cloth_image	目标衣服图片
cloth_line_image	衣服线稿，约束衣服结构
cloth_caption_json	衣服文字描述，用作 prompt

上身/下身/全身区别
区别主要在 mask 和 agnostic 怎么生成：
上身试衣：mask 遮住上衣区域
下身试衣：mask 遮住裤子/裙子区域
全身试衣：mask 遮住上下身或整套衣服区域

果针对 MagicTryOn_1.3B 目标是：
自己蒸一个 few-step 的 try-on student
重点关心生成质量和速度，不要想要使用当前的仓库，全网搜索最新效果好，适合该模型蒸馏的方法，提供具体链接

Scope 现在的 segformer-tryon 本质是：
LongLive + VACE inpainting + garment reference image + SegFormer mask

 蒸馏 segformer-tryon 使用的模型：有效，但投入最大
有效，尤其是做成“Magic-TryOn → LongLive/VACE realtime”的蒸馏。
可以蒸馏的目标：
Teacher: MagicTryOn_1.3B base
Student: LongLive-1.3B + VACE + LoRA