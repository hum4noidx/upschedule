import hashlib
from asyncio import sleep
from aiogram import types
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from loader import bot
from keyboards.inline import nav_btns
from loader import dp
from utils.db_api.db import DBAdmin
from utils.set_bot_commands import set_default_commands


# Получение информации о пользователе по user_id
@dp.callback_query_handler(is_vip=True, text="admin_info", state="*")
async def user(call: types.CallbackQuery):
    await call.answer("Временно не работает, а может и не временно...", show_alert=True)


@dp.message_handler(commands=['i'], is_vip=True, state="*")
async def get_user_info(message: types.message):
    info = message.get_args()
    await message.answer(await DBAdmin.db_get_info(info), reply_markup=nav_btns.cancel_today)


# @dp.inline_handler()
# async def inline_echo(inline_query: InlineQuery):
#     text = inline_query.query
#     if not text:
#         await sleep(2)
#     else:
#         info1 = str(await DBAdmin.db_get_info(text))
#         input_content = InputTextMessageContent(info1)
#         result_id: str = hashlib.md5(text.encode()).hexdigest()
#         item = InlineQueryResultArticle(
#             id=result_id,
#             title=f'Result {text!r}',
#             input_message_content=input_content,
#         )
#         # don't forget to set cache_time=1 for testing (default is 300s or 5m)
#         await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)

# TODO: попробовать сделать динамические кнопки
# Получение информации о всех пользователях
@dp.callback_query_handler(is_vip=True, text="admin_all_users", state="*")
async def all_info(call: types.CallbackQuery):
    await call.message.edit_text(await DBAdmin.db_get_all_info(), reply_markup=nav_btns.cancel_today)


# Сброс состояния, если застрял
@dp.message_handler(commands="reset", state="*")
async def reset_state(message: types.message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()


@dp.message_handler(is_vip=True, commands="vip", state="*")
async def add_vip(message: types.message):
    info = message.get_args()
    await set_default_commands(dp)
    await message.answer("Пользователь успешно добавлен", await DBAdmin.db_add_vip(info))


@dp.message_handler(is_vip=False, commands="vip", state="*")
async def add_vip(message: types.message):
    await message.answer("Не твой уровень, дорогой")

# TODO: Сделать отдельную панель для учителей с проверкой из бд
