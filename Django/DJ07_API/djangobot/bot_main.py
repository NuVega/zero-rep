from telebot.types import Message
import telebot
import requests
import os

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message: Message):
    data = {
        "user_id": message.from_user.id,
        "username": message.from_user.username
    }
    response = requests.post(API_URL + "/register/", json=data)
    if response.status_code == 200:
        if response.json().get('message'):
            bot.send_message(message.chat.id, "Вы уже были зарегистрированы ранее!")
        else:
            bot.send_message(message.chat.id, f"Вы успешно зарегистрированы! Ваш уникальный номер: {response.json()['id']}")
    else:
        bot.send_message(message.chat.id, f"Произошла ошибка при регистрации!")
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")

@bot.message_handler(commands=['myinfo'])
def user_info(message: Message):
    response = requests.get(f"{API_URL}/user/{message.from_user.id}/")
    if response.status_code == 200:
        data = response.json()
        bot.send_message(
            message.chat.id,
            f"Ваш ID: {data['user_id']}\nНик: {data.get('username') or 'нет'}\nЗарегистрирован: {data['created_at']}"
        )
    elif response.status_code == 404:
        bot.send_message(message.chat.id, "Вы не зарегистрированы!")
    else:
        bot.send_message(message.chat.id, "Непредвиденная ошибка!")

if __name__ == "__main__":
    bot.polling(none_stop=True)