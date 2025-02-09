import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# Создаём переводчик
translator = GoogleTranslator(source="en", target="ru")

# Функция для получения слова и его перевода
def get_english_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Получаем английское слово и его определение
        english_word = soup.find("div", id="random_word").text.strip()
        word_definition = soup.find("div", id="random_word_definition").text.strip()

        # Переводим слово и его определение (без async)
        translated_word = translator.translate(english_word)
        translated_definition = translator.translate(word_definition)

        return {
            "english_word": english_word,
            "translated_word": translated_word,
            "word_definition": word_definition,
            "translated_definition": translated_definition
        }
    except Exception as e:
        print(f"⚠️ Произошла ошибка: {e}")
        return None

# Основная игра
def word_game():
    print("🎮 Добро пожаловать в игру 'Угадай слово'!\n")

    while True:
        word_dict = get_english_words()
        if not word_dict:
            break  # Выход из игры при ошибке

        word = word_dict["translated_word"]
        word_definition = word_dict["translated_definition"]
        original_word = word_dict["english_word"]
        original_definition = word_dict["word_definition"]

        # Выводим и оригинал, и перевод
        print(f"📖 Определение: {word_definition} ({original_definition})")
        user_input = input("📝 Какое это слово? ")

        if user_input.lower() == word.lower():
            print("✅ Верно!")
        else:
            print(f"❌ Ошибка! Правильный ответ: {word} ({original_word})")

        # Спрашиваем, хочет ли игрок продолжить
        play_again = input("\n🔄 Сыграть ещё раз? (y/n): ").strip().lower()
        if play_again != "y":
            print("👋 Спасибо за игру!")
            break

# Запуск игры
word_game()