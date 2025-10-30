"""
基于深度学习的中国象棋识别器
使用预训练的 ONNX 模型
项目来源: https://github.com/TheOne1006/chinese-chess-recognition
"""

import sys
import cv2
import numpy as np
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

try:
    import onnxruntime as ort
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False
    print("请安装 onnxruntime: pip install onnxruntime")


class CChessDeepRecognizer:
    """
    中国象棋深度学习识别器
    使用两步识别：1) 棋盘关键点检测 2) 棋子分类
    """
    
    def __init__(self, models_dir='models/cchess_recognition'):
        """
        初始化识别器
        
        Args:
            models_dir: 模型文件目录
        """
        self.models_dir = Path(models_dir)
        
        # 棋子类别映射（16类）
        self.piece_map = {
            '.': '.',      # 空位
            'x': 'x',      # 其他
            'K': 'K',      # 红帅
            'A': 'A',      # 红仕
            'B': 'B',      # 红相
            'N': 'N',      # 红马
            'R': 'R',      # 红车
            'C': 'C',      # 红炮
            'P': 'P',      # 红兵
            'k': 'k',      # 黑将
            'a': 'a',      # 黑士
            'b': 'b',      # 黑象
            'n': 'n',      # 黑马
            'r': 'r',      # 黑车
            'c': 'c',      # 黑炮
            'p': 'p',      # 黑卒
        }
        
        self.class_names = [
            'point', 'other', 
            'red_king', 'red_advisor', 'red_bishop', 'red_knight', 'red_rook', 'red_cannon', 'red_pawn',
            'black_king', 'black_advisor', 'black_bishop', 'black_knight', 'black_rook', 'black_cannon', 'black_pawn'
        ]
        
        self.class_to_fen = {
            'point': '.', 'other': 'x',
            'red_king': 'K', 'red_advisor': 'A', 'red_bishop': 'B', 'red_knight': 'N', 
            'red_rook': 'R', 'red_cannon': 'C', 'red_pawn': 'P',
            'black_king': 'k', 'black_advisor': 'a', 'black_bishop': 'b', 'black_knight': 'n',
            'black_rook': 'r', 'black_cannon': 'c', 'black_pawn': 'p'
        }
        
        self.pose_model = None
        self.classifier_model = None
        
        self.load_models()
    
    def load_models(self):
        """加载ONNX模型"""
        if not ONNX_AVAILABLE:
            print("⚠ ONNX Runtime 未安装，无法加载模型")
            return False
        
        # 检查模型文件
        # 注意：文件名和功能实际是反的！
        # rtmpose实际上是分类模型，swinv2实际上是关键点检测模型
        pose_model_path = self.models_dir / 'swinv2-nano_cchess16.onnx'  # 关键点检测
        classifier_model_path = self.models_dir / 'rtmpose-t-cchess_4.onnx'  # 棋子分类
        
        if not pose_model_path.exists():
            print(f"⚠ 棋盘检测模型不存在: {pose_model_path}")
            print("请运行: python download_cchess_models.py")
            return False
        
        if not classifier_model_path.exists():
            print(f"⚠ 棋子分类模型不存在: {classifier_model_path}")
            print("请运行: python download_cchess_models.py")
            return False
        
        try:
            # 加载模型
            print("正在加载棋盘检测模型...")
            self.pose_model = ort.InferenceSession(str(pose_model_path))
            
            # 打印模型输入输出信息
            print(f"  输入: {[(inp.name, inp.shape) for inp in self.pose_model.get_inputs()]}")
            print(f"  输出: {[(out.name, out.shape) for out in self.pose_model.get_outputs()]}")
            print("✓ 棋盘检测模型加载成功")
            
            print("正在加载棋子分类模型...")
            self.classifier_model = ort.InferenceSession(str(classifier_model_path))
            print(f"  输入: {[(inp.name, inp.shape) for inp in self.classifier_model.get_inputs()]}")
            print(f"  输出: {[(out.name, out.shape) for out in self.classifier_model.get_outputs()]}")
            print("✓ 棋子分类模型加载成功")
            
            return True
            
        except Exception as e:
            print(f"✗ 模型加载失败: {e}")
            return False
    
    def recognize(self, image):
        """
        识别棋盘
        
        Args:
            image: 输入图像 (numpy array)
        
        Returns:
            FEN字符串
        """
        if self.pose_model is None or self.classifier_model is None:
            print("模型未加载")
            return None
        
        try:
            # 步骤1: 检测棋盘关键点
            print("步骤1: 检测棋盘关键点...")
            keypoints = self.detect_keypoints(image)
            
            if keypoints is None:
                print("未检测到棋盘")
                return None
            
            # 步骤2: 透视变换对齐棋盘
            print("步骤2: 对齐棋盘...")
            aligned_board = self.align_board(image, keypoints)
            
            if aligned_board is None:
                print("棋盘对齐失败")
                return None
            
            # 步骤3: 识别棋子
            print("步骤3: 识别棋子...")
            fen = self.classify_pieces(aligned_board)
            
            return fen
            
        except Exception as e:
            print(f"识别失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def preprocess_pose_image(self, image):
        """预处理图像用于关键点检测"""
        # 调整大小到模型输入尺寸
        img = cv2.resize(image, (256, 256))  # 模型需要256x256
        
        # 归一化
        img = img.astype(np.float32) / 255.0
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        img = (img - mean) / std
        
        # 调整维度 (H,W,C) -> (C,H,W)
        img = np.transpose(img, (2, 0, 1))
        
        # 添加batch维度
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def detect_keypoints(self, image):
        """检测棋盘4个角点"""
        try:
            # 预处理图像
            input_tensor = self.preprocess_pose_image(image)
            
            # 运行推理
            input_name = self.pose_model.get_inputs()[0].name
            outputs = self.pose_model.run(None, {input_name: input_tensor})
            
            # 调试：打印输出信息
            print(f"  模型输出数量: {len(outputs)}")
            for i, output in enumerate(outputs):
                print(f"  输出{i}: shape={output.shape}, dtype={output.dtype}")
            
            # 解析输出 - RTMPose输出格式
            # outputs[0]: simcc_x, outputs[1]: simcc_y
            if len(outputs) < 2:
                print(f"✗ 模型输出格式异常，期望至少2个输出，实际: {len(outputs)}")
                return None
            
            simcc_x, simcc_y = outputs[0][0], outputs[1][0]
            
            # 获取4个关键点的坐标
            keypoints = []
            for i in range(4):  # 4个角点
                x_coord = np.argmax(simcc_x[i])
                y_coord = np.argmax(simcc_y[i])
                
                # 将坐标映射回原图
                x = int(x_coord * image.shape[1] / simcc_x.shape[1])
                y = int(y_coord * image.shape[0] / simcc_y.shape[1])
                
                keypoints.append([x, y])
            
            keypoints = np.array(keypoints, dtype=np.float32)
            print(f"✓ 检测到4个角点: {keypoints.tolist()}")
            
            return keypoints
            
        except Exception as e:
            print(f"✗ 关键点检测失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def align_board(self, image, keypoints):
        """透视变换对齐棋盘"""
        try:
            # 目标尺寸：标准俯视棋盘
            target_width = 400
            target_height = 450  # 保持9:10比例
            
            # 定义目标点（俯视图的四个角）
            dst_points = np.array([
                [0, 0],                      # 左上 (黑方左角)
                [target_width, 0],           # 右上 (黑方右角)
                [target_width, target_height], # 右下 (红方右角)
                [0, target_height]           # 左下 (红方左角)
            ], dtype=np.float32)
            
            # 对关键点进行排序：按照左上、右上、右下、左下的顺序
            # 首先按y坐标排序，分出上下两组
            points = keypoints.copy()
            points_sorted_y = points[np.argsort(points[:, 1])]
            
            # 上面两个点（y较小）
            top_points = points_sorted_y[:2]
            # 下面两个点（y较大）
            bottom_points = points_sorted_y[2:]
            
            # 在每组内按x坐标排序
            top_points = top_points[np.argsort(top_points[:, 0])]  # 左上、右上
            bottom_points = bottom_points[np.argsort(bottom_points[:, 0])]  # 左下、右下
            
            # 组合成正确的顺序：左上、右上、右下、左下
            src_points = np.array([
                top_points[0],      # 左上
                top_points[1],      # 右上
                bottom_points[1],   # 右下
                bottom_points[0]    # 左下
            ], dtype=np.float32)
            
            print(f"  排序后的角点:")
            print(f"    左上: {src_points[0]}")
            print(f"    右上: {src_points[1]}")
            print(f"    右下: {src_points[2]}")
            print(f"    左下: {src_points[3]}")
            
            # 计算透视变换矩阵
            matrix = cv2.getPerspectiveTransform(src_points, dst_points)
            
            # 应用透视变换
            aligned = cv2.warpPerspective(image, matrix, (target_width, target_height))
            
            print(f"✓ 棋盘对齐完成，尺寸: {aligned.shape}")
            
            # 保存调试图像
            cv2.imwrite("debug_aligned_board.png", aligned)
            print("  调试图像已保存: debug_aligned_board.png")
            
            return aligned
            
        except Exception as e:
            print(f"✗ 棋盘对齐失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def preprocess_classifier_image(self, aligned_board):
        """预处理对齐的棋盘图像用于分类"""
        # Swin Transformer输入尺寸
        target_size = (280, 315)  # (width, height)
        
        # Resize
        img = cv2.resize(aligned_board, target_size)
        
        # BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # 归一化 - ImageNet标准
        mean = np.array([123.675, 116.28, 103.53], dtype=np.float32)
        std = np.array([58.395, 57.12, 57.375], dtype=np.float32)
        img = (img - mean) / std
        
        img = img.astype(np.float32)
        
        # 调整维度 (H,W,C) -> (C,H,W)
        img = np.transpose(img, (2, 0, 1))
        
        # 添加batch维度
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def classify_pieces(self, aligned_board):
        """识别棋子并返回FEN"""
        try:
            # 预处理图像
            input_tensor = self.preprocess_classifier_image(aligned_board)
            
            # 运行推理
            input_name = self.classifier_model.get_inputs()[0].name
            outputs = self.classifier_model.run(None, {input_name: input_tensor})
            
            # 解析输出 - shape: (1, 90, 16)
            # 90个位置 (10行×9列)，每个位置16类
            predictions = outputs[0][0]  # shape: (90, 16)
            
            # 获取每个位置的最高概率类别
            class_indices = np.argmax(predictions, axis=1)  # shape: (90,)
            confidences = np.max(predictions, axis=1)  # shape: (90,)
            
            # 将类别索引转换为FEN字符
            fen_chars = []
            for i in range(90):
                class_idx = class_indices[i]
                conf = confidences[i]
                class_name = self.class_names[class_idx]
                fen_char = self.class_to_fen[class_name]
                fen_chars.append(fen_char)
            
            # 生成FEN字符串
            fen_rows = []
            for row in range(10):
                row_chars = fen_chars[row*9:(row+1)*9]
                row_fen = self.compress_fen_row(row_chars)
                fen_rows.append(row_fen)
            
            fen = '/'.join(fen_rows) + ' w - - 0 1'
            
            # 统计识别情况
            recognized = sum(1 for c in fen_chars if c not in ['.', 'x'])
            avg_conf = np.mean(confidences)
            print(f"✓ 识别完成: {recognized}/32 个棋子")
            print(f"  平均置信度: {avg_conf:.2%}")
            
            return fen
            
        except Exception as e:
            print(f"✗ 棋子分类失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def compress_fen_row(self, row_chars):
        """压缩FEN行表示（连续空格用数字表示）"""
        result = []
        empty_count = 0
        
        for char in row_chars:
            if char in ['.', 'x']:  # 空位
                empty_count += 1
            else:  # 棋子
                if empty_count > 0:
                    result.append(str(empty_count))
                    empty_count = 0
                result.append(char)
        
        # 处理行尾的空位
        if empty_count > 0:
            result.append(str(empty_count))
        
        # 如果整行为空
        if not result:
            return '9'
        
        return ''.join(result)


def test_recognition():
    """测试识别功能"""
    recognizer = CChessDeepRecognizer()
    
    if recognizer.pose_model is None:
        print("\n" + "="*60)
        print("模型文件缺失！")
        print("="*60)
        print("\n请按以下步骤操作：")
        print("\n1. 下载模型文件：")
        print("   访问: https://huggingface.co/spaces/yolo12138/Chinese_Chess_Recognition/tree/main/onnx")
        print("   下载以下两个文件到 models/cchess_recognition/ 目录：")
        print("   - rtmpose-t-cchess_4.onnx")
        print("   - swinv2-nano_cchess16.onnx")
        print("\n2. 或使用原项目的完整环境：")
        print("   cd chess_recognition_model")
        print("   pip install -e .")
        print("\n" + "="*60)
        return
    
    # 测试图片
    test_image = "images/1.png"
    if not Path(test_image).exists():
        print(f"测试图片不存在: {test_image}")
        return
    
    image = cv2.imread(test_image)
    fen = recognizer.recognize(image)
    
    if fen:
        print(f"\n✓ 识别成功！")
        print(f"FEN: {fen}")
    else:
        print("\n✗ 识别失败")


if __name__ == "__main__":
    print("="*60)
    print("中国象棋深度学习识别器")
    print("基于: https://github.com/TheOne1006/chinese-chess-recognition")
    print("="*60)
    print()
    
    test_recognition()

