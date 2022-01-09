from typing import List


class Repo:

    def __init__(self, conn):
        self.conn = conn

    # ______________________ USERS ______________________
    async def add_user(self, user_id, full_name):
        """Store user in DB, ignore duplicates"""
        await self.conn.execute(
            'INSERT INTO users_new(user_id, full_name) SELECT $1, $2 WHERE NOT(SELECT TRUE FROM users_new WHERE '
            'user_id=$1)', user_id, full_name)

    async def schedule_user_usage(self, user_id):
        await self.conn.execute(
            'UPDATE users_new SET (uses, last_seen) = (uses + 1, localtimestamp(0)::timestamp) '
            'WHERE user_id = $1', user_id)

    async def show_user_info(self, user_id):
        user_data = dict(await self.conn.fetchrow('Select full_name, uses, user_class, user_math, user_prof, vip '
                                                  'from users_new Where user_id = $1', user_id))
        msg = (f"Имя - {user_data['full_name']}\n"
               f"Жмякал на кнопки - {user_data['uses']} раз\n"
               f"Класс - {user_data['user_class']}\n"
               f"Профиль - {user_data['user_prof']}\n"
               f"Математика - {user_data['user_math']}\n"
               f"VIP - {user_data['vip']}")
        message = msg.replace('prof', 'Профиль').replace('base', 'База').replace('fm', 'Физмат').replace(
            'bh', 'Биохим').replace('se', 'Соцэконом').replace('gum', 'Гуманитарий')
        return message

    async def user_change_name(self, user_id, name):
        await self.conn.execute('Update users_new Set full_name = $1 Where user_id = $2', name, user_id)

    # ______________________ REGISTRATION ______________________
    async def register_user(self, user_class, user_prof, user_math, userid):
        await self.conn.execute(
            'UPDATE users_new SET (user_class, user_prof, user_math) = ($1, $2, $3) WHERE user_id =$4',
            user_class, user_prof, user_math, userid
        )

    # user_data for recent_schedule
    async def get_timetable(self, userid):
        user_profile = await self.conn.fetchrow(
            'SELECT user_class, user_prof, user_math FROM users_new WHERE user_id = $1', userid
        )
        return dict(user_profile)

    # ______________________ ROLES ______________________
    async def get_admins(self) -> List[int]:
        admins = await self.conn.fetch(
            'SELECT user_id FROM users_new WHERE admin = True'
        )
        data = ([admin['user_id'] for admin in admins])
        return data

    async def get_vips(self) -> List[int]:
        vips = await self.conn.fetch(
            'SELECT user_id FROM users_new WHERE vip = True'
        )
        data = ([vip['user_id'] for vip in vips])
        return data

    # ______________________ GROUPS ______________________
    async def add_group(self, group_id, group_name):
        await self.conn.execute(
            'INSERT INTO groups (chat_id, group_name) VALUES ($1, $2)'
            'ON CONFLICT (chat_id) DO UPDATE SET group_name = $2',
            group_id, group_name)
        return

    async def get_groups(self):
        groups = dict(await self.conn.fetch('SELECT group_name, chat_id FROM groups'))
        groups = list(groups.items())
        return groups

    # ______________________ ADMIN PANEL ______________________
    async def list_all_users(self):
        all_info = await self.conn.fetch(
            'Select id, full_name, uses, vip From users_new Order by id'
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
            'SELECT id, full_name, uses, last_seen From users_new WHERE last_seen::date=current_date '
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
            'SELECT * FROM users_new WHERE id = $1', uid
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
            'UPDATE users_new SET vip = true WHERE id = $1', user_id
        )
        # status = await self.conn.fetchrow('SELECT vip FROM users_new Where id = $1', user_id)
        # return status['vip']

    async def get_user_name(self, user_id):
        name = await self.conn.fetchrow(
            'SELECT full_name FROM users_new WHERE  user_id=$1', user_id
        )
        return name['full_name']

    async def admin_switch(self, user_id):
        await self.conn.executemany('IF users_new.admin = True THEN UPDATE users_new SET admin = False', user_id)
        # broadcast

    async def get_user_ids(self):  # getting ALL id's to broadcast
        ids = await self.conn.fetch(
            'SELECT user_id from users_new'
        )
        data = ([uid['user_id'] for uid in ids])
        return data

    async def broadcast_get_first_ids(self, user_class, user_profile, user_math1):
        user_math = str(user_math1)
        ids = await self.conn.fetch(
            'Select user_id From users_new Where user_class = $1 And user_prof = $2 And user_math = $3',
            user_class, user_profile, user_math
        )
        data = ([uid['user_id'] for uid in ids])
        return data

    async def broadcast_get_class_ids(self, user_class):
        ids = await self.conn.fetch(
            'Select user_id From users_new Where user_class = $1', user_class
        )
        data = ([uid['user_id'] for uid in ids])
        return data

    async def broadcast_get_profile_ids(self, user_profile):
        ids = await self.conn.fetch(
            'Select user_id From users_new Where user_prof = $1', user_profile
        )
        data = ([uid['user_id'] for uid in ids])
        return data

    #  ======================== COMPLIMENTS ========================

    # async def db_get_compliments(self):
    #     result = await self.conn.fetch('SELECT compliment, com_owner, theme FROM compliments')
    #     compliments = ([compliment['compliment'] for compliment in result])
    #     return compliments
    async def add_compliment(self, compliment, full_name):
        await self.conn.execute('INSERT INTO compliments (compliment, com_owner) Values($1,$2)', compliment, full_name)

    async def add_compliment_subscription(self, user_id, full_name):
        await self.conn.execute(
            'INSERT INTO user_compliments (user_id, full_name) Values ($1, $2) ON CONFLICT (user_id) DO NOTHING ',
            user_id, full_name)
#  ======================== SCHEDULE DATABASE ATTEMPTS ========================
