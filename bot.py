import logging

import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import start_webhook
from aiogram_dialog import DialogRegistry
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter, VIPFilter
from tgbot.handlers.admins.admin import register_admin
from tgbot.handlers.admins.broadcaster import register_broadcast
from tgbot.handlers.dialogs.admin.admin_panel import dialog_admin
from tgbot.handlers.dialogs.admin.broadcaster import dialog_broadcaster
from tgbot.handlers.dialogs.misc.horoscope_parser import schedule_jobs
from tgbot.handlers.dialogs.misc.timetable import dialog_timetable, dialog_fast_timetable
from tgbot.handlers.dialogs.user.horoscope_dialog import horoscopes
from tgbot.handlers.dialogs.user.main_dialog import register_user, dialog_main
from tgbot.handlers.dialogs.user.registration import dialog_reg, dialogs
from tgbot.handlers.dialogs.user.user_settings import dialog_user_settings, dialog_subscriptions, \
    dialog_horoscope_subscribe
from tgbot.handlers.groups.group_helper import register_groups
from tgbot.handlers.users.compliments import register_compliments
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


config = load_config("bot.ini")
if config.tg_bot.use_redis:
    storage = RedisStorage2(host='92.53.105.144', password=config.db.redis_pass)
else:
    storage = MemoryStorage()

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)
bot['config'] = config
webhook_url = f"{config.tg_bot.webhook_host}/hook"


async def on_startup(dp):
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    await bot.set_webhook(webhook_url)
    logging.error('Starting Webhook')
    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
    )
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(VIPFilter)
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    registry = DialogRegistry(dp)

    register_admin(dp)
    register_vip(dp)
    register_user(dp)
    register_timetable(dp)
    register_broadcast(dp)
    register_user_reg(dp)
    register_user_settings(dp)
    register_groups(dp)
    register_compliments(dp)
    schedule_jobs(dp, scheduler)
    dialogs(dp)

    registry.register(dialog_main)
    registry.register(dialog_user_settings)
    registry.register(dialog_broadcaster)
    registry.register(dialog_reg)
    registry.register(dialog_timetable)
    registry.register(dialog_fast_timetable)
    registry.register(dialog_admin)
    registry.register(horoscopes)
    registry.register(dialog_subscriptions)
    registry.register(dialog_horoscope_subscribe)

    scheduler.start()


async def on_shutdown(dp):
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.session.close()
    logging.error('Bot stopped. Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=config.tg_bot.webhook_path,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='localhost',
        port=7000,
    )
