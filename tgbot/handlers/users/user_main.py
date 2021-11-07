import datetime
import random
import typing

import aiogram
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards import nav_btns, choose_btns
from tgbot.keyboards.choose_btns import classes, profile, math, week, make_buttons, profile_other, profile_other_day
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
    text = 'Главное меню'
    rand = random.randint(1, 5)
    if rand == 5:
        text = text + '\nЕсли понравился бот и есть желание поддержать проект - /donut'
    await c.message.edit_text(text, reply_markup=nav_btns.main_menu)


# # \____________________ SCHEDULE FUNCTIONS ____________________/
async def make_schedule(c: CallbackQuery, state: FSMContext, user_class,
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
            f"{days.get(user_class).get(user_profile).get(user_math).get(user_date).get('classes')}"
            ,
            parse_mode='HTML', reply_markup=markup)
        await state.set_state('other_schedule')
    except aiogram.exceptions.MessageNotModified:
        pass


async def get_schedule(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    user_data = await state.get_data()
    user_class = user_data['user_class']
    user_profile = user_data['user_profile']
    user_math = user_data['user_math']
    user_date = callback_data['day']
    await state.update_data(user_date=callback_data['day'])
    await make_schedule(c, state, user_class, user_profile, user_math, user_date)


async def user_schedule_choose_day(c: CallbackQuery, state: FSMContext, callback_data: typing.Dict[str, str]):
    await state.update_data(user_math=callback_data['math'])
    await c.message.edit_text('Выбери день недели', reply_markup=choose_btns.user_choose_day)


async def user_schedule_choose_class(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text('Выбери класс', reply_markup=choose_btns.user_choose_class)
    await Schedule.choose_profile.set()


async def user_schedule_choose_profile(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await c.answer()
    await state.update_data(user_class=callback_data['classes'])
    if int(callback_data['classes']) == 11:
        await c.message.edit_text('Выбери профиль', reply_markup=choose_btns.user_choose_profile_11)
    else:
        await c.message.edit_text('Выбери профиль', reply_markup=choose_btns.user_choose_profile_10)
    await Schedule.next()


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


async def user_schedule_recent_handler(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    data = ctx_data.get()
    repo = data.get("repo")
    user_data = await repo.get_schedule(c.from_user.id)
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
    await make_schedule(c, state, user_class, user_profile, user_math, user_date)


async def other_schedule_11(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
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
            elif date == 'next':
                user_date = user_date + 1
        if user_date == 8:
            user_date -= 7
        elif user_date == 0:
            user_date += 7
        user_date = str(user_date)
        await c.answer()

        await make_schedule(c, state, user_class, user_profile, user_math, user_date)
    except KeyError:
        await c.answer(
            'Ошибка!\nСкорее всего, это произошло из-за того, что вы долго оставались в этом меню.\n'
            'Вернитесь в главное меню', show_alert=True)


async def donut_info(message: Message):
    await message.answer('Привет!\nЭтот бот работает на некоммерческой основе и требует средства на свое '
                         'обслуживание(хостинг)\n'
                         'Если он действительно полезный - поддержи его работу.', reply_markup=nav_btns.donut)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=['start'], state='*')
    dp.register_callback_query_handler(user_schedule_choose_class, text='schedule', state='*')
    dp.register_callback_query_handler(user_schedule_choose_profile, classes.filter(), state=Schedule.choose_profile)
    dp.register_callback_query_handler(user_schedule_choose_math, profile.filter(), state=Schedule.choose_math)
    dp.register_callback_query_handler(user_schedule_choose_day, math.filter(), state=Schedule.choose_day)
    dp.register_callback_query_handler(get_schedule, week.filter(), state=Schedule.choose_day)
    dp.register_callback_query_handler(user_schedule_recent_handler, recent_schedule.filter(), state='*')
    dp.register_callback_query_handler(other_schedule_11, profile_other.filter(), state='*')
    dp.register_message_handler(donut_info, commands='donut', state='*')

# TODO: переписать названия функций на нормальный язык
