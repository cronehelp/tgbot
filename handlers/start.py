
import logging
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from utils.db import add_user  # Импортируем функцию добавления пользователя


async def cmd_start(msg: Message, pool):
    user_id = msg.from_user.id
    logging.info(f"Добавление пользователя с ID: {msg.from_user.id}")
    try:
        # Добавляем пользователя в базу данных
        await add_user(pool, msg.from_user.id, ['achievement1'], ['audio1'])
        logging.info("Пользователь успешно добавлен.")
    except Exception as e:
        logging.error(f"Ошибка при добавлении пользователя: {e}")
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Начать викторину", callback_data="quiz"))
    keyboard = builder.as_markup()
    await msg.answer("Добро пожаловать! Готовы начать викторину?", reply_markup=keyboard)


def register_start_handlers(router, pool):
    async def start_handler(msg):
        await cmd_start(msg, pool)
    router.message.register(start_handler, Command(commands=['start', 'run']))
