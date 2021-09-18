from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.admin_btns import vip_schedule

classes = CallbackData('class', 'classes')
prof = CallbackData('profile', 'profile')
week = CallbackData('day', 'day')
math = CallbackData('math', 'math')
cancel_btn = InlineKeyboardButton(text="Назад", callback_data="cancel")  # Возврат в главное меню
cancel_class_btn = InlineKeyboardButton(text="Назад", callback_data="reg_cancel_to_class")  # Возврат к выбору класса

go_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Начать", callback_data="go_main")
        ]
    ]
)
# Отмена обычного расприсания
cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel_to_class")
        ]
    ]
)
cancel_today = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel")
        ]
    ]
)
cancel_prof = InlineKeyboardButton(text="Назад", callback_data="cancel_to_class")
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Расписание", callback_data="main_schedule")
        ],
        [
            InlineKeyboardButton(text="Регистрация", callback_data="register")
        ],
        [
            InlineKeyboardButton(text="Сегодня", callback_data=vip_schedule.new(vipday='today'))
        ]
    ]
)

choose_class = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            # InlineKeyboardButton(text="10 класс", callback_data=classes.new(classes="10")),
            InlineKeyboardButton(text="11 класс", callback_data=classes.new(classes="11"))
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel")
        ]
    ]
)
choose_profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Физмат", callback_data=prof.new(profile="fm")),
            InlineKeyboardButton(text="Гуманитарий", callback_data=prof.new(profile="gum"))],
        [
            InlineKeyboardButton(text="Соцэконом", callback_data=prof.new(profile="se")),
            InlineKeyboardButton(text="Биохим", callback_data=prof.new(profile="bh"))
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel_to_class")
        ]
    ]
)
choose_math = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Профиль', callback_data=math.new(math='prof')),
            InlineKeyboardButton(text='База', callback_data=math.new(math='base')),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel_to_class")
        ]
    ]
)
choose_day = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Понедельник", callback_data=week.new(day="1")),
            InlineKeyboardButton(text="Вторник", callback_data=week.new(day="2"))],
        [
            InlineKeyboardButton(text="Среда", callback_data=week.new(day="3")),
            InlineKeyboardButton(text="Четверг", callback_data=week.new(day="4"))],
        [
            InlineKeyboardButton(text="Пятница", callback_data=week.new(day="5")),
            InlineKeyboardButton(text="Назад", callback_data="cancel_to_class")
        ]
    ]

)
support = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Написать создателю", url="t.me/hum4noidx")
        ],

        [
            InlineKeyboardButton(text="Назад", callback_data="cancel")
        ]
    ]
)
