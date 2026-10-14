# Virtual Try-on Video

# input

- agnostic video
 - agnostic image
 - mask
 - pose representations


 a novel DiT-based video
virtual try-on

SOTA

# KeyTailor（还没有开源）

关键帧采样
源视频 -> IKS选3帧 -> GDDE提服装特征 + CBDO提背景特征 -> 与姿态/掩码拼接 -> 注入DiT -> 出视频

KeyTailor的核心原理是以“关键帧”为信息锚点，在不改动扩散Transformer（DiT）主干架构的前提下，通过轻量化模块向生成过程注入细粒度细节，解决视频虚拟试穿中的服装动态丢失与背景失真问题。

具体而言，它首先利用视觉语言模型进行指令引导采样，从源视频中精准筛选出包含多视角和动作变化的关键帧；随后通过服装动态增强（GDDE）和协同背景优化（CBDO）两个模块，分别从关键帧中蒸馏出服装的褶皱、纹理等动态特征，以及背景的结构完整性特征。最终，这些增强特征以替换交叉注意力中的文本令牌和特征相加的方式注入DiT，配合LoRA微调，在不增加额外交互模块和大量参数的前提下，实现高保真、时序一致的视频合成。

核心痛点（三个挑战）：
# 1
细节不够：现有方法（如CatV2TON）生成的服装，背面的纹理、手臂举起时产生的褶皱、光影变化等动态细节经常丢失。
背景穿帮：生成的视频中，背景（如地板纹理、墙上画框）经常模糊或闪烁，与前景服装不协调。
模型太重、数据太少：为了提升效果，很多方法给DiT（扩散Transformer）加了很多额外模块，导致参数暴增、训练巨慢。同时，公开数据集（如VVT）分辨率低、样本少，喂不饱大模型。
核心解决方案（关键帧驱动细节注入）：

思路：与其让模型从头生成所有细节，不如从原始视频中挑选出信息最丰富的几个“关键帧”，像“作弊”一样把其中的服装动态和背景细节“提取”出来，再“注入”到生成过程中。

两大模块：用GDDE模块抓取服装细节，用CBDO模块抓取背景细节。

配套：自己建了一个高质量的大数据集ViT-HD，解决数据荒。

# 2
潜在的“软肋”（真正读懂的人会思考这些）：

推理时间：虽然参数量小，但它的推理时间（281秒）仍比Wan2.1（~203秒）和CatV2TON（209秒）慢不少（见表5）。这说明轻量级模块在生成阶段还是有额外开销。
依赖预处理：它高度依赖OpenPose和HumanParsing等预处理工具生成姿态和掩码。如果这些预处理步骤在复杂场景（如极端遮挡、剧烈运动）下出错，生成的视频质量会雪崩式下降。论文对此讨论不足。
极限泛化能力：作者在附录J中坦诚，处理“极其复杂”的服装-身体交互运动仍有困难。这说明当训练数据未覆盖的极端情况出现时，模型依然会失效。

# 3
它继承了CatV2TON用DiT的思路，但解决了CatV2TON细节不够的痛点，同时又比MagicTryOn更轻量。它的设计哲学是“先做减法（不加模块），再做加法（注入细节）”。

# CatV2TON （开源）
takes as input images
or videos of persons, 
clothing-agnostic masks, pose rep-
resentations, and target garment images.

CatV2TON提出了一个基于扩散Transformer（DiT）的统一虚拟试穿框架，通过将服装和人物在时间维度上简单拼接，配合混合图像-视频数据集训练，以仅微调骨干网络不到20%的参数，同时实现高质量的图像试穿和视频试穿（含长视频），并配套提出了长视频分段推理策略（AdaCN）和一个精炼的数据集（ViViD-S）。


# OIE 模型（还没有开源）
  基于DIT Diffusion Transformer 

# iTryOn（还没有开源）



# 传统视频试穿的做法像PS：
把衣服从图片上"抠"下来
用算法把衣服变形、扭曲，贴合人体的姿势
贴到人身上
问题很明显：人一转身、手一挡脸、衣服皱起来，就露馅了（遮挡、形变失真）。

