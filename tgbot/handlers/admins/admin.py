from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from tgbot.handlers.users.user_main import main_menu
from tgbot.keyboards import nav_btns
from tgbot.services.repository import Repo


async def main_menu_admin(c: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await c.answer()
    await c.message.edit_text('Главное меню|Админ👑', reply_markup=nav_btns.admin_main_menu)


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
