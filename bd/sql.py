import sqlite3 as sq

# Создание бд
async def db_start():
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
    cur.execute('''CREATE TABLE IF NOT EXISTS employees(
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        newsletter INTEGER)
        ''')
    db.commit()

# Добавляет вновь прибывших сотрудников
async def create_profile(user_id, username):
    user = cur.execute("SELECT 1 FROM employees WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    
    if not user:
        cur.execute('INSERT INTO employees VALUES(?, ?, ?)', (user_id, username, 1))
        db.commit()

# Добавляем элемент в базу
async def add_tend(id, name, description, link, dateStart, dateEnd, id_tenderSubject, tenderSubject, published = 1, actual = 1):
    application = cur.execute("SELECT 1 FROM neftehgim_tender WHERE id == '{key}'".format(key=id)).fetchone()
    if not application:
        cur.execute('INSERT INTO neftehgim_tender VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                    (id, name, description, link, dateStart, str(dateEnd), id_tenderSubject, tenderSubject, published, actual)
                    )
        db.commit()

# Проверяем наличие не опубликованых тендоров из базы
async def sel_published():
    with sq.connect('TENDERS.db') as con:
        cur = con.cursor()

        cur.execute('''SELECT * FROM neftehgim_tender WHERE published = 1''')
        return cur.fetchall()

# Обнавляем полe публикации
async def up_published(id):
    with sq.connect('TENDERS.db') as con:
        cur = con.cursor()

        cur.execute(f'UPDATE neftehgim_tender SET published = 2 WHERE id={id}')
        return cur.fetchall()

# Обнавляем полe актальности
async def up_actual(id):
    with sq.connect('TENDERS.db') as con:
        cur = con.cursor()

        cur.execute(f'UPDATE neftehgim_tender SET actual = 2 WHERE id={id}')
        return cur.fetchall()

# Осуществляем выбурку из всей таблицы тендеры
async def all_tender():
    with sq.connect('TENDERS.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM neftehgim_tender')
        return cur.fetchall()

# Осуществляем выбурку из всей таблицы тендеры по типу работы
async def tender_9():
    with sq.connect('TENDERS.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM neftehgim_tender WHERE id_tenderSubject = 9')
        return cur.fetchall()

# Меняет статус на рассылке сотрудников
async def get_mailing(id, status):
    with sq.connect('TENDERS.db') as con:
        cur = con.cursor()
        cur.execute(f'UPDATE employees SET newsletter = {status} WHERE user_id = {id}')
        return cur.fetchall()

# Посмотреть статус рассылки
async def mailing_status(id):
    with sq.connect('TENDERS.db') as con:
        cur = con.cursor()
        cur.execute('SELECT newsletter FROM employees WHERE user_id = ' + id)
        return cur.fetchall()

# Посмотреть статус рассылки
async def mailing_empl():
    with sq.connect('TENDERS.db') as con:
        cur = con.cursor()
        cur.execute('SELECT user_id FROM employees WHERE newsletter = 2')
        return cur.fetchall()