echo $DASHSCOPE_API_KEY
export DASHSCOPE_API_KEY="sk-ws-H.EIYRIYP.Rei6.MEUCIQDW8JqABOTbbZ6caT1pQl6MqRzUMq64I5VNKAMSIPaWVwIgU2r2EGuGQ0gQ6wazBANCyE-Yy-YqoMFWnOOKd1EcjqY"
wan2.1 api

demo 图片已成功生成，尺寸为 1536x512，包含人物、mask/遮挡预览、服装、试穿

运行 Gradio demo：
cd /root/autodl-tmp/VTO/CatV2TON/CatVTON
HF_ENDPOINT=https://hf-mirror.com python app.py \
  --output_dir="resource/demo/output" \
  --mixed_precision="bf16" \
  --allow_tf32

  HF_HUB_OFFLINE=1 python app.py \
  --output_dir="resource/demo/output" \
  --mixed_precision="bf16" \
  --allow_tf32

  已使用镜像
- PyPI/uv：清华源 https://pypi.tuna.tsinghua.edu.cn/simple
- npm：https://registry.npmmirror.com
- HuggingFace：https://hf-mirror.com
- GitHub 大 wheel：https://gh-proxy.com/...

日常操作
启动服务：
cd /root/autodl-tmp/VTO/scope
source .env.local
setsid .venv/bin/daydream-scope --host 0.0.0.0 --port 8000 > .logs/server.log 2>&1 < /dev/null &
查看状态：
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/v1/pipeline/status
重新加载实时 VACE 管线：
curl -X POST http://127.0.0.1:8000/api/v1/pipeline/load \
  -H 'Content-Type: application/json' \
  -d '{"pipeline_ids":["longlive"],"load_params":{"vace_enabled":true}}'
前端使用：
打开 http://你的服务器IP:8000，选择/确认 longlive，Settings 里 VACE 保持 On。Reference image 放到 UI 里上传即可，文件会进入 .assets。


- 当前容器内 IP：172.17.0.5
- 本机访问地址：http://127.0.0.1:8000
- 如果你在 AutoDL/云服务器网页外部访问，通常要在平台里把 8000 端口映射/自定义服务暴露出来，然后访问平台给你的公网链接或公网 IP + 端

启动服务
cd /root/autodl-tmp/VTO/scope
source .env.local
.venv/bin/daydream-scope --host 0.0.0.0 --port 8000
如果想后台运行：
cd /root/autodl-tmp/VTO/scope
source .env.local
.venv/bin/python -c "import subprocess; log=open('.logs/server.log','ab'); subprocess.Popen(['.venv/bin/daydream-scope','--host','0.0.0.0','--port','8000'], stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)"

http://116.172.96.159:8000

ssh -L 8000:127.0.0.1 端口转发

默认：网页里的实时视频预览，走 WebRTC。

最可能原因
你是通过公网 IP 或 AutoDL HTTP 代理打开网页的。网页能打开，但 WebRTC 视频流不是普通 HTTP，它需要浏览器和服务器之间建立媒体连接。AutoDL/云服务器/NAT/容器环境经常会导致：
页面能打开，但视频预览为空
ICE failed

这是 WebRTC 网络问题，不是模型没加载。用服务器端保存 MP4 的方式最稳定。当前模型已经加载成功。

kill 296273 -9

你也可以先确认一下：
ps -fp 296273
nvidia-smi

重新启动服务
你当前看到的启动命令是：
.venv/bin/daydream-scope --host 0.0.0.0 --port 8000

方式 1，按原命令在原项目目录启动：
先进入当时启动这个服务的项目目录，再执行：
.venv/bin/daydream-scope --host 0.0.0.0 --port 8000
方式 2，直接用完整可执行文件启动：
/root/autodl-tmp/VTO/scope/.cache/uv/environments-v2/daydream-scope-cp3.12.3-08c637b3908d2dd0/bin/python3 .venv/bin/daydream-scope --host 0.0.0.0 --port 8000


在 scope 项目目录执行：
uv run daydream-scope --host 0.0.0.0 --port 8000

推荐你这样操作
1. 先停旧服务
kill 296273
2. 启动新服务
uv run --directory /root/autodl-tmp/VTO/scope daydream-scope --host 0.0.0.0 --port 8000
3. 另开一个终端检查
nvidia-smi
ps -ef | grep daydream-scope
如果想后台运行
nohup uv run --directory /root/autodl-tmp/VTO/scope daydream-scope --host 0.0.0.0 --port 8000 > /root/autodl-tmp/VTO/scope/daydream-scope.log 2>&1 &
检查日志：
readlink -f /root/autodl-tmp/VTO/scope/daydream-scope.log
如果提示 uv: command not found
说明你机器里没把 uv 放进当前 shell 的 PATH，这时先试：
/root/.local/bin/uv run --directory /root/autodl-tmp/VTO/scope daydream-scope --host 0.0.0.0 --port 8000
如果还不行，再查 uv 在哪：
which uv


