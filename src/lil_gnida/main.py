import logging
import asyncio
from typing import NoReturn

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, InlineQueryHandler
from telegram.error import TelegramError

# Импортируем наши модули
from config import settings
from handlers import start, button_click_handler, inline_interaction_handler


def setup_logging() -> None:
    """Настройка структурированного логирования"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler('bot.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    # Уменьшаем логирование от некоторых библиотек
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)


def create_application() -> Application:
    """
    Фабрика для создания и настройки экземпляра Application.
    
    Returns:
        Application: Настроенное приложение бота
    """
    # Создаем Application с persistence (если нужно сохранять данные между перезапусками)
    application = Application.builder().token(settings.telegram_bot_token).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    
    # Добавляем обработчик нажатий на кнопки
    application.add_handler(CallbackQueryHandler(button_click_handler))

    application.add_handler(InlineQueryHandler(inline_interaction_handler))
    
    # Добавляем обработчик ошибок
    # application.add_error_handler(error_handler)
    
    # Сохраняем настройки в bot_data для доступа из handlers
    application.bot_data["settings"] = settings
    application.bot_data["logger"] = logging.getLogger(__name__)
    
    return application


if __name__ == "__main__":
    """Основная асинхронная функция запуска бота"""
    # Настройка логирования
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Запуск инициализации Telegram бота...")
    
    try:
        # Создаем и настраиваем приложение
        application = create_application()

        logger.info("Бот успешно инициализирован. Запускаем polling...")
        # logger.info(f"Разрешены пользователи: {settings.allowed_user_ids}")
        # logger.info(f"Целевой сервер: {settings.target_server_base_url}")

        application.run_polling(
            allowed_updates=['message', 'callback_query', 'inline_query'],
            drop_pending_updates=True,  # Игнорируем сообщения, пришедшие пока бот был оффлайн
            close_loop=False  # Не закрываем event loop при остановке
        )
        
    except TelegramError as e:
        logger.error(f"Ошибка Telegram API: {e}")
        raise
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске бота: {e}")
        raise
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Бот остановлен пользователем (Ctrl+C)")
    except Exception as e:
        logging.getLogger(__name__).critical(f"Бот аварийно завершил работу: {e}")
        exit(1)

