import asyncio
import os

from aiohttp import web

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



async def health_check(request):

    return web.Response(
        text="Whiteout ATA Bot aktif"
    )



async def start_web_server():

    app = web.Application()

    app.router.add_get(
        "/",
        health_check
    )

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    runner = web.AppRunner(app)

    await runner.setup()


    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()


    print(
        f"Web server aktif: {port}"
    )



async def start_bot():

    await init_db()


    bot = Bot(
        token=BOT_TOKEN
    )


    set_bot(bot)


    dp = Dispatcher()


    dp.include_router(start.router)
    dp.include_router(events.router)
    dp.include_router(admin.router)
    dp.include_router(repeat.router)
    dp.include_router(broadcast.router)
    dp.include_router(alliance.router)
    dp.include_router(alliance_admin.router)
    dp.include_router(contact.router)


    start_scheduler()


    print(
        "🤖 Whiteout ATA Bot Başlatıldı"
    )


    await dp.start_polling(
        bot
    )



async def main():

    await start_web_server()

    await start_bot()



if __name__ == "__main__":

    asyncio.run(main())
