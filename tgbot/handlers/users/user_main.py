from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message, CallbackQuery

from tgbot.handlers.admins.admin import greeting
from tgbot.keyboards import nav_btns
from tgbot.services.repository import Repo


async def user_usage(user_id):
    data = ctx_data.get()
    repo = data.get("repo")
    await repo.schedule_user_usage(user_id)


async def user_start(m: Message, repo: Repo):
    await repo.add_user(m.from_user.id, m.from_user.full_name)
    await m.answer(f'<b>Hello, {m.from_user.full_name}!</b>\n'
                   f'<u>Это многофункциональный бот для школы.</u>\n'
                   f'При добавлении в группы автоматически удаляет сообщения о вступлении и выходе участников('
                   f'требуются права администратора)\n\n'
                   f'Для удобства пользования рекомендуется сразу выбрать класс и профиль.\n'
                   f'Для этого нажми кнопку \'Регистрация\'',
                   parse_mode="HTML", reply_markup=nav_btns.start)


async def main_menu(c: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await c.message.edit_text(f'<b>Главное меню</b>\n{await greeting(c.from_user.id)}\n'
                              f'<a href="https://t.me/upschedulebot">Rebranding</a>',
                              reply_markup=nav_btns.main_menu, parse_mode='HTML')


async def donut_info(message: Message):
    await message.answer('Привет!\nЭтот бот работает на некоммерческой основе и требует средства на свое '
                         'обслуживание(хостинг)\n'
                         'Если он действительно полезный - поддержи его работу.', reply_markup=nav_btns.donut)


async def user_feedback(c: CallbackQuery):
    await c.message.edit_text('Вопросы, замечания, предложения')


async def show_help_info(m: Message):
    await m.answer(f'<b>Информация</b>\n'
                   f'Исходный код - <a href="https://github.com/hum4noidx/1208bot">ссылка</a>\n'
                   f'По всем вопросам - <a href="tg://user?id=713870562">сюда</a>', parse_mode='HTML')


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=['start'], state='*')
    dp.register_message_handler(donut_info, commands='donut', state='*')
    dp.register_message_handler(show_help_info, commands=['help'], state='*')

# TODO: переписать названия функций на нормальный язык
