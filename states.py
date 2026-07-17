from aiogram.fsm.state import State, StatesGroup

class ChangeUserStatus(StatesGroup):
    user_id = State()
    new_status = State()

class ElonJoylash(StatesGroup):
    name = State()
    category = State()
    price = State()
    status = State()
    image = State()
    phone = State()
    yes_or_no = State()

class SotibOlish(StatesGroup):
    name = State()
    category = State()
    price = State()
    status = State()
    image = State()
    phone = State()
    