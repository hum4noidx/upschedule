import typing
from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline import reg_btns
from utils.db_api.db import DBComm
from states.states import Register
from keyboards.inline.reg_btns import register_class, register_profile, register_math


@dp.callback_query_handler(text="reg_cancel_to_class", state="*")
async def reg_cancel_to_class(call: types.CallbackQuery):
    await reg_class(call)
    await Register.choose_class.set()


@dp.callback_query_handler(text="register", state="*")
async def register(call: types.CallbackQuery):
    await Register.main.set()
    await call.answer()
    await call.message.edit_text("<b>Такс, это регистрация.</b>\nТут можно указать свой класс и букву, чтобы в "
                                 "будущем не выбирать их.\nСтатус: WIP", reply_markup=reg_btns.register)
    await call.answer()


@dp.callback_query_handler(text="reg.choose_class", state=Register.main)
async def reg_class(call: types.CallbackQuery):
    await call.answer()
    await Register.choose_class.set()
    await call.message.edit_text("Выбор класса", reply_markup=reg_btns.select_classes)
    await call.answer()


@dp.callback_query_handler(register_class.filter(), state=Register.choose_class)
async def reg_class_filter(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    callback = callback_data['reg_classes']
    info = ""
    for c in callback:
        if c.isdigit():
            info = info + c
    await DBComm.reg_class(info)
    await Register.choose_profile.set()
    classes = int(info)
    if classes > 9:
        await call.message.edit_text("Выбери профиль", reply_markup=reg_btns.select_profiles)
    else:
        await call.message.edit_text("Выбери букву", reply_markup=reg_btns.select_letters)
    await call.answer()


@dp.callback_query_handler(register_profile.filter(), state=Register.choose_profile)
async def reg_class_filter(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    async with state.proxy() as data:
        data['profile'] = callback_data['reg_profile']
    await Register.choose_math.set()
    # await call.message.edit_text("Круто, ты зарегистрирован.", reply_markup=reg_btns.main_menu)
    await call.message.edit_text('Выбери уровень математики', reply_markup=reg_btns.select_math)
    await call.answer()


@dp.callback_query_handler(register_math.filter(), state=Register.choose_math)
async def register_math(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    math = callback_data['reg_math']
    async with state.proxy() as data:
        profile = data['profile']
    await DBComm.reg_profile(profile, math)
    await call.message.edit_text("Круто, ты зарегистрирован.", reply_markup=reg_btns.main_menu)
    await state.reset_state()