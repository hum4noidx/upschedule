from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

register_class = CallbackData('smth', 'reg_classes')
register_profile = CallbackData('smth', 'reg_profile')
register_math = CallbackData('smth', 'reg_math')

cancel_btn = InlineKeyboardButton(text="Назад", callback_data="cancel")  # Возврат в главное меню
cancel_class_btn = InlineKeyboardButton(text="Назад", callback_data="reg_cancel_to_class")  # Возврат к выбору класса
register = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Дальше", callback_data="reg.choose_class")
        ]
    ]
)
register.add(cancel_btn)
select_classes = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="11 класс", callback_data=register_class.new(reg_classes="reg_11"))
        ]
    ]
)
select_classes.add(cancel_btn)
select_profiles = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Физмат", callback_data=register_profile.new(reg_profile="fm")),
            InlineKeyboardButton(text="Гуманитарий", callback_data=register_profile.new(reg_profile="gum")),
        ],
        [
            InlineKeyboardButton(text="Соцэконом", callback_data=register_profile.new(reg_profile="se")),
            InlineKeyboardButton(text="Биохим", callback_data=register_profile.new(reg_profile="bh")),
        ]
    ]
)
select_profiles.add(cancel_class_btn)
select_math = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Профиль', callback_data=register_math.new(reg_math='prof')),
            InlineKeyboardButton(text='База', callback_data=register_math.new(reg_math='base'))
        ]
    ]
)
select_math.add(cancel_class_btn)
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="В главное меню", callback_data="cancel")
        ]
    ]
)
