from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from states import ElonJoylash, SotibOlish
from keyboards import (
    category_menu, status_menu, Ha_Yoq_menu, user_main_menu,
    CATEGORIES, STATUSES, confirmation_button
)
from database import add_elon, get_elonlar_by_category, get_user_history, set_elon_status, reject_elon
from validators import validate_phone_number, validate_price
from config import ADMINS

dp = Router()

AD_DETAIL = (
    "📛 Mahsulot nomi: {name}\n"
    "🎞️ Bo'lim: {category}\n"
    "💎 Narxi: {price}\n"
    "📦 Holati: {status}\n"
    "📞 Telefon: {phone}"
)

SUCCESS_TEXT = "📍 E'lon joylashtirildi!\n\n" + AD_DETAIL


@dp.message(F.text == "➕E'lon joylash")
async def elon_joylash_start(message: types.Message, state: FSMContext):
    await message.answer("Mahsulot nomini yozing:")
    await state.set_state(ElonJoylash.name)

@dp.message(ElonJoylash.name)
async def elon_j_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Mahsulot qaysi bo'limga tegishli?", reply_markup=category_menu)
    await state.set_state(ElonJoylash.category)

@dp.message(ElonJoylash.category)
async def elon_j_category(message: types.Message, state: FSMContext):
    if message.text not in CATEGORIES:
        await message.answer("⚠️ Iltimos, quyidagi tugmalardan birini tanlang:", reply_markup=category_menu)
        return
    await state.update_data(category=message.text)
    await message.answer("Mahsulot narxini yozing:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ElonJoylash.price)

@dp.message(ElonJoylash.price)
async def elon_j_price(message: types.Message, state: FSMContext):
    if not validate_price(message.text):
        await message.answer("⚠️ Narx faqat raqamlardan iborat bo'lishi kerak. Qaytadan kiriting:")
        return
    await state.update_data(price=message.text)
    await message.answer("Mahsulot holatini tanlang:", reply_markup=status_menu)
    await state.set_state(ElonJoylash.status)

@dp.message(ElonJoylash.status)
async def elon_j_status(message: types.Message, state: FSMContext):
    if message.text not in STATUSES:
        await message.answer("⚠️ Iltimos, quyidagi tugmalardan birini tanlang:", reply_markup=status_menu)
        return
    await state.update_data(status=message.text)
    await message.answer("Mahsulot rasmini yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ElonJoylash.image)

@dp.message(ElonJoylash.image, F.photo)
async def elon_j_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Mahsulot telefon raqamini yozing:")
    await state.set_state(ElonJoylash.phone)

@dp.message(ElonJoylash.image)
async def elon_j_image_invalid(message: types.Message, state: FSMContext):
    await message.answer("⚠️ Iltimos, faqat rasm formatida fayl yuboring!")

@dp.message(ElonJoylash.phone)
async def elon_j_phone(message: types.Message, state: FSMContext):
    if not validate_phone_number(message.text):
        await message.answer("⚠️ Telefon raqami noto'g'ri. Masalan: +998901234567 yoki 901234567")
        return
    await state.update_data(phone=message.text)
    await message.answer("E'lon joylashsinmi? (Ha/Yo'q)", reply_markup=Ha_Yoq_menu)
    await state.set_state(ElonJoylash.yes_or_no)

@dp.message(ElonJoylash.yes_or_no)
async def elon_j_yes_or_no(message: types.Message, state: FSMContext):
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

        # E'lonni ko'rib chiqish uchun adminga yuborish
        admin_caption = (
            "🆕 Yangi e'lon (ko'rib chiqish uchun):\n"
            f"👤 Foydalanuvchi: {message.from_user.full_name} (@{message.from_user.username})\n"
            f"🆔 ID: {message.from_user.id}\n\n"
            f"{ad_detail}"
        )
        try:
            await message.bot.send_photo(
                chat_id=ADMINS, photo=data['image'],
                caption=admin_caption,
                reply_markup=confirmation_button(ad_id)
            )
        except Exception:
            # Adminga yuborishda xatolik bo'lsa ham foydalanuvchi jarayoni to'xtamasin
            pass

        # Foydalanuvchiga xabar berish
        user_caption = (
            "✅ E'loningiz qabul qilindi va ko'rib chiqish uchun adminga yuborildi!\n"
            "Tez orada botda e'lon qilinadi.\n\n"
            f"{ad_detail}"
        )
        await message.answer_photo(photo=data['image'], caption=user_caption, reply_markup=user_main_menu)
    else:
        await message.answer("E'lon bekor qilindi!", reply_markup=user_main_menu)

    await state.clear()



@dp.callback_query(lambda c: c.data and c.data.startswith("review_accept:"))
async def elon_tasdiqlash(call: types.CallbackQuery):
    elon_id = int(call.data.split(":")[1])
    user_id = set_elon_status(elon_id)

    try:
        await call.bot.send_message(
            chat_id=user_id,
            text="✅ E'loningiz tasdiqlandi va tez orada botda e'lon qilinadi!"
        )
    except Exception:
        pass

    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await call.answer("Siz e'lonni tasdiqladingiz!")


@dp.callback_query(lambda c: c.data and c.data.startswith("review_reject:"))
async def elon_bekor_qilish(call: types.CallbackQuery):
    elon_id = int(call.data.split(":")[1])
    user_id = reject_elon(elon_id)

    if user_id:
        try:
            await call.bot.send_message(
                chat_id=user_id,
                text="❌ Afsuski, e'loningiz admin tomonidan rad etildi."
            )
        except Exception:
            pass

    # Takroriy bosishni oldini olish uchun tugmalarni olib tashlash
    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await call.answer("Siz e'lonni rad etdingiz!")








@dp.message(F.text == "🎁Sotib olish")
async def sotib_olish(message: types.Message, state: FSMContext):
    await message.answer("🎁 Siz Sotib olish bo'limiga keldingiz. Marhamat, kategoriya tanlang:", reply_markup=category_menu)
    await state.set_state(SotibOlish.category)

@dp.message(SotibOlish.category)
async def sotib_olish_category(message: types.Message, state: FSMContext):
    chosen_category = message.text

    ads_found = get_elonlar_by_category(chosen_category)

    if not ads_found:
        await message.answer("Siz tanlagan bo'limda hozircha mahsulotlar yo'q.", reply_markup=ReplyKeyboardRemove())
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

    await state.clear()

@dp.message(F.text == "📝Mening tarixim")
async def tarix_m(message: types.Message, state: FSMContext):
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

@dp.message(F.text == "📞Biz bilan bog'lanish")
async def biz_boglanish(message: types.Message):
    await message.answer("+998 20 003 722")
