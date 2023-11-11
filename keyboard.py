from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='Помощь')
b2 = KeyboardButton(text='Описание')
b3 = KeyboardButton(text='Откликнуться')
b4 = KeyboardButton(text='Позвонить')

kb.add(b1,b2)
kb.add(b3)
kb.add(b4)