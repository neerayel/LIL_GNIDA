from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from uuid import uuid4

from keyboards import get_main_menu_keyboard
from commands import execute_server_command
from ollama_interaction import llm_process_single

async def is_user_allowed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    is_user_allowed = user_id in context.bot_data["settings"].allowed_user_ids
    if not is_user_allowed:
        return


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await is_user_allowed(update, context)
    keyboard = get_main_menu_keyboard()
    await update.message.reply_text("BENIS", reply_markup=keyboard)


async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await is_user_allowed(update, context)
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
    keyboard = get_main_menu_keyboard()
    await query.edit_message_text(text=result_message, result_message=keyboard)


async def inline_interaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await is_user_allowed(update, context)
    query = update.inline_query.query
    
    llmResponse = await llm_process_single(query)
    results = []
    results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Переписал твою хуйню на внятном лангуаге:',
            description=llmResponse.message.content,
            input_message_content=InputTextMessageContent(message_text=llmResponse.message.content)
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results, is_personal=True, cache_time=context.bot_data["settings"].inline_cache_time)
