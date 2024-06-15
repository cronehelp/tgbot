import asyncio
import logging
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from config import TOKEN, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH
from bot import dp
from handlers.init import router, setup_handlers
from utils.db import create_pool, create_tables

load_dotenv()

async def on_startup(app: web.Application = None) -> None:
    bot = Bot(TOKEN)
    dp.include_router(router)
    try:
        pool = await create_pool()  # Создание пула соединений с базой данных
        await create_tables(pool)  # Создание таблиц, если они еще не существуют
        setup_handlers(router, bot, pool)  # Передаем pool в setup_handlers
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        return

    if os.getenv('ENV') == 'production':
        await bot.set_webhook(WEBHOOK_URL)  # Устанавливаем вебхук на сервере

    if app:
        app['bot'] = bot
        app['pool'] = pool

async def on_shutdown(app: web.Application = None) -> None:
    if app:
        await app['bot'].delete_webhook()  # Удаляем вебхук при завершении работы
        await app['bot'].session.close()
        await app['pool'].close()

async def handle(request: web.Request) -> web.Response:
    bot = request.app['bot']
    update = await request.json()
    await dp.process_update(update)
    return web.Response()

async def index(request):
    return web.Response(text="Hello, this is the bot server!")

async def start_polling():
    bot = Bot(TOKEN)
    dp.include_router(router)
    try:
        pool = await create_pool()  # Создание пула соединений с базой данных
        await create_tables(pool)  # Создание таблиц, если они еще не существуют
        setup_handlers(router, bot, pool)  # Передаем pool в setup_handlers
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        return

    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    if os.getenv('ENV') == 'production':
        app = web.Application()
        app.router.add_post(WEBHOOK_PATH, handle)
        app.router.add_get('/', index)
        app.on_startup.append(on_startup)
        app.on_shutdown.append(on_shutdown)
        web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
    else:
        asyncio.run(start_polling())
