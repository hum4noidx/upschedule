from typing import List


class Repo:

    def __init__(self, conn):
        self.conn = conn

    # ______________________ USERS ______________________
    async def add_user(self, user_id, full_name):
        """Store user in DB, ignore duplicates"""
        await self.conn.execute(
            'INSERT INTO users_new (user_id, full_name) VALUES ($1, $2)'
            'ON CONFLICT (user_id) DO UPDATE SET uses=users_new.uses+1',
            user_id, full_name)
        return

    async def schedule_user_usage(self, user_id):
        await self.conn.execute(
            'UPDATE users_new SET (uses, last_seen) = (uses + 1, localtimestamp(0)::timestamp) WHERE user_id = $1',
            user_id)

    # ______________________ REGISTRATION ______________________
    async def register_user(self, user_class, user_prof, user_math, userid):
        await self.conn.execute(
            'UPDATE users_new SET (user_class, user_prof, user_math) = ($1, $2, $3) WHERE user_id =$4',
            user_class, user_prof, user_math, userid)

    # user_data for recent_schedule
    async def get_schedule(self, userid):
        user_profile = await self.conn.fetchrow(
            'SELECT user_class, user_prof, user_math FROM users_new WHERE user_id = $1', userid)
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

    # ______________________ ADMIN PANEL ______________________
    async def list_all_users(self):
        all_info = await self.conn.fetch('Select id, full_name, uses, vip From users_new Order by id')
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
            'Order by id')
        top_text = ['ID Name Uses Last seen']
        for user in today_users:
            data = [f"{user[0]}|{user[1]}|{user[2]}|{user[3]}"]
            textpath = '\n'.join(data)
            top_text.append(textpath)
        text = '\n'.join(top_text)
        return text

    async def user_info(self, info):
        uid = int(info)
        rer = await self.conn.fetchrow('SELECT * FROM users_new WHERE id = $1', uid)
        in1 = dict(rer)
        text = (f'ID - <code>{in1["id"]}</code>\n'
                f'User_ID - <code>{in1["user_id"]}</code>\n'
                f'Имя - <code>{in1["full_name"]}</code>\n'
                f'Количество использований - <code>{in1["uses"]}</code>\n'
                f'Класс пользователя - <code>{in1["user_class"]}</code>\n'
                f'Профиль пользователя - <code>{in1["user_prof"]}</code>\n'
                f'Математика - <code>{in1["user_math"]}</code>\n'
                f'VIP - <code>{in1["vip"]}</code>\n'
                f'Admin - <code>{in1["admin"]}</code>\n'
                f'Last seen - <code>{in1["last_seen"]}</code>')
        return text

    async def add_vip_user(self, user_id):
        await self.conn.execute('UPDATE users SET vip = true WHERE id = $1 and vip = False', user_id)
        status = await self.conn.fetchrow('SELECT vip FROM users_new Where id = $1', user_id)
        return status['vip']

    # broadcast
    async def get_user_ids(self):  # getting ALL id's to broadcast
        ids = await self.conn.fetch('SELECT user_id from users_new')
        data = ([uid['user_id'] for uid in ids])
        return data

    async def broadcast_get_first_ids(self, user_class, user_profile, user_math):
        ids = await self.conn.fetch(
            'Select user_id From users_new Where user_class = $1 And user_prof = $2 And user_math = $3',
            user_class, user_profile, user_math)
        data = ([uid['user_id'] for uid in ids])
        return data

    async def broadcast_get_class_ids(self, user_class):
        ids = await self.conn.fetch('Select user_id From users_new Where user_class = $1', user_class)
        data = ([uid['user_id'] for uid in ids])
        return data

    async def broadcast_get_profile_ids(self, user_profile):
        ids = await self.conn.fetch('Select user_id From users_new Where user_prof = $1', user_profile)
        data = ([uid['user_id'] for uid in ids])
        return data

    #  ======================== SCHEDULE DATABASE ATTEMPTS ========================

    async def experimental_schedule(self):
        schedule = await self.conn.fetchrow(
            'SELECT l_1, l_2, l_3, l_4, l_5, l_6, l_7, l_8, l_9 From timetable Where day=2')
        text1 = []
        for lesson in schedule:
            data = [f"{lesson}"]
            data = '\n'.join(data)
            if data == 'None':
                break
            text1.append(data)
        text2 = '\n'.join(text1)
        return text2
