import typing

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message, CallbackQuery
from aiogram_broadcaster import MessageBroadcaster

from tgbot.keyboards import choose_btns
from tgbot.keyboards.choose_btns import classes, profile, math
from tgbot.states.states import Broadcast


async def broadcast_data_collect(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    pass


async def broadcast_command_handler(c: CallbackQuery, state: FSMContext):
    """
    Обработчик, выполняемый после ввода команды /broadcast
    """
    await c.message.answer('Введите текст для начала рассылки:')
    await state.set_state('broadcast_text')


async def start_broadcast(msg: Message, state: FSMContext):
    data = ctx_data.get()
    repo = data.get("repo")
    # collecting data
    users = None
    user_data = await state.get_data()
    user_class = user_data['user_class']
    user_profile = user_data['user_prof']
    user_math = user_data['user_math']
    print(user_data)
    # getting id's from Db
    if user_class == 'class_all':
        users = await repo.get_user_ids()
    if user_profile == 'prof_all':
        users = await repo.broadcast_get_profile_ids()
    print(users)
    await state.finish()
    await MessageBroadcaster(users, msg).run()


async def broadcast_choose_class(c: CallbackQuery):
    await c.message.answer('Рассылка для:', reply_markup=choose_btns.broadcast_choose_class)
    await Broadcast.choose_profile.set()


async def broadcast_choose_profile(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await c.answer()
    await Broadcast.next()
    await state.update_data(user_class=callback_data['classes'])
    if callback_data['classes'] == '11':
        await c.message.edit_text('Профиль:', reply_markup=choose_btns.broadcast_choose_profile_11)
    elif callback_data['classes'] == 'class_all':
        await state.update_data(user_prof=None, user_math=None)
        await broadcast_command_handler(c, state)
    else:
        await c.message.edit_text('Профиль:', reply_markup=choose_btns.broadcast_choose_profile_10)


async def broadcast_choose_math(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await state.update_data(user_prof=callback_data['profile'])
    data = await state.get_data()
    await Broadcast.next()
    if callback_data['profile'] == 'prof_all':
        pass
    if data['user_class'] == '11':
        await c.message.edit_text('Уровень математики:', reply_markup=choose_btns.broadcast_choose_math)
    else:
        await state.update_data(user_math='None')
        await broadcast_command_handler(c, state)


async def broadcast_math_handler(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    # await state.update_data(user_math=callback_data['math'])
    print(callback_data)


# def register_broadcast(dp: Dispatcher):
#     dp.register_callback_query_handler(broadcast_choose_class, text='broadcast',
#                                        state='*')
#     dp.register_callback_query_handler(broadcast_choose_profile, classes.filter(),
#                                        state=Broadcast.choose_profile)
#     dp.register_callback_query_handler(broadcast_choose_math, profile.filter(), state=Broadcast.choose_math)
#     dp.register_callback_query_handler(broadcast_math_handler, math.filter(), state=Broadcast.data)
#     dp.register_callback_query_handler(broadcast_command_handler, is_admin=True, state=Broadcast.confirm)
    dp.register_message_handler(start_broadcast, state='broadcast_text',
                                content_types=types.ContentTypes.ANY)
