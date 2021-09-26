from aiogram import types

from data.shedule import days
from keyboards.inline import nav_btns


async def get_user_math_10(call: types.CallbackQuery):
    await call.message.edit_text("Выбери день недели:", reply_markup=nav_btns.choose_day)
    await call.answer()


async def choose_day10(call: types.CallbackQuery, user_data, day_data):
    await call.message.edit_text(
        f"{days.get(user_data['user_class']).get(user_data['profile']).get(day_data).get('description')}:\n\n"
        f"{days.get(user_data['user_class']).get(user_data['profile']).get(day_data).get('classes')}",
        reply_markup=nav_btns.cancel_today)
    await call.answer()


async def today_sch_10(call:types.CallbackQuery, user_class, user_prof, date):
    try:
        await call.message.edit_text(
            f"{days.get(user_class).get(user_prof).get(date).get('description')}:\n\n"
            f"{days.get(user_class).get(user_prof).get(date).get('classes')}",
            reply_markup=nav_btns.cancel_today)
        await call.answer()
    except Exception:
        await call.answer('Ошибка!', show_alert=True)