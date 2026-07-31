from aiogram.fsm.state import State, StatesGroup


class RepeatEventForm(StatesGroup):

    name = State()

    repeat_type = State()

    time = State()