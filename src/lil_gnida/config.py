from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    telegram_bot_token: str
    allowed_user_ids: int
    
    target_server_base_url: str = "http://localhost:8080"
    request_timeout: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Создаем экземпляр настроек
settings = Settings()