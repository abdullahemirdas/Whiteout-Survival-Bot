from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

event_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⚔️ Foundry Battle")],
        [KeyboardButton(text="🏰 Sunfire Castle")],
        [KeyboardButton(text="❄️ Frostfire Mine")],
        [KeyboardButton(text="🧟 Crazy Joe")],
        [KeyboardButton(text="⚔️ Brothers in Arms")],
        [KeyboardButton(text="📆 Alliance Mobilization")],
        [KeyboardButton(text="⬅️ Ana Menü")]
    ],
    resize_keyboard=True
)