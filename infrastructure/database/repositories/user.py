import logging
from datetime import datetime
from typing import Optional, Union

from pydantic import parse_obj_as
from sqlalchemy import select, insert
from sqlalchemy import update

from infrastructure.database.models.user import User
from infrastructure.database.models.user_profile import UserProfile
from infrastructure.database.repositories.repo import SQLAlchemyRepo
from infrastructure.domain.dto.user import UserDTO

logger = logging.getLogger(__name__)


class UserRepo(SQLAlchemyRepo):
    async def get_user(self, user_id: int = None, username: str = None) -> Union[UserDTO, None]:
        if user_id:
            query = select(User).where(User.user_id == user_id)
        elif username:
            query = select(User).where(User.username == username)
        else:
            return None
        result = (await self.session.execute(query))
        return parse_obj_as(Optional[UserDTO], result.scalars().first())

    async def update_user_if_not_exists(self, user_id: int, full_name: str, registered_at: datetime,
                                        username: str):
        sql = select(User.user_id).where(User.user_id == user_id)
        result = (await self.session.execute(sql)).first()
        if not result:
            await self.session.execute(
                insert(User).values(user_id=user_id, full_name=full_name, registered_at=registered_at,
                                    username=username))
            await self.session.commit()

    async def update_username(self, user_id: int, username: str):
        await self.session.execute(
            update(User).values(username=username).where(
                User.user_id == user_id))
        await self.session.commit()

    async def get_users(self) -> list[UserDTO] | None:
        query = await self.session.execute(select(User).where(User.is_blocked == False))
        result = query.scalars().all()
        return parse_obj_as(list[UserDTO], result) if result else None

    async def get_admins(self) -> list[UserDTO] | None:
        result = await self.session.execute(select(User).where(User.is_admin == True))
        admins = result.scalars().all()
        return parse_obj_as(list[UserDTO], admins) if admins else None

    async def update_user_profile(self, user_id: int, grade: int = None):
        await self.session.execute(
            update(UserProfile).values(grade=grade).where(
                UserProfile.user_id == user_id))
        await self.session.commit()
