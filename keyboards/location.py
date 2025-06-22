from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def location_keyboard(locations: list[str]|None) -> InlineKeyboardMarkup:
    buttons = []
    if locations:
        buttons = [
            [InlineKeyboardButton(text=f"❌ {loc}", callback_data=f"delete_location:{loc}")]
            for loc in locations
        ]
    buttons.append([InlineKeyboardButton(text="🔙 Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
