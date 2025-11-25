from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    telegram_bot_token: str = ""
    allowed_user_ids: List[int] = []
    
    inline_cache_time: int = 10
    
    target_server_base_url: str = "http://localhost:8080"
    ollama_server_base_url: str = "http://localhost:8080"

    request_timeout: int = 30

    ollama_inline_model: str = ""
    ollama_chat_model: str = ""

    ollama_chat_input_json_path: str = "./data/LLM_CHAT_INPUT_DATA.json"
    ollama_single_input_json_path: str = "./data/LLM_SINGLE_INPUT_DATA.json"
    llm_response_path: str = "./data/LLM_RESPONSE_FOR_TTS.txt"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Создаем экземпляр настроек
settings = Settings()