# 新一代方法直接用扩散模型（Diffusion Model，就是Stable Diffusion那套）来"画"出穿新衣服的人，不再靠机械变形，而是让AI理解衣服长什么样、人体怎么动，然后重新生成每一帧画面。


1. 为什么“抠图+粘贴”（传统形变法）会失败？
你设想的流程是：提取服装 → 变形贴合人体 → 贴回原视频。这在静态图或简单转身时尚可，但一旦遇到真实视频，三个“死穴”就会暴露：

遮挡灾难（Occlusion）：当手、头发或物体挡住衣服时，“抠图”只能抠出被遮挡的碎片。传统算法无法“脑补”出被挡住的那部分纹理，只能硬拉，导致换上去的衣服出现“空洞”或“错位”（如CatV²TON论文提到的“手臂举起时背面纹理丢失”）。

形变失真（非刚性变形）：衣服是布料，会有褶皱、拉伸和飘动。传统方法用数学网格（如TPS薄板样条）去扭曲衣服，无法处理大幅度的3D旋转。比如人一转身，正面衣服纹理被强行扭到背面，会产生严重的撕裂感和模糊（即你报告中提到的“PS式机械变形”）。

边缘闪烁与背景割裂：逐帧抠图会导致衣服边缘像“纸片”一样抖动（闪烁），且因为光照无法随环境变化，贴上去的衣服与原背景有明显的“拼接感”，显得极不真实。

2. DiT（扩散模型）虽然慢，但解决了什么？
DiT采用“毁灭与重生”的策略：它不保留原视频中的像素，而是将姿态、遮罩、服装图像作为“文字提示”，利用大模型的先验知识重新绘制每一帧。

生成遮挡部分：当手挡住衣服时，DiT会“推理”出手臂下方应有的衣摆褶皱，而不是硬抠。

保持物理一致性：它能根据人体姿态生成符合重力、拉伸规律的动态褶皱和光影（这正是KeyTailor强调的“细节注入”）。

背景和谐：它是全图重新绘制，因此服装与背景的光影、色调是融合的，不会出现纸片感。


# 能否用“一张图片 + 一段视频流”实现实时虚拟试衣？
从技术上看是可行的，但这通常不是“通用世界模型”的直接应用，而是由专门的“虚拟试衣”模型来完成。

可行性：目前已经有专门的AI模型可以实现这类功能。例如，Lucy 2.0 模型就支持通过文字或参考图，在视频中实时换衣服。另一个名为 Lucy VTON 的系统，甚至能通过实时摄像头画面流，根据文字描述或服装参考图，为视频中的人物进行逼真的虚拟试穿。

技术路径：这类模型不依赖复杂的3D建模，而是通过扩散模型直接学习视频中的物理变化和服装纹理来实现试穿效果。

# RVT
为每件衣服收集专属数据集，并为每件衣服训练一个专属模型

# 阶段一：准备“人体模特”的基础能力（训练 BodyMap 网络）
你不能随便拍，需要一个固定的模特（论文中称为Human Model）。

录制紧身衣视频：让该模特穿着紧身衣（为了暴露真实身体轮廓），按照预设动作（如原地旋转）录制一段视频。

提取数据：从这段视频中，提取“服装不变表示”（6通道图）和对应的“真实人体语义图”（通过DensePose获取）。

训练辅助网络：用这些数据训练一个名叫 BodyMap 的辅助网络（基于pix2pixHD）。这个网络的作用是：以后即使模特穿宽松衣遮住身体，只要输入“服装不变表示”，它就能脑补出被遮住的人体骨骼和语义图。


# 阶段二：采集目标衣服的“原始视频”（数据采集）
现在开始针对你想要的那件具体衣服（比如那件汉服）进行操作：

模特换上目标宽松衣：让同一个模特穿上这件汉服。

执行相同动作：让模特再次执行与阶段一完全相同的预设动作（如原地旋转），并录制视频。

# 3
生成汉服的“标准答案数据集”（耗时3小时，代码自动跑）

得到 汉服专属 ReGarSyn 模型权重


