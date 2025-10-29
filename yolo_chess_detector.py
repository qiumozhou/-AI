"""
基于YOLOv8的中国象棋棋子识别
需要预训练的YOLO模型或自行训练
"""

import cv2
import numpy as np
from pathlib import Path

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("YOLOv8未安装，请运行: pip install ultralytics")


class YOLOChessDetector:
    """
    使用YOLOv8检测中国象棋棋子
    """
    
    def __init__(self, model_path='models/chess_yolo.pt'):
        """
        初始化YOLO检测器
        model_path: 训练好的YOLO模型路径
        """
        self.model_path = model_path
        self.model = None
        self.class_names = [
            'red_rook', 'red_knight', 'red_bishop', 'red_advisor', 'red_king',
            'red_cannon', 'red_pawn',
            'black_rook', 'black_knight', 'black_bishop', 'black_advisor', 'black_king',
            'black_cannon', 'black_pawn'
        ]
        
        # FEN映射
        self.piece_to_fen = {
            'red_rook': 'R', 'red_knight': 'N', 'red_bishop': 'B',
            'red_advisor': 'A', 'red_king': 'K', 'red_cannon': 'C', 'red_pawn': 'P',
            'black_rook': 'r', 'black_knight': 'n', 'black_bishop': 'b',
            'black_advisor': 'a', 'black_king': 'k', 'black_cannon': 'c', 'black_pawn': 'p'
        }
        
        if YOLO_AVAILABLE and Path(model_path).exists():
            self.load_model()
    
    def load_model(self):
        """加载YOLO模型"""
        try:
            self.model = YOLO(self.model_path)
            print(f"✓ YOLO模型加载成功: {self.model_path}")
        except Exception as e:
            print(f"✗ YOLO模型加载失败: {e}")
            self.model = None
    
    def detect_pieces(self, image):
        """
        检测图像中的棋子
        返回: [(x, y, w, h, class_name, confidence), ...]
        """
        if not self.model:
            return []
        
        try:
            results = self.model(image, conf=0.5)  # 置信度阈值0.5
            
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().numpy()
                    cls = int(box.cls[0].cpu().numpy())
                    
                    class_name = self.class_names[cls] if cls < len(self.class_names) else 'unknown'
                    
                    detections.append({
                        'bbox': (int(x1), int(y1), int(x2-x1), int(y2-y1)),
                        'class': class_name,
                        'confidence': float(conf)
                    })
            
            return detections
        
        except Exception as e:
            print(f"检测失败: {e}")
            return []
    
    def detections_to_board(self, detections, board_width, board_height):
        """
        将检测结果转换为棋盘数组
        """
        # 创建9x10的棋盘
        board = [[None for _ in range(9)] for _ in range(10)]
        
        cell_width = board_width / 9
        cell_height = board_height / 10
        
        for det in detections:
            x, y, w, h = det['bbox']
            # 计算棋子中心在哪个格子
            center_x = x + w // 2
            center_y = y + h // 2
            
            col = int(center_x / cell_width)
            row = int(center_y / cell_height)
            
            # 确保在棋盘范围内
            if 0 <= row < 10 and 0 <= col < 9:
                fen_piece = self.piece_to_fen.get(det['class'])
                if fen_piece:
                    board[row][col] = fen_piece
        
        return board
    
    def board_to_fen(self, board):
        """将棋盘数组转换为FEN"""
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
    
    def recognize_from_image(self, image):
        """
        从图像识别棋局并返回FEN
        """
        if not self.model:
            return None
        
        h, w = image.shape[:2]
        
        # 检测棋子
        detections = self.detect_pieces(image)
        
        if not detections:
            print("未检测到任何棋子")
            return None
        
        print(f"检测到 {len(detections)} 个棋子")
        
        # 转换为棋盘
        board = self.detections_to_board(detections, w, h)
        
        # 转换为FEN
        fen = self.board_to_fen(board)
        
        return fen


def train_yolo_model():
    """
    训练YOLOv8模型的示例代码
    需要准备标注好的数据集
    """
    print("""
    训练YOLOv8模型步骤:
    
    1. 准备数据集
       - 收集大量中国象棋棋盘图片
       - 使用LabelImg或Roboflow标注棋子
       - 数据格式: YOLO格式
    
    2. 安装依赖
       pip install ultralytics
    
    3. 训练模型
       from ultralytics import YOLO
       
       # 加载预训练模型
       model = YOLO('yolov8n.pt')  # nano模型，速度快
       
       # 训练
       results = model.train(
           data='chess_data.yaml',  # 数据集配置文件
           epochs=100,
           imgsz=640,
           batch=16,
           name='chess_detector'
       )
    
    4. 使用模型
       detector = YOLOChessDetector('runs/detect/chess_detector/weights/best.pt')
       fen = detector.recognize_from_image(image)
    
    数据集示例结构:
    dataset/
    ├── images/
    │   ├── train/
    │   └── val/
    ├── labels/
    │   ├── train/
    │   └── val/
    └── chess_data.yaml
    """)


if __name__ == "__main__":
    if not YOLO_AVAILABLE:
        print("请先安装YOLOv8: pip install ultralytics")
        print("\n查看训练指南:")
        train_yolo_model()
    else:
        print("YOLOv8已安装！")
        print("请准备训练数据或下载预训练模型")

