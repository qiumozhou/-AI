# 中国象棋辅助程序

使用深度学习技术识别中国象棋棋局并提供最佳走法建议的智能辅助工具。

## ✨ 特性

- 🧠 **深度学习识别** - 使用ONNX模型进行高精度棋盘和棋子识别（准确率85-90%）
- 🚀 **实时分析** - 集成Pikafish引擎提供最佳走法建议
- 🖥️ **智能GUI界面** - 直观易用的图形界面，支持拖拽图片识别
- 📸 **自动截图** - 可设置间隔（1-10秒）自动截取屏幕并识别
- ⚙️ **引擎深度调节** - 支持1-15级搜索深度设置，平衡速度与准确性
- 🔄 **自动分析** - 识别成功后可自动进行引擎分析
- 🎯 **多种模式** - 支持图形界面、命令行和实时截屏三种使用方式
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

### 🖥️ 图形界面（推荐）
```bash
python chess_gui.py
```
或直接双击 `run.bat` 启动

**GUI功能:**
- **图片识别**: 点击"选择图片"选择棋盘图片，点击"开始识别"进行智能识别
- **自动截图**: 设置截图间隔（1-10秒），点击"开始自动截图"进入自动模式
- **引擎设置**: 调节搜索深度（1-15级），开启/关闭自动分析
- **结果显示**: 自动显示棋盘状态、FEN格式和最佳走法
- **实时日志**: 显示详细的处理过程和时间戳

### 📝 命令行模式

**识别图片中的棋局**
```bash
python recognize_board.py images/1.png
```

**识别并获得走法建议**
```bash
python recognize_board.py images/1.png --analyze
```

**实时截屏辅助**
```bash
python chess_assistant.py
# 按 Ctrl+S 开始/暂停分析
# 按 Ctrl+Q 退出程序
```

## 📁 项目结构

```
chess/
├── chess_gui.py                # 图形界面程序（推荐）
├── chess_assistant.py          # 实时截屏辅助
├── recognize_board.py          # 命令行识别程序
├── cchess_deep_recognizer.py   # 深度学习识别核心
├── download_nnue.py           # 模型下载工具
├── requirements.txt           # 依赖列表
├── run.bat                   # 一键启动脚本
├── engine/                   # Pikafish引擎
│   ├── pikafish.exe
│   └── pikafish.nnue
├── models/                   # ONNX模型文件
│   └── cchess_recognition/
└── images/                   # 测试图片
```

## 🎮 使用方法

### 图形界面模式（推荐）

**基础识别流程：**
1. **启动程序** - 双击 `run.bat` 或运行 `python chess_gui.py`
2. **选择图片** - 点击"选择图片"按钮，选择清晰的棋盘图片
3. **开始识别** - 点击"开始识别"按钮，程序自动识别棋盘和棋子
4. **查看结果** - 在界面中查看棋盘状态和FEN格式
5. **引擎分析** - 点击"手动分析"获得最佳走法建议

**自动截图模式：**
1. **设置参数** - 调整截图间隔（1-10秒）和引擎深度（1-15级）
2. **开启自动分析** - 勾选"自动分析"选项
3. **开始自动截图** - 点击"开始自动截图"按钮
4. **实时监控** - 程序将自动截图、识别并分析，结果实时显示
5. **停止监控** - 点击"停止自动截图"结束自动模式

### 命令行模式
1. **图片识别** - `python recognize_board.py images/1.png`
2. **带分析** - `python recognize_board.py images/1.png --analyze`
3. **实时辅助** - `python chess_assistant.py`（按Ctrl+S开始/暂停）

## 🔧 技术架构

- **棋盘检测**: RTMPose模型进行关键点检测和透视变换
- **棋子识别**: SwinV2模型进行棋子分类
- **引擎分析**: Pikafish引擎提供走法建议
- **图像处理**: OpenCV进行图像预处理和后处理

## 💡 使用技巧

### 自动截图模式优化
- **间隔设置**: 根据对局节奏调整截图间隔，快棋建议1-2秒，慢棋可设置5-10秒
- **引擎深度**: 
  - 快速分析：深度4-6（1-2秒出结果）
  - 平衡模式：深度8-10（3-5秒出结果）
  - 精确分析：深度12-15（10-30秒出结果）
- **屏幕准备**: 确保棋盘完整显示在屏幕上，避免被其他窗口遮挡

### 识别准确性提升
- 选择光线充足、对比度高的棋盘图片
- 确保棋盘边界清晰，棋子摆放规整
- 避免反光、阴影等影响识别的因素

## ⚠️ 注意事项

- 确保图片中棋盘清晰可见，光线充足
- 首次运行需要下载约40MB的ONNX模型文件  
- 需要Windows系统（包含Pikafish引擎）
- 推荐Python 3.8+
- 自动截图需要屏幕访问权限

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Pikafish](https://github.com/official-pikafish/Pikafish) - 强大的中国象棋引擎
- [chinese-chess-recognition](https://github.com/TheOne1006/chinese-chess-recognition) - 深度学习识别方案
- OpenMMLab 生态系统 - 提供优秀的深度学习框架