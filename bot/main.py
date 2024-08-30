import logging
import os
import aioredis

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from dotenv import load_dotenv

from product_service import format_product_info, get_product_info

load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
API_TOKEN = os.getenv("BOT_TOKEN")
REDIS_URL = os.getenv("REDIS_URL")
LIMITING_BOT_REQUESTS = int(os.getenv("LIMITING_BOT_REQUESTS"))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = RedisStorage2('localhost', 6379, db=5, pool_size=10, prefix='my_fsm_key')
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Добро пожаловать!\n"
                        "Введите ID товара на Wildberries, "
                        "чтобы получить подробную информацию!\n"
                        "Бот создан @gusoyn.")


async def hello_throttled(*args, **kwargs):
    message = args[0]
    await message.answer("Разрешено создавать не более 1 запроса в минуту.")


@dp.message_handler()
@dp.throttled(hello_throttled, rate=LIMITING_BOT_REQUESTS)
async def product_info_handler(message: types.Message):
    try:
        # Получаем ID товара из сообщения
        nm_id = int(message.text.strip())

        # Получаем информацию о товаре
        product_info = await get_product_info(nm_id)

        # Формируем человекочитаемое сообщение
        response_message = format_product_info(product_info)

        # Отправляем ответ пользователю
        await message.answer(response_message, parse_mode="Markdown")

    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID товара.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

