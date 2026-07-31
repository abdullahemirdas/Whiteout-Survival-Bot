from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.repeat_event import RepeatEventForm

from database import (
    add_event,
    is_admin
)


router = Router()



# =========================
# TEKRARLI ETKİNLİK BAŞLAT
# =========================

@router.message(F.text == "🔁 Tekrarlı Etkinlik")
async def repeat_start(
    message: Message,
    state: FSMContext
):

    if not await is_admin(message.from_user.id):
        return


    await state.clear()


    await message.answer(
        "📌 Tekrarlı etkinlik adı:"
    )


    await state.set_state(
        RepeatEventForm.name
    )



# =========================
# İSİM
# =========================

@router.message(RepeatEventForm.name)
async def repeat_name(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        name=message.text
    )


    await message.answer(
"""
🔁 Tekrar türü seç:

1 - Her gün
2 - 2 günde bir
3 - 3 günde bir
4 - Her hafta
5 - Her ay
"""
    )


    await state.set_state(
        RepeatEventForm.repeat_type
    )



# =========================
# TEKRAR TÜRÜ
# =========================

@router.message(RepeatEventForm.repeat_type)
async def repeat_type(
    message: Message,
    state: FSMContext
):

    repeat_types = {

        "1": "daily",

        "2": "every_2_days",

        "3": "every_3_days",

        "4": "weekly",

        "5": "monthly"

    }


    repeat = repeat_types.get(
        message.text
    )


    if repeat is None:

        await message.answer(
            "❌ 1-5 arasında seçim yapın."
        )

        return



    await state.update_data(
        repeat_type=repeat
    )


    await message.answer(
        "⏰ Saat giriniz:\nÖrnek: 20:00"
    )


    await state.set_state(
        RepeatEventForm.time
    )



# =========================
# KAYDET
# =========================

@router.message(RepeatEventForm.time)
async def repeat_time(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()


    await add_event(

        data["name"],

        "REPEAT",

        message.text,

        data["repeat_type"]

    )


    await message.answer(
        "✅ Tekrarlı etkinlik kaydedildi."
    )


    await state.clear()