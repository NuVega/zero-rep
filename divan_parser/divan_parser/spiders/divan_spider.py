import scrapy
import csv
import os


class DivanLightingSpider(scrapy.Spider):
    name = "divan_lighting"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]
    item_counter = 1  # Счётчик товаров

    def __init__(self, *args, **kwargs):
        super(DivanLightingSpider, self).__init__(*args, **kwargs)
        filename = "divan_lighting.csv"
        if os.path.exists(filename):
            os.remove(filename)
            self.logger.info(f"Удален существующий файл {filename}")

    def parse(self, response):
        items = []
        products = response.css("div[data-testid='product-card']")

        for product in products:
            item = {
                "№": self.item_counter,
                "Наименование": product.css("a.ProductName span[itemprop='name']::text").get(),
                "Цена": product.css("div.pY3d2 span[data-testid='price']::text").get(),
                "Ссылка": response.urljoin(product.css("a.ProductName::attr(href)").get())
            }
            self.item_counter += 1
            items.append(item)
            yield item  # отдаём в Scrapy пайплайны, если нужны

        if items:
            self.save_to_csv(items)

        # Пагинация
        pages = response.css("a.PaginationLink::attr(href)").getall()
        if not pages:
            self.logger.info("Страницы пагинации не найдены")
            return

        pages = list(dict.fromkeys(pages))  # Убираем дубликаты
        current_page_index = None
        for i, page in enumerate(pages):
            if response.url.endswith(page):
                current_page_index = i
                break

        if current_page_index is not None and current_page_index + 1 < len(pages):
            next_page = pages[current_page_index + 1]
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info("Достигнута последняя страница или не удалось определить текущую страницу")

    def save_to_csv(self, items):
        filename = "divan_lighting.csv"
        fieldnames = ["№", "Наименование", "Цена", "Ссылка"]

        file_exists = os.path.exists(filename)

        with open(filename, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(items)

    def closed(self, reason):
        self.logger.info(f"Паук завершил работу по причине: {reason}")
        self.logger.info(f"Всего собрано товаров: {self.item_counter - 1}")