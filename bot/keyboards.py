from vkbottle import Keyboard, KeyboardButtonColor, Text

KEYBOARD_NEW_USER = Keyboard(one_time=True, inline=False)
KEYBOARD_NEW_USER.add(Text("Начать знакомства", {"cmd": "new_start_dating"}),
                      color=KeyboardButtonColor.POSITIVE)
KEYBOARD_NEW_USER.add(Text("Закончить диалог",
                      {"cmd": "new_end_conversation"}),
                      color=KeyboardButtonColor.NEGATIVE)


KEYBOARD_MAIN_MENU = Keyboard(one_time=True, inline=False)
KEYBOARD_MAIN_MENU.add(Text("Искать знакомства", {"cmd": "to_dating"}),
                       color=KeyboardButtonColor.POSITIVE)
KEYBOARD_MAIN_MENU.add(Text("Посмотреть избранное", {"cmd": "to_favourites"}),
                       color=KeyboardButtonColor.NEGATIVE)

KEYBOARD_DATING = Keyboard(one_time=True, inline=False)
KEYBOARD_DATING.add(Text("В избранное", {"cmd": "dating_add_to_favourites"}),
                    color=KeyboardButtonColor.POSITIVE)
KEYBOARD_DATING.add(Text("Дальше", {"cmd": "dating_next_variant"}),
                    color=KeyboardButtonColor.NEGATIVE)
KEYBOARD_DATING.row()
KEYBOARD_DATING.add(Text("В главное меню", {"cmd": "to_main_menu"}),
                    color=KeyboardButtonColor.PRIMARY)

KEYBOARD_FAVOURITES = Keyboard(one_time=True, inline=False)
KEYBOARD_FAVOURITES.add(Text("Дальше", {"cmd": "next_favourite"}),
                        color=KeyboardButtonColor.POSITIVE)
KEYBOARD_FAVOURITES.add(Text("В главное меню", {"cmd": "to_main_menu"}),
                        color=KeyboardButtonColor.NEGATIVE)

KEYBOARD_TO_MAIN_MENU = Keyboard(one_time=True, inline=False)
KEYBOARD_TO_MAIN_MENU.add(Text("В главное меню", {"cmd": "to_main_menu"}),
                          color=KeyboardButtonColor.POSITIVE)
