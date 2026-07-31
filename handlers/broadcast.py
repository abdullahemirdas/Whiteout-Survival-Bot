from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.broadcast import BroadcastForm
from database import get_users, is_admin


router = Router()



# =========================
# DUYURU BAŞLAT
# =========================

@router.message(F.text == "📢 Duyuru Gönder")
async def broadcast_start(
    message: Message,
    state: FSMContext
):

    if not await is_admin(message.from_user.id):
        await message.answer(
            "⛔ Bu işlem için yetkiniz yok."
        )
        return


    await state.clear()


    await message.answer(
        "📢 Göndermek istediğiniz duyuruyu yazınız."
    )


    await state.set_state(
        BroadcastForm.message
    )



# =========================
# DUYURU GÖNDER
# =========================

@router.message(BroadcastForm.message)
async def send_broadcast(
    message: Message,
    state: FSMContext
):

    if not await is_admin(message.from_user.id):
        await state.clear()
        return


    users = await get_users()


    success = 0
    failed = 0


    text = f"""
📢 WHITEOUT SURVIVAL ATA

{message.text}
"""


    await message.answer(
        "⏳ Duyuru gönderiliyor..."
    )


    for user in users:

        telegram_id = user[1]


        try:

            await message.bot.send_message(
                telegram_id,
                text
            )

            success += 1


        except Exception:

            failed += 1



    await message.answer(
        f"""
✅ Duyuru tamamlandı.

📨 Başarılı: {success}

❌ Başarısız: {failed}
"""
    )


    await state.clear()