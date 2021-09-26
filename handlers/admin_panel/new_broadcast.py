import typing

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import nav_btns, broadcast_btns
from keyboards.inline.broadcast_btns import broadcast_class_data, broadcast_prof_data
from loader import dp, bot
from states.states import Mailing
from utils.db_api.db import DBBroadcast


async def check_broadcast(state: FSMContext):
    data = await state.get_data()
    text = (f'Проверь рассылку:\n\n'
            f'Текст рассылки:\n{data["text"]}\n'
            f'Класс: {data["broadcast_class"]}\n'
            f'Профиль: {data["prof"]}')
    return text


@dp.message_handler(commands='broadcast', state='*')  # Начинаем рассылку
@dp.callback_query_handler(is_vip=True, text='broadcast')
async def make_broadcast(call: types.CallbackQuery, state: FSMContext):
    message_id = await call.message.edit_text('Пришли текст рассылки', reply_markup=nav_btns.cancel_today)
    await state.update_data(message=message_id['message_id'])
    await Mailing.Text.set()


@dp.message_handler(state=Mailing.Text)  # Получаем текст для рассылки
async def store_text(message: types.message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await bot.delete_message(message.chat.id, data['message'])
    await bot.delete_message(message.chat.id, message.message_id)
    await Mailing.Class.set()
    await message.answer('Кому делаем рассылку?', reply_markup=broadcast_btns.broadcast_class)


@dp.callback_query_handler(broadcast_class_data.filter(), state=Mailing.Class)  # Фильтруем по классам
async def choose_broadcast_class(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await state.update_data(broadcast_class=callback_data['b_class'])
    data = await state.get_data()
    await Mailing.Prof.set()
    if callback_data['b_class'] == 'everyone':  # Делаем рассылку всем пользователям бота
        users = await DBBroadcast.get_user_ids()  # Получаем всех пользователей вне зависимости от класса
        await state.update_data(users=users, prof='None')
        await call.message.edit_text(await check_broadcast(state), reply_markup=broadcast_btns.broadcast_confirm)
    elif callback_data['b_class'] == '10' or '11':
        # Делаем рассылку конкретному классу, после выбираем профиль или делаем для всего класса
        if callback_data['b_class'] == '11':
            await call.message.edit_text('Какому профилю?', reply_markup=broadcast_btns.broadcast_prof11)
        else:
            await call.message.edit_text('Какому профилю?', reply_markup=broadcast_btns.broadcast_prof10)


@dp.callback_query_handler(broadcast_prof_data.filter(), state=Mailing.Prof)  # Фильтруем по профилям
async def choose_broadcast_class(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await state.update_data(prof=callback_data['b_prof'])
    data = await state.get_data()
    if callback_data['b_prof'] == 'everyone':  # Делаем рассылку всему классу
        await call.message.edit_text(await check_broadcast(state), reply_markup=broadcast_btns.broadcast_confirm)
        users = await DBBroadcast.user_class_broadcast(int(data['broadcast_class']))
        await state.update_data(users=users)
    else:  # Отправляем на функцию проверки введенных данных
        users = await DBBroadcast.user_profile_broadcast(data['broadcast_class'], data['prof'])
        await state.update_data(users=users)
        await call.message.edit_text(await check_broadcast(state), reply_markup=broadcast_btns.broadcast_confirm)


# @dp.callback_query_handler(text='continue_broadcast', state='*')
# # Получаем списки пользователей в зависимости от выбранного выше
# async def confirm_broadcast(call: types.CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     await state.reset_state()
#     await call.message.edit_reply_markup()
#     print(data['users'])
# if data['broadcast_class'] == 'everyone':
#     users = await DBBroadcast.get_user_ids()
#     await call.message.edit_text(f'Рассылка для {len(users)} человек\n'
#                                  f'Текст: {data["text"]}\n'
#                                  f'Класс: {data["broadcast_class"]}\n'
#                                  f'Продолжаем?', reply_markup=broadcast_btns.confirmation)
#     await state.update_data(users=users)  # Отдаем id всех пользователей
# elif data['broadcast_class'] != 'everyone':  # Получаем список пользователей по классу
#     users = await DBBroadcast.user_class_broadcast(int(data['broadcast_class']))
#     await call.message.edit_text('Одному классу')
#     await state.update_data(users=users)  # Отдаем id пользователей одного класса
# elif data['prof'] == 'everyone':
#     users = await DBBroadcast.user_class_broadcast(int(data['broadcast_class']))
#     await state.update_data(users=users)
# elif data['prof'] == '11' or '10':
#     users = await DBBroadcast.user_profile_broadcast(data['broadcast_class'], data['prof'])
#     await state.update_data(users=users)  # Отдаем id пользователей по классу и профилю


@dp.callback_query_handler(text='broadcast_confirm', state="*")
async def broadcasting(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # for user in data['users']:
    #     try:
    #         await bot.send_message(chat_id=user, text=data['text'])
    #         await sleep(0.3)
    #     except Exception:
    #         pass
    await call.message.edit_text('Рассылка успешна', reply_markup=nav_btns.cancel_today)
    await state.reset_state()


@dp.callback_query_handler(text="broadcast_cancel", state='*')
async def cancel_broadcast(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    await make_broadcast(call, state)
