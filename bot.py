import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 5585690159  # твой ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище заявок
user_data = {}

# Клавиатура
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📌 О нас")],
        [KeyboardButton(text="💼 Услуги")],
        [KeyboardButton(text="💰 Цены")],
        [KeyboardButton(text="📞 Контакты")],
        [KeyboardButton(text="📝 Оставить заявку")]
    ],
    resize_keyboard=True
)

# Старт
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Рад тебя видеть\n\n"
        "Я помогаю автоматизировать бизнес с помощью Telegram-ботов 🤖\n\n"
        "С ботом ты сможешь:\n"
        "— принимать заявки 24/7\n"
        "— экономить время\n"
        "— увеличивать прибыль 💰\n\n"
        "👇 Выбери, что тебя интересует",
        reply_markup=kb
    )

# Основная логика
@dp.message()
async def menu(message: types.Message):
    user_id = message.from_user.id

    # О нас
    if message.text == "📌 О нас":
        await message.answer("🚀 Мы создаём Telegram-ботов под задачи бизнеса")

    # Услуги
    elif message.text == "💼 Услуги":
        await message.answer(
            "💼 Наши услуги:\n\n"
            "— Боты для бизнеса\n"
            "— Автоматизация\n"
            "— Приём заявок\n"
            "— Интеграции"
        )

    # Цены
    elif message.text == "💰 Цены":
        await message.answer(
            "💰 Примерные цены:\n\n"
            "— Простой бот: от 50$\n"
            "— Средний: 100-200$\n"
            "— Сложный: от 300$\n\n"
            "📩 Напиши, и скажу точнее"
        )

    # Контакты
    elif message.text == "📞 Контакты":
        await message.answer(
            "📞 Связь:\n\n"
            "Telegram: @твой_ник\n"
            "WhatsApp: +123456789"
        )

    # НАЧАЛО ЗАЯВКИ
    elif message.text == "📝 Оставить заявку":
        user_data[user_id] = {"step": "name"}
        await message.answer("✍️ Напиши своё имя:")

    # ОБРАБОТКА ЗАЯВКИ
    elif user_id in user_data:

        if user_data[user_id]["step"] == "name":
            user_data[user_id]["name"] = message.text
            user_data[user_id]["step"] = "request"
            await message.answer("📋 Опиши задачу:")

        elif user_data[user_id]["step"] == "request":
            name = user_data[user_id]["name"]
            request = message.text

            text = (
                f"🔥 Новая заявка!\n\n"
                f"👤 Имя: {name}\n"
                f"🆔 ID: {user_id}\n"
                f"📩 Запрос: {request}"
            )

            # отправка тебе
            await bot.send_message(ADMIN_ID, text)

            await message.answer("✅ Заявка отправлена! Я скоро свяжусь с тобой")

            del user_data[user_id]

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())