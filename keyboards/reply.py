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


BACK_TEXT = "⬅️Ortga qaytish"

# Sotib olish bo'limi uchun: kategoriyalar + "Ortga qaytish" tugmasi.
# CATEGORIES ro'yxati oddiy category_menu dan olinadi, shuning uchun
# "Ortga qaytish" kategoriya sifatida hisoblanmaydi.
category_menu_back = ReplyKeyboardMarkup(
    keyboard=category_menu.keyboard + [[KeyboardButton(text=BACK_TEXT)]],
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
