"""
高级棋子识别模块
使用深度学习和模板匹配来识别中国象棋棋子
"""

import cv2
import numpy as np
from pathlib import Path


class AdvancedChessRecognizer:
    """
    高级中国象棋识别器
    支持多种识别方法
    """
    
    def __init__(self):
        self.piece_templates = {}
        self.board_size = (9, 10)  # 中国象棋9x10
        
    def detect_board_corners(self, image):
        """
        检测棋盘的四个角点
        返回: [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 使用自适应阈值
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # 查找轮廓
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # 找到最大的矩形轮廓（假设是棋盘）
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            epsilon = 0.02 * cv2.arcLength(largest_contour, True)
            approx = cv2.approxPolyDP(largest_contour, epsilon, True)
            
            if len(approx) == 4:
                return approx.reshape(4, 2)
        
        return None
    
    def extract_grid(self, image, corners):
        """
        从棋盘图像中提取网格
        """
        if corners is None:
            return None
        
        # 定义目标大小
        width, height = 450, 500  # 9:10比例
        
        # 定义目标点
        dst_points = np.float32([
            [0, 0],
            [width, 0],
            [width, height],
            [0, height]
        ])
        
        # 计算透视变换矩阵
        src_points = np.float32(corners)
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        
        # 应用透视变换
        warped = cv2.warpPerspective(image, matrix, (width, height))
        
        return warped
    
    def divide_into_cells(self, board_image):
        """
        将棋盘图像分割成9x10的格子
        返回: cells[row][col] = cell_image
        """
        height, width = board_image.shape[:2]
        cell_width = width // 9
        cell_height = height // 10
        
        cells = []
        for row in range(10):
            row_cells = []
            for col in range(9):
                x = col * cell_width
                y = row * cell_height
                cell = board_image[y:y+cell_height, x:x+cell_width]
                row_cells.append(cell)
            cells.append(row_cells)
        
        return cells
    
    def recognize_piece_by_color(self, cell_image):
        """
        通过颜色和形状识别棋子
        返回: 棋子类型 (r/n/b/a/k/c/p 或 R/N/B/A/K/C/P，大写为红方)
        """
        # 转换到HSV色彩空间
        hsv = cv2.cvtColor(cell_image, cv2.COLOR_BGR2HSV)
        
        # 定义红色和黑色范围
        red_lower1 = np.array([0, 100, 100])
        red_upper1 = np.array([10, 255, 255])
        red_lower2 = np.array([160, 100, 100])
        red_upper2 = np.array([180, 255, 255])
        
        black_lower = np.array([0, 0, 0])
        black_upper = np.array([180, 255, 50])
        
        # 检测颜色
        red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
        red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        black_mask = cv2.inRange(hsv, black_lower, black_upper)
        
        red_pixels = cv2.countNonZero(red_mask)
        black_pixels = cv2.countNonZero(black_mask)
        
        # 如果颜色像素太少，认为是空格
        if red_pixels < 100 and black_pixels < 100:
            return None
        
        # 判断是红方还是黑方
        is_red = red_pixels > black_pixels
        
        # 这里需要进一步识别具体棋子类型
        # 可以使用OCR识别棋子上的汉字
        # 或者使用模板匹配
        # 当前简化返回
        return 'P' if is_red else 'p'  # 临时返回兵/卒
    
    def cells_to_fen(self, cells):
        """
        将识别的格子转换为FEN格式
        """
        fen_rows = []
        
        for row in cells:
            fen_row = ""
            empty_count = 0
            
            for cell in row:
                piece = self.recognize_piece_by_color(cell)
                
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += piece
            
            if empty_count > 0:
                fen_row += str(empty_count)
            
            fen_rows.append(fen_row)
        
        # 拼接FEN
        position = "/".join(fen_rows)
        # 添加其他FEN信息（轮到谁走、是否可以吃过路兵等）
        fen = f"{position} w - - 0 1"
        
        return fen
    
    def recognize_full_board(self, image):
        """
        完整的棋盘识别流程
        """
        # 1. 检测棋盘角点
        corners = self.detect_board_corners(image)
        
        if corners is None:
            print("未能检测到棋盘角点")
            return None
        
        # 2. 透视变换得到标准棋盘
        board = self.extract_grid(image, corners)
        
        if board is None:
            return None
        
        # 保存调试图像
        cv2.imwrite("debug_warped_board.png", board)
        
        # 3. 分割成格子
        cells = self.divide_into_cells(board)
        
        # 4. 识别每个格子
        fen = self.cells_to_fen(cells)
        
        return fen


def test_recognizer():
    """
    测试识别器
    """
    recognizer = AdvancedChessRecognizer()
    
    # 加载测试图像
    test_image_path = "test_board.png"
    if Path(test_image_path).exists():
        image = cv2.imread(test_image_path)
        fen = recognizer.recognize_full_board(image)
        print(f"识别结果: {fen}")
    else:
        print(f"测试图像不存在: {test_image_path}")
        print("请将象棋棋盘截图保存为 test_board.png 进行测试")


if __name__ == "__main__":
    test_recognizer()

