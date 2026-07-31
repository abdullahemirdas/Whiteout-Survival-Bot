from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.alliance import AllianceForm

from database import update_alliance

from config import ADMIN_IDS


router = Router()



def is_admin(user_id):

    return user_id in ADMIN_IDS



# =========================
# ALLIANCE DÜZENLE BAŞLAT
# =========================

@router.message(F.text == "🏰 Alliance Düzenle")
async def alliance_start(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):

        await message.answer(
            "⛔ Yetkiniz yok."
        )

        return


    await state.clear()


    await message.answer(
        "🏰 Alliance adı:"
    )


    await state.set_state(
        AllianceForm.name
    )



# =========================
# ALLIANCE ADI
# =========================

@router.message(AllianceForm.name)
async def alliance_name(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        name=message.text
    )


    await message.answer(
        "👑 Lider adı:"
    )


    await state.set_state(
        AllianceForm.leader
    )



# =========================
# LİDER
# =========================

@router.message(AllianceForm.leader)
async def alliance_leader(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        leader=message.text
    )


    await message.answer(
        "🌍 Sunucu bilgisi:"
    )


    await state.set_state(
        AllianceForm.server
    )



# =========================
# SUNUCU
# =========================

@router.message(AllianceForm.server)
async def alliance_server(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        server=message.text
    )


    await message.answer(
        "📜 Kurallar:"
    )


    await state.set_state(
        AllianceForm.rules
    )



# =========================
# KURALLAR
# =========================

@router.message(AllianceForm.rules)
async def alliance_rules(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        rules=message.text
    )


    await message.answer(
        "📢 Açıklama:"
    )


    await state.set_state(
        AllianceForm.description
    )



# =========================
# KAYDET
# =========================

@router.message(AllianceForm.description)
async def alliance_save(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()


    await update_alliance(

        data["name"],

        data["leader"],

        data["server"],

        data["rules"],

        message.text

    )


    await message.answer(
        "✅ Alliance bilgileri güncellendi."
    )


    await state.clear()