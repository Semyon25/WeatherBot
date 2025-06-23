from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def settings_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Изменить локацию")],
            [KeyboardButton(text="🔔 Уведомления")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
