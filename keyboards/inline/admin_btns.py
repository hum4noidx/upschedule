from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from keyboards.inline.nav_btns import main_menu

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
            InlineKeyboardButton(text="Сегодня", callback_data="today_schedule"),
            InlineKeyboardButton(text="Инфо по ID", callback_data="admin_info")
        ]
    ]
)
cancel = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Назад", callback_data="vip_cancel")
        ]
    ]
)