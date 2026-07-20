import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from handlers import command_router, user_router, admin_router
from middlewares import BanMiddleware
from database import init_db

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    init_db()

    bot = Bot(token=TOKEN)

    # Ban qilingan foydalanuvchilarni barcha xabar va tugmalarda bloklash
    dp.message.middleware(BanMiddleware())
    dp.callback_query.middleware(BanMiddleware())

    dp.include_router(command_router)
    dp.include_router(user_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
