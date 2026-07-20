from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirmation_button(ad_id):
    """E'lonni tasdiqlash / rad etish tugmalari (admin uchun)."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"review_accept:{ad_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"review_reject:{ad_id}")
        ]
    ])


def changeuserstatusbutton(status):
    """Foydalanuvchi holatiga qarab ban yoki unban tugmasini qaytaradi."""
    if status == 1:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌Ban qilish", callback_data='ban❌')]
        ])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅Bandan chiqarish", callback_data='unban✅')]
    ])
