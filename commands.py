from aiogram import Router, types, F
from aiogram.filters import Command

from config import ADMINS
from keyboards import admin_main_menu, user_main_menu
from database import add_user, count_users 

dp = Router()

@dp.message(Command('start'))
async def start(message: types.Message):
    try:
        add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    except Exception:
        # Foydalanuvchi allaqachon bazada mavjud (takroriy INSERT) — e'tiborsiz qoldiriladi
        pass
    if str(message.from_user.id) == str(ADMINS):
        await message.answer(f"Salom {message.from_user.full_name} xush kelibsiz Admin!", reply_markup=admin_main_menu)
    else:
        await message.answer(f"Salom {message.from_user.full_name} xush kelibsiz", reply_markup=user_main_menu)


@dp.message(F.text == "👨‍💼Foydalanuvchilar soni")
async def show_users_count(message: types.Message):
    if str(message.from_user.id) == str(ADMINS):
        jami = count_users()
        await message.answer(f"Botingizdagi jami foydalanuvchilar soni: {jami} ta")


@dp.message(Command('help'))
async def help(message: types.Message):
    await message.answer(f"{message.from_user.full_name} shunchaki /start ni bosing!")

@dp.message(Command('get_my_id'))
async def get_my_id(message: types.Message):
    text = f"""
🥸Ism sharif - {message.from_user.full_name}
🏠Username - @{message.from_user.username}
🆔User ID - {message.from_user.id}
"""
    await message.answer(text)


@dp.message(Command('admin_button'))
async def admin_button_handler(message: types.Message):
    if str(message.from_user.id) == str(ADMINS):
        await message.answer("Admin button menu", reply_markup=admin_main_menu)
    else:
        await message.answer("Sizda bunga huquq yo'q!🤌🏻")