import os
import uuid
from fastapi import UploadFile
from app.config import settings


def ensure_directories():
    """确保必要的目录存在"""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.RESULT_DIR, exist_ok=True)


def get_file_url(filename: str, directory: str) -> str:
    """获取文件访问URL"""
    return f"/{directory}/{filename}"


async def save_upload_file(file: UploadFile, upload_dir: str) -> str:
    """保存上传的文件"""
    # 生成唯一文件名
    ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    filename = f"temp_{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(upload_dir, filename)

    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)

    return filename
