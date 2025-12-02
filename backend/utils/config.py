"""
配置管理模块
使用 pydantic-settings 加载环境变量
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """应用配置"""

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production-make-it-very-long-and-random"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24小时

    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/alpha-score.db"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# 全局配置实例
settings = Settings()
