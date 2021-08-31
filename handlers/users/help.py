from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/support - Написать создателю",
            "/discord - Discord сервер")

    await message.answer("\n".join(text))


@dp.message_handler(commands="discord", state="*")
async def discord(message: types.message):
    await message.answer('https://discord.gg/4ySJkst')
