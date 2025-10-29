# 快速参考卡片

## 🚀 10秒开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置引擎  
python download_engine.py

# 3. 启动程序
python chess_gui.py
```

## ⌨️ 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + S` | 开始/停止分析 |
| `Ctrl + C` | 立即截图 |
| `Ctrl + Q` | 退出程序 |

## 📂 重要文件

| 文件 | 用途 |
|------|------|
| `chess_gui.py` | GUI版本（推荐） |
| `chess_assistant.py` | 命令行版本 |
| `test_basic.py` | 测试安装 |
| `download_engine.py` | 配置引擎 |
| `engine/pikafish.exe` | 象棋引擎 |

## 🔧 常用命令

```bash
# 测试安装
python test_basic.py

# 启动GUI
python chess_gui.py

# 启动命令行
python chess_assistant.py

# 配置引擎
python download_engine.py

# 快速启动（交互式）
python quickstart.py

# Windows快捷启动
run.bat
```

## ⚙️ 参数调节

### 截图间隔
- **快速**: 1-2秒
- **标准**: 2-3秒  
- **慢速**: 3-5秒

### 分析深度
- **快速**: depth 10 (~1-2秒)
- **标准**: depth 15 (~3-5秒)
- **深度**: depth 20 (~10-20秒)

## 🐛 快速故障排除

| 问题 | 解决方案 |
|------|----------|
| 找不到引擎 | `python download_engine.py` |
| 依赖缺失 | `pip install -r requirements.txt` |
| 识别不到棋盘 | 调整棋盘位置到屏幕中央 |
| 程序卡顿 | 降低分析深度，增加截图间隔 |

## 📊 引擎配置

### UCI命令示例
```
uci                          # 初始化
setoption name Hash value 256    # 哈希表256MB
setoption name Threads value 4   # 使用4线程
ucinewgame                   # 新游戏
position fen <FEN>           # 设置局面
go depth 15                  # 分析15层
quit                         # 退出
```

### 常用选项
```
Hash: 128/256/512/1024       # 内存使用（MB）
Threads: 1/2/4/8             # CPU线程数
Depth: 10/15/20/25           # 搜索深度
```

## 📖 FEN格式示例

### 初始局面
```
rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1
```

### 格式说明
```
<棋子位置> <轮到谁> <可吃过路兵> <其他> <半回合> <回合数>
```

## 🎯 使用技巧

### 提高识别率
1. 棋盘放在屏幕中央
2. 使用标准棋盘样式
3. 确保完整显示
4. 避免遮挡和透明

### 提高分析速度
1. 降低分析深度
2. 使用固定截图区域
3. 增加截图间隔
4. 启用多线程

### 提高分析准确度
1. 增加分析深度
2. 增大哈希表
3. 使用多线程
4. 延长思考时间

## 🔗 常用链接

- **Pikafish下载**: https://github.com/official-pikafish/Pikafish/releases
- **问题反馈**: GitHub Issues
- **完整文档**: README.md
- **使用教程**: USAGE.md
- **安装指南**: setup_guide.md

## 📞 获取帮助

1. 查看 `USAGE.md` - 详细使用说明
2. 运行 `python test_basic.py` - 诊断问题
3. 检查 `debug_board.png` - 查看识别效果
4. 查看程序日志 - 了解错误信息
5. GitHub Issues - 报告问题

## ⚠️ 重要提醒

### ✅ 允许
- 个人学习练习
- 棋局复盘分析
- 研究象棋理论

### ❌ 禁止
- 线上排位作弊
- 正式比赛使用
- 违反平台规则

## 📈 性能参考

| 操作 | 耗时 |
|------|------|
| 截图 | < 0.1秒 |
| 棋盘检测 | < 0.5秒 |
| 棋子识别 | < 1秒 |
| 分析(depth 15) | 3-5秒 |

## 🔄 版本信息

- **当前版本**: v1.0.0
- **Python要求**: 3.8+
- **系统支持**: Windows 10/11
- **更新日期**: 2025-10-29

---

**💡 提示**: 首次使用建议阅读 `USAGE.md` 获取完整说明！

