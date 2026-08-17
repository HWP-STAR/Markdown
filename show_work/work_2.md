# 为什么现在慢
现在的 try-on pipeline 慢在几层：
1. LongLive/VACE 每个 chunk 都要跑生成模型
即使是 few-step，它仍然是视频扩散/视频生成模型，不是普通 CNN 前向。
2. SegFormer mask 仍然有开销
如果每帧都跑人体解析，实时成本会很高。segformer-tryon-fast 已经用 mask_stride=2 降低了这部分，但还不够。
3. chunk 太短会低效，chunk 太长会延迟高
现在 8 帧 chunk 是折中。短了不稳定，长了延迟高。
4. 每个 chunk 可能重复做参考图/文本/条件处理
garment/person reference embedding 如果不缓存，会浪费很多时间。
5. VACE 不是专门的 try-on 实时模型
它是通用视频编辑能力，能做 try-on，但不是为衣服替换这个单任务极限优化过的。

# 1 . SegFormer 降频 + mask 传播
当前 fast 是 mask_stride=2。可以进一步：
参数	当前	可尝试
mask_stride	2	3-5
mask 更新	插值	光流/跟踪传播
SegFormer 分辨率	368x640 或 512x512	256x448 mask 内部推理，再上采样
做法：
第 0 帧跑 SegFormer
第 1-4 帧用 optical flow / tracker 传播 mask
第 5 帧再跑 SegFormer 校正

# 2 . 参考图 embedding 缓存
目前参考图每次作为 vace_ref_images 传入时，可能会重复走图像编码逻辑。
应该做成：
用户上传参考图
-> 预编码成 reference embedding / latent
-> 后续 chunk 只传 embedding
# 3 文本编码缓存
prompt 不变时，T5/UMT5 embedding 不应该每个 chunk 重算。
做法：
prompt -> text embedding -> cache by prompt hash

# 4. 固定 shape + torch.compile / CUDA graph
现在已经固定了输入尺寸。下一步是：
- 固定 height/width
- 固定 chunk_frames
- 固定 denoising step list
- 预热模型
- 捕获 CUDA graph 或 torch.compile
# 5. 降低输出分辨率
如果目标是实时预览，可以先做：
模式	分辨率
preview	256x448 / 288x512
balanced	368x640
quality	512x512 / 480x864

###
# 1. 异步流水线
现在很多流程是串行：
读取帧 -> SegFormer -> VACE -> 输出
应该改成三段异步：
线程/GPU stream A: 接收帧 + resize
线程/GPU stream B: mask / tracking
线程/GPU stream C: VACE generation
线程 D: encode / output
队列设计：
FrameQueue -> MaskQueue -> GenerateQueue -> OutputQueue

# 2. 滑窗复用 latent / KV cache
现在每个 chunk 都像重新生成一段视频。更好的做法：
上一 chunk 的 latent / hidden state / KV cache
-> 作为下一 chunk 的 warm state
这样可以减少重复计算和时序抖动。

# 3. mask 不再输入全帧
如果只是换衣服，没必要让模型处理整帧生成。
可以做局部 crop：
检测 torso bbox
-> 扩大 bbox
-> 只对 bbox 区域做 VACE
-> paste 回原图

# 4. 两阶段输出
实时先输出低质量帧：
fast low-res tryon -> 立即显示
background enhance / refine -> 延迟替换
效果：
- 用户看到 15-20 fps 预览
- 后台可以生成更高质量版本
- 体验上更像实时

####

# 1. 训练 1-4 step try-on student
当前 LongLive/VACE 虽然比 MagicTryOn 快很多，但仍然是通用视频生成模型。
真正实时需要训练专用模型：
Teacher:
MagicTryOn / CatV2TON / LongLive high-quality offline outputs

Student:
small causal try-on video model
训练目标：
- 输入：视频短窗口 + mask + garment/person ref embedding
- 输出：换衣后视频短窗口
- denoise steps：1-4
- 支持 streaming state
可用方法：
- DMD distillation
- consistency distillation
- rectified flow distillation
- adversarial video distillation
- latent consistency model

# 2. 从通用 VACE 改成专用 try-on generator
VACE 是通用视频编辑。实时试衣应该用专用结构：
Garment Encoder
Human Parser Encoder
Pose/Motion Encoder
Causal Video Generator
Temporal Memory
输入：
current frames
previous generated frames
mask
pose / dense flow
garment embedding
输出：
new try-on frames
这样模型不用每次“理解所有任务”，只做衣服替换

# 3. 服装 texture warping + 小模型修复
大胆一点，可以不用扩散模型做所有工作。
流程：
人体解析 + DensePose/SMPL
-> 估计衣服区域 UV / flow
-> 把服装图 texture warp 到身体
-> 小模型修复边缘、褶皱、光照
这会比扩散快很多。

