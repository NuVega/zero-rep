import scrapy
import csv
import os
import numpy as np
import matplotlib.pyplot as plt


class DivanCouchSpider(scrapy.Spider):
    name = "divan_couch"
    allowed_domains = ["divan.ru"]
    item_counter = 1
    max_empty_pages = 3  # После нескольких пустых страниц останавливаем

    def __init__(self, *args, **kwargs):
        super(DivanCouchSpider, self).__init__(*args, **kwargs)
        self.prices = []
        self.empty_pages = 0
        self.filename = "divan_couch.csv"
        self.visited_pages = set()

        if os.path.exists(self.filename):
            os.remove(self.filename)
            self.logger.info(f"Удален старый файл: {self.filename}")

    def start_requests(self):
        base_url = "https://www.divan.ru/category/divany/page-{}"
        for page in range(1, 100):  # запас по страницам
            yield scrapy.Request(url=base_url.format(page), callback=self.parse)

    def parse(self, response):
        items = []
        products = response.css("div[data-testid='product-card']")
        self.visited_pages.add(response.url)

        if not products:
            self.empty_pages += 1
            self.logger.warning(f"Пустая страница #{self.empty_pages}")
            if self.empty_pages >= self.max_empty_pages:
                self.logger.info("Слишком много пустых страниц — остановка")
                return
            return

        for product in products:
            price_text = product.css("div.pY3d2 span[data-testid='price']::text").get()
            if price_text:
                price = int(price_text.replace(" ", ""))
                self.prices.append(price)

            item = {
                "№": self.item_counter,
                "Наименование": product.css("a.ProductName span[itemprop='name']::text").get(),
                "Цена": price_text,
                "Ссылка": response.urljoin(product.css("a.ProductName::attr(href)").get())
            }
            self.item_counter += 1
            items.append(item)
            yield item

        if items:
            self.save_to_csv(items)

    def save_to_csv(self, items):
        fieldnames = ["№", "Наименование", "Цена", "Ссылка"]
        file_exists = os.path.exists(self.filename)

        with open(self.filename, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(items)

    def process_prices(self):
        if not self.prices:
            self.logger.warning("Цены не найдены")
            return

        avg_price = np.mean(self.prices)
        self.logger.info(f"Средняя цена дивана: {avg_price:.2f} руб.")

        plt.figure(figsize=(10, 5))
        plt.hist(self.prices, bins=100, edgecolor="black", alpha=0.75)
        plt.xlabel("Цена (руб.)")
        plt.ylabel("Количество диванов")
        plt.title("Гистограмма цен на диваны")
        plt.grid(True)
        plt.show()

    def closed(self, reason):
        self.logger.info(f"Паук завершил работу: {reason}")
        self.logger.info(f"Всего собрано товаров: {self.item_counter - 1}")
        self.process_prices()
        self.logger.info(f"Всего страниц обработано: {len(self.visited_pages)}")