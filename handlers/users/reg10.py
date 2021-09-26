from aiogram import types

from aiogram import types

from keyboards.inline import reg_btns
from utils.db_api.db import DBRegistration


async def register_math10(call: types.CallbackQuery, profile):
    math = 'None'
    await DBRegistration.reg_profile(profile, math)
    await call.message.edit_text("Круто, ты зарегистрирован.", reply_markup=reg_btns.main_menu)
