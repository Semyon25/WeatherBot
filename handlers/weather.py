from aiogram import Router, F
from aiogram.types import Message, User
from services.weather import get_weather
from typing import cast
from db.database import get_session
from db.locations import get_location_by_user_id

router = Router()

@router.message(F.text == "🌦 Узнать погоду")
async def show_weather(message: Message):
    user = cast(User, message.from_user)
    async with get_session() as session:
        location = await get_location_by_user_id(session, user.id)
    if not location:
        await message.answer("❗ Вы не указали локацию. Пожалуйста, укажите её в меню.")
        return
    weather = await get_weather(location)
    await message.answer(weather)
