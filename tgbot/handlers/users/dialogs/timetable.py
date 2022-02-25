import logging
import operator
from typing import Any

from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Select, Group, Back, Cancel, Button
from aiogram_dialog.widgets.text import Format

from tgbot.handlers.users.dialogs.getters import Getter
from tgbot.handlers.users.dialogs.registration import on_grade_selected
from tgbot.states.states import Timetablenew, FastTimetable


async def on_profile_selected_1(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    manager.current_context().dialog_data["profile"] = item_id
    await manager.dialog().next()


async def timetable_show(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    grade = int(manager.current_context().dialog_data.get("grade", None))
    profile = int(manager.current_context().dialog_data.get("profile", None))
    # math = int(manager.current_context().dialog_data['math'])
    date = manager.current_context().dialog_data["day"] = int(item_id)
    data = ctx_data.get()
    repo = data.get("repo")
    schedule = await repo.get_schedule(grade, profile, date)
    manager.current_context().dialog_data["timetable"] = schedule
    await repo.schedule_user_usage(manager.event.from_user.id)
    await manager.dialog().next()


async def fast_timetable_profile(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    logging.info(item_id)
    user_profile = item_id
    manager.current_context().dialog_data['user_profile'] = user_profile


async def fast_timetable_date(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    user_date = manager.current_context().dialog_data['user_date']
    if item_id:
        chosen_date = item_id
        if chosen_date == 'prev_date':
            user_date = user_date - 1
        elif chosen_date == 'next_date':
            user_date = user_date + 1

        if user_date == 8:
            user_date -= 7
        elif user_date == 0:
            user_date += 7

    manager.current_context().dialog_data['user_date'] = user_date


async def change_profile_visibility(c: CallbackQuery, widget: Any, manager: DialogManager):
    extended = not manager.current_context().dialog_data.get('profile_extended', None)
    manager.current_context().dialog_data['profile_extended'] = extended


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
                on_click=on_profile_selected_1
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
dialog_fast_timetable = Dialog(
    Window(
        Format('<pre>{timetable}</pre>'),
        Group(
            Select(
                Format('{item[0]}'),
                id='profile',
                item_id_getter=operator.itemgetter(1),
                items='profiles',
                on_click=fast_timetable_profile,

            ),
            width=2,
            when='extended'
        ),
        Group(
            Button(Format('Профили'), id='btn_profiles', on_click=change_profile_visibility),
        ),
        Group(
            Select(
                Format('{item[0]}'),
                id='day1',
                item_id_getter=operator.itemgetter(1),
                items='days',
                on_click=fast_timetable_date,

            ),
            width=2
        ),
        Group(

            Cancel(Format('🔝 В главное меню')),
            width=2,
        ),
        state=FastTimetable.main,
        getter=Getter.fast_timetable_getter
    ),
)
