from pydantic import BaseModel
from typing import List
import os


class Settings(BaseModel):
    APP_NAME: str = "RSOD Detection Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_DIR: str = "static"
    UPLOAD_DIR: str = "static/uploads"
    RESULT_DIR: str = "static/results"

    YOLO_MODEL_PATH: str = "yolo11n.pt"
    CONFIDENCE_THRESHOLD: float = 0.5
    IOU_THRESHOLD: float = 0.45

    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]


def get_settings() -> Settings:
    settings = Settings()

    env_file = os.path.join(settings.BASE_DIR, ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()
                        if hasattr(settings, key):
                            current_value = getattr(settings, key)
                            try:
                                if isinstance(current_value, bool):
                                    setattr(settings, key, value.lower() in ("true", "1", "yes"))
                                elif isinstance(current_value, int):
                                    setattr(settings, key, int(value))
                                elif isinstance(current_value, float):
                                    setattr(settings, key, float(value))
                                elif isinstance(current_value, list):
                                    setattr(settings, key, [v.strip() for v in value.split(",")])
                                else:
                                    setattr(settings, key, value)
                            except (ValueError, TypeError):
                                pass

    return settings


settings = get_settings()
