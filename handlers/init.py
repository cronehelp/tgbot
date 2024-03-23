from aiogram import Router

from .broadcast import register_broadcast_handlers
from .start import register_start_handlers
from .quiz import register_quiz_handlers
from .media import register_media_handlers
from .support import register_support_handlers
from .statistics import register_statistics_handlers

router = Router()

def setup_handlers(router, bot, pool):
    register_start_handlers(router, pool)  # Передаем pool в register_start_handlers
    register_quiz_handlers(router, pool, bot)  # Передаем pool и bot в register_quiz_handlers
    register_media_handlers(router)  # Передаем router в register_media_handlers
    register_support_handlers(router)  # Передаем router в register_support_handlers
    register_statistics_handlers(router, pool)
    register_broadcast_handlers(router, pool, bot)




