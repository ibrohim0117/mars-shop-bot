import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from commands import dp as command_router
from users import dp as user_router
from admin import admin_router
from database import init_db

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def main():
    init_db()  
    
    bot = Bot(token=TOKEN)
    dp.include_router(command_router)
    dp.include_router(user_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())