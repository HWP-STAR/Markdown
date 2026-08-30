import numpy as np
import torch
print("ok")

print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 是否可用: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA 版本: {torch.version.cuda}")
    print(f"GPU 数量: {torch.cuda.device_count()}")
    print(f"当前 GPU: {torch.cuda.get_device_name(0)}")
    # 执行一个简单的GPU张量运算
    x = torch.randn(1000, 1000).to('cuda')
    y = torch.randn(1000, 1000).to('cuda')
    z = torch.mm(x, y)
    print("GPU 张量运算成功！")
else:
    print("GPU 不可用，请检查安装。")
