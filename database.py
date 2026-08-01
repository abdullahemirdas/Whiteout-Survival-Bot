import asyncpg

from datetime import datetime

from config import DATABASE_URL

pool = None


async def get_pool():
    global pool

    if pool is None:

        pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=1,
            max_size=5
        )

    return pool



# =========================
# DATABASE OLUŞTURMA
# =========================

async def init_db():

    db = await get_pool()

    async with db.acquire() as conn:

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS users(

            id BIGSERIAL PRIMARY KEY,

            telegram_id BIGINT UNIQUE,

            username TEXT,

            first_name TEXT,

            is_admin BOOLEAN DEFAULT FALSE

        );

        """)

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS events(

            id BIGSERIAL PRIMARY KEY,

            name TEXT,

            event_date TEXT,

            event_time TEXT,

            repeat_type TEXT DEFAULT 'none',

            last_run TEXT,

            reminder_sent TEXT DEFAULT ''

        );

        """)

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS alliance(

            id INTEGER PRIMARY KEY,

            name TEXT,

            leader TEXT,

            server TEXT,

            rules TEXT,

            description TEXT

        );

        """)



# =========================
# KULLANICI EKLE
# =========================

async def add_user(user):

    db = await get_pool()

    async with db.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO users
            (
                telegram_id,
                username,
                first_name
            )
            VALUES ($1,$2,$3)

            ON CONFLICT (telegram_id)
            DO NOTHING
            """,
            user.id,
            user.username,
            user.first_name
        )



# =========================
# TÜM KULLANICILAR
# =========================

# =========================
# TÜM KULLANICILAR
# =========================

async def get_users():

    db = await get_pool()

    async with db.acquire() as conn:

        rows = await conn.fetch("""
            SELECT *
            FROM users
            ORDER BY id
        """)

        return [tuple(row) for row in rows]


# =========================
# ÜYE SAYISI
# =========================

async def get_user_count():

    db = await get_pool()

    async with db.acquire() as conn:

        count = await conn.fetchval("""

            SELECT COUNT(*)

            FROM users

        """)

        return count



# =========================
# ADMIN EKLE
# =========================

async def add_admin(telegram_id):

    db = await get_pool()

    async with db.acquire() as conn:

        await conn.execute(
            """
            UPDATE users

            SET is_admin=TRUE

            WHERE telegram_id=$1
            """,
            telegram_id
        )



# =========================
# ADMINLER
# =========================

async def get_admins():

    db = await get_pool()

    async with db.acquire() as conn:

        rows = await conn.fetch(
            """
            SELECT
                telegram_id,
                first_name

            FROM users

            WHERE is_admin=TRUE
            """
        )

        return [tuple(row) for row in rows]



# =========================
# ADMIN KONTROL
# =========================

async def is_admin(telegram_id):

    db = await get_pool()

    async with db.acquire() as conn:

        result = await conn.fetchval(
            """
            SELECT is_admin

            FROM users

            WHERE telegram_id=$1
            """,
            telegram_id
        )

        return bool(result)



# =========================
# ETKİNLİK EKLE
# =========================

async def add_event(
    name,
    event_date,
    event_time,
    repeat_type="none"
):

    db = await get_pool()

    async with db.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO events
            (
                name,
                event_date,
                event_time,
                repeat_type,
                last_run,
                reminder_sent
            )

            VALUES
            ($1,$2,$3,$4,$5,$6)
            """,
            name,
            event_date,
            event_time,
            repeat_type,
            "",
            ""
        )



# =========================
# ETKİNLİKLERİ GETİR
# =========================

async def get_events():

    db = await get_pool()

    async def get_events():

    db = await get_pool()

    async with db.acquire() as conn:

        rows = await conn.fetch(
            """
            SELECT *
            FROM events
            ORDER BY id DESC
            """
        )

        return [tuple(row) for row in rows]


# =========================
# LAST RUN GÜNCELLE
# =========================

async def update_last_run(event_id):

    db = await get_pool()

    async with db.acquire() as conn:

        await conn.execute(
            """
            UPDATE events

            SET last_run=$1

            WHERE id=$2
            """,
            datetime.now().strftime("%Y-%m-%d"),
            event_id
        )



# =========================
# HATIRLATMA GÜNCELLE
# =========================

async def update_reminder_sent(
    event_id,
    reminder
):

    db = await get_pool()

    async with db.acquire() as conn:

        await conn.execute(
            """
            UPDATE events

            SET reminder_sent=$1

            WHERE id=$2
            """,
            str(reminder),
            event_id
        )



# =========================
# HATIRLATMA SIFIRLA
# =========================

async def reset_reminder_sent(
    event_id
):

    db = await get_pool()

    async with db.acquire() as conn:

        await conn.execute(
            """
            UPDATE events

            SET reminder_sent=''

            WHERE id=$1
            """,
            event_id
        )



# =========================
# ETKİNLİK SİL
# =========================

async def delete_event(event_id):

    db = await get_pool()

    async with db.acquire() as conn:

        await conn.execute(
            """
            DELETE FROM events

            WHERE id=$1
            """,
            event_id
        )



# =========================
# ALLIANCE BİLGİLERİ
# =========================

async def get_alliance():

    db = await get_pool()

    async with db.acquire() as conn:

        row = await conn.fetchrow(
            """
            SELECT *
            FROM alliance
            WHERE id=1
            """
        )

        if row:

            return tuple(row)

        return None



async def update_alliance(
    name,
    leader,
    server,
    rules,
    description
):

    db = await get_pool()

    async with db.acquire() as conn:

        await conn.execute(
            """
            DELETE FROM alliance
            """
        )

        await conn.execute(
            """
            INSERT INTO alliance
            (
                id,
                name,
                leader,
                server,
                rules,
                description
            )

            VALUES
            (1,$1,$2,$3,$4,$5)
            """,
            name,
            leader,
            server,
            rules,
            description
        )



