from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

vip_schedule = CallbackData('schedule', 'vipday')
presence_filter = CallbackData('user', 'ishere')
main_admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Расписание", callback_data="main_schedule"),
            InlineKeyboardButton(text="Рассылка", callback_data="admin_broadcast")
        ],
        [
            InlineKeyboardButton(text="Регистрация", callback_data="register"),
            InlineKeyboardButton(text="Все пользователи", callback_data="admin_all_users")
        ],
        [
            InlineKeyboardButton(text="Сегодня", callback_data=vip_schedule.new(vipday='today')),
            InlineKeyboardButton(text="Завтра", callback_data=vip_schedule.new(vipday='tomorrow'))
        ]
    ]
)

presence_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='В школе', callback_data=presence_filter.new(ishere='here')),
            InlineKeyboardButton(text='Не в школе', callback_data=presence_filter.new(ishere='not_here'))
        ]
    ]
)
