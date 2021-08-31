from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, inline_keyboard
from aiogram.utils.callback_data import CallbackData

classes = CallbackData('1', 'classes')
letter = CallbackData('2', 'letter')
prof = CallbackData('profile1', 'profile')
d_o_week = CallbackData('vote', 'day')
math = CallbackData('3', 'math')
start_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Начать", callback_data="start")
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
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Расписание", callback_data="main_schedule")
        ],
        [
            InlineKeyboardButton(text="Регистрация", callback_data="register")
        ],
        [
          InlineKeyboardButton(text="Сегодня", callback_data="today_schedule")
        ]
    ]
)

choose_class = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="9 класс", callback_data=classes.new(classes="9")),
            InlineKeyboardButton(text="10 класс", callback_data=classes.new(classes="10")),
            InlineKeyboardButton(text="11 класс", callback_data=classes.new(classes="11"))
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel")
        ]
    ]
)
choose_letter = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="А", callback_data=letter.new(letter="a")),
            InlineKeyboardButton(text="Б", callback_data=letter.new(letter="b")),
            InlineKeyboardButton(text="В", callback_data=letter.new(letter="v"))
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel_to_class")
        ]
    ]
)
choose_profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Физмат", callback_data=letter.new(letter="fm")),
            InlineKeyboardButton(text="Гуманитарий", callback_data=letter.new(letter="gum"))],
        [
            InlineKeyboardButton(text="Соцэконом", callback_data=letter.new(letter="se")),
            InlineKeyboardButton(text="Биохим", callback_data=letter.new(letter="bh"))
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
            InlineKeyboardButton(text='База', callback_data=math.new(math='base'))
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel")
        ]
    ]
)
choose_day = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Понедельник", callback_data=d_o_week.new(day="1")),
            InlineKeyboardButton(text="Вторник", callback_data=d_o_week.new(day="2"))],
        [
            InlineKeyboardButton(text="Среда", callback_data=d_o_week.new(day="3")),
            InlineKeyboardButton(text="Четверг", callback_data=d_o_week.new(day="4"))],
        [
            InlineKeyboardButton(text="Пятница", callback_data=d_o_week.new(day="5")),
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

