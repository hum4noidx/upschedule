import typing

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.reg10 import register_math10
from keyboards.inline import reg_btns
from keyboards.inline.reg_btns import register_class, register_profile, register_math
from loader import dp
from states.states import Register
from utils.db_api.db import DBMain, DBRegistration


@dp.callback_query_handler(text="reg_cancel_to_class", state="*")
async def reg_cancel_to_class(call: types.CallbackQuery):
    await reg_class(call)
    await Register.choose_class.set()


@dp.callback_query_handler(text="register", state="*")
async def register(call: types.CallbackQuery):
    await Register.main.set()
    await call.answer()
    await call.message.edit_text("<b>Такс, это регистрация.</b>\nТут можно указать свой класс и букву, чтобы в "
                                 "будущем не выбирать их.", reply_markup=reg_btns.register)
    await call.answer()


@dp.callback_query_handler(text="reg.choose_class", state=Register.main)
async def reg_class(call: types.CallbackQuery):
    await call.answer()
    await Register.choose_class.set()
    await call.message.edit_text("Выбор класса", reply_markup=reg_btns.select_classes)
    await call.answer()


# TODO: Попробовать сделать регистрацию сначала
@dp.callback_query_handler(register_class.filter(), state=Register.choose_class)
async def reg_class_filter(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    callback = callback_data['reg_classes']
    info = ""
    for c in callback:
        if c.isdigit():
            info = info + c
    await DBRegistration.reg_class(info)
    await Register.choose_profile.set()
    async with state.proxy() as data:
        data['class'] = classes = int(info)
    if classes == 11:
        await call.message.edit_text("Выбери профиль", reply_markup=reg_btns.select_profiles11)
    else:
        await call.message.edit_text("Выбери профиль", reply_markup=reg_btns.select_profiles10)
    await call.answer()


@dp.callback_query_handler(register_profile.filter(), state=Register.choose_profile)
async def reg_class_filter(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    async with state.proxy() as data:
        profile = data['profile'] = callback_data['reg_profile']
        user_class = data['class']
    await Register.choose_math.set()
    if data['class'] == 11:
        await call.message.edit_text('Выбери уровень математики', reply_markup=reg_btns.select_math)
        await call.answer()
    elif data['class'] == 10:
        await register_math10(call, profile)


@dp.callback_query_handler(register_math.filter(), state=Register.choose_math)
async def register_math(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    math = callback_data['reg_math']
    async with state.proxy() as data:
        profile = data['profile']
        user_class = data['class']
    if user_class == 11:
        await DBRegistration.reg_profile(profile, math)
        await call.message.edit_text("Круто, ты зарегистрирован.", reply_markup=reg_btns.main_menu)
        await state.reset_state()
    else:
        await register_math10(call, profile)
