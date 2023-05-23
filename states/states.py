from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    CONNECTING_API = State()
    RESERVE_DAY = State()
    FREE_CONNECTING_API = State()
    CHANGE_API = State()
    SET_SEARCH = State()
    ANOTHER_PERIOD = State()
    CONNECTING_API_FBS = State()
