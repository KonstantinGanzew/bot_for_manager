import sqlite3 as sq

# Создание бд

def db_start():
    global db, cur
    db = sq.connect('TENDERS.db')
    cur = db.cursor()

    # Определяем существует ли база с таблицей neftehgim_tender, если нет то создаем ее с необходимыми параметрами

    cur.execute('''CREATE TABLE IF NOT EXISTS neftehgim_tender(
        id INTEGER PRIMARY KEY,
        name TEXT, 
        description TEXT, 
        link TEXT, 
        dateStart TEXT, 
        dateEnd TEXT, 
        id_tenderSubject INTEGER,
        tenderSubject TEXT,
        published INTEGER DEFAULT 1,
        actual INTEGER DEFAULT 1)''')
    db.commit()

async def create_profile(user_id, username):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    
    if not user:
        cur.execute('INSERT INTO profile VALUES(?, ?, ?)', (user_id, username, 0))
        db.commit()

# Добавляем элемент в базу

def add_tend(id, name, description, link, dateStart, dateEnd, id_tenderSubject, tenderSubject, published = 1, actual = 1):
    application = cur.execute("SELECT 1 FROM neftehgim_tender WHERE id == '{key}'".format(key=id)).fetchone()
    if not application:
        cur.execute('INSERT INTO neftehgim_tender VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                    (id, name, description, link, dateStart, str(dateEnd), id_tenderSubject, tenderSubject, published, actual)
                    )
        db.commit()

# Проверяем наличие не опубликованых тендоров из базы

def sel_published():
    with sq.connect('TENDERS.db') as con:
        cur = con.cursor()

        cur.execute('''SELECT * FROM neftehgim_tender 
                    WHERE published = 2''')
        return cur.fetchall()

# Обнавляем полe публикации

def up_published(id):
    with sq.connect('TENDERS.db') as con:
        cur = con.cursor()

        cur.execute(f'UPDATE neftehgim_tender SET published = 2 WHERE id={id}')
        return cur.fetchall()

# Обнавляем полe актальности

def up_actual(id):
    with sq.connect('TENDERS.db') as con:
        cur = con.cursor()

        cur.execute(f'UPDATE neftehgim_tender SET actual = 2 WHERE id={id}')
        return cur.fetchall()
    