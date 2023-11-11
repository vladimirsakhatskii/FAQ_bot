from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from app import keyboard as kb
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from app import database as db
import os

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)

HELP_ADMIN = '''
/help_admin - команды бота,
/description - пока не придумал
Создать вопросы - сделать список, часто задаваемых вопросов
'''

HELP = '''
/help - команды бота,
/description - пока не придумал
Задать вопрос - написать вопрос, который интересует
'''

class QUESTION (StatesGroup):
    question = State()
    key_world = State()


@dp.message_handler (commands=['start'])
async def start_menu(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await bot.send_message(
            text=f'{message.from_user.first_name}, добро пожаловать в окно организатора!',
            chat_id=message.from_user.id,
            reply_markup=kb.kb_admin)
        await message.answer_sticker('CAACAgIAAxkBAAJbeWVOSPO1kfycT6sZDT_nfWEvscivAAL2OQAClS-oS8_duFr-hvoVMwQ')
    else:
        await bot.send_message(
            text=f'{message.from_user.first_name}, добро пожаловать в окно участника!',
            chat_id=message.from_user.id,
            reply_markup=kb.kb)
        await message.answer_sticker('CAACAgIAAxkBAAJbeWVOSPO1kfycT6sZDT_nfWEvscivAAL2OQAClS-oS8_duFr-hvoVMwQ')


@dp.message_handler (commands=['description'])
async def def_description(message: types.Message):
    await message.reply(text='пока не придумал')
    await message.delete()

@dp.message_handler (commands=['help_admin'])
async def def_help(message: types.Message):
    await message.reply(text=HELP_ADMIN)
    await message.delete()

@dp.message_handler (commands=['help'])
async def def_help(message: types.Message):
    await message.reply(text=HELP)
    await message.delete()

@dp.message_handler (text = 'Создать вопросы')
async def def_question(message: types.Message,  state: FSMContext):
    await message.reply(text='Напишите вопрос')
    await state.set_state(QUESTION.num)
    await QUESTION.next()

@dp.message_handler (state = QUESTION.question)
async def add_question(message: types.Message,  state: FSMContext):
    async with state.proxy() as data:
        data['question'] = call.data
    await QUESTION.next()

@dp.message_handler (state = QUESTION.question)
async def add_question(message: types.Message,  state: FSMContext):
    async with state.proxy() as data:
        data['key_world'] = call.data
    await QUESTION.finish()


@dp.message_handler (text = 'Задать вопрос')
async def def_question(message: types.Message):
    await message.reply(text='Пока не придумал')
    await message.delete()


@dp.message_handler()
async def def_error(message: types.Message):
    await message.answer(text='Я тебя не понимаю')


if __name__ == '__main__':
    print('Бот успешно запущен!')
    executor.start_polling(dp)