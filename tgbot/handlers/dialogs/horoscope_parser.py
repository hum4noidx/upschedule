import aiohttp

from aiogram.dispatcher.handler import ctx_data

signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn',
         'aquarius', 'pisces']

formatted_signs = {}


async def main():
    async with aiohttp.ClientSession() as session:
        db = ctx_data.get().get('repo')
        for sign in signs:
            async with session.get(f'https://horoscopes.rambler.ru/api/front/v1/horoscope/today/{sign}') as resp:
                print(resp.status)
                print(sign)
                text = await resp.json()
                text = text['text']
                formatted_signs[f'{sign}'] = text
                await db.add_horoscope(sign, text)
    print(formatted_signs)

#
# if __name__ == '__main__':
#     asyncio.run(main())
# try:
#
# except Exception:
#     print(Exception)
