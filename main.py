import asyncio
import os
import threading
import http.server
import socketserver
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

TOKEN = "7299128795:AAG3WCduCnh8RQL2_Le1yzUdshMTCSubADc"
MENU_URL = "https://krisrush111.github.io/em-rush/"
OTHER_BOT_TOKEN = "7990654679:AAGD6i5kLTpFZ2IIXCY2f-YyUUBNxWQc33M"  # Токен другого бота
OTHER_BOT_CHAT_ID = "5574610358"  # ID чата другого бота

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

# Функция для запуска фейкового HTTP-сервера
def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Фейковый сервер запущен на порту {port}")
        httpd.serve_forever()

# Запускаем сервер в отдельном потоке
threading.Thread(target=keep_alive, daemon=True).start()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id

    # Уведомление в другой бот с именем пользователя в формате @username
    other_bot = Bot(token=OTHER_BOT_TOKEN)
    await other_bot.send_message(OTHER_BOT_CHAT_ID, f'Новый пользователь: @{message.from_user.username} (ID: {user_id})')

    # Создание inline-клавиатуры
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=" 🦝 play in one click 🦝", web_app=types.WebAppInfo(url=f"{MENU_URL}?userId={user_id}"))],
        [InlineKeyboardButton(text="Перейти на канал", url="https://t.me/Empire_Rush")],
    ])

    await message.answer(
        f'<b>HI, {user_name}! Welcome to Empire Rush!</b> '
        'Click on the raccoon to collect RCCoin. Grow your '
        'businesses — buy, upgrade, and earn more. Complete '
        'missions to unlock new opportunities and speed up your '
        'progress. 🌚🚀\n\n'
        'Invite your friends — it’s more fun and rewarding together!'
        'Team up, take on challenges, and rise to the top of Empire '
        'Rush as a group! 🔥💫\n\n',
        reply_markup=keyboard
    )


@dp.message(F.text)
async def unknown_command(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=" 🦝 play in one click 🦝",
            web_app=types.WebAppInfo(url=f"{MENU_URL}?userId={user_id}")
        )],
        [InlineKeyboardButton(
            text="Перейти на канал",
            url="https://t.me/Empire_Rush"
        )],
    ])

    await message.answer(
        f'<b>HI, {user_name}! Welcome to Empire Rush!</b> '
        'Click on the raccoon to collect RCCoin. Grow your '
        'businesses — buy, upgrade, and earn more. Complete '
        'missions to unlock new opportunities and speed up your '
        'progress. 🌚🚀\n\n'
        'Invite your friends — it’s more fun and rewarding together! '
        'Team up, take on challenges, and rise to the top of Empire '
        'Rush as a group! 🔥💫\n\n',
        reply_markup=keyboard
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
