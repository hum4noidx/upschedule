import typing

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.kbd import Group, Start, Button
from aiogram_dialog.widgets.text import Const, Format

from tgbot.handlers.admins.admin import greeting
from tgbot.handlers.dialogs.misc.getters import Getter
from tgbot.handlers.dialogs.misc.horoscope_parser import main
from tgbot.handlers.dialogs.user.registration import name_handler
from tgbot.keyboards import nav_btns
from tgbot.states.states import MainSG, RegSG, FastTimetable


async def user_usage(user_id):
    data = ctx_data.get()
    repo = data.get("repo")
    await repo.update_user_usage(user_id)


dialog_main = Dialog(
    Window(
        Format('Привет!'),
        Button(Const('➡️ Вперед'), id='main_menu', on_click=name_handler),
        state=MainSG.greeting,
    ),
    Window(
        Format('<b>Главное меню</b>\n{name}', when='registered'),
        Group(
            # Start(Const('Расписание'), id='utimetable', state=Timetablenew.choose_class),

            Start(Format('Сегодня [{date}]'), id='now', data={'date': 'now'}, state=FastTimetable.main),
            Start(Format('Завтра [{next_date}]'), id='next_day', data={'date': 'next_day'}, state=FastTimetable.main),
            when='registered'
        ),
        Format('Необходима регистрация', when='not_registered'),
        Group(
            Start(Const('Регистрация'), id='register', state=RegSG.school, when='not_registered'),
        ),
        state=MainSG.main_menu,
        getter=Getter.check_exists,
    ),
)


async def main_menu(c: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await c.message.edit_text(f'<b>Главное меню</b>\n{await greeting(c.from_user.id)}\n',
                              reply_markup=nav_btns.main_menu, disable_web_page_preview=True, parse_mode='HTML')


async def donut_info(message: Message):
    await message.answer('Привет!\nЭтот бот работает на некоммерческой основе и требует средства на свое '
                         'обслуживание(хостинг)\n'
                         'Если он действительно полезный - поддержи его работу.', reply_markup=nav_btns.donut)


async def user_feedback(c: CallbackQuery):
    await c.answer(
        'Из-за изменений в коде бота могут возникать ошибки при нажатии на кнопки предыдущих сообщений. '
        '\nУдалите все предыдущие сообщения, пожалуйста')


async def show_help_info(m: Message):
    await m.answer(f'<b>Информация</b>\n'
                   f'Исходный код - <a href="https://github.com/hum4noidx/1208bot">ссылка</a>\n'
                   f'По всем вопросам - <a href="tg://user?id=713870562">тык</a>', parse_mode='HTML',
                   disable_web_page_preview=True)


async def test(m: Message, **kwargs):
    # await m.answer('т', reply_markup=await make_buttons_class())
    await main(m)
    print('test')


async def test1(c: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    pass


async def start(c: CallbackQuery, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(MainSG.greeting, mode=StartMode.RESET_STACK)


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(donut_info, commands='donut', state='*')
    dp.register_message_handler(show_help_info, commands=['help'], state='*')
    dp.register_message_handler(test, commands=['y'], state='*')
    dp.register_callback_query_handler(test, state='*')
    dp.register_callback_query_handler(user_feedback, text='notification', state='*')

# TODO: переписать названия функций на нормальный язык
