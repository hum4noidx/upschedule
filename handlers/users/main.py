import datetime
import typing

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from data.shedule import days
from handlers.admin_panel.admin_panel import reset_state
from keyboards.inline import nav_btns, admin_btns
from keyboards.inline.nav_btns import classes, letter, d_o_week, math
from loader import dp
from states.states import Main
from utils.db_api.db import DBComm
from utils.notify_admins import subscriber


@dp.message_handler(CommandStart(), state="*")
async def bot_start(call: types.CallbackQuery):
    await call.answer(f"Привет, {call.from_user.full_name}!", reply_markup=nav_btns.start_btn)
    if not await DBComm.db_user_exists():
        await DBComm.db_new_user()
        await subscriber()
    else:
        await DBComm.db_usage()


@dp.message_handler(commands="support", state="*")
async def bot_support(call: types.CallbackQuery):
    await call.answer("Связь с администратором - t.me/hum4noidx")


@dp.callback_query_handler(text='cancel', state="*", is_vip=True)
async def cancel_vip_panel(call: types.CallbackQuery):
    await main_menu_vip(call)
    await reset_state(call)


@dp.callback_query_handler(text='cancel', state="*", is_vip=False)
async def cancel_vip_panel(call: types.CallbackQuery):
    await main_menu(call)
    await reset_state(call)


@dp.callback_query_handler(text="cancel_to_class", state="*")
async def cancel_to_class(call: types.CallbackQuery):
    await choose_class(call)


@dp.callback_query_handler(text="start", state="*", is_vip=True)
async def main_menu_vip(call: types.CallbackQuery):
    await call.message.edit_text("Главное меню VIP", reply_markup=admin_btns.main_admin_panel)


@dp.callback_query_handler(text="start", is_vip=False, state="*")
async def main_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("Главное меню", reply_markup=nav_btns.main_menu)


@dp.callback_query_handler(text="main_schedule", state="*")
async def choose_class(call: types.CallbackQuery):
    await Main.main.set()
    await call.answer()
    await DBComm.db_usage()
    await call.message.edit_text("<b>Выбери класс</b>", reply_markup=nav_btns.choose_class)


@dp.callback_query_handler(classes.filter(), state=Main.main)
async def choose_profile(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    # await Main.choose_profile.set()
    async with state.proxy() as data:
        data['classes'] = callback_data['classes']
    chosen_class = int(data['classes'])

    if chosen_class > 9:
        await call.message.edit_text("Выбор профиля", reply_markup=nav_btns.choose_profile)
    else:
        await call.message.edit_text("Выбор буквы", reply_markup=nav_btns.choose_letter)

    await call.answer()


@dp.callback_query_handler(letter.filter(), state=Main.main)
async def choose_letter(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    async with state.proxy() as data:
        data['letter'] = callback_data['letter']
    if callback_data['letter'] == ['a', 'b', 'v']:
        await call.message.edit_text("Выбери день недели:", reply_markup=nav_btns.choose_day)
    else:
        await call.message.edit_text('Уровень математики:', reply_markup=nav_btns.choose_math)
    await call.answer()


@dp.callback_query_handler(math.filter(), state=Main.main)
async def get_user_math(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    async with state.proxy() as data:
        data['math'] = callback_data['math']
    await call.message.edit_text("Выбери день недели:", reply_markup=nav_btns.choose_day)


@dp.callback_query_handler(d_o_week.filter(), state=Main.main)
async def choose_day9(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    day_data = callback_data['day']
    async with state.proxy() as data:
        classes = data['classes']
        letter = data['letter']
        user_math = data['math']
        await call.message.edit_text(
            f"{days.get(classes).get(letter).get(user_math).get(day_data).get('description')}:\n\n"
            f"{days.get(classes).get(letter).get(user_math).get(day_data).get('classes')}",
            reply_markup=nav_btns.cancel_today)
        await call.answer()


# Расписание на сегодня
@dp.callback_query_handler(text="today_schedule", state="*")
async def today_sch(call: types.CallbackQuery):
    data = await DBComm.get_schedule()
    if data['user_class'] and data['prof'] is not None:
        user_class = str(data['user_class'])
        user_prof = str(data['prof'])
        if data['math'] is None:
            user_math = 'prof'
        else:
            user_math = str(data['math'])
        date = str(datetime.date.today().isoweekday())
        await DBComm.db_usage()
        await call.message.edit_text(
            f"{days.get(user_class).get(user_prof).get(user_math).get(date).get('description')}:\n\n"
            f"{days.get(user_class).get(user_prof).get(user_math).get(date).get('classes')}",
            reply_markup=nav_btns.cancel_today)
        await call.answer()
    else:
        await call.answer("Необходима регистрация", show_alert=True)
