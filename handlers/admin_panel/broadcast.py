import typing
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import broadcast_btns, nav_btns
from keyboards.inline.broadcast_btns import broadcast_class, broadcast_prof
from loader import dp, bot
from states.states import Mailing
from utils.db_api.db import DBAdmin


@dp.callback_query_handler(is_vip=True, text="admin_broadcast")
async def mailing(call: types.CallbackQuery, state: FSMContext):
    m_id = await call.message.edit_text('Пришли текст рассылки', reply_markup=nav_btns.cancel_today)
    async with state.proxy() as data:
        data['m_id'] = m_id['message_id']
    await Mailing.Text.set()


@dp.message_handler(state=Mailing.Text)
async def enter_text(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        m_id = data['m_id']
    await bot.delete_message(message.chat.id, m_id)
    await bot.delete_message(message.chat.id, message.message_id)
    await Mailing.Class.set()
    await message.answer('Кому будем рассылать?', reply_markup=broadcast_btns.broad_class)


@dp.callback_query_handler(broadcast_class.filter(), state=Mailing.Class)
async def broad_class(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    async with state.proxy() as data:
        data['class'] = b_class = callback_data['b_class']
    print(b_class)
    await Mailing.Prof.set()
    m_id2 = await call.message.edit_text('Профиль/буква класса:\nВыбрать любое, если рассылка всем(о,костыль!)',
                                         reply_markup=broadcast_btns.broad_prof)


# TODO: Починить костыль


@dp.callback_query_handler(broadcast_prof.filter(), state=Mailing.Prof)
async def broad_class(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    async with state.proxy() as data:
        data['prof'] = callback_data['b_prof']
    await Mailing.Confirm.set()
    async with state.proxy() as data:
        b_class = data['class']
        b_prof = data['prof']
        text = data['text']
        await call.message.edit_text(f"Подтвердите рассылку сообщения\n\n"
                                     f"Текст:\n"
                                     f" <code>{text}</code>\n"
                                     f"Класс: <b>{b_class}</b>\n"
                                     f"Профиль/буква: <b>{b_prof}</b>", reply_markup=broadcast_btns.confirmation,
                                     parse_mode=types.ParseMode.HTML)


# @dp.callback_query_handler(broadcast_prof.filter(), state=Mailing.Prof)
# async def broad_class(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
#     await call.message.edit_text('Уровень математики')


@dp.callback_query_handler(text="confirm", state=Mailing.Confirm)
async def confirm_broadcast(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        b_class = data['class']
        b_prof = data['prof']
        text = data['text']
    await state.reset_state()
    await call.message.edit_reply_markup()
    if b_class == "everyone":
        users = await DBAdmin.get_user_ids()
    else:
        users = await DBAdmin.user_profile_broadcast(b_class, b_prof)

    for user in users:
        try:
            await bot.send_message(chat_id=user, text=text)
            await sleep(0.3)
        except Exception:
            pass
    await call.message.edit_text('Рассылка успешна', reply_markup=nav_btns.cancel_today)


@dp.callback_query_handler(text="cancel_broadcast", state=Mailing.Confirm)
async def cancel_broadcast(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    await call.message.edit_reply_markup()
    await call.message.answer("Рассылка отменена", reply_markup=nav_btns.cancel_today)
