from typing import List

from database.models import Favorite


def get_favorites_ids(list_of_favorites: List[Favorite]):
    """Возвращает список VK ID из записей избранного.

    Args:
        list_of_favorites: список объектов Favorite.

    Returns:
        Список строк profile_vk_id в том же порядке.
    """
    return [favorite.profile_vk_id for favorite in list_of_favorites]

