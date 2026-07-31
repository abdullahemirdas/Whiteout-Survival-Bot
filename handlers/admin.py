from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import ADMIN_IDS

from keyboards.admin import admin_menu
from keyboards.main import main_menu

from database import (
    add_admin,
    get_admins,
    get_user_count
)

from states.admin import AdminForm


router = Router()



def is_admin(user_id):

    return user_id in ADMIN_IDS



# =========================
# /admin
# =========================

@router.message(Command("admin"))
async def admin_command(
    message: Message,
    state: FSMContext
):

    await state.clear()


    if not is_admin(message.from_user.id):

        await message.answer(
            "⛔ Bu alana giriş yetkiniz yok."
        )

        return


    await message.answer(
        "⚙️ Yönetim Paneli",
        reply_markup=admin_menu()
    )



# =========================
# Yönetim Menü
# =========================

@router.message(F.text == "⚙️ Yönetim")
async def open_management(
    message: Message,
    state: FSMContext
):

    await state.clear()


    if not is_admin(message.from_user.id):
        return


    await message.answer(
        "⚙️ Yönetim Paneli",
        reply_markup=admin_menu()
    )



# =========================
# Ana Menü
# =========================

@router.message(F.text == "⬅️ Ana Menü")
async def back_main(
    message: Message,
    state: FSMContext
):

    await state.clear()


    await message.answer(
        "Ana Menü",
        reply_markup=main_menu(
            is_admin(message.from_user.id)
        )
    )



# =========================
# Adminleri Gör
# =========================

@router.message(F.text == "👑 Adminleri Gör")
async def admin_list(
    message: Message
):

    if not is_admin(message.from_user.id):
        return


    admins = await get_admins()


    if not admins:

        await message.answer(
            "Kayıtlı admin bulunmuyor."
        )

        return


    text = "👑 Admin Listesi\n\n"


    for admin in admins:

        text += (
            f"• {admin[1]} ({admin[0]})\n"
        )


    await message.answer(text)



# =========================
# Admin Ekle
# =========================

@router.message(F.text == "👤 Admin Ekle")
async def admin_add_start(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return


    await state.clear()


    await message.answer(
        "👤 Admin yapılacak Telegram ID giriniz:"
    )


    await state.set_state(
        AdminForm.add_admin
    )



@router.message(AdminForm.add_admin)
async def admin_add_finish(
    message: Message,
    state: FSMContext
):

    try:

        telegram_id = int(message.text)


        await add_admin(
            telegram_id
        )


        if telegram_id not in ADMIN_IDS:

            ADMIN_IDS.append(
                telegram_id
            )


        await message.answer(
            "✅ Yeni admin eklendi."
        )


    except:

        await message.answer(
            "❌ Geçersiz Telegram ID."
        )


    await state.clear()



# =========================
# Admin Sil
# =========================

@router.message(F.text == "👤 Admin Sil")
async def admin_remove(
    message: Message
):

    if not is_admin(message.from_user.id):
        return


    await message.answer(
        "🚧 Admin silme sistemi aktif."
    )



# =========================
# ÜYE YÖNETİMİ
# =========================

@router.message(F.text == "👥 Üye Yönetimi")
async def member_management(
    message: Message
):

    if not is_admin(message.from_user.id):
        return


    count = await get_user_count()


    await message.answer(
        f"""
👥 Üye İstatistikleri


👤 Toplam Üye: {count}
"""
    )