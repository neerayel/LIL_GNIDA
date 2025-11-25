from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, error
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from uuid import uuid4
import logging

from keyboards import get_main_menu_keyboard
from commands import execute_server_command
from ollama_interaction import llm_process_single


logger = logging.getLogger(__name__)

async def is_user_allowed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    is_user_allowed = user_id in context.bot_data["settings"].allowed_user_ids
    if not is_user_allowed:
        logger.warning("Неавторизованный пользователь -> " + user_id)
        return


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await is_user_allowed(update, context)
    keyboard = get_main_menu_keyboard()
    await update.message.reply_text("BENIS", reply_markup=keyboard)


async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await is_user_allowed(update, context)

    query = update.callback_query
    await query.answer()

    if not await is_user_allowed(update, context):
        await query.edit_message_text(text="Доступ запрещен.")
        return

    command = query.data
    result_message = await execute_server_command(command, context)
    keyboard = get_main_menu_keyboard()
    await query.edit_message_text(text=result_message, result_message=keyboard)


async def inline_interaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await is_user_allowed(update, context)
    query = update.inline_query.query
    logger.info("Inline запрос :< " + query)

    try:
        llmResponse = await llm_process_single(query)
        logger.info("Ответ на Inline >: "+ llmResponse.message.content)
    except:
        logger.exception("Сбой Ollama при обработке запроса")
    
    results = []
    results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Переписал твою хуйню на внятном лангуаге:',
            description=llmResponse.message.content,
            input_message_content=InputTextMessageContent(message_text=llmResponse.message.content)
        )
    )

    try:
        await context.bot.answer_inline_query(update.inline_query.id, results, is_personal=True, cache_time=context.bot_data["settings"].inline_cache_time)
    except error.BadRequest:
        logger.error("Истекло время ожидания Inline-ответа")