# 中国象棋辅助程序

使用深度学习技术识别中国象棋棋局并提供最佳走法建议的智能辅助工具。

## ✨ 特性

- 🧠 **深度学习识别** - 使用ONNX模型进行高精度棋盘和棋子识别（准确率85-90%）
- 🚀 **实时分析** - 集成Pikafish引擎提供最佳走法建议
- 🎯 **简单易用** - 命令行界面，支持图片识别和实时截屏
- ⚡ **高性能** - 优化的识别流程，快速响应

## 📦 安装

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd chess
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **下载模型和引擎**
   ```bash
   python download_nnue.py
   ```

## 🚀 快速开始

### 识别图片中的棋局
```bash
python recognize_board.py images/1.png
```

### 识别并获得走法建议
```bash
python recognize_board.py images/1.png --analyze
```

### 实时截屏辅助
```bash
python chess_assistant.py
# 按 Ctrl+S 开始/暂停分析
# 按 Ctrl+Q 退出程序
```

或者双击 `run.bat` 直接运行

## 📁 项目结构

```
chess/
├── chess_assistant.py          # 主程序（实时截屏辅助）
├── recognize_board.py          # 图片识别程序
├── cchess_deep_recognizer.py   # 深度学习识别核心
├── download_nnue.py           # 模型下载工具
├── requirements.txt           # 依赖列表
├── run.bat                   # Windows启动脚本
├── engine/                   # Pikafish引擎
│   ├── pikafish.exe
│   └── pikafish.nnue
├── models/                   # ONNX模型文件
│   └── cchess_recognition/
└── images/                   # 测试图片
```

## 🎮 使用方法

1. **准备棋局图片** - 确保图片清晰，棋盘完整可见
2. **运行识别** - 使用 `recognize_board.py` 识别棋局
3. **获得建议** - 添加 `--analyze` 参数获得最佳走法
4. **实时辅助** - 运行 `chess_assistant.py` 进行实时截屏分析

## 🔧 技术架构

- **棋盘检测**: RTMPose模型进行关键点检测和透视变换
- **棋子识别**: SwinV2模型进行棋子分类
- **引擎分析**: Pikafish引擎提供走法建议
- **图像处理**: OpenCV进行图像预处理和后处理

## ⚠️ 注意事项

- 确保图片中棋盘清晰可见，光线充足
- 首次运行需要下载约40MB的ONNX模型文件
- 需要Windows系统（包含Pikafish引擎）
- 推荐Python 3.8+

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Pikafish](https://github.com/official-pikafish/Pikafish) - 强大的中国象棋引擎
- [chinese-chess-recognition](https://github.com/TheOne1006/chinese-chess-recognition) - 深度学习识别方案
- OpenMMLab 生态系统 - 提供优秀的深度学习框架