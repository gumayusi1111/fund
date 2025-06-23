from pydantic_settings import BaseSettings
from typing import List, Optional, Dict
import os

class Settings(BaseSettings):
    """应用程序配置"""
    
    # 基础配置
    APP_NAME: str = "个人指数分析平台"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # API配置
    API_V1_STR: str = "/api/v1"
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    
    # 数据源配置
    AKSHARE_ENABLED: bool = True
    
    # 缓存配置
    CACHE_TTL: int = 300  # 5分钟缓存
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# 创建全局设置实例
settings = Settings() 