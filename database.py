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
    results1 = cur.fetchall()


#async def grab_question():
#    cur.execute('SELECT question FROM admin')
#    results2 = cur.fetchall()


#async def grab_answer():
#    cur.execute('SELECT answer FROM admin')
#    results3 = cur.fetchall()
