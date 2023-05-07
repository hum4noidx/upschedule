from aiogram.fsm.state import StatesGroup, State


class RegistrationSG(StatesGroup):
    choose_grade = State()
    success = State()
