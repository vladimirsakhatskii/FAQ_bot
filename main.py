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


async def on_startup(_):
    await db.db_start()
    print('База данных успешно запущена!')


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
    answer = State()


@dp.message_handler (commands=['start'])
async def start_menu(message: types.Message):
    if (message.from_user.id == int(os.getenv('ADMIN_ID_1'))) or (message.from_user.id == int(os.getenv('ADMIN_ID_2'))):
        await bot.send_message(
            text=f'{message.from_user.first_name}, добро пожаловать в окно организатора!',
            chat_id=message.from_user.id,
            reply_markup=kb.kb_admin)
        await message.answer_sticker('CAACAgIAAxkBAAJbgWVPVqh6R2jme1XPYujOay8f5mxwAALyOwACO4Z5St1QvCGWR8SGMwQ')
    else:
        await bot.send_message(
            text=f'{message.from_user.first_name}, добро пожаловать в окно участника!',
            chat_id=message.from_user.id,
            reply_markup=kb.kb)
        await message.answer_sticker('CAACAgIAAxkBAAJbgWVPVqh6R2jme1XPYujOay8f5mxwAALyOwACO4Z5St1QvCGWR8SGMwQ')


@dp.message_handler (commands=['description'])
async def def_description(message: types.Message):
    await message.reply(text='пока не придумал')


@dp.message_handler (commands=['help_admin'])
async def def_help(message: types.Message):
    await message.reply(text=HELP_ADMIN)


@dp.message_handler (commands=['help'])
async def def_help(message: types.Message):
    await message.reply(text=HELP)


@dp.message_handler (text = 'Создать вопрос')
async def def_question(message: types.Message):
    await QUESTION.question.set()
    await message.reply(text='Напишите вопрос')


@dp.message_handler (state = QUESTION.question)
async def add_question(message: types.Message,  state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
    await message.answer(text = 'Напишите ключевое слово')
    await QUESTION.next()


@dp.message_handler (state = QUESTION.key_world)
async def add_question(message: types.Message,  state: FSMContext):
    async with state.proxy() as data:
        data['key_world'] = message.text
    await message.answer(text='Напишите ответ на вопрос')
    await QUESTION.next()


@dp.message_handler (state = QUESTION.answer)
async def add_question(message: types.Message,  state: FSMContext):
    async with state.proxy() as data:
        data['answer'] = message.text
    await db.add_item(state)
    await message.answer(text='Вопрос создан')
    await message.answer_sticker('CAACAgIAAxkBAAJbg2VPVsrAvcqdL1rUZRigLS9ACpeeAALMNgAC9GmASlZMmFp0lZCIMwQ')
    await state.finish()


@dp.message_handler (text = 'Задать вопрос')
async def def_question(message: types.Message):
    await message.reply(text='Пока не придумал')


@dp.message_handler()
async def def_error(message: types.Message):
    await message.answer(text='Я тебя не понимаю')


if __name__ == '__main__':
    print('Бот успешно запущен!')
    executor.start_polling(dp, on_startup = on_startup)