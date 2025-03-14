import scrapy

class DivanLightingSpider(scrapy.Spider):
    name = "divan_lighting"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]  # Категория освещения

    def parse(self, response):
        # Находим карточки товаров
        products = response.css("div[data-testid='product-card']")

        for product in products:
            yield {
                "name": product.css("a.ProductName span[itemprop='name']::text").get(),
                "price": product.css("div.pY3d2 span[data-testid='price']::text").get(),
                "link": response.urljoin(product.css("a.ProductName::attr(href)").get())
            }

        # ПАГИНАЦИЯ
        
        # Получаем все ссылки на страницы
        pages = response.css("a.PaginationLink::attr(href)").getall()

        # Убираем дубликаты (сохраняя порядок)
        pages = list(dict.fromkeys(pages))

        # Определяем текущую страницу
        current_page_index = None
        for i, page in enumerate(pages):
            if response.url.endswith(page):  # Текущая страница
                current_page_index = i
                break

        # Если есть следующая страница
        if current_page_index is not None and current_page_index + 1 < len(pages):
            next_page = pages[current_page_index + 1]
            yield response.follow(next_page, callback=self.parse)

