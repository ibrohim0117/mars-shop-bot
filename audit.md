# Mars Shop Bot — Loyiha Auditi

**Sana:** 2026-07-20
**Qamrov:** butun loyiha (handlers, database, keyboards, middlewares, states, utils, config)
**Tekshiruv usuli:** kod tahlili + `venv` (aiogram 3.29.1) orqali haqiqiy import va handler tartibini tekshirish

---

## Mundarija

- [🔴 A. Bajarilmagan holatlar](#-a-bajarilmagan-umuman-yoq)
- [🟡 B. Bajarilgan, lekin kamchiligi bor](#-b-bajarilgan-lekin-kamchiligi-bor)
- [⚪ C. E'tiborga olish kerak](#-c-etiborga-olish-kerak)
- [✅ To'g'ri ishlayotgan qismlar](#-togri-ishlayotgan-qismlar)
- [📋 Tuzatish tartibi](#-tavsiya-etilgan-tuzatish-tartibi)

---

## 🔴 A. BAJARILMAGAN (umuman yo'q)

### A1. Tasdiqlangan e'lonlar filtri yo'q — ENG JIDDIY XATO

**Fayl:** `database/queries.py` → `get_elonlar_by_category`

`WHERE is_active = 1` sharti **yo'q**.

**Natija:** butun ko'rib chiqish (review) tizimi ishlamayapti. Foydalanuvchi e'lon joylashi bilanoq,
admin tasdiqlamasdan turib ham u "🎁Sotib olish" bo'limida ko'rinadi. `is_active` ustuni mavjud,
admin uni `1` qiladi — lekin hech qayerda tekshirilmaydi.

**Tuzatish:** so'rovga `AND is_active = 1` qo'shish.

---

### A2. `/cancel` yoki "Bekor qilish" tugmasi yo'q — jarayondan chiqib bo'lmaydi

**Fayl:** `handlers/user.py`

Handler ro'yxatdan o'tish tartibi tekshirildi:

```
 1. elon_joylash_start_handler   (F.text == "➕E'lon joylash")
 2. elon_name_handler            (ElonJoylash.name — matn filtri YO'Q)
 ...
10. sotib_olish_start_handler    (F.text == "🎁Sotib olish")
```

`elon_name_handler` (#2) `sotib_olish_start_handler` (#10) dan **oldin** turadi va unda matn filtri yo'q.

**Natija:** user "➕E'lon joylash" bosib, mahsulot nomi so'ralganda "🎁Sotib olish" tugmasini bossa —
**u mahsulot nomi sifatida saqlanadi**. `📝Mening tarixim` va `📞Biz bilan bog'lanish` ham xuddi shunday
yutiladi. Jarayondan chiqishning yagona yo'li — oxirigacha borish.

**Tuzatish:** `/cancel` komandasi + har bir FSM bosqichida "❌ Bekor qilish" tugmasi.

---

### A3. `/start` FSM holatini tozalamaydi

**Fayl:** `handlers/commands.py` → `start_handler`

`state.clear()` yo'q (`state: FSMContext` parametri ham olinmagan).

**Natija:** user jarayon o'rtasida `/start` bossa — menyu chiqadi, lekin **eski holat saqlanib qoladi**.
Keyingi bosgan tugmasi yana o'sha yarim qolgan e'longa ma'lumot bo'lib ketadi.

> Eslatma: aiogram 3 da state filtri ko'rsatilmagan handler **har qanday holatda** ishlaydi,
> shuning uchun `/start` o'zi ishlaydi — muammo faqat holat tozalanmasligida.

---

### A4. Ikkita admin tugmasi umuman ishlamaydi

**Fayl:** `keyboards/reply.py` → `admin_main_menu`

| Tugma | Handler |
|---|---|
| `👨🏻‍💻Kategory yaratish` | ❌ yo'q |
| `🔥Reklama xizmati` | ❌ yo'q |

Bosilganda hech narsa sodir bo'lmaydi. Kategoriyalar hozir `keyboards/reply.py` da qattiq
yozilgan (hardcoded), bazadan olinmaydi — ya'ni "Kategory yaratish" ishlashi uchun avval
kategoriyalar uchun alohida jadval kerak.

---

### A5. Admin uchun "kutilayotgan e'lonlar" ro'yxati yo'q

Agar admin xabarni o'chirib yuborsa yoki o'tkazib yuborsa, e'lon abadiy `is_active=0` bo'lib qoladi —
uni topishning **hech qanday yo'li yo'q**.

**Tuzatish:** admin menyusiga "⏳ Kutilayotgan e'lonlar" tugmasi.

---

### A6. README yo'q

Loyihani ishga tushirish bo'yicha hujjat mavjud emas (o'rnatish, `.env` sozlash, ishga tushirish).

---

## 🟡 B. BAJARILGAN, LEKIN KAMCHILIGI BOR

### B1. Ban qilingan userning e'lonlari sotuvda qolaveradi

Ban faqat foydalanuvchining **harakatlarini** to'xtatadi. Uning avval joylagan e'lonlari
"Sotib olish" bo'limida ko'rinaveradi.

---

### B2. Ko'p adminda takroriy tasdiqlash muammosi

**Fayl:** `handlers/admin.py`

E'lon barcha adminlarga boradi va har birida tugma bo'ladi.

- 1-admin **rad etsa** (e'lon o'chadi) → 2-admin "Tasdiqlash" bossa: `set_elon_status` `None` qaytaradi,
  userga xabar bormaydi, **ammo adminga "Siz e'lonni tasdiqladingiz!" deb ko'rsatiladi** — yolg'on tasdiq.
- Tugmalar faqat **bosgan adminning** xabarida o'chiriladi, qolgan adminlarda qolaveradi.

---

### B3. `📝Mening tarixim` e'lon holatini ko'rsatmaydi

**Fayl:** `database/queries.py` → `get_user_history`

`is_active` tanlanmaydi. User o'z e'loni **tasdiqlanganmi yoki kutilyaptimi — bila olmaydi**.
Hammasi "📍 E'lon joylashtirildi!" deb chiqadi.

---

### B4. `SUCCESS_TEXT` sarlavhasi chalg'ituvchi

**Fayl:** `handlers/user.py`

"📍 E'lon joylashtirildi!" matni **sotib olish** va **tarix** bo'limlarida ham ishlatiladi.
Xaridor boshqa odamning mahsulotini ko'rib turib "E'lon joylashtirildi" degan yozuvni o'qiydi.

---

### B5. `VARCHAR(50)` cheklovi haqiqiy emas

SQLite `VARCHAR(n)` uzunligini **majburlamaydi**. Kodda ham uzunlik tekshiruvi yo'q.

**Natija:** user 4000 belgilik mahsulot nomi yubora oladi. Bu Telegram caption limitidan (1024 belgi)
oshib ketadi va `answer_photo` ni ishdan chiqaradi.

**Tuzatish:** `utils/validators.py` ga uzunlik tekshiruvi qo'shish.

---

### B6. 9 ta bare `except Exception` — xatolar ko'rinmay yutiladi

| Fayl | Soni |
|---|---|
| `handlers/admin.py` | 6 |
| `handlers/user.py` | 2 |
| `handlers/commands.py` | 1 |

Hech biri **log yozmaydi**. Adminga e'lon yuborilmasa yoki DB xato bersa — sabab hech qayerda
qolmaydi, debug qilish imkonsiz.

**Tuzatish:** `logging.exception(...)` qo'shish.

---

### B7. `data['image']` — KeyError xavfi

**Fayl:** `handlers/user.py` → `elon_confirm_handler`

`.get()` emas, to'g'ridan-to'g'ri indeks ishlatilgan (2 joyda). Holat buzilgan bo'lsa
(masalan bot qayta ishga tushsa, `MemoryStorage` o'chadi) — handler ishdan chiqadi.

---

### B8. `add_user` ma'lumotni yangilamaydi

**Fayl:** `database/queries.py`

Oddiy `INSERT` + chaqiruv joyida `except: pass`. User ismini yoki username'ini o'zgartirsa —
bazada **eski qiymat abadiy qoladi**.

**Tuzatish:** `INSERT ... ON CONFLICT(user_id) DO UPDATE SET full_name=..., username=...`

---

### B9. Telefon raqami turli formatlarda saqlanadi

**Fayl:** `utils/validators.py`

`validate_phone_number` ikkalasini ham qabul qiladi: `901234567` va `+998901234567`.
Normalizatsiya yo'q — bazada aralash format yig'iladi.

---

### B10. `count_users` ban qilinganlarni ham sanaydi

"Jami foydalanuvchilar" soni faol/ban ajratmaydi.

---

### B11. `MemoryStorage` — qayta ishga tushirilsa hammasi yo'qoladi

**Fayl:** `main.py`

Bot restart bo'lsa, yarim to'ldirilgan e'lonlar yo'qoladi. Kichik loyiha uchun qabul qilsa bo'ladi,
lekin bilib qo'yish kerak.

---

### B12. Sotib olishda sahifalash (pagination) yo'q

Kategoriyada 100 ta mahsulot bo'lsa — 100 ta rasm ketma-ket yuboriladi.
Telegram rate-limit'iga tushadi.

---

### B13. `elon_image_invalid_handler` da ishlatilmagan parametr

**Fayl:** `handlers/user.py`

`state: FSMContext` olinadi, lekin ishlatilmaydi.

---

## ⚪ C. E'TIBORGA OLISH KERAK

| Holat | Izoh |
|---|---|
| **Baza nomi o'zgardi** | `DB_NAME = "mars_shop_clone.db"`. Hozircha hech qanday `.db` fayl yo'q — baza **noldan** yaratiladi. Eski `bot_data.db` (11 user, 2 e'lon) o'chirilgan |
| **`.env` xavfsiz** | Tekshirildi — git tarixiga **hech qachon tushmagan**, `.gitignore` himoyalayapti ✅ |
| **`.gitignore`da ortiqcha qator** | `bot_data.db` alohida yozilgan, lekin `*.db` uni allaqachon qamrab oladi |
| **Katta refaktoring commit qilinmagan** | `git status` da 8 ta o'chirilgan fayl va 6 ta yangi papka turibdi |

---

## ✅ TO'G'RI ISHLAYOTGAN QISMLAR

Bular tekshirildi va muammosiz:

- **Papka tuzilishi** — `handlers/`, `keyboards/`, `database/`, `middlewares/`, `states/`, `utils/`
  paketlarga to'g'ri ajratilgan, `__init__.py` orqali toza importlar
- **Handler nomlari** — 25 tasi ham `_handler` bilan tugaydi, ma'noli nomlangan
- **Ban middleware** — barcha xabar va callback'larni qamrab oladi, adminlar istisno,
  yangi foydalanuvchi (`status=None`) to'silmaydi
- **Ko'p adminli tizim** — `is_admin()` matn/`None`/noto'g'ri qiymatlarda ishdan chiqmaydi;
  `"111,222 , 333,,xato,444"` → `[111, 222, 333, 444]`
- **Kirish tekshiruvlari** — narx (faqat raqam), telefon (regex), kategoriya va holat
  (tugmalar ro'yxatidan) tekshiriladi
- **`CATEGORIES` / `STATUSES`** — menyularning o'zidan hosil qilinadi, chalkashish mumkin emas;
  `BACK_TEXT` kategoriya sifatida hisoblanmaydi
- **DB ulanishlari** — barcha funksiyalarda `try/finally`, ulanish sizib chiqmaydi
- **Adminni ban qilib bo'lmaydi** — `is_admin()` guard bilan himoyalangan

---

## 📋 TAVSIYA ETILGAN TUZATISH TARTIBI

| # | Nima | Nega birinchi |
|---|---|---|
| 1 | **A1** — `is_active = 1` filtri | Bir qatorlik tuzatish, butun review tizimini tiklaydi |
| 2 | **A2 + A3** — `/cancel` va `/start` da `state.clear()` | Eng ko'p uchraydigan foydalanuvchi muammosi |
| 3 | **B3** — tarixda holat ko'rsatish | A1 dan keyin user o'z e'loni qayerdaligini bilishi shart |
| 4 | **B2** — takroriy tasdiqlash | Ko'p admin endi qo'shilgani uchun dolzarb |
| 5 | **B6** — logging | Qolgan xatolarni topish uchun kerak |
| 6 | **A4, A5** — yetishmayotgan admin funksiyalari | Yangi imkoniyatlar |
| 7 | Qolganlari (B1, B4, B5, B7–B13) | Sifat yaxshilash |

> **Eslatma:** 1–3 nuqtalar o'zaro bog'liq — ularni birgalikda qilish mantiqiy.
