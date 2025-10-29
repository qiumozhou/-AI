# YOLOv8 中国象棋识别训练指南

## 🎯 概述

使用YOLOv8训练一个中国象棋棋子识别模型，可以达到95%+的识别准确率。

## 📋 准备工作

### 1. 安装依赖

```bash
pip install ultralytics
pip install labelImg  # 标注工具（可选，也可用Roboflow）
```

### 2. 收集数据

#### 方式1：自己拍照/截图
- 收集200-500张中国象棋棋盘图片
- 包含不同角度、光照、棋盘样式
- 建议：开局、中局、残局都要有

#### 方式2：使用现有数据集
- GitHub搜索"chinese chess dataset"
- Roboflow Universe搜索中国象棋数据集
- 推荐：https://universe.roboflow.com/

### 3. 标注数据

#### 使用LabelImg（本地）

```bash
labelImg
```

标注格式：YOLO格式
- 每张图片一个.txt文件
- 格式：`class_id center_x center_y width height`（归一化坐标）

#### 使用Roboflow（在线，推荐）

1. 注册：https://roboflow.com/
2. 创建项目：Chinese Chess Detection
3. 上传图片
4. 在线标注（更方便）
5. 自动生成训练数据

**类别定义（14类）：**
```
0: red_rook      (红车)
1: red_knight    (红马)
2: red_bishop    (红相)
3: red_advisor   (红仕)
4: red_king      (红帅)
5: red_cannon    (红炮)
6: red_pawn      (红兵)
7: black_rook    (黑车)
8: black_knight  (黑马)
9: black_bishop  (黑象)
10: black_advisor (黑士)
11: black_king   (黑将)
12: black_cannon (黑炮)
13: black_pawn   (黑卒)
```

## 🏋️ 训练模型

### 准备数据配置文件

创建 `chess_data.yaml`:

```yaml
# 数据路径
path: ./chess_dataset  # 数据集根目录
train: images/train    # 训练图片
val: images/val        # 验证图片

# 类别
nc: 14  # 类别数量
names: ['red_rook', 'red_knight', 'red_bishop', 'red_advisor', 'red_king',
        'red_cannon', 'red_pawn',
        'black_rook', 'black_knight', 'black_bishop', 'black_advisor', 'black_king',
        'black_cannon', 'black_pawn']
```

### 数据集目录结构

```
chess_dataset/
├── images/
│   ├── train/
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   └── val/
│       ├── img101.jpg
│       └── ...
├── labels/
│   ├── train/
│   │   ├── img001.txt
│   │   ├── img002.txt
│   │   └── ...
│   └── val/
│       ├── img101.txt
│       └── ...
└── chess_data.yaml
```

### 训练脚本

创建 `train_yolo.py`:

```python
from ultralytics import YOLO

# 加载预训练模型
model = YOLO('yolov8n.pt')  # nano模型，速度快
# 或使用: yolov8s.pt (small), yolov8m.pt (medium), yolov8l.pt (large)

# 训练参数
results = model.train(
    data='chess_data.yaml',     # 数据配置文件
    epochs=100,                  # 训练轮数
    imgsz=640,                   # 图像大小
    batch=16,                    # 批次大小（根据显存调整）
    device=0,                    # GPU设备（0=第一块GPU，cpu=使用CPU）
    project='chess_training',    # 项目名称
    name='exp1',                 # 实验名称
    patience=20,                 # 早停耐心值
    save=True,                   # 保存模型
    plots=True,                  # 生成训练图表
    
    # 数据增强
    hsv_h=0.015,                 # 色调增强
    hsv_s=0.7,                   # 饱和度增强
    hsv_v=0.4,                   # 亮度增强
    degrees=10,                  # 旋转角度
    translate=0.1,               # 平移
    scale=0.5,                   # 缩放
    flipud=0.5,                  # 上下翻转概率
    fliplr=0.5,                  # 左右翻转概率
    mosaic=1.0,                  # Mosaic增强
)

print("训练完成！")
print(f"最佳模型: chess_training/exp1/weights/best.pt")
```

