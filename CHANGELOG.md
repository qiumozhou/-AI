# 更新日志

所有重要的项目变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2025-10-29

### 🎉 首次发布

这是中国象棋辅助程序的第一个正式版本！

### ✨ 新增功能

#### 核心功能
- ✅ 自动屏幕截图功能
- ✅ 基于OpenCV的棋盘检测
- ✅ 基于颜色识别的棋子检测
- ✅ Pikafish引擎集成
- ✅ UCI协议通信
- ✅ FEN格式局面表示
- ✅ 实时走法建议

#### 用户界面
- ✅ GUI图形界面版本（基于Tkinter）
  - 棋盘实时预览
  - 参数可视化调节
  - 日志实时显示
  - 友好的操作界面
- ✅ 命令行版本
  - 轻量级运行
  - 快捷键控制
  - 适合后台运行

#### 辅助工具
- ✅ 引擎下载配置脚本 (`download_engine.py`)
- ✅ 功能测试脚本 (`test_basic.py`)
- ✅ 快速启动脚本 (`quickstart.py`)
- ✅ Windows批处理脚本 (`run.bat`)
- ✅ Linux/Mac Shell脚本 (`run.sh`)

#### 高级功能
- ✅ 可调节的截图间隔
- ✅ 可调节的分析深度
- ✅ 调试图像保存
- ✅ 热键快速控制
- ✅ 多线程分析

### 📚 文档

- ✅ 完整的README.md
- ✅ 详细的使用教程 (USAGE.md)
- ✅ 安装配置指南 (setup_guide.md)
- ✅ 快速参考卡片 (QUICK_REFERENCE.md)
- ✅ 项目技术总结 (PROJECT_SUMMARY.md)
- ✅ 贡献指南 (CONTRIBUTING.md)
- ✅ 新手入门指南 (START_HERE.md)
- ✅ 引擎配置说明 (engine/README.md)
- ✅ MIT开源许可证 (LICENSE)

### 🛠️ 技术栈

- Python 3.8+
- OpenCV 4.8 - 图像处理
- PyAutoGUI 0.9 - 屏幕截图
- Tkinter - GUI界面
- NumPy 1.24 - 数值计算
- Pillow 10.1 - 图像处理
- keyboard 0.13 - 热键控制
- Pikafish - 象棋引擎

### 📦 依赖管理

- ✅ requirements.txt - Python依赖清单
- ✅ 国内镜像源支持
- ✅ 自动依赖安装

### 🎯 支持的平台

- ✅ Windows 10/11 - 完全支持
- ⚠️ Linux - 基本支持
- ⚠️ macOS - 基本支持

### 🔧 配置

- ✅ 配置文件示例 (config.ini.example)
- ✅ .gitignore 规则
- ✅ 调试模式

### 📊 性能

- 截图速度：< 0.1秒
- 棋盘检测：< 0.5秒
- 棋子识别：< 1秒
- 引擎分析：3-5秒 (depth 15)

---

## [未来计划]

### v1.1.0 - 计划中

#### 改进
- [ ] 更准确的棋盘角点检测
- [ ] 透视变换优化
- [ ] OCR识别棋子汉字
- [ ] 配置文件加载和保存
- [ ] 分析历史记录

#### 新功能
- [ ] 多引擎支持
- [ ] 引擎对比分析
- [ ] 开局库支持
- [ ] 棋局保存和导出
- [ ] 中英文界面切换

#### 修复
- [ ] 提高Linux/Mac平台兼容性
- [ ] 优化资源占用
- [ ] 改进错误处理

### v2.0.0 - 长期目标

#### 重大改进
- [ ] YOLOv8深度学习识别
  - 训练专用模型
  - 更高的识别准确率
  - 支持更多棋盘样式
  
- [ ] Web界面
  - 浏览器访问
  - 移动端支持
  - 云端部署
  
- [ ] 棋局数据库
  - 历史记录
  - 统计分析
  - 学习建议

#### 高级功能
- [ ] 走法可视化
  - 棋盘着色
  - 箭头指示
  - 评分显示
  
- [ ] 智能助手
  - 语音提示
  - 自动落子（可选）
  - 学习模式

- [ ] 社区功能
  - 用户系统
  - 棋谱分享
  - 在线对弈

---

## 版本说明

### 版本号格式
```
主版本号.次版本号.修订号
MAJOR.MINOR.PATCH
```

- **主版本号**：重大功能变更，可能不向后兼容
- **次版本号**：新增功能，向后兼容
- **修订号**：Bug修复和小改进

### 更新类型

- **新增 (Added)**: 新功能
- **变更 (Changed)**: 现有功能的变更
- **弃用 (Deprecated)**: 即将移除的功能
- **移除 (Removed)**: 已移除的功能
- **修复 (Fixed)**: Bug修复
- **安全 (Security)**: 安全相关的修复

---

## 贡献

欢迎查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何为项目做出贡献。

## 许可

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**项目主页**: https://github.com/yourusername/chinese-chess-assistant  
**问题反馈**: https://github.com/yourusername/chinese-chess-assistant/issues  
**更新通知**: 关注项目获取最新版本

