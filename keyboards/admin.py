from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_menu():

    keyboard = [

        [
            KeyboardButton(text="➕ Etkinlik Ekle"),
            KeyboardButton(text="📋 Etkinlikleri Gör")
        ],

        [
            KeyboardButton(text="🗑 Etkinlik Sil"),
            KeyboardButton(text="🔁 Tekrarlı Etkinlik")
        ],

        [
            KeyboardButton(text="⚔️ Savaş Ekle"),
            KeyboardButton(text="📢 Duyuru Gönder")
        ],

        [
            KeyboardButton(text="👑 Adminleri Gör"),
            KeyboardButton(text="👤 Admin Ekle")
        ],

        [
            KeyboardButton(text="👤 Admin Sil"),
            KeyboardButton(text="👥 Üye Yönetimi")
        ],

        [
            KeyboardButton(text="🏰 Alliance Düzenle")
        ],

        [
            KeyboardButton(text="⬅️ Ana Menü")
        ]

    ]


    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )