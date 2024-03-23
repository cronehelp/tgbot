from functools import partial
import random

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.start import cmd_start
from utils.db import add_user
from utils.quiz_utils import get_random_question, quiz_questions, send_new_question, user_correct_answers, \
    user_questions_count, user_asked_questions


async def register_user(message: Message):
    user_id = message.from_user.id
    # Регистрация пользователя в БД
    await add_user(user_id, ['achievement1'], ['audio1'])

async def start_quiz(bot, message: Message):

    # Выбираем случайный вопрос из списка
    question = random.choice(quiz_questions)

    # Делаем клавиатуру

    builder = InlineKeyboardBuilder()

    for answer in question['answers']:
        # Для каждого ответа создаем кнопку и добавляем ее в клавиатуру
        builder.button(text=answer, callback_data=answer)

    # Получаем готовую инлайн-клавиатуру
    keyboard = builder.as_markup()

    # Отправляем аудиофайл и клавиатуру с вариантами ответов
    await bot.send_voice(chat_id=message.chat.id, voice=question['audio'], reply_markup=keyboard)

async def handle_callback_query(bot, callback_query: CallbackQuery, pool):
    # Получаем данные вопроса, чтобы определить правильный ответ
    question = next((q for q in quiz_questions if callback_query.data in q["answers"]), None)

    if question:
        if callback_query.data == question["correct"]:
            await bot.send_sticker(callback_query.message.chat.id,
                                   'CAACAgIAAxkBAAEDqltl1orYpI5Y4QZuIFcicdSM6QWRswACDAEAAh8BTBVU4NYLtR3iMTQE')
            # Увеличиваем счетчик правильных ответов
            user_correct_answers[callback_query.from_user.id] = user_correct_answers.get(callback_query.from_user.id,
                                                                                         0) + 1
        else:
            await bot.send_sticker(callback_query.message.chat.id,
                                   'CAACAgIAAxkBAAEDql9l1osB8CykQIniuyv7g4etYXpvtgAC-AADHwFMFW6QRJDhlznONAQ')

    # Удаляем клавиатуру с вопросом
    await callback_query.message.edit_reply_markup(reply_markup=None)

    # После ответа отправляем новый вопрос
    await send_new_question(bot, callback_query.message.chat.id, pool)

async def restart_quiz(message: Message, pool, bot):
    # Логика перезапуска викторины
    user_id = message.from_user.id
    # Сбрасываем данные пользователя
    user_questions_count[user_id] = 0
    user_asked_questions[user_id] = set()
    user_correct_answers[user_id] = 0
    # Предлагаем начать викторину заново
    await cmd_start(message, pool)


def register_quiz_handlers(router, pool, bot):
    router.message.register(partial(start_quiz, bot), Command("quiz"))
    router.callback_query.register(partial(handle_callback_query, bot, pool=pool))
    router.message.register(partial(restart_quiz, pool=pool, bot=bot), Command("restart"))
