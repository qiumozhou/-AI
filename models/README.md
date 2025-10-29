# YOLO模型目录

## 📁 模型文件

将训练好的YOLOv8模型放在这个目录：

```
models/
└── chess_yolo.pt  # 你的YOLO模型文件
```

## 🎯 获取模型的方式

### 方式1：下载预训练模型（推荐）⭐

搜索并下载现成的中国象棋YOLO模型：

**GitHub搜索：**
```
chinese chess yolo
xiangqi yolo
中国象棋 目标检测
```

**Roboflow Universe：**
https://universe.roboflow.com/
搜索：chinese chess

**HuggingFace：**
https://huggingface.co/
搜索：chinese chess detection

### 方式2：自己训练模型

参考 `YOLO训练指南.md` 文件，步骤：

1. 准备数据集（200-1000张图片）
2. 使用LabelImg或Roboflow标注
3. 训练YOLOv8模型
4. 将best.pt重命名为chess_yolo.pt
5. 放入此目录

### 方式3：使用在线标注服务

**Roboflow（推荐）：**
1. 注册 https://roboflow.com/
2. 上传100-200张棋盘图片
3. 在线标注（很方便）
4. 点击"Train Model"
5. 下载训练好的模型

**优点**：
- 免费训练（有限额度）
- 在线标注工具很好用
- 自动数据增强
- 一键导出模型

## 📝 模型规格

**类别（14类）：**
```
红方（大写）：
- R: 车
- N: 马  
- B: 相
- A: 仕
- K: 帅
- C: 炮
- P: 兵

黑方（小写）：
- r: 車
- n: 馬
- b: 象
- a: 士
- k: 将
- c: 炮
- p: 卒
```

**模型要求：**
- 格式：PyTorch (.pt)
- 框架：YOLOv8
- 输入尺寸：640x640（推荐）
- 类别数：14

## 🚀 使用方法

### 1. 安装依赖

```bash
pip install ultralytics
```

### 2. 放置模型

将模型文件重命名为 `chess_yolo.pt` 并放入此目录

### 3. 运行程序

```bash
python chess_gui.py
```

程序会自动检测并使用YOLO模型进行识别！

## ✅ 验证安装

运行测试：

```python
from ultralytics import YOLO

# 加载模型
model = YOLO('models/chess_yolo.pt')

# 测试
print("✓ 模型加载成功！")
print(f"类别数：{len(model.names)}")
print(f"类别：{model.names}")
```

## 🔍 模型性能指标

好的模型应该达到：

- **mAP@0.5**: > 0.90
- **mAP@0.5:0.95**: > 0.70
- **Precision**: > 0.90
- **Recall**: > 0.85

## 📊 推荐的数据集大小

| 场景 | 图片数 | 训练时间 | 预期效果 |
|------|--------|---------|---------|
| 快速测试 | 100-200 | 1-2小时 | 基本可用 |
| 标准应用 | 500-1000 | 3-6小时 | 良好 |
| 生产级别 | 2000+ | 12-24小时 | 优秀 |

## 🎓 学习资源

### 教程
- [YOLOv8官方文档](https://docs.ultralytics.com/)
- [Roboflow教程](https://blog.roboflow.com/)
- B站搜索：YOLOv8目标检测

### 示例项目
- GitHub: yolov8-object-detection
- Google Colab: YOLOv8 training notebook

## 💡 常见问题

### Q: 没有GPU可以训练吗？
A: 可以，但很慢。推荐使用：
- Google Colab（免费GPU）
- Kaggle Notebooks（免费GPU）
- 阿里云/腾讯云GPU服务器

### Q: 需要多少数据？
A: 
- 最少：100张（每类至少20个样本）
- 推荐：500-1000张
- 理想：2000+张

### Q: 训练需要多久？
A: 
- CPU：12-48小时
- GPU（RTX 3060）：2-6小时
- Google Colab：3-8小时

### Q: 模型文件多大？
A: 
- YOLOv8n：6MB
- YOLOv8s：22MB
- YOLOv8m：52MB

## 🔗 有用的链接

- **YOLOv8**: https://github.com/ultralytics/ultralytics
- **Roboflow**: https://roboflow.com/
- **Label Studio**: https://labelstud.io/ （开源标注工具）

---

**如果你找到或训练了好的模型，欢迎分享！** 🎯

