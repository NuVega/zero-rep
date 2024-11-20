import json


class Store:
    def __init__(self, name, address):
        """
        Конструктор для магазина.
        """
        self.name = name
        self.address = address
        self.items = {}

    def add_item(self, item_name, price):
        """
        Добавить товар в ассортимент.
        """
        self.items[item_name] = price
        print(f"Товар '{item_name}' добавлен с ценой {price}.")

    def remove_item(self, item_name):
        """
        Удалить товар из ассортимента.
        """
        if item_name in self.items:
            del self.items[item_name]
            print(f"Товар '{item_name}' удален.")
        else:
            print(f"Товар '{item_name}' не найден в ассортименте.")

    def get_price(self, item_name):
        """
        Получить цену товара по названию.
        """
        return self.items.get(item_name, None)

    def update_price(self, item_name, price):
        """
        Обновить цену товара.
        """
        if item_name in self.items:
            self.items[item_name] = price
            print(f"Цена товара '{item_name}' обновлена до {price}.")
        else:
            print(f"Товар '{item_name}' не найден.")

    def to_dict(self):
        """
        Преобразовать магазин в словарь для сохранения в JSON.
        """
        return {
            "name": self.name,
            "address": self.address,
            "items": self.items
        }

    @staticmethod
    def from_dict(data):
        """
        Создать магазин из словаря (при загрузке из JSON).
        """
        store = Store(data["name"], data["address"])
        store.items = data["items"]
        return store


class StoreManager:
    def __init__(self, filename="stores.json"):
        """
        Конструктор менеджера магазинов.
        """
        self.filename = filename
        self.stores = self.load_stores()

    def save_stores(self):
        """
        Сохранить магазины в файл JSON.
        """
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([store.to_dict() for store in self.stores], file, indent=4, ensure_ascii=False)

    def load_stores(self):
        """
        Загрузить магазины из файла JSON.
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Store.from_dict(store) for store in data]
        except FileNotFoundError:
            return []

    def add_store(self, name, address):
        """
        Добавить новый магазин.
        """
        self.stores.append(Store(name, address))
        self.save_stores()
        print(f"Магазин '{name}' добавлен.")

    def list_stores(self):
        """
        Вывести список магазинов.
        """
        if not self.stores:
            print("Нет доступных магазинов.")
        else:
            for idx, store in enumerate(self.stores, start=1):
                print(f"{idx}. {store.name} ({store.address})")


def main():
    manager = StoreManager()

    while True:
        print("\nМеню:")
        print("1. Выбрать магазин")
        print("2. Добавить новый магазин")
        print("3. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            if not manager.stores:
                print("Магазинов пока нет. Сначала добавьте новый магазин.")
                continue

            print("Доступные магазины:")
            manager.list_stores()
            try:
                store_index = int(input("Введите номер магазина: ")) - 1
                if 0 <= store_index < len(manager.stores):
                    store = manager.stores[store_index]
                    store_menu(store, manager)
                else:
                    print("Неверный номер магазина.")
            except ValueError:
                print("Пожалуйста, введите корректный номер.")

        elif choice == "2":
            name = input("Введите название магазина: ")
            address = input("Введите адрес магазина: ")
            manager.add_store(name, address)

        elif choice == "3":
            print("Спасибо за использование менеджера магазинов!")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


def store_menu(store, manager):
    while True:
        print(f"\nМагазин: {store.name} ({store.address})")
        print("1. Добавить товар")
        print("2. Удалить товар")
        print("3. Обновить цену товара")
        print("4. Показать цену товара")
        print("5. Показать весь ассортимент")
        print("6. Вернуться в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":
            item_name = input("Введите название товара: ")
            try:
                price = float(input("Введите цену товара: "))
                store.add_item(item_name, price)
                manager.save_stores()
            except ValueError:
                print("Пожалуйста, введите корректное значение цены.")

        elif choice == "2":
            item_name = input("Введите название товара: ")
            store.remove_item(item_name)
            manager.save_stores()

        elif choice == "3":
            item_name = input("Введите название товара: ")
            try:
                price = float(input("Введите новую цену товара: "))
                store.update_price(item_name, price)
                manager.save_stores()
            except ValueError:
                print("Пожалуйста, введите корректное значение цены.")

        elif choice == "4":
            item_name = input("Введите название товара: ")
            price = store.get_price(item_name)
            if price is not None:
                print(f"Цена товара '{item_name}': {price}")
            else:
                print(f"Товар '{item_name}' не найден.")

        elif choice == "5":
            if not store.items:
                print("Ассортимент магазина пуст.")
            else:
                print("Ассортимент магазина:")
                for item_name, price in store.items.items():
                    print(f"- {item_name}: {price}")

        elif choice == "6":
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()