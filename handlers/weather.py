from aiogram import Router, F
from aiogram.types import Message
from services.weather import get_weather

router = Router()

@router.message(F.text == "🌦 Узнать погоду")
async def show_weather(message: Message):
    weather = await get_weather()
    await message.answer(weather)
