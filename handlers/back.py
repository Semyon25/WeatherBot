from aiogram import Router, F
from aiogram.types import Message
from services.weather import get_weather
from keyboards.main import main_keyboard

router = Router()

@router.message(F.text == "🔙 Назад")
async def back_to_main_menu(message: Message):
    await message.answer("Главное меню", reply_markup=main_keyboard())
