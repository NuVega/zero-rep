import websockets
import json
from collections import deque
from aiogram import Bot

URL_1H = "wss://stream.binance.com:9443/ws/btcusdt@kline_1h"
URL_1M = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"

body_queue_1h = deque(maxlen=5)
body_queue_1m = deque(maxlen=5)

chat_id = None  # задаётся вручную, чтобы знать, куда слать

async def run_btc_watchdog(bot: Bot):
    global chat_id
    async with websockets.connect(URL_1H) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            k = data["k"]
            if not k["x"]:  # незакрытая свеча
                continue

            body = abs(float(k["c"]) - float(k["o"]))
            body_queue_1h.append(body)

            if len(body_queue_1h) < 5:
                continue

            avg = sum(body_queue_1h) / len(body_queue_1h)
            if body > 3 * avg:
                print(f"[DEBUG] chat_id: {chat_id}, body: {body:.5f}, avg: {avg:.5f}")
                if chat_id:
                    await bot.send_message(chat_id, f"⚠️ <b>Аномальная 1H свеча BTC</b>\nТело: {body:.2f}, Среднее: {avg:.2f}")
                else:
                    print("[!] Найдена аномалия (1ч), но chat_id не задан")

async def run_btc_watchdog_1m(bot: Bot):
    global chat_id
    async with websockets.connect(URL_1M) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            k = data["k"]
            if not k["x"]:
                continue

            body = abs(float(k["c"]) - float(k["o"]))
            body_queue_1m.append(body)

            if len(body_queue_1m) < 5:
                continue

            avg = sum(body_queue_1m) / len(body_queue_1m)
            if body > 3 * avg:
                print(f"[DEBUG] chat_id: {chat_id}, body: {body:.5f}, avg: {avg:.5f}")
                if chat_id:
                    await bot.send_message(chat_id, f"⚠️ <b>Аномальная 1M свеча BTC</b>\nТело: {body:.5f}, Среднее: {avg:.5f}")
                else:
                    print("[!] Найдена аномалия (1м), но chat_id не задан")