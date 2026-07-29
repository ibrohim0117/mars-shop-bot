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
            KeyboardButton(text="⏳ Kutilayotgan e'lonlar")
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

# Barcha kategoriyalar (hozircha shu yerda; keyinchalik bazadan olinadi).
CATEGORY_NAMES = [
    "Keyboard Sticker (Klaviatura stikeri)",
    "Mars Pen (Mars ruchkasi)",
    "Strobar (Strobar batonchigi)",
    "Notepad (Bloknot / Daftar)",
    "Mars Rug (Sichqoncha gilamchasi)",
    "Keychain (Brelok / Kalit zanjiri)",
    "Phone Stand (Telefon tagligi)",
    "Mug (Krujka / Finjon)",
    "Sun Glass (Quyoshdan saqlovchi ko'zoynak)",
    "Branded Cap (Brendli kepka)",
    "USB Flash Drive (Fleshka / USB xotira)",
    "Wireless Mouse (Simsiz sichqoncha)",
    "Branded Thermos (Brendli termos)",
    "Mouse (Sichqoncha)",
    "Keyboard (Klaviatura)",
    "MARS Futbolka (Mars futbolkasi)",
    "Keyboard&Mouse (Klaviatura va sichqoncha jamlanmasi)",
    "AirPods Max (AirPods Max quloqchinlari)",
    "Wireless Keyboard & Mouse (Simsiz klaviatura va sichqoncha)",
    "Branded Hoodie (Brendli xudi / Tolstovka)",
    "Branded Powerbank (Brendli poverbank / Tashqi batareya)",
    "Mars Backpack (Mars ryukzaki / Sumka)",
    "AirPods (AirPods simsiz quloqchinlari)",
    "Smartwatch (Aqlli soat)",
    "Yandex Station (Yandex aqlli karnayi / Kolonka)",
    "Smartphone (Smartfon / Telefon)",
    "Planshet Samsung (Samsung plansheti)",
]

# Har bir qatordagi tugmalar soni.
CATEGORY_COLUMNS = 2

category_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=name) for name in CATEGORY_NAMES[i:i + CATEGORY_COLUMNS]]
        for i in range(0, len(CATEGORY_NAMES), CATEGORY_COLUMNS)
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


CANCEL_TEXT = "❌ Bekor qilish"

# Matn kiritish bosqichlarida ko'rsatiladi (nom, narx, telefon, rasm) —
# foydalanuvchiga jarayondan chiqish uchun ko'rinadigan yo'l beradi.
cancel_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=CANCEL_TEXT)]],
    resize_keyboard=True
)


# Reklama xizmati (admin) — tur tanlash tugmalari.
REKLAMA_MATN = "📝 Matnli reklama"
REKLAMA_RASM = "🖼 Rasmli reklama"
REKLAMA_VIDEO = "🎬 Videoli reklama"

reklama_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=REKLAMA_MATN)],
        [KeyboardButton(text=REKLAMA_RASM)],
        [KeyboardButton(text=REKLAMA_VIDEO)],
        [KeyboardButton(text=CANCEL_TEXT)],
    ],
    resize_keyboard=True
)


# Menyulardagi tugmalar ro'yxati — kelgan xabarni tekshirish uchun.
# Menyularning o'zidan hosil qilinadi, shuning uchun doim mos bo'ladi.
# CANCEL_TEXT bu ro'yxatlarga kirmaydi — bekor qilish alohida handlerda ushlanadi.
CATEGORIES = [button.text for row in category_menu.keyboard for button in row]
STATUSES = [button.text for row in status_menu.keyboard for button in row]
