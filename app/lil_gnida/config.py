from pydantic_settings import BaseSettings
from typing import List

import logging

class Settings(BaseSettings):
    telegram_bot_token: str = ""
    allowed_user_ids: List[int] = []
    
    inline_cache_time: int = 10
    
    target_server: List[str] = ["http://localhost","8080"]
    ollama_server: List[str] = ["http://localhost","11434"]
    redis_server: List[str] = ["http://localhost","6379"]

    request_timeout: int = 30

    llm_list: List[str] = ["gemma3:1b"]

    ollama_inline_model: str = "gemma3:1b" # сделать установку индивидуально для юзера
    ollama_chat_model: str = "gemma3:1b" # сделать установку индивидуально для юзера
    llm_creativity: float = 0. # сделать установку индивидуально для юзера

    ollama_chat_input_json_path: str = "./data/LLM_CHAT_INPUT_DATA.json"
    ollama_single_input_json_path: str = "./data/LLM_SINGLE_INPUT_DATA.json"
    llm_response_path: str = "./data/LLM_RESPONSE_FOR_TTS.txt"

    start_message_path: str = "./data/START_MESSAGE.txt"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def convert_server(server: List[str]) -> dict[str,str]:
        return {"host":server[0], "port":server[1]}


# Создаем экземпляр настроек
settings = Settings()
settings.target_server = convert_server(settings.target_server)
settings.ollama_server = convert_server(settings.ollama_server)
settings.redis_server = convert_server(settings.redis_server)


def setup_logging() -> None:
    """Настройка логирования"""
    logging.basicConfig(
        format='%(asctime)s\t||\t%(name)s\t||\t%(levelname)s\t||\t%(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler('./app/bot.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    # Уменьшаем логирование от некоторых библиотек
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
