import os
import pprint
import vk_api
from vk_api import VkApiError
from vk_lib import get_user_info, search_user
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

load_dotenv()
vk_group_key = os.getenv('VK_GROUP_API_KEY')
vk_bot = vk_api.VkApi(token=vk_group_key)   #бот#сообщество

#Бот
def create_keyboard():
    keyboard = VkKeyboard(one_time=True)  # Создаем клавиатуру
    keyboard.add_button('Привет', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Найди друга', color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()

def send_message(user_id:int, message:str, keyboard: None) -> int:
    """
    #бот
    messages.send
        Метод отправляет сообщение.
    :param user_id:
    :param message:
    :return: message_id
    """

    try:
        response = vk_bot.method('messages.send', {
            'user_id': user_id,
            'message': message,
            'random_id': 0,
            'keyboard' : keyboard
        })
    except VkApiError:
        return -1
    if not response:
        return -1
    print(response)

    return response

#util#
def create_message_user_info(user_info:dict) -> str:
    if 'photo_URL' in user_info:
        message = f"Привет, {user_info['first_name']} {user_info['last_name']}\n{user_info['profile_URL']}\n{user_info['photo_URL']}"
    else:
        message = f"Привет, {user_info['first_name']} {user_info['last_name']}\n{user_info['profile_URL']}\nФото в профиле нет"
    return message

#main process#
def vk_process():
    user_info = dict()
    # Работа с сообщениями
    longpoll = VkLongPoll(vk_bot)

    # Основной цикл
    for event in longpoll.listen():

        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:

            # Если оно имеет метку для меня( то есть бота)
            if event.to_me:

                # Сообщение от пользователя
                request = event.text.lower()

                # логика ответа
                if request == "привет":
                    test_id = event.user_id
                    user_info[test_id] = get_user_info(test_id)
                    pprint.pprint(user_info)
                    send_message(user_id=event.user_id, message = create_message_user_info(user_info[test_id]), keyboard = create_keyboard())
                elif request == "найди друга":
                    send_message(user_id=event.user_id, message = "Ищем друзей", keyboard = create_keyboard())
                    result = search_user(
                        user_sex=1,
                        age_from = 47,
                        age_to = 49,
                        city_id = 122)
                    pprint.pprint(result)
                    for item in result:
                        send_message(user_id=event.user_id, message=create_message_user_info(item), keyboard = create_keyboard())
                elif request == 'начать':
                    send_message(user_id=event.user_id, message = 'Привет! Начнем?', keyboard = create_keyboard())
                else:
                    send_message(user_id=event.user_id, message = "Не поняла вашего ответа...", keyboard = create_keyboard())

#main#
if __name__ == '__main__':
    vk_process()