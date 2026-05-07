import os
import time
from datetime import datetime
import vk_api
from vk_api import VkApiError
from dotenv import load_dotenv

load_dotenv()
vk_token = os.getenv('VK_USER_TOKEN')

vk_session = vk_api.VkApi(token=vk_token)   #сессия
vk = vk_session.get_api()   #приложение

#utils#
def calc_age(bdate: str) -> int:
    """
    вычислить возраст по дате рождения
    :param bdate: дата рождения в виде строки
    :return: возраст в годах в виде числа
    """
    day, month, year = map(int, bdate.split('.'))
    today = datetime.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age

def get_top3_photo(photos: list[dict]) -> list[str]:
    """
    из списка фотографий выбираем 3 самые популярные по количеству лайков
    :param photos: list[dict]
    :return:list[int]
    """
    print("photos count: ", len(photos))
    sorted_photos = sorted(
        photos,
        key=lambda photo: photo['likes']['count'],
        reverse=True
    )
    photo_url = [photo['orig_photo']['url'] for photo in sorted_photos[:3]]
    print("sorted photos count: ", len(photo_url))
    return photo_url

def extract_user_data(item:dict) -> dict:
    user_data = {
        'user_id': item['id'],
        'first_name': item['first_name'],
        'last_name': item['last_name'],
        'sex': "Женский" if item['sex'] == 1 else "Мужской",
        'profile_URL': f"https://vk.com/id{item['id']}"
    }
    if 'bdate' in item and len(item['bdate'].split('.')) == 3:
        user_data['age'] = calc_age(item['bdate'])
    if 'city' in item:
        user_data['city_id'] = item['city']['id']
        user_data['city'] = item['city']['title']

    photos = get_profile_photos(item['id'])
    if photos:
        user_data['photo_URL'] = list()
        user_data['photo_URL'] = get_top3_photo(photos)
    return user_data

#API#
def get_user_info(user_id: int) -> dict:
    """
    users.get()
    Параметры user_ids string
        Перечисленные через запятую идентификаторы пользователей или их короткие имена (screen_name).
        По умолчанию — идентификатор текущего пользователя.

    fields  string
        Список дополнительных полей профилей, которые необходимо вернуть

    :param user_id:
    :return:dict{id, first_name, last_name, sex, city}
    """
    print(user_id)
    try:
        response = vk.users.get(
            user_ids=user_id,
            fields='bdate, sex, city'
        )
    except VkApiError:
        return {}
    if not response:
        return {}
    print(response)

    item = response[0]
    print(item)


    return extract_user_data(item)

def search_user(
        user_sex: int,
        age_from: int,
        age_to: int,
        city_id: int,
        count: int = 2) -> list[dict]:
    """
    users.search()
    Возвращает список пользователей в соответствии с заданным критерием поиска.
    :params:sex
            age_from
            age_to
            city_id
            count
    :return:list[dict]
    """

    try:
        response = vk.users.search(
            sex=user_sex,
            age_from=age_from,
            age_to=age_to,
            city_id=city_id,
            count=count,
            has_photo=1,
            fields='bdate, sex, city'
        )
    except VkApiError:
        return []
    if not response['items']:
        return []

    print(response)

    user_list = []
    for item in response['items']:
        user_data = extract_user_data(item)
        user_list.append(user_data)

    return user_list

def get_profile_photos(user_id: int) -> list[dict]:
    """
    photos.get()
        Возвращает список фотографий в альбоме.

    :param user_id:
    :return:
    После успешного выполнения возвращает объект, содержащий число результатов в поле count
    и массив объектов фотографий в поле items

    Если был задан параметр extended=1, возвращаются дополнительные поля:

    •likes — количество отметок Мне нравится и информация о том, поставил ли лайк текущий пользователь,
    """

    photos = []
    max_photo_cnt = 5
    offset=0
    while True:
        try:
            response = vk.photos.get(
                owner_id=user_id,
                album_id='profile',
                extended=1,
                count=max_photo_cnt,
                offset=offset)

        except VkApiError:
            return []
        print(response)
        items = response['items']
        if not items:
            return []
        photos.extend(items)
        if len(items) < max_photo_cnt:
            break
        offset+=max_photo_cnt
        time.sleep(0.1)
    return photos

def get_photo_by_id(user_id:int, photo_id:int) -> list[dict]:
    """
    photos.getById
        Возвращает информацию о фотографиях по их идентификаторам.
    :param user_id:
    :param photo_id:
    :return:List() фото с параметрами
    """
    try:
        response = vk.photos.getById(
            photos = f"{user_id}_{photo_id}",
            extended = 1)
    except VkApiError:
        return []
    print(response)
    return response

