from pydantic import parse_obj_as
from sqlalchemy import update, select

from infrastructure.database.models.bot_settings import BotSettings
from infrastructure.database.models.text import BotText
from infrastructure.database.repositories.repo import SQLAlchemyRepo
from infrastructure.domain.dto.bot import BotDTO
from infrastructure.domain.dto.text import BotTextDTO


class BotRepo(SQLAlchemyRepo):

    async def get_bot_settings(self):
        query = await self.session.get(BotSettings, 1)
        return parse_obj_as(BotDTO, query)

    async def set_maintenance(self):
        await self.session.execute(
            update(BotSettings).where(BotSettings.id == 1).values(status='maintenance')
        )
        await self.session.commit()

    async def disable_maintenance(self):
        await self.session.execute(
            update(BotSettings).where(BotSettings.id == 1).values(status='normal')
        )
        await self.session.commit()

    async def get_texts(self):
        query = await self.session.execute(select(BotText))
        result = query.scalars().all()
        return parse_obj_as(list[BotTextDTO], result)

    async def get_text(self, text_id: str):
        query = await self.session.get(BotText, text_id)
        return BotTextDTO.from_orm(query)

    async def update_text(self, text_id: str, text: str, image: str = None):
        await self.session.execute(
            update(BotText).where(BotText.id == text_id).values(text=text, image=image)
        )
        await self.session.commit()
