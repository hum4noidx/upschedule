from typing import List

from pydantic import parse_obj_as
from sqlalchemy import select, update

from infrastructure.database.models.user import User
from infrastructure.database.repositories.repo import SQLAlchemyRepo
from infrastructure.domain.dto.user import UserDTO


class AdminRepo(SQLAlchemyRepo):
    # ========== Methods for managing users ==========
    async def get_admins(self) -> List[UserDTO]:
        """
        Get all admins
        :return: List[UserDTO]
        """
        _ = await self.session.execute(select(User).where(User.is_admin == True))
        return parse_obj_as(List[UserDTO], _.scalars().all())

    async def add_admin(self, admin_id: int):
        """
        Add admin to database
        Args:
            admin_id: int
        """
        _ = await self.session.execute(update(User).where(User.user_id == admin_id).values(
            is_admin=True))
        await self.session.commit()
        return _.rowcount

    async def remove_rights(self, user_id: int):
        """
        Remove admin and trader rights from user
        Args:
            user_id: int
        """
        _ = await self.session.execute(update(User).where(User.user_id == user_id).values(
            is_admin=False))
        await self.session.commit()
        return _.rowcount

    async def ban_user(self, user_id: int):
        """
        Ban user
        Args:
            user_id: int
        """
        _ = await self.session.execute(update(User).where(User.user_id == user_id).values(
            is_blocked=True, is_admin=False, is_trader=False))
        await self.session.commit()
        return _.rowcount
