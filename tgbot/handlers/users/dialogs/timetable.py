import operator
from typing import Any

from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Select, Group, Back, Cancel
from aiogram_dialog.widgets.text import Format

from tgbot.handlers.users.dialogs.getters import Getter
from tgbot.handlers.users.dialogs.registration import on_grade_selected, on_profile_selected
from tgbot.states.states import Timetablenew, FastTimetable


async def on_math_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    manager.current_context().dialog_data["math"] = item_id
    await manager.dialog().next()


async def timetable_show(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    school = manager.current_context().dialog_data.get("school", None)
    grade = int(manager.current_context().dialog_data.get("grade", None))
    profile = int(manager.current_context().dialog_data.get("profile", None))
    math = int(manager.current_context().dialog_data['math'])
    date = manager.current_context().dialog_data["day"] = int(item_id)
    data = ctx_data.get()
    repo = data.get("repo")
    await manager.dialog().next()
    schedule = await repo.get_schedule(grade, profile, math, date)
    manager.current_context().dialog_data["timetable"] = schedule


dialog_timetable = Dialog(
    Window(
        Format('Выбери класс'),
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
        Cancel(Format('🔝 В главное меню')),
        state=Timetablenew.choose_class,
        getter=Getter.get_user_grades
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
        Group(
            Back(Format("🔙 Назад")),
            Cancel(Format('🔝 В главное меню')),
            width=2,
        ),

        state=Timetablenew.choose_profile,
        getter=Getter.get_profiles,

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
        Group(
            Back(Format("🔙 Назад")),
            Cancel(Format('🔝 В главное меню')),
            width=2,
        ),
        state=Timetablenew.choose_math,
        getter=Getter.get_maths,

    ),
    Window(
        Format("День недели:"),
        Group(
            Select(
                Format('{item[0]}'),
                id='day',
                item_id_getter=operator.itemgetter(1),
                items='days',
                on_click=timetable_show
            ),
            width=2
        ),
        Group(
            Back(Format("🔙 Назад")),
            Cancel(Format('🔝 В главное меню')),
            width=2,
        ),
        state=Timetablenew.choose_day,
        getter=Getter.get_days,

    ),
    Window(
        Format('<pre>{timetable}</pre>'),
        Group(
            Back(Format("🔙 Назад")),
            Cancel(Format('🔝 В главное меню')),
            width=2,
        ),
        state=Timetablenew.show_timetable,
        getter=Getter.get_timetable,

    ),

)
fast_timetable = Dialog(
    Window(
        Format('<pre>{timetable}</pre>'),
        Select(
            Format('{item[0]}'),
            id='btn',
            item_id_getter=operator.itemgetter(1),
            items='btns',
            on_click=timetable_show
        ),
        Group(
            Back(Format("🔙 Назад")),
            Cancel(Format('🔝 В главное меню')),
            width=2,
        ),
        state=FastTimetable.main,
        getter=Getter.fast_timetable_getter
    ),
)
