from aiogram.types import BotCommand
from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat

from utils.db_api.db import DBAdmin


async def set_default_commands(dp):
    commands = [
        BotCommand("start", "Запустить бота"),
        BotCommand("help", "Вывести справку"),
        BotCommand("support", "Написать создателю"),
        BotCommand("discord", "Discord сервер"),
        BotCommand("dice", "Бросить кубик")
    ]

    admin_commands = commands.copy()
    data = str(await DBAdmin.vips()).strip('[]')
    try:
        await dp.bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
        await dp.bot.set_my_commands(
            commands=admin_commands,
            scope=BotCommandScopeChat(
                chat_id=data))
    except:
        Exception
