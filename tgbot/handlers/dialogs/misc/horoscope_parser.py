import asyncio

import aiohttp
import asyncpg
from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import load_config
from tgbot.keyboards import nav_btns

signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn',
         'aquarius', 'pisces']
formatted_signs = {}


async def main(m: Message):
    try:
        async with aiohttp.ClientSession() as session:
            config1 = load_config("bot.ini")
            conn = await asyncpg.connect(user=config1.db.user,
                                         password=config1.db.password,
                                         database=config1.db.database,
                                         host=config1.db.host)
            for sign in signs:
                async with session.get(f'https://horoscopes.rambler.ru/api/front/v1/horoscope/today/{sign}') as resp:
                    text = await resp.json()
                    text = text['text']
                    formatted_signs[f'{sign}'] = text
                    await conn.execute('UPDATE main_horoscope SET sign_text = $2 WHERE sign_name = $1', sign, text)
                    # await db.add_horoscope(sign, text)
                    await asyncio.sleep(0.1)
                    print('Успешно')
        await m.bot.send_message(chat_id='-1001277650014', text='✅ Парсинг завершен')
    except:
        await m.bot.send_message(chat_id='-1001277650014', text='❌ Парсинг не завершен. Ошибка!')


async def broadcast_horoscopes(dp: Dispatcher):
    count = 0
    try:
        config1 = load_config("bot.ini")
        conn = await asyncpg.connect(user=config1.db.user,
                                     password=config1.db.password,
                                     database=config1.db.database,
                                     host=config1.db.host)
        result = await conn.fetch('SELECT user_id, args FROM main_subscription WHERE status = True')
        for user, args in result:
            for text in await conn.fetchrow('SELECT sign_text FROM main_horoscope WHERE sign_name = $1', args):
                await dp.bot.send_message(chat_id=user, text=f'<i>{text}</i>',
                                          reply_markup=nav_btns.start)
                count = count + 1
                await asyncio.sleep(0.2)
        await dp.bot.send_message(chat_id=-1001277650014, text=f'✅ Рассылка завершена.{count}')
    except Exception:
        await dp.bot.send_message(chat_id=-1001277650014, text=f'❌ Ошибка в рассылке гороскопов\n{Exception}')


def schedule_jobs(dp: Dispatcher, scheduler):
    scheduler.add_job(main, trigger='cron', hour=3, args=(dp,))
    scheduler.add_job(broadcast_horoscopes, trigger='cron', hour=7, args=(dp,))
    # scheduler.add_job(broadcast_horoscopes, 'interval', seconds=15, args=(dp,))
