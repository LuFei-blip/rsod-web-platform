from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.api.detection import router as detection_router
from app.utils.file_utils import ensure_directories

# 确保必要目录存在
ensure_directories()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="遥感目标检测平台后端API"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件服务
uploads_dir = os.path.join(settings.BASE_DIR, "static", "uploads")
results_dir = os.path.join(settings.BASE_DIR, "static", "results")

if os.path.exists(uploads_dir):
    app.mount("/static/uploads", StaticFiles(directory=uploads_dir), name="uploads")
if os.path.exists(results_dir):
    app.mount("/static/results", StaticFiles(directory=results_dir), name="results")

# 注册路由
app.include_router(detection_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
