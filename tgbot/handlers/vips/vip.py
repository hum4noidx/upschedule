from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from tgbot.keyboards import nav_btns


async def main_menu_vip(c: CallbackQuery, state: FSMContext):
    await state.reset_state()
    try:
        # await c.message.edit_text(
        #     f'<b>Главное меню</b>\n{await greeting(c.from_user.id)}', reply_markup=nav_btns.main_menu_vip,
        #     parse_mode='HTML'
        # )
        await c.message.edit_text('<a href="https://t.me/news_1208bot/7">Closed Access</a>',
                                  reply_markup=nav_btns.main_menu_vip, disable_web_page_preview=True)
    except MessageNotModified:
        print('Edit failure.', c.from_user.id)


def register_vip(dp: Dispatcher):
    dp.register_callback_query_handler(main_menu_vip, text=['go_main'], is_vip=True, state='*')
