from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from uuid import uuid4
import logging

from keyboards import get_main_menu_keyboard
from commands import execute_server_command
from ollama_interaction import llm_process_single, llm_process_chat
from filewriter import read_start_message

default_message = "Введите текст для обработки"
server_await_message = "Ожидание ответа от сервера"
inline_reply_title = 'Результат:'

logger = logging.getLogger(__name__)


def get_settings(context: ContextTypes.DEFAULT_TYPE):
    return context.bot_data["settings"]


def is_message(message: str) -> bool:
    """ Is None, empty or whitespace """
    if not message: return False
    message = message.strip()
    if len(message) == 0: return False
    return True


def is_user_allowed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """ Проверка наличия id пользователя в белом списке """

    settings = get_settings(context)
    
    user_id = update.effective_user.id
    is_user_allowed = user_id in settings.allowed_user_ids

    if not is_user_allowed:
        logger.warning("Неавторизованный пользователь -> " + str(user_id))
    
    return is_user_allowed


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("/start от -> " + str(update.effective_user.id))
    if not is_user_allowed(update, context): return

    settings = get_settings(context)
    keyboard = get_main_menu_keyboard()
    start_message = read_start_message(settings.start_message_path)
    await update.message.reply_text(start_message, reply_markup=keyboard)


async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Взаимодействие с клавиатурой от -> " + str(update.effective_user.id))
    if not is_user_allowed(update, context): return

    query = update.callback_query
    command = query.data

    await query.edit_message_text(text=server_await_message)

    result_message = await execute_server_command(command, context)
    keyboard = get_main_menu_keyboard()
    
    await query.edit_message_text(text=result_message, reply_markup=keyboard)


async def inline_interaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("inline запрос от -> " + str(update.effective_user.id))
    if not is_user_allowed(update, context): return

    settings = get_settings(context)

    message = update.inline_query.query
    if not is_message(message): response_text = default_message
    else:
        response_text = await llm_process_single(message, settings)
    
    results = []
    results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=inline_reply_title,
            description=response_text,
            input_message_content=InputTextMessageContent(message_text=response_text)
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results, is_personal=True, cache_time=settings.inline_cache_time)

    
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Взаимодействие с чатом от -> " + str(update.effective_user.id))
    if not is_user_allowed(update, context): return

    settings = get_settings(context)
    
    message = update.message.text
    if not is_message(message): response_text = default_message
    else: response_text = await llm_process_chat(message, settings)

    await update.message.reply_text(response_text)
