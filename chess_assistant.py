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

# Windows平台的subprocess标志
if sys.platform == 'win32':
    CREATE_NO_WINDOW = 0x08000000
else:
    CREATE_NO_WINDOW = 0


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
        
        # 获取程序运行目录（支持打包后的exe）
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe
            base_path = Path(sys.executable).parent
        else:
            # 如果是Python脚本
            base_path = Path(__file__).parent
        
        # 检查引擎是否存在
        engine_dir = base_path / "engine"
        engine_dir.mkdir(exist_ok=True)
        
        # Windows平台
        if sys.platform == "win32":
            engine_file = engine_dir / "pikafish.exe"
            if not engine_file.exists():
                print("未找到引擎文件，请手动下载Pikafish引擎")
                print("下载地址: https://github.com/official-pikafish/Pikafish/releases")
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
        try:
            # 调整图像大小以便处理
            h, w = board_image.shape[:2]
            if w > 900 or h > 1000:
                scale = min(900/w, 1000/h)
                board_image = cv2.resize(board_image, (int(w*scale), int(h*scale)))
            
            # 保存调试图像
            cv2.imwrite("debug_board_original.png", board_image)
            
            # 分析棋盘并识别棋子
            fen = self._analyze_board_image(board_image)
            return fen
            
        except Exception as e:
            print(f"棋子识别出错: {e}")
            # 返回初始局面作为后备
            return "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"
    
    def _analyze_board_image(self, board_image):
        """
        分析棋盘图像并生成FEN
        """
        # 转换为HSV色彩空间
        hsv = cv2.cvtColor(board_image, cv2.COLOR_BGR2HSV)
        h, w = board_image.shape[:2]
        
        # 将棋盘分成9x10的格子
        cell_width = w / 9
        cell_height = h / 10
        
        # 用于存储棋盘状态 [10行][9列]
        board = [[None for _ in range(9)] for _ in range(10)]
        
        # 检测每个格子
        for row in range(10):
            for col in range(9):
                # 计算格子中心位置
                x = int((col + 0.5) * cell_width)
                y = int((row + 0.5) * cell_height)
                
                # 提取格子区域（中心区域，避免边界线干扰）
                # 使用更大的区域以提高检测率
                x1 = int(col * cell_width + cell_width * 0.2)
                y1 = int(row * cell_height + cell_height * 0.2)
                x2 = int((col + 1) * cell_width - cell_width * 0.2)
                y2 = int((row + 1) * cell_height - cell_height * 0.2)
                
                cell = board_image[y1:y2, x1:x2]
                if cell.size == 0:
                    continue
                
                # 检测这个格子是否有棋子
                piece = self._detect_piece_in_cell(cell, hsv[y1:y2, x1:x2], row, col)
                board[row][col] = piece
                
                # 保存第一行的格子用于调试（可选）
                # if row == 0:
                #     cv2.imwrite(f"debug_cell_{row}_{col}.png", cell)
        
        # 转换为FEN格式
        fen = self._board_to_fen(board)
        return fen
    
    def _detect_piece_in_cell(self, cell_bgr, cell_hsv, row, col):
        """
        检测单个格子中的棋子
        返回: 'r', 'n', 'b', 'a', 'k', 'c', 'p' (黑方小写) 
              'R', 'N', 'B', 'A', 'K', 'C', 'P' (红方大写)
              或 None (空格)
        """
        if cell_hsv.size == 0:
            return None
        
        # 定义颜色范围 (HSV) - 放宽范围以提高识别率
        # 红色棋子（两个范围，因为红色跨越HSV色相环）
        red_lower1 = np.array([0, 50, 50])      # 降低饱和度和亮度要求
        red_upper1 = np.array([15, 255, 255])   # 扩大色相范围
        red_lower2 = np.array([165, 50, 50])
        red_upper2 = np.array([180, 255, 255])
        
        # 黑色棋子（包括深灰色）
        black_lower = np.array([0, 0, 0])
        black_upper = np.array([180, 255, 100])  # 提高亮度上限
        
        # 检测红色
        mask_red1 = cv2.inRange(cell_hsv, red_lower1, red_upper1)
        mask_red2 = cv2.inRange(cell_hsv, red_lower2, red_upper2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        # 检测黑色
        mask_black = cv2.inRange(cell_hsv, black_lower, black_upper)
        
        red_pixels = cv2.countNonZero(mask_red)
        black_pixels = cv2.countNonZero(mask_black)
        total_pixels = cell_hsv.shape[0] * cell_hsv.shape[1]
        
        # 如果颜色像素占比太少，认为是空格
        threshold = total_pixels * 0.10  # 提高阈值
        
        # 调试输出
        if red_pixels > 10 or black_pixels > 10:
            piece_found = red_pixels > threshold or black_pixels > threshold
            # print(f"格子[{row},{col}]: 红={red_pixels}, 黑={black_pixels}, 阈值={threshold:.0f}, 有棋子={piece_found}")
        
        if red_pixels < threshold and black_pixels < threshold:
            return None
        
        # 额外验证：两种颜色不能都很多（可能是噪声）
        if red_pixels > threshold * 0.5 and black_pixels > threshold * 0.5:
            # 如果红黑都有，选择占比更大的
            if abs(red_pixels - black_pixels) < threshold * 0.3:
                return None  # 颜色混杂，可能不是棋子
        
        # 根据位置推断棋子类型（使用初始局面的位置）
        is_red = red_pixels > black_pixels
        
        # 根据行列位置推断棋子类型
        piece = self._infer_piece_by_position(row, col, is_red)
        
        return piece
    
    def _infer_piece_by_position(self, row, col, is_red):
        """
        根据位置推断棋子类型（基于标准开局）
        对于非标准位置，返回通用棋子标记
        """
        # 黑方（上方，row 0-4）
        if not is_red:
            if row == 0:  # 第一行
                if col in [0, 8]: return 'r'  # 车
                if col in [1, 7]: return 'n'  # 马
                if col in [2, 6]: return 'b'  # 象
                if col in [3, 5]: return 'a'  # 士
                if col == 4: return 'k'  # 将
                return None  # 第一行其他位置不应有棋子
            elif row == 2:  # 第三行
                if col in [1, 7]: return 'c'  # 炮
                return None
            elif row == 3:  # 第四行
                if col in [0, 2, 4, 6, 8]: return 'p'  # 卒
                return None
            elif row == 1:  # 第二行
                return None  # 开局时第二行应为空
            else:
                # 中局时可能有棋子，使用通用标记
                if row <= 4:
                    return 'p'  # 黑方其他位置默认为卒
                return None
        
        # 红方（下方，row 5-9）
        else:
            if row == 9:  # 第十行
                if col in [0, 8]: return 'R'  # 车
                if col in [1, 7]: return 'N'  # 马
                if col in [2, 6]: return 'B'  # 相
                if col in [3, 5]: return 'A'  # 仕
                if col == 4: return 'K'  # 帅
                return None
            elif row == 7:  # 第八行
                if col in [1, 7]: return 'C'  # 炮
                return None
            elif row == 6:  # 第七行
                if col in [0, 2, 4, 6, 8]: return 'P'  # 兵
                return None
            elif row == 8:  # 第九行
                return None  # 开局时第九行应为空
            else:
                # 中局时可能有棋子
                if row >= 5:
                    return 'P'  # 红方其他位置默认为兵
                return None
        
        return None
    
    def _board_to_fen(self, board):
        """
        将棋盘数组转换为FEN格式
        board: 10x9的二维数组
        """
        fen_rows = []
        
        for row in board:
            fen_row = ""
            empty_count = 0
            
            for piece in row:
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += piece
            
            # 添加末尾的空格数
            if empty_count > 0:
                fen_row += str(empty_count)
            
            # 如果整行为空，用9表示
            if not fen_row or fen_row == "":
                fen_row = "9"
            
            fen_rows.append(fen_row)
        
        # 拼接FEN（行之间用/分隔）
        position = "/".join(fen_rows)
        
        # 添加其他FEN信息
        # 格式: <位置> <轮到谁> <吃过路兵> <其他> <半回合> <回合数>
        fen = f"{position} w - - 0 1"
        
        # 打印棋盘状态用于调试
        print(f"\n识别的FEN: {fen}")
        print("棋盘状态:")
        piece_symbols = {
            'r': '車', 'n': '馬', 'b': '象', 'a': '士', 'k': '将',
            'c': '炮', 'p': '卒',
            'R': '车', 'N': '马', 'B': '相', 'A': '仕', 'K': '帅',
            'C': '砲', 'P': '兵'
        }
        for i, row in enumerate(board):
            row_str = f"第{i+1:2d}行: "
            for piece in row:
                if piece:
                    row_str += piece_symbols.get(piece, piece) + " "
                else:
                    row_str += "· "
            print(row_str)
        print()
        
        return fen
    
    def analyze_position(self, fen):
        """
        使用引擎分析局面
        返回最佳走法
        """
        if not self.engine_path or not os.path.exists(self.engine_path):
            return "引擎未就绪，请先下载Pikafish引擎"
        
        process = None
        try:
            # 启动引擎进程 - 使用更兼容的方式
            startupinfo = None
            creationflags = 0
            
            if sys.platform == 'win32':
                # Windows下隐藏控制台窗口
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                creationflags = CREATE_NO_WINDOW
            
            process = subprocess.Popen(
                [self.engine_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # 合并stderr到stdout
                text=True,
                encoding='utf-8',
                errors='ignore',  # 忽略编码错误
                bufsize=0,  # 无缓冲
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            
            # 等待进程启动
            time.sleep(0.1)
            
            # 发送UCI命令
            commands = [
                "uci\n",
                "isready\n",
                "setoption name Hash value 128\n",  # 降低内存使用
                "ucinewgame\n",
                f"position fen {fen}\n",
                "go depth 8\n"  # 进一步降低深度提高响应速度
            ]
            
            for cmd in commands:
                try:
                    if process.poll() is not None:
                        # 进程已结束
                        return "引擎进程意外终止"
                    process.stdin.write(cmd)
                    process.stdin.flush()
                    time.sleep(0.05)  # 短暂延迟
                except Exception as e:
                    print(f"发送命令失败: {cmd.strip()} - {e}")
                    return "引擎通信失败"
            
            # 读取引擎输出
            best_move = None
            timeout_counter = 0
            max_timeout = 300  # 最多等待3秒
            start_time = time.time()
            max_wait_time = 10  # 最长等待10秒
            
            print("等待引擎响应...")
            
            while timeout_counter < max_timeout:
                try:
                    # 检查总时间
                    if time.time() - start_time > max_wait_time:
                        print("引擎响应超时，强制退出")
                        break
                    
                    if process.poll() is not None:
                        # 进程已结束
                        print("引擎进程已结束")
                        break
                    
                    line = process.stdout.readline()
                    if not line:
                        timeout_counter += 1
                        time.sleep(0.01)
                        continue
                    
                    line = line.strip()
                    if line:
                        # 打印关键信息
                        if line.startswith("bestmove") or "depth" in line.lower():
                            print(f"引擎: {line}")
                        
                        if line.startswith("bestmove"):
                            parts = line.split()
                            if len(parts) >= 2:
                                best_move = parts[1]
                            break
                    
                    timeout_counter += 1
                except Exception as e:
                    print(f"读取输出异常: {e}")
                    break
            
            if not best_move:
                print(f"未找到最佳走法（超时计数: {timeout_counter}）")
            
            return best_move if best_move else "未找到最佳走法"
            
        except Exception as e:
            print(f"引擎分析异常: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"引擎错误: {str(e)}"
        finally:
            # 确保进程被正确关闭
            if process:
                try:
                    if process.poll() is None:
                        process.stdin.write("quit\n")
                        process.stdin.flush()
                        process.wait(timeout=1)
                except:
                    pass
                finally:
                    try:
                        if process.poll() is None:
                            process.terminate()
                            time.sleep(0.1)
                            if process.poll() is None:
                                process.kill()
                    except:
                        pass
    
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

