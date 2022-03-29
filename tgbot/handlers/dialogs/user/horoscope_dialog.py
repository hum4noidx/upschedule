import operator

from aiogram.dispatcher.handler import ctx_data
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, Select, Cancel, Back
from aiogram_dialog.widgets.text import Const, Format

from tgbot.handlers.dialogs.misc.getters import Getter
from tgbot.states.states import HoroscopeSG


async def on_horoscope_selected(manager: DialogManager, item_id: str):
    manager.current_context().dialog_data["sign"] = item_id
    db = ctx_data.get().get('repo')
    manager.current_context().dialog_data['horoscope_text'] = await db.get_horoscope_texts(item_id)
    await manager.dialog().next()


horoscopes = Dialog(
    Window(
        Const('Зачем я это делаю...'),
        Group(
            Select(
                Format('{item[0]}'),
                id='sign',
                item_id_getter=operator.itemgetter(1),
                items='signs',
                on_click=on_horoscope_selected
            ),
            Cancel(Const('В главное меню')),

            width=2
        ),
        state=HoroscopeSG.main,
        getter=Getter.get_horoscope_signs
    ),
    Window(
        Format('{text}'),
        Back(Const('Назад')),
        state=HoroscopeSG.text,
        getter=Getter.get_horoscope_text
    )
)
