import os
from telebot import TeleBot
from telebot.types import Message
from deep_translator import GoogleTranslator
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(
        message.chat.id,
        "Привет! Я мультизадачный ботик, вот что я могу:\n📥 сохранять фото\n🎙 отправлять голосовое (напиши /voice)\n🌍 переводить текст на английский!"
    )


@bot.message_handler(commands=['help'])
def help_command(message: Message):
    bot.send_message(message.chat.id, "Доступные команды:\n/start — начать\n/help — помощь\n/voice — голосовое сообщение")


@bot.message_handler(commands=['voice'])
def send_voice(message: Message):
    try:
        with open('voice.ogg', 'rb') as voice:
            bot.send_voice(message.chat.id, voice)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл voice.ogg не найден.")


@bot.message_handler(content_types=['photo'])
def save_photo(message: Message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    if not os.path.exists("img"):
        os.makedirs("img")

    file_name = f"img/{message.from_user.id}_{file_info.file_unique_id}.jpg"
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, "Фото сохранено!")


@bot.message_handler(func=lambda msg: True, content_types=['text'])
def translate_to_english(message: Message):
    translated = GoogleTranslator(source='auto', target='en').translate(message.text)
    bot.send_message(message.chat.id, f"Перевод на английский:\n{translated}")


if __name__ == "__main__":
    bot.polling(none_stop=True)
