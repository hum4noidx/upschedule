from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.keyboards import nav_btns


async def main_menu_vip(c: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await c.message.edit_text('Главное меню|VIP', reply_markup=nav_btns.main_menu_vip)


def register_vip(dp: Dispatcher):
    dp.register_callback_query_handler(main_menu_vip, text=['go_main'], is_vip=True, state='*')
