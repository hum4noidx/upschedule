import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Group, Select, Cancel, Back
from aiogram_dialog.widgets.text import Const, Format

from tgbot.handlers.dialogs.getters import Getter
from tgbot.handlers.dialogs.registration import on_grade_selected, on_profile_selected
from tgbot.states.states import BroadcastSG

dialog_broadcaster = Dialog(
    Window(
        Const('Кому будем рассылать?'),
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
        Cancel(Format('🔝 Назад')),
        state=BroadcastSG.choose_class,
        getter=Getter.get_user_grades
    ),
    Window(
        Format('{grade}\nПрофиль/буква класса:'),
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
        getter=Getter.get_profiles,
        state=BroadcastSG.choose_profile
    ),
)
