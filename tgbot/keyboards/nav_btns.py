from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

recent_schedule = CallbackData('user', 'day')
# Start button
start_butt = InlineKeyboardButton(text="Погнали!", callback_data='go_main')
start = InlineKeyboardMarkup(row_width=1).add(start_butt)
# \____________________ CANCEL BUTTONS ____________________/
# Cancel to start menu
cancel_butt = InlineKeyboardButton(text='В главное меню', callback_data='go_main')
back_to_mm = InlineKeyboardMarkup(row_width=1).add(cancel_butt)
# \____________________ NAVIGATION ____________________/
# Main menu buttons
# base buttons
schedule_button = InlineKeyboardButton('Расписание', callback_data='schedule')
register_button = InlineKeyboardButton('Регистрация', callback_data='user_register')
today_button = InlineKeyboardButton('Сегодня', callback_data=recent_schedule.new(day='today'))
tomorrow_button = InlineKeyboardButton(text="Завтра", callback_data=recent_schedule.new(day='tomorrow'))
main_menu = InlineKeyboardMarkup(row_width=1).add(schedule_button, register_button, today_button)
# vip buttons
main_menu_vip = InlineKeyboardMarkup(row_width=2).add(schedule_button).row(register_button).row(
    today_button, tomorrow_button)
# admin buttons
admin_button_broadcast = InlineKeyboardButton(text="Рассылка", callback_data="broadcast")
admin_button_all_users = InlineKeyboardButton(text="USERS", callback_data="admin_all_users")
admin_main_menu = InlineKeyboardMarkup(row_width=2).add(
    schedule_button, register_button).row(admin_button_broadcast, admin_button_all_users).row(
    today_button, tomorrow_button)
# Register navigation buttons
go_register = InlineKeyboardButton('Поехали', callback_data='reg.class')
cancel_register = InlineKeyboardButton('Назад', callback_data='go_main')
user_confirm_register = InlineKeyboardMarkup(row_width=2).add(go_register, cancel_register)
