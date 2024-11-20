from datetime import datetime


class Task:
    def __init__(self, description, deadline):
        """
        Инициализация задачи.
        :param description: Описание задачи.
        :param deadline: Срок выполнения задачи в формате 'YYYY-MM-DD'.
        """
        self.description = description
        self.deadline = datetime.strptime(deadline, '%Y-%m-%d')
        self.completed = False

    def mark_completed(self):
        """Отметить задачу как выполненную."""
        self.completed = True

    def __str__(self):
        """Вернуть строковое представление задачи."""
        status = "✅ Выполнено" if self.completed else "❌ Не выполнено"
        return f"{self.description} (до {self.deadline.strftime('%Y-%m-%d')}) — {status}"


class TaskManager:
    def __init__(self):
        """Инициализация менеджера задач."""
        self.tasks = []

    def add_task(self, description, deadline):
        """Добавить новую задачу."""
        task = Task(description, deadline)
        self.tasks.append(task)
        print(f"Задача '{description}' добавлена.")

    def mark_task_completed(self, index):
        """Отметить задачу как выполненную по индексу."""
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            print(f"Задача '{self.tasks[index].description}' отмечена как выполненная.")
        else:
            print("Ошибка: Задача с таким индексом не найдена.")

    def list_tasks(self, show_completed=False):
        """Вывести список задач."""
        tasks_to_show = [
            task for task in self.tasks
            if show_completed or not task.completed
        ]
        if not tasks_to_show:
            print("\nЗадач пока нет.")
            return

        print("\nСписок задач:")
        for i, task in enumerate(tasks_to_show):
            print(f"{i}: {task}")
        print()


def main():
    manager = TaskManager()

    while True:
        print("\nМеню:")
        print("1. Добавить задачу")
        print("2. Отметить задачу как выполненную")
        print("3. Показать текущие задачи")
        print("4. Показать все задачи")
        print("5. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            description = input("Введите описание задачи: ")
            deadline = input("Введите срок выполнения (YYYY-MM-DD): ")
            try:
                manager.add_task(description, deadline)
            except ValueError:
                print("Ошибка: неверный формат даты. Используйте формат YYYY-MM-DD.")
        elif choice == "2":
            manager.list_tasks(show_completed=False)
            index = input("Введите индекс задачи, которую хотите отметить выполненной: ")
            if index.isdigit():
                manager.mark_task_completed(int(index))
            else:
                print("Ошибка: индекс должен быть числом.")
        elif choice == "3":
            manager.list_tasks(show_completed=False)
        elif choice == "4":
            manager.list_tasks(show_completed=True)
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Ошибка: выберите корректный пункт меню.")


if __name__ == "__main__":
    main()