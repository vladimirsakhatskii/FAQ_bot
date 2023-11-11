from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='/help_admin')
b2 = KeyboardButton(text='/description')
b3 = KeyboardButton(text='Создать вопрос')
b4 = KeyboardButton(text='/list_command')
b5 = KeyboardButton(text='/start')
kb_admin.add(b1,b2,b5)
kb_admin.add(b3)
kb_admin.add(b4)


kb = ReplyKeyboardMarkup(resize_keyboard=True)
b_1 = KeyboardButton(text='/help')
b_2 = KeyboardButton(text='/description')
b_3 = KeyboardButton(text='Задать вопрос')
b_4 = KeyboardButton(text='/list_command')
b_5 = KeyboardButton(text='/alone')
b_6 = KeyboardButton(text='/start')
kb.add(b_1,b_2,b_6)
kb.add(b_3)
kb.add(b_5)
kb.add(b_4)