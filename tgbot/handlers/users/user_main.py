import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards import nav_btns
from tgbot.services.repository import Repo


async def user_usage(user_id):
    data = ctx_data.get()
    repo = data.get("repo")
    await repo.schedule_user_usage(user_id)


async def user_start(m: Message, repo: Repo):
    await repo.add_user(m.from_user.id, m.from_user.full_name)
    await m.answer(f'<b>Hello, {m.from_user.full_name}!</b>\n'
                   f'<u>Это многофункциональный школьный бот</u>\n'
                   f'<b>Одни из возможностей:</b>\n'
                   f'При добавлении в группы автоматически удаляет сообщения о вступлении и выходе участников('
                   f'требуются права администратора)\n\n'
                   f'Для удобства пользования рекомендуется сразу выбрать класс и профиль.\n'
                   f'Для этого нажми кнопку \'Регистрация\'',
                   parse_mode="HTML", reply_markup=nav_btns.start)


async def main_menu(c: CallbackQuery, state: FSMContext):
    await state.reset_state()
    text = 'Главное меню'
    rand = random.randint(1, 5)
    if rand == 5:
        text = text + '\nЕсли понравился бот и есть желание поддержать проект - /donut'
    await c.message.edit_text(text, reply_markup=nav_btns.main_menu)


async def donut_info(message: Message):
    await message.answer('Привет!\nЭтот бот работает на некоммерческой основе и требует средства на свое '
                         'обслуживание(хостинг)\n'
                         'Если он действительно полезный - поддержи его работу.', reply_markup=nav_btns.donut)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=['start'], state='*')
    dp.register_message_handler(donut_info, commands='donut', state='*')

# TODO: переписать названия функций на нормальный язык
