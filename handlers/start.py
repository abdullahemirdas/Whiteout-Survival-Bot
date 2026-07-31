from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import ADMIN_IDS
from database import add_user
from keyboards.main import main_menu


router = Router()



@router.message(CommandStart())
async def start_command(message: Message):


    await add_user(
        message.from_user
    )


    is_admin = (
        message.from_user.id in ADMIN_IDS
    )


    await message.answer(
        "🤖 Whiteout Survival Alliance Bot\n\n"
        "Hoş geldin.",
        reply_markup=main_menu(is_admin)
    )