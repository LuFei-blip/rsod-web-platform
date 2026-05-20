import os
import time
import uuid
from datetime import datetime
from typing import List, Dict, Any
from PIL import Image
import cv2
import numpy as np

from app.config import settings
from app.models.schemas import DetectionBox, DetectionResult
from app.utils.file_utils import get_file_url


class DetectionService:
    def __init__(self):
        self.model = None
        self.class_names = {}
        self._load_model()
        self._init_class_names()

    def _load_model(self):
        """加载YOLO模型"""
        try:
            from ultralytics import YOLO
            if os.path.exists(settings.YOLO_MODEL_PATH):
                self.model = YOLO(settings.YOLO_MODEL_PATH)
                print(f"模型加载成功: {settings.YOLO_MODEL_PATH}")
            else:
                print(f"警告: 模型文件未找到: {settings.YOLO_MODEL_PATH}，使用模拟模式")
                self.model = None
        except ImportError:
            print("警告: ultralytics未安装，使用模拟模式")
            self.model = None

    def _init_class_names(self):
        """初始化COCO类别名称"""
        self.class_names = {
            0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 4: "airplane",
            5: "bus", 6: "train", 7: "truck", 8: "boat", 9: "traffic light",
            10: "fire hydrant", 11: "stop sign", 12: "parking meter", 13: "bench",
            14: "bird", 15: "cat", 16: "dog", 17: "horse", 18: "sheep", 19: "cow",
            20: "elephant", 21: "bear", 22: "zebra", 23: "giraffe", 24: "backpack",
            25: "umbrella", 26: "handbag", 27: "tie", 28: "suitcase", 29: "frisbee",
            30: "skis", 31: "snowboard", 32: "sports ball", 33: "kite",
            34: "baseball bat", 35: "baseball glove", 36: "skateboard", 37: "surfboard",
            38: "tennis racket", 39: "bottle", 40: "wine glass", 41: "cup", 42: "fork",
            43: "knife", 44: "spoon", 45: "bowl", 46: "banana", 47: "apple",
            48: "sandwich", 49: "orange", 50: "broccoli", 51: "carrot", 52: "hot dog",
            53: "pizza", 54: "donut", 55: "cake", 56: "chair", 57: "couch",
            58: "potted plant", 59: "bed", 60: "dining table", 61: "toilet", 62: "tv",
            63: "laptop", 64: "mouse", 65: "remote", 66: "keyboard", 67: "cell phone",
            68: "microwave", 69: "oven", 70: "toaster", 71: "sink", 72: "refrigerator",
            73: "book", 74: "clock", 75: "vase", 76: "scissors", 77: "teddy bear",
            78: "hair drier", 79: "toothbrush",
            # 遥感目标类别
            80: "airplane_rs", 81: "oil_tank", 82: "playground", 83: "building",
            84: "ship", 85: "pest",
        }

    def detect_single_image(self, image_path: str, model_name: str = "pest-v1") -> DetectionResult:
        """单图检测"""
        start_time = time.time()
        detection_id = str(uuid.uuid4())

        if self.model is not None:
            # 真实检测
            results = self.model.predict(
                source=image_path,
                conf=settings.CONFIDENCE_THRESHOLD,
                iou=settings.IOU_THRESHOLD,
                save=False
            )

            boxes = []
            for result in results:
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        class_name = self.class_names.get(class_id, f"class_{class_id}")

                        boxes.append(DetectionBox(
                            x1=round(x1, 2),
                            y1=round(y1, 2),
                            x2=round(x2, 2),
                            y2=round(y2, 2),
                            confidence=round(confidence, 4),
                            class_id=class_id,
                            class_name=class_name
                        ))

            # 保存结果图片
            result_filename = f"result_{uuid.uuid4().hex}.jpg"
            result_path = os.path.join(settings.RESULT_DIR, result_filename)

            annotated_image = results[0].plot()
            cv2.imwrite(result_path, cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
        else:
            # 模拟模式
            boxes = self._mock_detect(image_path)
            result_filename = f"result_{uuid.uuid4().hex}.jpg"
            result_path = os.path.join(settings.RESULT_DIR, result_filename)

            # 创建模拟结果图片
            img = cv2.imread(image_path)
            if img is not None:
                for box in boxes:
                    cv2.rectangle(img, (int(box.x1), int(box.y1)), (int(box.x2), int(box.y2)), (0, 255, 0), 2)
                    cv2.putText(img, f"{box.class_name} {box.confidence:.2f}",
                                (int(box.x1), int(box.y1) - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.imwrite(result_path, img)
            else:
                # 如果原图无法读取，创建一个简单的结果图
                img = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(img, "Mock Detection Result", (150, 240),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imwrite(result_path, img)

        detection_time = time.time() - start_time
        image_filename = os.path.basename(image_path)

        return DetectionResult(
            detection_id=detection_id,
            image_url=get_file_url(image_filename, "uploads"),
            result_image_url=get_file_url(result_filename, "results"),
            boxes=boxes,
            total_objects=len(boxes),
            detection_time=round(detection_time, 3),
            model_name=model_name,
            created_at=datetime.now()
        )

    def _mock_detect(self, image_path: str) -> List[DetectionBox]:
        """模拟检测结果"""
        # 读取图片获取尺寸
        img = cv2.imread(image_path)
        if img is not None:
            h, w = img.shape[:2]
        else:
            h, w = 480, 640

        # 生成模拟目标
        import random
        num_objects = random.randint(1, 5)
        boxes = []
        classes = ["airplane_rs", "oil_tank", "building", "ship", "playground"]

        for i in range(num_objects):
            x1 = random.randint(50, w - 150)
            y1 = random.randint(50, h - 150)
            x2 = x1 + random.randint(50, 100)
            y2 = y1 + random.randint(50, 100)

            boxes.append(DetectionBox(
                x1=round(float(x1), 2),
                y1=round(float(y1), 2),
                x2=round(float(x2), 2),
                y2=round(float(y2), 2),
                confidence=round(random.uniform(0.7, 0.99), 4),
                class_id=80 + i,
                class_name=random.choice(classes)
            ))

        return boxes


# 单例
detection_service = DetectionService()
