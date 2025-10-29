# 贡献指南

感谢你考虑为中国象棋辅助程序做出贡献！

## 如何贡献

### 报告Bug

如果你发现了Bug，请创建一个Issue，包含以下信息：

1. **Bug描述** - 清晰简洁地描述问题
2. **复现步骤** - 详细的复现步骤
3. **期望行为** - 你期望发生什么
4. **实际行为** - 实际发生了什么
5. **环境信息**：
   - 操作系统和版本
   - Python版本
   - 依赖包版本
   - 引擎版本
6. **截图** - 如果适用，添加截图帮助说明问题
7. **日志** - 相关的错误日志

### 建议新功能

如果你有好的想法，请创建一个Feature Request Issue：

1. **功能描述** - 清晰描述建议的功能
2. **使用场景** - 这个功能解决什么问题
3. **实现思路** - 如果有，说明你的实现想法
4. **替代方案** - 是否考虑过其他方案

### 提交代码

#### 开发流程

1. **Fork项目** - 点击Fork按钮复制项目到你的账户
2. **创建分支** - 从main创建功能分支
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **编写代码** - 实现你的功能或修复
4. **遵循规范** - 确保代码符合项目规范
5. **测试代码** - 运行测试确保没有破坏现有功能
   ```bash
   python test_basic.py
   ```
6. **提交更改** - 使用清晰的提交信息
   ```bash
   git commit -m "Add: 添加XXX功能"
   ```
7. **推送分支** - 推送到你的Fork
   ```bash
   git push origin feature/amazing-feature
   ```
8. **创建PR** - 在GitHub上创建Pull Request

#### 代码规范

**Python代码风格**：
- 遵循PEP 8规范
- 使用4个空格缩进
- 函数和变量使用snake_case命名
- 类使用PascalCase命名
- 常量使用UPPER_CASE命名

**文档字符串**：
```python
def function_name(param1, param2):
    """
    函数的简短描述
    
    详细描述（如果需要）
    
    参数:
        param1 (type): 参数1的描述
        param2 (type): 参数2的描述
    
    返回:
        type: 返回值的描述
    """
    pass
```

**注释**：
- 复杂逻辑添加注释说明
- 使用中文或英文注释都可以
- 避免无意义的注释

**提交信息格式**：
```
类型: 简短描述

详细描述（如果需要）

关联Issue: #123
```

类型包括：
- `Add`: 新增功能
- `Fix`: 修复Bug
- `Update`: 更新功能
- `Refactor`: 重构代码
- `Docs`: 文档更新
- `Test`: 测试相关
- `Style`: 代码格式调整

#### 测试

在提交PR前，请确保：

1. 所有现有测试通过
2. 新功能有相应的测试
3. 代码覆盖率不降低

运行测试：
```bash
python test_basic.py
```

### 改进文档

文档改进也是重要的贡献：

- 修正错别字
- 改进说明的清晰度
- 添加使用示例
- 翻译文档

## 开发环境设置

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/chinese-chess-assistant.git
cd chinese-chess-assistant
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置引擎
```bash
python download_engine.py
```

### 5. 运行测试
```bash
python test_basic.py
```

## 项目结构说明

```
chess/
├── chess_assistant.py          # 命令行版主程序
│   └── ChineseChessAssistant类 - 核心功能类
├── chess_gui.py                # GUI版本
│   └── ChessAssistantGUI类 - GUI界面类
├── advanced_chess_recognizer.py # 高级识别
│   └── AdvancedChessRecognizer类 - 图像识别类
├── download_engine.py          # 引擎配置
├── test_basic.py               # 基础测试
└── docs/                       # 文档目录
```

## 优先开发的功能

以下是一些我们希望实现的功能，欢迎认领：

### 高优先级
- [ ] 基于深度学习的棋子识别（YOLOv8）
- [ ] OCR识别棋子上的汉字
- [ ] 更准确的棋盘检测算法
- [ ] 配置文件支持

### 中优先级
- [ ] 多引擎支持
- [ ] 棋局记录和回放
- [ ] 走法可视化
- [ ] 支持更多象棋平台

### 低优先级
- [ ] 英文界面
- [ ] 主题切换
- [ ] 插件系统
- [ ] 移动端支持

## 技术栈和依赖

### 核心依赖
- **Python 3.8+** - 编程语言
- **OpenCV** - 图像处理
- **PyAutoGUI** - 屏幕截图
- **Tkinter** - GUI界面
- **NumPy** - 数值计算

### 可选依赖（用于高级功能）
- **YOLOv8** - 目标检测
- **EasyOCR** - 文字识别
- **PyTorch** - 深度学习框架

## 行为准则

### 我们的承诺

为了营造开放和友好的环境，我们承诺：

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表现出同理心

### 不可接受的行为

- 使用性别化语言或图像
- 骚扰任何形式
- 公开或私下的侮辱
- 未经许可发布他人私人信息
- 其他不道德或不专业的行为

## 获取帮助

如果你在贡献过程中遇到问题：

1. 查看现有的Issues和PR
2. 阅读项目文档
3. 创建新的Issue询问

## 许可

通过贡献，你同意你的贡献将在MIT许可下发布。

## 致谢

感谢所有贡献者的付出！

---

再次感谢你的贡献！🎉

