import telebot
from telebot.types import Message
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

weather_icons = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧",
    "drizzle": "🌦",
    "thunderstorm": "⛈",
    "snow": "❄️",
    "mist": "🌫",
    "fog": "🌫"
}

@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id, "Привет! Я покажу тебе погоду в Петербурге — просто используй команду /weather.\n\nЕсли хочешь узнать погоду в другой локации — пропиши вручную /weather и название города на английском (пример: /weather Tokyo)")

@bot.message_handler(commands=['help'])
def help_command(message: Message):
    bot.send_message(message.chat.id, "Доступные команды:\n/start — начать\n/help — помощь\n/weather — погода")

@bot.message_handler(commands=['weather'])
def weather(message: Message):
    parts = message.text.strip().split(maxsplit=1)
    city = parts[1] if len(parts) > 1 else "Saint Petersburg"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={WEATHER_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        main = data['weather'][0]['main']
        icon = weather_icons.get(main.lower(), "🌡")  # fallback на универсальный значок
        bot.send_message(message.chat.id, f"{icon} Погода в {city}:\nТемпература: {temp}°C\nСостояние: {desc}")
    elif response.status_code == 404:
        bot.send_message(message.chat.id, f"Город '{city}' не найден.")
    else:
        bot.send_message(message.chat.id, "Ошибка при получении погоды.")
        print("Ошибка:", response.status_code)
        print(response.text)



if __name__ == "__main__":
    bot.polling(none_stop=True)
