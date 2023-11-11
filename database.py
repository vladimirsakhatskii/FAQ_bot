import sqlite3 as sq

db = sq.connect('tg.db')
cur = db.cursor()

async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "user_name TEXT, "
                "user_surname TEXT, "
                "user_email varchar, "
                "user_university TEXT, "
                "user_phone_number TEXT)")
    db.commit()

async def add_item(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO accounts (user_name, user_surname, user_email, user_university, user_phone_number) VALUES (?, ?, ?, ?, ?)",
                    (data['user_name'], data['user_surname'], data['user_email'], data['user_university'], data['user_phone_number']))
        db.commit()


