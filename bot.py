import asyncio
import logging

import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram_dialog import DialogRegistry
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter, VIPFilter
from tgbot.handlers.admins.admin import register_admin
from tgbot.handlers.admins.broadcaster import register_broadcast
from tgbot.handlers.filter import register_level_filter
from tgbot.handlers.groups.group_helper import register_groups
from tgbot.handlers.users.compliments import register_compliments
from tgbot.handlers.users.compliments_broadcaster import schedule_jobs
# from tgbot.keyboards.test_keyboards import register_dialog
from tgbot.handlers.users.dialogs.main_dialog import dialog_main, register_user
from tgbot.handlers.users.dialogs.registration import dialog_reg, dialogs
from tgbot.handlers.users.dialogs.timetable import dialog_timetable, fast_timetable
from tgbot.handlers.users.timetable import register_timetable
from tgbot.handlers.users.user_settings import register_user_settings
from tgbot.handlers.users.users_register import register_user_reg
from tgbot.handlers.vips.vip import register_vip
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
        storage = RedisStorage2(host='87.249.53.148')
    else:
        storage = MemoryStorage()
    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
    )

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config

    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(VIPFilter)
    scheduler = AsyncIOScheduler()
    registry = DialogRegistry(dp)

    register_level_filter(dp)
    register_admin(dp)
    register_vip(dp)
    register_user(dp)
    register_timetable(dp)
    register_broadcast(dp)
    register_user_reg(dp)
    register_user_settings(dp)
    register_groups(dp)
    register_compliments(dp)
    # register_dialog(dp)
    schedule_jobs(dp, scheduler)
    dialogs(dp)
    registry.register(dialog_main)
    registry.register(dialog_reg)
    registry.register(dialog_timetable)
    registry.register(fast_timetable)

    # start
    try:
        scheduler.start()
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
