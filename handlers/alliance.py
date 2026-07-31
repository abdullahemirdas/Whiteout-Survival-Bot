from aiogram import Router, F
from aiogram.types import Message

from database import get_alliance


router = Router()



@router.message(F.text == "🏰 Alliance Bilgileri")
async def alliance_info(message: Message):

    print("Alliance handler çalıştı")


    alliance = await get_alliance()


    if alliance is None:

        await message.answer(
            "🏰 Alliance bilgileri henüz girilmemiş."
        )

        return



    await message.answer(
f"""
🏰 Alliance Bilgileri


⚔️ Alliance:
{alliance[1]}


👑 Lider:
{alliance[2]}


🌍 Sunucu:
{alliance[3]}


📜 Kurallar:
{alliance[4]}


📢 Açıklama:
{alliance[5]}
"""
    )