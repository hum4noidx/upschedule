from aiogram import Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.kbd import Group, Start, Button, Row
from aiogram_dialog.widgets.text import Const, Format

from tgbot.handlers.dialogs.misc.getters import Getter
from tgbot.handlers.dialogs.misc.horoscope_parser import main
from tgbot.handlers.dialogs.user.registration import name_handler
from tgbot.states.states import MainSG, RegSG, Timetablenew, FastTimetable, UserSettings, AdminPanelSG, HoroscopeSG

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
            Start(Const('ГоРоСкОп'), id='horoscopes', state=HoroscopeSG.main),
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


async def start(c: CallbackQuery, dialog_manager: DialogManager, **kwargs):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(MainSG.greeting, mode=StartMode.RESET_STACK)


async def test(m: Message):
    await main(m)
    # await broadcast_horoscopes(m, repo)


async def test1(m: Message):
    await m.answer(m)


async def restrict_usage_in_groups(m: Message):
    await m.reply(f'❗ Использование только в личных сообщениях с <a href="https://t.me/upschedulebot">ботом</a>',
                  disable_web_page_preview=True)


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*', chat_type=[types.ChatType.PRIVATE])
    dp.register_callback_query_handler(start, text='go_main', state='*', chat_type=[types.ChatType.PRIVATE])
    dp.register_message_handler(restrict_usage_in_groups, commands=['start', ''], state='*',
                                chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
    dp.register_message_handler(test, commands=['reload'], state='*')
    dp.register_message_handler(test1, commands=['test'], state='*')
