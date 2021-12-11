import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from tgbot.handlers.admins.broadcaster import broadcast_get_message
from tgbot.services.repository import Repo
from tgbot.states.states import RemindGroup

broadcast_group = CallbackData('group_id', 'group_id')


async def on_user_join(message: types.Message):
    await message.delete()


async def on_user_left(message: types.Message):
    await message.delete()


# Регистрируем группу в базе данных
async def reg_group(m: Message, repo: Repo):
    chat_id = m.chat.id
    group_name = m.chat.title
    try:
        await repo.add_group(chat_id, group_name)
        await m.reply(f'Успешно ✅\nID группы - <code>{chat_id}</code>', parse_mode='HTML')
    except:
        await m.reply('❌ Ошибка')


async def add_buttons():
    data = ctx_data.get()
    repo = data.get("repo")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for group in await repo.get_groups():
        btn_text = group[0]
        btn_chat_id = group[1]
        keyboard.add(types.InlineKeyboardButton(text=btn_text, callback_data=broadcast_group.new(btn_chat_id)))

    return keyboard


async def broadcast_choose_groups(c: CallbackQuery):
    await c.message.edit_text('Разослать в группы класса:', reply_markup=await add_buttons())


async def broadcast_group_continue(c: CallbackQuery, state: FSMContext):
    await broadcast_get_message(c, state)


# Напоминалка

async def remind_group(m: Message, state: FSMContext):
    async with state.proxy() as data:
        data['remind_text'] = text = m.get_args()
        data['user_id'] = m.from_user.id
    await RemindGroup.SetTime.set()
    await m.answer(f'{text}\nКогда тебе напомнить?')


async def remind_set_time(m: Message, state: FSMContext):
    async with state.proxy() as data:
        text = data['remind_text']
        user_id = data['user_id']
    time_raw = m.text
    l = len(time_raw)
    time_value = time_raw[:l - 1]
    time_scale = time_raw[-1]
    print(time_raw[-1])
    time = 0
    if time_scale == 'h':
        time = int(time_value) * 3600
        print(time)
    elif time_scale == 'm':
        time = int(time_value) * 60
        print(time)
    elif time_scale == 'd':
        time = int(time_value) * 86400
        print(time)
    else:
        await m.answer('Ошибка')
    await state.reset_state()
    await m.answer(f'Напомню тебе через {time // 60} минут.')
    await asyncio.sleep(time * 60)
    await m.answer(f'<a href="tg://user?id={user_id}">Напоминаю</a>\n{text}', parse_mode='HTML')


def register_groups(dp: Dispatcher):
    dp.register_message_handler(on_user_left, content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
    dp.register_message_handler(on_user_join, content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
    dp.register_message_handler(reg_group, commands=['reg'])
    dp.register_message_handler(remind_group, commands=['remind'])
    dp.register_message_handler(remind_set_time, state=RemindGroup.SetTime)
    dp.register_callback_query_handler(broadcast_choose_groups, text="group_broadcast", state="*")
