import asyncio
import logging
import sys
from aiogram import Bot

from config import TOKEN
from bot import dp
from handlers.init import router

from handlers.init import setup_handlers
from utils.db import create_pool, create_tables
from utils.broadcast import send_broadcast_message

async def main() -> None:
    bot = Bot(TOKEN)
    dp.include_router(router)
    pool = await create_pool()  # Создание пула соединений с базой данных
    await create_tables(pool)  # Создание таблиц, если они еще не существуют
    setup_handlers(router, bot, pool)  # Передаем pool в setup_handlers
    await dp.start_polling(bot)  # Запуск polling
    await pool.close()  # Завершение работы с пулом соединений

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())