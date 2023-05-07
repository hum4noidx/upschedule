from operator import attrgetter

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Select, Cancel
from aiogram_dialog.widgets.text import Const, Format

from tgbot.dialogs.registration.handlers import on_grade_selected
from tgbot.states.user_states import RegistrationSG

registration = Dialog(
    Window(
        Const('<b>🔧 Регистрация</b>'),
        Const('Для того, чтобы полноценно пользоваться ботом, необходимо пройти регистрацию.'),
        Const('Быстрее, чем в вк, обещаю!'),
        Const('<tg-spoiler>А есть что-то медленнее?</tg-spoiler>'),
        Const('Ближе к делу: выбери свой класс:'),
        Select(
            Format('{item.name}'),
            id='grade',
            item_id_getter=attrgetter('id'),
            items='grades',
            on_click=on_grade_selected,
        ),
        Cancel(Const('Отмена')),
        state=RegistrationSG.choose_grade,
    ),
    Window(
        Const('А я что говорил? Быстро же!'),
        state=RegistrationSG.success,
    ),
)
