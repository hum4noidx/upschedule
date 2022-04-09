from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, Button, Start, Cancel, Back
from aiogram_dialog.widgets.text import Const, Format

from tgbot.handlers.dialogs.misc.getters import Getter
from tgbot.states.states import AdminPanelSG, BroadcastSG


async def on_click_users_list(c: CallbackQuery, button: Button, manager: DialogManager):
    db = ctx_data.get().get('repo')
    manager.current_context().dialog_data["users_list"] = f'<pre>{await db.get_users_list()}</pre>'
    await manager.dialog().next()


dialog_admin = Dialog(
    Window(
        Format('Админка'),
        Group(
            Start(Const('Рассылка'), id='broadcast', state=BroadcastSG.choose_class),
            Button(Format('Пользователи [{count}]'), id='users', on_click=on_click_users_list),
        ),
        Cancel(Format('🔝 В главное меню')),

        getter=Getter.get_users_count,
        state=AdminPanelSG.main
    ),
    Window(
        Format('{users_list}'),
        Back(Const("Назад")),
        getter=Getter.get_users_list,
        state=AdminPanelSG.users_list
    )
)
