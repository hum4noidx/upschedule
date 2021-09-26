from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    text = f'Этот бот был создан за 2 недели как индивидуальный проект.\n\nИзначально в нем не было <b>ничего</b> ' \
           f'полезного<i>(' \
           f'это просто чистое поле, в котором валяется самолёт)</i>, но время шло<i>(ага, по ночам делать ' \
           f'нечего)</i> и проект ' \
           f'развивался, появлялись новые функции, расширялась аудитория.\n\nЗдесь было потрачено много нервов и часов ' \
           f'сна и мне кажется, что получилось круто.' \
           f'\n\n ' \
           f'Если ты пришел сюда за помощью, мне жаль, бот не использует команды, все делается волшебными кнопками.\n' \
           f'А, нет, есть /dice'

    await message.answer(text)


@dp.message_handler(commands="discord", state="*")
async def discord(message: types.message):
    await message.answer('https://discord.gg/4ySJkst')


@dp.message_handler(commands="support", state="*")
async def bot_support(call: types.CallbackQuery):
    await call.answer("Связь с администратором - t.me/hum4noidx")
