from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models.notification import Notification

def notifications_keyboard(notifications: list[Notification], canAdd: bool) -> InlineKeyboardMarkup:
    buttons = []
    for notif in notifications:
        emoji = {
            "daily": "📅",
            "weekdays": "🏢",
            "weekends": "🏖️"
        }.get(notif.mode, "")
        label = f"{emoji} {notif.time}"
        callback_data = f"del_{notif.time}|{notif.mode}"
        buttons.append([InlineKeyboardButton(text=f"❌ {label}", callback_data=callback_data)])

    if canAdd:
        buttons.append([InlineKeyboardButton(text="➕ Добавить", callback_data="add_notification")])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def hour_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for h in range(24):
        row.append(InlineKeyboardButton(text=f"{h:02d}", callback_data=f"set_hour:{h:02d}"))
        if len(row) == 6:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="🔙 Отмена", callback_data="back_to_notifications")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def minute_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for m in range(0, 60, 10):
        row.append(InlineKeyboardButton(text=f"{m:02d}", callback_data=f"set_minute:{m:02d}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="add_notification")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def mode_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📅 Каждый день", callback_data="set_mode:daily")],
        [InlineKeyboardButton(text="🏢 По будням", callback_data="set_mode:weekdays")],
        [InlineKeyboardButton(text="🏖️ По выходным", callback_data="set_mode:weekends")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="add_notification")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
