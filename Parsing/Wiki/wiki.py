import sys
import time
from urllib.parse import quote
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def scroll_paragraphs(driver):
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

def debug_headers(driver):
    print("\n--- Все заголовки на странице ---")
    headers = driver.find_elements(By.CSS_SELECTOR, ".mw-headline, .mw-heading")
    for i, header in enumerate(headers, 1):
        try:
            print(f"{i}. '{header.text}' (родитель: {header.find_element(By.XPATH, './parent::*').tag_name})")
        except:
            print(f"{i}. '{header.text}' (не удалось определить родителя)")
    print("--- Конец списка заголовков ---\n")

def debug_after_header(driver, header_element):
    print("\n--- Элементы после заголовка 'См. также' ---")
    try:
        parent = header_element.find_element(By.XPATH, "./parent::*")
        print(f"Родительский элемент: {parent.tag_name}, класс: {parent.get_attribute('class')}")

        # Смотрим до 5 следующих элементов после родительского заголовка
        for i in range(1, 6):
            try:
                next_element = parent.find_element(By.XPATH, f"./following-sibling::*[{i}]")
                print(f"{i}. Тег: {next_element.tag_name}, класс: {next_element.get_attribute('class')}")
                print(f"   Текст: {next_element.text[:100]}...")  # Первые 100 символов текста

                # Если это список, покажем его содержимое
                if next_element.tag_name in ['ul', 'ol', 'div']:
                    try:
                        list_items = next_element.find_elements(By.CSS_SELECTOR, "li, a")
                        print(f"   Найдено элементов внутри: {len(list_items)}")
                        for j, item in enumerate(list_items[:5], 1):  # Покажем первые 5
                            print(f"     {j}. {item.tag_name}: {item.text}")
                    except:
                        print("   Не удалось получить содержимое")
            except:
                print(f"{i}. Не удалось найти следующий элемент")
    except Exception as e:
        print(f"Ошибка при анализе: {e}")
    print("--- Конец анализа ---\n")


def debug_see_also_section(driver):
    print("\n--- Детальная отладка раздела 'См. также' ---")

    try:
        # Используем JavaScript для более полного анализа структуры раздела
        script = """
        function analyzeSeeAlsoSection() {
            // Ищем заголовок "См. также" по разным критериям
            var result = { found: false, structure: [], htmlSample: "" };

            // Попытка найти по ID
            var possibleIds = ["См._также", ".D0.A1.D0.BC._.D1.82.D0.B0.D0.BA.D0.B6.D0.B5"];
            var header = null;

            for (var i = 0; i < possibleIds.length; i++) {
                var element = document.getElementById(possibleIds[i]);
                if (element) {
                    header = element;
                    result.idFound = possibleIds[i];
                    break;
                }
            }

            // Если не нашли по ID, ищем по тексту
            if (!header) {
                var headers = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
                for (var i = 0; i < headers.length; i++) {
                    if (headers[i].textContent.trim() === "См. также") {
                        header = headers[i];
                        result.textFound = true;
                        break;
                    }
                }
            }

            if (!header) {
                return "Элемент 'См. также' не найден ни по ID, ни по тексту заголовка";
            }

            result.found = true;

            // Информация о найденном заголовке
            result.headerInfo = {
                tagName: header.tagName,
                id: header.id,
                classes: header.className,
                text: header.textContent.trim(),
                parentTagName: header.parentElement ? header.parentElement.tagName : null,
                parentClasses: header.parentElement ? header.parentElement.className : null
            };

            // Находим ближайший родительский div.mw-heading, если есть
            var headerParent = header;
            while (headerParent && !headerParent.classList.contains('mw-heading')) {
                headerParent = headerParent.parentElement;
            }

            // Если нашли родительский заголовок div.mw-heading
            if (headerParent && headerParent !== header) {
                result.headerParent = {
                    tagName: headerParent.tagName,
                    id: headerParent.id,
                    classes: headerParent.className
                };
            }

            // Анализируем следующие элементы (до 5)
            var current = headerParent || header;
            var nextElements = [];

            for (var i = 0; i < 5; i++) {
                var next = current.nextElementSibling;
                if (!next) break;

                var elementInfo = {
                    tag: next.tagName,
                    classes: next.className,
                    id: next.id,
                    textPreview: next.textContent.substr(0, 100).trim() + (next.textContent.length > 100 ? "..." : "")
                };

                // Если это список, проверим наличие ссылок
                if (next.tagName === 'UL' || next.tagName === 'OL') {
                    elementInfo.listInfo = {
                        itemCount: next.children.length,
                        hasLinks: next.querySelectorAll('a').length > 0,
                        firstFewLinks: []
                    };

                    // Сохраняем информацию о первых 3 ссылках
                    var links = next.querySelectorAll('a');
                    for (var j = 0; j < Math.min(links.length, 3); j++) {
                        elementInfo.listInfo.firstFewLinks.push({
                            text: links[j].textContent.trim(),
                            href: links[j].getAttribute('href')
                        });
                    }
                }

                // Если это div, проверим наличие вложенных списков
                if (next.tagName === 'DIV') {
                    var nestedLists = next.querySelectorAll('ul, ol');
                    if (nestedLists.length > 0) {
                        elementInfo.nestedListInfo = {
                            listCount: nestedLists.length,
                            totalLinks: next.querySelectorAll('a').length
                        };

                        // Информация о первом вложенном списке
                        if (nestedLists.length > 0) {
                            var firstListLinks = nestedLists[0].querySelectorAll('a');
                            elementInfo.nestedListInfo.firstListLinkCount = firstListLinks.length;
                            elementInfo.nestedListInfo.firstListLinks = [];

                            for (var j = 0; j < Math.min(firstListLinks.length, 3); j++) {
                                elementInfo.nestedListInfo.firstListLinks.push({
                                    text: firstListLinks[j].textContent.trim(),
                                    href: firstListLinks[j].getAttribute('href')
                                });
                            }
                        }
                    }
                }

                nextElements.push(elementInfo);
                current = next;

                // Если наткнулись на следующий заголовок, останавливаемся
                if (next.tagName === 'H2' || next.tagName === 'H3' || 
                    (next.classList.contains('mw-heading') && next.querySelector('h2, h3'))) {
                    break;
                }
            }

            result.nextElements = nextElements;

            // Получаем фрагмент HTML для отладки
            try {
                var tempContainer = document.createElement('div');
                var clonedHeader = (headerParent || header).cloneNode(true);
                tempContainer.appendChild(clonedHeader);

                current = headerParent || header;
                for (var i = 0; i < Math.min(nextElements.length, 3); i++) {
                    current = current.nextElementSibling;
                    if (current) {
                        tempContainer.appendChild(current.cloneNode(true));
                    }
                }

                result.htmlSample = tempContainer.innerHTML;
            } catch (e) {
                result.htmlError = e.toString();
            }

            return result;
        }

        return JSON.stringify(analyzeSeeAlsoSection(), null, 2);
        """

        js_result = driver.execute_script(script)
        print("\nДиагностика структуры раздела 'См. также':")
        print(js_result)

    except Exception as e:
        print(f"Ошибка при отладке: {e}")

    print("--- Конец отладки раздела 'См. также' ---\n")


