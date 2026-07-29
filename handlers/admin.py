import asyncio

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from database import (
    set_elon_status, reject_elon, get_user_status, change_user_status,
    get_pending_elonlar, get_elon_status, get_all_user_ids
)
from keyboards import (
    user_main_menu, admin_main_menu, reklama_menu, Ha_Yoq_menu, cancel_menu,
    changeuserstatusbutton, confirmation_button,
    REKLAMA_MATN, REKLAMA_RASM, REKLAMA_VIDEO
)
from states import ChangeUserStatus, Reklama
from config import is_admin
from middlewares import invalidate_ban_cache

admin_router = Router()


# ==================== KUTILAYOTGAN E'LONLAR ====================

@admin_router.message(F.text == "⏳ Kutilayotgan e'lonlar", StateFilter(None))
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
        await asyncio.sleep(0.05)  # Telegram cheklovlariga tushmaslik uchun


# ==================== E'LONNI KO'RIB CHIQISH ====================

async def _remove_buttons(call: types.CallbackQuery):
    """Xabardagi inline tugmalarni olib tashlaydi (takroriy bosishga qarshi)."""
    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass


@admin_router.callback_query(lambda c: c.data and c.data.startswith("review_accept:"))
async def elon_tasdiqlash_handler(call: types.CallbackQuery):
    elon_id = int(call.data.split(":")[1])

    status = get_elon_status(elon_id)
    # Boshqa admin allaqachon ko'rib chiqqan bo'lishi mumkin
    if status is None:
        await _remove_buttons(call)
        await call.answer("Bu e'lon allaqachon rad etilgan yoki o'chirilgan.", show_alert=True)
        return
    if status == 1:
        await _remove_buttons(call)
        await call.answer("Bu e'lon allaqachon tasdiqlangan.", show_alert=True)
        return

    user_id = set_elon_status(elon_id)
    if user_id:
        try:
            await call.bot.send_message(
                chat_id=user_id,
                text="✅ E'loningiz tasdiqlandi va tez orada botda e'lon qilinadi!"
            )
        except Exception:
            pass

    await _remove_buttons(call)
    await call.answer("Siz e'lonni tasdiqladingiz!")


@admin_router.callback_query(lambda c: c.data and c.data.startswith("review_reject:"))
async def elon_rad_etish_handler(call: types.CallbackQuery):
    elon_id = int(call.data.split(":")[1])

    # Boshqa admin allaqachon rad etib, o'chirib yuborgan bo'lishi mumkin
    if get_elon_status(elon_id) is None:
        await _remove_buttons(call)
        await call.answer("Bu e'lon allaqachon ko'rib chiqilgan.", show_alert=True)
        return

    user_id = reject_elon(elon_id)
    if user_id:
        try:
            await call.bot.send_message(
                chat_id=user_id,
                text="❌ Afsuski, e'loningiz admin tomonidan rad etildi."
            )
        except Exception:
            pass

    await _remove_buttons(call)
    await call.answer("Siz e'lonni rad etdingiz!")


# ==================== FOYDALANUVCHI HOLATINI BOSHQARISH ====================

