from sqlalchemy import BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import Base


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'),
                                         primary_key=True)
    grade: Mapped[int] = mapped_column(Integer, ForeignKey('grades.id', ondelete='CASCADE'))
    user = relationship('User', uselist=False, back_populates='profile', foreign_keys=[user_id])
