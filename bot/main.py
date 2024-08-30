import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from dotenv import load_dotenv

from product_service import format_product_info, get_product_info

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
REDIS_URL = os.getenv("REDIS_URL")
LIMITING_BOT_REQUESTS = int(os.getenv("LIMITING_BOT_REQUESTS"))
BOT_REDIS_HOST = os.getenv("BOT_REDIS_HOST")
BOT_REDIS_PORT = int(os.getenv("BOT_REDIS_PORT"))
BOT_REDIS_DB = int(os.getenv("BOT_REDIS_DB"))
BOT_REDIS_POOL_SIZE = int(os.getenv("BOT_REDIS_POOL_SIZE"))
BOT_REDIS_PREFIX = os.getenv("BOT_REDIS_PREFIX")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = RedisStorage2(
    host=BOT_REDIS_HOST,
    port=BOT_REDIS_PORT,
    db=BOT_REDIS_DB,
    pool_size=BOT_REDIS_POOL_SIZE,
    prefix=BOT_REDIS_PREFIX
)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Отправка сообщения при использовании команд `/start` or `/help`.
    """
    await message.reply(
        "Добро пожаловать!\n"
        "Введите ID товара на Wildberries, "
        "чтобы получить подробную информацию!\n"
        "Бот создан @gusoyn."
    )


async def hello_throttled(*args, **kwargs):
    message = args[0]
    await message.answer("Разрешено создавать не более 1 запроса в минуту.")


@dp.message_handler()
@dp.throttled(hello_throttled, rate=LIMITING_BOT_REQUESTS)
async def product_info_handler(message: types.Message):
    """Обработка запросов пользователей."""
    try:
        # Получаем ID товара из сообщения
        nm_id = int(message.text.strip())

        # Получаем информацию о товаре
        product_info = await get_product_info(nm_id)

        # Формируем человеко-читаемое сообщение
        response_message = format_product_info(product_info)

        # Отправляем ответ пользователю
        await message.answer(response_message, parse_mode="Markdown")

    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID товара.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