预设动作必须标准化：论文中模特旋转的速度、角度必须固定。如果第1幕紧身衣转得快，第2幕汉服转得慢，生成的BodyMap会有严重偏差，训练出来的汉服模型会崩掉。

不要试图换脸换头：这个模型只管衣服。如果模特是瘦子，你是个胖子，推理时虽然论文说能泛化（图13），但袖子长短会穿模，因为它没有真实的物理碰撞模拟，只是2D图像扭曲。

12小时只是训练，数据标注要更久：SAM2自动抠图虽然省事，但遇到汉服褶皱重叠时容易抠错，你可能需要人工修正几百张关键帧，这部分时间成本至少是训练的3倍。

# MagicTryOn 
MagicTryOn 基于 DiT（Diffusion Transformer），其核心是 全自注意力机制（Full Self-Attention）。

在模型内部，第 
t
t 帧（比如第 30 帧）的像素，需要去“关注”（Attention）第 
t
−
1
t−1 帧（第 29 帧）和第 
t
+
1
t+1 帧（第 31 帧）的同一个衣服纹理长什么样。n

如果每次只输入 1 帧，模型根本看不到前后帧，无法计算“帧与帧之间的对应关系”，那它就只能瞎猜衣服在下一帧怎么变形，结果必然是严重的画面抖动

Lucy Virtual Try-On 3模型：

硬件感知的自定义架构与 Mega-Kernels：根据加速器（NVIDIA GPU、AWS Trainium 等）的周期级微基准测试定制模型结构，使用大型融合内核（mega-kernels）减少启动开销和内存搬运，让激活值尽量靠近 Tensor Core，避免昂贵的 HBM 访问。
低精度量化与稀疏注意力：采用 MXFP8 / NVFP4 等混合精度，配合动态稀疏注意力，大幅减少计算量，同时保持质量（不同网络部分用不同精度）。
Shortcut Distillation + 剪枝：通过蒸馏和模型剪枝减少每帧所需计算量。
自定义 WebRTC 传输管线：专为双向视频流优化，最小化缓冲和传输延迟，确保全球范围内低延迟。
DOS（Decart Optimization Stack）：自研超优化的推理与训练基础设施，支持高利用率（可达到很高的 Tensor Core 利用率），并在专用加速器上跑得更快。

# Daydream Scope
只能对自回归模型使用，其他模型不适合（要改造）
按 chunk / frame 逐步生成


- 输入稳定性不同
- scripts/segformer_mask_tryon.py 读的是固定视频文件，帧率、分辨率、帧顺序都稳定。
- segformer-tryon 吃的是实时 WebRTC/camera chunk，可能有抖动、丢帧、时间间隔不均、首帧不稳定。
- chunk 策略不同
- 脚本使用更稳定的离线 chunk 流程，例如之前记录里是 FRAMES_PER_CHUNK = 12、OVERLAP_FRAMES = 3。
- pipeline 当前默认多为 chunk_frames=8 或更短，实时延迟低，但上下文少，衣服更容易漂。
- overlap stitching 不同
- 脚本可以用 overlap 做过渡，把前后 chunk 接起来，减轻闪烁。
- realtime pipeline 通常直接输出当前 chunk，没有完整离线式 overlap/stitching，否则会增加延迟。
- reference image 使用策略不同
- 脚本之前效果好的关键之一是：只在第一个 chunk 使用 vace_ref_images，后面依赖 autoregressive/cache 延续。
- 原 segformer-tryon / segformer-tryon-ref 曾为了增强衣服参考，默认每个 chunk 传参考图。这样可能更强，但也更容易参考图泄漏、画面不稳定。
- cache 状态更容易被破坏
- 脚本是单次连续运行，cache 连贯。
- pipeline 受实时会话、参数变更、输入抖动、pipeline 调度影响，cache 连续性更难保证。
- mask 连续性不同
- 脚本对完整视频连续处理，mask 时间上更一致。
- pipeline 实时分 chunk 处理，SegFormer 每个 chunk 独立跑，边界更容易

为什么LongLive/VACE 实时效果（pipeline 中的SegFormertryon）比不上离线处理 脚本（ Scope LongLivePipeline + SegFormer ）


