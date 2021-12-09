import asyncio
import logging

import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram_dialog import DialogRegistry

from tgbot.config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter, VIPFilter
from tgbot.handlers.admins.admin import register_admin
from tgbot.handlers.admins.broadcaster import register_broadcast
from tgbot.handlers.filter import register_level_filter
from tgbot.handlers.groups.group_helper import register_groups
from tgbot.handlers.user_settings import register_user_settings
from tgbot.handlers.users.timetable import register_timetable
from tgbot.handlers.users.user_main import register_user
from tgbot.handlers.users.users_register import register_user_reg
from tgbot.handlers.vips.vip import register_vip
# from tgbot.keyboards.test_keyboards import register_dialog
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware

logger = logging.getLogger(__name__)


async def create_pool(user, password, database, host):
    pool = await asyncpg.create_pool(user=user, password=password, database=database, host=host,
                                     command_timeout=60)
    return pool


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config("bot.ini")

    if config.tg_bot.use_redis:
        storage = RedisStorage()
    else:
        storage = MemoryStorage()
    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
    )

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(VIPFilter)

    register_level_filter(dp)
    register_admin(dp)
    register_vip(dp)
    register_user(dp)
    register_timetable(dp)
    register_broadcast(dp)
    register_user_reg(dp)
    register_user_settings(dp)
    register_groups(dp)
    # register_dialog(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
