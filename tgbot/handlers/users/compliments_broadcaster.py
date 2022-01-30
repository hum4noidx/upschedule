import random

import asyncpg
from aiogram import Dispatcher

from tgbot.config import load_config


# ids = [862986140, 713870562]


async def get_compliments():
    # временно костыль
    config1 = load_config("bot.ini")
    conn = await asyncpg.connect(user=config1.db.user,
                                 password=config1.db.password,
                                 database=config1.db.database,
                                 host=config1.db.host)
    result = await conn.fetch('SELECT compliment, com_owner, theme FROM compliments')
    compliments_raw = ([compliment['compliment'] for compliment in result])
    return compliments_raw


async def get_ids():
    # временно костыль
    config1 = load_config("bot.ini")
    conn = await asyncpg.connect(user=config1.db.user,
                                 password=config1.db.password,
                                 database=config1.db.database,
                                 host=config1.db.host)
    result = await conn.fetch('SELECT user_id FROM user_compliments')
    ids = ([uid['user_id'] for uid in result])
    return ids


async def compliments(dp: Dispatcher):
    compliments = await get_compliments()
    ids = await get_ids()
    for uid in ids:
        compliment = random.choice(compliments)
        await dp.bot.send_message(chat_id=uid, text=compliment)


def schedule_jobs(dp: Dispatcher, scheduler):
    pass
    # scheduler.add_job(compliments, 'cron', day_of_week='mon-fri', hour=8, args=(dp,))
    # scheduler.add_job(compliments, 'cron', day_of_week='mon-fri', hour=12, args=(dp,))

    # scheduler.add_job(compliments, 'interval', seconds=5, args=(dp,))
