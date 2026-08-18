# 实验
：datasets/garment/upper_body/cloth/00462_00.jpg
速度结果
A. 基线  
chunk=12 overlap=3 mask_every=1
mask_seconds = 3.55s
inference_seconds = 21.91s
end_to_end_fps = 4.75
peak_gpu_memory_mb = 19070
B. 只改窗口  
chunk=16 overlap=2 mask_every=1
mask_seconds = 3.15s
inference_seconds = 15.83s
end_to_end_fps = 4.85
peak_gpu_memory_mb = 20856
C. 改窗口 + 降低分割频率  
chunk=16 overlap=2 mask_every=2
mask_seconds = 2.48s
inference_seconds = 15.22s
end_to_end_fps = 5.20
peak_gpu_memory_mb = 17314
对比分析
A -> B
只把 12/3 改成 16/2，总速度只小幅提升：
4.75 -> 4.85 FPS
提升大约 2%
这说明单纯减少 overlap 和 chunk 数量，帮助有限，但确实有正向效果。
B -> C
在 16/2 基础上把 SegFormer 改成每 2 帧跑一次，速度提升明显：
4.85 -> 5.20 FPS
提升大约 7%
A -> C
从基线 A 到方案 C：
4.75 -> 5.20 FPS
总提升大约 9.4%
所以这轮实验的结论是：
我提出的方向是有效的
但“只改 chunk/overlap”收益不大
“减少分割频率”比“改窗口参数”更值
当前主瓶颈仍然是 LongLive/VACE 推理，不是 SegFormer
效果观察
我这里没有做自动图像质量评分，只能基于这三组输出的结构判断：
A：最稳，mask 每帧更新，边缘更保守
B：和 A 观感应该接近，主要是调度差异
C：理论上会有更高概率出现边缘迟滞或小幅闪动，因为偶数帧直接复用了前一帧 mask
但在这条样本视频上，C 仍然是最值得继续挖的方向，因为速度收益已经开始出现，而代价还不算大
你可以直接看这三个输出：
exp_A_tryon.mp4 (/root/autodl-tmp/VTO/scope/outputs/segformer_mask_tryon_streaming_benchmark/20260813_204401/exp_A_tryon.mp4)
exp_B_tryon.mp4 (/root/autodl-tmp/VTO/scope/outputs/segformer_mask_tryon_streaming_benchmark/20260813_204401/exp_B_tryon.mp4)
exp_C_tryon.mp4 (/root/autodl-tmp/VTO/scope/outputs/segformer_mask_tryon_streaming_benchmark/20260813_204401/exp_C_tryon.mp4)
结论
目前最好的实验配置是 C：
chunk=16
overlap=2
mask_every=2
但这轮结果也说明了一件更重要的事：
如果目标是大幅提速，光靠脚本层 chunk 策略优化不够。  
下一步真正值得做的是：
SegFormer batch 化保留，并进一步做 TensorRT/ONNX
继续提高 mask_every，但加时序平滑或插值，避免效果掉太多
更深地优化 LongLive/VACE 本体，因为它还是大头

# 优化
改成 4 个常驻模块并行工作：
1. Decode/Resize Worker
2. SegFormer Worker
3. Mask Temporal Worker
4. LongLive/VACE Worker
它们之间用固定大小 ring buffer 连接，不再每个 chunk 重建一堆中间对

模块 1：视频解码与滑窗缓冲
具体做法：
- 输入统一转成固定分辨率，默认 384x384
- 使用滑动窗口：
- chunk_size = 16
- overlap = 2
- 实际步长 14
- 建立 GPU/CPU 共享 ring buffer，存最近 16 帧
- 每来 14 帧，触发一次新的 VACE 推理
- 不再为每个 chunk 重新切整块 numpy/tensor
为什么这样做：
- 比 12/3 少重复计算
- overlap 成本更低
- 时序连续性还够用

模块 2：SegFormer 深度优化
这是最值得动的一层。
具体做法：
1. 不再逐帧单独跑 SegFormer
2. 改成 chunk 内 batch 推理
3. 不再每帧都跑分割，而是低频运行
建议策略：
-分辨率固定 512x512 ，- mask_every=1 效果好

- 16 帧 chunk 中，只在 0, 4, 8, 12 这些关键帧跑真实分割
- 也就是 mask_every = 4
- 如果效果不够稳，退到 mask_every = 2
实现方式：
- 把 SegFormer 独立导出 ONNX
- 再转 TensorRT FP16 engine
- 每次送一批关键帧进去，例如 4 帧 batch
- 输出 logits 后不落回 CPU，直接在 GPU 上做：
- argmax
- label 选择
- morphology
- dilate

