from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from states import ElonJoylash, SotibOlish
from keyboards import (
    category_menu, category_menu_back, status_menu, Ha_Yoq_menu,
    user_main_menu, admin_main_menu, cancel_menu,
    CATEGORIES, STATUSES, BACK_TEXT, CANCEL_TEXT, confirmation_button
)
from database import add_elon, get_elonlar_by_category, get_user_history
from utils import validate_phone_number, validate_price
from config import ADMINS, is_admin

user_router = Router()


def main_menu_for(user_id):
    """Foydalanuvchi roliga mos asosiy menyu."""
    return admin_main_menu if is_admin(user_id) else user_main_menu


# ==================== BEKOR QILISH ====================
# Har qanday FSM bosqichida "❌ Bekor qilish" tugmasini ushlaydi.
# Boshqa state handlerlaridan OLDIN ro'yxatdan o'tgani uchun ustuvor.

@user_router.message(F.text == CANCEL_TEXT)
async def cancel_button_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Amal bekor qilindi.", reply_markup=main_menu_for(message.from_user.id))

AD_DETAIL = (
    "📛 Mahsulot nomi: {name}\n"
    "🎞️ Bo'lim: {category}\n"
    "💎 Narxi: {price}\n"
    "📦 Holati: {status}\n"
    "📞 Telefon: {phone}"
)

SUCCESS_TEXT = "📍 E'lon joylashtirildi!\n\n" + AD_DETAIL


# ==================== E'LON JOYLASH ====================

@user_router.message(F.text == "➕E'lon joylash")
async def elon_joylash_start_handler(message: types.Message, state: FSMContext):
    await message.answer("Mahsulot nomini yozing:", reply_markup=cancel_menu)
    await state.set_state(ElonJoylash.name)


@user_router.message(ElonJoylash.name)
async def elon_name_handler(message: types.Message, state: FSMContext):
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
async def elon_image_invalid_handler(message: types.Message, state: FSMContext):
    await message.answer("⚠️ Iltimos, faqat rasm formatida fayl yuboring!")


@user_router.message(ElonJoylash.phone)
async def elon_phone_handler(message: types.Message, state: FSMContext):
    if not validate_phone_number(message.text):
        await message.answer("⚠️ Telefon raqami noto'g'ri. Masalan: +998901234567 yoki 901234567")
        return
    await state.update_data(phone=message.text)
    await message.answer("E'lon joylashsinmi? (Ha/Yo'q)", reply_markup=Ha_Yoq_menu)
    await state.set_state(ElonJoylash.yes_or_no)


@user_router.message(ElonJoylash.yes_or_no)
async def elon_confirm_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if message.text == "Ha":
        try:
            ad_id = add_elon(
                user_id=message.from_user.id,
                name=data.get('name', 'Kiritilmagan'),
                category=data.get('category', 'Kiritilmagan'),
                price=data.get('price', 'Kiritilmagan'),
                status=data.get('status', 'Kiritilmagan'),
                image=data.get('image'),
                phone=data.get('phone', 'Kiritilmagan')
            )
        except Exception:
            await message.answer("❌ E'lonni saqlashda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            await state.clear()
            return

        ad_detail = AD_DETAIL.format(
            name=data.get('name', "Kiritilmagan"),
            category=data.get('category', "Kiritilmagan"),
            price=data.get('price', "Kiritilmagan"),
            status=data.get('status', "Kiritilmagan"),
            phone=data.get('phone', "Kiritilmagan")
        )

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
                    chat_id=admin_id, photo=data['image'],
                    caption=admin_caption,
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
        await message.answer_photo(photo=data.get('image'), caption=user_caption, reply_markup=user_main_menu)
    else:
        await message.answer("E'lon bekor qilindi!", reply_markup=user_main_menu)

    await state.clear()


# ==================== SOTIB OLISH ====================

@user_router.message(F.text == "🎁Sotib olish")
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
        await message.answer("🏠 Asosiy menyu:", reply_markup=user_main_menu)
        await state.clear()
        return

    if chosen_category not in CATEGORIES:
        await message.answer("⚠️ Iltimos, quyidagi tugmalardan birini tanlang:", reply_markup=category_menu_back)
        return

    ads_found = get_elonlar_by_category(chosen_category)

    if not ads_found:
        await message.answer("Siz tanlagan bo'limda hozircha mahsulotlar yo'q.", reply_markup=user_main_menu)
        await state.clear()
        return

    for ad in ads_found:
        text = SUCCESS_TEXT.format(
            name=ad.get('name', '-'),
            category=ad.get('category', '-'),
            price=ad.get('price', '-'),
            status=ad.get('status', '-'),
            phone=ad.get('phone', '-')
        )
        await message.answer_photo(photo=ad['image'], caption=text)

    await message.answer("🏠 Asosiy menyu:", reply_markup=user_main_menu)
    await state.clear()


# ==================== TARIX VA BOG'LANISH ====================

@user_router.message(F.text == "📝Mening tarixim")
async def mening_tarixim_handler(message: types.Message):
    user_ads = get_user_history(message.from_user.id)

    if not user_ads:
        await message.answer("📭 Sizda hali e'lonlar mavjud emas.")
        return

    for ad in user_ads:
        text = SUCCESS_TEXT.format(
            name=ad.get('name', '-'),
            category=ad.get('category', '-'),
            price=ad.get('price', '-'),
            status=ad.get('status', '-'),
            phone=ad.get('phone', '-')
        )
        await message.answer_photo(photo=ad['image'], caption=text)


@user_router.message(F.text == "📞Biz bilan bog'lanish")
async def biz_bilan_boglanish_handler(message: types.Message):
    await message.answer("+998 20 003 722")
