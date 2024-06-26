import os
from dotenv import load_dotenv
import asyncpg

# Загрузить переменные окружения из файла .env
load_dotenv()

async def create_pool():
    dsn = os.getenv('DATABASE_URL')
    if not dsn:
        raise ValueError("Не удалось найти переменную среды DATABASE_URL")
    return await asyncpg.create_pool(dsn=dsn)

async def create_tables(pool):
    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL
            );
        ''')

async def add_user(pool, telegram_id, achievements=[], audio_codes=[], best_score=0):
    async with pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO users (telegram_id, achievements, audio_codes, best_score)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (telegram_id) DO NOTHING;
        ''', telegram_id, achievements, audio_codes, best_score)

async def update_best_score(pool, telegram_id, best_score):
    async with pool.acquire() as conn:
        await conn.execute('''
            UPDATE users SET best_score = $2 WHERE telegram_id = $1 AND best_score < $2;
        ''', telegram_id, best_score)

async def get_user(pool, telegram_id):
    async with pool.acquire() as conn:
        return await conn.fetchrow('''
            SELECT * FROM users WHERE telegram_id = $1;
        ''', telegram_id)

async def update_achievements(pool, telegram_id, achievements):
    async with pool.acquire() as conn:
        await conn.execute('''
            UPDATE users SET achievements = $2 WHERE telegram_id = $1;
        ''', telegram_id, achievements)

# Дополните другими функциями для работы с базой данных по мере необходимости.
