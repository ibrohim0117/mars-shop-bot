from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from states import ElonJoylash, SotibOlish
from keyboards import (
    category_menu, category_menu_back, status_menu, Ha_Yoq_menu, cancel_menu,
    CATEGORIES, STATUSES, BACK_TEXT, CANCEL_TEXT,
    confirmation_button, next_page_button
)
from database import (
    add_elon, get_elonlar_by_category, count_elonlar_by_category, get_user_history
)
from utils import validate_phone_number, validate_price, normalize_phone, main_menu_for
from config import ADMINS

user_router = Router()

MAX_NAME_LEN = 100        # mahsulot nomi uzunligi chegarasi
MAX_PRICE_LEN = 15        # narx uzunligi chegarasi
CAPTION_LIMIT = 1024      # Telegram rasm izohi chegarasi
PAGE_SIZE = 5             # sotib olishda bir sahifadagi e'lonlar soni

AD_DETAIL = (
    "📛 Mahsulot nomi: {name}\n"
    "🎞️ Bo'lim: {category}\n"
    "💎 Narxi: {price}\n"
    "📦 Holati: {status}\n"
    "📞 Telefon: {phone}"
)


def format_ad(ad):
    """E'lon lug'atidan AD_DETAIL matnini hosil qiladi."""
    return AD_DETAIL.format(
        name=ad.get('name', '-'),
        category=ad.get('category', '-'),
        price=ad.get('price', '-'),
        status=ad.get('status', '-'),
        phone=ad.get('phone', '-')
    )


async def _safe_send_ad(msg, image, caption):
    """E'lonni rasm bilan yuboradi; izoh uzun bo'lsa qisqartiradi, rasm yuborilmasa matn qiladi."""
    caption = caption[:CAPTION_LIMIT]
    try:
        await msg.answer_photo(photo=image, caption=caption)
    except Exception:
        await msg.answer(caption)


# ==================== BEKOR QILISH ====================
# Har qanday FSM bosqichida "❌ Bekor qilish" tugmasini ushlaydi.
# Boshqa state handlerlaridan OLDIN ro'yxatdan o'tgani uchun ustuvor.

@user_router.message(F.text == CANCEL_TEXT)
async def cancel_button_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Amal bekor qilindi.", reply_markup=main_menu_for(message.from_user.id))


# ==================== E'LON JOYLASH ====================

@user_router.message(F.text == "➕E'lon joylash", StateFilter(None))
async def elon_joylash_start_handler(message: types.Message, state: FSMContext):
    await message.answer("Mahsulot nomini yozing:", reply_markup=cancel_menu)
    await state.set_state(ElonJoylash.name)


@user_router.message(ElonJoylash.name)
async def elon_name_handler(message: types.Message, state: FSMContext):
    if not message.text:
        await message.answer("⚠️ Iltimos, mahsulot nomini matn ko'rinishida yozing:", reply_markup=cancel_menu)
        return
    if len(message.text) > MAX_NAME_LEN:
        await message.answer(
            f"⚠️ Nom juda uzun (ko'pi bilan {MAX_NAME_LEN} belgi). Qaytadan yozing:",
            reply_markup=cancel_menu
        )
        return
    await state.update_data(name=message.text)
    await message.answer("Mahsulot qaysi bo'limga tegishli?", reply_markup=category_menu)
    await state.set_state(ElonJoylash.category)


@user_router.message(ElonJoylash.category)
async def elon_category_handler(message: types.Message, state: FSMContext):
    if message.text not in CATEGORIES:
        await message.answer("⚠️ Iltimos, quyidagi tugmalardan birini tanlang:", reply_markup=category_menu)
        return
    await state.update_data(category=message.text)
    await message.answer("Mahsulot narxini yozing:", reply_markup=cancel_menu)
    await state.set_state(ElonJoylash.price)


