import time

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from config import is_admin
from database import get_user_status

_CACHE_TTL = 60  # sekund — shu muddat davomida DB'ga qayta murojaat qilinmaydi
_status_cache = {}  # {user_id: (banned: bool, expires_at: float)}


def invalidate_ban_cache(user_id):
    """Ban/unban qilinganda keshni tozalaydi — o'zgarish darhol kuchga kiradi."""
    _status_cache.pop(int(user_id), None)


def _is_banned(user_id):
    now = time.time()
    cached = _status_cache.get(user_id)
    if cached and cached[1] > now:
        return cached[0]

    status = get_user_status(user_id)
    banned = status is not None and status[1] == 0
    _status_cache[user_id] = (banned, now + _CACHE_TTL)
    return banned


class BanMiddleware(BaseMiddleware):
    """Ban qilingan foydalanuvchilarni barcha handlerlardan oldin bloklaydi."""

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")

        # Foydalanuvchi aniqlanmasa yoki admin bo'lsa — o'tkazib yuboriladi
        if user is None or is_admin(user.id):
            return await handler(event, data)

        if _is_banned(user.id):
            text = "🚫 Siz admin tomonidan ban qilingansiz!"
            if isinstance(event, CallbackQuery):
                await event.answer(text, show_alert=True)
            elif isinstance(event, Message):
                await event.answer(text)
            return

        return await handler(event, data)
