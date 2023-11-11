from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='/help_admin')
b2 = KeyboardButton(text='/description')
b3 = KeyboardButton(text='Создать вопросы')
kb_admin.add(b1,b2)
kb_admin.add(b3)


kb = ReplyKeyboardMarkup(resize_keyboard=True)
b_1 = KeyboardButton(text='/help')
b_2 = KeyboardButton(text='/description')
b_3 = KeyboardButton(text='Задать вопрос')
kb.add(b_1,b_2)
kb.add(b_3)