from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, User
from typing import cast
from services.weather import get_weather
from keyboards.main import main_keyboard
from keyboards.location import location_keyboard
from states.location import LocationStates
from services.weather import is_weather_available
from db.database import get_session
from db.locations import upsert_location

router = Router()

@router.message(F.text == "📍 Изменить локацию")
async def change_location(message: Message, state: FSMContext):
    await message.answer("Введите название города или отправьте свою локацию", reply_markup=location_keyboard())
    await state.set_state(LocationStates.waiting_for_city_name)

@router.message(StateFilter(LocationStates.waiting_for_city_name))
async def city_name_handler(message: Message, state: FSMContext):
    city_name = message.text or ""
    city_exists = await is_weather_available(city_name)
    if not city_exists:
        await message.answer("❗ Такого города не существует. Попробуйте ещё раз.", reply_markup=main_keyboard())
        return
        
    user = cast(User, message.from_user)
    async with get_session() as session:
        await upsert_location(
            session=session,
            user_id=user.id,
            location_name=city_name
        )
    await message.answer(f"Вы ввели город: {city_name}", reply_markup=main_keyboard())
    await state.clear()