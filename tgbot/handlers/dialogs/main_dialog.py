from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.kbd import Group, Start, Button, Row
from aiogram_dialog.widgets.text import Const, Format

from tgbot.handlers.dialogs.getters import Getter
from tgbot.handlers.dialogs.registration import name_handler
from tgbot.states.states import MainSG, RegSG, Timetablenew, FastTimetable, UserSettings, AdminPanelSG

dialog_main = Dialog(
    Window(
        Format('Привет!'),
        Button(Const('➡️ Вперед'), id='main_menu', on_click=name_handler),
        state=MainSG.greeting,
    ),
    Window(
        Format('<b>Главное меню</b>\n{name}', when='registered'),
        Group(
            Start(Const('Расписание'), id='utimetable', state=Timetablenew.choose_class),
            Row(Start(Const('Настройки'), id='usettings', state=UserSettings.profile),
                Start(Const('Админка'), id='admin_panel', state=AdminPanelSG.main, when='admin'), ),
            Start(Format('Сегодня [{date}]'), id='now', data={'date': 'now'}, state=FastTimetable.main),
            Start(Format('Завтра [{next_date}]'), id='next_day', data={'date': 'next_day'}, state=FastTimetable.main),
            when='registered'
        ),
        Format('Бот обновился. Теперь регистрация обязательна', when='not_registered'),
        # Format('Необходима регистрация', when='not_registered'),
        Group(
            Start(Const('Регистрация'), id='register', state=RegSG.school, when='not_registered'),
        ),
        state=MainSG.main_menu,
        getter=Getter.check_exists,
    ),
)


async def start(c: CallbackQuery, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(MainSG.greeting, mode=StartMode.RESET_STACK)


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_callback_query_handler(start, text='go_main', state='*')
