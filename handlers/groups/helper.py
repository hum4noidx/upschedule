from asyncio import sleep

from aiogram import types

from loader import dp, bot


@dp.message_handler(commands='dice', state='*')
async def send_dice(message: types.Message):
    await bot.send_dice(chat_id=message.chat.id)


@dp.message_handler(commands='gul', state='*', is_vip=True)
async def spam(message: types.Message):
    x = 1000
    await sleep(1)
    while x > 7:
        await message.answer(f"{x} - 7 = {x - 7}")
        x -= 7
        await sleep(0.1)
