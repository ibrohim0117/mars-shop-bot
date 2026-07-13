import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from commands import dp as command_dp
from users import dp as op_dp
from database import init_db  
BOTTOKEN = TOKEN
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def main():
    init_db()  
    
    bot = Bot(token=BOTTOKEN)
    dp.include_router(command_dp)
    dp.include_router(op_dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())