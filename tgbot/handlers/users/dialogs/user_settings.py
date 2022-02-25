from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Group
from aiogram_dialog.widgets.text import Format

from tgbot.handlers.users.dialogs.getters import Getter
from tgbot.states.states import UserSettings

dialog_user_settings = Dialog(
    Window(
        Format('{settings}'),
        Group(

        ),
        getter=Getter.settings_getter,
        state=UserSettings.profile
    ),
    Window(),
)
