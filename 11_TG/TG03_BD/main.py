import telebot
from telebot.types import Message
import sqlite3
import os
from dotenv import load_dotenv
from db import init_db, save_student, get_all_students



load_dotenv()
init_db()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

user_states = {}  # временное хранилище ввода


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id, "Привет! Это бот по противодействию экстремизму МВД РФ. Давай тебя зарегистрируем😊\n\nКак тебя зовут?")
    user_states[message.chat.id] = {'step': 'name'}


@bot.message_handler(func=lambda msg: msg.chat.id in user_states)
def handle_input(message: Message):
    state = user_states[message.chat.id]
    step = state['step']

    if step == 'name':
        state['name'] = message.text
        state['step'] = 'age'
        bot.send_message(message.chat.id, "Сколько тебе лет?")

    elif step == 'age':
        if not message.text.isdigit():
            bot.send_message(message.chat.id, "Пожалуйста, введи число.")
            return
        state['age'] = int(message.text)
        state['step'] = 'grade'
        bot.send_message(message.chat.id, "В каком ты классе? (Например: 9A)")

    elif step == 'grade':
        state['grade'] = message.text
        save_student(state['name'], state['age'], state['grade'])
        bot.send_message(message.chat.id, "Спасибо! Тебя зарегистрировали.")
        user_states.pop(message.chat.id)


@bot.message_handler(commands=['students'])
def list_students(message: Message):
    students = get_all_students()
    if not students:
        bot.send_message(message.chat.id, "В базе пока нет учеников.")
        return

    response = "👨‍🎓 Список учеников:\n"
    for i, (name, age, grade) in enumerate(students, start=1):
        response += f"{i}. {name}, {age} лет, {grade} класс\n"

    bot.send_message(message.chat.id, response)


if __name__ == "__main__":
    bot.polling(none_stop=True)
