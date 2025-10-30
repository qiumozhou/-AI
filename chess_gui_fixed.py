#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋识别助手 - 图形界面版本
使用深度学习技术识别中国象棋棋局并提供最佳走法建议
支持自动截图和自定义引擎深度
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import time
from pathlib import Path
import cv2
from PIL import Image, ImageTk
import pyautogui

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入项目模块
from cchess_deep_recognizer import CChessDeepRecognizer
from chess_assistant import ChineseChessAssistant


class ChessGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("中国象棋识别助手 - 增强版")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # 设置图标（如果存在）
        try:
            # 这里可以添加程序图标
            pass
        except:
            pass
        
        # 初始化变量
        self.current_image_path = None
        self.current_fen = None
        self.recognizer = None
        self.assistant = None
        
        # 自动截图相关变量
        self.auto_capture_running = False
        self.auto_capture_thread = None
        self.capture_interval = tk.DoubleVar(value=3.0)  # 默认3秒间隔
        self.engine_depth = tk.IntVar(value=8)  # 默认搜索深度8
        self.auto_analyze = tk.BooleanVar(value=True)  # 是否自动分析
        
        # 初始化识别器
        self.init_recognizers()
        
        # 创建界面
        self.create_widgets()
        
    def init_recognizers(self):
        """初始化识别器"""
        try:
            # 初始化深度学习识别器
            self.log_message("正在初始化深度学习识别器...")
            self.recognizer = CChessDeepRecognizer()
            
            if self.recognizer.pose_model and self.recognizer.classifier_model:
                self.log_message("✓ 深度学习识别器初始化成功")
            else:
                self.log_message("✗ 深度学习识别器初始化失败")
                self.recognizer = None
            
            # 初始化象棋助手（用于引擎分析）
            self.log_message("正在初始化引擎...")
            self.assistant = ChineseChessAssistant()
            if self.assistant.engine_path:
                self.log_message("✓ Pikafish引擎初始化成功")
            else:
                self.log_message("✗ Pikafish引擎未找到")
                
        except Exception as e:
            self.log_message(f"✗ 初始化失败: {e}")
    
    def create_widgets(self):
        """创建界面组件"""
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 1. 文件选择和自动截图区域
        file_frame = ttk.LabelFrame(main_frame, text="图片选择 & 自动截图", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # 文件选择行
        ttk.Button(file_frame, text="选择图片", command=self.select_image).grid(row=0, column=0, padx=(0, 10))
        
        self.file_path_var = tk.StringVar(value="请选择要识别的棋盘图片...")
        ttk.Label(file_frame, textvariable=self.file_path_var, foreground="gray").grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        self.recognize_btn = ttk.Button(file_frame, text="开始识别", command=self.start_recognition, state="disabled")
        self.recognize_btn.grid(row=0, column=2, padx=(10, 0))
        
        # 自动截图控制行
        ttk.Label(file_frame, text="截图间隔:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        interval_frame = ttk.Frame(file_frame)
        interval_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 0), padx=(10, 0))
        
        ttk.Scale(interval_frame, from_=1.0, to=10.0, variable=self.capture_interval, 
                 orient=tk.HORIZONTAL, length=150).grid(row=0, column=0)
        ttk.Label(interval_frame, text="秒").grid(row=0, column=1, padx=(5, 0))
        self.interval_label = ttk.Label(interval_frame, text="3.0")
        self.interval_label.grid(row=0, column=2, padx=(5, 0))
        
        # 更新间隔显示
        self.capture_interval.trace('w', self.update_interval_display)
        
        self.auto_capture_btn = ttk.Button(file_frame, text="开始自动截图", command=self.toggle_auto_capture)
        self.auto_capture_btn.grid(row=1, column=2, padx=(10, 0), pady=(10, 0))
        
        # 2. 引擎设置区域
        engine_frame = ttk.LabelFrame(main_frame, text="引擎设置", padding="5")
        engine_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        engine_frame.columnconfigure(1, weight=1)
        
        ttk.Label(engine_frame, text="搜索深度:").grid(row=0, column=0, sticky=tk.W)
        
        depth_frame = ttk.Frame(engine_frame)
        depth_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        ttk.Scale(depth_frame, from_=1, to=15, variable=self.engine_depth, 
                 orient=tk.HORIZONTAL, length=200).grid(row=0, column=0)
        self.depth_label = ttk.Label(depth_frame, text="8")
        self.depth_label.grid(row=0, column=1, padx=(5, 0))
        
        # 更新深度显示
        self.engine_depth.trace('w', self.update_depth_display)
        
        ttk.Checkbutton(engine_frame, text="自动分析", variable=self.auto_analyze).grid(row=0, column=2, padx=(20, 0))
        
        # 3. 结果显示区域
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        result_frame.columnconfigure(0, weight=1)
        result_frame.columnconfigure(1, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 3.1 左侧：棋盘显示
        board_frame = ttk.LabelFrame(result_frame, text="棋盘状态", padding="5")
        board_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        board_frame.columnconfigure(0, weight=1)
        board_frame.rowconfigure(0, weight=1)
        
        self.board_text = scrolledtext.ScrolledText(board_frame, height=12, width=35, 
                                                   font=("Consolas", 11), state="disabled")
        self.board_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 3.2 右侧：FEN和分析结果
        info_frame = ttk.LabelFrame(result_frame, text="识别结果与分析", padding="5")
        info_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(1, weight=1)
        
        # FEN结果
        ttk.Label(info_frame, text="FEN:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.fen_text = scrolledtext.ScrolledText(info_frame, height=3, width=40, 
                                                 font=("Consolas", 9), state="disabled")
        self.fen_text.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 分析按钮
        self.analyze_btn = ttk.Button(info_frame, text="分析双方走法", command=self.start_analysis, state="disabled")
        self.analyze_btn.grid(row=2, column=0, pady=(0, 10))
        
        # 分析结果
        ttk.Label(info_frame, text="最佳走法:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.analysis_text = scrolledtext.ScrolledText(info_frame, height=6, width=40, 
                                                      font=("Consolas", 9), state="disabled")
        self.analysis_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 4. 日志输出区域
        log_frame = ttk.LabelFrame(main_frame, text="运行日志", padding="5")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 初始化日志
        self.log_message("中国象棋识别助手 - 增强版已启动")
        self.log_message("=" * 50)
        
        if self.recognizer:
            self.log_message("✓ 深度学习识别器已就绪")
        else:
            self.log_message("✗ 深度学习识别器未就绪，请检查模型文件")
            
        if self.assistant and self.assistant.engine_path:
            self.log_message("✓ Pikafish引擎已就绪")
        else:
            self.log_message("✗ Pikafish引擎未就绪")
            
        self.log_message("=" * 50)
        self.log_message("新功能:")
        self.log_message("- 自动截图：设置间隔后可定时截取屏幕")
        self.log_message("- 引擎深度：可调整引擎搜索深度（1-15）")
        self.log_message("- 双方分析：同时分析红方和黑方的最佳走法")
        self.log_message("- 自动分析：识别后自动进行双方引擎分析")
        self.log_message("=" * 50)
    
    def update_interval_display(self, *args):
        """更新间隔显示"""
        value = self.capture_interval.get()
        self.interval_label.config(text=f"{value:.1f}")
    
    def update_depth_display(self, *args):
        """更新深度显示"""
        value = self.engine_depth.get()
        self.depth_label.config(text=str(value))
    
    def log_message(self, message):
        """在日志区域显示消息"""
        if hasattr(self, 'log_text'):
            self.log_text.config(state="normal")
            self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
            self.log_text.see(tk.END)
            self.log_text.config(state="disabled")
            self.root.update_idletasks()
        else:
            print(message)  # 如果GUI还没创建完成，就打印到控制台
    
    def select_image(self):
        """选择图片文件"""
        file_types = [
            ("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
            ("PNG文件", "*.png"),
            ("JPEG文件", "*.jpg *.jpeg"),
            ("所有文件", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="选择棋盘图片",
            filetypes=file_types
        )
        
        if filename:
            self.current_image_path = filename
            self.file_path_var.set(f"已选择: {Path(filename).name}")
            self.recognize_btn.config(state="normal")
            self.log_message(f"已选择图片: {filename}")
    
    def toggle_auto_capture(self):
        """切换自动截图状态"""
        if self.auto_capture_running:
            self.stop_auto_capture()
        else:
            self.start_auto_capture()
    
    def start_auto_capture(self):
        """开始自动截图"""
        if not self.recognizer:
            messagebox.showerror("错误", "深度学习识别器未就绪，无法开始自动截图")
            return
        
        self.auto_capture_running = True
        self.auto_capture_btn.config(text="停止自动截图")
        
        # 禁用相关控件
        self.recognize_btn.config(state="disabled")
        
        self.log_message("开始自动截图模式")
        self.log_message(f"截图间隔: {self.capture_interval.get():.1f}秒")
        self.log_message(f"引擎深度: {self.engine_depth.get()}")
        self.log_message(f"自动分析: {'开启' if self.auto_analyze.get() else '关闭'}")
        
        # 启动自动截图线程
        self.auto_capture_thread = threading.Thread(target=self.auto_capture_loop, daemon=True)
        self.auto_capture_thread.start()
    
    def stop_auto_capture(self):
        """停止自动截图"""
        self.auto_capture_running = False
        self.auto_capture_btn.config(text="开始自动截图")
        
        # 重新启用控件
        self.recognize_btn.config(state="normal" if self.current_image_path else "disabled")
        
        self.log_message("已停止自动截图模式")
    
    def auto_capture_loop(self):
        """自动截图循环（后台线程）"""
        while self.auto_capture_running:
            try:
                # 截取屏幕
                self.log_message("正在截取屏幕...")
                screenshot = pyautogui.screenshot()
                
                # 转换为OpenCV格式
                screenshot_cv = cv2.cvtColor(cv2.array(screenshot), cv2.COLOR_RGB2BGR)
                
                # 保存临时截图
                temp_path = "temp_screenshot.png"
                cv2.imwrite(temp_path, screenshot_cv)
                
                # 在主线程中处理识别
                self.root.after(0, self.process_auto_capture, screenshot_cv, temp_path)
                
                # 等待指定间隔
                time.sleep(self.capture_interval.get())
                
            except Exception as e:
                self.root.after(0, self.log_message, f"✗ 自动截图出错: {e}")
                break
    
    def process_auto_capture(self, image, temp_path):
        """处理自动截图的识别"""
        try:
            # 使用深度学习识别
            self.log_message("正在识别截图...")
            fen = self.recognizer.recognize(image)
            
            if fen:
                fen = fen.strip()
                self.current_fen = fen
                self.log_message("✓ 识别成功")
                
                # 更新显示
                self.update_recognition_results(fen)
                
                # 如果开启自动分析
                if self.auto_analyze.get() and self.assistant and self.assistant.engine_path:
                    self.log_message("开始自动引擎分析（红/黑双方）...")
                    # 在后台线程中进行分析
                    threading.Thread(target=self.run_both_sides_analysis, daemon=True).start()
            else:
                self.log_message("✗ 截图识别失败，未检测到有效棋盘")
                
        except Exception as e:
            self.log_message(f"✗ 处理截图出错: {e}")
        finally:
            # 清理临时文件
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass
    
    def start_recognition(self):
        """开始识别（在后台线程中运行）"""
        if not self.current_image_path:
            messagebox.showwarning("警告", "请先选择图片文件")
            return
            
        if not self.recognizer:
            messagebox.showerror("错误", "深度学习识别器未就绪，请检查模型文件")
            return
        
        # 禁用按钮防止重复点击
        self.recognize_btn.config(state="disabled")
        self.analyze_btn.config(state="disabled")
        
        # 清空之前的结果
        self.clear_results()
        
        # 在后台线程中运行识别
        thread = threading.Thread(target=self.run_recognition, daemon=True)
        thread.start()
    
    def run_recognition(self):
        """运行识别（后台线程）"""
        try:
            self.log_message(f"开始识别图片: {Path(self.current_image_path).name}")
            
            # 读取图片
            image = cv2.imread(self.current_image_path)
            if image is None:
                raise ValueError("无法读取图片文件")
            
            self.log_message(f"图片尺寸: {image.shape[1]}x{image.shape[0]}")
            
            # 使用深度学习识别
            self.log_message("正在进行深度学习识别...")
            fen = self.recognizer.recognize(image)
            
            if fen:
                self.current_fen = fen.strip()
                self.log_message("✓ 识别成功！")
                self.log_message(f"FEN: {self.current_fen}")
                
                # 在主线程中更新GUI
                self.root.after(0, self.update_recognition_results, self.current_fen)
                
                # 如果开启自动分析
                if self.auto_analyze.get() and self.assistant and self.assistant.engine_path:
                    self.log_message("开始自动引擎分析（红/黑双方）...")
                    self.run_both_sides_analysis()
            else:
                self.log_message("✗ 识别失败")
                self.root.after(0, self.recognition_failed)
                
        except Exception as e:
            self.log_message(f"✗ 识别出错: {e}")
            self.root.after(0, self.recognition_failed)
    
    def update_recognition_results(self, fen):
        """更新识别结果显示"""
        # 更新FEN显示
        self.fen_text.config(state="normal")
        self.fen_text.delete(1.0, tk.END)
        self.fen_text.insert(1.0, fen)
        self.fen_text.config(state="disabled")
        
        # 更新棋盘显示
        self.display_board_from_fen(fen)
        
        # 启用分析按钮
        if self.assistant and self.assistant.engine_path:
            self.analyze_btn.config(state="normal")
        
        # 重新启用识别按钮（如果不在自动截图模式）
        if not self.auto_capture_running:
            self.recognize_btn.config(state="normal")
    
    def recognition_failed(self):
        """识别失败处理"""
        if not self.auto_capture_running:
            self.recognize_btn.config(state="normal")
        messagebox.showerror("识别失败", "图片识别失败，请检查图片质量或模型文件")
    
    def display_board_from_fen(self, fen):
        """从FEN显示棋盘"""
        try:
            piece_symbols = {
                'r': '車', 'n': '馬', 'b': '象', 'a': '士', 'k': '将',
                'c': '炮', 'p': '卒',
                'R': '车', 'N': '马', 'B': '相', 'A': '仕', 'K': '帅',
                'C': '砲', 'P': '兵'
            }
            
            # 解析FEN
            position = fen.split()[0]
            rows = position.split('/')
            
            # 构建棋盘显示
            board_display = "  " + "─" * 27 + "\n"
            
            for i, row in enumerate(rows):
                line = f"{i+1:2d}│"
                
                for char in row:
                    if char.isdigit():
                        # 数字表示空格数量
                        line += " · " * int(char)
                    else:
                        # 棋子
                        symbol = piece_symbols.get(char, char)
                        line += f" {symbol} "
                
                board_display += line + "\n"
            
            board_display += "  " + "─" * 27 + "\n"
            
            # 更新棋盘显示
            self.board_text.config(state="normal")
            self.board_text.delete(1.0, tk.END)
            self.board_text.insert(1.0, board_display)
            self.board_text.config(state="disabled")
            
        except Exception as e:
            self.log_message(f"棋盘显示出错: {e}")
    
    def start_analysis(self):
        """开始引擎分析（在后台线程中运行）"""
        if not self.current_fen:
            messagebox.showwarning("警告", "请先进行棋盘识别")
            return
        
        if not self.assistant or not self.assistant.engine_path:
            messagebox.showerror("错误", "Pikafish引擎未就绪")
            return
        
        # 禁用按钮
        self.analyze_btn.config(state="disabled")
        
        # 清空分析结果
        self.analysis_text.config(state="normal")
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.config(state="disabled")
        
        # 在后台线程中运行分析
        thread = threading.Thread(target=self.run_both_sides_analysis, daemon=True)
        thread.start()
    
    def run_both_sides_analysis(self):
        """同时分析红方和黑方的最佳走法（后台线程）"""
        try:
            depth = self.engine_depth.get()
            self.log_message(f"开始双方引擎分析（深度: {depth}）...")
            
            # 使用analyze_both_sides方法
            both_moves = self.assistant.analyze_both_sides(self.current_fen)
            
            red_move = both_moves.get('red', '未找到最佳走法')
            black_move = both_moves.get('black', '未找到最佳走法')
            
            if red_move != "未找到最佳走法" or black_move != "未找到最佳走法":
                self.log_message(f"✓ 双方分析完成（深度{depth}）")
                self.log_message(f"红方最佳走法: {red_move}")
                self.log_message(f"黑方最佳走法: {black_move}")
                
                # 格式化走法
                red_desc = self.assistant.format_move(red_move, self.current_fen) if red_move != "未找到最佳走法" else "未找到最佳走法"
                black_desc = self.assistant.format_move(black_move, self.current_fen) if black_move != "未找到最佳走法" else "未找到最佳走法"
                
                # 在主线程中更新GUI
                self.root.after(0, self.update_both_sides_results, red_move, red_desc, black_move, black_desc)
            else:
                self.log_message("✗ 双方分析均失败")
                self.root.after(0, self.analysis_failed)
            
        except Exception as e:
            self.log_message(f"✗ 双方分析出错: {e}")
            self.root.after(0, self.analysis_failed)
    
    def update_both_sides_results(self, red_move, red_desc, black_move, black_desc):
        """更新双方分析结果显示"""
        result_text = "═══ 双方最佳走法分析 ═══\n\n"
        
        # 红方分析结果
        result_text += "🔴 红方（帅方）:\n"
        if red_move != "未找到最佳走法":
            result_text += f"  走法: {red_move}\n"
            result_text += f"  说明: {red_desc.split(' | ')[1] if ' | ' in red_desc else red_desc}\n"
            result_text += f"  坐标: {red_move[:2]} → {red_move[2:4]}\n"
        else:
            result_text += "  暂无可行走法\n"
        
        result_text += "\n"
        
        # 黑方分析结果
        result_text += "⚫ 黑方（将方）:\n"
        if black_move != "未找到最佳走法":
            result_text += f"  走法: {black_move}\n"
            result_text += f"  说明: {black_desc.split(' | ')[1] if ' | ' in black_desc else black_desc}\n"
            result_text += f"  坐标: {black_move[:2]} → {black_move[2:4]}\n"
        else:
            result_text += "  暂无可行走法\n"
        
        result_text += "\n"
        result_text += f"搜索深度: {self.engine_depth.get()}\n"
        result_text += "提示: 根据实际轮次选择对应走法"
        
        # 更新显示
        self.analysis_text.config(state="normal")
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, result_text)
        self.analysis_text.config(state="disabled")
        
        # 重新启用分析按钮（如果不在自动截图模式）
        if not self.auto_capture_running:
            self.analyze_btn.config(state="normal")
    
    def analysis_failed(self):
        """分析失败处理"""
        self.analysis_text.config(state="normal")
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, "引擎分析失败\n请检查FEN格式或引擎配置")
        self.analysis_text.config(state="disabled")
        
        if not self.auto_capture_running:
            self.analyze_btn.config(state="normal")
    
    def clear_results(self):
        """清空结果显示"""
        # 清空FEN
        self.fen_text.config(state="normal")
        self.fen_text.delete(1.0, tk.END)
        self.fen_text.config(state="disabled")
        
        # 清空棋盘
        self.board_text.config(state="normal")
        self.board_text.delete(1.0, tk.END)
        self.board_text.config(state="disabled")
        
        # 清空分析
        self.analysis_text.config(state="normal")
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.config(state="disabled")
        
        # 重置变量
        self.current_fen = None
    
    def run(self):
        """运行GUI主循环"""
        try:
            # 程序退出时停止自动截图
            def on_closing():
                self.auto_capture_running = False
                self.root.destroy()
            
            self.root.protocol("WM_DELETE_WINDOW", on_closing)
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log_message("程序被用户中断")
        except Exception as e:
            self.log_message(f"程序出错: {e}")
            messagebox.showerror("错误", f"程序出现异常: {e}")


def main():
    """主函数"""
    # 设置工作目录
    os.chdir(Path(__file__).parent)
    
    # 创建并运行GUI
    app = ChessGUI()
    app.run()


if __name__ == "__main__":
    main()
