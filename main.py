from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from app import keyboard as kb
from app import database as db
import os

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)

async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен!')


class VAL (StatesGroup):
    user_name = State()
    user_surname = State()
    user_email = State()
    user_university = State()
    user_phone_number = State()


HELP = """
Помощь - список комманд
Откликнуться - откликнуться на вакансию
Описание - описание бота
Позвонить - показывает номера, куда можно позвонить по вопросам
/cat - прикольный стикер с котёнком
"""

NOMBER = """
8913.......
8904.......
"""


@dp.message_handler (text = 'Помощь')
async def help_menu(message: types.Message):
    await message.reply(text=HELP)

@dp.message_handler (text = 'Позвонить')
async def help_menu(message: types.Message):
    await message.answer(text='Вот номера телефонов')
    await message.reply(text=NOMBER)

@dp.message_handler (text = 'Откликнуться')
async def respond(message: types.Message):
    await VAL.user_name.set()
    await message.answer(text='Введите имя')

@dp.message_handler (state = VAL.user_name)
async def add_respond(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_name'] = message.text
    await message.answer(text = 'Введите фамилию')
    await VAL.next()

@dp.message_handler (state = VAL.user_surname)
async def add_respond(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_surname'] = message.text
    await message.answer(text = 'Введите почту')
    await VAL.next()


@dp.message_handler (state = VAL.user_email)
async def add_respond(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_email'] = message.text
    await message.answer(text = 'Введите название вуза, который закончили')
    await VAL.next()

@dp.message_handler (state = VAL.user_university)
async def add_respond(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_university'] = message.text
    await message.answer(text = 'Введите номер телефона, чтобы мы могли с вами связаться')
    await VAL.next()

@dp.message_handler (state = VAL.user_phone_number)
async def add_respond(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_phone_number'] = message.text
    await db.add_item(state)
    await message.answer(text = 'Ваши данные были добавлены в базу данных')
    await message.answer(text = 'Ждите с вами свяжутся')
    await state.finish()

@dp.message_handler (commands=['start'])
async def start_menu(message: types.Message):
    await bot.send_message(
        text=f'{message.from_user.first_name}, добро пожаловать!',
        chat_id=message.from_user.id,
        reply_markup=kb.kb)
    await message.answer_sticker('CAACAgIAAxkBAAIBYWUr3Tb-uAtGQA9i9lXseYkslWU0AALVDAACKxeYSs2dNpuTnoMBMAQ')
    await message.answer(text='В данном боте вы можете откликнуться на вакансию, вписав боту ваши данные для работодателя')


@dp.message_handler (text = 'Описание')
async def description(message: types.Message):
    await message.answer(text='В данном боте вы можете откликнуться на вакансию, вписав боту ваши данные для работодателя')
    await message.delete()


@dp.message_handler (commands=['cat'])
async def cat_sticker(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAIBf2UsByFX7L9tvSbqYuohdMjpUsJWAAKmJgAC0EQ5SmMpKc4MwbzTMAQ')
    await message.delete()


@dp.message_handler()
async def error(message: types.Message):
    await message.reply(text='^^5@$**&%.......Я тебя не понимаю.......&%$#***&')
    await message.answer(text='Такой команды нету')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup = on_startup)