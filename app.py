import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from database import init_db

from handlers import (
    start,
    events,
    admin,
    repeat,
    broadcast,
    alliance,
    alliance_admin,
    contact
)

from scheduler import (
    start_scheduler,
    set_bot
)



async def main():


    # =========================
    # DATABASE
    # =========================

    await init_db()



    # =========================
    # BOT
    # =========================

    bot = Bot(
        token=BOT_TOKEN
    )



    # =========================
    # SCHEDULER
    # =========================

    set_bot(bot)



    # =========================
    # DISPATCHER
    # =========================

    dp = Dispatcher()



    # =========================
    # ROUTERLAR
    # =========================

    dp.include_router(
        start.router
    )

    dp.include_router(
        events.router
    )

    dp.include_router(
        admin.router
    )

    dp.include_router(
        repeat.router
    )

    dp.include_router(
        broadcast.router
    )

    dp.include_router(
        alliance.router
    )

    dp.include_router(
        alliance_admin.router
    )

    dp.include_router(
        contact.router
    )



    # =========================
    # SCHEDULER
    # =========================

    start_scheduler()



    print(
        "🤖 Whiteout ATA Bot Başlatıldı"
    )



    await dp.start_polling(
        bot
    )



if __name__ == "__main__":

    asyncio.run(main())