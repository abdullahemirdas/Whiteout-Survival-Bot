from aiogram.fsm.state import State, StatesGroup


class BroadcastForm(StatesGroup):

    message = State()