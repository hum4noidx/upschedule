import operator
from typing import Any

from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, Select, Cancel
from aiogram_dialog.widgets.text import Const, Format

from tgbot.handlers.dialogs.getters import Getter
from tgbot.states.states import HoroscopeSG


async def on_horoscope_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    manager.current_context().dialog_data["sign"] = item_id
    db = ctx_data.get().get('repo')
    await db.update_user_horoscope_sign(item_id, c.from_user.id)


horoscopes = Dialog(
    Window(
        Const('По просьбам трудящихся...'),
        Const('Выбери свой знак зодиака'),
        Group(
            Select(
                Format('{item[0]} класс'),
                id='sign',
                item_id_getter=operator.itemgetter(1),
                items='signs',
                on_click=on_horoscope_selected
            ),
            Cancel(Const('В главное меню')),
        ),
        state=HoroscopeSG.main,
        getter=Getter.get_horoscope_signs
    ),
    Window(
        Const('Теперь можно вернуться в главное меню'),
        Cancel('В главное меню'),
        state=HoroscopeSG.Confirm,
    )
)