模块 3：Mask 时序稳定层
这是让“少跑分割”还能保持效果的关键。
具体做法：
1. 对关键帧得到的 mask 做 EMA 平滑
2. 用相邻关键帧之间的线性或光流传播生成中间帧 mask
3. 对 mask 做区域清理：
- connected components
- torso ROI 限制
- 边缘平滑
4. 可加一个“上一 chunk 尾帧 mask 作为先验”的状

模块 4：LongLive/VACE 核心推理优化
这一层不建议先做全链路 ONNX。最优做法是保留 PyTorch，但把执行形态改成“常驻 + 缓存 + 固定 shape”。
具体做法：
1. LongLivePipeline 只初始化一次
2. garment reference 首 chunk 编码一次，缓存特征
3. text prompt 首次编码一次，缓存 embedding
4. 输入 shape 固定：
- B=1
- T=16
- H=W=384
5. 基于固定 shape 尝试：
- flash_attn 2
- torch.compile
- CUDA Graph capture
6. 不再每个 chunk 重建 input_chunk / mask_tensor 的新存储
7. 用预分配 GPU tensor，把新增帧直接写进 buffer

VACE 输入构造优化

最佳做法：
1. 这三步都尽量搬到 GPU
2. gray fill 直接对 GPU tensor 原位写
3. mask tensor 保持常驻
4. 只更新当前新增帧对应的时间片
也就是：
- 不再“每个 chunk 整块重做”
- 改成“对滑窗里的新增部分增量更新”

异步执行模型
用三条 CUDA stream：
1. stream_decode_preprocess
2. stream_segformer
3. stream_vace
执行重叠关系：
- decode(n+2)
- segment(n+1)
- infer(n)
同时并行。
这和现在脚本的串行模式差别很大。当前脚本实际上还是：
读一块 -> 分一块 -> 推一块 -> 再读下一块
最佳方案要改成真正的流水并发

输出策略
不再等全视频结束再保存。
文件模式：
- 每个 chunk 完成后，把新增帧写到输出 writer
实时模式：
- 每个 chunk 去 overlap 后，立刻推送新增帧到 sink
这样这条链才真的接近“流式

量化策略
这里要明确：
- SegFormer：不做 4bit，直接 TensorRT FP16
- LongLive/VACE：4bit 不是默认主线
具体建议：
- 如果显存压力大，才尝试对 LongLive/VACE 做 weight-only quant
- 量化目标是让 chunk 更大、分辨率更高、OOM 更少
- 不要预设 4bit 一定更快

默认配置建议是：
- 分辨率：384x384
- chunk_size = 16
- overlap = 2
- mask_every = 2 或 4
- SegFormer：TensorRT FP16 batch
- LongLive/VACE：PyTorch FP16/BF16 常驻
- mask smoothing：开启
- garment/text 特征缓存：开启
高质量模式：
- 448x448
- mask_every = 2
更高质量模式：
- 512 * 512
- mask_every = 1
更快模式：
- 320x320
- mask_every = 4

如果要开始做，具体代码顺序应该是
1. 把当前 streaming 脚本重构成可插拔模块
2. 先固定 chunk=16 overlap=2
3. 加 mask_every 和 mask 复用
4. 加 mask smoothing
5. 把 SegFormer 改成 chunk batch 推理
6. 再把 SegFormer 独立替换成 TensorRT
7. 再做 VACE 输入 buffer 常驻化
8. 最后做多 stream 异步和实时输出

完成这些优化工作后使用优化后的方案和基线方案做对比（看看效果和速度如何）

# 优化2
做进去的东西：
四个常驻 worker 的结构已经落地
bounded ring buffer 用 queue.Queue(maxsize=3) 落地
SegFormer 关键帧 batch 推理和 mask temporal smoothing 都在
LongLive/VACE 预分配输入 tensor、增量写入也在
CUDA stream 路径可切换
现在输出写盘改成了显式 cv2.VideoWriter
最关键的是，输出 mp4 实际帧数已经修正并验证为和输入一致
验证结果：
ffprobe 证明 full optimized 最终输出是 48 帧，不再少帧
ruff check 和 ruff format --check 都通过
这次对比用的是 datasets/person/customize/video/00001/video.mp4 和 datasets/garment/upper_body/cloth/01430_00.jpg
最终对比，48 帧：
Baseline: 4.2067 fps, 11.41s
Full optimized: 8.2590 fps, 5.81s
也就是在这组样本上，完整优化版大约快了 ~1.96x。
还有一条要实话实说：
SegFormer ONNX/TensorRT FP16 engine 的导出接口已经留在 full optimized 脚本里
但这台环境没有 onnx / onnxruntime / tensorrt / polygraphy
所以我没有办法在当前环境里把 TRT 引擎真正构建并运行成实测结果
也就是说，导出链路“代码上已经接好”，但 TRT 运行时不是这个机器现成能验证的
关于你最开始点名的“为什么没完成”的项，现在的状态是：
多 worker: 已完成
CUDA streams: 已完成并可切换
VACE 常驻预分配输入: 已完成
输出逐 chunk 写出: 已完成
帧数对齐: 已完成
SegFormer TRT: 代码路径已接好，但当前环境缺运行时依赖，无法给出真机 TRT 实测
如果你要继续往前推，下一步最值得做的是把 TRT 依赖装齐后，把 --export-segformer-onnx 和 --build-segformer-engine 真正跑通，然后再把 SegFormer worker 切成 TRT runtime。


