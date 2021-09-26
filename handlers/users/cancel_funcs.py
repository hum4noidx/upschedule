from aiogram import types

from handlers.admin_panel.admin_panel import reset_state
from handlers.users.main import main_menu_vip, choose_class, main_menu, choose_profile, main_menu_admin
from loader import dp
from aiogram import types

from handlers.admin_panel.admin_panel import reset_state
from handlers.users.main import main_menu_vip, choose_class, main_menu, choose_profile
from loader import dp


@dp.callback_query_handler(text='cancel', state="*", is_admin1=True)
async def cancel_admin_panel(call: types.CallbackQuery):
    await main_menu_admin(call)
    await reset_state(call)


# @dp.callback_query_handler(text='cancel', state="*", is_admin1=False)
# async def cancel_admin_panel(call: types.CallbackQuery):
#     await main_menu(call)
#     await reset_state(call)


@dp.callback_query_handler(text='cancel', state="*", is_vip=True)
async def cancel_vip_panel(call: types.CallbackQuery):
    await main_menu_vip(call)
    await reset_state(call)


# @dp.callback_query_handler(text='cancel', state="*", is_vip=False)
# async def cancel_vip_panel(call: types.CallbackQuery):
#     await main_menu(call)
#     await reset_state(call)


@dp.callback_query_handler(text="cancel_to_class", state="*")
async def cancel_to_class(call: types.CallbackQuery):
    await choose_class(call)


@dp.callback_query_handler(text="cancel_to_profile", state="*")
async def cancel_to_class(call: types.CallbackQuery):
    await choose_profile(call)
