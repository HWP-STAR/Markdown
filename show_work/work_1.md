- Scope pipeline：segformer-tryon / segformer-tryon-ref 用的是 LongLive-1.3B + Wan VACE module + SegFormer mask 做实时 VACE inpainting/reference conditioning。

LongLive + VACE 是通用实时视频生成/控制模型，不是专门的虚拟试衣模型

 训练/接入 try-on LoRA 给 LongLive/VACE。
  使用专门蒸馏过的实时 try-on 模型，才可能兼顾实时和质量。

  Scope pipeline：segformer-tryon不是参考scope/scripts/segformer_mask_tryon.py脚本处理的吗，为什么效果比不上scope/scripts/segformer_mask_tryon.py

# magictryon 模型
输入：
每个样本至少要有：
- target video 或 target latent
- prompt / caption
- masked_video_latents
- pose_latents
- mask_input
- cloth_latents
- cloth_line_latents
- image_clip

# 做 SegFormer mask 感知扩张
- 继续用 SegFormer 找上衣区域
- 基于人体 bbox 做非对称扩张：
- 左右各扩 10% ~ 18%
- 向上扩 3% ~ 6%
- 向下扩 15% ~ 30%
- 如果参考衣服像连衣裙/长款上衣，再向下扩到臀部甚至大腿上部
- 对边界做一次高斯羽化，生成 soft mask


# WebRTC 真正的视频流会尝试建立浏览器和服务器之间的媒体通道
用的是：
ssh -L 8000:127.0.0.1:8000 ...

# 模型
Scope 是"壳"，Wan2.1 是"底模"，LongLive 和 VACE 是长在 Wan2.1 身上的两种不同改造方向

LongLive —— 把 Wan2.1 蒸馏成"实时自回归"的管线
Wan2.1-VACE​ 是直接基于 Wan2.1 权重微调出来的另一个权重版本，不是独立架构。

- try-on 生成模型：Scope LongLivePipeline
- mask 模型：mattmdjaga/segformer_b2_clothes
- VACE/LongLive 权重：
- .models/LongLive-1.3B/models/longlive_base.pt
- .models/LongLive-1.3B/models/lora.pt
- .models/WanVideo_comfy/Wan2_1-VACE_module_1_3B_bf16.safetensors
- .models/WanVideo_comfy/umt5-xxl-enc-fp8_e4m3fn.safetensors
- .models/Wan2.1-T2V-1.3B/google/umt5-xxl

# 模型效果
编写并运行了 MagicTryOn /蒸馏模型哦 离线 benchmark
我新增了这些脚本：
- scripts/prepare_vto_benchmark_inputs.py
- scripts/benchmark_magictryon_models.py

# 新增了 segformer-tryon-person-ref pipeline
你提出新思路：
不改原 segformer-tryon-ref，新增一个 pipeline：把整个人物 mask 掉，上传的图片是换衣后的整个人物参考图，模型参考这张图在 mask 区域生成视频流。
我新增了独立 pipeline，没有改原 segformer-tryon-ref 行为。
新增文件：
src/scope/core/pipelines/segformer_tryon_person_ref/__init__.py
src/scope/core/pipelines/segformer_tryon_person_ref/schema.py
src/scope/core/pipelines/segformer_tryon_person_ref/pipeline.py
修改注册文件：
src/scope/core/pipelines/__init__.py
src/scope/core/pipelines/schema.py
src/scope/server/pipeline_manager.py
新增 pipeline id：
segformer-tryon-person-ref
行为：
用 SegFormer 生成人物区域 mask
默认人物标签：1-15,17，排除 bag=16
上传图语义改为“换衣后的人物参考图”
prompt 改成 reference-person inpainting
vace_ref_images / garment_image_path 指向人物参考图
默认固定 512x512
加载参数传其他尺寸时也会固定回 512x512

# 不同的pipeline
Pipeline	参考图语义	Mask 区域	主要目标	典型效果
segformer-tryon	服装图	上衣/手臂相关区域	基础实时试衣	能换衣，但可能参考图泄漏或衣服不稳定
segformer-tryon-ref	服装图	上衣/手臂相关区域	减少参考图泄漏	比基础版更少出现悬浮衣服/图中图
segformer-tryon-stable	服装图	更平滑、更扩大的上衣区域	稳定性优先	闪烁更少，但速度更慢、编辑区域更保守
segformer-tryon-fast	服装图	上衣区域，mask 降频推理	低延迟	更快，但细节和稳定性可能弱一些
segformer-tryon-person-ref	换衣后人物参考图	整个人物区域	参考人物图驱动重绘	可以迁移整个人物造型，但身份/脸/身体更容易漂移


