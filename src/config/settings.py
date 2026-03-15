from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DEEPSEEK_API_KEY: str
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL_NAME: str = "deepseek-chat"
    API_TIMEOUT: int = 120
    API_MAX_RETRIES: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings