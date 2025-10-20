from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio

TOKEN = "8453726026:AAE2xfG2oQGDzul1glzPcEdP4NDEAC1Kwlc"
WEBAPP_URL = "https://giftroulette1.netlify.app/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="🎁 Играть", web_app=WebAppInfo(url=WEBAPP_URL))
    await message.answer("Привет! Добро пожаловать в Gifts Battle 🎁", reply_markup=kb.as_markup(resize_keyboard=True))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
