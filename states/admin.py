from aiogram.fsm.state import State, StatesGroup


class AdminForm(StatesGroup):

    add_admin = State()

    remove_admin = State()