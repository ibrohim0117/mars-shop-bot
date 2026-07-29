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
    category = State()


class Reklama(StatesGroup):
    turi = State()      # reklama turini tanlash (matn / rasm / video)
    matn = State()      # matn kutilmoqda
    rasm = State()      # rasm kutilmoqda
    video = State()     # video kutilmoqda
    tasdiq = State()    # yuborishni tasdiqlash
