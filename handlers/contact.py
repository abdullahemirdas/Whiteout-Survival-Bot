from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.contact import ContactForm

from database import get_admins


router = Router()



# =========================
# ADMIN MESAJ BAŞLAT
# =========================

@router.message(F.text == "📩 Admin'e Mesaj")
async def contact_start(
    message: Message,
    state: FSMContext
):

    await state.clear()


    await message.answer(
        "📩 Adminlere göndermek istediğiniz mesajı yazınız:"
    )


    await state.set_state(
        ContactForm.message
    )



# =========================
# MESAJ GÖNDER
# =========================

@router.message(ContactForm.message)
async def send_to_admins(
    message: Message,
    state: FSMContext
):

    admins = await get_admins()


    if not admins:

        await message.answer(
            "❌ Sistemde kayıtlı admin bulunamadı."
        )

        await state.clear()

        return



    text = f"""
📩 Yeni Üye Mesajı


👤 Gönderen:
{message.from_user.first_name}


🆔 Telegram ID:
{message.from_user.id}


💬 Mesaj:

{message.text}
"""



    success = 0



    for admin in admins:


        admin_id = admin[0]


        try:

            await message.bot.send_message(
                admin_id,
                text
            )

            success += 1


        except Exception as e:

            print(
                "Admin mesaj hatası:",
                admin_id,
                e
            )



    await message.answer(
        f"✅ Mesajınız adminlere gönderildi.\n\n"
        f"📩 Ulaşan admin: {success}"
    )


    await state.clear()