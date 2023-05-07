from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base


class Grade(Base):
    __tablename__ = 'grades'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Integer)
