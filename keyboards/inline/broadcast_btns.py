from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

broadcast_class_data = CallbackData('smth', 'b_class')
broadcast_prof_data = CallbackData('smth', 'b_prof')
broadcast_math_data = CallbackData('math', 'b_math')
broadcast_class = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="10 класс", callback_data=broadcast_class_data.new(b_class="10")),
            InlineKeyboardButton(text="11 класс", callback_data=broadcast_class_data.new(b_class="11"))
        ],
        [
            InlineKeyboardButton(text="Всем", callback_data=broadcast_class_data.new(b_class="everyone"))
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="broadcast_cancel")
        ]
    ]
)
broadcast_prof11 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Физмат", callback_data=broadcast_prof_data.new(b_prof="fm")),
            InlineKeyboardButton(text="Гуманитарий", callback_data=broadcast_prof_data.new(b_prof="gum")),
        ],
        [
            InlineKeyboardButton(text="Соцэконом", callback_data=broadcast_prof_data.new(b_prof="se")),
            InlineKeyboardButton(text="Биохим", callback_data=broadcast_prof_data.new(b_prof="bh")),
        ],
        [
            InlineKeyboardButton(text="Всему классу", callback_data=broadcast_prof_data.new(b_prof='everyone'))
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="broadcast_cancel")
        ]
    ]
)
broadcast_prof10 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Медицинский", callback_data=broadcast_prof_data.new(b_prof="med")),
            InlineKeyboardButton(text="Медиа", callback_data=broadcast_prof_data.new(b_prof="media"))],
        [
            InlineKeyboardButton(text="Академический", callback_data=broadcast_prof_data.new(b_prof="akadem")),
            InlineKeyboardButton(text="Инженеры/IT", callback_data=broadcast_prof_data.new(b_prof="it"))
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel_to_class")
        ]
    ]
)
# broadcast_choose_math = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text='Профиль', callback_data=broadcast_math_data.new(b_math='prof')),
#             InlineKeyboardButton(text='База', callback_data=broadcast_math_data.new(b_math='base')),
#         ],
#         [
#             InlineKeyboardButton(text="Назад", callback_data="cancel_to_class")
#         ]
#     ]
# )
confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Погнали", callback_data='broadcast_confirm')
        ],
        [
            InlineKeyboardButton(text="Не, давай назад", callback_data='broadcast_cancel')
        ]
    ]
)
broadcast_confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Дальше', callback_data='broadcast_confirm'),
            InlineKeyboardButton(text='Отмена', callback_data='broadcast_cancel')
        ]
    ]
)
