import datetime
import typing

import aiogram
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards import nav_btns, choose_btns
from tgbot.keyboards.choose_btns import classes, profile, math, week, make_buttons, profile_other
from tgbot.keyboards.nav_btns import recent_schedule
from tgbot.schedule import days
from tgbot.services.repository import Repo
from tgbot.states.states import Schedule


async def user_usage(user_id):
    data = ctx_data.get()
    repo = data.get("repo")
    await repo.schedule_user_usage(user_id)


async def user_start(m: Message, repo: Repo):
    await repo.add_user(m.from_user.id, m.from_user.full_name)
    await m.answer(f'<b>Hello, {m.from_user.full_name}!</b>\n'
                   f'<u>Это многофункциональный школьный бот</u>\n'
                   f'<b>Одни из возможностей:</b>\n'
                   f'При добавлении в группы автоматически удаляет сообщения о вступлении и выходе участников('
                   f'требуются права администратора)\n\n'
                   f'Бросить кубик можно командой /dice\n\n'
                   f'Для удобства пользования рекомендуется сразу выбрать класс и профиль.\n'
                   f'Для этого нажми кнопку \'Регистрация\'',
                   parse_mode="HTML", reply_markup=nav_btns.start)


async def main_menu(c: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await c.message.edit_text('Главное меню', reply_markup=nav_btns.main_menu)


# # \____________________ SCHEDULE FUNCTIONS ____________________/
# 6
async def get_schedule(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext, *args):
    user_data = await state.get_data()
    user_class = user_data['user_class']
    user_profile = user_data['user_profile']
    user_math = user_data['user_math']
    user_day = callback_data['day']
    try:
        await c.message.edit_text(
            f"{days.get(user_class).get(user_profile).get(user_math).get(user_day).get('description')}:\n\n"
            f"{days.get(user_class).get(user_profile).get(user_math).get(user_day).get('classes')}",
            parse_mode='HTML', reply_markup=nav_btns.back_to_mm)
    except:
        await c.answer('Ошибка')


# 4
async def user_schedule_choose_day(c: CallbackQuery, state: FSMContext, callback_data: typing.Dict[str, str]):
    await state.update_data(user_math=callback_data['math'])
    await c.message.edit_text('Выбери день недели', reply_markup=choose_btns.user_choose_day)


# 1
async def user_schedule_choose_class(c: CallbackQuery, state: FSMContext):
    await c.answer()
    await c.message.edit_text('Выбери класс', reply_markup=choose_btns.user_choose_class)
    await Schedule.choose_profile.set()


# 2
async def user_schedule_choose_profile(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await c.answer()
    await state.update_data(user_class=callback_data['classes'])
    if int(callback_data['classes']) == 11:
        await c.message.edit_text('Выбери профиль', reply_markup=choose_btns.user_choose_profile_11)
    else:
        await c.message.edit_text('Выбери профиль', reply_markup=choose_btns.user_choose_profile_10)
    await Schedule.next()


# 3
async def user_schedule_choose_math(c: CallbackQuery, state: FSMContext, callback_data: typing.Dict[str, str]):
    await c.answer()
    await state.update_data(user_profile=callback_data['profile'])
    data = await state.get_data()
    if data['user_class'] == '11':
        if callback_data['profile'] == 'fm':
            await Schedule.next()
            callback_data['math'] = 'prof'
            await user_schedule_choose_day(c, state, callback_data)
        else:
            await Schedule.next()
            await c.message.edit_text('Выбери уровень математики', reply_markup=choose_btns.user_choose_math)
    else:
        await Schedule.next()
        callback_data['math'] = 'None'
        await user_schedule_choose_day(c, state, callback_data)


async def make_schedule(c: CallbackQuery, state: FSMContext, user_class, user_profile, user_math, user_date):
    await c.answer()
    await user_usage(c.from_user.id)
    if user_class == '11':
        markup = make_buttons()
    else:
        markup = nav_btns.back_to_mm
    try:
        await c.message.edit_text(
            f"{days.get(user_class).get(user_profile).get(user_math).get(user_date).get('description')}\n\n"
            f"{days.get(user_class).get(user_profile).get(user_math).get(user_date).get('classes')}",
            parse_mode='HTML', reply_markup=markup)
        await state.set_state('other_schedule')
    except aiogram.exceptions.MessageNotModified:
        pass


async def user_schedule_recent(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext, *kwargs):
    data = ctx_data.get()
    repo = data.get("repo")
    udata = await repo.get_schedule(c.from_user.id)
    user_class = str(udata['user_class'])
    user_profile = str(udata['user_prof'])
    user_math = str(udata['user_math'])
    if callback_data['day'] == 'today':
        user_date = str(datetime.date.today().isoweekday())
    else:
        user_date = datetime.date.today() + datetime.timedelta(days=1)
        user_date = str(user_date.isoweekday())
    await state.update_data(user_class=user_class, user_profile=user_profile, user_math=user_math,
                            user_date=user_date)
    await make_schedule(c, state, user_class, user_profile, user_math, user_date)


async def other_schedule11(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    data = await state.get_data()
    try:
        user_class = str(data['user_class'])
        user_date = str(data['user_date'])
        user_profile = callback_data['profile']
        user_math = callback_data['math']
        await c.answer()
        await make_schedule(c, state, user_class, user_profile, user_math, user_date)
    except:
        await c.answer('Ошибка!\nВернитесь в главное меню')


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=['start'], state='*')
    dp.register_callback_query_handler(user_schedule_choose_class, text='schedule', state='*')
    dp.register_callback_query_handler(user_schedule_choose_profile, classes.filter(), state=Schedule.choose_profile)
    dp.register_callback_query_handler(user_schedule_choose_math, profile.filter(), state=Schedule.choose_math)
    dp.register_callback_query_handler(user_schedule_choose_day, math.filter(), state=Schedule.choose_day)
    dp.register_callback_query_handler(get_schedule, week.filter(), state=Schedule.choose_day)
    dp.register_callback_query_handler(user_schedule_recent, recent_schedule.filter(), state='*')
    dp.register_callback_query_handler(other_schedule11, profile_other.filter(), state='*')
