# Upschedule[LEGACY]
![App Logo](https://github.com/hum4noidx/upschedule/blob/main/logo.png?raw=true)
## _Multifunctional Telegram Bot for School_

## Tech

Upschedule uses a number of open source projects to work properly:

- [Python] - interpreted high-level general-purpose programming language.
- [PostgreSQL] - awesome database
- [Aiogram] - pretty simple and fully asynchronous framework for Telegram Bot API
- [Asyncpg] - database interface library designed specifically for PostgreSQL and Python/asyncio.

## Features

- Can simply show lesson schedule for the current day or for tomorrow
- Simple broadcast for different groups or for everyone
- Some cool features for groups, including auto-deleting join messages

## Installation

First you need to create virtual environment

Go to project folder and create venv

```bash
$ python3 -m venv env
source env/bin/activate
```

When venv is activated you need to install requirements for **bot**

```bash
cd tgbot
pip install -r requirements.txt
```

If you also want to install a website:

```bash
cd website
pip install -r requirements.txt
```

## Environment Variables

To run this project, you will need to add the following environment variables to your bot.ini file

```
[tg_bot]
token = your bot TOKEN here
admin_id = your telegram id or chat_id
use_redis = false
# if you want to store user's state, you need to use redis
bot_language = ru

[db]
user = your database_user
password = database_pass
database = database_name
host = database_host
redis_pass = password_for_your_redis
```
## Run Locally

Clone the project

```bash
  git clone https://github.com/hum4noidx/upschedule
```

Go to the project directory

```bash
  cd my-project
```

Start the bot

```bash
  python3 bot.py
```

Start the DJANGO server(optionally)

```bash
cd mysite
python3 manage.py runserver
```

## Tech Stack

**Back:** Python

**Front:** HTML, CSS, JS, Bootstrap

**Frameworks and libraries:** Aiogram, aiogram_broadcaster, apscheduler, prettytable, DJANGO
