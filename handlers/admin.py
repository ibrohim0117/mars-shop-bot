from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from database import (
    set_elon_status, reject_elon, get_user_status, change_user_status, get_pending_elonlar
)
from keyboards import user_main_menu, changeuserstatusbutton, confirmation_button
from states import ChangeUserStatus
from config import is_admin

admin_router = Router()


# ==================== KUTILAYOTGAN E'LONLAR ====================

@admin_router.message(F.text == "⏳ Kutilayotgan e'lonlar")
async def pending_elonlar_handler(message: types.Message):
    if not is_admin(message.from_user.id):
        return

    ads = get_pending_elonlar()
    if not ads:
        await message.answer("✅ Tasdiq kutayotgan e'lonlar yo'q.")
        return

    await message.answer(f"⏳ Tasdiq kutayotgan e'lonlar: {len(ads)} ta")
    for ad in ads:
        caption = (
            "⏳ Kutilayotgan e'lon:\n"
            f"👤 Foydalanuvchi ID: {ad['user_id']}\n\n"
            f"📛 Mahsulot nomi: {ad['name']}\n"
            f"🎞️ Bo'lim: {ad['category']}\n"
            f"💎 Narxi: {ad['price']}\n"
            f"📦 Holati: {ad['status']}\n"
            f"📞 Telefon: {ad['phone']}"
        )
        try:
            await message.answer_photo(
                photo=ad['image'],
                caption=caption,
                reply_markup=confirmation_button(ad['id'])
            )
        except Exception:
            # Rasm yuborilmasa (masalan file_id eskirgan) — matn ko'rinishida
            await message.answer(caption, reply_markup=confirmation_button(ad['id']))


# ==================== E'LONNI KO'RIB CHIQISH ====================

@admin_router.callback_query(lambda c: c.data and c.data.startswith("review_accept:"))
async def elon_tasdiqlash_handler(call: types.CallbackQuery):
    elon_id = int(call.data.split(":")[1])
    user_id = set_elon_status(elon_id)

    if user_id:
        try:
            await call.bot.send_message(
                chat_id=user_id,
                text="✅ E'loningiz tasdiqlandi va tez orada botda e'lon qilinadi!"
            )
        except Exception:
            pass

    # Takroriy bosishning oldini olish uchun tugmalarni olib tashlash
    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await call.answer("Siz e'lonni tasdiqladingiz!")


@admin_router.callback_query(lambda c: c.data and c.data.startswith("review_reject:"))
async def elon_rad_etish_handler(call: types.CallbackQuery):
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

    # Takroriy bosishning oldini olish uchun tugmalarni olib tashlash
    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await call.answer("Siz e'lonni rad etdingiz!")


# ==================== FOYDALANUVCHI HOLATINI BOSHQARISH ====================

@admin_router.message(F.text == "🥸Foydalanuvchi buttonlari ochish")
async def user_menu_handler(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer(
        "Siz foydalanuvchi menyusini ochdingiz. Adminga qaytish uchun /admin_button ni bosing.",
        reply_markup=user_main_menu
    )


@admin_router.message(F.text == "🔃Foydalanuvchini holatini o'zgartirish")
async def change_user_status_handler(message: types.Message, state: FSMContext):
    if is_admin(message.from_user.id):
        await message.answer("Bu tugma foydalanuvchi holatini o'zgartiradi.\nYa'ni ban qiladi yoki bandan chiqaradi!")
        await message.answer("Foydalanuvchining user_id raqamini yozing:")
        await state.set_state(ChangeUserStatus.user_id)


@admin_router.message(ChangeUserStatus.user_id)
async def get_user_id_handler(message: types.Message, state: FSMContext):
    user_id = message.text

    if not user_id.isdigit():
        await message.answer("⚠️ Iltimos, faqat raqam yozing:")
        return

    if is_admin(user_id):
        await message.answer("⚠️ Adminning holatini o'zgartirib bo'lmaydi!")
        await state.clear()
        return

    user_data = get_user_status(int(user_id))
    if user_data:
        await state.update_data(user_id=user_id)
        await message.answer(
            f"{user_data[0]} - @{user_data[2]}",
            reply_markup=changeuserstatusbutton(user_data[1])
        )
        await state.set_state(ChangeUserStatus.new_status)
    else:
        await message.answer(f"🆔 {user_id} id ga ega foydalanuvchi topilmadi!")


@admin_router.callback_query(F.data == "ban❌", ChangeUserStatus.new_status)
async def user_ban_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    change_user_status(0, int(user_id))

    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await call.message.answer("❌ Foydalanuvchi ban qilindi!")
    await call.answer()
    await state.clear()


@admin_router.callback_query(F.data == "unban✅", ChangeUserStatus.new_status)
async def user_unban_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    change_user_status(1, int(user_id))

    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await call.message.answer("✅ Foydalanuvchi bandan chiqarildi!")
    await call.answer()
    await state.clear()
