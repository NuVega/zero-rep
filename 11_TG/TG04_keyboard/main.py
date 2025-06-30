import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_hello = KeyboardButton("Привет")
    btn_bye = KeyboardButton("Пока")
    markup.add(btn_hello, btn_bye)

    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Выбери опцию:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!")
    elif message.text == "Пока":
        bot.send_message(message.chat.id, f"До свидания, {message.from_user.first_name}!")


if __name__ == "__main__":
    bot.polling(none_stop=True)
