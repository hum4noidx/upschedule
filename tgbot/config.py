import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    redis_pass: str


@dataclass
class TgBot:
    token: str
    admin_id: int
    use_redis: bool
    lang: str


@dataclass
class Hosting:
    authorization: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    hosting: Hosting


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config['tg_bot']

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            admin_id=int(tg_bot["admin_id"]),
            use_redis=cast_bool(tg_bot.get("use_redis")),
            lang=tg_bot["bot_language"],
        ),
        db=DbConfig(**config["db"]),
        hosting=Hosting(**config['host'])
    )
