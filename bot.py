import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import asyncio
import os

# ===============================
# Настройки
# ===============================

# ⚙️ Вставь свой токен от BotFather
BOT_TOKEN = os.getenv("8453726026:AAE2xfG2oQGDzul1glzPcEdP4NDEAC1Kwlc")

# 🌐 URL твоего сайта / Web App (например Render или Netlify)
WEBAPP_URL = os.getenv("https://giftroulette1.netlify.app/")

# ===============================
# Настройка логов
# ===============================
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# ===============================
# Команды
# ===============================
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    """
    Отправляет приветствие и кнопку для открытия Web App.
    """
    keyboard = InlineKeyboardMarkup()
    webapp_button = InlineKeyboardButton(
        text="🎁 Открыть Gifts Battle",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    keyboard.add(webapp_button)

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Добро пожаловать в *Gifts Battle*! 🎁\n"
        "Нажми на кнопку ниже, чтобы открыть игру:",
        parse_mode="Markdown",
        reply_markup=keyboard
    )


@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.answer(
        "⚙️ Доступные команды:\n"
        "/start — начать игру 🎮\n"
        "/help — справка 📖"
    )


# ===============================
# Обработка сообщений от WebApp
# ===============================
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def webapp_message(message: types.Message):
    """
    Получает данные из WebApp (например, очки, выбор подарка и т.п.)
    """
    data = message.web_app_data.data  # данные JSON-строкой
    logging.info(f"📦 Получены данные из WebApp: {data}")
    await message.answer(f"✅ Получены данные: {data}")


# ===============================
# Основной запуск
# ===============================
async def main():
    logging.info("🚀 Gifts Battle Bot запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("⛔️ Бот остановлен.")
