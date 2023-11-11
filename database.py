from sqlite3 import*

connection = sqlite3.connect('my_tg.db')
cur = connection.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS admin (
id INTEGER PRIMARY KEY,
question TEXT NOT NULL,
key_world TEXT NOT NULL
)
''')
cur.commit()

async def def_insert_question():
    async with state.proxy() as data:
        cur.execute(('INSERT INTO admin (question) VALUES (?)', ('question',)))
    cur.commit()