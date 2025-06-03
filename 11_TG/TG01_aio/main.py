import telebot
from telebot.types import Message
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id, "Привет! Я покажу тебе погоду. Напиши /weather")

@bot.message_handler(commands=['help'])
def help_command(message: Message):
    bot.send_message(message.chat.id, "Доступные команды:\n/start — начать\n/help — помощь\n/weather — погода")

@bot.message_handler(commands=['weather'])
def weather(message: Message):
    import os
    city = "Saint Petersburg"
    lat, lon = 59.93, 30.31
    API_KEY = os.getenv("WEATHER_API_KEY")

    if not API_KEY:
        bot.send_message(message.chat.id, "API-ключ не найден в переменных окружения.")
        return

    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&lang=ru&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['current']['temp']
        desc = data['current']['weather'][0]['description']
        bot.send_message(message.chat.id, f"🌤 Погода в {city}:\nТемпература: {temp}°C\nСостояние: {desc}")
    else:
        bot.send_message(message.chat.id, "Ошибка при получении погоды.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
