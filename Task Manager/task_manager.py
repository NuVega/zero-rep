import json

class Task:
    def __init__(self, description, due_date, status=False):
        """
        Конструктор задачи.
        """
        self.description = description
        self.due_date = due_date
        self.status = status  # False - невыполнено, True - выполнено

    def mark_complete(self):
        """
        Отметить задачу как выполненную.
        """
        self.status = True

    def to_dict(self):
        """
        Преобразовать задачу в словарь для сохранения в JSON.
        """
        return {
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """
        Создать задачу из словаря (при загрузке из JSON).
        """
        return Task(data["description"], data["due_date"], data["status"])


class TaskManager:
    def __init__(self, filename="tasks.json"):
        """
        Конструктор менеджера задач.
        """
        self.filename = filename
        self.tasks = self.load_tasks()

    def save_tasks(self):
        """
        Сохранить задачи в файл JSON.
        """
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4, ensure_ascii=False)

    def load_tasks(self):
        """
        Загрузить задачи из файла JSON.
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Task.from_dict(task) for task in data]
        except FileNotFoundError:
            return []

    def add_task(self, description, due_date):
        """
        Добавить новую задачу.
        """
        self.tasks.append(Task(description, due_date))
        self.save_tasks()
        print("Задача добавлена.")

    def list_tasks(self):
        """
        Показать все задачи.
        """
        if not self.tasks:
            print("Список задач пуст.")
        else:
            for idx, task in enumerate(self.tasks, start=1):
                status = "✅ Выполнено" if task.status else "❌ Не выполнено"
                print(f"{idx}. {task.description} (до {task.due_date}) - {status}")

    def list_incomplete_tasks(self):
        """
        Показать только невыполненные задачи.
        """
        incomplete_tasks = [task for task in self.tasks if not task.status]
        if not incomplete_tasks:
            print("Все задачи выполнены.")
        else:
            for idx, task in enumerate(incomplete_tasks, start=1):
                print(f"{idx}. {task.description} (до {task.due_date})")

    def mark_task_complete(self, task_index):
        """
        Отметить задачу как выполненную.
        """
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].mark_complete()
            self.save_tasks()
            print("Задача отмечена как выполненная.")
        else:
            print("Неверный номер задачи.")

    def remove_task(self, task_index):
        """
        Удалить задачу.
        """
        if 0 <= task_index < len(self.tasks):
            removed_task = self.tasks.pop(task_index)
            self.save_tasks()
            print(f"Задача '{removed_task.description}' удалена.")
        else:
            print("Неверный номер задачи.")


def main():
    manager = TaskManager()

    while True:
        print("\nМеню:")
        print("1. Добавить задачу")
        print("2. Показать все задачи")
        print("3. Показать невыполненные задачи")
        print("4. Отметить задачу как выполненную")
        print("5. Удалить задачу")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            description = input("Введите описание задачи: ")
            due_date = input("Введите срок выполнения (YYYY-MM-DD): ")
            manager.add_task(description, due_date)

        elif choice == "2":
            manager.list_tasks()

        elif choice == "3":
            manager.list_incomplete_tasks()

        elif choice == "4":
            manager.list_tasks()
            try:
                task_index = int(input("Введите номер задачи для отметки как выполненной: ")) - 1
                manager.mark_task_complete(task_index)
            except ValueError:
                print("Неверный ввод. Введите номер задачи.")

        elif choice == "5":
            manager.list_tasks()
            try:
                task_index = int(input("Введите номер задачи для удаления: ")) - 1
                manager.remove_task(task_index)
            except ValueError:
                print("Неверный ввод. Введите номер задачи.")

        elif choice == "6":
            print("Спасибо за использование менеджера задач!")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()