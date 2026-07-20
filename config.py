import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

# .env da bir nechta admin vergul bilan yoziladi: ADMINS=123456789,987654321
ADMINS = [
    int(admin_id.strip())
    for admin_id in os.getenv("ADMINS", "").split(",")
    if admin_id.strip().isdigit()
]


def is_admin(user_id):
    """Berilgan user_id adminlar ro'yxatida bormi?"""
    try:
        return int(user_id) in ADMINS
    except (TypeError, ValueError):
        return False
