"""
中国象棋辅助程序
通过截图识别棋局，使用Pikafish引擎分析最佳走法
"""

import time
import numpy as np
import cv2
from PIL import Image
import pyautogui
import keyboard
import os
import sys
from pathlib import Path
import subprocess
import urllib.request
import zipfile


class ChineseChessAssistant:
    def __init__(self):
        self.running = False
        self.screenshot_interval = 2  # 截图间隔（秒）
        self.engine_path = None
        self.current_fen = None
        
        # 初始化引擎
        self.setup_engine()
        
    def setup_engine(self):
        """设置Pikafish引擎"""
        print("正在设置Pikafish引擎...")
        
        # 检查引擎是否存在
        engine_dir = Path("engine")
        engine_dir.mkdir(exist_ok=True)
        
        # Windows平台
        if sys.platform == "win32":
            engine_file = engine_dir / "pikafish.exe"
            if not engine_file.exists():
                print("未找到引擎文件，请手动下载Pikafish引擎")
                print("下载地址: https://github.com/pikafish-Pikafish/Pikafish/releases")
                print(f"请将pikafish.exe放置在 {engine_dir.absolute()} 目录下")
                self.engine_path = None
            else:
                self.engine_path = str(engine_file.absolute())
                print(f"引擎路径: {self.engine_path}")
        else:
            print("当前仅支持Windows平台")
            
    def capture_screen(self, region=None):
        """
        截取屏幕
        region: (x, y, width, height) 截图区域，None表示全屏
        """
        screenshot = pyautogui.screenshot(region=region)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def detect_chessboard(self, image):
        """
        检测棋盘位置
        返回棋盘的边界框 (x, y, w, h)
        """
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 边缘检测
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # 霍夫变换检测直线
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
                                minLineLength=100, maxLineGap=10)
        
        if lines is None:
            return None
            
        # 分析线条找出棋盘区域
        # 这里简化处理，实际应用中需要更复杂的算法
        h, w = image.shape[:2]
        return (w//4, h//4, w//2, h//2)  # 返回中心区域作为示例
    
    def recognize_pieces(self, board_image):
        """
        识别棋盘上的棋子
        返回FEN格式的棋局描述
        """
        # 这是一个简化的实现
        # 实际应用中需要训练深度学习模型来识别棋子
        
        # 中国象棋初始局面的FEN
        initial_fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"
        
        print("棋子识别功能需要训练专门的模型，当前返回初始局面")
        return initial_fen
    
    def analyze_position(self, fen):
        """
        使用引擎分析局面
        返回最佳走法
        """
        if not self.engine_path or not os.path.exists(self.engine_path):
            return "引擎未就绪，请先下载Pikafish引擎"
        
        try:
            # 启动引擎进程
            process = subprocess.Popen(
                [self.engine_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # 发送UCI命令
            commands = [
                "uci\n",
                "setoption name Hash value 256\n",
                "ucinewgame\n",
                f"position fen {fen}\n",
                "go depth 15\n"  # 分析深度15
            ]
            
            for cmd in commands:
                process.stdin.write(cmd)
                process.stdin.flush()
            
            # 读取引擎输出
            best_move = None
            for line in process.stdout:
                print(f"引擎输出: {line.strip()}")
                if line.startswith("bestmove"):
                    best_move = line.split()[1]
                    break
            
            # 关闭引擎
            process.stdin.write("quit\n")
            process.stdin.flush()
            process.wait(timeout=5)
            
            return best_move if best_move else "未找到最佳走法"
            
        except Exception as e:
            return f"引擎分析出错: {str(e)}"
    
    def format_move(self, move_uci):
        """
        将UCI格式的走法转换为中文描述
        例如: e2e4 -> 兵二进四
        """
        if not move_uci or len(move_uci) < 4:
            return move_uci
        
        # 坐标映射
        files = "abcdefghi"
        ranks = "0123456789"
        
        from_file = files.index(move_uci[0])
        from_rank = int(move_uci[1])
        to_file = files.index(move_uci[2])
        to_rank = int(move_uci[3])
        
        # 简化的中文数字
        chinese_nums = "一二三四五六七八九"
        
        # 这里需要更复杂的逻辑来准确转换
        # 当前仅返回UCI格式
        return f"{move_uci} (坐标: {move_uci[0]}{move_uci[1]} -> {move_uci[2]}{move_uci[3]})"
    
    def display_suggestion(self, move):
        """
        显示走法建议
        """
        print("\n" + "="*50)
        print(f"建议走法: {self.format_move(move)}")
        print("="*50 + "\n")
    
    def run(self):
        """
        主循环
        """
        print("中国象棋辅助程序启动")
        print("按 Ctrl+S 开始/暂停分析")
        print("按 Ctrl+Q 退出程序")
        print("-" * 50)
        
        # 检查引擎
        if not self.engine_path:
            print("\n警告: 引擎未配置，程序将无法提供走法建议")
            print("请按照提示下载并配置Pikafish引擎\n")
        
        keyboard.add_hotkey('ctrl+s', self.toggle_running)
        keyboard.add_hotkey('ctrl+q', self.stop)
        
        try:
            while True:
                if self.running:
                    try:
                        # 截取屏幕
                        print("正在截图...")
                        screen = self.capture_screen()
                        
                        # 检测棋盘
                        board_region = self.detect_chessboard(screen)
                        if board_region:
                            x, y, w, h = board_region
                            board_image = screen[y:y+h, x:x+w]
                            
                            # 保存截图用于调试
                            cv2.imwrite("debug_board.png", board_image)
                            print("棋盘截图已保存到 debug_board.png")
                            
                            # 识别棋子
                            print("正在识别棋局...")
                            fen = self.recognize_pieces(board_image)
                            
                            # 如果局面发生变化，进行分析
                            if fen != self.current_fen:
                                self.current_fen = fen
                                print(f"当前局面 FEN: {fen}")
                                
                                # 分析局面
                                print("正在分析...")
                                best_move = self.analyze_position(fen)
                                self.display_suggestion(best_move)
                        else:
                            print("未检测到棋盘")
                        
                    except Exception as e:
                        print(f"处理出错: {str(e)}")
                    
                    # 等待下一次截图
                    time.sleep(self.screenshot_interval)
                else:
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\n程序已停止")
    
    def toggle_running(self):
        """切换运行状态"""
        self.running = not self.running
        status = "开始" if self.running else "暂停"
        print(f"\n>>> {status}分析 <<<\n")
    
    def stop(self):
        """停止程序"""
        print("\n正在退出...")
        os._exit(0)


def main():
    assistant = ChineseChessAssistant()
    assistant.run()


if __name__ == "__main__":
    main()

