# 可穿戴六轴 IMU 
IMU（Inertial Measurement Unit，惯性测量单元）​ 是一种通过惯性原理测量物体运动状态的传感器模组。六轴 IMU​ 内部集成了两类传感器，共六个测量轴：
三轴加速度计（3-axis Accelerometer）：分别沿 X、Y、Z 三个正交轴，测量线性加速度（包括重力加速度），可感知设备的倾斜、震动、冲击和直线运动。
三轴陀螺仪（3-axis Gyroscope）：同样沿 X、Y、Z 三轴，测量角速度（物体绕各轴的旋转速率），可感知设备的旋转、翻转、偏航等姿态变化。

# 作用
实时感知设备在三维空间中的运动与姿态

# RSRW 是一种在训练时给每个样本分配权重的策略，
权重由“类别稀有度、鲁棒难度、真实/合成可靠性”三部分决定；所有计算都用 detached logits 和小批量统计，只做一阶、stop-gradient 加权，不传二阶梯度。

# WGAN（Wasserstein GAN）
改进的GAN方法，用来生成数据
用 Wasserstein 距离（推土机距离，Earth Mover's Distance）替代 JS 散度，来衡量真实分布与生成分布之间的差距