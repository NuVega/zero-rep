import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import alert, volume
from ws import btc_watchdog

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(alert.router)
dp.include_router(volume.router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    # запускаем фоновую задачу
    asyncio.create_task(btc_watchdog.run_btc_watchdog(bot))
    asyncio.create_task(btc_watchdog.run_btc_watchdog_1m(bot))

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())