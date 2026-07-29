# 🚀 Mars Shop Bot

Brendli mahsulotlar uchun **e'lonlar bozori** Telegram bot. Foydalanuvchilar mahsulot e'loni
joylaydi, adminlar ularni ko'rib chiqib tasdiqlaydi yoki rad etadi, tasdiqlangan e'lonlar esa
"Sotib olish" bo'limida kategoriya bo'yicha ko'rinadi. Bundan tashqari admin foydalanuvchilarni
boshqaradi va reklama tarqatadi.

Aiogram 3 asosida, modulli (papkalarga ajratilgan) tuzilma bilan yozilgan.

---

## ✨ Imkoniyatlar

### 👤 Foydalanuvchi
- **➕ E'lon joylash** — bosqichma-bosqich: nom → kategoriya → narx → holat → rasm → telefon → tasdiq
- **🎁 Sotib olish** — kategoriya tanlab, tasdiqlangan mahsulotlarni ko'rish (sahifalab, "Keyingi ➡️")
- **📝 Mening tarixim** — o'z e'lonlari va ularning holati (✅ tasdiqlangan / ⏳ ko'rib chiqilmoqda)
- **📞 Biz bilan bog'lanish**
- Istalgan bosqichda **`/cancel`** yoki **❌ Bekor qilish** bilan chiqish

### 🛡 Admin
- **E'lonni ✅ tasdiqlash / ❌ rad etish** — foydalanuvchiga avtomatik xabar boradi
- **⏳ Kutilayotgan e'lonlar** — hali ko'rib chiqilmagan e'lonlar ro'yxati
- **🔃 Foydalanuvchini boshqarish** — ban qilish / bandan chiqarish
- **🔥 Reklama xizmati** — barcha foydalanuvchilarga matn / rasm / video reklama tarqatish
- **👨‍💼 Foydalanuvchilar statistikasi** — jami / faol / ban qilingan
- **Bir nechta admin** qo'llab-quvvatlanadi

---

## 🧰 Texnologiyalar

- **Python 3.10+**
- **[aiogram 3.x](https://docs.aiogram.dev/)** — Telegram Bot Framework (FSM, middleware, router)
- **SQLite** — ma'lumotlar bazasi (tashqi kutubxonasiz)
- **python-dotenv** — `.env` sozlamalari

---

## ⚙️ O'rnatish

```bash
# 1. Loyihani klonlash / ochish
cd mars-shop-bot

# 2. Virtual muhit
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Kutubxonalar
pip install -r requirements.txt

# 4. Sozlamalar fayli
cp .env.example .env
```

`.env` faylni to'ldiring:

```env
TOKEN=8123456789:AA...            # @BotFather dan olinadi
ADMINS=1038185913                 # Admin ID. Bir nechta bo'lsa vergul bilan: 111,222,333
```

> 💡 O'z Telegram ID'ingizni bilish uchun botga **`/get_my_id`** yozing.

---

## ▶️ Ishga tushirish

```bash
python main.py
```

Baza fayli (`mars_shop_clone.db`) birinchi ishga tushishda avtomatik yaratiladi.

---

## 🗂 Loyiha tuzilishi

```
mars-shop-bot/
├── main.py                  # Kirish nuqtasi: router va middleware ulash, polling
├── config.py                # TOKEN, ADMINS ro'yxati, is_admin()
├── requirements.txt
├── .env.example
│
├── handlers/                # Xabar va tugma ishlovchilari (barchasi *_handler)
│   ├── commands.py          # /start, /cancel, /help, /get_my_id, /admin_button, statistika
│   ├── user.py              # E'lon joylash, sotib olish (sahifalash), tarix, bog'lanish
│   └── admin.py             # Tasdiqlash/rad etish, ban/unban, reklama tarqatish
│
├── keyboards/               # Klaviaturalar
│   ├── reply.py             # Reply menyular + CATEGORY_NAMES / CATEGORIES / STATUSES
│   └── inline.py            # Inline tugmalar (tasdiqlash, ban, "Keyingi")
│
├── database/                # Ma'lumotlar bazasi
│   └── queries.py           # Barcha SQL funksiyalar (users, elonlar)
│
├── middlewares/             # Oraliq qatlam
│   └── ban.py               # Ban qilinganlarni bloklash (TTL kesh bilan)
│
├── states/                  # FSM holatlari
│   └── states.py            # ElonJoylash, SotibOlish, ChangeUserStatus, Reklama
│
└── utils/                   # Yordamchi funksiyalar
    ├── validators.py        # Telefon/narx tekshiruvi va normalizatsiya
    └── menus.py             # main_menu_for() — rolga mos menyu
```

Har bir paketda `__init__.py` mavjud, shuning uchun importlar toza:
`from database import add_elon`, `from keyboards import user_main_menu`.

---

## 💬 Komandalar

| Komanda | Vazifasi |
|---|---|
| `/start` | Botni ishga tushirish (yarim qolgan jarayonni tozalaydi) |
| `/cancel` | Joriy amalni bekor qilish |
| `/help` | Yordam |
| `/get_my_id` | O'z Telegram ma'lumotlaringiz (ism, username, ID) |
| `/admin_button` | Admin menyusiga qaytish (faqat admin) |

---

## 🗃 Ma'lumotlar bazasi

**`users`**

| Ustun | Turi | Izoh |
|---|---|---|
| `user_id` | INTEGER PK | Telegram ID |
| `full_name` | VARCHAR(100) | To'liq ism |
| `username` | VARCHAR(50) | @username |
| `is_active` | INTEGER | 1 = faol, 0 = ban |

**`elonlar`**

| Ustun | Turi | Izoh |
|---|---|---|
| `id` | INTEGER PK | E'lon ID |
| `user_id` | INTEGER | E'lon egasi |
| `name` | VARCHAR(50) | Mahsulot nomi |
| `category` | VARCHAR(50) | Kategoriya |
| `price` | VARCHAR(50) | Narx |
| `status` | VARCHAR(50) | Holati (Yangi/O'rtacha/Eski) |
| `image` | VARCHAR(255) | Rasm file_id |
| `phone` | VARCHAR(20) | Telefon (901234567 formatida) |
| `is_active` | INTEGER | 1 = tasdiqlangan, 0 = kutilmoqda |

---

## 🔄 E'lon oqimi

```
Foydalanuvchi e'lon to'ldiradi
        │
        ▼
Baza ga is_active=0 (kutilmoqda) bilan saqlanadi
        │
        ▼
Barcha adminlarga ko'rib chiqish uchun yuboriladi
        │
        ├── ✅ Tasdiqlash → is_active=1, userga xabar, "Sotib olish"da ko'rinadi
        └── ❌ Rad etish  → e'lon o'chiriladi, userga xabar
```

---

## 🧱 Muhandislik yechimlari

- **Ban middleware** — ban qilingan foydalanuvchi hech qanday tugma/komanda ishlata olmaydi;
  natijalar 60s **TTL kesh**da saqlanadi, ban/unban paytida darhol yangilanadi.
- **Reklama tarqatish** — `copy_message` orqali (matn/rasm/video asl ko'rinishda), faqat faol
  foydalanuvchilarga, rate-limit himoyasi bilan.
- **Kirish tekshiruvlari** — telefon (regex + normalizatsiya), narx (faqat raqam), nom uzunligi,
  kategoriya/holat (tugmalar ro'yxatidan).
- **Sahifalash** — sotib olishda `LIMIT/OFFSET` bilan har sahifada 5 ta e'lon.
- **Xavfsiz yuborish** — uzun izoh 1024 belgiga qisqartiriladi, rasm yuborilmasa matnga o'tadi.

---

## 📄 Litsenziya

Ushbu loyiha o'quv/shaxsiy maqsadlar uchun. Erkin foydalaning.
