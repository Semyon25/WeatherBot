from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User, CallbackQuery, Location
from typing import cast
from keyboards.main import main_keyboard
from keyboards.location import location_keyboard
from states.location import LocationStates
from services.weather import is_weather_available
from services.geo_location import get_city_from_coords
from db.database import get_session
import db.locations as locations_db

router = Router()

# -------------------------------
# Основной хендлер: вход в состояние
# -------------------------------
@router.message(F.text == "📍 Изменить локацию")
async def change_location(message: Message, state: FSMContext):
    user = cast(User, message.from_user)
    async with get_session() as session:
        locations = await locations_db.get_location_by_user_id(
            session=session,
            user_id=user.id
        )

    if len(locations) >= 5:
        text = (
            "⚠️ У вас уже 5 сохранённых локаций.\n"
            "Чтобы добавить новую, удалите одну из существующих:"
        )
    else:
        text = (
            "📍 Вы можете:\n"
            "• Отправить название города текстом\n"
            "• Или отправить геолокацию 📎\n\n"
            "❌ Нажмите на локацию ниже, чтобы удалить её:"
        )
        # Разрешаем добавление только если меньше 5
        await state.set_state(LocationStates.waiting_for_location)

    await message.answer(
        text=text,
        reply_markup=location_keyboard(locations)
    )

# -------------------------------
# Удаление локации
# -------------------------------
@router.callback_query(F.data.startswith("delete_location:"))
async def delete_location_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if callback.data is None:
        return
    loc_to_delete = callback.data.split(":", 1)[1]
    
    async with get_session() as session:
        await locations_db.delete_user_location(
            session=session,
            user_id=user_id,
            location_name=loc_to_delete
        )
        locations = await locations_db.get_location_by_user_id(
            session=session,
            user_id=user_id
        )

    if isinstance(callback.message, Message):
        await callback.message.edit_reply_markup(reply_markup=location_keyboard(locations))
    await callback.answer(f"Локация «{loc_to_delete}» удалена")

# -------------------------------
# Отмена (выход из состояния)
# -------------------------------
@router.callback_query(F.data == "cancel")
async def cancel_location_change(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if isinstance(callback.message, Message):
        await callback.message.delete()
        await callback.message.answer("Главное меню 🏠", reply_markup=main_keyboard())
    await callback.answer()

# -------------------------------
# Добавление локации по тексту
# -------------------------------
@router.message(LocationStates.waiting_for_location, F.text)
async def add_location_by_text(message: Message, state: FSMContext):
    await state.clear()
    user = cast(User, message.from_user)
    city = message.text or ""
    await process_location_addition(user.id, city, message, state)

# -------------------------------
# Добавление локации по гео
# -------------------------------
@router.message(LocationStates.waiting_for_location, F.location)
async def add_location_by_geo(message: Message, state: FSMContext):
    await state.clear()
    user = cast(User, message.from_user)
    if not message.location:
        await message.answer("❌ Не удалось получить координаты.", reply_markup=main_keyboard())
        return

    loc: Location = message.location
    city = await get_city_from_coords(loc.latitude, loc.longitude)
    if city is None:
        await message.answer("❌ Не удалось определить город по геолокации", reply_markup=main_keyboard())
        return

    await process_location_addition(user.id, city, message, state)

async def process_location_addition(user_id: int, city: str, message: Message, state: FSMContext):
    city = city.strip()
    if not city:
        await message.answer("❌ Вы не указали название города.", reply_markup=main_keyboard())
        return

    available = await is_weather_available(city)
    if not available:
        await message.answer(f"❌ Погода для города «{city}» недоступна", reply_markup=main_keyboard())
        return

    async with get_session() as session:
        res = await locations_db.add_user_location(
            session=session,
            user_id=user_id,
            location_name=city
        )
        if res:
            await message.answer(f"✅ Локация «{city}» добавлена!", reply_markup=main_keyboard())
            await state.clear()
        else:
            await message.answer(f"❌ Локация «{city}» уже существует.", reply_markup=main_keyboard())