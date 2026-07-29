from keyboards import admin_main_menu, user_main_menu
from config import is_admin


def main_menu_for(user_id):
    """Foydalanuvchi roliga mos asosiy menyu (admin yoki oddiy user)."""
    return admin_main_menu if is_admin(user_id) else user_main_menu
