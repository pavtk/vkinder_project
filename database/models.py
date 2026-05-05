from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, relationship, validates


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)


class UniqueUserProfileMixin:
    user_vk_id: Mapped[str] = mapped_column(ForeignKey('users.vk_id'))
    profile_vk_id: Mapped[str] = mapped_column(String(30))
    photos: Mapped[str | None] = mapped_column(String)

    __table_args__ = (
        UniqueConstraint('user_vk_id', 'profile_vk_id'),
    )


class User(Base):
    vk_id: Mapped[str] = mapped_column(String(30), unique=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    age: Mapped[int] = mapped_column(Integer)
    sex: Mapped[int] = mapped_column(Integer)
    city: Mapped[str | None] = mapped_column(String(255))
    favorites: Mapped[list['Favorite']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )
    viewed: Mapped[list['Viewed']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )

    @validates('age')
    def validate_age(self, key, value):
        if not (18 <= value <= 100):
            raise ValueError(
                f'Возраст дложен быть от 18 до 100, сейчас {value}')
        return value


class Favorite(Base, UniqueUserProfileMixin):
    user: Mapped['User'] = relationship(back_populates='favorites')


class Viewed(Base, UniqueUserProfileMixin):
    user: Mapped['User'] = relationship(back_populates='viewed')
