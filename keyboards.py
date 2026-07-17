from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def confirmation_button(ad_id):
    return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"review_accept:{ad_id}"),
                InlineKeyboardButton(text="❌ Rad etish", callback_data=f"review_reject:{ad_id}")
            ]
        ])


def changeuserstatusbutton(status):
    if status == 1:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌Ban qilish", callback_data='ban❌')]])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅Bandan chiqarish", callback_data='unban✅')]])


admin_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👨🏻‍💻Kategory yaratish")
        ],
        [
            KeyboardButton(text="👨‍💼Foydalanuvchilar soni"),
            KeyboardButton(text="🔥Reklama xizmati")
        ],
        [
            KeyboardButton(text="🔃Foydalanuvchini holatini o'zgartirish"),
        ],
        [
            KeyboardButton(text="🥸Foydalanuvchi buttonlari ochish")
        ]
    ],
    resize_keyboard=True
)

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕E'lon joylash"),
            KeyboardButton(text="🎁Sotib olish")
        ],
        [
            KeyboardButton(text="📝Mening tarixim"),
            KeyboardButton(text="📞Biz bilan bog'lanish")
        ]
    ],
    resize_keyboard=True
)

category_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Mars pen"),
            KeyboardButton(text="Keyboard sticker"),
            KeyboardButton(text="Strobar")
        ],
        [
            KeyboardButton(text="Notepad"),
            KeyboardButton(text="Mars rug")
        ],
        [
            KeyboardButton(text="Keychain"),
            KeyboardButton(text="Phone Stand"),
            KeyboardButton(text="Mug")
        ],
        [
            KeyboardButton(text="Mouse"),
            KeyboardButton(text="Keyboard")
        ],
    ],
    resize_keyboard=True
)


status_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✨Yangi"),
            KeyboardButton(text="⚖️O'rtacha"),
            KeyboardButton(text="📦Eski")
        ]
    ],
    resize_keyboard=True
)


Ha_Yoq_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ha"),
            KeyboardButton(text="Yo'q")
        ]
    ],
    resize_keyboard=True
)


# Menyulardagi tugmalar ro'yxati — kelgan xabarni tekshirish uchun.
# Menyularning o'zidan hosil qilinadi, shuning uchun doim mos bo'ladi.
CATEGORIES = [button.text for row in category_menu.keyboard for button in row]
STATUSES = [button.text for row in status_menu.keyboard for button in row]