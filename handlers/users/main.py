import typing

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from data.shedule import days
from keyboards.inline import nav_btns, admin_btns
from keyboards.inline.nav_btns import classes, math, prof, week
from loader import dp, bot
from states.states import Main
from utils.db_api.db import DBComm


@dp.message_handler(CommandStart(), state="*")
async def bot_start(call: types.CallbackQuery):
    await call.answer(f"Привет, {call.from_user.full_name}!", reply_markup=nav_btns.go_main_menu)
    if not await DBComm.db_user_exists():
        await DBComm.db_new_user()
        await bot.send_message(text=f'Новый пользователь - <a href="tg://user?id={call.from_user.id}">{call.from_user.full_name}</a>',
                               chat_id=713870562)
    else:
        await DBComm.db_usage()


@dp.callback_query_handler(text="go_main", is_vip=True, state="*", )
async def main_menu_vip(call: types.CallbackQuery):
    await call.message.edit_text("Главное меню VIP", reply_markup=admin_btns.main_admin_panel)


@dp.callback_query_handler(text="go_main", is_vip=False, state="*")
async def main_menu(call: types.CallbackQuery):
    await call.message.edit_text("Главное меню", reply_markup=nav_btns.main_menu)
    await call.answer()


@dp.callback_query_handler(text="main_schedule", state="*")
async def choose_class(call: types.CallbackQuery):
    await Main.main.set()
    await DBComm.db_usage()
    await call.message.edit_text("<b>Выбери класс</b>", reply_markup=nav_btns.choose_class)
    await call.answer()


@dp.callback_query_handler(classes.filter(), state=Main.main)
async def choose_profile(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await state.update_data(user_class=callback_data['classes'])
    await call.message.edit_text("Выбор профиля", reply_markup=nav_btns.choose_profile)
    await call.answer()


@dp.callback_query_handler(prof.filter(), state=Main.main)
async def choose_letter(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await state.update_data(profile=callback_data['profile'])
    await call.message.edit_text('Уровень математики:', reply_markup=nav_btns.choose_math)
    await call.answer()


@dp.callback_query_handler(math.filter(), state=Main.main)
async def get_user_math(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await state.update_data(math=callback_data['math'])
    await call.message.edit_text("Выбери день недели:", reply_markup=nav_btns.choose_day)
    await call.answer()


@dp.callback_query_handler(week.filter(), state=Main.main)
async def choose_day9(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    day_data = callback_data['day']
    user_data = await state.get_data()
    try:
        await call.message.edit_text(
            f"{days.get(user_data['user_class']).get(user_data['profile']).get(user_data['math']).get(day_data).get('description')}:\n\n"
            f"{days.get(user_data['user_class']).get(user_data['profile']).get(user_data['math']).get(day_data).get('classes')}",
            reply_markup=nav_btns.cancel_today)
    except:
        await call.answer('Ошибка')
    await call.answer()
