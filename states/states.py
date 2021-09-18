from aiogram.dispatcher.filters.state import StatesGroup, State


class Main(StatesGroup):
    main = State()
    choose_profile = State()
    choose_day = State()


class Register(StatesGroup):
    main = State()
    choose_class = State()
    choose_profile = State()
    choose_math = State()


class Mailing(StatesGroup):
    Text = State()
    People = State()
    Class = State()
    Prof = State()
    Math = State()
    Confirm = State()
    Broadcast = State()


class RemindGroup(StatesGroup):
    SetTime = State()