import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards import nav_btns
from tgbot.services.repository import Repo


async def show_settings(c: CallbackQuery, repo: Repo):
    await c.message.edit_text(await repo.show_user_info(c.from_user.id), reply_markup=nav_btns.user_settings)


async def vip_change_name(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text('Введите имя...', reply_markup=nav_btns.back_to_mm)
    await state.update_data(m_id=c.message.message_id)
    await state.set_state('change_name')


async def vip_change_name_text(m: Message, repo: Repo, state: FSMContext):
    await repo.user_change_name(m.from_user.id, m.text)
    m_id = await state.get_data()
    await m.bot.delete_message(m.chat.id, m_id['m_id'])
    await m.delete()
    await asyncio.sleep(0.5)
    await m.answer('Имя изменено', reply_markup=nav_btns.back_to_mm)
    await state.reset_state()


def register_user_settings(dp: Dispatcher):
    dp.register_callback_query_handler(show_settings, text='user_settings', state='*')
    dp.register_callback_query_handler(vip_change_name, text='user_change_name', state='*')
    dp.register_message_handler(vip_change_name_text, state='change_name')
