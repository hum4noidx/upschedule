import logging
import operator
from typing import Any

from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Select, Group, Back
from aiogram_dialog.widgets.text import Const, Format

from tgbot.keyboards import nav_btns


class DialogSG(StatesGroup):
    greeting = State()
    school = State()
    grade = State()
    profile = State()
    math = State()
    finish = State()
    age = State()


async def get_data1(dialog_manager: DialogManager, **kwargs):
    age = dialog_manager.current_context().dialog_data.get("age", None)
    name = dialog_manager.current_context().dialog_data.get("full_name", None)
    user_id = int(dialog_manager.current_context().dialog_data.get("user_id", None))

    data = ctx_data.get()
    repo = data.get("repo")
    schools = await repo.get_schools()
    await repo.add_user(user_id, name)
    return {
        "name": dialog_manager.current_context().dialog_data.get("name", ""),
        "age": age,
        "can_smoke": age in ("18-25", "25-40", "40+"),
        "schools": schools,

    }


async def get_data2(dialog_manager: DialogManager, **kwargs):
    school = dialog_manager.current_context().dialog_data.get("school", None)
    print(school)
    data = ctx_data.get()
    repo = data.get("repo")
    grades = await repo.get_grades(school)

    return {
        "name": dialog_manager.current_context().dialog_data.get("name", ""),
        "grades": grades,

    }


async def get_data3(dialog_manager: DialogManager, **kwargs):
    grade = dialog_manager.current_context().dialog_data.get("grade", None)
    print(grade)
    data = ctx_data.get()
    repo = data.get("repo")
    profiles = await repo.get_profiles(grade)

    return {
        "name": dialog_manager.current_context().dialog_data.get("name", ""),
        "profiles": profiles,

    }


async def get_data4(dialog_manager: DialogManager, **kwargs):
    math = dialog_manager.current_context().dialog_data.get("profile", None)
    print(math)
    data = ctx_data.get()
    repo = data.get("repo")
    math = await repo.get_maths()

    return {
        "name": dialog_manager.current_context().dialog_data.get("name", ""),
        "maths": math,

    }


async def name_handler(c: CallbackQuery, button: Button, manager: DialogManager):
    manager.current_context().dialog_data["name"] = c.from_user.full_name
    manager.current_context().dialog_data["user_id"] = c.from_user.id
    await manager.dialog().next()


async def on_school_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    logging.info(f'School selected: {item_id}')
    manager.current_context().dialog_data["school"] = item_id
    await manager.dialog().next()


async def on_grade_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    logging.info(f'Grade selected: {item_id}')
    manager.current_context().dialog_data["grade"] = item_id
    await manager.dialog().next()


async def on_profile_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    logging.info(f'Profile selected: {item_id}')
    manager.current_context().dialog_data["profile"] = item_id
    await manager.dialog().next()


async def on_math_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    logging.info(f'Math selected: {item_id}')
    manager.current_context().dialog_data["math"] = item_id
    await c.message.edit_text("Успешная регистрация", reply_markup=nav_btns.back_to_mm)
    school = int(manager.current_context().dialog_data['school'])
    grade = int(manager.current_context().dialog_data['grade'])
    profile = int(manager.current_context().dialog_data['profile'])
    math = int(manager.current_context().dialog_data['math'])
    user_id = int(manager.current_context().dialog_data['user_id'])
    await manager.done()
    data = ctx_data.get()
    repo = data.get("repo")
    await repo.register_user(school, grade, profile, math, user_id)


dialog = Dialog(
    Window(
        Const('Hi!'),
        Button(Const('Go!'), 'b1', on_click=name_handler),
        state=DialogSG.greeting,
    ),
    Window(
        Format("{name}! Из какой ты школы?"),
        Group(
            Select(
                Format('{item[0]}'),
                id='school',
                item_id_getter=operator.itemgetter(1),
                items='schools',
                on_click=on_school_selected
            ),
            width=1
        ),
        state=DialogSG.school,
        getter=get_data1,
    ),
    Window(
        Format("Класс:"),
        Group(
            Select(
                Format('{item[0]} класс'),
                id='grade',
                item_id_getter=operator.itemgetter(1),
                items='grades',
                on_click=on_grade_selected
            ),
            width=2
        ),
        Back(Const("Назад")),
        state=DialogSG.grade,
        getter=get_data2,

    ),
    Window(
        Format("Профиль:"),
        Group(
            Select(
                Format('{item[0]}'),
                id='profile',
                item_id_getter=operator.itemgetter(1),
                items='profiles',
                on_click=on_profile_selected
            ),
            width=2
        ),
        Back(Const("Назад")),
        state=DialogSG.profile,
        getter=get_data3,

    ),
    Window(
        Format("Уровень математики:"),
        Group(
            Select(
                Format('{item[0]}'),
                id='profile',
                item_id_getter=operator.itemgetter(1),
                items='maths',
                on_click=on_math_selected
            ),
            width=2
        ),
        Back(Const("Назад")),
        state=DialogSG.math,
        getter=get_data4,

    ),

)


async def start(m: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(DialogSG.greeting, )


def dialogs(dp: Dispatcher):
    dp.register_message_handler(start, text="/s", state="*")
