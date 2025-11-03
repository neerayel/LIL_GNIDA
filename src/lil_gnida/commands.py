import aiohttp
from config import settings
from telegram.ext import ContextTypes

async def execute_server_command(command: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    # Маппинг command -> URL или SSH-команда
    command_map = {
        "cmd_system_status": f"{settings.target_server_base_url}/api/status"
    }

    url = command_map.get(command)
    if not url:
        return "Неизвестная команда."

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, timeout=settings.request_timeout) as resp:
                if resp.status == 200:
                    return f"Команда выполнена\nОтвет сервера:\n{await resp.text()}"
                else:
                    return f"Ошибка на сервере. Код: {resp.status}"
    except Exception as e:
        return f"Не удалось соединиться с сервером: {e}"