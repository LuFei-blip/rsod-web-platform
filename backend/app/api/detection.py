import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime
from typing import List

from app.services.detection_service import detection_service
from app.utils.file_utils import save_upload_file, ensure_directories
from app.config import settings
from app.models.schemas import (
    SingleDetectionResponse, HistoryResponse, HistoryItem,
    TargetListResponse, TargetItem, DetectionResult
)

router = APIRouter(prefix="/detection", tags=["detection"])

# 确保目录存在
ensure_directories()

# 模拟历史记录存储
_history_store: List[HistoryItem] = []


@router.post("/single", response_model=SingleDetectionResponse)
async def detect_single_image(
    file: UploadFile = File(...),
    model_name: str = Form("pest-v1")
):
    """单图检测接口"""
    try:
        # 保存上传文件
        filename = await save_upload_file(file, settings.UPLOAD_DIR)
        image_path = os.path.join(settings.UPLOAD_DIR, filename)

        # 执行检测
        result = detection_service.detect_single_image(image_path, model_name)

        # 保存历史记录
        _history_store.append(HistoryItem(
            id=result.detection_id,
            image_url=result.image_url,
            result_image_url=result.result_image_url,
            total_objects=result.total_objects,
            created_at=result.created_at,
            model_name=result.model_name
        ))

        return SingleDetectionResponse(
            success=True,
            message="检测成功",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")


@router.get("/history", response_model=HistoryResponse)
async def get_detection_history(
    page: int = 1,
    limit: int = 10
):
    """获取检测历史记录"""
    try:
        # 按时间倒序
        sorted_history = sorted(_history_store, key=lambda x: x.created_at, reverse=True)
        total = len(sorted_history)
        start = (page - 1) * limit
        end = start + limit
        page_data = sorted_history[start:end]

        return HistoryResponse(
            success=True,
            message="获取成功",
            data=page_data,
            total=total
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")


@router.get("/detail/{detection_id}", response_model=SingleDetectionResponse)
async def get_detection_detail(detection_id: str):
    """获取检测详情"""
    try:
        for item in _history_store:
            if item.id == detection_id:
                return SingleDetectionResponse(
                    success=True,
                    message="获取成功",
                    data=DetectionResult(
                        detection_id=item.id,
                        image_url=item.image_url,
                        result_image_url=item.result_image_url,
                        boxes=[],
                        total_objects=item.total_objects,
                        detection_time=0,
                        model_name=item.model_name,
                        created_at=item.created_at
                    )
                )
        return SingleDetectionResponse(
            success=False,
            message="未找到该检测记录",
            data=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取详情失败: {str(e)}")


@router.get("/targets/list", response_model=TargetListResponse)
async def get_target_list():
    """获取目标类型列表"""
    targets = [
        TargetItem(id=0, name="airplane", chinese_name="飞机", description="固定翼飞机、直升机等航空器"),
        TargetItem(id=1, name="oil_tank", chinese_name="油罐", description="储油罐、化工罐等容器"),
        TargetItem(id=2, name="playground", chinese_name="操场", description="运动场、操场等场地"),
        TargetItem(id=3, name="building", chinese_name="建筑物", description="各类建筑物"),
        TargetItem(id=4, name="ship", chinese_name="船舶", description="各类船舶"),
        TargetItem(id=5, name="pest", chinese_name="农业虫害", description="农作物病虫害"),
    ]
    return TargetListResponse(
        success=True,
        message="获取成功",
        data=targets
    )
