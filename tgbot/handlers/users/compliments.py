from aiogram import Dispatcher
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards import nav_btns


async def compliments_info(c: CallbackQuery):
    await c.message.edit_text(
        'Жми \"Включить\", чтобы получать ежедневные комплименты для поднятия настроения :)\nПока они будут приходить два раза в день: утром и днем. Позже что-то придумаю\nАвтор идеи - @ptrnaaa',
        reply_markup=nav_btns.compliments)


async def compliments_subscribe(c: CallbackQuery):
    data = ctx_data.get()
    repo = data.get("repo")
    await c.message.edit_text('Ты подписан на рассылку комплиментов.\nНе грусти!', reply_markup=nav_btns.back_to_mm)
    await repo.add_compliment_subscription(c.from_user.id, c.from_user.full_name)


async def add_compliment(c: CallbackQuery):
    await c.message.edit_text('Если у тебя есть парочка комплиментов или фраз, можешь смело их добавлять',
                              reply_markup=nav_btns.back_to_mm)


async def compliment_handler(m: Message):
    compl = m.text
    data = ctx_data.get()
    repo = data.get("repo")
    await repo.add_compliment(compl, m.from_user.full_name)
    await m.answer('Успешно', reply_markup=nav_btns.back_to_mm)


def register_compliments(dp: Dispatcher):
    dp.register_callback_query_handler(compliments_info, text="compliments_subscription", state='*')
    dp.register_callback_query_handler(compliments_subscribe, text='turn_compliments', state='*')
    dp.register_callback_query_handler(add_compliment, text='add_compliment', state='*')
    dp.register_message_handler(compliment_handler, state='*')
