import os

from database.models import Base
from database.service import add_to_favorite, add_to_viewed, get_favorites, get_or_create_user, engine, get_viewed, is_viewed
from dotenv import load_dotenv

from utils import get_favorites_ids
from vk.vk_lib import extract_user_data, get_user_info, get_user_only_id, search_user
from vkbottle import BaseStateGroup
from vkbottle.bot import Bot, Message
from vkinder_project.bot.keyboards import KEYBOARD_DATING, KEYBOARD_FAVOURITES, KEYBOARD_MAIN_MENU, KEYBOARD_TO_MAIN_MENU


load_dotenv()
BOT_TOKEN = os.environ["VK_BOT_TOKEN"]
API_TOKEN = os.environ["VK_API_TOKEN"]


bot = Bot(token=BOT_TOKEN)

class BotState(BaseStateGroup):
    NEW_USER_MENU = "new_user_menu"
    MAIN_MENU = "main_menu"
    DATING = "dating"
    FAVOURITES = "favourites"


# Новое сообщение, если стейт не задан
@bot.on.private_message(state=None)
async def greet_handler(message: Message):
    user = get_user_info(message.from_id)
    print('USER = ', user)
    print(user['city_id'])
    get_or_create_user(str(user['user_id']), user['first_name'], user['last_name'], user['age'], user['sex'], user['city_id'])


    await message.answer(f"Привет,  {user['first_name']}")
    await message.answer("Чем хочешь заняться?", keyboard=KEYBOARD_MAIN_MENU)

    await bot.state_dispenser.set(
        message.peer_id, 
        BotState.MAIN_MENU, 
        user=user
        )


# Знакомства
@bot.on.private_message(state=BotState.MAIN_MENU, payload={"cmd": "to_dating"}) # Кнопка 'Искать знакомства'
async def start_dating(message: Message):
    state_peer = await bot.state_dispenser.get(message.peer_id)
    user = state_peer.payload["user"]
    search_index = 1
    search_sex_id = 2 if user['sex'] == 1 else 1
    search_user_id = get_user_only_id(search_sex_id, user['age'],user['city_id'], search_index)
    viewed_list = get_viewed(str(user['user_id']))
    is_user_viewed = str(search_user_id) in viewed_list

    while is_user_viewed:
        search_index += 1
        search_user_id = get_user_only_id(search_sex_id, user['age'],user['city_id'], search_index)
        is_user_viewed = str(search_user_id) in viewed_list

    search_result = get_user_info(search_user_id)

    await message.answer(f"{search_result['first_name']} {search_result['last_name']}{', г. ' + search_result['city'] if search_result['city'] is not None else ''}{', ' + str(search_result['age']) + ' лет' if search_result['age'] is not None else ''}", attachment=[*search_result["photo_URL"]],  keyboard=KEYBOARD_DATING)

    add_to_viewed(str(user['user_id']),str(search_result['user_id']))
    viewed_list.append(str(search_result['user_id']))
    search_index += 1
    await bot.state_dispenser.set(
        message.peer_id, 
        BotState.DATING, 
        user=user,
        search_index=search_index,
        current_search_user=search_result,
        viewed_list=viewed_list
        )
    

@bot.on.private_message(state=BotState.DATING, payload={"cmd": "dating_next_variant"}) # Кнопка 'Дальше' в знакомствах
async def next_dating(message: Message):
    state_peer = await bot.state_dispenser.get(message.peer_id)
    user = state_peer.payload["user"]

    search_index = state_peer.payload["search_index"]
    search_sex_id = 2 if user['sex'] == 1 else 1
    search_user_id = get_user_only_id(search_sex_id, user['age'],user['city_id'], search_index)

    viewed_list = get_viewed(str(user['user_id']))
    is_user_viewed = str(search_user_id) in viewed_list

    
    while is_user_viewed:
        search_index += 1
        search_user_id = get_user_only_id(search_sex_id, user['age'],user['city_id'], search_index)
        is_user_viewed = str(search_user_id) in viewed_list

    search_result = get_user_info(search_user_id)
    await message.answer(f"{search_result['first_name']} {search_result['last_name']}{', г. ' + search_result['city'] if search_result['city'] is not None else ''}{', ' + str(search_result['age']) if search_result['age'] is not None else ''}", attachment=[*search_result["photo_URL"]],  keyboard=KEYBOARD_DATING)

    add_to_viewed(str(user['user_id']),str(search_result['user_id']))
    viewed_list.append(str(search_result['user_id']))
    search_index += 1
    await bot.state_dispenser.set(
        message.peer_id, 
        BotState.DATING, 
        user=user,
        search_index=search_index,
        current_search_user=search_result,
        viewed_list=viewed_list
        )


