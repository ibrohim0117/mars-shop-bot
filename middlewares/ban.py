from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from config import is_admin
from database import get_user_status


class BanMiddleware(BaseMiddleware):
    """Ban qilingan foydalanuvchilarni barcha handlerlardan oldin bloklaydi."""

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")

        # Foydalanuvchi aniqlanmasa yoki admin bo'lsa — o'tkazib yuboriladi
        if user is None or is_admin(user.id):
            return await handler(event, data)

        status = get_user_status(user.id)

        # status None bo'lsa — yangi foydalanuvchi (hali bazada yo'q), ruxsat beriladi.
        # is_active == 0 bo'lsa — ban qilingan, bloklanadi.
        if status is not None and status[1] == 0:
            text = "🚫 Siz admin tomonidan ban qilingansiz!"
            if isinstance(event, CallbackQuery):
                await event.answer(text, show_alert=True)
            elif isinstance(event, Message):
                await event.answer(text)
            return

        return await handler(event, data)
