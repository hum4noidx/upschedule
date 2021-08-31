from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat
from aiogram.types import BotCommand
from utils.db_api.db import DBAdmin


async def set_default_commands(dp):
    commands = [
        BotCommand("start", "Запустить бота"),
        BotCommand("help", "Вывести справку"),
        BotCommand("support", "Написать создателю"),
        BotCommand("discord", "Discord сервер")
    ]

    admin_commands = commands.copy()
    admin_commands.append(BotCommand(command="broadcast", description="Рассылка сообщений"))
    admin_commands.append(BotCommand(command="all", description="Посмотреть всех пользователей"))
    data = str(await DBAdmin.vips()).strip('[]')
    await dp.bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
    await dp.bot.set_my_commands(
        commands=admin_commands,
        scope=BotCommandScopeChat(
            chat_id=data))