# 要让实时效果接近离线脚本，通常要做这些优化：
- 预先缓存 garment embedding / reference conditioning
- SegFormer 与 LongLive 分离成异步流水线
- mask 低频更新，帧间光流/传播补齐
- 使用固定滑窗，例如 12 帧推理、3 帧 overlap，但用队列隐藏等待
- 保持模型常驻 GPU，避免动态加载和 CPU offload
- 降低分辨率或减少 denoising steps
- 用 Turbo/蒸馏版模型替代 20-step diffusion


# 根本解决方向
要实时，不能只“优化脚本”。需要改变模型和系统设计。
1. 从 20 step 变成 1-4 step
这是最关键的。需要蒸馏：
- DMD / consistency distillation
- LCM-style video distillation
- flow matching few-step distillation
- teacher: MagicTryOn/CatV2TON
- student: 小型 try-on video model
目标是把 20 次 denoise 压到 1-4 次。
2. 训练专用实时学生模型
不要直接实时跑 14B 或 EasyAnimate base。训练一个小模型：
- 输入：人物帧/短窗口 + mask + pose + garment embedding
- 输出：替换衣服后的短窗口
- 模型规模控制在 1B 以内，最好几百 M
- 支持 causal/streaming temporal state
3. 服装图只编码一次
用户上传衣服后：
- CLIP/视觉 embedding 预计算
- garment texture features 预计算
- line/segmentation/caption 预计算
- 后续每帧复用
4. mask/pose 不要每帧重算完整模型
实时路径应当：
- 每 N 帧跑一次 SegFormer/DensePose
- 中间帧用 optical flow / tracking / lightweight segmentation 传播
=d- 或用轻量人体解析模型替代 SCHP/DensePose
5. Build用流式滑窗，而不是整段视频生成·GPT-5.5OpenAI
例如：
/root/autodl-tmp/VTO/scope- 缓冲 8-12 帧
- overlap 2-3 帧
- 每次只吐出后面的新帧
- 保留 latent/cache/state
- 不重复计算已生成窗口
6. 去掉重型文本编码器在线路径
T5/UMT5 很重。实时系统里应当：
- caption 离线生成一次
- 或不用文本，直接用 garment visual embedding
- 或把文本 embedding 缓存
7. 降低分辨率，后接实时增强
实时生成可以先做：
- 256x384 或 384x512
- 再用轻量超分/细节增强
- 对衣服区域局部增强，而不是全帧增强
8. 模型常驻 GPU
不能有 CPU offload、频繁加载、频繁 tokenizer/encoder 初始化。实时服务必须：
- model warm
- CUDA graph / torch compile
- 固定 shape
- pinned memory
- 异步 pipeline

最现实的路线
1. 先用 LongLive/VACE 或 MagicTryOn Turbo 做基线，因为它们更接近少步数。
2. 收集 MagicTryOn/CatV2TON 离线高质量结果作为 teacher 数据。
3. 训练一个专用 few-step student。
4. 用 SegFormer/AutoMasker 生成训练条件，但线上换成轻量 mask + tracking。
5. 做固定分辨率、固定窗口、固定 batch 的 CUDA 优化。
结论：MagicTryOn/CatV2TON 慢的主要原因是多步视频扩散 + 大型 DiT + 多条件预处理。要实时，必须蒸馏成少步小模型，并把预处理、服装编码、滑窗推理全部流式化和缓

大胆一点的实时方案
我会这样设计：
模块	实时方案
Garment encoder	上传衣服时跑一次，缓存 garment token/texture map
Human parser	轻量 segmentation，每 5-10 帧一次
Mask tracking	optical flow / video tracker 传播 mask
Pose	可选，低频估计或不用 DensePose
Generator	1-4 step distilled causal video try-on student
Temporal memory	保存上一窗口 latent/state
Output	8-12 帧滑窗，输出 4-8 新帧
Enhancement	衣服区域轻量超分/锐化
目标性能：
阶段	目标
预处理首帧	< 1s
garment embedding	< 0.5s，只做一次
单窗口生成	< 200-300ms
实时输出	15-30 fps
延迟	0.5-1.5s 可接受