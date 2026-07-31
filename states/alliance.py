from aiogram.fsm.state import State, StatesGroup


class AllianceForm(StatesGroup):

    name = State()

    leader = State()

    server = State()

    rules = State()

    description = State()