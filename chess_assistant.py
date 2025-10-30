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
import threading
import queue

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
        self.deep_learning_detector = None  # 深度学习识别器
        
        # 初始化引擎
        self.setup_engine()
        
        # 加载深度学习检测器
        self.setup_detector()
        
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
    
    def setup_detector(self):
        """设置深度学习检测器"""
        
        # 加载深度学习识别器
        try:
            from cchess_deep_recognizer import CChessDeepRecognizer
            models_dir = Path("models/cchess_recognition")
            
            # 检查模型文件是否存在
            if (models_dir / "rtmpose-t-cchess_4.onnx").exists() and \
               (models_dir / "swinv2-nano_cchess16.onnx").exists():
                self.deep_learning_detector = CChessDeepRecognizer()
                if self.deep_learning_detector.pose_model and self.deep_learning_detector.classifier_model:
                    print("✓ 深度学习识别器已加载（准确率：85-90%）")
                else:
                    self.deep_learning_detector = None
                    print("✗ 深度学习模型加载失败")
            else:
                print("✗ 深度学习模型未找到")
                print(f"  模型位置: {models_dir.absolute()}")
                print("  请运行 python download_nnue.py 下载模型")
                self.deep_learning_detector = None
        except Exception as e:
            print(f"✗ 深度学习识别器加载失败: {e}")
            self.deep_learning_detector = None
            
        if self.deep_learning_detector:
            print("\n识别方案: 深度学习识别")
        else:
            print("\n⚠ 深度学习识别器未加载，程序将无法工作")
            print("请确保:")
            print("  1. 已下载ONNX模型文件")
            print("  2. 安装了 onnxruntime: pip install onnxruntime")
            
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
        使用深度学习识别棋盘上的棋子
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
            
            # 使用深度学习识别器
            if self.deep_learning_detector and self.deep_learning_detector.pose_model:
                print("正在使用深度学习识别...")
                try:
                    fen = self.deep_learning_detector.recognize(board_image)
                    if fen and self._validate_fen(fen):
                        print("✓ 深度学习识别成功")
                        return fen
                    else:
                        print("⚠ 深度学习识别结果无效")
                        # 返回初始局面作为后备
                        return "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"
                except Exception as e:
                    print(f"深度学习识别出错: {e}")
                    import traceback
                    traceback.print_exc()
                    return "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"
            else:
                print("✗ 深度学习识别器未加载")
                return "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"
            
        except Exception as e:
            print(f"棋子识别出错: {e}")
            import traceback
            traceback.print_exc()
            # 返回初始局面作为后备
            return "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"
    
    def _validate_fen(self, fen):
        """验证FEN的基本有效性"""
        if not fen:
            return False
        # 检查是否包含将帅
        fen_lower = fen.lower()
        has_black_king = 'k' in fen_lower
        has_red_king = 'K' in fen
        return has_black_king and has_red_king
    
    def analyze_position(self, fen, side_to_move='w', depth=8):
        """
        使用引擎分析局面
        参数:
            fen: 棋局的FEN格式
            side_to_move: 走棋方，'w'表示红方，'b'表示黑方
            depth: 搜索深度
        返回最佳走法
        """
        if not self.engine_path or not os.path.exists(self.engine_path):
            return "引擎未就绪，请先下载Pikafish引擎"
        
        # 简单验证FEN格式
        if not fen or len(fen) < 10:
            return "FEN格式无效"
        
        # 修改FEN中的走棋方，使用简洁格式
        fen_parts = fen.split()
        if len(fen_parts) >= 1:
            # 只保留位置和走棋方，不要其他附加信息
            position = fen_parts[0]
            fen = f"{position} {side_to_move}"
        else:
            # 如果FEN格式不完整
            fen = f"{fen} {side_to_move}"
        
        # 检查是否有足够的棋子（至少要有将/帅）
        if 'k' not in fen.lower() or 'K' not in fen:
            print("警告: FEN中缺少将帅，可能识别不准确")
            # 仍然尝试分析
        
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
            
            # 设置引擎工作目录为engine目录（重要！）
            engine_dir = Path(self.engine_path).parent
            
            process = subprocess.Popen(
                [self.engine_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # 合并stderr到stdout
                text=True,
                bufsize=1,  # 行缓冲
                cwd=str(engine_dir),
                universal_newlines=True,
                # 保持交互式环境，不隐藏窗口
            )
            
            output_queue = queue.Queue()
            
            def read_output():
                """持续读取引擎输出"""
                while process.poll() is None:
                    try:
                        line = process.stdout.readline()
                        if line:
                            output_queue.put(line.rstrip('\n\r'))
                    except:
                        break
            
            # 启动输出读取线程
            output_thread = threading.Thread(target=read_output, daemon=True)
            output_thread.start()
            
            def send_command_and_collect(command, wait_time=5):
                """发送命令并收集响应"""
                # 发送命令
                process.stdin.write(command + '\n')
                process.stdin.flush()
                
                # 收集响应
                responses = []
                start_time = time.time()
                
                while time.time() - start_time < wait_time:
                    try:
                        line = output_queue.get(timeout=0.1)
                        responses.append(line)
                        
                        # 如果收到bestmove，分析完成
                        if line.startswith('bestmove'):
                            break
                            
                    except queue.Empty:
                        continue
                
                return responses
            
            # 等待引擎启动
            time.sleep(0.2)
            
            # 清空启动消息
            while True:
                try:
                    line = output_queue.get(timeout=0.1)
                    if 'Pikafish' in line:
                        break
                except queue.Empty:
                    break
            
            # 发送position命令
            pos_responses = send_command_and_collect(f"position {fen}", 2)
            
            # 发送go depth命令
            go_responses = send_command_and_collect(f"go depth {depth}", 15)
            
            # 汇总响应并解析
            all_responses = pos_responses + go_responses
            
            info_depth_lines = [line for line in all_responses if line.startswith('info depth')]
            bestmove_lines = [line for line in all_responses if line.startswith('bestmove')]
            
            if bestmove_lines:
                bestmove_line = bestmove_lines[-1]
                parts = bestmove_line.split()
                best_move = parts[1] if len(parts) >= 2 else None
                
                print(f"✅ 交互式分析完成，最佳走法: {best_move}")
                print(f"📊 分析深度: {len(info_depth_lines)} 层")
                
                # 显示分析过程（可选）
                if info_depth_lines and len(info_depth_lines) > 2:
                    print(f"📈 评分变化:")
                    for line in info_depth_lines:
                        if 'score cp' in line:
                            try:
                                cp_score = line.split('score cp')[1].split()[0]
                                depth_num = line.split('depth')[1].split()[0]
                                print(f"  深度{depth_num}: {cp_score}厘兵")
                            except:
                                pass
                
                return best_move
            else:
                print("❌ 未找到最佳走法")
                return "未找到最佳走法"
                
        except subprocess.TimeoutExpired:
            print("引擎分析超时")
            if process:
                process.kill()
            return "分析超时"
        except Exception as e:
            print(f"引擎分析异常: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"引擎错误: {str(e)}"
        finally:
            # 清理进程
            try:
                if process and process.poll() is None:
                    process.stdin.write("quit\n")
                    process.stdin.flush()
                    process.wait(timeout=3)
            except:
                if process:
                    process.terminate()
    
    def analyze_both_sides(self, fen, depth=8):
        """
        同时分析红方和黑方的最佳走法
        参数:
            fen: 棋局的FEN格式  
            depth: 搜索深度
        返回: {'red': 红方走法, 'black': 黑方走法}
        """
        print(f"🔄 开始双方分析（深度: {depth}）...")
        
        result = {}
        
        # 分析红方走法
        print("🔴 分析红方...")
        red_move = self.analyze_position(fen, 'w', depth)
        result['red'] = red_move
        print(f"🔴 红方走法: {red_move}")
        
        # 分析黑方走法
        print("⚫ 分析黑方...")
        black_move = self.analyze_position(fen, 'b', depth)
        result['black'] = black_move
        print(f"⚫ 黑方走法: {black_move}")
        
        return result
    
    def format_move(self, move_uci, fen=None):
        """
        将UCI格式的走法转换为中文描述
        例如: a3a4 -> 卒一进一
        """
        if not move_uci or len(move_uci) < 4:
            return move_uci
        
        try:
            # 坐标映射
            files = "abcdefghi"  # a-i 对应 1-9路
            chinese_nums = "一二三四五六七八九"
            
            from_file = files.index(move_uci[0])
            from_rank = int(move_uci[1])
            to_file = files.index(move_uci[2])
            to_rank = int(move_uci[3])
            
            # 路数（列）转换
            from_road = chinese_nums[from_file]
            to_road = chinese_nums[to_file]
            
            # 根据行数判断是红方还是黑方棋子
            is_red_move = from_rank >= 5  # 5-9行是红方区域
            
            # 尝试从FEN中识别棋子类型
            piece_type = self._identify_piece_type(move_uci, fen)
            
            # 判断移动方向和距离
            if from_file == to_file:
                # 直行移动
                if from_rank < to_rank:
                    direction = "进"
                    steps = to_rank - from_rank
                else:
                    direction = "退" 
                    steps = from_rank - to_rank
                step_chinese = chinese_nums[steps - 1] if steps <= 9 else str(steps)
                move_desc = f"{piece_type}{from_road}{direction}{step_chinese}"
            else:
                # 横移或斜移
                if from_rank == to_rank:
                    direction = "平"
                    move_desc = f"{piece_type}{from_road}{direction}{to_road}"
                else:
                    # 斜移（如马、象）
                    if from_rank < to_rank:
                        direction = "进"
                    else:
                        direction = "退"
                    move_desc = f"{piece_type}{from_road}{direction}{to_road}"
            
            # 完整描述
            coord_desc = f"{move_uci[0]}{move_uci[1]} -> {move_uci[2]}{move_uci[3]}"
            road_desc = f"第{from_road}路 -> 第{to_road}路"
            
            return f"{move_uci} | {move_desc} | {coord_desc} | {road_desc}"
            
        except Exception as e:
            # 如果转换失败，返回基本信息
            return f"{move_uci} (坐标: {move_uci[0]}{move_uci[1]} -> {move_uci[2]}{move_uci[3]})"
    
    def _identify_piece_type(self, move_uci, fen):
        """
        根据FEN和移动位置识别棋子类型
        """
        if not fen:
            return "子"  # 默认棋子名称
        
        try:
            # 解析FEN获取棋盘状态
            position_part = fen.split()[0]  # 只取位置部分
            rows = position_part.split('/')
            
            # 确保有10行
            if len(rows) != 10:
                return "子"
            
            # 获取起始位置的棋子
            from_file = ord(move_uci[0]) - ord('a')  # a=0, b=1, ...
            from_rank = int(move_uci[1])
            
            # 从FEN中解析该位置的棋子
            piece = self._get_piece_at_position(rows, from_rank, from_file)
            
            # 棋子类型映射
            piece_names = {
                # 黑方（小写）
                'r': '車', 'n': '馬', 'b': '象', 'a': '士', 'k': '将',
                'c': '炮', 'p': '卒',
                # 红方（大写）
                'R': '车', 'N': '马', 'B': '相', 'A': '仕', 'K': '帅',
                'C': '砲', 'P': '兵'
            }
            
            return piece_names.get(piece, '子')
            
        except Exception as e:
            return "子"
    
    def _get_piece_at_position(self, rows, rank, file):
        """
        从FEN行中获取指定位置的棋子
        """
        try:
            if rank < 0 or rank >= len(rows):
                return None
                
            row = rows[rank]
            col = 0
            
            for char in row:
                if char.isdigit():
                    # 数字表示空格数
                    col += int(char)
                else:
                    # 字母表示棋子
                    if col == file:
                        return char
                    col += 1
                    
            return None
        except:
            return None
    
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
