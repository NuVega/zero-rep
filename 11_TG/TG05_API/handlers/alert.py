from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from ws import btc_watchdog  # импортируем наш модуль с WebSocket

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    btc_watchdog.chat_id = message.chat.id  # сохраняем ID чата
    print(f"[INFO] chat_id установлен: {btc_watchdog.chat_id}")

    await message.answer(
        "📡 Бот следит за <b>BTCUSDT</b> свечами (1ч и 1м).\n"
        "Ты будешь получать уведомления о резких движениях цены!\n"
        "\nЕсли хочешь узнать цену и объемы по /btc или /eth, отправь нужную команду"
    )