def get_see_also_links(driver):
    try:
        print("\nПоиск раздела 'См. также' и ссылок...")

        # Найдем идентификатор раздела "См. также"
        see_also_id = None
        possible_ids = ["См._также", ".D0.A1.D0.BC._.D1.82.D0.B0.D0.BA.D0.B6.D0.B5"]

        for id_value in possible_ids:
            try:
                if driver.find_element(By.ID, id_value):
                    see_also_id = id_value
                    break
            except NoSuchElementException:
                continue

        if not see_also_id:
            # Если не нашли по ID, попробуем найти по тексту заголовка
            try:
                see_also_header = driver.find_element(By.XPATH, "//h2[normalize-space(.)='См. также']")
                see_also_id = see_also_header.get_attribute("id")
            except NoSuchElementException:
                print("Заголовок 'См. также' не найден")
                return []

        print(f"Найден раздел 'См. также' с ID: {see_also_id}")

        # Используем JavaScript для получения списка ссылок
        # JavaScript может легче работать с различными структурами DOM
        script = """
        function getSeeAlsoLinks(seeAlsoId) {
            // Находим заголовок по ID
            var header = document.getElementById(seeAlsoId);
            if (!header) {
                return {error: "Заголовок не найден"};
            }

            // Находим родительский элемент заголовка (обычно div.mw-heading)
            var headerParent = header;
            while (headerParent && !headerParent.classList.contains('mw-heading')) {
                headerParent = headerParent.parentElement;
            }

            if (!headerParent) {
                headerParent = header.parentElement;
            }

            // Максимальное количество элементов для проверки после заголовка
            var maxElements = 10;
            var linksFound = [];
            var currentElement = headerParent;

            // Ищем списки ссылок в следующих после заголовка элементах
            for (var i = 0; i < maxElements; i++) {
                // Переходим к следующему соседнему элементу
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

                // Ищем списки и ссылки в текущем элементе
                var lists = [];

                // Если это сам список
                if (currentElement.tagName === 'UL' || currentElement.tagName === 'OL') {
                    lists.push(currentElement);
                }
                // Если это div с колонками или другой контейнер со списками
                else {
                    var nestedLists = currentElement.querySelectorAll('ul, ol');
                    for (var j = 0; j < nestedLists.length; j++) {
                        lists.push(nestedLists[j]);
                    }
                }

                // Извлекаем ссылки из всех найденных списков
                for (var k = 0; k < lists.length; k++) {
                    var links = lists[k].querySelectorAll('a');
                    for (var l = 0; l < links.length; l++) {
                        var link = links[l];
                        var href = link.getAttribute('href');

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

        return getSeeAlsoLinks(arguments[0]);
        """

        links = driver.execute_script(script, see_also_id)

        if not links or (isinstance(links, dict) and 'error' in links):
            print(
                "Не удалось найти ссылки: " + (links.get('error') if isinstance(links, dict) else "неизвестная ошибка"))
            return []

        # Фильтруем литературу (ISBN, DOI и т.д.)
        filtered_links = []
        for link in links:
            if not any(marker in link['title'] for marker in ['ISBN', 'DOI', 'ISSN']):
                filtered_links.append(link)

        if not filtered_links:
            print("На этой странице в разделе 'См. также' отсутствуют ссылки или структура страницы нестандартная.")
            return []

        print(f"Найдено {len(filtered_links)} ссылок в разделе 'См. также'")
        for i, link in enumerate(filtered_links, 1):
            print(f"  {i}. {link['title']} ({link['href']})")

        return filtered_links

    except Exception as e:
        print(f"Общая ошибка при поиске ссылок: {e}")
        import traceback
        traceback.print_exc()
        return []

def choose_link(driver):
    # Добавляем задержку для полной загрузки страницы
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.8);")  # Прокрутка почти до конца
    time.sleep(1)

    # Отладка для диагностики
    debug_see_also_section(driver)

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
    query = input("Введите поисковый запрос для Википедии: ")
    encoded_query = quote(query)
    url = f"https://ru.wikipedia.org/wiki/{encoded_query}"

    driver = webdriver.Chrome()
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

    driver.quit()


if __name__ == "__main__":
    main()


