async def send_broadcast_message(bot, pool, message_text):
    async with pool.acquire() as conn:
        users = await conn.fetch('SELECT telegram_id FROM users;')
        for user in users:
            try:
                await bot.send_message(user['telegram_id'], message_text)
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user['telegram_id']}: {e}")
