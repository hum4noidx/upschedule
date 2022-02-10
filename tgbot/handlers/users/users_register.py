import typing

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery

from tgbot.keyboards import nav_btns, choose_btns
from tgbot.keyboards.choose_btns import classes, profile, math
from tgbot.states.states import Register


async def user_end_registration(c: CallbackQuery, state: FSMContext, callback_data: typing.Dict[str, str]):
    user_data = await state.get_data()
    data = ctx_data.get()
    repo = data.get("repo")
    await c.answer()

    user_class = int(user_data.get('user_class'))
    user_prof = user_data.get('user_profile')
    userid = c.from_user.id
    if user_data.get('user_math') == 'None':
        user_math = user_data.get('user_math')
    else:
        user_math = callback_data['math']

    await repo.register_user(user_class, user_prof, user_math, userid)
    await state.reset_state()
    await c.message.edit_text('Регистрация успешна.', reply_markup=nav_btns.back_to_mm)


async def user_register(c: CallbackQuery):
    await c.message.edit_text('ℹ️Регистрация предоставляет доступ к функционалу расписания на сегодняшний и '
                              'завтрашний день[VIP].\n '
                              'Без нее эти функции работать не будут!',
                              reply_markup=nav_btns.user_confirm_register)
    await Register.choose_class.set()
    await c.answer()


async def user_register_class(c: CallbackQuery):
    await c.message.edit_text('Выбери класс', reply_markup=choose_btns.user_choose_class)
    await Register.choose_profile.set()
    await c.answer()


async def user_register_profile(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    # saving class data from user:
    await state.update_data(user_class=callback_data['classes'])
    if int(callback_data['classes']) == 11:
        await c.message.edit_text('Выбери профиль', reply_markup=choose_btns.user_choose_profile_11)
    elif int(callback_data['classes']) == 10:
        await c.message.edit_text('Выбери профиль', reply_markup=choose_btns.user_choose_profile_10)
    else:
        await c.message.edit_text('Выбери букву класса', reply_markup=choose_btns.user_choose_letter)
    await Register.choose_math.set()
    await c.answer()


async def user_register_math(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    # saving profile data from user:
    await state.update_data(user_profile=callback_data['profile'])
    data = await state.get_data()
    if data['user_class'] == '11':
        if callback_data['profile'] == 'fm':
            callback_data['math'] = 'prof'
            await user_end_registration(c, state, callback_data)
        else:
            await c.message.edit_text('Выбери уровень математики', reply_markup=choose_btns.user_choose_math)
    else:
        await state.update_data(user_math='None')
        await user_end_registration(c, state, callback_data)
    await Register.confirm.set()
    await c.answer()


def register_user_reg(dp: Dispatcher):
    # dp.register_callback_query_handler(user_register, text=['user_register'], state="*")
    dp.register_callback_query_handler(user_register_class, text=['reg.class'],
                                       state=Register.choose_class)
    dp.register_callback_query_handler(user_register_profile, classes.filter(),
                                       state=Register.choose_profile)
    dp.register_callback_query_handler(user_register_math, profile.filter(),
                                       state=Register.choose_math)
    dp.register_callback_query_handler(user_end_registration, math.filter(), state=Register.confirm)