关闭服务
在服务器终端执行：
pkill -f daydream-scope
确认是否关闭：
curl http://127.0.0.1:8000/health
如果显示连接失败，说明已关闭。
启动服务
cd /root/autodl-tmp/VTO/scope
source .env.local
.venv/bin/daydream-scope --host 0.0.0.0 --port 8000

后台启动
如果你想关闭终端后服务还继续运行：
cd /root/autodl-tmp/VTO/scope
source .env.local
.venv/bin/python -c "import subprocess; log=open('.logs/server.log','ab'); subprocess.Popen(['.venv/bin/daydream-scope','--host','0.0.0.0','--port','8000'], stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)"
查看服务是否启动成功
curl http://127.0.0.1:8000/health


cd /root/autodl-tmp/VTO/scope
scripts/save_text_video.sh "a cute panda walking in a sunny park, cinematic" 10 output.mp4

我是这样处理的：
1. 使用 test/person.mp4 作为视频输入。
2. 使用 test/cloth.jpeg 作为 VACE 参考图。
3. 加载 Scope 的 longlive 管线，并开启 VACE：
{
  "vace_enabled": true,
  "height": 640,
  "width": 480,
  "vace_context_scale": 1.2
}
4. 启动 headless session：
{
  "input_mode": "video",
  "vace_use_input_video": true,
  "vace_ref_images": ["/root/autodl-tmp/VTO/scope/.assets/cloth.jpeg"]
}
5. 用 prompt 引导：
same person from the input video wearing the exact clothing garment from the reference image, preserve body pose and motion, realistic virtual try on, natural fabric, keep face and background consistent
6. 从 Scope 的 MPEG-TS 输出流录制成 MP4。
效果不好的原因：
- longlive + VACE 不是专门的虚拟试衣模型。
- VACE 更像“参考图 + 视频结构引导”的视频生成/编辑，不会精准分割人体、服装区域和布料细节。
- 没有使用人体解析、服装 mask、densepose、openpose、agnostic person 等虚拟试衣关键条件。
- 没有对衣服区域做 inpainting mask，所以模型不知道“只替换上衣/衣服，保留脸、手、背景”。
- 参考图是单张衣服图，VACE 只能弱约束外观，不能保证 exact garment transfer。
- 输入视频分辨率较低且只有几秒，生成模型会自由发挥，容易改脸、改背景、改景、改衣服形状。
我使用的是实时管线，优先速度，不是高质量离线 VTO

但它不能保证“真实商品级换衣”。原因是它缺少专业 VTON 所需的：
- 人体解析
- 上衣分割 mask
- DensePose/OpenPose
- agnostic person
- garment warping
- 专门 try-on diffusion 模型
- 时序一致性后处理


