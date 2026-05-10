from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import DATABASE_URL
from database.models import User, Favorite, Viewed


engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(engine, expire_on_commit=False)


def get_or_create_user(user_id, first_name, last_name, age, sex, city_id):
    """Возвращает существующего пользователя или создаёт нового.

    Args:
        user_id: VK ID пользователя
        first_name: имя
        last_name: фамилия
        age: возраст (может быть None если скрыт в профиле)
        sex: пол (1 — женский, 2 — мужской)
        city: город (может быть None если не указан)

    Returns:
        User: объект пользователя из БД
    """
    with Session() as session:
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            user = User(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                age=age,
                sex=sex,
                city_id=city_id,
            )
            session.add(user)
            session.commit()
        return user


def add_to_favorite(current_user_id, profile_user_id):
    """Добавляет профиль в избранное. Игнорирует дубли.

    Args:
        current_user_id: VK ID текущего пользователя
        profile_user_id: VK ID кандидата

    Returns:
        Favorite: новая или существующая запись
    """
    with Session() as session:
        exists = session.query(Favorite).filter_by(
            vk_user_id=current_user_id,
            profile_vk_id=profile_user_id
        ).first()
        if not exists:
            favorite = Favorite(
                vk_user_id=current_user_id,
                profile_vk_id=profile_user_id,
            )
            session.add(favorite)
            session.commit()
            return favorite
        return exists


def get_favorites(current_user_id):
    """Возвращает список избранных профилей пользователя.

    Args:
        current_user_id: VK ID текущего пользователя

    Returns:
        list[Favorite]: список записей избранного
    """
    with Session() as session:
        favorites = session.query(Favorite).filter_by(
            vk_user_id=current_user_id
        ).all()
    return favorites


def add_to_viewed(current_user_id, profile_user_id):
    """Отмечает профиль как просмотренный. Игнорирует дубли.

    Args:
        current_user_id: VK ID текущего пользователя
        profile_user_id: VK ID просмотренного кандидата
    """
    with Session() as session:
        exists = session.query(Viewed).filter_by(
            vk_user_id=current_user_id,
            profile_vk_id=profile_user_id
        ).first()
        if not exists:
            session.add(Viewed(
                vk_user_id=current_user_id,
                profile_vk_id=profile_user_id,
            ))
            session.commit()


def is_viewed(current_user_id, profile_user_id):
    """Проверяет, был ли профиль уже показан пользователю.

    Args:
        current_user_id: VK ID текущего пользователя
        profile_user_id: VK ID кандидата

    Returns:
        bool: True если уже просматривали, False если нет
    """
    with Session() as session:
        return session.query(Viewed).filter_by(
            vk_user_id=current_user_id,
            profile_vk_id=profile_user_id
        ).first() is not None


def get_viewed(current_user_id):
    """Возвращает список избранных профилей пользователя.

    Args:
        current_user_id: VK ID текущего пользователя

    Returns:
        list[Favorite]: список записей избранного
    """
    with Session() as session:
        list_of_viewed = session.query(Viewed).filter_by(
            vk_user_id=current_user_id
        ).all()
    return [viewed.profile_vk_id for viewed in list_of_viewed]