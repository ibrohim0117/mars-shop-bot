from aiogram import Router, types, F

from database import set_elon_status, reject_elon
from keyboards import user_main_menu

admin_router = Router()


@admin_router.callback_query(lambda c: c.data and c.data.startswith("review_accept:"))
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

    # Takroriy bosishning oldini olish uchun tugmalarni olib tashlash
    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await call.answer("Siz e'lonni tasdiqladingiz!")


@admin_router.callback_query(lambda c: c.data and c.data.startswith("review_reject:"))
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

    # Takroriy bosishning oldini olish uchun tugmalarni olib tashlash
    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await call.answer("Siz e'lonni rad etdingiz!")


@admin_router.message(F.text == "🥸Foydalanuvchi buttonlari ochish")
async def user_button_handler(message: types.Message):
    await message.answer(
        "Siz user menu ni ochdiz adminga qaytish uchun /admin_button ni bosing",
        reply_markup = user_main_menu
        )
