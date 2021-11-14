import typing

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery, Message
from aiogram_broadcaster import MessageBroadcaster

from tgbot.keyboards import choose_btns, nav_btns
from tgbot.keyboards.choose_btns import classes, profile, math
from tgbot.states.states import Broadcast


# Broadcast steps:
# 1. click button in admin menu
# 2. enter text or images, save them
# 3. ask for a class to broadcast
# 4. ask for a profile to broadcast
# 5. ask for a level of math
# 6. if in (3) chosen 'all' skip (4-5) go to confirmation message
# 7. if in (4) chosen 'all_class' go to (5) and then go to confirmation message
# 8. if in  (3) chosen '10' skip (5) and go to confirmation message
# 9. ask for confirmation and do broadcast


async def broadcast_get_message(c: CallbackQuery):
    await c.message.edit_text('Введите текст для рассылки:', reply_markup=nav_btns.back_to_mm)


async def broadcast_start(msg: Message, state: FSMContext):
    data = ctx_data.get()
    repo = data.get("repo")
    # collecting data
    users = None
    user_data = await state.get_data()
    user_class = user_data['broadcast_class']
    user_profile = user_data['broadcast_profile']
    user_math = user_data['broadcast_math']

    # getting id's from Db

    # getting ALL user_id's to broadcast
    if user_class == 'classes_all':
        users = await repo.get_user_ids()
    # getting only one class user_id's to broadcast
    else:
        user_class = int(user_class)
        if user_profile == 'class_all':
            users = await repo.broadcast_get_class_ids(int(user_class))
            # Берем список айдишников для одного класса
        elif user_profile != 'class_all' and user_math == 'all':
            users = await repo.broadcast_get_profile_ids(user_profile)
            # Берем айдишники для класса и профиля, математика не учитывается
        elif user_profile != 'prof_all' and user_math != 'all':
            users = await repo.broadcast_get_first_ids(user_class, user_profile, user_math)
            # Берем айдишники для класса, профиля и математики

    await state.finish()
    await MessageBroadcaster(users, msg).run()
    await msg.edit_text('Рассылка успешна', reply_markup=nav_btns.back_to_mm)


async def broadcast_choose_class(c: CallbackQuery):
    await c.message.edit_text('Получатели рассылки:', reply_markup=choose_btns.broadcast_choose_class)
    await Broadcast.choose_profile.set()


async def broadcast_choose_profile(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await state.update_data(broadcast_class=callback_data['classes'])
    if callback_data['classes'] == '11':
        await c.message.edit_text('Профиль:', reply_markup=choose_btns.broadcast_choose_profile_11)
        await Broadcast.choose_math.set()
    elif callback_data['classes'] == 'classes_all':
        await state.update_data(broadcast_profile=None, broadcast_math=None)
        await Broadcast.final.set()
        await broadcast_get_message(c)
    elif callback_data['classes'] == '10':
        await Broadcast.choose_math.set()
        await c.message.edit_text('Профиль:', reply_markup=choose_btns.broadcast_choose_profile_10)


async def broadcast_choose_math(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await state.update_data(broadcast_profile=callback_data['profile'])
    data = await state.get_data()
    if data['broadcast_class'] == '11' and callback_data['profile'] != 'fm':
        await Broadcast.confirm.set()
        await c.message.edit_text('Уровень математики', reply_markup=choose_btns.broadcast_choose_math)
    else:
        if callback_data['profile'] == 'fm':
            await state.update_data(broadcast_math='prof')
        else:
            await state.update_data(broadcast_math=None)
        await Broadcast.final.set()
        await broadcast_get_message(c)


async def broadcast_data_collect(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await state.update_data(broadcast_math=callback_data['math'])
    await Broadcast.final.set()
    await broadcast_get_message(c)


def register_broadcast(dp: Dispatcher):
    dp.register_callback_query_handler(broadcast_choose_class, text='broadcast', state='*')
    dp.register_callback_query_handler(broadcast_choose_profile, classes.filter(),
                                       state=Broadcast.choose_profile)
    dp.register_callback_query_handler(broadcast_choose_math, profile.filter(), state=Broadcast.choose_math)
    dp.register_callback_query_handler(broadcast_data_collect, math.filter(), state=Broadcast.confirm)
    dp.register_callback_query_handler(broadcast_get_message, state=Broadcast.confirm)
    dp.register_message_handler(broadcast_start, state=Broadcast.final,
                                content_types=types.ContentTypes.ANY)

# TODO: мб сделать планировщик рассылки?..
