from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# 模拟模型加载
class DetectionModel:
    def __init__(self):
        self.loaded = False
    
    def load(self, model_path):
        """加载模型"""
        print(f"加载模型: {model_path}")
        self.loaded = True
    
    def predict(self, image):
        """执行推理"""
        # 这里应该调用真实的模型推理
        # 返回模拟的检测结果
        return {
            "detections": [
                {
                    "class": "airplane",
                    "confidence": 0.95,
                    "bbox": [100, 100, 200, 200]
                },
                {
                    "class": "ship",
                    "confidence": 0.88,
                    "bbox": [300, 300, 400, 400]
                }
            ],
            "image_size": image.size
        }

model = DetectionModel()

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model.loaded
    })

@app.route('/load_model', methods=['POST'])
def load_model():
    """加载模型"""
    data = request.json
    model_path = data.get('model_path', 'weights/best.pt')
    model.load(model_path)
    return jsonify({"message": "模型加载成功"})

@app.route('/detect', methods=['POST'])
def detect():
    """目标检测"""
    if 'image' not in request.files:
        return jsonify({"error": "未提供图像文件"}), 400
    
    file = request.files['image']
    image = Image.open(file.stream).convert('RGB')
    
    # 执行检测
    results = model.predict(image)
    
    return jsonify(results)

@app.route('/detect_batch', methods=['POST'])
def detect_batch():
    """批量目标检测"""
    data = request.json
    image_paths = data.get('image_paths', [])
    
    results = []
    for path in image_paths:
        if os.path.exists(path):
            image = Image.open(path).convert('RGB')
            result = model.predict(image)
            results.append({
                "image_path": path,
                "detections": result["detections"]
            })
    
    return jsonify({"results": results})

if __name__ == '__main__':
    # 启动时加载默认模型
    if os.path.exists('weights/best.pt'):
        model.load('weights/best.pt')
    
    app.run(host='0.0.0.0', port=5000, debug=True)
