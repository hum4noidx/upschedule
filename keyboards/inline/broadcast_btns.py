from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

broadcast_class = CallbackData('smth', 'b_class')
broadcast_prof = CallbackData('smth', 'b_prof')
broadcast_math = CallbackData('math', 'b_math')
broad_class = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="9 класс", callback_data=broadcast_class.new(b_class="9")),
            InlineKeyboardButton(text="10 класс", callback_data=broadcast_class.new(b_class="10")),
            InlineKeyboardButton(text="11 класс", callback_data=broadcast_class.new(b_class="11")),
            InlineKeyboardButton(text="Всем", callback_data=broadcast_class.new(b_class="everyone"))
        ]
    ]
)
broad_prof = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Физмат", callback_data=broadcast_prof.new(b_prof="fm")),
            InlineKeyboardButton(text="Гуманитарий", callback_data=broadcast_prof.new(b_prof="gum")),
        ],
        [
            InlineKeyboardButton(text="Соцэконом", callback_data=broadcast_prof.new(b_prof="se")),
            InlineKeyboardButton(text="Биохим", callback_data=broadcast_prof.new(b_prof="bh")),
        ]
    ]
)
choose_math = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Профиль', callback_data=broadcast_math.new(b_math='prof')),
            InlineKeyboardButton(text='База', callback_data=broadcast_math.new(b_math='base')),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel_to_class")
        ]
    ]
)
confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить", callback_data='confirm')
        ],
[
            InlineKeyboardButton(text="Отмена", callback_data='cancel_broadcast')
        ]
    ]
)