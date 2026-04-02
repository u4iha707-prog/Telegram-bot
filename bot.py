import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

import os
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="О нас")],
        [KeyboardButton(text="Услуги")],
        [KeyboardButton(text="Контакты")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Добро пожаловать!\n\nЯ помогу вам узнать о наших услугах.\nВыберите ниже 👇", reply_markup=kb)

@dp.message()
async def menu(message: types.Message):
    if message.text == "О нас":
        await message.answer("Мы делаем ботов 😎")

    elif message.text == "Услуги":
        await message.answer("Боты, автоматизация, помощь")

    elif message.text == "Контакты":
        await message.answer("Напиши: @твой_ник/nИли WhatsApp: +123456789")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())