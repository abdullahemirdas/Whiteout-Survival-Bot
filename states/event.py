from aiogram.fsm.state import State, StatesGroup


class EventForm(StatesGroup):

    # Etkinlik ekleme
    name = State()

    date = State()

    time = State()

    repeat_type = State()


    # Etkinlik silme
    delete_id = State()


    # Savaş ekleme
    war_name = State()

    war_date = State()

    war_time = State()