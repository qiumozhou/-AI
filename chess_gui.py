"""
中国象棋辅助程序 - GUI版本
提供图形界面，更方便使用
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from chess_assistant import ChineseChessAssistant
import pyautogui
from PIL import Image, ImageTk
import cv2
import numpy as np


class ChessAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("中国象棋辅助程序")
        self.root.geometry("800x600")
        
        self.assistant = ChineseChessAssistant()
        self.is_running = False
        self.analysis_thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """
        设置UI界面
        """
        # 顶部控制面板
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # 开始/停止按钮
        self.start_btn = ttk.Button(
            control_frame, 
            text="开始分析 (Ctrl+S)", 
            command=self.toggle_analysis
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # 截图按钮
        self.capture_btn = ttk.Button(
            control_frame,
            text="立即截图",
            command=self.capture_once
        )
        self.capture_btn.pack(side=tk.LEFT, padx=5)
        
        # 清空日志按钮
        clear_btn = ttk.Button(
            control_frame,
            text="清空日志",
            command=self.clear_log
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态标签
        self.status_label = ttk.Label(
            control_frame,
            text="状态: 未启动",
            foreground="gray"
        )
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        # 设置面板
        settings_frame = ttk.LabelFrame(self.root, text="设置", padding="10")
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 截图间隔
        interval_frame = ttk.Frame(settings_frame)
        interval_frame.pack(fill=tk.X)
        
        ttk.Label(interval_frame, text="截图间隔(秒):").pack(side=tk.LEFT)
        self.interval_var = tk.IntVar(value=2)
        interval_spinbox = ttk.Spinbox(
            interval_frame,
            from_=1,
            to=10,
            textvariable=self.interval_var,
            width=10
        )
        interval_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 分析深度
        depth_frame = ttk.Frame(settings_frame)
        depth_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(depth_frame, text="分析深度:").pack(side=tk.LEFT)
        self.depth_var = tk.IntVar(value=15)
        depth_spinbox = ttk.Spinbox(
            depth_frame,
            from_=5,
            to=25,
            textvariable=self.depth_var,
            width=10
        )
        depth_spinbox.pack(side=tk.LEFT, padx=5)
        ttk.Label(depth_frame, text="(越大越准确但越慢)").pack(side=tk.LEFT)
        
        # 主内容区域 - 使用PanedWindow分割
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 左侧：棋盘预览
        left_frame = ttk.LabelFrame(main_paned, text="棋盘预览", padding="5")
        main_paned.add(left_frame, weight=1)
        
        self.board_canvas = tk.Canvas(left_frame, bg="white", width=300, height=350)
        self.board_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 右侧：日志和建议
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # 建议走法
        suggestion_frame = ttk.LabelFrame(right_frame, text="建议走法", padding="10")
        suggestion_frame.pack(fill=tk.X, pady=5)
        
        self.suggestion_text = tk.Text(
            suggestion_frame,
            height=3,
            font=("Arial", 14, "bold"),
            foreground="blue",
            wrap=tk.WORD
        )
        self.suggestion_text.pack(fill=tk.X)
        self.suggestion_text.insert("1.0", "等待分析...")
        self.suggestion_text.config(state=tk.DISABLED)
        
        # 日志输出
        log_frame = ttk.LabelFrame(right_frame, text="运行日志", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 底部状态栏
        status_bar = ttk.Frame(self.root)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.engine_status = ttk.Label(
            status_bar,
            text=f"引擎: {'就绪' if self.assistant.engine_path else '未配置'}",
            relief=tk.SUNKEN
        )
        self.engine_status.pack(side=tk.LEFT, padx=5)
        
        # 绑定快捷键
        self.root.bind('<Control-s>', lambda e: self.toggle_analysis())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        
        # 初始日志
        self.log("程序已启动")
        self.log("快捷键: Ctrl+S 开始/停止, Ctrl+Q 退出")
        
        if not self.assistant.engine_path:
            self.log("警告: 引擎未配置，请运行 download_engine.py", "warning")
    
    def log(self, message, level="info"):
        """
        添加日志
        """
        timestamp = time.strftime("%H:%M:%S")
        
        # 颜色标记
        colors = {
            "info": "black",
            "warning": "orange",
            "error": "red",
            "success": "green"
        }
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        
        # 滚动到底部
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def update_suggestion(self, move):
        """
        更新建议走法显示
        """
        self.suggestion_text.config(state=tk.NORMAL)
        self.suggestion_text.delete("1.0", tk.END)
        self.suggestion_text.insert("1.0", f"建议: {move}")
        self.suggestion_text.config(state=tk.DISABLED)
    
    def update_board_preview(self, image):
        """
        更新棋盘预览
        """
        # 调整图像大小以适应canvas
        h, w = image.shape[:2]
        canvas_w = self.board_canvas.winfo_width()
        canvas_h = self.board_canvas.winfo_height()
        
        if canvas_w > 1 and canvas_h > 1:
            scale = min(canvas_w/w, canvas_h/h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            
            resized = cv2.resize(image, (new_w, new_h))
            
            # 转换为PIL格式
            rgb_image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_image)
            photo = ImageTk.PhotoImage(pil_image)
            
            # 更新canvas
            self.board_canvas.delete("all")
            self.board_canvas.create_image(
                canvas_w//2, canvas_h//2,
                image=photo,
                anchor=tk.CENTER
            )
            self.board_canvas.image = photo  # 保持引用
    
    def toggle_analysis(self):
        """
        切换分析状态
        """
        if not self.is_running:
            self.start_analysis()
        else:
            self.stop_analysis()
    
    def start_analysis(self):
        """
        开始分析
        """
        self.is_running = True
        self.start_btn.config(text="停止分析")
        self.status_label.config(text="状态: 运行中", foreground="green")
        self.log("开始分析...", "success")
        
        # 更新助手配置
        self.assistant.screenshot_interval = self.interval_var.get()
        
        # 启动分析线程
        self.analysis_thread = threading.Thread(target=self.analysis_loop, daemon=True)
        self.analysis_thread.start()
    
    def stop_analysis(self):
        """
        停止分析
        """
        self.is_running = False
        self.start_btn.config(text="开始分析 (Ctrl+S)")
        self.status_label.config(text="状态: 已停止", foreground="gray")
        self.log("分析已停止", "info")
    
    def analysis_loop(self):
        """
        分析循环（在独立线程中运行）
        """
        while self.is_running:
            try:
                # 截图
                self.log("正在截图...")
                screen = self.assistant.capture_screen()
                
                # 检测棋盘
                board_region = self.assistant.detect_chessboard(screen)
                
                if board_region:
                    x, y, w, h = board_region
                    board_image = screen[y:y+h, x:x+w]
                    
                    # 更新预览
                    self.root.after(0, self.update_board_preview, board_image)
                    
                    # 识别棋子
                    self.log("识别棋局...")
                    fen = self.assistant.recognize_pieces(board_image)
                    
                    # 分析
                    if self.assistant.engine_path:
                        self.log("引擎分析中...")
                        best_move = self.assistant.analyze_position(fen)
                        formatted_move = self.assistant.format_move(best_move)
                        
                        self.log(f"最佳走法: {formatted_move}", "success")
                        self.root.after(0, self.update_suggestion, formatted_move)
                    else:
                        self.log("引擎未配置，跳过分析", "warning")
                else:
                    self.log("未检测到棋盘", "warning")
                
                # 等待
                time.sleep(self.assistant.screenshot_interval)
                
            except Exception as e:
                self.log(f"错误: {str(e)}", "error")
                time.sleep(1)
    
    def capture_once(self):
        """
        立即截图一次
        """
        self.log("立即截图...")
        try:
            screen = self.assistant.capture_screen()
            board_region = self.assistant.detect_chessboard(screen)
            
            if board_region:
                x, y, w, h = board_region
                board_image = screen[y:y+h, x:x+w]
                self.update_board_preview(board_image)
                self.log("截图成功", "success")
            else:
                self.log("未检测到棋盘", "warning")
        except Exception as e:
            self.log(f"截图失败: {str(e)}", "error")
    
    def clear_log(self):
        """
        清空日志
        """
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = ChessAssistantGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