@bot.on.private_message(state=BotState.DATING, payload={"cmd": "dating_add_to_favourites"}) # Кнопка 'В избранное' в знакомствах
async def add_to_favourite(message: Message):
    state_peer = await bot.state_dispenser.get(message.peer_id)
    user = state_peer.payload["user"]
    current_search_user = state_peer.payload["current_search_user"]
    search_index = state_peer.payload["search_index"]
    search_index += 1
    search_sex_id = 2 if user['sex'] == 1 else 1
    search_result = search_user(search_sex_id, user['age'],user['city'], search_index)
    search_index += 1

    add_to_favorite(str(user['user_id']), str(current_search_user['user_id']))

    await bot.state_dispenser.set(
        message.peer_id, 
        BotState.DATING, 
        user=user,
        search_index=search_index,
        current_search_user=search_result
        )
    
    await message.answer(f"Пользователь {current_search_user['first_name']} {current_search_user['last_name']} добавлен в избранное")
    await message.answer(f"{search_result['first_name']} {search_result['last_name']}{', г. ' + search_result['city'] if search_result['city'] is not None else ''}{', ' + str(search_result['age']) if search_result['age'] is not None else ''}", attachment=[*search_result["photo_URL"]],  keyboard=KEYBOARD_DATING)


@bot.on.private_message(state=BotState.MAIN_MENU, payload={"cmd": "to_favourites"}) # Кнопка 'Посмотреть избранное'
async def go_to_favourite(message: Message):
    state_peer = await bot.state_dispenser.get(message.peer_id)
    user = state_peer.payload["user"]
    favourites_list = get_favorites_ids(str(message.from_id))

    current_index = 0
    favourite_user_info = get_user_info(favourites_list[current_index])
    current_index += 1

    if len(favourites_list) == 0:
        await message.answer("Список избранного пока что пуст", keyboard=KEYBOARD_TO_MAIN_MENU)

        return
    
    await bot.state_dispenser.set(
        message.peer_id, 
        BotState.FAVOURITES, 
        current_index=current_index,
        favourites_list=favourites_list,
        user=user,
        )

    await message.answer(f"{favourite_user_info['first_name']} {favourite_user_info['last_name']}{', г. ' + favourite_user_info['city'] if favourite_user_info['city'] is not None else ''}{', ' + str(favourite_user_info['age']) + ' лет' if favourite_user_info['age'] is not None else ''}",attachment=[*favourite_user_info["photo_URL"]], keyboard=KEYBOARD_FAVOURITES)

    if len(favourites_list) == 1:
        await message.answer("Это последний элемент списка!", keyboard=KEYBOARD_TO_MAIN_MENU)


@bot.on.private_message(state=BotState.FAVOURITES, payload={"cmd": "next_favourite"}) # Кнопка 'Дальше' в избранном
async def next_favourite(message: Message):
    state_peer = await bot.state_dispenser.get(message.peer_id)
    user = state_peer.payload["user"]
    favourites_list = state_peer.payload["favourites_list"]
    current_index = state_peer.payload["current_index"]
    favourite_user_info = get_user_info(favourites_list[current_index])
    current_index += 1

    if len(favourites_list) == 0:
        await message.answer("Список избранного пока что пуст", keyboard=KEYBOARD_TO_MAIN_MENU)

        return

    await bot.state_dispenser.set(
        message.peer_id, 
        BotState.FAVOURITES, 
        current_index=current_index,
        favourites_list=favourites_list,
        user=user,
        )

    await message.answer(f"{favourite_user_info['first_name']} {favourite_user_info['last_name']}{', г. ' + favourite_user_info['city'] if favourite_user_info['city'] is not None else ''}{', ' + str(favourite_user_info['age']) + ' лет' if favourite_user_info['age'] is not None else ''}",attachment=[*favourite_user_info["photo_URL"]], keyboard=KEYBOARD_FAVOURITES)

    if len(favourites_list) == 1 or len(favourites_list) == current_index:
        await message.answer("Это последний элемент списка!", keyboard=KEYBOARD_TO_MAIN_MENU)
    

@bot.on.private_message(payload={"cmd": "to_main_menu"}) # Кнопка 'В главное меню'
async def go_to_main_menu(message: Message):
    state_peer = await bot.state_dispenser.get(message.peer_id)
    user = state_peer.payload["user"]
    await message.answer("Чем хочешь заняться?", keyboard=KEYBOARD_MAIN_MENU)
    await bot.state_dispenser.set(
        message.peer_id, 
        BotState.MAIN_MENU, 
        user=user
        )


if __name__ == "__main__":
    bot.run_forever()
