from aiogram.types import Message
from aiogram.filters import Command
from functools import partial

async def send_statistics(message: Message, pool):
    user_id = message.from_user.id
    async with pool.acquire() as conn:
        best_score = await conn.fetchval('''
            SELECT best_score FROM users WHERE telegram_id = $1;
        ''', user_id)
        await message.answer(f"Ваш лучший результат: {best_score} ответов.")

def register_statistics_handlers(router, pool):
    router.message.register(partial(send_statistics, pool=pool), Command("stat"))
