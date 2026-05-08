from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, declared_attr, mapped_column, relationship
)


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)


class UniqueUserProfileMixin:
    vk_user_id: Mapped[str] = mapped_column(ForeignKey('users.user_id'))
    profile_vk_id: Mapped[str] = mapped_column(String(30))

    __table_args__ = (
        UniqueConstraint('vk_user_id', 'profile_vk_id'),
    )


class User(Base):
    """Данные пользователя VK."""

    user_id: Mapped[str] = mapped_column(String(30), unique=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    age: Mapped[int | None] = mapped_column(Integer, default=None)
    sex: Mapped[int] = mapped_column(Integer)
    city: Mapped[str | None] = mapped_column(String(255), default=None)
    photos: Mapped[str | None] = mapped_column(String, default=None)
    favorites: Mapped[list['Favorite']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
        foreign_keys='Favorite.vk_user_id'
    )
    viewed: Mapped[list['Viewed']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
        foreign_keys='Viewed.vk_user_id'
    )


class Favorite(Base, UniqueUserProfileMixin):
    """Избранные профили текущего пользователя."""

    user: Mapped['User'] = relationship(
        back_populates='favorites',
        foreign_keys='Favorite.vk_user_id'
    )


class Viewed(Base, UniqueUserProfileMixin):
    """Просмотренные профили текущего пользователя."""
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    user: Mapped['User'] = relationship(
        back_populates='viewed',
        foreign_keys='Viewed.vk_user_id'
    )
