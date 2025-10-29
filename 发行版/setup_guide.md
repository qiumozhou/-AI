# 中国象棋辅助程序 使用指南

## 功能介绍

这个程序可以：
1. 定期截取屏幕上的中国象棋棋局
2. 自动识别棋盘和棋子位置
3. 使用世界顶级的开源中国象棋引擎 **Pikafish** 分析局面
4. 给出最佳应对走法

## 安装步骤

### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 2. 下载Pikafish引擎

Pikafish 是目前最强的开源中国象棋引擎（基于Stockfish改进）

**下载地址**: https://github.com/pikafish-Pikafish/Pikafish/releases

步骤：
1. 访问上述链接
2. 下载最新版本的Windows版本（pikafish-*-win64.zip）
3. 解压后找到 `pikafish.exe`
4. 在项目根目录创建 `engine` 文件夹
5. 将 `pikafish.exe` 复制到 `engine` 文件夹中

目录结构应该是：
```
chess/
├── engine/
│   └── pikafish.exe
├── chess_assistant.py
├── requirements.txt
└── setup_guide.md
```

### 3. （可选）棋子识别模型优化

当前版本使用简化的棋子识别方法。如需更准确的识别，可以：

1. 训练YOLOv8模型识别中国象棋棋子
2. 使用OCR识别棋子上的汉字
3. 使用模板匹配方法

## 使用方法

### 启动程序

```bash
python chess_assistant.py
```

### 快捷键

- **Ctrl + S**: 开始/暂停分析
- **Ctrl + Q**: 退出程序

### 使用流程

1. 运行程序
2. 打开你的中国象棋对弈界面（网页、软件等）
3. 按 `Ctrl + S` 开始分析
4. 程序会自动：
   - 每2秒截图一次
   - 检测棋盘位置
   - 识别棋子
   - 调用Pikafish引擎分析
   - 显示最佳走法

## 配置说明

在 `chess_assistant.py` 中可以调整：

```python
self.screenshot_interval = 2  # 截图间隔（秒）
```

在引擎分析时可以调整搜索深度：
```python
"go depth 15\n"  # 深度越大分析越准确，但耗时越长
```

## 关于Pikafish引擎

Pikafish是基于Stockfish的中国象棋引擎，特点：
- 使用NNUE神经网络评估
- 支持UCI协议
- 等级分超过3500
- 开源免费

## 技术栈

- **截图**: PyAutoGUI
- **图像处理**: OpenCV, Pillow
- **棋子识别**: OpenCV (可扩展深度学习模型)
- **象棋引擎**: Pikafish (UCI协议)
- **热键**: keyboard

## 注意事项

1. **首次使用**: 必须先下载Pikafish引擎
2. **棋子识别**: 当前版本使用简化的识别方法，建议在标准棋盘上使用
3. **性能**: 搜索深度越大，分析越准确但越慢
4. **合法性**: 请仅在个人学习和练习时使用，不要用于线上对弈作弊

## 后续优化方向

1. **改进棋子识别**:
   - 训练YOLOv8目标检测模型
   - 使用深度学习识别棋子类型和颜色
   
2. **智能棋盘检测**:
   - 改进棋盘边缘检测算法
   - 自动校准棋盘坐标系统

3. **界面优化**:
   - 添加GUI界面
   - 实时显示分析结果
   - 可视化最佳走法

4. **多引擎支持**:
   - 支持其他中国象棋引擎
   - 多引擎对比分析

## 故障排除

### 问题1: 找不到引擎
**解决**: 确保 `engine/pikafish.exe` 文件存在且可执行

### 问题2: 识别不到棋盘
**解决**: 
- 确保棋盘在屏幕中央
- 调整棋盘大小
- 检查 `debug_board.png` 查看截图效果

### 问题3: 依赖安装失败
**解决**: 
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 开源协议

本项目仅供学习交流使用。

