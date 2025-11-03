from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard():
    # Кнопки - это callback_data, которые мы будем обрабатывать
    keyboard = [
        [InlineKeyboardButton("Статус Системы", callback_data="cmd_system_status")]
    ]
    return InlineKeyboardMarkup(keyboard)