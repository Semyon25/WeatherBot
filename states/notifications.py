from aiogram.fsm.state import StatesGroup, State

class NotificationStates(StatesGroup):
   choosing_hour = State()
   choosing_minute = State()
   choosing_mode = State()