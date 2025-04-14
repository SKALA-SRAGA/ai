from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API 설정
    PROJECT_NAME: str = "Receipt Processing API"

    # 파일 저장 경로
    TEMP_DIR: Path = Path("temp_images")
    OUTPUT_DIR: Path = Path("output")

    # LLM 설정
    OPENAI_API_KEY: Optional[str] = None
    EXCHANGE_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# 필요한 디렉토리 생성
settings.TEMP_DIR.mkdir(exist_ok=True)
settings.OUTPUT_DIR.mkdir(exist_ok=True)
