import operator
from typing import Any

from aiogram import Dispatcher
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window, StartMode
from aiogram_dialog.widgets.kbd import Button, Select, Group, Back, Cancel
from aiogram_dialog.widgets.text import Const, Format

from tgbot.handlers.users.dialogs.getters import Getter
from tgbot.states.states import RegSG


async def name_handler(c: CallbackQuery, button: Button, manager: DialogManager):
    manager.current_context().dialog_data["name"] = c.from_user.full_name
    manager.current_context().dialog_data["user_id"] = c.from_user.id
    data = ctx_data.get()
    repo = data.get("repo")
    await repo.add_user(c.from_user.id, c.from_user.full_name)
    await manager.dialog().next()


async def on_school_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    manager.current_context().dialog_data["school"] = item_id
    manager.current_context().dialog_data["user_id"] = c.from_user.id
    await manager.dialog().next()


async def on_grade_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    manager.current_context().dialog_data["grade"] = item_id
    await manager.dialog().next()


async def on_profile_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    manager.current_context().dialog_data["profile"] = item_id
    school = int(manager.current_context().dialog_data['school'])
    grade = int(manager.current_context().dialog_data['grade'])
    profile = int(manager.current_context().dialog_data['profile'])
    user_id = int(manager.current_context().dialog_data['user_id'])
    await manager.dialog().next()
    data = ctx_data.get()
    repo = data.get("repo")
    await repo.register_user(school, grade, profile, user_id)


async def on_register_start(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.dialog().next()


async def on_math_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    manager.current_context().dialog_data["math"] = item_id


dialog_reg = Dialog(
    Window(
        Format("Из какой ты школы?"),
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
        getter=Getter.get_schools,
        state=RegSG.school,

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
        state=RegSG.grade,
        getter=Getter.get_grades,

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
        state=RegSG.profile,
        getter=Getter.get_profiles,

    ),
    # Window(
    #     Format("Уровень математики:"),
    #     Group(
    #         Select(
    #             Format('{item[0]}'),
    #             id='profile',
    #             item_id_getter=operator.itemgetter(1),
    #             items='maths',
    #             on_click=on_math_selected
    #         ),
    #         width=2
    #     ),
    #     Back(Const("Назад")),
    #     state=RegSG.math,
    #     getter=Getter.get_maths,
    #
    # ),
    Window(
        Format('Успешная регистрация'),
        Cancel(Const('Главное меню')),
        state=RegSG.finish
    ),

)


async def start(c: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(RegSG.school, mode=StartMode.RESET_STACK)


def dialogs(dp: Dispatcher):
    # dp.register_message_handler(user_start, commands=['start'], state='*')
    dp.register_message_handler(start, text="/s", state="*")
    dp.register_callback_query_handler(start, text=['user_register'], state="*")
