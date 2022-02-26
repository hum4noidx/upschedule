from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Group, Cancel, Start
from aiogram_dialog.widgets.text import Format, Const

from tgbot.handlers.users.dialogs.getters import Getter
from tgbot.states.states import UserSettings, RegSG

dialog_user_settings = Dialog(
    Window(
        Format('{settings}'),
        Group(
            Start(Const('Регистрация'), id='register', state=RegSG.school),
            Cancel(Format('🔝 В главное меню')),
        ),
        getter=Getter.settings_getter,
        state=UserSettings.profile
    ),
    Window(
        Format('NAME'),
        Cancel(),
        state=UserSettings.change_name
    ),
)
