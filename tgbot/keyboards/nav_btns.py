from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

recent_schedule = CallbackData('user', 'day')

start_button = InlineKeyboardButton(text="Открыть меню", callback_data='go_main')
cancel_button = InlineKeyboardButton(text='В главное меню', callback_data='go_main')
schedule_button = InlineKeyboardButton('📚 Расписание', callback_data='timetable')
register_button = InlineKeyboardButton('📝 Регистрация', callback_data='user_register')
settings_button = InlineKeyboardButton('⚙️ Настройки', callback_data='user_settings')
change_name_button = InlineKeyboardButton('✏️ Изменить имя', callback_data='user_change_name')
today_button = InlineKeyboardButton('Сегодня', callback_data=recent_schedule.new(day='today'))
tomorrow_button = InlineKeyboardButton(text="Завтра", callback_data=recent_schedule.new(day='tomorrow'))
admin_button_broadcast = InlineKeyboardButton(text="📢 Рассылка", callback_data="broadcast")
admin_button_all_users = InlineKeyboardButton(text="📊 Users", callback_data="admin_all_users")
today_users = InlineKeyboardButton(text="Сегодня", callback_data='admin_today_all_users')
go_register = InlineKeyboardButton('Поехали', callback_data='reg.class')
cancel_register = InlineKeyboardButton('Назад', callback_data='go_main')
donut_link = InlineKeyboardButton(text='Ссылка на сбор', url='https://www.tinkoff.ru/cf/AJ5VRaWJQjq')
compliments_subscription = InlineKeyboardButton('Настроение📈', callback_data='compliments_subscription')
turn_compliments = InlineKeyboardButton('Включить', callback_data='turn_compliments')
add_compliment = InlineKeyboardButton('Добавить', callback_data='add_compliment')
news_link = InlineKeyboardButton('Ссылка', url='https://t.me/news_1208bot/7')

start = InlineKeyboardMarkup(row_width=1).add(start_button)
donut = InlineKeyboardMarkup(row_width=1).add(donut_link)
back_to_mm = InlineKeyboardMarkup(row_width=1).add(cancel_button)
main_menu = InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(schedule_button, register_button, today_button)
main_menu_vip = InlineKeyboardMarkup(resize_keyboard=True, row_width=2).add(schedule_button).row(settings_button).row(
    today_button, tomorrow_button)
admin_main_menu = InlineKeyboardMarkup(resize_keyboard=True, row_width=2).add(schedule_button, settings_button).row(
    admin_button_broadcast, admin_button_all_users).row(today_button, tomorrow_button)
admin_users_list = InlineKeyboardMarkup(row_width=1).add(today_users, cancel_button)
user_confirm_register = InlineKeyboardMarkup(row_width=2).add(go_register, cancel_register)
user_settings = InlineKeyboardMarkup(resize_keyboard=True, row_width=2).add(change_name_button).row(
    register_button).row(cancel_button)
compliments = InlineKeyboardMarkup(resize_keyboard=True, row_width=2).add(turn_compliments, add_compliment,
                                                                          cancel_button)
compliments_add = InlineKeyboardMarkup(resize_keyboard=True, row_width=2).row(add_compliment, cancel_button)
news_link_markup = InlineKeyboardMarkup(row_width=1).add(news_link)
InlineKeyboardMarkup(InlineKeyboardButton(text='Открыть меню', callback_data='go_main'))