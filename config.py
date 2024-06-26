from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
YOUR_DOMAIN = os.getenv("YOUR_DOMAIN")
YOUR_WEBHOOK_PATH = os.getenv("YOUR_WEBHOOK_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if TOKEN is None:
    raise ValueError("Не удалось найти токен бота. Убедитесь, что вы правильно задали переменную среды TELEGRAM_BOT_TOKEN.")

# Webhook settings
YOUR_DOMAIN = os.getenv("YOUR_DOMAIN")
YOUR_WEBHOOK_PATH = os.getenv("YOUR_WEBHOOK_PATH")

if YOUR_DOMAIN is None or YOUR_WEBHOOK_PATH is None:
    raise ValueError("Не удалось найти настройки вебхуков. Убедитесь, что вы правильно задали переменные среды YOUR_DOMAIN и YOUR_WEBHOOK_PATH.")

WEBHOOK_URL = f"https://{YOUR_DOMAIN}/{YOUR_WEBHOOK_PATH}"
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv("PORT", 3000))
WEBHOOK_PATH = f'/{YOUR_WEBHOOK_PATH}'