运行训练：

```bash
python train_yolo.py
```

### 训练技巧

1. **数据量建议**
   - 最少：200张图片
   - 推荐：500-1000张
   - 理想：2000+张

2. **硬件要求**
   - GPU：推荐（NVIDIA，4GB显存以上）
   - CPU：可以但很慢
   - 内存：8GB以上

3. **超参数调整**
   - `epochs`：100-300，根据数据量
   - `batch`：16（4GB显存），32（8GB），64（12GB+）
   - `imgsz`：640（标准），1280（高精度）

4. **模型选择**
   - `yolov8n.pt`：最快，适合实时（推荐）
   - `yolov8s.pt`：平衡
   - `yolov8m.pt`：更准确但慢
   - `yolov8l.pt`：最准确但最慢

## 🔍 测试模型

创建 `test_yolo.py`:

```python
from ultralytics import YOLO
import cv2

# 加载训练好的模型
model = YOLO('chess_training/exp1/weights/best.pt')

# 测试单张图片
results = model('test_image.jpg', conf=0.5)

# 显示结果
for result in results:
    result.show()  # 显示检测框
    result.save(filename='result.jpg')  # 保存结果
    
    # 打印检测到的棋子
    boxes = result.boxes
    for box in boxes:
        cls = int(box.cls[0])
        conf = box.conf[0]
        print(f"检测到: {model.names[cls]}, 置信度: {conf:.2f}")
```

## 📦 使用训练好的模型

### 方式1：下载预训练模型（推荐）

如果有现成的模型，直接使用：

```bash
# 创建models目录
mkdir models

# 下载或复制模型文件
# 将 best.pt 放入 models/chess_yolo.pt
```

### 方式2：使用我们的程序

模型文件放置位置：
```
chess/
└── models/
    └── chess_yolo.pt  # 你训练的或下载的模型
```

程序会自动检测并使用YOLO模型！

## 🎯 提高识别率的技巧

### 数据质量
1. **多样性**
   - 不同棋盘样式（木质、塑料、电子）
   - 不同光照条件
   - 不同角度（俯视最好）
   - 不同局面（开局、中局、残局）

2. **标注质量**
   - 标注框紧贴棋子
   - 不要遗漏棋子
   - 分类要准确

3. **数据增强**
   - 自动旋转、翻转
   - 亮度、对比度调整
   - Mosaic拼接

### 训练优化
1. **分阶段训练**
   ```python
   # 第一阶段：快速收敛
   model.train(epochs=50, lr0=0.01)
   
   # 第二阶段：精细调优
   model.train(epochs=50, lr0=0.001, resume=True)
   ```

2. **使用预训练权重**
   - 从COCO预训练的YOLOv8开始
   - 迁移学习更快收敛

3. **验证集监控**
   - 观察mAP50、mAP50-95指标
   - 防止过拟合

## 📊 评估指标

- **mAP@0.5**: 主要指标，目标>0.9
- **mAP@0.5:0.95**: 综合指标，目标>0.7
- **Precision**: 精确率，目标>0.9
- **Recall**: 召回率，目标>0.9

## 🔗 资源链接

### 官方文档
- YOLOv8: https://docs.ultralytics.com/
- Roboflow: https://docs.roboflow.com/

### 数据集
- Roboflow Universe: https://universe.roboflow.com/
- Kaggle: 搜索"chinese chess"

### 预训练模型
- 如果你找到现成的中国象棋YOLO模型，可以直接使用
- GitHub搜索：yolo chinese chess

## ⚡ 快速开始（使用现成模型）

如果你不想自己训练，可以：

1. 从GitHub/Roboflow下载预训练模型
2. 将模型放入 `models/chess_yolo.pt`
3. 安装ultralytics：`pip install ultralytics`
4. 运行程序，自动使用YOLO识别！

## 💡 提示

- 训练需要时间（几小时到一天）
- 建议在Google Colab免费GPU上训练
- 数据质量>数据数量
- 持续迭代改进模型

---

**祝训练成功！🎯**

