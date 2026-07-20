from aiogram import Router, types, F
from aiogram.filters import Command

from config import is_admin
from keyboards import admin_main_menu, user_main_menu
from database import add_user, count_users

command_router = Router()


@command_router.message(Command('start'))
async def start_handler(message: types.Message):
    try:
        add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    except Exception:
        # Foydalanuvchi allaqachon bazada mavjud (takroriy INSERT) — e'tiborsiz qoldiriladi
        pass

    if is_admin(message.from_user.id):
        await message.answer(f"Salom {message.from_user.full_name} xush kelibsiz Admin!", reply_markup=admin_main_menu)
    else:
        await message.answer(f"Salom {message.from_user.full_name} xush kelibsiz", reply_markup=user_main_menu)


@command_router.message(Command('help'))
async def help_handler(message: types.Message):
    await message.answer(f"{message.from_user.full_name} shunchaki /start ni bosing!")


@command_router.message(Command('get_my_id'))
async def get_my_id_handler(message: types.Message):
    text = f"""
🥸Ism sharif - {message.from_user.full_name}
🏠Username - @{message.from_user.username}
🆔User ID - {message.from_user.id}
"""
    await message.answer(text)


@command_router.message(Command('admin_button'))
async def admin_menu_handler(message: types.Message):
    if is_admin(message.from_user.id):
        await message.answer("Admin button menu", reply_markup=admin_main_menu)
    else:
        await message.answer("Sizda bunga huquq yo'q!🤌🏻")


@command_router.message(F.text == "👨‍💼Foydalanuvchilar soni")
async def users_count_handler(message: types.Message):
    if is_admin(message.from_user.id):
        jami = count_users()
        await message.answer(f"Botingizdagi jami foydalanuvchilar soni: {jami} ta")
