from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base


class BotText(Base):
    __tablename__ = 'bot_texts'

    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=True)
