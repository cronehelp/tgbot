from aiogram import F
from aiogram.types import Message

async def message_handler_audio(message: Message):
    # Логика обработки аудио
    await message.reply("Ваше id audio: " + message.audio.file_id)

async def message_handler_photo(message: Message):
    # Логика обработки фото
    await message.reply("Вы прислали фото или картинку, спасибо. Но здесь у нас викторина, "
                        "нажмите /restart чтобы начать игру "
                        "или /sup, чтобы связаться с нами")

async def message_handler_sticker(message: Message):
    # Логика обработки стикеров
    await message.reply("Вы прислали стикер, спасибо. Но здесь у нас викторина, "
                        "нажмите /restart начать игру "
                        "или /sup, чтобы связаться с нами")

def register_media_handlers(router):
    router.message.register(message_handler_audio, F.audio)
    router.message.register(message_handler_photo, F.photo)
    router.message.register(message_handler_sticker, F.sticker)
