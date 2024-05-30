import asyncio
import logging
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv

from config import TOKEN, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH
from bot import dp
from handlers.init import router, setup_handlers
from utils.db import create_pool, create_tables

# Загрузка переменных окружения
load_dotenv()

async def on_startup(app: web.Application) -> None:
    bot = Bot(TOKEN)
    dp.include_router(router)
    pool = await create_pool()  # Создание пула соединений с базой данных
    await create_tables(pool)  # Создание таблиц, если они еще не существуют
    setup_handlers(router, bot, pool)  # Передаем pool в setup_handlers
    await bot.set_webhook(WEBHOOK_URL)  # Устанавливаем вебхук
    app['bot'] = bot
    app['pool'] = pool

async def on_shutdown(app: web.Application) -> None:
    await app['bot'].delete_webhook()  # Удаляем вебхук при завершении работы
    await app['bot'].session.close()
    await app['pool'].close()

async def handle(request: web.Request) -> web.Response:
    bot = request.app['bot']
    update = await request.json()
    Dispatcher.set_current(dp)
    await dp.feed_update(bot, update)
    return web.Response()

async def index(request):
    return web.Response(text="Hello, this is the bot server!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    app = web.Application()
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    handler.register(app, path=WEBHOOK_PATH)
    app.router.add_get('/', index)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
