from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.event import EventForm

from database import (
    add_event,
    get_events,
    delete_event,
    is_admin
)


router = Router()



# ==================================
# NORMAL ÜYE ETKİNLİKLERİ GÖR
# ==================================

@router.message(F.text == "📅 Etkinlikler")
async def user_events(
    message: Message
):

    events = await get_events()


    if not events:

        await message.answer(
            "📭 Henüz etkinlik bulunmuyor."
        )

        return


    text = "📅 Yaklaşan Etkinlikler\n\n"


    for event in events:

        text += (
            f"⚔️ {event[1]}\n"
            f"📅 Tarih: {event[2]}\n"
            f"⏰ Saat: {event[3]}\n"
            f"🔁 {event[4]}\n"
            "──────────\n"
        )


    await message.answer(text)



# ==================================
# ETKİNLİK EKLE
# ==================================

@router.message(F.text == "➕ Etkinlik Ekle")
async def start_event_add(
    message: Message,
    state: FSMContext
):

    if not await is_admin(message.from_user.id):
        return


    await state.clear()


    await message.answer(
        "📌 Etkinlik adı nedir?"
    )


    await state.set_state(
        EventForm.name
    )



@router.message(EventForm.name)
async def get_event_name(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        name=message.text
    )


    await message.answer(
        "📅 Tarih giriniz:\nÖrnek: 05.08.2026"
    )


    await state.set_state(
        EventForm.date
    )



@router.message(EventForm.date)
async def get_event_date(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        date=message.text
    )


    await message.answer(
        "⏰ Saat giriniz:\nÖrnek: 20:00"
    )


    await state.set_state(
        EventForm.time
    )



@router.message(EventForm.time)
async def get_event_time(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        time=message.text
    )


    await message.answer(
        """
🔁 Tekrar türü seç:

1 - Tek sefer
2 - Günlük
3 - Haftalık
"""
    )


    await state.set_state(
        EventForm.repeat_type
    )



@router.message(EventForm.repeat_type)
async def save_event(
    message: Message,
    state: FSMContext
):

    repeat_types = {

        "1": "none",
        "2": "daily",
        "3": "weekly"

    }


    repeat = repeat_types.get(
        message.text
    )


    if not repeat:

        await message.answer(
            "❌ 1, 2 veya 3 giriniz."
        )

        return


    data = await state.get_data()


    await add_event(
        data["name"],
        data["date"],
        data["time"],
        repeat
    )


    await message.answer(
        "✅ Etkinlik eklendi."
    )


    await state.clear()



# ==================================
# ADMİN ETKİNLİKLERİ GÖR
# ==================================

@router.message(F.text == "📋 Etkinlikleri Gör")
async def admin_events(
    message: Message
):

    if not await is_admin(message.from_user.id):
        return


    events = await get_events()


    if not events:

        await message.answer(
            "📭 Kayıtlı etkinlik yok."
        )

        return


    text = "⚙️ Etkinlik Listesi\n\n"


    for event in events:

        text += (
            f"🆔 ID: {event[0]}\n"
            f"⚔️ {event[1]}\n"
            f"📅 {event[2]}\n"
            f"⏰ {event[3]}\n"
            f"🔁 {event[4]}\n"
            "──────────\n"
        )


    await message.answer(text)



# ==================================
# ETKİNLİK SİL
# ==================================

@router.message(F.text == "🗑 Etkinlik Sil")
async def delete_start(
    message: Message,
    state: FSMContext
):

    if not await is_admin(message.from_user.id):
        return


    await state.clear()


    await message.answer(
        "🗑 Silinecek etkinlik ID:"
    )


    await state.set_state(
        EventForm.delete_id
    )



@router.message(EventForm.delete_id)
async def delete_confirm(
    message: Message,
    state: FSMContext
):

    if not await is_admin(message.from_user.id):
        return


    try:

        event_id = int(message.text)


        await delete_event(
            event_id
        )


        await message.answer(
            "✅ Etkinlik silindi."
        )


    except:

        await message.answer(
            "❌ Geçersiz ID."
        )


    await state.clear()



# ==================================
# ⚔️ SAVAŞ EKLE
# ==================================

@router.message(F.text == "⚔️ Savaş Ekle")
async def war_start(
    message: Message,
    state: FSMContext
):

    if not await is_admin(message.from_user.id):
        return


    await state.clear()


    await message.answer(
        "⚔️ Savaş adı:"
    )


    await state.set_state(
        EventForm.war_name
    )



@router.message(EventForm.war_name)
async def war_name(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        name=message.text
    )


    await message.answer(
        "📅 Savaş tarihi:"
    )


    await state.set_state(
        EventForm.war_date
    )



@router.message(EventForm.war_date)
async def war_date(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        date=message.text
    )


    await message.answer(
        "⏰ Savaş saati:"
    )


    await state.set_state(
        EventForm.war_time
    )



@router.message(EventForm.war_time)
async def war_save(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()


    await add_event(
        "⚔️ " + data["name"],
        data["date"],
        message.text,
        "war"
    )


    await message.answer(
        "✅ Savaş takvime eklendi."
    )


    await state.clear()