# 1
它解决的问题：
- 自动从输入视频中找到上衣区域
- 不需要用户手动画 mask
- 可以用一张服装图驱动视频换衣
它的问题：
- 参考图可能泄漏到画面里，比如出现悬浮服装、图中图、边框
- 每个 chunk 独立生成，衣服纹理可能闪
- mask 只覆盖当前衣服布局，如果目标衣服版型差异很大，生成空间不足
- 如果原衣服区域太小，模型容易只“重绘原衣服”，不一定完整生成目标衣服
适合：
- 快速验证服装图试衣
- 原衣服和目标衣服版型接近的场景
- 不追求最高稳定
配置重点：
项	值
默认分辨率	512x512
chunk	8 帧
mask labels	[4, 7, 14, 15]
参考图	garment_image_path
VACE strength	1.5
reference every chunk	true


# 2 
这是基础版的防泄漏增强版。
它继承 segformer-tryon，主要改了 prompt。
新增 anti-leak prompt：
Use the garment reference only as clothing appearance guidance.
Do not show the reference image, product photo, clothing catalog image,
picture-in-picture panel, floating garment, duplicate garment, border, frame,
or any standalone clothing image in the video.
Only the person should wear the garment naturally on their body.
它解决的问题：
- 减少参考服装图片被直接画进视频
- 减少“图片贴片”“服装悬浮”“重复服装”
- 强调衣服应该自然穿在人身上

为什么 VACE strength 比基础版低：
- 基础版 1.5 参考图影响强，容易泄漏
- ref 版降到 1.25，让参考图更像“外观指导”，不是直接复制图片
适合：
- 服装图换衣
- 不想画面里出现参考图本身
- 比基础版更稳一点的在线 try-on
代价：
- 参考图约束弱一点，衣服细节可能没有基础版强
- 如果目标衣服图案复杂，可能不如强参考时还原得
配置重点：
项	值
默认分辨率	当前 loader 里是 864x480
chunk	8 帧
VACE strength	1.25
reference every chunk	true
mask 区域	上衣/手臂区域


# 3
这是稳定性优先版。
它继承 segformer-tryon-ref，核心思路是：
更长 chunk
更平滑 mask
更大的 mask dilation
更低参考强度
不每个 chunk 都重复注入参考图

它解决的问题：
- 衣服区域帧间闪烁
- mask 边缘抖动
- 每个 chunk 重复参考图导致的外观跳变
- 过强参考图注入导致的泄漏
它的效果：
- 时序更稳
- 衣服边界更连续
- 背景/人物不容易突然重绘
- 更接近“可持续视频流”的体验
代价：
- 速度比基础版慢
- 参考图细节可能弱
- mask 更大，可能影响身体/手臂更多区域
- 如果只想快速看效果，不如 fast 或基础版轻
适合：
- 更长时间的视频流
- 对稳定性要求高的 demo
- 不希望衣服每几帧就跳

配置重点：
项	值
默认分辨率	当前 loader 里是 864x480
chunk	12 帧
VACE strength	1.15
reference every chunk	false
morph kernel	9
mask dilation	11
mask_smoothing_alpha	0.55

# 4. segformer-tryon-fast
这是低延迟版。
它的目标不是最高质量，而是尽量降低实时交互延迟。
配置重点：
项	值
默认分辨率	368x640
chunk	已修为 8 帧
VACE strength	1.05
reference every chunk	false
morph kernel	5
mask dilation	7
mask_stride	2


mask_stride=2 的意思：
不是每一帧都跑 SegFormer
每 2 帧跑一次 mask
中间帧插值/复用 mask
它解决的问题：
- SegFormer 每帧推理造成延迟
- 分辨率高造成 LongLive/VACE 慢
- reference 每 chunk 注入造成开销和泄漏
为什么我把它从 4 帧 chunk 修到 8：
- 4 帧对 VACE/LongLive 上下文太短
- 太短会导致生成不稳定、衣服语义不足、时序漂移
- 8 帧仍然比 12 帧低延迟，但比 4 帧更稳
它的效果：
- 延迟更低
- 帧率更好
- 适合在线预览
代价：
- mask 不逐帧更新，快速动作时边界可能滞后
- 分辨率较低
- 参考图细节更弱
- 复杂衣服图案更容易丢失
适合：
- 实时交互预览
- 先让用户看到大致效果
- 后台再用 stable/offline 做高质量版本

核心差异：mask 范围
Pipeline	Mask 范围	优点	风险
segformer-tryon	上衣 + 手臂	保留身份和背景较好	目标衣服版型受限
segformer-tryon-ref	上衣 + 手臂	减少参考图泄漏	细节可能弱
segformer-tryon-stable	平滑/扩大上衣区域	时序更稳	慢，编辑范围更大
segformer-tryon-fast	上衣区域，mask 降频	快	mask 滞后，细节弱
segformer-tryon-person-ref	整个人物	造型迁移能力强	身份/脸/身体漂移

