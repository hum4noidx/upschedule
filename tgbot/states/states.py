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


class UserSettings(StatesGroup):
    profile = State()


class Timetablenew(StatesGroup):
    choose_class = State()
    choose_profile = State()
    # choose_math = State()
    choose_day = State()
    show_timetable = State()


class FastTimetable(StatesGroup):
    main = State()
    second = State()
    third = State()


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
    # math = State()
    finish = State()


class BroadcastSG(StatesGroup):
    choose_class = State()
    choose_profile = State()
    choose_math = State()
    data = State()
    confirm = State()
    final = State()


class AdminPanelSG(StatesGroup):
    main = State()
    users_list = State()


class HoroscopeSG(StatesGroup):
    main = State()
    text = State()
    Confirm = State()


class SubscriptionsSG(StatesGroup):
    subscriptions = State()


class RegHoroscopeSG(StatesGroup):
    main = State()
    finish = State()
