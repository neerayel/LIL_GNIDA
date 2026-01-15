from telegram.ext import Application, CommandHandler, CallbackQueryHandler, InlineQueryHandler, MessageHandler
from telegram.error import TelegramError

import logging
from config import settings, setup_logging
# from app.redis.connection import setup_redis_connection
from handlers import start, button_click_handler, inline_interaction_handler, chat_handler


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
    
    # Добавляем обработчик нажатий на кнопки
    application.add_handler(CallbackQueryHandler(button_click_handler))

    # Добавляем обработчик inline-запросов
    application.add_handler(InlineQueryHandler(inline_interaction_handler))
    
    # Добавляем обработчик чата
    application.add_handler(MessageHandler(None, chat_handler))
    
    # Добавляем обработчик ошибок
    # application.add_error_handler(error_handler)
    
    # Сохраняем настройки в bot_data для доступа из handlers
    application.bot_data["settings"] = settings
    # application.bot_data["redis"] = setup_redis_connection()
    
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

        application.run_polling(
            allowed_updates=['message', 'callback_query', 'inline_query'],
            drop_pending_updates=True,  # Игнорируем сообщения, пришедшие пока бот был оффлайн
            close_loop=False  # Не закрываем event loop при остановке
        )
        
    except TelegramError as e:
        logger.error("Ошибка Telegram API: "+ str(e))
    except KeyboardInterrupt:
        logger.info("Бот остановлен в консоли (Ctrl+C)")
    except Exception as e:
        logger.critical("Бот аварийно завершил работу: " + str(e))
        exit(1)

