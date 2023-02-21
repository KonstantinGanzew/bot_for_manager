import sqlite3 as sq

async def db_start():
    global db, cur
    global db1, cur1
    db = sq.connect('user.db')
    db1 = sq.connect('tender.db')

    cur = db.cursor()
    cur1 = db.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, username TEXT, point INT)')
    cur.execute('CREATE TABLE IF NOT EXISTS profile()')
    db.commit()

async def create_profile(user_id, username):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute('INSERT INTO profile VALUES(?, ?, ?)', (user_id, username, 0))
        db.commit()
