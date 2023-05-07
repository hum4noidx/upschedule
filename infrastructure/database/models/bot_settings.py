from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base


class BotSettings(Base):
    __tablename__ = 'bot_settings'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False, default='normal')
