from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from binance.spot import Spot
from datetime import datetime, timedelta
from statistics import mean

router = Router()
client = Spot()

def get_volume_ratio(symbol: str):
    try:
        now = datetime.utcnow()
        today_str = now.strftime("%Y-%m-%d")
        hour = now.hour

        # Получаем 30 дней часовых свечей
        klines = client.klines(symbol.upper(), "1h", limit=24 * 30)

        # Разбиваем свечи по дням
        daily_volumes = {}

        for k in klines:
            ts = datetime.utcfromtimestamp(k[0] // 1000)
            day = ts.strftime("%Y-%m-%d")
            if ts.hour >= hour:
                continue
            vol = float(k[5])
            daily_volumes.setdefault(day, []).append(vol)

        if today_str in daily_volumes:
            del daily_volumes[today_str]

        # Считаем средний объем до текущего часа
        volumes_up_to_hour = [sum(v) for v in daily_volumes.values() if len(v) >= hour]
        average_volume = mean(volumes_up_to_hour)

        # Получаем объем текущего дня
        today_klines = client.klines(symbol.upper(), "1h", limit=hour)
        today_volume = sum(float(k[5]) for k in today_klines)

        # Получаем текущую цену
        ticker = client.ticker_price(symbol=symbol)
        price = float(ticker["price"])

        ratio = today_volume / average_volume if average_volume else 0

        return {
            "price": price,
            "today_volume": today_volume,
            "average_volume": average_volume,
            "ratio": ratio
        }

    except Exception as e:
        return f"Ошибка при получении данных: {e}"

@router.message(Command("btc"))
async def volume_command(message: Message):
    result = get_volume_ratio("BTCUSDT")

    if isinstance(result, str):
        await message.answer(result)
        return

    ratio = result["ratio"]
    status = (
        "⬆️ Повышенный объем" if ratio > 1.2 else
        "⬇️ Пониженный объем" if ratio < 0.8 else
        "➖ Объем в норме"
    )

    await message.answer(
        f"<b>BTCUSDT</b>\n"
        f"💰 Цена: {result['price']:.2f}\n"
        f"📊 Объем с начала дня: {result['today_volume']:.2f}\n"
        f"📈 Исторический средний объем: {result['average_volume']:.2f}\n"
        f"{status}"
    )

@router.message(Command("eth"))
async def volume_eth(message: Message):
    result = get_volume_ratio("ETHUSDT")

    if isinstance(result, str):
        await message.answer(result)
        return

    ratio = result["ratio"]
    status = (
        "⬆️ Повышенный объем" if ratio > 1.2 else
        "⬇️ Пониженный объем" if ratio < 0.8 else
        "➖ Объем в норме"
    )

    await message.answer(
        f"<b>ETHUSDT</b>\n"
        f"💰 Цена: {result['price']:.2f}\n"
        f"📊 Объем с начала дня: {result['today_volume']:.2f}\n"
        f"📈 Исторический средний объем: {result['average_volume']:.2f}\n"
        f"{status}"
    )