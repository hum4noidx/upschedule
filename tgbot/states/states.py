from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    start = State()
    choose_class = State()
    choose_profile = State()
    choose_math = State()
    confirm = State()


class Timetable(StatesGroup):
    choose_profile = State()
    choose_math = State()
    choose_day = State()


class Broadcast(StatesGroup):
    choose_class = State()
    choose_profile = State()
    choose_math = State()
    data = State()
    confirm = State()
    final = State()
