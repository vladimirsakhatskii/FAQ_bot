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


async def add_item(state):
    async with state.proxy() as data:
        cur.execute(
                "INSERT INTO admin (question, key_world, answer) VALUES (?, ?, ?)",
                (data['question'], data['key_world'], data['answer']))
        db.commit()