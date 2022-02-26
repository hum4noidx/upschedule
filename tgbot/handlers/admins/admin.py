import datetime

import requests
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery, Message

from tgbot.config import load_config
from tgbot.keyboards import nav_btns
# test_keyboards
from tgbot.services.repository import Repo

opts = {"hey": ('Привет', 'Здравствуйте', 'Доброе утро', 'Добрый день', 'Добрый вечер', 'Доброй ночи')}


async def greeting(user_id):
    data = ctx_data.get()
    repo = data.get("repo")
    name = await repo.get_user_name(user_id)
    now = datetime.datetime.now()
    now += datetime.timedelta(hours=1)
    if 4 < now.hour <= 12:
        greet = opts["hey"][2]
    if 12 < now.hour <= 16:
        greet = opts["hey"][3]
    if 16 < now.hour <= 24:
        greet = opts["hey"][4]
    if 0 <= now.hour <= 4:
        greet = opts["hey"][5]

    text = f'{greet}, {name}🖤'
    return text


async def main_menu_admin(c: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await c.answer()
    await c.message.edit_text(f'<b>Главное меню</b>\n{await greeting(c.from_user.id)}\n'
                              f'<a href="https://t.me/upschedulebot">Rebranding</a>',
                              reply_markup=nav_btns.admin_main_menu, parse_mode='HTML', disable_web_page_preview=True)


async def get_user_list(c: CallbackQuery, repo: Repo):
    await c.answer()
    await c.message.edit_text(await repo.list_all_users(), reply_markup=nav_btns.admin_users_list)


async def get_today_user_list(c: CallbackQuery, repo: Repo):
    await c.message.edit_text(await repo.list_all_today_users(), reply_markup=nav_btns.back_to_mm)


async def get_user_info(message: types.message, repo: Repo):
    info = message.get_args()
    try:
        await message.answer(await repo.user_info(info), parse_mode='HTML', reply_markup=nav_btns.back_to_mm)
    except ValueError:
        await message.answer('<b>Ошибка!</b>\nИспользование: /i {id пользователя}')


async def add_vip_user(m: Message, repo: Repo):
    info = m.get_args()
    await m.answer(f"Статус обновлен. Текущий статус - {await repo.add_vip_user(int(info))}")


async def admin_panel_switch(m: Message, repo: Repo):
    await repo.admin_switch(int(m.from_user.id))
    await m.delete()
    await m.answer(f'<a href="tg://user?id={m.from_user.id}">Успешно</a>', parse_mode='HTML')


async def restart_server(m: Message):
    config1 = load_config("bot.ini")

    headers = {
        'accept': '*/*',
        'Authorization': config1.hosting.authorization,
    }


async def add_vip_user(m: Message, repo: Repo):
    info = m.get_args()
    await m.answer(f"Статус обновлен. Текущий статус - {await repo.add_vip_user(int(info))}")


async def admin_panel_switch(m: Message, repo: Repo):
    await repo.admin_switch(int(m.from_user.id))
    await m.delete()
    await m.answer(f'<a href="tg://user?id={m.from_user.id}">Успешно</a>', parse_mode='HTML')


async def restart_server(m: Message):
    config1 = load_config("bot.ini")

    headers = {
        'accept': '*/*',
        'Authorization': config1.hosting.authorization,
    }

    response = requests.post('https://public-api.timeweb.com/api/v1/vds/611025/reboot', headers=headers)
    if response.status_code == 200:
        await m.answer('Успешно')
    else:
        print(response.status_code)
        await m.answer('Ошибка')


async def add_vip_user(message: types.message, repo: Repo):
    info = message.get_args()
    await message.answer(f"Статус обновлен. Текущий статус - {await repo.add_vip_user(int(info))}")
    response = requests.post('https://public-api.timeweb.com/api/v1/vds/611025/reboot', headers=headers)
    if response.status_code == 200:
        await message.answer('Успешно')
    else:
        print(response.status_code)
        await message.answer('Ошибка')


async def admin_access(m: Message):
    await m.answer('Привет!..', reply_markup=nav_btns.start)


async def leave_all(m: Message):
    chats = []
    for chat in chats:
        await m.bot.leave_chat(chat)


def register_admin(dp: Dispatcher):
    dp.register_callback_query_handler(get_user_list, text=['admin_all_users'], is_admin=True,
                                       state='*')
    dp.register_message_handler(get_user_info, commands=['i'], state='*', is_admin=True)
    dp.register_message_handler(add_vip_user, commands=['vip'], state='*', is_admin=True)
    dp.register_callback_query_handler(get_today_user_list, text=['admin_today_all_users'], state='*', is_admin=True)
    dp.register_message_handler(admin_panel_switch, commands='a', commands_prefix='!', state='*')
    # dp.register_message_handler(compliments, text='/cc', state='*')
    dp.register_message_handler(restart_server, commands='restart', is_admin=True, state='*')
    dp.register_message_handler(admin_access, commands=['admin'], is_admin=True, state='*')
    dp.register_message_handler(admin_access, commands=['admin'], is_vip=True, state='*')
    dp.register_message_handler(admin_panel_switch, commands='a', commands_prefix='!', state='*')
    # dp.register_message_handler(compliments, text='/cc', state='*')
    dp.register_message_handler(restart_server, commands='restart', is_admin=True, state='*')
