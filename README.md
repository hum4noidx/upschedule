# 1208 BOT

![1208bot](https://b.radikal.ru/b26/2112/a9/00288387fe79.png "1208bot")

## _Multifunctional Telegram Bot for School_

## Features

- Can simply show lesson schedule for the current day or for tomorrow
- Simple broadcast for different groups or for everyone
- Some cool features for groups, including auto-deleting join messages

## Tech

1208 BOT uses a number of open source projects to work properly:

- [Python] - interpreted high-level general-purpose programming language.
- [PostgreSQL] - awesome database
- [Aiogram] - pretty simple and fully asynchronous framework for Telegram Bot API
- [Asyncpg] - database interface library designed specifically for PostgreSQL and Python/asyncio.

## Installation

First you need to create virtual environment

Go to project folder and create venv

```bash
$ python3 -m venv env
source env/bin/activate
```

When venv is activated you need to install requirements.

```bash
pip install -r requirements.txt
```

## Environment Variables

To run this project, you will need to add the following environment variables to your bot.ini file

```
[tg_bot]
token = your telegram token from @BotFather
admin_id = your telegram id(optional)
use_redis = false

[db]
user = database user(ex. postgres)
password = pass
database = somedatabase
host = 111.111.111.111
```

## Tech Stack

**Back:** Python

**Front:** HTML, CSS, JS, Bootstrap

**Frameworks and libraries:** Aiogram, aiogram_broadcaster, apscheduler, prettytable, DJANGO

## Run Locally

Clone the project

```bash
  git clone https://github.com/hum4noidx/1208bot
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the bot

```bash
  python3 bot.py
```

Start the DJANGO server

```bash
cd mysite
python3 manage.py runserver
```

