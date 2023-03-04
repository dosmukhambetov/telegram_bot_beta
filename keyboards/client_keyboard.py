from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


client_kb = ReplyKeyboardMarkup(resize_keyboard=True)
client_button_1 = KeyboardButton('/start')
client_button_2 = KeyboardButton('/help')
client_button_3 = KeyboardButton('/products')
client_button_4 = KeyboardButton('/description')
client_kb.add(client_button_1).insert(client_button_2).add(client_button_3).insert(client_button_4)
