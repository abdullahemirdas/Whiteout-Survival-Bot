from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import datetime, timedelta

from database import (
    get_events,
    get_users,
    update_last_run,
    update_reminder_sent,
    reset_reminder_sent
)


scheduler = AsyncIOScheduler()

bot_instance = None



# =========================
# BOT BAĞLAMA
# =========================

def set_bot(bot):

    global bot_instance

    bot_instance = bot



# =========================
# TEKRAR KONTROL
# =========================

def can_run_repeat(
    repeat_type,
    last_run,
    now
):

    if not last_run:

        return True


    try:

        last = datetime.strptime(
            last_run,
            "%Y-%m-%d"
        )

    except:

        return True



    diff = (
        now.date()
        -
        last.date()
    ).days



    if repeat_type == "daily":

        return diff >= 1


    if repeat_type == "every_2_days":

        return diff >= 2


    if repeat_type == "every_3_days":

        return diff >= 3


    if repeat_type == "weekly":

        return diff >= 7


    if repeat_type == "monthly":

        return diff >= 30


    return False



# =========================
# EVENT KONTROL
# =========================

async def check_events():


    if bot_instance is None:

        print("Bot bağlantısı yok")

        return



    events = await get_events()
    print("Toplam etkinlik:", len(events), flush=True)
    print("Kontrol edilen etkinlik:", event, flush=True)
    


    now = datetime.now()



    print(
        "Scheduler kontrol:",
        now.strftime("%H:%M:%S")
    )



    for event in events:


        try:


            event_id = event[0]

            name = event[1]

            event_date = event[2]

            event_time = event[3]

            repeat_type = event[4]

            last_run = event[5] or ""

            reminder_sent = event[6] if len(event) > 6 else ""



            if not event_time:

                continue



            if ":" not in event_time:

                continue



            hour, minute = event_time.split(":")



            event_datetime = datetime.strptime(
    f"{event_date} {event_time}",
    "%d.%m.%Y %H:%M"
)



            diff = event_datetime - now



            reminder = None



            # 30 dakika

            if timedelta(minutes=29) <= diff <= timedelta(minutes=31):

                reminder = "30"



            # 10 dakika

            elif timedelta(minutes=9) <= diff <= timedelta(minutes=11):

                reminder = "10"



            # 5 dakika

            elif timedelta(minutes=4) <= diff <= timedelta(minutes=6):

                reminder = "5"



            if reminder is None:

                continue



            print(
                "Bildirim kontrol:",
                name,
                reminder
            )



            if reminder_sent == reminder:

                continue



            # Tekrarlı etkinlik kontrolü

            if event_date == "REPEAT":


                if not can_run_repeat(

                    repeat_type,

                    last_run,

                    now

                ):

                    continue



            await send_notification(

                name,

                event_time,

                reminder

            )



            await update_reminder_sent(

                event_id,

                reminder

            )



            print(
                "Bildirim gönderildi:",
                name,
                reminder
            )



            # 5 dakika sonrası yeni döngü

            if reminder == "5":


                await update_last_run(

                    event_id

                )


                await reset_reminder_sent(

                    event_id

                )



        except Exception as e:


            print(
                "Scheduler hata:",
                e
            )



# =========================
# MESAJ GÖNDER
# =========================

async def send_notification(
    name,
    time,
    reminder
):


    users = await get_users()



    for user in users:


        telegram_id = user[1]


        try:


            await bot_instance.send_message(

                telegram_id,

                f"""
🔔 ETKİNLİK HATIRLATMA


⚔️ {name}


⏰ Saat: {time}


⏳ {reminder} dakika sonra başlayacak.
"""

            )


        except Exception as e:


            print(
                "Mesaj gönderilemedi:",
                telegram_id,
                e
            )



# =========================
# SCHEDULER BAŞLAT
# =========================

def start_scheduler():


    scheduler.add_job(

        check_events,

        "interval",

        minutes=1,

        id="event_checker",

        replace_existing=True

    )


    scheduler.start()
