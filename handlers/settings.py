from aiogram import Router, F
from aiogram.types import Message
from services.weather import get_weather
from keyboards.settings import settings_keyboard

router = Router()

@router.message(F.text == "⚙ Настройки")
async def show_settings(message: Message):
    await message.answer("Вы в настройках. Выберите действие", reply_markup=settings_keyboard())