可以结合，但要分清两件事：
- Magic-TryOn：专门做虚拟试衣，效果方向对。
- Scope + VACE：专门做实时交互视频生成，实时性强，但虚拟试衣精度不够。
我看了 Magic-TryOn
它确实是虚拟试衣模型，并且基于 Wan2.1：
MagicTryOn: Wan2.1 diffusion Transformer backbone
MagicTryOn_1.3B
MagicTryOn_Turbo
MagicTryOn_14B
你本地已经有权重：
/root/autodl-tmp/VTO/Magic-TryOn/weights/MagicTryOn_1.3B
/root/autodl-tmp/VTO/Magic-TryOn/weights/MagicTryOn_Turbo
/root/autodl-tmp/VTO/Magic-TryOn/weights/MagicTryOn_14B_V1
大小大概：
MagicTryOn_1.3B: 19GB
MagicTryOn_Turbo: 5.9GB
MagicTryOn_14B: 47GB
Turbo 配置是：
1.3B
4 step
640x480
16 fps
默认 21 帧
它和 Scope 的区别
Magic-TryOn 的输入不是简单的：
person video + cloth image
它真正需要：
person_video
masked_video / agnostic video
mask_video
pose_video / densepose video
cloth_image
cloth_line_image
cloth_caption
也就是说它有完整的虚拟试衣条件：
- 人体上衣 mask
- 去衣服后的 agnostic person
- DensePose
- 衣服线稿
- 衣服 caption
- 衣服图
这就是它比 Scope VACE 更适合换衣的原因。
能不能实现实时虚拟试衣
严格实时很难。
原因：
- Magic-TryOn 是分段/批处理视频试衣，不是 WebRTC 逐帧 autoregressive pipeline。
- 它需要提前准备 mask、agnostic、densepose、cloth line map。
- 推理是按 21/30/60 帧块生成，而不是一帧进一帧出。
- 依赖栈和 Scope 不一样：Magic-TryOn README 要求 torch==2.2，Scope 当前是 torch==2.9.1，直接塞进同一个进程风险很高。
所以不建议把 Magic-TryOn 直接硬接进 Scope 当前 Python 进程。
推荐方案
我建议做“准实时/低延迟分块虚拟试衣”，不是硬实时。
架构：
摄像头/视频输入
→ 分段缓存 1-2 秒
→ Magic-TryOn Turbo 做 4-step try-on
→ 输出 MP4/帧流
→ Scope 负责播放、切换、Web UI、录制
也就是：
Magic-TryOn 负责换衣质量
Scope 负责实时交互和视频系统
更具体的方案
方案 A：最稳，离线/准实时保存视频
1. 从输入视频抽帧
2. Magic-TryOn 生成 mask / agnostic / densepose
3. Magic-TryOn Turbo 4step 生成试衣视频
4. 保存 result.mp4
5. Scope 或网页播放 result.mp4
优点：效果最好，最稳定。  
缺点：不是实时。
方案 B：分块准实时
1. 每 21 帧或 30 帧作为一个 chunk
2. 后台 Magic-TryOn Turbo 推理
3. 前端播放上一 chunk，同时生成下一 chunk
4. 用缓存队列降低卡顿
优点：可以接近实时体验。  
缺点：有 1-3 秒延迟，工程复杂。
方案 C：Scope VACE 实时预览 + Magic-TryOn 高质量输出
实时预览：Scope + VACE，低质量快速看效果
最终输出：Magic-TryOn Turbo，高质量保存视频
这是我最推荐的实际产品方案。
是否能用 Magic-TryOn 改进 Scope VACEc
可以，最有价值的是复用 Magic-TryOn 的预处理：
upper-body mask
agnostic person
densepose
cloth line map
cloth caption


然后把这些作为 Scope VACE 的控制输入：
densepose → vace_input_frames
upper-body mask → vace_input_masks
cloth image → vace_ref_images
cloth caption → prompt
这会比我之前用粗略矩形 mask 好很多。
但即使这样，Scope VACE 还是不如 Magic-TryOn 本体精确，因为 Magic-TryOn 是专门训练过的 try-on 模型。
我的建议
如果你的目标是“实时虚拟试衣产品”，建议分两层：
1. 实时交互层
- Scope + VACE
- 做快速预览
- 低延迟
- 可接受衣服不完全一致
2. 高质量渲染层
- Magic-TryOn Turbo 1.3B
- 4step 分块生成
- 输出最终 MP4
- 衣服保持更好
我不建议一开始就追求“真正实时 + 高精度换衣”。更现实的是：
先做 1-3 秒延迟的准实时分块试衣
这在 H800 上更可行。

激活环境，在./datasets随即抽取3张衣服图片和3个视频，把衣服图片用红框固定在视频的每帧中，提示模型让视频中的人物换上红框中的衣服，完成后告诉我


如何运行
先激活环境，再指定模型目录运行：
source .venv/bin/activate
DAYDREAM_SCOPE_MODELS_DIR="/root/autodl-tmp/VTO/scope/.models" python scripts/random_redbox_tryon.py

Scope 是"壳"，Wan2.1 是"底模"，LongLive 和 VACE 是长在 Wan2.1 身上的两种不同改造方向

LongLive —— 把 Wan2.1 蒸馏成"实时自回归"的管线
Wan2.1-VACE​ 是直接基于 Wan2.1 权重微调出来的另一个权重版本，不是独立架构。
Scope 跑起来时用的权重，绝大部分是官方原版


1. 先用 Magic-TryOn 这类 SegFormer clothes parsing 当实时 baseline
2. 再补规则层或时序修正，扩大上衣 mask
3. 如果追求质量，再引入 CatV2TON AutoMasker 风格的人体解析 + DensePose 方案



