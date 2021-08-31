import asyncpg
from aiogram import types

from data.config import DB_host, DB_name, DB_user, DB_pass, DB_port


class DBComm:
    async def db_new_user(use=True, uses=1):
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        user = types.User.get_current()
        user_id = user.id
        full_name = user.full_name
        args = (user_id, use, full_name)
        await conn.execute('INSERT INTO users (user_id, use, full_name, uses) VALUES ($1, $2, $3, $4) RETURNING id',
                           user_id, use, full_name, uses)
        await conn.close()

    async def db_user_exists():
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        user = types.User.get_current()
        user_id = user.id
        result = await conn.execute('SELECT * FROM users WHERE user_id = $1', user_id)
        result = int(result.replace('SELECT', ''))
        await conn.close()
        return bool(result)

    async def db_usage():
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        user = types.User.get_current()
        user_id = user.id
        await conn.execute('UPDATE users  SET uses = uses + 1 WHERE user_id = $1', user_id)
        await conn.close()

    async def reg_class(info):
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        user = types.User.get_current()
        user_id = user.id
        num = int(info)
        await conn.execute('UPDATE users  SET user_class = $2 WHERE user_id = $1', user_id, num)
        await conn.close()

    async def reg_profile(info, math):
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        user = types.User.get_current()
        user_id = user.id
        await conn.execute('UPDATE users  SET prof = $2, math = $3 WHERE user_id = $1', user_id, info, math)
        await conn.close()

    async def get_schedule():
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        user = types.User.get_current()
        user_id = user.id
        data = await conn.fetchrow('SELECT user_class,prof, math FROM users WHERE user_id = $1', user_id)
        a = dict(data)
        return a


class DBAdmin:
    async def db_get_info(info):
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        uid = int(info)
        rer = await conn.fetchrow('SELECT * FROM users WHERE id = $1', uid)
        in1 = dict(rer)
        text = (f'ID - <code>{in1["id"]}</code>\n'
                f'User_ID - <code>{in1["user_id"]}</code>\n'
                f'Пользовался? - <code>{in1["use"]}</code>\n'
                f'Количество использований - <code>{in1["uses"]}</code>\n'
                f'Класс пользователя - <code>{in1["user_class"]}</code>\n"'
                f'Профиль пользователя - <code>{in1["prof"]}</code>\n"'
                f'Имя - <code>{in1["full_name"]}</code>\n"'
                f'VIP - <code>{in1["vip"]}</code>')
        await conn.close()
        return text

    async def db_get_all_info():
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        all_info = await conn.fetch('SELECT id, full_name FROM users ORDER BY id')
        a = dict(all_info)
        data = [f"{k}-{v}" for k, v in a.items()]
        text = "\n".join(data)
        await conn.close()
        return text

    async def get_user_ids():
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        ids = await conn.fetch('SELECT user_id from users')
        data = ([id['user_id'] for id in ids])
        await conn.close()
        return data

    async def db_add_vip(info):
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        uid = int(info)
        await conn.execute('UPDATE users SET vip = true WHERE user_id = $1', uid)
        await conn.close()

    async def vips():
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        vips = await conn.fetch('SELECT user_id FROM users WHERE vip = True')
        data = ([vip['user_id'] for vip in vips])
        await conn.close()
        return data

    async def user_profile_broadcast(b_class, b_prof):
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        _class = int(b_class)
        users = await conn.fetch('SELECT user_id FROM users where prof = $1 AND user_class = $2', b_prof, _class)
        data = ([user['user_id'] for user in users])
        print(data)
        await conn.close()
        return data


class DBGroup:
    async def db_add_group(chat_id, group_name):
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        await conn.execute('INSERT INTO groups (chat_id, group_name) VALUES ($1, $2)', chat_id, group_name)
        await conn.close()

    async def db_group_exists(chat_id):
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        result = await conn.execute('SELECT * FROM groups WHERE chat_id = $1', chat_id)
        result = int(result.replace('SELECT', ''))
        await conn.close()
        return bool(result)

    async def db_group_update(chat_id, group_name):
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        await conn.execute('UPDATE groups SET group_name = $1 WHERE chat_id = $2', group_name, chat_id)
        await conn.close()

    async def create_note(note_id, note_text, note_owner, chat_id):
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        await conn.execute('INSERT INTO notes (note_id, note_text, note_owner, chat_id) VALUES($1, $2, $3, $4)', note_id, note_text,
                           note_owner, chat_id)
        await conn.close()

    async def show_notes(chat_id):
        conn = await asyncpg.connect(host=DB_host, database=DB_name, user=DB_user, password=DB_pass,
                                     port=DB_port)
        result = await conn.fetch('SELECT note_id, note_text FROM notes WHERE chat_id = $1 ORDER BY note_id', chat_id)
        a = dict(result)
        data = [f"ID - {k}\nТекст - {v}\n" for k, v in a.items()]
        text = "\n".join(data)
        await conn.close()
        return text
