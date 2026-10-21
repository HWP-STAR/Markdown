# 数据集
LUAD-HistoSeg  BCSS

# 研究
病理 WSSS
weakly supervised histopathology image segmentation 
Weakly Supervised Pathological Tissue Segmentation # 小方向
弱监督病理组织分割

 WSSS = Weakly Supervised Semantic Segmentation（弱监督语义分割） # 大方向
更广泛的非 CAM 弱监督方法
# ESFAN
弱监督方法通常用 CAM（类激活图） 从图像级标签生成“伪掩码”当作像素标签。

## 问题 challenge
CAM 伪掩码边界不精确、语义不完整；

伪掩码中的噪声会降低分割训练稳定性与精度。

过程：
# 第一阶段：分类网络生成伪掩码
输入图像级标签，训练分类网络。
在分类网络中引入 ESF：Edge-semantic Synergy Fusion，边缘-语义协同融合。
## 把 CAM 伪标签修得更准、边界更好
最后融合最后三层 CAM，经过 argmax 生成伪掩码。

第二阶段：分割网络抗噪训练
用第一阶段生成的伪掩码训练分割网络。
引入 ANM：Adaptive Noise-aware Mechanism，自适应噪声感知机制，抑制伪掩码噪声，提高分割鲁棒性。
## 在分割训练中过滤噪声标签

整体流程可以记成：

图像级标签 → 分类网络 + ESF → 更好的 CAM → 伪掩码 → 分割网络 + ANM → 最终分割结果。

# 结果
LUAD-HistoSeg：肺腺癌病理图像，四类：TE、NEC、LYM、TAS。
（TE​ = Tumor Epithelial = 肿瘤上皮 / 肿瘤上皮细胞区
TAS​ = Tumor-Associated Stroma = 肿瘤相关间质
LYM​ = Lymphocyte = 淋巴细胞 / 淋巴浸润区
NEC​ = Necrosis = 坏死）

BCSS：乳腺癌病理图像，四类：TUM、STR、LYM、NEC。
TUM​ = Tumor = 肿瘤区
STR​ = Stroma = 间质
LYM​ = Lymphocytic infiltrate = 淋巴样浸润 / 淋巴细胞浸润区
NEC​ = Necrosis = 坏死

# SSHR

单阶段完成弱监督病理分割
# 问题
- 现有病理 WSSS 方法大多是 多阶段流程：

训练分类网络；

用 CAM 生成粗定位；

离线后处理，把 CAM 修成伪掩码；

再用伪掩码训练一个分割网络。

# 方法
病理图像块 → Backbone CNN → 中间特征 + 深层特征 → HFRM（重点，有GSR和CH） 矫正中间特征 → 多尺度 CAM → 分类损失 → 推理时融合 CAM → argmax 得到分割掩码。

GSR 抑制语义不一致的假阳性，CH 消除空间离群点

# CAM 热力图
传统方法是：

先生成 CAM（主要是逐像素处理）→ 发现 CAM 不好 → 离线修 CAM

SSHR 是：

- 在特征层就修 → 再生成 CAM → CAM 已经比较干净
- 最终分割直接来自分类网络的多尺度 CAM

# C²RM-Seg
## 问题
现有 CAM 方法没有显式建模这些混杂因素
如何从因果层面去除混杂因素，生成形态对齐的伪标签，并在分割阶段结合强语义先验和抗噪损失，提高弱监督病理分割的准确性和边界质量。

## 方法
第一阶段：伪掩码生成
用 C²RM 修正 CAM，通过反事实去混杂生成更干净的伪掩码。

第二阶段：分割训练
用 Dual-Path Structural-Semantic Architecture 做分割，并用 UGM 损失抗噪。

### 效果汇总
# LUAD-HistoSeg
方法	阶段/设定	Backbone	mIoU	Dice / mDice	其他指标
ESFAN phase2	两阶段	ResNet200	79.29%	88.41%	—
SSHR	单阶段	ResNet38	77.93%	87.54%	—
C²RM-Seg	两阶段	ResNeSt-200e + 冻结 DINOv3	79.62%	未报	bIoU 49.47，HD95 18.07
数据来源：ESFAN 表 1、SSHR 表 1、C²RM-Seg 表 1。

# BCSS
方法	阶段/设定	Backbone	mIoU	Dice / mDice	其他指标
ESFAN phase2	两阶段	ResNet200	71.41%	83.16%	—
SSHR	单阶段	ResNet38	71.82%	83.52%	—
C²RM-Seg	两阶段	ResNeSt-200e + 冻结 DINOv3	72.17%	未报	bIoU 49.52，HD95 27.31


# HomoSeg
弱监督：只有弱标签
半监督：少量数据有像素级标注，大量数据没有标注

## 问题
WSSS常见问题
像素级标注太贵；

纯弱监督 CAM 有定位偏差、边界差；

半监督分割性能好但通常依赖像素级标注。

## 方法
弱监督和半监督结合
HomoSeg 的定位是：弱标签引导的半监督框架，不是传统 WSSS，也不是需要像素标注的 SSSS。它训练时只用图像级标签，通过数据重构“造”出密集标签，再做半监督一致性训练，最后蒸馏成轻量学生模型。


# 综合
- 分类/伪掩码生成阶段

两篇都使用 ResNet38d 作为分类网络 backbone。

ESFAN 用 ResNet38d 生成 CAM；C²RM-Seg 也用 ResNet38d

