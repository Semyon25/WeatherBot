from aiogram import Router, F
from aiogram.types import Message
from keyboards.main import main_keyboard

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Привет! Нажми кнопку ниже, чтобы узнать погоду ☀️", reply_markup=main_keyboard())
