from typing import cast
from aiogram import Router, F
from aiogram.types import Message, User, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import false
from states.notifications import NotificationStates
from models.notification import Notification
from keyboards.notifications import (
    hour_keyboard, minute_keyboard, mode_keyboard, notifications_keyboard
)
from keyboards.main import main_keyboard
from db.database import get_session
import db.notifications as db

router = Router()

@router.message(F.text == "🔔 Уведомления")
async def show_notifications(message: Message, state: FSMContext):
  user = cast(User, message.from_user)
  await show_notifications_for_user(user.id, message, edit=False)

async def show_notifications_for_user(user_id: int, message, edit=True):
  async with get_session() as session:
    notifications = await db.get_user_notifications(
        session=session,
        user_id=user_id
    )
  text = "Ваши уведомления" if notifications  else "У вас нет уведомлений"
  canAdd = len(notifications) < 10
  if edit:
    await message.edit_text(text, reply_markup=notifications_keyboard(notifications, canAdd))
  else:
    await message.answer(text, reply_markup=notifications_keyboard(notifications, canAdd))

@router.callback_query(F.data.startswith("del_"))
async def delete_notification_handler(callback: CallbackQuery):
  if not isinstance(callback.message, Message):
    return
  if callback.data is None:
    return
  user_id = callback.from_user.id
  data = callback.data[4:]
  try:
    time, mode = data.split("|")
  except ValueError:
    await callback.answer("Некорректные данные", show_alert=True)
    return
  notif = Notification(user_id=user_id, time=time, mode=mode)
  async with get_session() as session:
    await db.delete_notification(
      session=session,
      notif=notif
    )
  await callback.answer("Уведомление удалено")
  await show_notifications_for_user(user_id, callback.message)

@router.callback_query(F.data == "add_notification")
async def add_notification_handler(callback: CallbackQuery, state: FSMContext):
  if not isinstance(callback.message, Message):
    return
  await state.set_state(NotificationStates.choosing_hour)
  await callback.message.edit_text("Выберите час:", reply_markup=hour_keyboard())
  await callback.answer()

@router.callback_query(F.data.startswith("set_hour:"))
async def set_hour(callback: CallbackQuery, state: FSMContext):
  if callback.data is None:
    return
  if not isinstance(callback.message, Message):
    return
  hour = callback.data.split(":")[1]
  await state.update_data(hour=hour)
  await state.set_state(NotificationStates.choosing_minute)
  await callback.message.edit_text("Выберите минуты:", reply_markup=minute_keyboard())
  await callback.answer()

@router.callback_query(F.data.startswith("set_minute:"))
async def set_minute(callback: CallbackQuery, state: FSMContext):
  if callback.data is None:
    return
  if not isinstance(callback.message, Message):
    return
  minute = callback.data.split(":")[1]
  data = await state.get_data()
  time = f"{data['hour']}:{minute}"
  await state.update_data(time=time)
  await state.set_state(NotificationStates.choosing_mode)
  await callback.message.edit_text("Выберите режим:", reply_markup=mode_keyboard())
  await callback.answer()

@router.callback_query(F.data.startswith("set_mode:"))
async def set_mode(callback: CallbackQuery, state: FSMContext):
  if callback.data is None:
    return
  if not isinstance(callback.message, Message):
    return
  mode = callback.data.split(":")[1]
  data = await state.get_data()
  time = data["time"]
  user_id = callback.from_user.id
  notif = Notification(user_id=user_id, time=time, mode=mode)
  async with get_session() as session:
    notifications = await db.get_user_notifications(session, user_id)
    if await notification_exists(notifications, notif):
        await callback.answer("Такое уведомление уже существует", show_alert=True)
    else:
        await db.add_notification(session=session, notif=notif)
        await callback.answer("Добавлено")
  await state.clear()
  await show_notifications_for_user(callback.from_user.id, callback.message)

@router.callback_query(F.data == "back_to_notifications")
async def back_to_notifications(callback: CallbackQuery, state: FSMContext):
  if not isinstance(callback.message, Message):
    return
  await state.clear()
  await show_notifications_for_user(callback.from_user.id, callback.message)
  await callback.answer()

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
  if not isinstance(callback.message, Message):
    return
  await callback.message.delete()
  await callback.message.answer("Главное меню 🏠", reply_markup=main_keyboard())
  await callback.answer()

async def notification_exists(notifications: list[Notification], notif: Notification) -> bool:
  time = notif.time
  mode = notif.mode

  # Сначала соберём все modes для того же времени
  existing_modes = {n.mode for n in notifications if n.time == time}

  if mode == "daily":
      # Если пытаемся добавить daily, но есть weekdays или weekends — запрещаем
      if "weekdays" in existing_modes or "weekends" in existing_modes or "daily" in existing_modes:
          return True

  elif mode in {"weekdays", "weekends"}:
      # Если пытаемся добавить weekdays или weekends
      # но уже есть daily — запрещаем
      if "daily" in existing_modes:
          return True
      # Если уже есть именно такой mode — тоже запрещаем (чтобы не дублировать)
      if mode in existing_modes:
          return True

  return False
