from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.handlers.admins.admin import main_menu_admin
from tgbot.handlers.users.user_main import main_menu
from tgbot.handlers.vips.vip import main_menu_vip


async def level_filter_admin(c: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    await main_menu_admin(c, state)


async def level_filter_vip(c: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    await main_menu_vip(c, state)


async def level_filter_base(c: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    await main_menu(c, state)


def register_level_filter(dp: Dispatcher):
    dp.register_callback_query_handler(level_filter_admin, text='go_main', is_admin=True, state='*')
    dp.register_callback_query_handler(level_filter_vip, text='go_main', is_vip=True, state='*')
    dp.register_callback_query_handler(level_filter_base, text='go_main', is_vip=False, state='*')