确认了：当前 ICE 配置只有 Google STUN，没有 TURN。SSH -L 和 AutoDL HTTP 代理只能转发网页/API，不会转发 WebRTC 动态 UDP/TCP 媒体连接，所以页面能打开但视频预览为空是预期现象。
原因不是模型没跑，而是网页预览走的是 WebRTC 媒体流，不是普通 HTTP。
我刚检查了当前服务的 ICE 配置：
{
  "iceServers": [
    {
      "urls": ["stun:stun.l.google.com:19302"]
    }
  ]
}
也就是：只有 STUN，没有 TURN。
这在 AutoDL、云服务器、NAT、容器、SSH -L、HTTP 代理环境里通常不够，所以会出现：
网页能打开
API 能访问
模型能加载
但视频预览为空
ICE checking / ICE failed
为什么 SSH -L 不行
你用的是：
ssh -L 8000:127.0.0.1:8000 ...
它只转发了：
HTTP API
网页资源
WebSocket 信令
但 WebRTC 真正的视频流会尝试建立浏览器和服务器之间的媒体通道


具体情况
现在是：
本地浏览器 -> SSH -L / AutoDL HTTP 代理 -> Scope 8000
这只能保证：
网页能打开
HTTP API 能访问
WebSocket 信令可能能访问
但 Scope 网页预览的视频不是普通 HTTP，而是 WebRTC。WebRTC 需要浏览器和服务器之间建立媒体连接，常见协议/端口是：
UDP 动态端口
ICE candidate
STUN
TURN
我已经检查过你当前 Scope 返回的 ICE 配置：
{
  "iceServers": [
    {
      "urls": ["stun:stun.l.google.com:19302"]
    }
  ]
}
也就是说当前只有 STUN，没有 TURN。
STUN 只能帮双方发现公网地址，不能中继媒体流。在 AutoDL、云服务器、NAT、容器、HTTP 代理、SSH 端口转发环境下，经常会失败，所以会出现：
页面能打开
模型能加载
但视频预览为空
ICE checking
ICE failed
为什么 SSH -L 不够
你转发的是：
ssh -L 8000:127.0.0.1:8000 ...
它只转发 TCP 8000。
但 WebRTC 视频媒体流不是固定走这个 TCP 8000，它会协商额外的网络路径，通常包括 UDP。SSH -L 不会自动转发这些动态媒体端口。
所以：
HTTP 页面成功 != WebRTC 视频成功
解决方案优先级
最推荐：配置 TURN。
可接受：不用网页预览，继续用 HTTP output.ts 录制 MP4。
不推荐：尝试暴露大量 UDP 端口，云平台/容器/NAT 下仍然可能失败。
如果只在服务器本机浏览器访问，可能不用 TURN，但你现在不是这个环境。
方案 A：使用 Twilio TURN，最省事
如果你有 Twilio 账号，设置：
export TWILIO_ACCOUNT_SID="你的SID"
export TWILIO_AUTH_TOKEN="你的TOKEN"
然后重启 Scope。
重启后检查：
curl http://127.0.0.1:8000/api/v1/webrtc/ice-servers
如果成功，应该看到：
turn:
turns:
而不是只有：
stun:
方案 B：使用 HF_TOKEN，如果项目当前支持
Scope 日志里写了：
No Twilio or HF_TOKEN credentials found, using default STUN server
说明它可能支持通过 HF_TOKEN 获取 TURN。
你可以试：
export HF_TOKEN="你的 HuggingFace token"
然后重启 Scope，再检查：
curl http://127.0.0.1:8000/api/v1/webrtc/ice-servers
如果还是只有 STUN，说明当前环境没有拿到 TURN 或该方式不可用。
方案 C：自建 coturn
如果你有一台真正公网 IP 的服务器，可以部署 TURN。
安装：
sudo apt update
sudo apt install coturn
配置 /etc/turnserver.conf：
listening-port=3478
fingerprint
lt-cred-mech
realm=你的公网IP或域名
user=scope:your_password
external-ip=你的公网IP
no-loopback-peers
no-multicast-peers
开放防火墙：
3478/tcp
3478/udp
49152-65535/udp
然后需要让 Scope 的 ICE 配置返回这个 TURN。当前项目默认自动识别 Twilio/HF_TOKEN，不一定直接支持自定义 TURN 环境变量；如果你要走自建 coturn，我可以帮你改 Scope 的 WebRTC ICE 配置代码，让它读取例如：
TURN_URL=turn:你的公网IP:3478
TURN_USERNAME=scope
TURN_CREDENTIAL=your_password


实际工程里我建议的优先顺序
1. 先做 SegFormer mask + 类别感知扩张
2. 再改成 agnostic mask
3. 最后再尝试 soft mask 或两阶段
如果你现在就要一个最务实的改法
我会这样改：


python scripts/segformer_mask_tryon.py --video test/person1.mp4 --num-garments 3 --seed 6

