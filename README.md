# 遥感目标检测平台 (RSOD Web Platform)

基于Vue3 + FastAPI + PyTorch的遥感目标检测Web平台

## 项目结构

```
rsod-web-platform/
├── frontend/          # Vue3前端项目
│   ├── src/
│   │   ├── views/    # 页面组件
│   │   ├── router/   # 路由配置
│   │   └── main.ts   # 入口文件
│   ├── Dockerfile
│   └── package.json
├── backend/           # FastAPI后端服务
│   ├── main.py       # API入口
│   ├── Dockerfile
│   └── requirements.txt
├── model/             # Python模型服务
│   ├── model_server.py  # 模型推理服务
│   ├── Dockerfile
│   └── requirements.txt
├── nginx/             # Nginx配置
│   └── nginx.conf
└── docker-compose.yml # Docker编排文件
```

## 快速开始

### 1. 环境要求

- Node.js >= 20.0.0
- Python >= 3.10
- Docker & Docker Compose
- (可选) NVIDIA GPU & CUDA

### 2. 安装依赖

#### 前端
```bash
cd frontend
pnpm install
```

#### 后端
```bash
cd backend
pip install -r requirements.txt
```

#### 模型服务
```bash
cd model
pip install -r requirements.txt
```

### 3. 启动服务

#### 开发模式

启动前端:
```bash
cd frontend
pnpm dev
```

启动后端:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

启动模型服务:
```bash
cd model
python model_server.py
```

#### Docker模式

一键启动所有服务:
```bash
docker-compose up -d
```

### 4. 访问服务

- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs
- 模型服务: http://localhost:5000

## 功能特性

- ✅ 遥感图像上传与管理
- ✅ 目标检测推理
- ✅ 检测结果可视化
- ✅ 多模型支持(YOLOv8, Faster R-CNN等)
- ✅ 批量检测
- ✅ 历史记录查询

## 技术栈

**前端**:
- Vue 3 + TypeScript
- Element Plus UI
- Vite
- Pinia状态管理

**后端**:
- FastAPI
- PostgreSQL
- Redis
- Celery任务队列

**模型服务**:
- PyTorch
- Ultralytics YOLO
- OpenCV
- Flask

## 开发指南

### 添加新模型

1. 在`model/`目录下添加模型代码
2. 更新`model_server.py`中的推理逻辑
3. 将模型权重放入`model/weights/`目录

### API接口

详见 http://localhost:8000/docs

## 部署

### 生产环境部署

```bash
docker-compose -f docker-compose.yml up -d --build
```

### 环境变量

创建`.env`文件:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/rsod_platform
REDIS_URL=redis://localhost:6379
MODEL_SERVICE_URL=http://localhost:5000
CUDA_VISIBLE_DEVICES=0
```

## 常见问题

### GPU加速

确保已安装NVIDIA Docker Toolkit:
```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### 模型权重下载

将训练好的模型权重文件放置在`model/weights/`目录下。

## 许可证

MIT License
