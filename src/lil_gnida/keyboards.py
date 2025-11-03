from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard():
    # Кнопки - это callback_data, которые мы будем обрабатывать
    keyboard = [
        # [InlineKeyboardButton("Перезапустить Сервис", callback_data="cmd_restart_service")],
        [InlineKeyboardButton("Статус Системы", callback_data="cmd_system_status")],
    ]
    return InlineKeyboardMarkup(keyboard)