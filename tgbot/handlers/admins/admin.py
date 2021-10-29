from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.handlers.users.user_main import main_menu
from tgbot.keyboards import nav_btns
from tgbot.services.repository import Repo


async def main_menu_admin(c: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await c.answer()
    await c.message.edit_text('Главное меню|Админ', reply_markup=nav_btns.admin_main_menu)


async def admin_get_user_list(c: CallbackQuery, repo: Repo):
    await c.answer()
    await c.message.edit_text(await repo.list_all_users(), reply_markup=nav_btns.back_to_mm)




async def get_user_info(message: types.message, repo: Repo):
    info = message.get_args()
    try:
        await message.answer(await repo.user_info(info), parse_mode='HTML', reply_markup=nav_btns.back_to_mm)
    except:
        await message.answer('Ошибка')


class MainMenu:
    async def cancel_to_al_3(self: types.CallbackQuery, state: FSMContext):
        await main_menu_admin(self, state)

    # async def cancel_to_al_2(call: types.CallbackQuery):
    #     await main_menu_vip(call)

    async def cancel_to_al_1(self: types.CallbackQuery, state: FSMContext):
        await main_menu(self, state)


def register_admin(dp: Dispatcher):
    dp.register_callback_query_handler(MainMenu.cancel_to_al_3, text='go_main', is_admin=True, state='*')
    dp.register_callback_query_handler(MainMenu.cancel_to_al_1, text='go_main', state='*')
    dp.register_callback_query_handler(admin_get_user_list, text=['admin_all_users'], is_admin=True,
                                       state='*')
    dp.register_message_handler(get_user_info, commands=['i'], state='*', is_admin=True)