# 提示词
原来：Use reference clothing images as clothing references. Let the person  in the input video naturally put on the upper garment, with a fitted shoulder and torso, realistic folds, and stable movements. Retain the person's identity, face, posture, camera frame, hands, pants, lighting, and background. Do not add floating clothes, copied clothes, or additional accessories.

修改：
Reference clothing images are provided solely for garment extraction and must NOT appear as visible content in the video frames. The input video person naturally puts on the upper garment with a fitted shoulder and torso, realistic fabric folds, and stable motion. Strictly preserve the person's identity, facial features, posture, camera framing, hands, lower-body clothing, lighting, and background. Prohibit floating garments, duplicated clothing layers, extra accessories, and any insertion of reference images into the scene.

Condition on the provided clothing reference images for apparel appearance only; do not render the reference images themselves. Transfer the upper garment onto the subject in the input video with anatomically correct fit at shoulders and torso, physically plausible folds, and temporally stable motion. Maintain strict identity consistency: preserve face, skin tone, body pose, camera viewpoint, hands, pants, scene lighting, and background across all frames. Forbid ghosting, double garments, floating clothes, accessory additions, or any visual artifacts from reference images.

Use clothing references for garment style only; never show reference images in video. Fit upper garment naturally to shoulders and torso with realistic folds and stable motion. Keep identity, face, pose, camera, hands, pants, lighting, background unchanged. No floating clothes, copied layers, accessories, or reference-image artifacts.


# 调节参数参数
- reference every chunk
- vace_context_scale: 参考图/条件对生成结果“施加多大力”（- 值越高，模型越会努力去贴近参考图，值越低，模型越偏向自然生成、保留原视频状态，默认1.5）
- morph_kernel: 分割出来的 mask 先做多强的去噪和平滑
- mask_dilate_kernel: 把 mask 往外扩多大
- mask_smoothing_alpha: mask 在时间维度上平滑多少（默认0.55）





# 蒸馏
没有完成完整蒸馏。已推进到 smoke 阶段并确认了阻塞点：当前 Scope 里的 LongLive/VACE 是 inference-only runtime，denoise/decode/VACE encoding 等 block 使用 @torch.no_grad()，输出没有 grad_fn，所以不能直接对 LoRA 反传训

# wan2.1
抛弃传统的GroupNorm，改用 RMSNorm 以保证因果性，并配合 分块特征缓存（Chunk-wise Cache）。处理下一段视频时，只缓存前两帧特征，丢弃更早的
RMSNorm只对当前帧本身的特征做归一化（计算均方根），完全不依赖其他帧的统计信息。每一帧都是独立归一化

## 传统方式（无缓存）：
把240帧一次性全部塞进VAE → 显存爆炸（尤其高分辨率下）

或者分成多个独立块处理，但块与块之间没有信息传递 → 视频拼接处会出现闪烁/不连贯

Wan的缓存方式



“多模态、多任务”的统一框架（VACE）

# longlive

LONGLIVE的定位：在单张H100显卡上，实现实时生成，支持最长240秒（4分钟）的长视频，且允许用户在生成过程中随时输入新提示词，画面平滑过渡。

# longlive 蒸馏
DMD 能把多步扩散模型压成单步/少步生成器
step 越少，画质/细节/稳定性可能会有下降
（ 默认 4-step）
4-step -> 2-step

tryon 一致性可能变差
对试衣来说，风险比普通文生视频更敏感：
衣服版型不稳定
衣摆/袖口闪烁
遮罩边界附近容易穿帮
人体和衣服贴合度下降

粒度：不是一帧一帧生，而是块（Chunk） 生
流程：模型每次吃进前文缓存，吐出下一个 3帧块，然后将这 3帧的 KV 状态存入缓存，继续预测下一块。


#####

这条流程可以拆成 4 段：
1. 视频解码 / resize / 拼 chunk
2. SegFormer 分割
3. mask 后处理与 VACE 输入准备
4. LongLive/VACE 扩散推理
这 4 段的优化价值完全不同

一条常驻进程，内部 4 个并行模块：
1. NVDEC/ffmpeg 视频解码器  
2. SegFormer TensorRT 分割器  
3. Mask Tracker + GPU 后处理  
4. LongLive/VACE GPU Worker
所有模块都常驻显存，不重复初始化，不重复加载模型，不重复 warmup。输入视频被切成滑动窗口，但窗口状态保留在 GPU 上，不回退到 Python 逐帧调度

是：
用 TensorRT 加速 SegFormer，用常驻 PyTorch 保留 LongLive/VACE，用 mask 跟踪减少分割次数，用 GPU ring buffer 和异步多流把整条 chunk 流水线做成低拷贝、低重复、常驻执行的混合推理引擎。