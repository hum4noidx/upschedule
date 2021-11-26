from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from tgbot.handlers.admins.admin import greeting
from tgbot.keyboards import nav_btns


async def main_menu_vip(c: CallbackQuery, state: FSMContext):
    await state.reset_state()
    try:
        await c.message.edit_text(
            f'{await greeting(c.from_user.id)}\nГлавное меню|VIP', reply_markup=nav_btns.main_menu_vip
        )
    except MessageNotModified:
        print('Edit failure.', c.from_user.id)


def register_vip(dp: Dispatcher):
    dp.register_callback_query_handler(main_menu_vip, text=['go_main'], is_vip=True, state='*')
