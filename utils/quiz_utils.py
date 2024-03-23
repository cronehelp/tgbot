import json
import random
import logging

from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.db import update_best_score


# Функция для загрузки вопросов из файла
def load_quiz_questions(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Загружаем вопросы в начале скрипта
quiz_questions = load_quiz_questions('quiz_questions.json')

# Функция для получения случайного вопроса
def get_random_question(quiz_questions):
    return random.choice(quiz_questions)

# Глобальные словари для отслеживания состояния викторины для каждого пользователя
user_questions_count = {}
user_asked_questions = {}
user_correct_answers = {}

# Функция для отправки нового вопроса
async def send_new_question(bot, chat_id, pool):
    user_id = chat_id  # В Telegram chat_id эквивалентен user_id для личных чатов
    # Проверяем, не превысил ли пользователь лимит вопросов
    if user_questions_count.get(chat_id, 0) >= 11:
        correct_answers = user_correct_answers.get(chat_id, 0)
        # Обновляем лучший результат пользователя
        await update_best_score(pool, user_id, correct_answers)
        # Выводим сообщение о результате викторины
        message = "Викторина окончена. "
        if correct_answers > 8:
            message += "Отличный результат! Вы правильно ответили на большинство вопросов. Нажмите /restart, чтобы начать заново."
        elif correct_answers >= 5:
            message += "Неплохо! Но есть куда стремиться. Нажмите /restart, чтобы начать заново."
        # else:
        elif correct_answers < 5:
            message += "Попробуйте еще раз. Уверен, вы сможете лучше! Нажмите /restart, чтобы начать заново."


        await bot.send_message(chat_id, message)
        return  # Прекращаем отправку вопросов



    # Получаем список уже заданных вопросов для пользователя
    asked_questions = user_asked_questions.get(chat_id, set())

    # Выбираем новый вопрос, который ещё не был задан
    new_questions = [q for q in quiz_questions if q['audio'] not in asked_questions]
    if not new_questions:
        await bot.send_message(chat_id,
                               "Вы ответили на все вопросы! Викторина окончена. Нажмите /restart, чтобы начать заново.")
        return

    question = random.choice(new_questions)

    asked_questions.add(question['audio'])
    user_asked_questions[chat_id] = asked_questions

    builder = InlineKeyboardBuilder()
    for answer in question['answers']:
        builder.button(text=answer, callback_data=answer)
    keyboard = builder.as_markup()
    await bot.send_voice(chat_id=chat_id, voice=question['audio'], reply_markup=keyboard)

    # Увеличиваем счётчик вопросов для пользователя
    user_questions_count[chat_id] = user_questions_count.get(chat_id, 0) + 1

    # Обработчик нажатий на кнопки инлайн-клавиатуры


async def handle_callback_query(bot, callback_query: CallbackQuery):
    logging.info(f"Пользователь {callback_query.from_user.id} выбрал ответ: {callback_query.data}")
    # Получаем данные вопроса, чтобы определить правильный ответ
    question = next((q for q in quiz_questions if callback_query.data in q["answers"]), None)

    if question:
        if callback_query.data == question["correct"]:
            await bot.send_sticker(callback_query.message.chat.id,
                                   'CAACAgIAAxkBAAEDqltl1orYpI5Y4QZuIFcicdSM6QWRswACDAEAAh8BTBVU4NYLtR3iMTQE')
            # Увеличиваем счетчик правильных ответов
            user_correct_answers[callback_query.from_user.id] = user_correct_answers.get(callback_query.from_user.id,
                                                                                         0) + 1
            logging.info(
                f"Это правильный ответ! Текущее количество правильных ответов: {user_correct_answers[callback_query.from_user.id]}")
        else:
            await bot.send_sticker(callback_query.message.chat.id,
                                   'CAACAgIAAxkBAAEDql9l1osB8CykQIniuyv7g4etYXpvtgAC-AADHwFMFW6QRJDhlznONAQ')
            logging.info("Это неправильный ответ.")

    # Удаляем клавиатуру с вопросом
    await callback_query.message.edit_reply_markup(reply_markup=None)
    logging.info(f"Отправляем новый вопрос пользователю {callback_query.from_user.id}")
    # После ответа отправляем новый вопрос
    await send_new_question(bot, callback_query.message.chat.id)
