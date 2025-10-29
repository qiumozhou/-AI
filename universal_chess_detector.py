"""
通用检测方案：不需要训练，直接使用预训练模型
使用圆形检测 + OCR识别汉字
"""

import cv2
import numpy as np
from pathlib import Path

# 检查依赖
try:
    from paddleocr import PaddleOCR
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("PaddleOCR未安装: pip install paddleocr")


class UniversalChessDetector:
    """
    通用中国象棋检测器
    使用OpenCV圆形检测 + PaddleOCR文字识别
    不需要专门训练的模型
    """
    
    def __init__(self):
        self.ocr = None
        self.piece_map = {
            # 红方（繁体和简体都支持）
            '车': 'R', '車': 'R',
            '马': 'N', '馬': 'N',
            '相': 'B',
            '仕': 'A',
            '帅': 'K', '帥': 'K',
            '炮': 'C', '砲': 'C',
            '兵': 'P',
            
            # 黑方
            '車': 'r',  # 黑车（繁体）
            '馬': 'n',  # 黑马
            '象': 'b',
            '士': 'a',
            '将': 'k', '將': 'k',
            '炮': 'c', '砲': 'c',
            '卒': 'p'
        }
        
        self.setup()
    
    def setup(self):
        """初始化OCR"""
        if OCR_AVAILABLE:
            try:
                # 初始化PaddleOCR（中文）
                self.ocr = PaddleOCR(
                    use_angle_cls=True,
                    lang='ch',
                    show_log=False
                )
                print("✓ OCR初始化成功")
            except Exception as e:
                print(f"OCR初始化失败: {e}")
                self.ocr = None
    
    def detect_circles(self, image):
        """
        检测圆形棋子位置
        返回: [(x, y, radius), ...]
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        
        # 使用霍夫圆检测
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=30,  # 最小距离
            param1=50,   # Canny边缘检测上阈值
            param2=30,   # 累加器阈值
            minRadius=15, # 最小半径
            maxRadius=60  # 最大半径
        )
        
        if circles is None:
            return []
        
        circles = np.uint16(np.around(circles))
        return [(int(x), int(y), int(r)) for x, y, r in circles[0, :]]
    
    def recognize_piece(self, image, x, y, radius):
        """
        识别单个棋子
        image: 原图
        x, y, radius: 棋子圆心和半径
        返回: FEN字符或None
        """
        if not self.ocr:
            return None
        
        # 提取棋子区域（放大一点以包含完整文字）
        r = int(radius * 1.2)
        x1 = max(0, x - r)
        y1 = max(0, y - r)
        x2 = min(image.shape[1], x + r)
        y2 = min(image.shape[0], y + r)
        
        piece_img = image[y1:y2, x1:x2]
        
        if piece_img.size == 0:
            return None
        
        try:
            # OCR识别
            result = self.ocr.ocr(piece_img, cls=True)
            
            if result and result[0]:
                for line in result[0]:
                    text = line[1][0]  # 识别的文字
                    conf = line[1][1]  # 置信度
                    
                    if conf > 0.5:  # 置信度阈值
                        # 匹配棋子
                        for char in text:
                            if char in self.piece_map:
                                return self.piece_map[char]
        
        except Exception as e:
            pass
        
        return None
    
    def detect_board_region(self, image):
        """
        检测棋盘区域
        返回: (x, y, w, h)
        """
        # 简化版：使用图像中心区域
        h, w = image.shape[:2]
        
        # 棋盘通常在中心
        margin_x = w // 6
        margin_y = h // 8
        
        return (margin_x, margin_y, w - 2*margin_x, h - 2*margin_y)
    
    def recognize_from_image(self, image):
        """
        从图像识别整个棋盘
        返回: FEN字符串
        """
        if not self.ocr:
            print("OCR未初始化")
            return None
        
        print("检测棋子位置...")
        
        # 检测棋盘区域
        board_x, board_y, board_w, board_h = self.detect_board_region(image)
        board_img = image[board_y:board_y+board_h, board_x:board_x+board_w]
        
        # 检测圆形棋子
        circles = self.detect_circles(board_img)
        
        if not circles:
            print("未检测到棋子")
            return None
        
        print(f"检测到 {len(circles)} 个圆形物体")
        
        # 创建棋盘数组
        board = [[None for _ in range(9)] for _ in range(10)]
        
        cell_w = board_w / 9
        cell_h = board_h / 10
        
        # 识别每个棋子
        for x, y, r in circles:
            # 计算在哪个格子
            col = int(x / cell_w)
            row = int(y / cell_h)
            
            if 0 <= row < 10 and 0 <= col < 9:
                # 识别棋子类型
                abs_x = board_x + x
                abs_y = board_y + y
                piece = self.recognize_piece(image, abs_x, abs_y, r)
                
                if piece:
                    board[row][col] = piece
                    print(f"  格子[{row},{col}]: {piece}")
        
        # 转换为FEN
        fen = self.board_to_fen(board)
        return fen
    
    def board_to_fen(self, board):
        """将棋盘转换为FEN"""
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
            
            if empty_count > 0:
                fen_row += str(empty_count)
            
            if not fen_row:
                fen_row = "9"
            
            fen_rows.append(fen_row)
        
        position = "/".join(fen_rows)
        fen = f"{position} w - - 0 1"
        
        return fen


# 测试函数
def test_detector():
    """测试检测器"""
    detector = UniversalChessDetector()
    
    if not detector.ocr:
        print("\n❌ OCR未安装或初始化失败")
        print("请安装: pip install paddleocr")
        return
    
    print("\n✓ 通用检测器已就绪！")
    print("\n使用方法:")
    print("1. 截取棋盘图片")
    print("2. detector.recognize_from_image(image)")
    print("3. 获得FEN格式")


if __name__ == "__main__":
    test_detector()

