from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.vip_btns import vip_schedule

main_admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Расписание", callback_data="main_schedule"),
            InlineKeyboardButton(text="Рассылка", callback_data="broadcast")
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