import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if TOKEN is None:
    raise ValueError("Не удалось найти токен бота. Убедитесь, что вы правильно задали переменную среды TELEGRAM_BOT_TOKEN.")
