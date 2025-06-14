from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, User
from keyboards.main import main_keyboard
from db.database import get_session
from db.users import add_user
from typing import cast

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = cast(User, message.from_user)
    async with get_session() as session:
        await add_user(
            session=session,
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name,
            last_name=user.last_name or ""
        )
    await message.answer("Привет! Нажми кнопку ниже, чтобы узнать погоду ☀️", reply_markup=main_keyboard())
