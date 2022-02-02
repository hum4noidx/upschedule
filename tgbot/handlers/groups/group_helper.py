import asyncio
import re
from datetime import timedelta

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from tgbot.handlers.admins.broadcaster import broadcast_get_message
from tgbot.handlers.groups.localization import get_string
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
    await repo.add_group(chat_id, group_name)
    await m.reply(f'Успешно ✅\nID группы - <code>{chat_id}</code>', parse_mode='HTML')


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


# ======================================GROUP ADMINISTRATION =========================================================
async def kick_user(m: Message):
    readonly_to = await m.chat.get_member(m.reply_to_message.from_user.id)
    if readonly_to.is_chat_admin():
        user_id = m.reply_to_message.from_user.id
        name = m.reply_to_message.from_user.full_name
        name_admin = m.from_user.full_name
        user_id_admin = m.from_user.id
        await m.bot.kick_chat_member(chat_id=m.chat.id, user_id=user_id)
        await m.bot.unban_chat_member(chat_id=m.chat.id, user_id=user_id)
        await m.answer(
            f'<a href="tg://user?id={user_id_admin}">{name_admin}</a> '
            f'кикнул <a href="tg://user?id={user_id}">{name}</a>')


restriction_time_regex = re.compile(r'(\b[1-9][0-9]*)([mhd]\b)')


async def error_no_reply(m: types.Message):
    lang = m.bot.get('config').tg_bot.lang
    await m.reply(get_string(lang, "error_no_reply"))


def get_restriction_period(text: str) -> int:
    """
    Extract restriction period (in seconds) from text using regex search
    :param text: text to parse
    :return: restriction period in seconds (0 if nothing found, which means permanent restriction)
    """
    multipliers = {"m": 60, "h": 3600, "d": 86400}
    if match := re.search(restriction_time_regex, text):
        time, modifier = match.groups()
        return int(time) * multipliers[modifier]
    return 0


async def cmd_ro(m: Message):
    """
    Handle /ro command in main group
    :param message: Telegram message starting with /ro
    """
    lang = m.bot.get('config').tg_bot.lang
    readonly_to = await m.chat.get_member(m.reply_to_message.from_user.id)
    if readonly_to.is_chat_admin():
        await m.reply(get_string(lang, "error_restrict_admin"))
        return
    user = await m.chat.get_member(m.from_user.id)
    if not user.is_chat_admin() or user.can_restrict_members is False:
        return
    ro_period = get_restriction_period(m.text)
    ro_end_date = m.date + timedelta(seconds=ro_period)
    await m.chat.restrict(
        user_id=m.reply_to_message.from_user.id,
        permissions=types.ChatPermissions(),
        until_date=ro_end_date
    )
    if ro_period == 0:
        await m.reply(get_string(lang, "readonly_forever"))
    else:
        await m.reply(
            get_string(lang, "readonly_temporary").format(time=ro_end_date.strftime("%d.%m.%Y %H:%M"))
        )


async def cmd_nomedia(m: types.Message):
    """
    Handle /nomedia command in main group
    :param message: Telegram message starting with /nomedia
    """
    lang = m.bot.get('config').tg_bot.lang
    nomedia_to = await m.chat.get_member(m.reply_to_message.from_user.id)
    if nomedia_to.is_chat_admin():
        await m.reply(get_string(lang, "error_restrict_admin"))
        return
    user = await m.chat.get_member(m.from_user.id)
    if not user.is_chat_admin() or user.can_restrict_members is False:
        return
    nomedia_period = get_restriction_period(m.text)
    nomedia_end_date = m.date + timedelta(seconds=nomedia_period)
    await m.chat.restrict(
        user_id=m.reply_to_message.from_user.id,
        permissions=types.ChatPermissions(can_send_messages=True),
        until_date=nomedia_end_date
    )
    if nomedia_period == 0:
        await m.reply(get_string(lang, "nomedia_forever"))
    else:
        await m.reply(
            get_string(lang, "nomedia_temporary").format(time=nomedia_end_date.strftime("%d.%m.%Y %H:%M"))
        )


async def stickers_switch(m: Message):
    user = await m.chat.get_member(m.from_user.id)
    if user.is_chat_admin():
        permissions_on = {'can_send_other_messages': True,
                          'can_send_messages': True,
                          'can_send_polls': True,
                          'can_pin_messages': True,
                          'can_add_web_page_previews': True}
        permissions_off = {'can_send_other_messages': False,
                           'can_send_messages': True}
        if m.get_args() == '1':
            permissions = permissions_on
            status = '✅'
        else:
            permissions = permissions_off
            status = '❌'

        await m.bot.set_chat_permissions(chat_id=m.chat.id, permissions=permissions)
        await m.answer(f'Использование стикеров: {status}')
    else:
        await m.answer('Нет прав)')


def register_groups(dp: Dispatcher):
    dp.register_message_handler(on_user_left, content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
    dp.register_message_handler(on_user_join, content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
    dp.register_message_handler(reg_group, commands=['reg'])
    dp.register_message_handler(remind_group, commands=['remind'], chat_type=types.ChatType.GROUP)
    dp.register_message_handler(remind_set_time, state=RemindGroup.SetTime)
    dp.register_callback_query_handler(broadcast_choose_groups, text="group_broadcast", state="*")
    dp.register_message_handler(kick_user, commands=['kick'], is_reply=True)
    dp.register_message_handler(error_no_reply, is_reply=False, commands=["ro", "nomedia"])
    dp.register_message_handler(cmd_ro, is_reply=True, commands=['ro'])
    dp.register_message_handler(cmd_nomedia, is_reply=True, commands="nomedia")
    dp.register_message_handler(stickers_switch, commands=['stick'])
