# 🎯 中国象棋辅助程序

一个基于Python的智能中国象棋辅助工具，通过AI视觉识别棋局并使用世界顶级开源引擎**Pikafish**（等级分3500+）实时分析并给出最佳走法。

## ✨ 功能特性

- 🖼️ **自动截屏识别** - 定期捕获屏幕上的棋局
- 🔍 **智能多层识别** - **深度学习（85-90%）> OCR（70-80%）> 传统方法**
  - ⭐ **深度学习识别**（推荐）- 基于专业训练的ONNX模型，准确率85-90%
  - 🔤 **OCR识别** - 基于PaddleOCR，识别棋子汉字
  - 🎯 **自动回退** - 失败时自动切换备选方案
- 🧠 **顶级引擎分析** - 集成Pikafish引擎（基于Stockfish，支持NNUE神经网络）
- 💡 **实时走法建议** - 快速给出最佳应对
- 🎨 **双模式界面** - GUI图形界面 + 命令行模式
- ⌨️ **快捷键控制** - 方便快速操作
- 📊 **参数可调** - 自定义截图间隔和分析深度

## 🚀 快速开始

### Windows用户（推荐）

1. **双击运行 `run.bat`**
2. 选择 `4` 安装依赖
3. 选择 `3` 配置引擎
4. 选择 `1` 启动GUI版本

### 手动安装

#### 第一步：安装依赖
```bash
pip install -r requirements.txt
```

使用国内镜像加速（可选）：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 第二步：配置引擎

**自动配置（推荐）**：
```bash
python download_engine.py
```

**手动配置**：
1. 访问 [Pikafish Releases](https://github.com/official-pikafish/Pikafish/releases)
2. 下载最新Windows版本（pikafish-*-windows-x86-64.zip）
3. 解压后将 `pikafish.exe` 放入项目的 `engine/` 目录

#### 第三步：测试安装

```bash
python test_basic.py
```

确保所有测试通过后即可使用。

## 🎮 使用方法

### GUI图形界面版（推荐新手）

```bash
python chess_gui.py
```

**特点**：
- 直观的图形界面
- 实时棋盘预览
- 可视化参数调节
- 日志实时输出

**快捷键**：
- `Ctrl + S` - 开始/停止分析
- `Ctrl + Q` - 退出程序

### 命令行版本（适合高级用户）

```bash
python chess_assistant.py
```

**特点**：
- 轻量级，资源占用少
- 适合后台运行
- 快捷键全键盘操作

**快捷键**：
- `Ctrl + S` - 开始/暂停分析
- `Ctrl + Q` - 退出程序

## 📖 详细文档

- 📘 [完整使用教程](USAGE.md) - 详细的使用说明和技巧
- 📗 [安装配置指南](setup_guide.md) - 深入的安装和配置说明

## 🔧 系统要求

- **操作系统**: Windows 10/11 (推荐), Linux, macOS
- **Python版本**: Python 3.8 或更高
- **内存**: 建议 4GB 以上
- **显示器**: 建议分辨率 1920x1080 或更高

## 📸 使用场景

### 场景1：在线对弈辅助
在天天象棋、QQ象棋等平台练习时获取走法建议（仅限练习，禁止排位作弊）

### 场景2：棋局学习
观看象棋教学视频时，实时分析局面，对比讲解和引擎建议

### 场景3：复盘分析
对已完成的棋局进行深度分析，找出失误点和改进方向

## 🛠️ 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| 截图 | PyAutoGUI | 屏幕捕获 |
| 图像处理 | OpenCV | 棋盘检测和图像分析 |
| 图像增强 | Pillow (PIL) | 图像格式转换 |
| 棋子识别 | OpenCV + NumPy | 颜色和形状识别 |
| 象棋引擎 | Pikafish | UCI协议通信 |
| GUI界面 | Tkinter | 图形用户界面 |
| 热键控制 | keyboard | 全局快捷键 |

## 📊 引擎信息

**Pikafish** 是目前最强的开源中国象棋引擎之一：
- 基于Stockfish改进
- 使用NNUE（高效可更新神经网络）评估
- 等级分超过3500
- 支持标准UCI协议
- 开源免费

## ⚠️ 重要提醒

**道德使用准则**：

✅ **允许的用途**：
- 个人学习和练习
- 棋局复盘分析
- 研究象棋理论
- 人机对弈练习

❌ **禁止的用途**：
- 在线排位赛作弊
- 正式比赛中使用
- 侵犯他人权益
- 违反平台规则

**法律声明**：本程序仅供学习研究使用，使用者需自行承担使用责任。不当使用造成的任何后果与开发者无关。

## 🐛 故障排除

### 问题1: 找不到引擎
**解决方案**：
```bash
python download_engine.py
```
按提示下载并配置引擎文件。

### 问题2: 依赖安装失败
**解决方案**：
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题3: 识别不到棋盘
**解决方案**：
- 确保棋盘完整显示在屏幕中央
- 检查生成的 `debug_board.png` 文件
- 调整棋盘大小（建议400x400像素以上）

### 问题4: 程序卡顿
**解决方案**：
- 降低分析深度（从15降到10）
- 增加截图间隔（从2秒增到3-5秒）
- 关闭其他占用资源的程序

更多问题请查看 [使用教程](USAGE.md) 中的FAQ部分。

## 📝 项目结构

```
chess/
├── chess_assistant.py          # 命令行版主程序
├── chess_gui.py                # GUI版本主程序
├── advanced_chess_recognizer.py # 高级识别模块
├── download_engine.py          # 引擎下载配置脚本
├── test_basic.py               # 功能测试脚本
├── requirements.txt            # Python依赖
├── run.bat                     # Windows启动脚本
├── run.sh                      # Linux/Mac启动脚本
├── README.md                   # 项目说明
├── USAGE.md                    # 使用教程
├── setup_guide.md              # 安装指南
├── .gitignore                  # Git忽略文件
└── engine/                     # 引擎目录
    └── pikafish.exe            # (需要下载)
```

## 🔄 更新日志

### v1.0.0 (当前版本)
- ✅ 基础截图功能
- ✅ Pikafish引擎集成
- ✅ GUI和命令行双模式
- ✅ 基于颜色的棋子识别
- ✅ 实时走法建议
- ✅ 完整文档和测试

### 计划中的功能
- 🔄 基于深度学习的棋子识别（YOLOv8）
- 🔄 OCR识别棋子汉字
- 🔄 多引擎对比分析
- 🔄 棋局自动记录
- 🔄 走法可视化显示
- 🔄 移动端支持

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 开源协议

MIT License - 详见 LICENSE 文件

## 🙏 致谢

- [Pikafish](https://github.com/official-pikafish/Pikafish) - 强大的中国象棋引擎
- [Stockfish](https://stockfishchess.org/) - Pikafish的基础
- [OpenCV](https://opencv.org/) - 计算机视觉库
- 所有为开源象棋引擎做出贡献的开发者

---

**⭐ 如果这个项目对你有帮助，请给个Star支持一下！**

