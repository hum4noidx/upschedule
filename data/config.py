from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
ADMINS = env.list('ADMINS')  # Тут у нас будет список из админов

DB_host = env.str('DB_host')
DB_name = env.str('DB_name')
DB_user = env.str('DB_user')
DB_pass = env.str('DB_pass')
DB_port = env.str('DB_port')
