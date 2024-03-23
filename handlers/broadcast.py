from aiogram.types import Message
from aiogram.filters import Command
from functools import partial
from utils.broadcast import send_broadcast_message

async def broadcast_command(message: Message, pool, bot):
    if message.from_user.id == 36677981:  # Замените YOUR_ADMIN_ID на ваш Telegram ID
        # Извлекаем текст после команды
        command_length = len('/broadcast')  # Длина команды
        broadcast_text = message.text[command_length:].strip()  # Обрезаем команду и пробелы
        if broadcast_text:
            await send_broadcast_message(bot, pool, broadcast_text)
            await message.answer("Сообщение успешно разослано.")
        else:
            await message.answer("Пожалуйста, укажите текст сообщения после команды /broadcast.")
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")

def register_broadcast_handlers(router, pool, bot):
    router.message.register(partial(broadcast_command, pool=pool, bot=bot), Command("broadcast"))