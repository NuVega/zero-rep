from telegram.ext import Application, CommandHandler

# Вставь свой токен
TOKEN = "7799012531:AAEH_oVQM8vSgvP3q1B0gODLKtmAM4kq_90"

# Асинхронная функция для обработки команды /start
async def start(update, context):
    await update.message.reply_text("Привет! Я готов отправить трек с обложкой. Напиши /send_audio, чтобы начать!")

# Асинхронная функция для обработки команды /send_audio
async def send_audio(update, context):
    chat_id = update.effective_chat.id

    # Путь к аудио и обложке
    audio_path = "NikePro.mp3"
    thumb_path = "image.jpeg"

    # Отправка аудио с миниатюрой
    await context.bot.send_audio(
        chat_id=chat_id,
        audio=open(audio_path, "rb"),
        thumbnail=open(thumb_path, "rb")  # Миниатюра остаётся
    )
    await update.message.reply_text("Аудио отправлено!")

# Настройка приложения
def main():
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("send_audio", send_audio))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()