from aiogram.fsm.state import State, StatesGroup


class ContactForm(StatesGroup):

    message = State()