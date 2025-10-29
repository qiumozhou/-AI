# 🎯 从这里开始

欢迎使用中国象棋辅助程序！这是你开始使用的第一步。

## 📋 开始前的检查清单

- [ ] Python 3.8 或更高版本已安装
- [ ] 有稳定的网络连接（用于下载依赖和引擎）
- [ ] 约500MB的磁盘空间
- [ ] Windows 10/11 操作系统（推荐）

## 🚀 三步快速开始

### 方法一：使用启动脚本（最简单）⭐

**Windows用户：**
1. 双击 `run.bat`
2. 选择 `4` - 安装依赖
3. 选择 `3` - 配置引擎
4. 选择 `1` - 启动程序

**就这么简单！**

### 方法二：使用快速启动程序

```bash
python quickstart.py
```

按照提示操作即可。程序会自动检查环境、安装依赖、配置引擎。

### 方法三：手动安装（完全掌控）

#### 步骤 1: 安装依赖包

打开命令行，执行：
```bash
pip install -r requirements.txt
```

如果下载慢，使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 步骤 2: 配置象棋引擎

运行配置脚本：
```bash
python download_engine.py
```

按照提示下载Pikafish引擎并放置到 `engine/` 目录。

或者手动下载：
1. 访问：https://github.com/official-pikafish/Pikafish/releases
2. 下载最新Windows版本
3. 解压后将 `pikafish.exe` 放入 `engine/` 目录

#### 步骤 3: 测试安装

```bash
python test_basic.py
```

确保所有测试通过。

#### 步骤 4: 启动程序

**GUI版本（推荐）：**
```bash
python chess_gui.py
```

**命令行版本：**
```bash
python chess_assistant.py
```

## 🎮 第一次使用

### 启动后的操作

1. **打开象棋对弈界面**
   - 可以是网页版象棋（天天象棋、QQ象棋等）
   - 也可以是桌面象棋软件
   - 确保棋盘清晰可见

2. **开始分析**
   - GUI版本：点击"开始分析"按钮
   - 命令行版本：按 `Ctrl + S`

3. **查看建议**
   - 程序会自动识别棋局
   - 显示最佳走法建议
   - 根据建议落子

4. **停止分析**
   - GUI版本：点击"停止分析"按钮
   - 命令行版本：再次按 `Ctrl + S`

### 快捷键参考

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + S` | 开始/停止分析 |
| `Ctrl + Q` | 退出程序 |

## ⚙️ 调整设置

### GUI版本

在界面上可以直接调整：
- **截图间隔**：建议2-3秒
- **分析深度**：建议15（深度越大越准确但越慢）

### 命令行版本

编辑 `chess_assistant.py`，修改这些参数：
```python
self.screenshot_interval = 2  # 截图间隔（秒）
```

在 `analyze_position` 方法中修改：
```python
"go depth 15\n"  # 分析深度
```

## 📚 进一步学习

### 新手必读
1. **QUICK_REFERENCE.md** - 快速参考卡片
2. **USAGE.md** - 详细使用教程

### 进阶阅读
3. **setup_guide.md** - 深入的配置说明
4. **README.md** - 完整的项目文档

### 开发者
5. **CONTRIBUTING.md** - 贡献指南
6. **PROJECT_SUMMARY.md** - 项目技术总结

## 🐛 遇到问题？

### 常见问题快速解决

**问题1: 提示找不到模块**
```bash
# 解决方案：安装依赖
pip install -r requirements.txt
```

**问题2: 找不到引擎**
```bash
# 解决方案：配置引擎
python download_engine.py
```

**问题3: 识别不到棋盘**
- 确保棋盘在屏幕中央
- 棋盘要完整显示
- 避免遮挡和半透明效果

**问题4: 程序很慢或卡顿**
- 降低分析深度（改为10）
- 增加截图间隔（改为3-5秒）

### 获取更多帮助

1. 查看 **USAGE.md** 的FAQ部分
2. 运行 `python test_basic.py` 诊断问题
3. 查看程序生成的 `debug_board.png` 了解识别情况
4. 在GitHub提交Issue

## ⚠️ 使用须知

### ✅ 推荐用途
- 🎓 学习象棋，提高棋艺
- 📊 复盘分析，找出失误
- 🔬 研究开局和残局
- 🤖 人机对弈练习

### ❌ 禁止用途
- 🚫 线上排位赛作弊
- 🚫 正式比赛中使用
- 🚫 侵犯他人权益
- 🚫 违反平台规则

**请合法、道德地使用本程序！**

## 🎯 快速参考

### 文件用途速查

```
chess_gui.py              GUI图形界面（推荐新手）
chess_assistant.py        命令行版本（高级用户）
test_basic.py             测试安装是否成功
download_engine.py        下载配置引擎
quickstart.py             交互式快速启动
run.bat                   Windows一键启动
```

### 目录说明

```
engine/                   象棋引擎存放处
  └─ pikafish.exe        需要下载
debug_*.png              调试图像（程序自动生成）
```

## 💡 使用技巧

1. **第一次使用**：建议用GUI版本，更直观
2. **调试问题**：查看生成的debug_board.png图像
3. **提高准确率**：使用标准棋盘界面，避免3D或特效
4. **节省资源**：不分析时记得停止程序
5. **快速操作**：记住快捷键 Ctrl+S 和 Ctrl+Q

## 📞 需要帮助？

- 💬 **使用问题**：查看 USAGE.md
- 🔧 **安装问题**：查看 setup_guide.md  
- 📖 **功能说明**：查看 README.md
- 🐛 **报告Bug**：GitHub Issues
- 💡 **功能建议**：GitHub Discussions

## 🎉 准备好了吗？

如果你已经完成了上述步骤，现在可以：

1. 打开象棋对弈界面
2. 启动程序（`python chess_gui.py`）
3. 点击"开始分析"
4. 享受智能辅助的乐趣！

---

**祝你使用愉快！提高棋艺！** 🎯♟️

如有任何问题，请查阅相关文档或提交Issue。