@admin_router.message(F.text == "🥸Foydalanuvchi buttonlari ochish", StateFilter(None))
async def user_menu_handler(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer(
        "Siz foydalanuvchi menyusini ochdingiz. Adminga qaytish uchun /admin_button ni bosing.",
        reply_markup=user_main_menu
    )


@admin_router.message(F.text == "🔃Foydalanuvchini holatini o'zgartirish", StateFilter(None))
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
    invalidate_ban_cache(user_id)  # ban darhol kuchga kirsin

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
    invalidate_ban_cache(user_id)  # bandan chiqarish darhol kuchga kirsin

    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await call.message.answer("✅ Foydalanuvchi bandan chiqarildi!")
    await call.answer()
    await state.clear()


# ==================== REKLAMA XIZMATI ====================

@admin_router.message(F.text == "🔥Reklama xizmati", StateFilter(None))
async def reklama_start_handler(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await message.answer("Qanday reklama yubormoqchisiz?", reply_markup=reklama_menu)
    await state.set_state(Reklama.turi)


@admin_router.message(Reklama.turi, F.text == REKLAMA_MATN)
async def reklama_matn_start_handler(message: types.Message, state: FSMContext):
    await message.answer("Reklama matnini yuboring:", reply_markup=cancel_menu)
    await state.set_state(Reklama.matn)


@admin_router.message(Reklama.turi, F.text == REKLAMA_RASM)
async def reklama_rasm_start_handler(message: types.Message, state: FSMContext):
    await message.answer("Rasmni yuboring (izoh ixtiyoriy):", reply_markup=cancel_menu)
    await state.set_state(Reklama.rasm)


@admin_router.message(Reklama.turi, F.text == REKLAMA_VIDEO)
async def reklama_video_start_handler(message: types.Message, state: FSMContext):
    await message.answer("Videoni yuboring (izoh ixtiyoriy):", reply_markup=cancel_menu)
    await state.set_state(Reklama.video)


@admin_router.message(Reklama.turi)
async def reklama_turi_invalid_handler(message: types.Message):
    await message.answer("⚠️ Iltimos, quyidagi tugmalardan birini tanlang:", reply_markup=reklama_menu)


# --- Kontentni qabul qilish va tasdiq so'rash ---

async def _reklama_tasdiq_sorash(message: types.Message, state: FSMContext):
    """Qabul qilingan reklama xabarini eslab qoladi va tasdiq so'raydi."""
    await state.update_data(
        content_chat_id=message.chat.id,
        content_message_id=message.message_id
    )
    await message.answer(
        "Yuqoridagi reklama barcha foydalanuvchilarga yuborilsinmi? (Ha/Yo'q)",
        reply_markup=Ha_Yoq_menu
    )
    await state.set_state(Reklama.tasdiq)


@admin_router.message(Reklama.matn, F.text)
async def reklama_matn_handler(message: types.Message, state: FSMContext):
    await _reklama_tasdiq_sorash(message, state)


@admin_router.message(Reklama.matn)
async def reklama_matn_invalid_handler(message: types.Message):
    await message.answer("⚠️ Iltimos, matn yuboring.", reply_markup=cancel_menu)


@admin_router.message(Reklama.rasm, F.photo)
async def reklama_rasm_handler(message: types.Message, state: FSMContext):
    await _reklama_tasdiq_sorash(message, state)


@admin_router.message(Reklama.rasm)
async def reklama_rasm_invalid_handler(message: types.Message):
    await message.answer("⚠️ Iltimos, rasm yuboring.", reply_markup=cancel_menu)


@admin_router.message(Reklama.video, F.video)
async def reklama_video_handler(message: types.Message, state: FSMContext):
    await _reklama_tasdiq_sorash(message, state)


@admin_router.message(Reklama.video)
async def reklama_video_invalid_handler(message: types.Message):
    await message.answer("⚠️ Iltimos, video yuboring.", reply_markup=cancel_menu)


# --- Tasdiqlash va tarqatish ---

@admin_router.message(Reklama.tasdiq, F.text == "Ha")
async def reklama_yuborish_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    from_chat = data.get('content_chat_id')
    msg_id = data.get('content_message_id')
    await state.clear()

    if not from_chat or not msg_id:
        await message.answer("❌ Reklama ma'lumoti topilmadi.", reply_markup=admin_main_menu)
        return

    user_ids = get_all_user_ids()
    await message.answer(
        f"📤 Reklama {len(user_ids)} ta foydalanuvchiga yuborilmoqda...",
        reply_markup=admin_main_menu
    )

    yuborildi = 0
    xato = 0
    for uid in user_ids:
        try:
            await message.bot.copy_message(chat_id=uid, from_chat_id=from_chat, message_id=msg_id)
            yuborildi += 1
        except Exception:
            # Foydalanuvchi botni bloklagan yoki chatni o'chirgan bo'lishi mumkin
            xato += 1
        await asyncio.sleep(0.05)  # Telegram cheklovlariga tushmaslik uchun

    await message.answer(
        f"✅ Reklama yuborildi!\n\n📬 Yetkazildi: {yuborildi} ta\n❌ Yuborilmadi: {xato} ta"
    )


@admin_router.message(Reklama.tasdiq)
async def reklama_bekor_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Reklama bekor qilindi.", reply_markup=admin_main_menu)
