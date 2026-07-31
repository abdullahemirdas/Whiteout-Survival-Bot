import aiosqlite

from datetime import datetime


DATABASE = "bot_database.db"



# =========================
# DATABASE OLUŞTURMA
# =========================

async def init_db():

    async with aiosqlite.connect(DATABASE) as db:


        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            telegram_id INTEGER UNIQUE,

            username TEXT,

            first_name TEXT,

            is_admin INTEGER DEFAULT 0
        )
        """)



        await db.execute("""
        CREATE TABLE IF NOT EXISTS events (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            event_date TEXT,

            event_time TEXT,

            repeat_type TEXT DEFAULT 'none',

            last_run TEXT,

            reminder_sent TEXT DEFAULT ''
        )
        """)



        await db.execute("""
        CREATE TABLE IF NOT EXISTS alliance (

            id INTEGER PRIMARY KEY,

            name TEXT,

            leader TEXT,

            server TEXT,

            rules TEXT,

            description TEXT
        )
        """)


        await db.commit()



# =========================
# KULLANICI EKLE
# =========================

async def add_user(user):

    async with aiosqlite.connect(DATABASE) as db:


        await db.execute("""
        INSERT OR IGNORE INTO users
        (
            telegram_id,
            username,
            first_name
        )

        VALUES (?,?,?)
        """,

        (
            user.id,
            user.username,
            user.first_name
        ))


        await db.commit()



# =========================
# TÜM KULLANICULAR
# =========================

async def get_users():

    async with aiosqlite.connect(DATABASE) as db:


        cursor = await db.execute("""
        SELECT *
        FROM users
        """)


        return await cursor.fetchall()



# =========================
# ÜYE SAYISI
# =========================

async def get_user_count():

    async with aiosqlite.connect(DATABASE) as db:


        cursor = await db.execute("""
        SELECT COUNT(*)
        FROM users
        """)


        result = await cursor.fetchone()


        return result[0]



# =========================
# ADMIN EKLE
# =========================

async def add_admin(telegram_id):

    async with aiosqlite.connect(DATABASE) as db:


        await db.execute("""
        UPDATE users

        SET is_admin=1

        WHERE telegram_id=?
        """,

        (
            telegram_id,
        ))


        await db.commit()



# =========================
# ADMINLER
# =========================

async def get_admins():

    async with aiosqlite.connect(DATABASE) as db:


        cursor = await db.execute("""
        SELECT telegram_id, first_name

        FROM users

        WHERE is_admin=1
        """)


        return await cursor.fetchall()



# =========================
# ADMIN KONTROL
# =========================

async def is_admin(telegram_id):

    async with aiosqlite.connect(DATABASE) as db:


        cursor = await db.execute("""
        SELECT is_admin

        FROM users

        WHERE telegram_id=?
        """,

        (
            telegram_id,
        ))


        result = await cursor.fetchone()


        if result:

            return result[0] == 1


        return False



# =========================
# ETKİNLİK EKLE
# =========================

async def add_event(
    name,
    event_date,
    event_time,
    repeat_type="none"
):

    async with aiosqlite.connect(DATABASE) as db:


        await db.execute("""
        INSERT INTO events
        (
            name,
            event_date,
            event_time,
            repeat_type,
            last_run,
            reminder_sent
        )

        VALUES (?,?,?,?,?,?)
        """,

        (
            name,
            event_date,
            event_time,
            repeat_type,
            "",
            ""
        ))


        await db.commit()



# =========================
# ETKİNLİKLERİ GETİR
# =========================

async def get_events():

    async with aiosqlite.connect(DATABASE) as db:


        cursor = await db.execute("""
        SELECT *

        FROM events

        ORDER BY id DESC
        """)


        return await cursor.fetchall()



# =========================
# LAST RUN GÜNCELLE
# =========================

async def update_last_run(event_id):

    async with aiosqlite.connect(DATABASE) as db:


        await db.execute("""
        UPDATE events

        SET last_run=?

        WHERE id=?
        """,

        (
            datetime.now().strftime("%Y-%m-%d"),

            event_id
        ))


        await db.commit()



# =========================
# HATIRLATMA GÜNCELLE
# =========================

async def update_reminder_sent(
    event_id,
    reminder
):

    async with aiosqlite.connect(DATABASE) as db:


        await db.execute("""
        UPDATE events

        SET reminder_sent=?

        WHERE id=?
        """,

        (
            str(reminder),

            event_id
        ))


        await db.commit()



# =========================
# HATIRLATMA SIFIRLA
# =========================

async def reset_reminder_sent(
    event_id
):

    async with aiosqlite.connect(DATABASE) as db:


        await db.execute("""
        UPDATE events

        SET reminder_sent=''

        WHERE id=?
        """,

        (
            event_id,
        ))


        await db.commit()



# =========================
# ETKİNLİK SİL
# =========================

async def delete_event(event_id):

    async with aiosqlite.connect(DATABASE) as db:


        await db.execute("""
        DELETE FROM events

        WHERE id=?
        """,

        (
            event_id,
        ))


        await db.commit()



# =========================
# ALLIANCE BİLGİLERİ
# =========================

async def get_alliance():

    async with aiosqlite.connect(DATABASE) as db:


        cursor = await db.execute("""
        SELECT *

        FROM alliance

        WHERE id=1
        """)


        return await cursor.fetchone()



async def update_alliance(
    name,
    leader,
    server,
    rules,
    description
):

    async with aiosqlite.connect(DATABASE) as db:


        await db.execute("""
        DELETE FROM alliance
        """)


        await db.execute("""
        INSERT INTO alliance
        (
            id,
            name,
            leader,
            server,
            rules,
            description
        )

        VALUES (1,?,?,?,?,?)
        """,

        (
            name,
            leader,
            server,
            rules,
            description
        ))


        await db.commit()