from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

broadcast_class = CallbackData('smth', 'b_class')
broadcast_prof = CallbackData('smth', 'b_prof')

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
        ],
        [
            InlineKeyboardButton(text="А", callback_data=broadcast_prof.new(b_prof="a")),
            InlineKeyboardButton(text="Б", callback_data=broadcast_prof.new(b_prof="b")),
        ],
        [
            InlineKeyboardButton(text="В", callback_data=broadcast_prof.new(b_prof="v"))
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