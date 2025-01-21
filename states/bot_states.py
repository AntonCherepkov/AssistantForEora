from aiogram.fsm.state import StatesGroup, State


class StatesBot(StatesGroup):
    START = State()
    DIALOG = State()