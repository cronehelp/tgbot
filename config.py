from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
YOUR_DOMAIN = os.getenv("YOUR_DOMAIN")
YOUR_WEBHOOK_PATH = os.getenv("YOUR_WEBHOOK_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")