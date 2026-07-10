from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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
            KeyboardButton(text="❌Foydalanuvchini ban qilish"),
            KeyboardButton(text="✅Foydalanuvchini bandan chiqarish")
        ],
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
            KeyboardButton(text="Ha", callback_data="ha"),
            KeyboardButton(text="Yoq", callback_data="yoq")
        ]
    ],
    resize_keyboard=True
    )


# Menyulardagi tugmalar ro'yxati — kelgan xabarni tekshirish uchun.
# Menyularning o'zidan hosil qilinadi, shuning uchun doim mos bo'ladi.
CATEGORIES = [button.text for row in category_menu.keyboard for button in row]
STATUSES = [button.text for row in status_menu.keyboard for button in row]