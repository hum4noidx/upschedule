from aiogram.dispatcher.filters import BoundFilter
from typing import Optional
from aiogram.types.base import TelegramObject
from utils.db_api.db import DBAdmin


class IsVIP(BoundFilter):
    key = 'is_vip'

    def __init__(self, is_vip: Optional[bool] = None):
        self.is_vip = is_vip

    async def check(self, obj: TelegramObject):
        if self.is_vip is None or self.is_vip is False:
            return True
        else:
            return obj.from_user.id in await DBAdmin.vips()
