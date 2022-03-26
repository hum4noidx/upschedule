from typing import List

from prettytable import PrettyTable


class Repo:

    def __init__(self, conn):
        self.conn = conn

    # ______________________ USERS ______________________
    async def add_user(self, user_id, full_name):
        """Store user in DB, ignore duplicates"""
        await self.conn.execute(
            'INSERT INTO main_passport(user_id, full_name) VALUES($1,$2) '
            'ON CONFLICT(user_id) DO UPDATE SET uses=main_passport.uses+1 WHERE main_passport.user_id=$1',
            user_id, full_name)
        return

    async def schedule_user_usage(self, user_id):
        await self.conn.execute(
            'UPDATE main_passport SET (uses, last_seen) = (uses + 1, now()) '
            'WHERE user_id = $1', user_id)

    async def show_user_info(self, user_id):
        user_data = dict(await self.conn.fetchrow(
            'SELECT main_passport.id,main_passport.full_name, main_passport.uses, main_grade.grade_short, '
            'main_profile.profile_db, main_passport.vip '
            'FROM main_passport '
            'LEFT JOIN main_grade ON main_passport.user_class_id = main_grade.id '
            'LEFT JOIN main_profile ON main_passport.user_prof_id = main_profile.id '
            # 'LEFT JOIN horoscopes ON main_passport.horoscope_sign = horoscopes.sign '
            'WHERE main_passport.user_id = $1', user_id))
        msg = (f"ID - {user_data['id']}\n"
               f"Имя - {user_data['full_name']}\n"
               f"Жмякал на кнопки - {user_data['uses']} раз\n"
               f"Класс - {user_data['grade_short']}\n"
               f"Профиль - {user_data['profile_db']}\n"
               f"VIP - {user_data['vip']}\n")
        # f"Знак - {user_data['sign_ru']}")
        return msg

    async def user_change_name(self, user_id, name):
        await self.conn.execute('Update main_passport Set full_name = $1 Where user_id = $2', name, user_id)

    # ______________________ REGISTRATION ______________________
    async def register_user(self, user_school, user_class, user_prof, userid):
        result = await self.conn.execute(
            'UPDATE main_passport SET (school_id, user_class_id, user_prof_id, registered) = ($1, $2, '
            '$3, $4) '
            'WHERE user_id =$5',
            user_school, user_class, user_prof, True, userid
        )
        return result[-1]

    # user_data for recent_schedule
    async def get_timetable(self, userid):
        user_profile = await self.conn.fetchrow(
            'SELECT user_class_id, user_prof_id, user_math_id FROM main_passport WHERE user_id = $1', userid
        )
        return dict(user_profile)

    # ______________________ ROLES ______________________
    async def get_admins(self, user_id):
        data = await self.conn.fetchrow(
            'SELECT admin FROM main_passport WHERE user_id = $1', user_id
        )
        return data['admin']

    async def get_vips(self) -> List[int]:
        vips = await self.conn.fetch(
            'SELECT user_id FROM main_passport WHERE vip = True'
        )
        data = ([vip['user_id'] for vip in vips])
        return data

    # ______________________ GROUPS ______________________
    async def add_group(self, group_id, group_name):
        await self.conn.execute(
            'INSERT INTO main_group (chat_id, group_name) VALUES ($1, $2)'
            'ON CONFLICT (chat_id) DO UPDATE SET group_name = $2',
            group_id, group_name)
        return

    #
    # async def get_groups(self):
    #     groups = dict(await self.conn.fetch('SELECT group_name, chat_id FROM groups'))
    #     groups = list(groups.items())
    #     return groups

    # ______________________ ADMIN PANEL ______________________
    async def list_all_users(self):
        all_info = await self.conn.fetch(
            'SELECT id, full_name, uses, vip From main_passport Order by id'
        )
        top_text = ['ID  Имя  Использований VIP']
        for info in all_info:
            data = [f"{info[0]}|{info[1]}|{info[2]}|{info[3]}"]
            textpath = '\n'.join(data)
            top_text.append(textpath)
        text = '\n'.join(top_text)
        text = text.replace('False', '')
        text = text.replace('True', 'VIP')
        return text

    async def list_all_today_users(self):
        today_users = await self.conn.fetch(
            'SELECT id, full_name, uses, last_seen From main_passport WHERE last_seen::date=current_date '
            'Order by last_seen'
        )
        top_text = ['ID Name Uses Last seen']
        for user in today_users:
            data = [f"{user[0]}|{user[1]}|{user[2]}|{user[3]}"]
            textpath = '\n'.join(data)
            top_text.append(textpath)
        text = '\n'.join(top_text)
        return text

    async def user_info(self, info):
        uid = int(info)
        user_info = dict(await self.conn.fetchrow(
            'SELECT * FROM main_passport WHERE id = $1', uid
        ))
        text = (f'ID - <code>{user_info["id"]}</code>\n'
                f'User_ID - <code>{user_info["user_id"]}</code>\n'
                f'Имя - <code>{user_info["full_name"]}</code>\n'
                f'Количество использований - <code>{user_info["uses"]}</code>\n'
                f'Класс пользователя - <code>{user_info["user_class"]}</code>\n'
                f'Профиль пользователя - <code>{user_info["user_prof"]}</code>\n'
                f'Математика - <code>{user_info["user_math"]}</code>\n'
                f'VIP - <code>{user_info["vip"]}</code>\n'
                f'Admin - <code>{user_info["admin"]}</code>\n'
                f'Last seen - <code>{user_info["last_seen"]}</code>')
        return text

    async def add_vip_user(self, user_id):
        await self.conn.execute(
            'UPDATE main_passport SET vip = true WHERE id = $1', user_id
        )
        status = await self.conn.fetchrow('SELECT vip FROM main_passport Where id = $1', user_id)
        return status['vip']

    async def get_user_name(self, user_id):
        name = await self.conn.fetchrow(
            'SELECT full_name FROM main_passport WHERE  user_id=$1', user_id
        )
        return name['full_name']

    async def admin_switch(self, user_id):
        await self.conn.executemany('IF main_passport.admin = True THEN UPDATE main_passport SET admin = False',
                                    user_id)
        # broadcast

    async def get_user_ids(self):  # getting ALL id's to broadcast
        ids = await self.conn.fetch(
            'SELECT user_id from main_passport'
        )
        data = ([uid['user_id'] for uid in ids])
        return data

    async def broadcast_get_first_ids(self, user_class, user_profile, user_math1):
        user_math = str(user_math1)
        ids = await self.conn.fetch(
            'SELECT user_id From main_passport Where user_class_id = $1 And user_prof_id = $2 And user_math_id = $3',
            user_class, user_profile, user_math
        )
        data = ([uid['user_id'] for uid in ids])
        return data

    async def broadcast_get_class_ids(self, user_class):
        ids = await self.conn.fetch(
            'SELECT user_id From main_passport Where user_class_id = $1', user_class
        )
        data = ([uid['user_id'] for uid in ids])
        return data

    async def broadcast_get_profile_ids(self, user_profile):
        ids = await self.conn.fetch(
            'SELECT user_id From main_passport Where user_prof_id = $1', user_profile
        )
        data = ([uid['user_id'] for uid in ids])
        return data

    # TODO : check this, start doing broadcast dialog
    #  ______________________ COMPLIMENTS ______________________

    # async def db_get_compliments(self):
    # result = await self.conn.fetch('SELECT compliment, com_owner, theme FROM compliments')
    # compliments = ([compliment['compliment']
    # for compliment in result]) return compliments
    # async def add_compliment(self, compliment, full_name):
    # await self.conn.execute('INSERT INTO compliments (compliment,com_owner) Values($1,$2)', compliment, full_name)
    #
    # async def add_compliment_subscription(self, user_id, full_name):
    #     await self.conn.execute(
    #         'INSERT INTO user_compliments (user_id, full_name) Values ($1, $2) ON CONFLICT (user_id) DO NOTHING ',
    #         user_id, full_name)

    #  ______________________ SCHEDULE DATABASE ______________________
    async def get_schedule(self, grade, profile, date):
        #  ======================== META ========================
        raw_meta = await self.conn.fetch(
            'SELECT main_grade.grade_short, main_profile.profile_db, main_date.date_short '
            'FROM  main_grade,main_profile,main_date '
            'WHERE main_grade.id = $1 AND main_profile.id = $2 AND main_date.id = $3',
            grade, profile, date
        )
        meta = str()
        for meta1 in raw_meta:
            meta = f"{meta1['grade_short']}|{meta1['profile_db']}|{meta1['date_short']}"
        #  ======================== DATA ========================
        if int(date) == 6 or int(date) == 7:
            schedule = meta + '\nТут пусто'
        else:
            raw_schedule = await self.conn.fetch(
                'SELECT main_schedule.lsn_number, main_discipline.lsn_name, main_classroom.number '
                'FROM main_schedule LEFT JOIN main_discipline ON main_schedule.lsn_text_id = main_discipline.id '
                'LEFT JOIN main_classroom ON main_schedule.lsn_class_id = main_classroom.id '
                'WHERE (main_schedule.lsn_grade_id=$1 AND main_schedule.lsn_profile_id = $2 '
                'AND main_schedule.lsn_date_id = $3) '
                'ORDER BY main_schedule.lsn_number', grade, profile, date)
            # Создаем таблицу
            schedule = PrettyTable()
            schedule.title = meta
            schedule.field_names = ["№", "Урок", "Каб."]
            schedule.align = "l"
            for lesson in raw_schedule:  # Заполняем таблицу данными
                schedule.add_row([lesson["lsn_number"], lesson["lsn_name"], lesson["number"]])
        return str(schedule)

    async def get_schools(self):
        data = dict(await self.conn.fetch('SELECT name, id '
                                          'FROM main_school ORDER BY name'))
        data = list(data.items())
        return data

    async def get_grades(self, user_id):
        data = dict(
            await self.conn.fetch('SELECT grade, grade_short '
                                  'FROM main_grade '
                                  'WHERE school_id = (SELECT school_id FROM main_passport WHERE user_id=$1)', user_id))
        data = list(data.items())
        return data

    async def reg_get_grades(self, school_id):
        data = dict(
            await self.conn.fetch('SELECT grade, grade_short '
                                  'FROM main_grade '
                                  'WHERE school_id = $1 ORDER BY grade', int(school_id)))
        data = list(data.items())
        return data

    async def get_profiles(self, grade_id):
        data = dict(await self.conn.fetch('SELECT profile_db, id '
                                          'FROM main_profile '
                                          'WHERE grade_id = $1 ORDER BY id', int(grade_id)))
        data = list(data.items())
        return data

    async def get_maths(self, ):
        data = dict(await self.conn.fetch('SELECT math, id '
                                          'FROM main_math ORDER BY id', ))
        data = list(data.items())
        return data

    async def check_registered(self, user_id):
        result = await self.conn.fetchrow('SELECT registered '
                                          'FROM main_passport '
                                          'WHERE user_id=$1', user_id)
        return result['registered']

    async def db_get_user_school(self, user_id):
        result = await self.conn.fetchrow('SELECT school_id '
                                          'FROM main_passport '
                                          'WHERE user_id=$1', user_id)
        return result['school_id']

    async def get_days(self):
        data = dict(await self.conn.fetch('SELECT day,id '
                                          'FROM main_date ORDER BY id', ))
        data = list(data.items())
        return data

    async def users_count(self):
        data = await self.conn.fetchrow('SELECT count(id) FROM main_passport')
        return data['count']

    async def add_horoscope(self, sign, text):
        await self.conn.execute('UPDATE main_horoscope SET sign_text = $2 WHERE sign_name = $1', sign, text)

    async def list_horoscope_subscribers(self):
        result = await self.conn.fetch("SELECT user_id, args FROM main_subscription "
                                       "WHERE main_subscription.title = 'horoscope'")
        return result

    async def get_horoscope_texts(self, sign):
        result = await self.conn.fetchrow('SELECT sign_text FROM horoscopes WHERE sign = $1', sign)
        return result['sign_text']

    async def db_get_horoscope_signs(self):
        result = dict(await self.conn.fetch('SELECT sign_ru, sign FROM horoscopes ORDER BY id'))
        data = list(result.items())
        return data

    async def update_user_horoscope_sign(self, sign, user_id):
        await self.conn.execute(
            'INSERT INTO main_subscription (args,user_id, title, status, title_ru) '
            'VALUES($1,$2,$3,$4,$5) ON CONFLICT(user_id) DO UPDATE SET args=$1', sign, user_id,
            'horoscope', True, 'Гороскоп')

    async def get_subscriptions(self, user_id):
        try:
            result = dict(
                await self.conn.fetchrow('SELECT title_ru, status FROM main_subscription WHERE user_id = $1', user_id))
        except TypeError:
            result = 'None'
        return result
