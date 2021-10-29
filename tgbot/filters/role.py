import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types.base import TelegramObject

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo


class RoleFilter(BoundFilter):
    key = 'role'

    def __init__(self, role: typing.Union[None, UserRole, typing.Collection[UserRole]] = None):
        if role is None:
            self.roles = None
        elif isinstance(role, UserRole):
            self.roles = {role}
        else:
            self.roles = set(role)

    async def check(self, obj: TelegramObject):
        if self.roles is None:
            return True
        data = ctx_data.get()
        return data.get("role") in self.roles


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj: TelegramObject):
        data = ctx_data.get()
        repo = data.get("repo")
        if self.is_admin is None or self.is_admin is False:
            return True
        else:
            return obj.from_user.id in await repo.get_admins()


class VIPFilter(BoundFilter):
    key = 'is_vip'

    def __init__(self, is_vip: typing.Optional[bool] = None):
        self.is_vip = is_vip

    async def check(self, obj: TelegramObject):
        data = ctx_data.get()
        repo = data.get("repo")
        if self.is_vip is None or self.is_vip is False:
            return True
        else:
            return obj.from_user.id in await repo.get_vips()
