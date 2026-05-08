from database.service import get_favorites


def get_favorites_ids(current_user_id):
    """Возвращает список VK ID избранных профилей пользователя.

    Args:
        current_user_id: VK ID текущего пользователя.

    Returns:
        Список строк profile_vk_id в том же порядке, что хранятся в БД.
    """
    list_of_favorites = get_favorites(current_user_id)
    return [favorite.profile_vk_id for favorite in list_of_favorites]
