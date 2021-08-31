from asyncio import sleep
import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.admin_panel.admin_panel import reset_state
from loader import dp
from states.states import RemindGroup
from utils.db_api.db import DBGroup


# Удаляем все сообщения о вступлении и выходе из группы
@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def on_user_join(message: types.Message):
    await message.delete()


@dp.message_handler(content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def on_user_join(message: types.Message):
    await message.delete()


# Регистрируем группу в базе данных
@dp.message_handler(commands=['reg'])
async def reg_group(message: types.Message):
    chat_id = message.chat.id
    group_name = message.chat.title
    if not await DBGroup.db_group_exists(chat_id):
        await DBGroup.db_add_group(chat_id, group_name)
        await message.reply(f'Группа успешна добавлена. ID группы - <code>{chat_id}</code>')
    else:
        await DBGroup.db_group_update(chat_id, group_name)
        await message.reply(f'Группа уже зарегистрирована, информация обновлена.\nID группы - <code>{chat_id}</code>')


# Напоминалка
@dp.message_handler(commands=['remind'])
async def remind_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['remind_text'] = text = message.get_args()
        data['user_id'] = message.from_user.id
    await RemindGroup.SetTime.set()
    await message.answer(f'{text}\nКогда тебе напомнить? (в минутах)')


@dp.message_handler(state=RemindGroup.SetTime)
async def remind_set_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        text = data['remind_text']
        user_id = data['user_id']
    time = int(message.text)
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.answer(f'Напомню тебе через {time} минут.')
    await sleep(time * 60)
    await message.answer(f'<a href="tg://user?id={user_id}">Напоминаю</a>\n{text}')


@dp.message_handler(commands=['note'])
async def create_note(message: types.Message):
    note_text = message.get_args()
    print(note_text)
    print(type(note_text))
    note_owner = int(message.from_user.id)
    note_id = int(random.randrange(1, 6734872, 3))
    chat_id = int(message.chat.id)
    await DBGroup.create_note(note_id, note_text, note_owner, chat_id)
    await message.answer(f'Заметка создана.\n'
                         f'Текст: {note_text}\n'
                         f'Уникальный ID - <code>{note_id}</code>')


@dp.message_handler(commands=['notes'])
async def show_notes(message: types.Message):
    chat_id = int(message.chat.id)
    await message.answer(await DBGroup.show_notes(chat_id))


@dp.poll_answer_handler()
async def some_poll_answer_handler(poll_answer: types.PollAnswer):
    print(poll_answer.user)
