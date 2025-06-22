from aiogram.fsm.state import StatesGroup, State

class LocationStates(StatesGroup):
  waiting_for_location = State()