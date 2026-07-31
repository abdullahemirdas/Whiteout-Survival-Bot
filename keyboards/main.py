from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu(is_admin=False):

    keyboard = [

        [
            KeyboardButton(text="📅 Etkinlikler"),
            KeyboardButton(text="🏰 Alliance Bilgileri")
        ],

        [
            KeyboardButton(text="📩 Admin'e Mesaj"),
            KeyboardButton(text="⚔️ Savaş Takvimi")
        ]

    ]


    if is_admin:

        keyboard.append(
            [
                KeyboardButton(text="⚙️ Yönetim")
            ]
        )


    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )