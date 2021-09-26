from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config
from filters.vip_users import IsVIP, IsAdmin1

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.filters_factory.bind(IsVIP)
dp.filters_factory.bind(IsAdmin1)
