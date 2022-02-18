from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    start = State()
    choose_class = State()
    choose_profile = State()
    choose_math = State()
    confirm = State()


class Timetable(StatesGroup):
    choose_class = State()
    choose_profile = State()
    choose_math = State()
    choose_day = State()


class Timetablenew(StatesGroup):
    choose_class = State()
    choose_profile = State()
    choose_math = State()
    choose_day = State()
    show_timetable = State()


class FastTimetable(StatesGroup):
    main = State()


class Broadcast(StatesGroup):
    choose_class = State()
    choose_profile = State()
    choose_math = State()
    data = State()
    confirm = State()
    final = State()


class RemindGroup(StatesGroup):
    SetTime = State()


class MainSG(StatesGroup):
    greeting = State()
    main_menu = State()


class RegSG(StatesGroup):
    greeting = State()
    school = State()
    grade = State()
    profile = State()
    math = State()
    finish = State()
