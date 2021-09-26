import datetime
import typing

from aiogram import types

from data.shedule import days
from handlers.users.main10 import today_sch_10
from keyboards.inline import nav_btns
from keyboards.inline.vip_btns import vip_schedule
from loader import dp
from utils.db_api.db import DBMain


# Расписание на сегодняшний день и на завтра
@dp.callback_query_handler(vip_schedule.filter(), state="*")
async def today_sch(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    data = await DBMain.get_schedule()
    await DBMain.db_usage()
    if data['user_class'] and data['prof'] and data['math'] is not None:
        user_class = str(data['user_class'])
        user_prof = str(data['prof'])
        user_math = str(data['math'])
        if callback_data['vipday'] == 'today':
            date = str(datetime.date.today().isoweekday())
        else:
            date = datetime.date.today() + datetime.timedelta(days=1)
            date = str(date.isoweekday())
        if user_class == '11':
            try:
                await call.message.edit_text(
                    f"{days.get(user_class).get(user_prof).get(user_math).get(date).get('description')}:\n\n"
                    f"{days.get(user_class).get(user_prof).get(user_math).get(date).get('classes')}",
                    reply_markup=nav_btns.cancel_today)
                await call.answer()
            except Exception:
                await call.answer('Ошибка!', show_alert=True)
        else:
            await today_sch_10(call, user_class, user_prof, date)
    else:
        await call.answer("Необходима регистрация", show_alert=True)
