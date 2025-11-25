import aiohttp
import logging
from config import settings
from telegram.ext import ContextTypes


logger = logging.getLogger(__name__)

# Маппинг command -> URL или SSH-команда
command_map = {
    "cmd_system_status": f"{settings.target_server_base_url}/api/status"
}

message: str

async def execute_server_command(command: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    url = command_map.get(command)
    if not url:
        message = "Неизвестная команда"
        logger.info(message)
        return message

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, timeout=settings.request_timeout) as resp:
                if resp.status == 200:
                    message = "Команда выполнена. Ответ сервера:"
                    text = await resp.text()
                    logger.info(message + text)
                    return message + "\n" + text
                else:
                    message = "Ошибка на сервере. Код: " + resp.status
                    logger.error(message)
                    return message
    except Exception as e:
        message = "Не удалось соединиться с сервером: " + e
        logger.error(message)
        return message