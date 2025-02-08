import requests

def task_1():
    """Задание 1: Получение данных с GitHub API"""
    print("\n=== ЗАДАНИЕ 1: Поиск репозиториев с HTML-кодом на GitHub ===")
    # Отправляем запрос к GitHub API
    url = "https://api.github.com/search/repositories"
    params = {"q": "language:html"}  # Ищем репозитории с HTML-кодом
    response = requests.get(url, params=params)

    # Проверяем статус-код
    print("Статус-код:", response.status_code)

    # Выводим общее количество найденных репозиториев
    print("Общее количество найденных репозиториев:", response.json().get("total_count", "Не найдено"))

    # Берём 3 первых репозитория
    repos = response.json().get("items", [])[:3]

    # Выводим краткую информацию о них
    for repo in repos:
        print(f"\n🔹 Репозиторий: {repo['name']}")
        print(f"📂 Полное имя: {repo['full_name']}")
        print(f"🔗 Ссылка: {repo['html_url']}")
        print(f"⭐️ Звёзды: {repo['stargazers_count']} | 🍴 Форки: {repo['forks_count']}")
        print(f"📝 Описание: {repo['description'] or 'Нет описания'}")


def task_2():
    """Задание 2: Фильтрация данных по параметрам (JSONPlaceholder API)"""
    print("\n=== ЗАДАНИЕ 2: Получение постов с userId=1 ===")
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": 1}  # Получаем посты только пользователя с id=1

    # Отправляем запрос
    response = requests.get(url, params=params)
    posts = response.json()

    # Выводим красиво
    print(f"📌 Всего постов у пользователя 1: {len(posts)}\n")

    for post in posts:
        print(f"🆔 Пост #{post['id']}")
        print(f"📢 Заголовок: {post['title']}")
        print(f"✍️  Текст: {post['body']}\n")
        print("-" * 50)  # Разделитель


def task_3():
    """Задание 3: Отправка POST-запроса"""
    print("\n=== ЗАДАНИЕ 3: Создание нового поста (POST-запрос) ===")
    url = "https://jsonplaceholder.typicode.com/posts"
    data = {"title": "foo", "body": "bar", "userId": 1}
    response = requests.post(url, json=data)

    print("Статус-код:", response.status_code)
    print("Ответ API:", response.json())


def main():
    """Главная функция"""
    task_1()
    task_2()
    task_3()


if __name__ == "__main__":
    main()