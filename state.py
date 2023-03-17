from aiogram.dispatcher.filters.state import State, StatesGroup


class StateGroup(StatesGroup):
    wait_for_answer = State()  # создаёте состояние
    wait_for_themes = State()
    wait_for_choice = State()