@user_router.message(ElonJoylash.price)
async def elon_price_handler(message: types.Message, state: FSMContext):
    if not validate_price(message.text):
        await message.answer("⚠️ Narx faqat raqamlardan iborat bo'lishi kerak. Qaytadan kiriting:")
        return
    if len(message.text) > MAX_PRICE_LEN:
        await message.answer(f"⚠️ Narx juda katta (ko'pi bilan {MAX_PRICE_LEN} raqam). Qaytadan kiriting:")
        return
    await state.update_data(price=message.text)
    await message.answer("Mahsulot holatini tanlang:", reply_markup=status_menu)
    await state.set_state(ElonJoylash.status)


@user_router.message(ElonJoylash.status)
async def elon_status_handler(message: types.Message, state: FSMContext):
    if message.text not in STATUSES:
        await message.answer("⚠️ Iltimos, quyidagi tugmalardan birini tanlang:", reply_markup=status_menu)
        return
    await state.update_data(status=message.text)
    await message.answer("Mahsulot rasmini yuboring:", reply_markup=cancel_menu)
    await state.set_state(ElonJoylash.image)


@user_router.message(ElonJoylash.image, F.photo)
async def elon_image_handler(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Mahsulot telefon raqamini yozing:", reply_markup=cancel_menu)
    await state.set_state(ElonJoylash.phone)


@user_router.message(ElonJoylash.image)
async def elon_image_invalid_handler(message: types.Message):
    await message.answer("⚠️ Iltimos, faqat rasm formatida fayl yuboring!")


@user_router.message(ElonJoylash.phone)
async def elon_phone_handler(message: types.Message, state: FSMContext):
    if not validate_phone_number(message.text):
        await message.answer("⚠️ Telefon raqami noto'g'ri. Masalan: +998901234567 yoki 901234567")
        return
    # Bazaga yagona formatda saqlash uchun normalizatsiya (901234567)
    await state.update_data(phone=normalize_phone(message.text))
    await message.answer("E'lon joylashsinmi? (Ha/Yo'q)", reply_markup=Ha_Yoq_menu)
    await state.set_state(ElonJoylash.yes_or_no)


@user_router.message(ElonJoylash.yes_or_no)
async def elon_confirm_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    menu = main_menu_for(message.from_user.id)

    if message.text == "Ha":
        # Holat buzilgan bo'lsa (masalan bot qayta ishga tushib, ma'lumot yo'qolsa)
        image = data.get('image')
        if not image:
            await message.answer("❌ E'lon ma'lumotlari topilmadi. Iltimos, boshidan boshlang.", reply_markup=menu)
            await state.clear()
            return

        try:
            ad_id = add_elon(
                user_id=message.from_user.id,
                name=data.get('name', 'Kiritilmagan'),
                category=data.get('category', 'Kiritilmagan'),
                price=data.get('price', 'Kiritilmagan'),
                status=data.get('status', 'Kiritilmagan'),
                image=image,
                phone=data.get('phone', 'Kiritilmagan')
            )
        except Exception:
            await message.answer("❌ E'lonni saqlashda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            await state.clear()
            return

        ad_detail = format_ad(data)

        # E'lonni ko'rib chiqish uchun barcha adminlarga yuborish
        admin_caption = (
            "🆕 Yangi e'lon (ko'rib chiqish uchun):\n"
            f"👤 Foydalanuvchi: {message.from_user.full_name} (@{message.from_user.username})\n"
            f"🆔 ID: {message.from_user.id}\n\n"
            f"{ad_detail}"
        )
        for admin_id in ADMINS:
            try:
                await message.bot.send_photo(
                    chat_id=admin_id, photo=image,
                    caption=admin_caption[:CAPTION_LIMIT],
                    reply_markup=confirmation_button(ad_id)
                )
            except Exception:
                # Bir adminga yuborishda xatolik bo'lsa ham qolganlariga yuborilaveradi
                continue

        # Foydalanuvchiga xabar berish
        user_caption = (
            "✅ E'loningiz qabul qilindi va ko'rib chiqish uchun adminga yuborildi!\n"
            "Tez orada botda e'lon qilinadi.\n\n"
            f"{ad_detail}"
        )
        await _safe_send_ad(message, image, user_caption)
        await message.answer("🏠 Asosiy menyu:", reply_markup=menu)
    else:
        await message.answer("E'lon bekor qilindi!", reply_markup=menu)

    await state.clear()


# ==================== SOTIB OLISH ====================

async def _send_ads_page(msg, state: FSMContext, category, offset, user_id):
    """Kategoriyadagi e'lonlarni sahifalab yuboradi; qolgan bo'lsa 'Keyingi' tugmasini ko'rsatadi."""
    total = count_elonlar_by_category(category)
    ads = get_elonlar_by_category(category, limit=PAGE_SIZE, offset=offset)

    for ad in ads:
        caption = "🛒 Sotuvdagi mahsulot:\n\n" + format_ad(ad)
        await _safe_send_ad(msg, ad['image'], caption)

    new_offset = offset + len(ads)
    if new_offset < total:
        await state.update_data(buy_category=category, buy_offset=new_offset)
        await state.set_state(SotibOlish.category)
        await msg.answer(f"📄 Ko'rsatildi: {new_offset}/{total} ta", reply_markup=next_page_button())
    else:
        await msg.answer("🏠 Asosiy menyu:", reply_markup=main_menu_for(user_id))
        await state.clear()


@user_router.message(F.text == "🎁Sotib olish", StateFilter(None))
async def sotib_olish_start_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "🎁 Siz Sotib olish bo'limiga keldingiz. Marhamat, kategoriya tanlang:",
        reply_markup=category_menu_back
    )
    await state.set_state(SotibOlish.category)


@user_router.message(SotibOlish.category)
async def sotib_olish_category_handler(message: types.Message, state: FSMContext):
    chosen_category = message.text

    # Ortga qaytish — asosiy menyuga
    if chosen_category == BACK_TEXT:
        await message.answer("🏠 Asosiy menyu:", reply_markup=main_menu_for(message.from_user.id))
        await state.clear()
        return

    if chosen_category not in CATEGORIES:
        await message.answer("⚠️ Iltimos, quyidagi tugmalardan birini tanlang:", reply_markup=category_menu_back)
        return

    if count_elonlar_by_category(chosen_category) == 0:
        await message.answer(
            "Siz tanlagan bo'limda hozircha mahsulotlar yo'q.",
            reply_markup=main_menu_for(message.from_user.id)
        )
        await state.clear()
        return

    await _send_ads_page(message, state, chosen_category, 0, message.from_user.id)


@user_router.callback_query(F.data == "buy_next")
async def buy_next_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data.get('buy_category')
    offset = data.get('buy_offset')

    if not category or offset is None:
        await call.answer("Bu ro'yxat eskirgan. Iltimos, qaytadan tanlang.", show_alert=True)
        return

    # Eski "Keyingi" tugmasini olib tashlash (takroriy bosishга qarshi)
    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await call.answer()
    await _send_ads_page(call.message, state, category, offset, call.from_user.id)


# ==================== TARIX VA BOG'LANISH ====================

@user_router.message(F.text == "📝Mening tarixim", StateFilter(None))
async def mening_tarixim_handler(message: types.Message):
    user_ads = get_user_history(message.from_user.id)

    if not user_ads:
        await message.answer("📭 Sizda hali e'lonlar mavjud emas.")
        return

    for ad in user_ads:
        holat = "✅ Tasdiqlangan" if ad.get('is_active') == 1 else "⏳ Ko'rib chiqilmoqda"
        caption = f"{holat}\n\n" + format_ad(ad)
        await _safe_send_ad(message, ad['image'], caption)


@user_router.message(F.text == "📞Biz bilan bog'lanish", StateFilter(None))
async def biz_bilan_boglanish_handler(message: types.Message):
    await message.answer("+998 20 003 722")
