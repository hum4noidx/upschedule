import datetime
import typing

from aiogram import types

from data.shedule import days
from keyboards.inline import nav_btns
from keyboards.inline.admin_btns import vip_schedule
from loader import dp
from utils.db_api.db import DBComm


# Расписание на сегодняшний день и на завтра
@dp.callback_query_handler(vip_schedule.filter(), state="*")
async def today_sch(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    data = await DBComm.get_schedule()
    await DBComm.db_usage()
    if data['user_class'] and data['prof'] and data['math'] is not None:
        user_class = str(data['user_class'])
        user_prof = str(data['prof'])
        user_math = str(data['math'])
        if callback_data['vipday'] == 'today':
            date = str(datetime.date.today().isoweekday())
        else:
            date = datetime.date.today() + datetime.timedelta(days=1)
            date = str(date.isoweekday())
        try:
            await call.message.edit_text(
                f"{days.get(user_class).get(user_prof).get(user_math).get(date).get('description')}:\n\n"
                f"{days.get(user_class).get(user_prof).get(user_math).get(date).get('classes')}",
                reply_markup=nav_btns.cancel_today)
            await call.answer()
        except Exception:
            await call.answer('Ошибка!', show_alert=True)
    else:
        await call.answer("Необходима регистрация", show_alert=True)
