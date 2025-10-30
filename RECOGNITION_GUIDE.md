# 象棋识别方案对比

本项目提供两种棋盘识别方案，您可以根据需求选择：

## 方案对比

| 特性 | 方案1: OCR识别 | 方案2: 深度学习识别 |
|------|---------------|------------------|
| **准确率** | 中等 (~70-80%) | 高 (83%-90%) |
| **速度** | 慢 (30-60秒首次加载) | 快 (模型加载后< 5秒) |
| **依赖** | PaddleOCR | ONNX Runtime + 专用模型 |
| **优点** | 已集成，开箱即用 | 专门训练，准确率高 |
| **缺点** | 速度慢，准确率一般 | 需要下载模型和额外配置 |
| **状态** | ✅ 已完成 | 🚧 需要集成 |

---

## 方案1: OCR识别（当前可用）

### 使用方法

```bash
# 直接运行测试
python test_recognize.py

# 或运行快速测试（只识别3个棋子）
python quick_test_ocr.py
```

### 特点
- ✅ 已集成到项目中
- ✅ 可以直接使用
- ✅ 基于PaddleOCR，通用OCR引擎
- ⚠️ 首次加载需要30-60秒
- ⚠️ 每个棋子识别需要~1秒

### 识别流程
1. 霍夫圆检测 → 找到32个棋子位置
2. OCR识别 → 识别每个棋子上的汉字
3. 颜色检测 → 区分红黑双方
4. 生成FEN → 输出标准棋盘表示

---

## 方案2: 深度学习识别（推荐，需配置）

### 项目来源
- GitHub: https://github.com/TheOne1006/chinese-chess-recognition
- HuggingFace Demo: https://huggingface.co/spaces/yolo12138/Chinese_Chess_Recognition

### 优势
- 🎯 专门为象棋训练的模型
- 🎯 高准确率：83%完全正确，90%允许1个错误
- 🎯 快速：加载后识别只需几秒
- 🎯 鲁棒性强：处理倾斜、复杂背景等场景

### 安装步骤

#### 步骤 1: 安装依赖

```bash
# 激活虚拟环境
.venv\Scripts\activate

# 安装ONNX Runtime
pip install onnxruntime opencv-python numpy

# 或者如果有GPU
pip install onnxruntime-gpu opencv-python numpy
```

#### 步骤 2: 下载模型文件

有两种方式：

**方式A: 手动下载（推荐）**

访问 HuggingFace Space 的文件页面：
https://huggingface.co/spaces/yolo12138/Chinese_Chess_Recognition/tree/main

下载以下两个文件到 `d:\chess\models\cchess_recognition\` 目录：
1. `rtmpose-t-cchess_4.onnx` （棋盘关键点检测模型，~5MB）
2. `swinv2-nano_cchess16.onnx` （棋子分类模型，~10MB）

**方式B: 使用项目完整环境**

```bash
cd chess_recognition_model
pip install -e .
pip install mmengine mmcv mmpretrain mmpose
```

然后使用项目自带的推理工具。

#### 步骤 3: 测试识别

```bash
# 测试ONNX模型是否加载成功
python cchess_deep_recognizer.py

# 如果使用完整环境
cd chess_recognition_model/cchess_reg
python examples/inference_demo.py ../../images/1.png --device cpu
```

### 技术原理

**两步识别流程：**

```
输入图像
    ↓
[步骤1: 棋盘关键点检测]
    → 检测棋盘4个角点 (RTMPose模型)
    ↓
[步骤2: 透视变换]
    → 将棋盘对齐为俯视图
    ↓
[步骤3: 多区域分类]
    → 10x9x16分类 (Swin Transformer2)
    → 每个位置16类：红7+黑7+空位+其他
    ↓
输出FEN
```

---

## 当前状态

### ✅ 已完成
1. OCR识别方案已集成并可用
2. 深度学习项目已克隆到本地
3. 创建了集成框架代码

### 🚧 待完成
1. 下载ONNX模型文件
2. 实现ONNX推理接口
3. 集成到主程序

---

## 快速开始指南

### 现在就想用？→ 使用方案1

```bash
# 等待30-60秒模型加载后即可识别
python test_recognize.py
```

### 想要更高准确率？→ 配置方案2

```bash
# 1. 手动下载模型（见上文）
# 2. 运行测试
python cchess_deep_recognizer.py
```

---

## 常见问题

### Q: 为什么OCR方案这么慢？
A: PaddleOCR是通用OCR引擎，需要加载多个模型。每次OCR调用都要运行完整的文本检测+识别流程。

### Q: 深度学习方案为什么更快？
A: 专门训练的模型直接输出10x9x16的分类结果，一次推理完成全部识别。

### Q: 哪个方案更准确？
A: 深度学习方案准确率更高（83%-90% vs 70-80%），因为它是专门为象棋训练的。

### Q: 可以同时用两个方案吗？
A: 可以！可以用深度学习方案做主要识别，OCR方案做备选。

---

## 下一步建议

1. **短期**: 使用OCR方案完成基本功能测试
2. **中期**: 配置深度学习方案，提高识别准确率
3. **长期**: 如果需要更高准确率，可以：
   - 收集更多训练数据
   - 微调现有模型
   - 或训练YOLO模型

---

## 参考资料

- 原项目: https://github.com/TheOne1006/chinese-chess-recognition
- HuggingFace Demo: https://huggingface.co/spaces/yolo12138/Chinese_Chess_Recognition
- PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR
- MMPose: https://github.com/open-mmlab/mmpose

