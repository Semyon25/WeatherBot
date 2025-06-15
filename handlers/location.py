from aiogram import Router, F
from aiogram.types import Message
from services.weather import get_weather

router = Router()

@router.message(F.text == "📍 Изменить локацию")
async def change_location(message: Message):
    await message.answer("Функция изменения локации пока не реализована.")
