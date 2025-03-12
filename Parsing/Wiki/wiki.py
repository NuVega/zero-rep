import sys
import time
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def scroll_paragraphs(driver):
    """Функция для последовательного просмотра параграфов статьи"""
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > p")
    paragraphs_text = [p.text for p in paragraphs if p.text.strip()]

    if not paragraphs_text:
        print("Параграфы не найдены.")
        return

    print("\n--- Начало статьи ---\n")
    for i, text in enumerate(paragraphs_text, start=1):
        print(f"Параграф {i}:\n{text}\n")
        user_input = input("Нажмите Enter для следующего параграфа или введите 'q' для выхода: ")
        if user_input.lower() == "q":
            break
    print("--- Конец статьи ---\n")


def get_see_also_links(driver):
    """Функция для получения ссылок из раздела 'См. также'"""
    try:
        print("\nПоиск раздела 'См. также'...")

        # JavaScript для нахождения и извлечения ссылок из раздела "См. также"
        script = """
        function getSeeAlsoLinks() {
            // Поиск заголовка "См. также" разными способами
            let header = null;

            // Поиск по ID
            const possibleIds = ["См._также", ".D0.A1.D0.BC._.D1.82.D0.B0.D0.BA.D0.B6.D0.B5"];
            for (const id of possibleIds) {
                const element = document.getElementById(id);
                if (element) {
                    header = element;
                    break;
                }
            }

            // Если не нашли по ID, ищем по тексту заголовка
            if (!header) {
                const headers = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
                for (const h of headers) {
                    if (h.textContent.trim() === "См. также") {
                        header = h;
                        break;
                    }
                }
            }

            if (!header) {
                return {error: "Заголовок 'См. также' не найден"};
            }

            // Находим родительский элемент заголовка (обычно div.mw-heading)
            let headerParent = header;
            while (headerParent && !headerParent.classList.contains('mw-heading')) {
                headerParent = headerParent.parentElement;
            }

            if (!headerParent) {
                headerParent = header.parentElement;
            }

            // Ищем связанные ссылки в следующих элементах
            const maxElements = 10;
            const linksFound = [];
            let currentElement = headerParent;

            for (let i = 0; i < maxElements; i++) {
                currentElement = currentElement.nextElementSibling;

                if (!currentElement) {
                    break;
                }

                // Если встретили новый заголовок h2/h3, значит вышли за пределы раздела
                if (currentElement.tagName === 'H2' || currentElement.tagName === 'H3' ||
                    (currentElement.classList.contains('mw-heading') && 
                     (currentElement.querySelector('h2') || currentElement.querySelector('h3')))) {
                    break;
                }

                // Ищем списки и ссылки
                const lists = [];

                // Если это сам список
                if (currentElement.tagName === 'UL' || currentElement.tagName === 'OL') {
                    lists.push(currentElement);
                }
                // Если это div с колонками или другой контейнер со списками
                else {
                    const nestedLists = currentElement.querySelectorAll('ul, ol');
                    for (let j = 0; j < nestedLists.length; j++) {
                        lists.push(nestedLists[j]);
                    }
                }

                // Извлекаем ссылки из всех найденных списков
                for (const list of lists) {
                    const links = list.querySelectorAll('a');
                    for (const link of links) {
                        const href = link.getAttribute('href');

                        // Фильтруем только ссылки на статьи Википедии
                        if (href && href.startsWith('/wiki/') && !href.includes('action=edit')) {
                            linksFound.push({
                                title: link.textContent.trim(),
                                href: window.location.origin + href
                            });
                        }
                    }
                }

                // Если нашли хотя бы одну ссылку, считаем, что это и есть раздел "См. также"
                if (linksFound.length > 0) {
                    break;
                }
            }

            return linksFound;
        }

        return getSeeAlsoLinks();
        """

        links = driver.execute_script(script)

        # Проверка на ошибки в результате выполнения скрипта
        if not links or (isinstance(links, dict) and 'error' in links):
            error_msg = links.get('error') if isinstance(links, dict) and 'error' in links else "неизвестная ошибка"
            print(f"Не удалось найти ссылки: {error_msg}")
            return []

        # Фильтруем литературу (ISBN, DOI и т.д.)
        filtered_links = []
        for link in links:
            if not any(marker in link['title'] for marker in ['ISBN', 'DOI', 'ISSN']):
                filtered_links.append(link)

        if not filtered_links:
            print("На этой странице в разделе 'См. также' отсутствуют ссылки или структура страницы нестандартная.")
            return []

        # Просто сообщаем о количестве найденных ссылок без подробного вывода
        print(f"Найдено {len(filtered_links)} ссылок в разделе 'См. также'")
        return filtered_links

    except Exception as e:
        print(f"Ошибка при поиске ссылок: {e}")
        return []


def choose_link(driver):
    """Функция для выбора ссылки из раздела 'См. также'"""
    # Задержка для полной загрузки страницы
    time.sleep(2)
    # Прокрутка вниз для доступа к разделу "См. также"
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.8);")
    time.sleep(1)

    # Получаем ссылки
    links = get_see_also_links(driver)
    if not links:
        print("Нет связанных страниц в разделе «См. также» или список не найден.")
        return None

    print("\nСвязанные страницы (См. также):")
    for idx, link in enumerate(links, start=1):
        print(f"{idx}. {link['title']}")

    while True:
        choice = input("Введите номер страницы для перехода или 'q' для отмены: ")
        if choice.lower() == "q":
            return None
        try:
            num = int(choice)
            if 1 <= num <= len(links):
                return links[num - 1]['href']
            else:
                print("Некорректный номер. Попробуйте снова.")
        except ValueError:
            print("Введите число или 'q' для отмены.")


def main():
    """Основная функция программы"""
    query = input("Введите поисковый запрос для Википедии: ")
    encoded_query = quote(query)
    url = f"https://ru.wikipedia.org/wiki/{encoded_query}"

    driver = webdriver.Chrome()
    try:
        driver.get(url)
        time.sleep(2)

        while True:
            print("\nТекущая статья:", driver.title)
            print("Выберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из страниц из раздела 'См. также'")
            print("3. Выйти из программы")
            choice = input("Введите номер пункта: ")

            if choice == "1":
                scroll_paragraphs(driver)
            elif choice == "2":
                new_url = choose_link(driver)
                if new_url:
                    driver.get(new_url)
                    time.sleep(2)
                    # Подменю для новой страницы
                    while True:
                        print("\nВы на странице:", driver.title)
                        print("Выберите действие:")
                        print("1. Листать параграфы статьи")
                        print("2. Перейти на страницу из раздела 'См. также'")
                        print("3. Вернуться в главное меню")
                        sub_choice = input("Введите номер пункта: ")
                        if sub_choice == "1":
                            scroll_paragraphs(driver)
                        elif sub_choice == "2":
                            next_url = choose_link(driver)
                            if next_url:
                                driver.get(next_url)
                                time.sleep(2)
                            else:
                                print("Переход отменён.")
                        elif sub_choice == "3":
                            break
                        else:
                            print("Некорректный выбор. Попробуйте снова.")
            elif choice == "3":
                print("Выход из программы.")
                break
            else:
                print("Некорректный выбор. Попробуйте снова.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()