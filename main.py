from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import keyboard as kb
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
#import database as db
import os



import sqlite3 as sq


async def db_start():
    global db, cur
    db = sq.connect('tg.db')
    cur = db.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY,
    question TEXT NOT NULL,
    key_world TEXT NOT NULL,
    answer TEXT NOT NULL
    )
    ''')
    db.commit()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS member (
        id INTEGER PRIMARY KEY,
        question_member TEXT NOT NULL
        )
        ''')
    db.commit()


async def add_item_admin(state):
    async with state.proxy() as data:
        cur.execute(
                "INSERT INTO admin (question, key_world, answer) VALUES (?, ?, ?)",
                (data['question'], data['key_world'], data['answer']))
        db.commit()


async def add_item_member(state):
    async with state.proxy() as data:
        cur.execute(
                "INSERT INTO member (question_member) VALUES (?)",
                (data['question_member'],))
        db.commit()


async def grab_kay():
    cur.execute('SELECT key_world FROM admin')
    global results1
    results1 = cur.fetchone()


async def grab_question():
    cur.execute('SELECT answer FROM admin')
    global results2
    results2 = cur.fetchone()

async def grab_mem_quest():
    cur.execute('SELECT question_member FROM member')
    global results3
    results3 = cur.fetchone()




#async def grab_answer():
#    cur.execute('SELECT answer FROM admin')
#    results3 = cur.fetchall()




storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db_start()
    print('База данных успешно запущена!')


HELP_ADMIN = '''
/help_admin - команды бота,
/description - пока не придумал
Создать вопросы - сделать список, часто задаваемых вопросов
/list_command - выдаёт список команд из одиночек
/start - запуск бота
'''


HELP = '''
/help - команды бота,
/description - пока не придумал
Задать вопрос - написать вопрос, который интересует
/alone - добавляет человека в список одиночек
/list_command - выдаёт список команд из одиночек
/start - запуск бота
'''


ALONE_TEAMS = []
TEAM = []
ALONE = '''
У Вас нет команды? Тогда мы Вас соединим с другими одиночками.
'''

class QUESTION (StatesGroup):
    question = State()
    key_world = State()
    answer = State()

class QUESTION_MEMBER (StatesGroup):
    question_member = State()


@dp.message_handler (commands=['start'])
async def start_menu(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID_1')):
        await bot.send_message(
            text=f'{message.from_user.first_name}, добро пожаловать в окно организатора!',
            chat_id=message.from_user.id,
            reply_markup=kb.kb_admin)
        await message.answer_sticker('CAACAgIAAxkBAAJbn2VPs2ABl5-2sgWD7qbmvgHwSxbfAALGMwACye14SrqAZc2rgexEMwQ')
        await message.answer("Подарок: https://t.me/addstickers/Hiroys10")
    else:
        await bot.send_message(
            text=f'{message.from_user.first_name}, добро пожаловать в окно участника!',
            chat_id=message.from_user.id,
            reply_markup=kb.kb)
        await message.answer_sticker('CAACAgIAAxkBAAJbn2VPs2ABl5-2sgWD7qbmvgHwSxbfAALGMwACye14SrqAZc2rgexEMwQ')
        await message.answer("Подарок: https://t.me/addstickers/Hiroys10")


@dp.message_handler (commands=['alone'])
async def def_alone(message: types.Message):
    await message.reply(text=ALONE)
    if len(TEAM) != 3:
        TEAM.append(message.from_user.username)
    else:
        ALONE_TEAMS.append(TEAM)


@dp.message_handler (commands=['list_command'])
async def def_alone2(message: types.Message):
    print(TEAM)
    ALONE_TEAMS.append(TEAM)
    await message.answer("Команды для одиночек:")
    await message.answer(ALONE_TEAMS)


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
    await add_item_admin(state)
    await message.answer(text='Вопрос создан')
    await message.answer_sticker('CAACAgIAAxkBAAJboWVPs4gFTYNpBrtKs--gNn5uRV01AALVOAACvkh5SlRivMxMxRCyMwQ')
    await state.finish()


@dp.message_handler (text = 'Задать вопрос')
async def def_question(message: types.Message):
    await QUESTION_MEMBER.question_member.set()
    await message.reply(text='Введите вопрос')



@dp.message_handler (state = QUESTION_MEMBER.question_member)
async def def_question(message: types.Message,  state: FSMContext):
    async with state.proxy() as data:
        data['question_member'] = message.text
    await add_item_member(state)
    await message.reply(text='Ждите ответ')
    await message.answer_sticker('CAACAgIAAxkBAAJbm2VPsbRZNnFF4zlkUwOhNMVk99ccAALNPAACUa6ASrPnlk7T5Xr3MwQ')
    await grab_kay()
    await grab_question()
    await grab_mem_quest()
    if results3 == results1:
        await message.answer(results2)
    print(results3)
    await state.finish()


@dp.message_handler()
async def def_error(message: types.Message):
    await message.answer(text='Я тебя не понимаю')
    await message.answer_sticker('CAACAgIAAxkBAAJbnWVPsfNvdPa7HoeQQmr9NZLxbhdAAAI0PAACb2CBSlicqJQdLg9AMwQ')


if __name__ == '__main__':
    print('Бот успешно запущен!')
    executor.start_polling(dp, on_startup = on_startup)