from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

async def send_support_info(message: Message):
    # Здесь вы можете указать свои контактные данные или инструкцию для связи
    support_message = "Если у вас возникли вопросы или предложения, пожалуйста, свяжитесь со мной: @klinok"
    await message.reply(support_message)


def register_support_handlers(router):
    router.message.register(send_support_info, Command('sup'))