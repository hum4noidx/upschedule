# # \____________________ SCHEDULE FUNCTIONS ____________________/
import datetime
import typing

import aiogram
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery

from tgbot.handlers.users.user_main import user_usage
from tgbot.keyboards import nav_btns, choose_btns
from tgbot.keyboards.choose_btns import week, profile, classes, math, profile_other, make_buttons
from tgbot.keyboards.nav_btns import recent_schedule
from tgbot.schedule import days
from tgbot.states.states import Timetable


async def timetable_make(c: CallbackQuery, state: FSMContext, user_class,
                         user_profile, user_math, user_date):
    await c.answer()
    await user_usage(c.from_user.id)
    if user_class == '11':
        markup = make_buttons()
        await state.update_data(user_class=user_class, user_profile=user_profile, user_math=user_math,
                                user_date=user_date)
    else:
        markup = nav_btns.back_to_mm
    try:  # собираем расписание по переданным данным

        await c.message.edit_text(
            f"{days.get(user_class).get(user_profile).get(user_math).get(user_date).get('description')}\n\n"
            f"{days.get(user_class).get(user_profile).get(user_math).get(user_date).get('classes')}",
            parse_mode='HTML', reply_markup=markup)
        await state.set_state('other_schedule')
    except aiogram.exceptions.MessageNotModified:
        pass


async def timetable_prepare_data(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    user_data = await state.get_data()
    user_class = user_data['user_class']
    user_profile = user_data['user_profile']
    user_math = user_data['user_math']
    user_date = callback_data['day']
    await state.update_data(user_date=callback_data['day'])
    await timetable_make(c, state, user_class, user_profile, user_math, user_date)


async def timetable_choose_day(c: CallbackQuery, state: FSMContext, callback_data: typing.Dict[str, str]):
    await state.update_data(user_math=callback_data['math'])
    await c.message.edit_text('Выбери день недели', reply_markup=choose_btns.user_choose_day)


async def timetable_choose_class(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text('Выбери класс', reply_markup=choose_btns.user_choose_class)
    await Timetable.choose_profile.set()


async def timetable_choose_profile(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await c.answer()
    await state.update_data(user_class=callback_data['classes'])
    if int(callback_data['classes']) == 11:
        await c.message.edit_text('Выбери профиль', reply_markup=choose_btns.user_choose_profile_11)
    else:
        await c.message.edit_text('Выбери профиль', reply_markup=choose_btns.user_choose_profile_10)
    await Timetable.next()


async def timetable_choose_math(c: CallbackQuery, state: FSMContext, callback_data: typing.Dict[str, str]):
    await c.answer()
    await state.update_data(user_profile=callback_data['profile'])
    data = await state.get_data()
    if data['user_class'] == '11':
        if callback_data['profile'] == 'fm':
            await Timetable.next()
            callback_data['math'] = 'prof'
            await timetable_choose_day(c, state, callback_data)
        else:
            await Timetable.next()
            await c.message.edit_text('Выбери уровень математики', reply_markup=choose_btns.user_choose_math)
    else:
        await Timetable.next()
        callback_data['math'] = 'None'
        await timetable_choose_day(c, state, callback_data)


async def timetable_nearest(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    data = ctx_data.get()
    repo = data.get("repo")
    user_data = await repo.timetable_prepare_data(c.from_user.id)
    user_class = str(user_data['user_class'])
    user_profile = str(user_data['user_prof'])
    user_math = str(user_data['user_math'])
    if callback_data['day'] == 'today':
        user_date = str(datetime.date.today().isoweekday())
    else:
        user_date = datetime.date.today() + datetime.timedelta(days=1)
        user_date = str(user_date.isoweekday())
    await state.update_data(user_class=user_class, user_profile=user_profile, user_math=user_math,
                            user_date=user_date)
    await timetable_make(c, state, user_class, user_profile, user_math, user_date)


async def timetable_other(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    data = await state.get_data()
    try:
        user_class = str(data['user_class'])
        user_date = int(data['user_date'])
        if callback_data['profile'] and callback_data['math'] != 'None':
            user_profile = callback_data['profile']
            user_math = callback_data['math']
        else:
            user_profile = str(data['user_profile'])
            user_math = str(data['user_math'])
        if callback_data['day']:
            date = callback_data['day']
            if date == 'prev':
                user_date = user_date - 1
            else:
                user_date = user_date + 1
        if user_date == 8:
            user_date -= 7
        elif user_date == 0:
            user_date += 7
        user_date = str(user_date)
        await c.answer()
        await timetable_make(c, state, user_class, user_profile, user_math, user_date)
    except KeyError:
        await c.answer(
            'Ошибка!\nСкорее всего, это произошло из-за того, что вы долго оставались в этом меню.\n'
            'Вернитесь в главное меню', show_alert=True)


def register_timetable(dp: Dispatcher):
    dp.register_callback_query_handler(timetable_choose_class, text='timetable', state='*')
    dp.register_callback_query_handler(timetable_choose_profile, classes.filter(), state=Timetable.choose_profile)
    dp.register_callback_query_handler(timetable_choose_math, profile.filter(), state=Timetable.choose_math)
    dp.register_callback_query_handler(timetable_choose_day, math.filter(), state=Timetable.choose_day)
    dp.register_callback_query_handler(timetable_prepare_data, week.filter(), state=Timetable.choose_day)
    dp.register_callback_query_handler(timetable_nearest, recent_schedule.filter(), state='*')
    dp.register_callback_query_handler(timetable_other, profile_other.filter(), state='*')
