import typing

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from data.shedule import days
from handlers.users.main10 import choose_day10, get_user_math_10
from keyboards.inline import nav_btns, vip_btns, admin_btns
from keyboards.inline.nav_btns import classes, math, prof, week
from loader import dp, bot
from states.states import Main
from utils.db_api.db import DBMain, DBAdmin


@dp.message_handler(CommandStart(), state="*")
async def bot_start(call: types.CallbackQuery):
    await call.answer(f"Привет, {call.from_user.full_name}!", reply_markup=nav_btns.go_main_menu)
    if not await DBMain.db_user_exists():
        await DBMain.db_new_user()
        await bot.send_message(
            text=f'Новый пользователь - <a href="tg://user?id={call.from_user.id}">{call.from_user.full_name}</a>',
            chat_id=713870562)
    else:
        await DBMain.db_usage()


@dp.callback_query_handler(text="go_main", is_admin1=True, state="*")
async def main_menu_admin(call: types.CallbackQuery):
    await call.message.edit_text("🔴Админ панель🔴", reply_markup=admin_btns.main_admin_panel)


@dp.callback_query_handler(text="go_main", is_vip=True, state="*")
async def main_menu_vip(call: types.CallbackQuery):
    await call.message.edit_text("Главное меню VIP", reply_markup=vip_btns.main_vip_panel)


@dp.callback_query_handler(text="go_main", is_vip=False, state="*")
async def main_menu(call: types.CallbackQuery):
    await call.message.edit_text("Главное меню", reply_markup=nav_btns.main_menu)
    await call.answer()


@dp.callback_query_handler(text="main_schedule", state="*")
async def choose_class(call: types.CallbackQuery):
    await Main.main.set()
    await DBMain.db_usage()
    await call.message.edit_text("<b>Выбери класс</b>", reply_markup=nav_btns.choose_class)
    await call.answer()


@dp.callback_query_handler(classes.filter(), state=Main.main)
async def choose_profile(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await state.update_data(user_class=callback_data['classes'])
    if callback_data['classes'] == '11':
        await call.message.edit_text("Выбор профиля", reply_markup=nav_btns.choose_profile11)
        await call.answer()
    else:
        await call.message.edit_text("Выбор профиля", reply_markup=nav_btns.choose_profile10)
        await call.answer()


@dp.callback_query_handler(prof.filter(), state=Main.main)
async def choose_letter(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await state.update_data(profile=callback_data['profile'])
    data = await state.get_data()
    if data['user_class'] == '11':
        await call.message.edit_text('Уровень математики:', reply_markup=nav_btns.choose_math)
        await call.answer()
    else:
        await get_user_math_10(call)


@dp.callback_query_handler(math.filter(), state=Main.main)
async def get_user_math(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await state.update_data(math=callback_data['math'])
    await call.message.edit_text("Выбери день недели:", reply_markup=nav_btns.choose_day)
    await call.answer()


@dp.callback_query_handler(week.filter(), state=Main.main)
async def choose_day9(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    day_data = callback_data['day']
    user_data = await state.get_data()
    if user_data['user_class'] == '11':
        try:
            await call.message.edit_text(
                f"{days.get(user_data['user_class']).get(user_data['profile']).get(user_data['math']).get(day_data).get('description')}:\n\n"
                f"{days.get(user_data['user_class']).get(user_data['profile']).get(user_data['math']).get(day_data).get('classes')}",
                reply_markup=nav_btns.cancel_today)
        except:
            await call.answer('Ошибка')
    else:
        await choose_day10(call, user_data, day_data)
    await call.answer()
