from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_button_1 = KeyboardButton('/admin')
admin_button_2 = KeyboardButton('/download')
admin_button_3 = KeyboardButton('/delete')
admin_button_4 = KeyboardButton('/cancel')
admin_button_5 = KeyboardButton('/home')
admin_kb.add(admin_button_1).insert(admin_button_2).add(admin_button_3).insert(admin_button_4).add(admin_button_5)
