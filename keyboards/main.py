from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌦 Узнать погоду")]
        ],
        resize_keyboard=True
    )
