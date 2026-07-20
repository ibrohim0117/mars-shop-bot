from .commands import command_router
from .user import user_router
from .admin import admin_router

__all__ = ["command_router", "user_router", "admin_router"]