1. 简单按原视频尺寸导出
可以在保存前把 512x512 的生成结果 resize 回 source_width x source_height。这样输出文件尺寸和输入一致，但模型实际生成内容仍然是基于 512x512 的，清晰度不会真正提升，只是上采样。

把原来的 Scope UI 挪到 /scope-ui，避免丢掉

当前 http://127.0.0.1:8000/ 上运行的是 Daydream Scope 后端服务

segformer-tryon为什么效果比不上 scripts/segformer_mask_tryon.py，该pipeline不是参考脚本来做的吗

- 论文：AnyFlow: Any-Step Video Diffusion Model with On-Policy Flow Map Distillation


第 1 步：准备数据
你需要的不是 AnyFlow 现在那种简单 video + prompt 数据，而是 MagicTryOn 完整条件数据。
每个样本至少要有：
- target video 或 target latent
- prompt / caption
- masked_video_latents
- pose_latents
- mask_input
- cloth_latents
- cloth_line_latents
- image_clip

- src/scope/core/pipelines/ 里总共 7 个 tryon pipeline 类
- 当前 pipeline_manager 的“内置”加载分支里实际显式处理 6 个：segformer-tryon、segformer-tryon-ref、segformer-tryon-person-ref、segformer-tryon-stable、segformer-tryon-fast、magic-tryon-distill，没把 segformer-tryon-longlive2 放进那个分支。pipeline_manager.py (</root/autodl-tmp/VTO/scope/src/scope/server/pipeline_manager.py:1038>)


# 为什么 LongLive 2.0 可以蒸馏
从 LongLive-main/README.md 和 trainer/distillation.py 看，它原生支持：
- train.py 训练入口
- trainer/distillation.py 蒸馏训练器
- configs/train_dmd.yaml / configs/train_i2v_dmd.yaml
- generator / real_score / fake_score 这种蒸馏结构
- FSDP、gradient checkpointing、LoRA adapter
- AR teacher-forcing 后再做 DMD distillation
也就是说，LongLive 2.0 的蒸馏是框架级能力，不是临时拼出来的。

# 为什么不能直接用当前 Scope 的 LongLive/VACE 蒸馏
因为 Scope 里的这条路径是：
- SegFormerTryOnStablePipeline
- MagicTryOnDistillPipeline
- LongLivePipeline
它们的目标是实时推理，不是训练


脚本用法
/root/autodl-tmp/VTO/Magic-TryOn/venv/bin/python scripts/cache_magictryon_teacher_vithd_full.py
默认参数就是面向大规模高质量缓存的：
- frames=49
- height=832
- width=624
- steps=20
如果要显式指定全量运行，也可以：
/root/autodl-tmp/VTO/Magic-TryOn/venv/bin/python scripts/cache_magictryon_teacher_vithd_full.py \
  --manifest datasets/magic_tryon_distill/vithd_10pct_manifest.jsonl \
  --output-dir datasets/magic_tryon_distill/teacher_cache_magictryon_1_3b_full \
  --start 0 \
  --limit 0 \
  --frames 49 \
  --height 832 \
  --width 624 \
  --steps 20

  启动方式:
set -a && source .env.local && set +a
PATH="/root/autodl-tmp/VTO/scope/.tools/bin:$PATH" \
UV_PYTHON="/root/miniconda3/bin/python3.12" \
setsid /root/autodl-tmp/VTO/scope/.tools/bin/uv run --python /root/miniconda3/bin/python3.12 \
daydream-scope --host 0.0.0.0 --port 8000 > .logs/server.log 2>&1 < /dev/null &
关闭方式:
pkill -f "daydream-scope --host 0.0.0.0 --port 8000"

set -a && source .env.local && set +a
.venv/bin/python scripts/segformer_mask_tryon_streaming_optimized.py \
  --video datasets/ViT-HD/subset_10pct/000016/video_000016.mp4 \
  --garment-image datasets/ViT-HD/subset_10pct/000016/reference_000016.jpg \
  --max-frames 48 \
  --no-parsing-video
使用示例：
set -a && source .env.local && set +a

.venv/bin/python scripts/segformer_mask_tryon_speed_profiles.py \
  --video datasets/ViT-HD/subset_10pct/000713/video_000713.mp4 \
  --garment-image datasets/garment/upper_body/cloth/01430_00.jpg \
  --max-frames 75 \
  --profile balanced448 \
  --profile fast384


cd /root/autodl-tmp/VTO/scope
source scripts/activate_scope_tryon_env.sh
python --version

我已经配好环境，参考scope/docs/vithd-000016-longlive-vace-tryon.md和scope/docs/local-startup.md的环境使用
下载/缓存都在当前目录，系统盘空间不够，网络不好使用镜像