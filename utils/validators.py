import re


def validate_phone_number(phone_number):
    pattern = r"^\+998\d{9}$|^\d{9}$"
    match = re.match(pattern, phone_number)
    if match:
        return True
    else:
        return False


def validate_price(price):
    """Narx faqat raqamlardan iborat bo'lishi kerak (bo'sh joylarga ruxsat beriladi)."""
    if not price:
        return False
    cleaned = price.replace(" ", "")
    return cleaned.isdigit()
