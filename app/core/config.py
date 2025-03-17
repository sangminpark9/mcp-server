import os

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

from typing import Dict, List, Optional
from functools import lru_cache

class Settings(BaseSettings):
    # 기본 설정
    APP_NAME: str = "MCP Server"
    DEBUG: bool = True
    
    # API 설정
    API_PREFIX: str = "/api"
    
    # 모델 설정
    DEEPSEEK_MODEL_PATH: str = os.getenv("DEEPSEEK_MODEL_PATH", "./models/deepseek")
    LLAMA_MODEL_PATH: str = os.getenv("LLAMA_MODEL_PATH", "./models/llama")
    
    # 모델 라우팅 설정 - 특정 태스크에 따라 다른 모델 사용
    MODEL_ROUTING: Dict[str, str] = {
        "default": "deepseek",  # 기본 모델
        "translation": "llama",  # 번역 작업용 모델
        "korean": "llama",      # 한국어 처리용 모델
    }
    
    # 컨텍스트 관리 설정
    CONTEXT_STORAGE: str = os.getenv("CONTEXT_STORAGE", "memory")  # memory, redis, sqlite
    CONTEXT_TTL: int = 3600  # 컨텍스트 유지 시간(초)
    
    # 모델 추론 설정
    MAX_NEW_TOKENS: int = 2048
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.95
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
