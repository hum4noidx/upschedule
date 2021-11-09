import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery
from tgbot.keyboards import nav_btns
from tgbot.services.repository import Repo

opts = {"hey": ('Привет', 'Здравствуйте', 'Доброе утро', 'Добрый день', 'Добрый вечер', 'Доброй ночи')}


async def main_menu_admin(c: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await c.answer()
    data = ctx_data.get()
    repo = data.get("repo")
    name = await repo.get_user_name(c.from_user.id)
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

    await c.message.edit_text(f'{greet}, {name}.\nГлавное меню|Админ👑', reply_markup=nav_btns.admin_main_menu)


async def get_user_list(c: CallbackQuery, repo: Repo):
    await c.answer()
    await c.message.edit_text(await repo.list_all_users(), reply_markup=nav_btns.admin_users_list)


async def get_today_user_list(c: CallbackQuery, repo: Repo):
    await c.message.edit_text(await repo.list_all_today_users(), reply_markup=nav_btns.back_to_mm)


async def get_user_info(message: types.message, repo: Repo):
    info = message.get_args()
    try:
        await message.answer(await repo.user_info(info), parse_mode='HTML', reply_markup=nav_btns.back_to_mm)
    except:
        await message.answer('Ошибка')


async def add_vip_user(message: types.message, repo: Repo):
    info = message.get_args()
    await message.answer(f"Статус обновлен. Текущий статус - {await repo.add_vip_user(int(info))}")


def register_admin(dp: Dispatcher):
    dp.register_callback_query_handler(get_user_list, text=['admin_all_users'], is_admin=True,
                                       state='*')
    dp.register_message_handler(get_user_info, commands=['i'], state='*', is_admin=True)
    dp.register_message_handler(add_vip_user, commands=['vip'], state='*', is_admin=True)
    dp.register_callback_query_handler(get_today_user_list, text=['admin_today_all_users'], state='*', is_admin=True)
