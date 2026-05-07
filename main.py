import os
from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

from database.models import Base
from database.service import engine

load_dotenv()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

vk = vk_api.VkApi(token=os.getenv('VK_GROUP_TOKEN'))
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {
              'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7), })


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            user_info = vk.method('users.get', {'user_ids': event.user_id, 'fields': 'bdate, city'})[0]

            if request == "привет":
                print(user_info)
                write_msg(event.user_id, f"Хай, {user_info}!!!")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
