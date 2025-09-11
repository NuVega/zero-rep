# 1. Вводим строку в терминал
# 2. Нормализуем:
# 2.1 Приводим к нижнему регистру
# 2.2 Исключаем пробелы, знаки препинания и прочие лишние символы
# 3. Переворачиваем строку
# 4. Сравниваем

def is_palindrome(text: str) -> bool:
    s = "".join(ch.lower() for ch in text if ch.isalnum())
    return s == s[::-1]

if __name__ == "__main__":
    print("Проверка палиндромов. Введите строку (или 'exit' для выхода).")

    while True:
        user_input = input(">>> ")

        if user_input.lower() in ("exit"):
            print("До встречи 👋")
            break

        if is_palindrome(user_input):
            print("✅ Это палиндром")
        else:
            print("❌ Это не палиндром")
