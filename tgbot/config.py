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
    webhook_host: str
    webhook_path: str
    webapp_host: str
    webapp_port: str
    webhook_enabled: bool
    use_local_server: bool


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
            webhook_host=tg_bot["WEBHOOK_HOST"],
            webhook_path=tg_bot["WEBHOOK_PATH"],
            webapp_host=tg_bot["WEBAPP_HOST"],
            webapp_port=tg_bot["WEBAPP_PORT"],
            webhook_enabled=cast_bool(tg_bot.get("WEBHOOK_ENABLED")),
            use_local_server=cast_bool(tg_bot.get("USE_LOCAL_SERVER"))
        ),
        db=DbConfig(**config["db"]),
        hosting=Hosting(**config['host'])
    )
