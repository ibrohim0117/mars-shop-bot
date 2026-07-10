from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from states import ElonJoylash, SotibOlish
from keyboards import category_menu, status_menu, Ha_Yoq_menu, user_main_menu, CATEGORIES, STATUSES
from database import add_elon, get_elonlar_by_category, get_user_history
from validators import validate_phone_number, validate_price
from config import ADMINS

op = Router()

AD_DETAIL = (
    "📛 Mahsulot nomi: {name}\n"
    "🎞️ Bo'lim: {category}\n"
    "💎 Narxi: {price}\n"
    "📦 Holati: {status}\n"
    "📞 Telefon: {phone}"
)

SUCCESS_TEXT = "📍 E'lon joylashtirildi!\n\n" + AD_DETAIL


@op.message(F.text == "➕E'lon joylash")
async def elon_joylash_start(message: types.Message, state: FSMContext):
    await message.answer("Mahsulot nomini yozing:")
    await state.set_state(ElonJoylash.name)

@op.message(ElonJoylash.name)
async def elon_j_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Mahsulot qaysi bo'limga tegishli?", reply_markup=category_menu)
    await state.set_state(ElonJoylash.category)

@op.message(ElonJoylash.category)
async def elon_j_category(message: types.Message, state: FSMContext):
    if message.text not in CATEGORIES:
        await message.answer("⚠️ Iltimos, quyidagi tugmalardan birini tanlang:", reply_markup=category_menu)
        return
    await state.update_data(category=message.text)
    await message.answer("Mahsulot narxini yozing:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ElonJoylash.price)

@op.message(ElonJoylash.price)
async def elon_j_price(message: types.Message, state: FSMContext):
    if not validate_price(message.text):
        await message.answer("⚠️ Narx faqat raqamlardan iborat bo'lishi kerak. Qaytadan kiriting:")
        return
    await state.update_data(price=message.text)
    await message.answer("Mahsulot holatini tanlang:", reply_markup=status_menu)
    await state.set_state(ElonJoylash.status)

@op.message(ElonJoylash.status)
async def elon_j_status(message: types.Message, state: FSMContext):
    if message.text not in STATUSES:
        await message.answer("⚠️ Iltimos, quyidagi tugmalardan birini tanlang:", reply_markup=status_menu)
        return
    await state.update_data(status=message.text)
    await message.answer("Mahsulot rasmini yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ElonJoylash.image)

@op.message(ElonJoylash.image, F.photo)
async def elon_j_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Mahsulot telefon raqamini yozing:")
    await state.set_state(ElonJoylash.phone)

@op.message(ElonJoylash.image)
async def elon_j_image_invalid(message: types.Message, state: FSMContext):
    await message.answer("⚠️ Iltimos, faqat rasm formatida fayl yuboring!")

@op.message(ElonJoylash.phone)
async def elon_j_phone(message: types.Message, state: FSMContext):
    if not validate_phone_number(message.text):
        await message.answer("⚠️ Telefon raqami noto'g'ri. Masalan: +998901234567 yoki 901234567")
        return
    await state.update_data(phone=message.text)
    await message.answer("E'lon joylashsinmi? (Ha/Yoq)", reply_markup=Ha_Yoq_menu)
    await state.set_state(ElonJoylash.yes_or_no)

@op.message(ElonJoylash.yes_or_no)
async def elon_j_yes_or_no(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if message.text == "Ha":
        try:
            add_elon(
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
            await message.bot.send_photo(chat_id=ADMINS, photo=data['image'], caption=admin_caption)
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












@op.message(F.text == "🎁Sotib olish")
async def sotib_olish(message: types.Message, state: FSMContext):
    await message.answer("🎁 Siz Sotib olish bo'limiga keldingiz. Marhamat, kategoriya tanlang:", reply_markup=category_menu)
    await state.set_state(SotibOlish.category)

@op.message(SotibOlish.category)
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

@op.message(F.text == "📝Mening tarixim")
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

@op.message(F.text == "📞Biz bilan bog'lanish")
async def biz_boglanish(message: types.Message):
    await message.answer("+998 20 003 722")
