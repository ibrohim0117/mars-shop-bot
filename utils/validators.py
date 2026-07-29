import re


def validate_phone_number(phone_number):
    if not phone_number:
        return False
    pattern = r"^\+998\d{9}$|^\d{9}$"
    return bool(re.match(pattern, phone_number))


def normalize_phone(phone_number):
    """Telefon raqamini bazaga yagona formatda saqlash uchun keltiradi: 901234567 (9 xonali).

    Masalan: '+998901234567' yoki '998901234567' -> '901234567'
    """
    if not phone_number:
        return ""
    digits = re.sub(r"\D", "", phone_number)  # faqat raqamlarni qoldiradi
    if len(digits) == 12 and digits.startswith("998"):
        return digits[3:]
    return digits


def validate_price(price):
    """Narx faqat raqamlardan iborat bo'lishi kerak (bo'sh joylarga ruxsat beriladi)."""
    if not price:
        return False
    cleaned = price.replace(" ", "")
    return cleaned.isdigit()
