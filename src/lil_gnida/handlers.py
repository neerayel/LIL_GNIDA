from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from keyboards import get_main_menu_keyboard
from commands import execute_server_command

async def is_user_allowed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    # return user_id in context.bot_data["settings"].allowed_user_ids
    return context.bot_data["settings"].allowed_user_ids


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_allowed(update, context):
        await update.message.reply_text("Доступ запрещен.")
        return
    keyboard = get_main_menu_keyboard()
    await update.message.reply_text("Выберите команду:", reply_markup=keyboard)

async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатия на все инлайн-кнопки."""
    query = update.callback_query
    await query.answer()  # Чтобы убрать "часики" в интерфейсе Telegram

    if not await is_user_allowed(update, context):
        await query.edit_message_text(text="Доступ запрещен.")
        return

    # Извлекаем команду из callback_data
    command = query.data
    # Вызываем функцию для выполнения команды
    result_message = await execute_server_command(command, context)
    # Показываем пользователю результат
    await query.edit_message_text(text=result_message)