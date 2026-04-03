import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "ТВОЙ_ТОКЕН"
ADMIN_ID = 123456789  # ТВОЙ ID

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = {}

# Старт
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("🔥 Бот в деле!\n\nКоманды:\n/roll\n/who\n/top\n/boost")

# Очки за актив
@dp.message_handler()
async def activity(message: types.Message):
    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {"name": message.from_user.first_name, "points": 0}

    users[user_id]["points"] += 1

    text = message.text.lower()

    # авто-мемы
    if "слил" in text or "проиграл" in text:
        await message.reply("💀 Бывает брат, апнешься")

    if "нуб" in text:
        await message.reply("😂 Кто-то позвал меня?")

# /roll
@dp.message_handler(commands=['roll'])
async def roll(message: types.Message):
    num = random.randint(1, 100)
    await message.answer(f"🎲 Выпало: {num}")

# /who
@dp.message_handler(commands=['who'])
async def who(message: types.Message):
    members = list(users.keys())
    if members:
        random_user = random.choice(members)
        name = users[random_user]["name"]
        await message.answer(f"😂 Нуб дня: {name}")
    else:
        await message.answer("Пока никого нет")

# /top
@dp.message_handler(commands=['top'])
async def top(message: types.Message):
    if not users:
        await message.answer("Пока нет активности")
        return

    sorted_users = sorted(users.items(), key=lambda x: x[1]["points"], reverse=True)

    text = "🏆 Топ игроков:\n\n"
    for i, (user_id, data) in enumerate(sorted_users[:5], start=1):
        text += f"{i}. {data['name']} — {data['points']} pts\n"

    await message.answer(text)

# /boost
@dp.message_handler(commands=['boost'])
async def boost(message: types.Message):
    user = message.from_user

    text = f"🔥 Новая заявка на буст!\n\n👤 {user.first_name}\n🆔 {user.id}"

    await bot.send_message(ADMIN_ID, text)
    await message.answer("✅ Заявка отправлена!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)