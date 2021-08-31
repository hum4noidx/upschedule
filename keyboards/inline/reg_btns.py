from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

register_class = CallbackData('smth', 'reg_classes')
register_profile = CallbackData('smth', 'reg_profile')
register_math = CallbackData('smth', 'reg_math')
register = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Дальше", callback_data="reg.choose_class")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel")
        ]
    ]
)
select_classes = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="9 класс", callback_data=register_class.new(reg_classes="reg_9")),
            InlineKeyboardButton(text="10 класс", callback_data=register_class.new(reg_classes="reg_10"))
        ],
        [
            InlineKeyboardButton(text="11 класс", callback_data=register_class.new(reg_classes="reg_11")),
            InlineKeyboardButton(text="Назад", callback_data="cancel")
        ]
    ]
)
select_profiles = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Физмат", callback_data=register_profile.new(reg_profile="fm")),
            InlineKeyboardButton(text="Гуманитарий", callback_data=register_profile.new(reg_profile="gum")),
        ],
        [
            InlineKeyboardButton(text="Соцэконом", callback_data=register_profile.new(reg_profile="se")),
            InlineKeyboardButton(text="Биохим", callback_data=register_profile.new(reg_profile="bh")),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="reg_cancel_to_class")
        ]
    ]
)
select_math = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Профиль', callback_data=register_math.new(reg_math='prof')),
            InlineKeyboardButton(text='База', callback_data=register_math.new(reg_math='base'))
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="reg_cancel_to_class")
        ]
    ]
)
select_letters = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="А", callback_data=register_profile.new(reg_profile="a")),
            InlineKeyboardButton(text="Б", callback_data=register_profile.new(reg_profile="b")),
        ],
        [
            InlineKeyboardButton(text="В", callback_data=register_profile.new(reg_profile="v")),
            InlineKeyboardButton(text="Назад", callback_data="reg_cancel_to_class")
        ]

    ]
)
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="В главное меню", callback_data="cancel")
        ]
    ]
)
