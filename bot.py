import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import executor

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 5585690159

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add("🚀 Клиенты", "💼 Возможности")
kb.add("💰 Цена", "📩 Связь")
kb.add("📝 Заявка")

user_data = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("👋 Привет! Выбери:", reply_markup=kb)

@dp.message_handler()
async def menu(message: types.Message):
    user_id = message.from_user.id

    if message.text == "📝 Заявка":
        user_data[user_id] = {"step": "name"}
        await message.answer("Имя:")

    elif user_id in user_data:
        if user_data[user_id]["step"] == "name":
            user_data[user_id]["name"] = message.text
            user_data[user_id]["step"] = "task"
            await message.answer("Задача:")

        elif user_data[user_id]["step"] == "task":
            await bot.send_message(
                ADMIN_ID,
                f"Заявка:\n{user_data[user_id]['name']}\n{message.text}"
            )
            await message.answer("Отправлено")
            del user_data[user_id]

def run_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    executor.start_polling(dp, skip_updates=True)