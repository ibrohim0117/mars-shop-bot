# Mars Shop Bot

Mahsulot e'lonlari uchun Telegram bot. Foydalanuvchilar e'lon joylaydi, admin ularni
ko'rib chiqib tasdiqlaydi yoki rad etadi, tasdiqlangan e'lonlar "Sotib olish" bo'limida ko'rinadi.

## Imkoniyatlar

**Foydalanuvchi:**
- ➕ E'lon joylash (nom, kategoriya, narx, holat, rasm, telefon)
- 🎁 Sotib olish — kategoriya bo'yicha tasdiqlangan e'lonlarni ko'rish
- 📝 Mening tarixim — o'z e'lonlari
- 📞 Biz bilan bog'lanish
- Istalgan bosqichda `/cancel` yoki "❌ Bekor qilish" bilan chiqish

**Admin:**
- E'lonni ✅ tasdiqlash / ❌ rad etish (foydalanuvchiga avtomatik xabar boradi)
- 🔃 Foydalanuvchini ban qilish / bandan chiqarish
- 👨‍💼 Foydalanuvchilar sonini ko'rish
- Bir nechta admin qo'llab-quvvatlanadi

## Texnologiyalar

- Python 3.10+
- [aiogram 3.x](https://docs.aiogram.dev/)
- SQLite

## O'rnatish

```bash
# 1. Virtual muhit yaratish
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Kutubxonalarni o'rnatish
pip install -r requirements.txt

# 3. Sozlamalar faylini tayyorlash
cp .env.example .env
```

`.env` faylni to'ldiring:

```env
TOKEN=8123456789:AA...          # @BotFather dan olinadi
ADMINS=1038185913               # Telegram user ID (bir nechta bo'lsa: 111,222,333)
```

> O'z ID'ingizni bilish uchun botga `/get_my_id` yozing.

## Ishga tushirish

```bash
python main.py
```

Baza (`mars_shop_clone.db`) birinchi ishga tushishda avtomatik yaratiladi.

## Loyiha tuzilishi

```
mars-shop-bot/
├── main.py                  # Botni ishga tushirish, router va middleware ulash
├── config.py                # TOKEN, ADMINS, is_admin()
├── requirements.txt
├── .env.example
├── handlers/
│   ├── commands.py          # /start, /help, /cancel, /get_my_id, /admin_button
│   ├── user.py              # E'lon joylash, sotib olish, tarix
│   └── admin.py             # Tasdiqlash/rad etish, ban/unban
├── keyboards/
│   ├── reply.py             # Reply menyular + CATEGORIES / STATUSES
│   └── inline.py            # Inline tugmalar
├── database/
│   └── queries.py           # Barcha SQL funksiyalar
├── middlewares/
│   └── ban.py               # Ban qilingan foydalanuvchilarni bloklash
├── states/
│   └── states.py            # FSM holatlar
└── utils/
    └── validators.py        # Telefon va narx tekshiruvi
```

## Komandalar

| Komanda | Vazifasi |
|---|---|
| `/start` | Botni ishga tushirish (yarim qolgan jarayonni ham tozalaydi) |
| `/cancel` | Joriy amalni bekor qilish |
| `/help` | Yordam |
| `/get_my_id` | O'z Telegram ma'lumotlaringiz |
| `/admin_button` | Admin menyusiga qaytish (faqat admin) |

## E'lon oqimi

1. Foydalanuvchi e'lon to'ldiradi → baza ga `is_active=0` bilan saqlanadi
2. E'lon barcha adminlarga ko'rib chiqish uchun yuboriladi
3. Admin **tasdiqlasa** → `is_active=1`, foydalanuvchiga xabar boradi, e'lon "Sotib olish"da ko'rinadi
4. Admin **rad etsa** → e'lon o'chiriladi, foydalanuvchiga xabar boradi