. 降低 denoising steps
-降低分辨率 448/384
448x448
denoising_steps = [1000, 750]
mask_every=1
速度/质量折中


384_2step
scripts/segformer_mask_tryon_streaming_full_optimized_nanovsr.py

- NanoVSR 阶段：1.13s
- 端到端：3.07s
完整 3 秒批量命令
set -a && source .env.local && set +a
export PYTHONPATH=/root/autodl-tmp/VTO/scope/src:/root/autodl-tmp/VTO/scope/scripts
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

.venv/bin/python scripts/segformer_mask_tryon_streaming_full_optimized_nanovsr.py \
  --garment-image datasets/garment/upper_body/cloth/01430_00.jpg \
  --random-videos 3 \
  --seed 7 \
  --max-frames 75 \
  --mask-every 1 \
  --mask-batch-size 1 \
  --mask-ema-alpha 0.0 \
  --chunk-size 16 \
  --overlap 2 \
  --profile 448_4step \
  --profile 448_2step \
  --profile 448_1step \
  --profile 384_4step \
  --profile 384_2step \
  --profile 384_1step \
  --nanovsr-chunk-size 5

# shape
使用非方形 profile
 384x512

 线在解码阶段直接做了固定尺寸 resize

 # 问题
 这条流水线怎么处理输入
- 入口脚本是 scripts/segformer_mask_tryon_streaming_full_optimized_nanovsr.py:1
- 输入可以是 --video 指定单个视频，或 --random-videos N 从 datasets/ViT-HD/subset_10pct 随机抽样。
- 每帧先用 OpenCV 解码，然后固定 resize 到 profile 分辨率，比如 384x384 或 448x448。
- 当前 384_2step 配置会把输入视频帧统一 resize 成 384x384，不是保持原始分辨率。
- SegFormer 对 resize 后的帧做人衣/上衣区域分割，生成 mask。
- mask 区域被填成灰色 127，作为 VACE inpaint/try-on 输入。
- LongLive/VACE 按 chunk 处理视频，当前是 chunk_size=16、overlap=2。
- 生成 try-on MP4 后，NanoVSR 再读取这个 MP4 做 4x 超分。
- 384x384 try-on 输出最终变成 1536x1536 NanoVSR 输出。

是否需要 Scope 服务
- 不需要启动 daydream-scope 服务。
- 这是离线 Python 脚本流程，不走 FastAPI、不走 WebRTC、不走前端。
- 它只是复用了 src/scope/core/pipelines/longlive 里的 LongLive/VACE pipeline 代码和本地模型路径。

- SegFormer：做人/服装语义分割，生成 mask。
- LongLive + VACE：根据衣服图、mask、输入视频做 try-on 生成。
- NanoVSR：对 try-on MP4 做 4x 视频超分。
- OpenCV/ffmpeg：负责视频解码、resize、写 MP4、编码。

# 优化

1. 去掉中间 MP4 写入/读取
VACE 输出帧 tensor/array -> 直接送 NanoVSR -> 只写最终超分视频

2. VACE 和 NanoVSR pipeline 并行化
现在基本是一个 job 的 try-on 完成后再跑 NanoVSR。可以改成 producer/consumer：
VACE 产生 chunk N
NanoVSR 同时处理 chunk N-1
编码器同时写 chunk N-2
这样端到端 FPS 会接近慢的那个阶段，而不是两个阶段相加。理论上如果 VACE ~18 FPS、NanoVSR ~20 FPS，流水化后可以接近 15-18 FPS，比现在 9.5 FPS 高很多。


# 服务
给对方的接口
启动服务：
.venv/bin/python scripts/portrait_tryon_stream_service.py --host 0.0.0.0 --port 8012


2. 这个脚本默认没有做时序平滑
在 portrait_nanovsr 里，mask_every=1、mask_ema_alpha=0.0、mask_batch_size=1，也就是：
- 每帧单独做一次 SegFormer
- 不做 EMA 平滑
- 不做跨帧稳定


decode/resize -> SegFormer 分割 -> mask 时间平滑/插值 -> LongLive/VACE try-on -> 写 try-on/mask 视频 -> NanoVSR 4x 超分