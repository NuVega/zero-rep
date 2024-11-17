import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json
import os

# Глобальные переменные
tasks_data = []
task_id_counter = 0
categories = []
category_trees = {}
previous_tab = None
deleting_category = False  # Флаг, указывающий на процесс удаления категории
drag_data = {"task_id": None, "widget": None, "category": None, "y": 0}

def save_categories():
    with open("categories.json", "w", encoding='utf-8') as file:
        json.dump(categories, file, ensure_ascii=False)

def load_categories():
    global categories
    if os.path.exists("categories.json"):
        with open("categories.json", "r", encoding='utf-8') as file:
            categories = json.load(file)
    else:
        categories = ["Дом", "Работа", "Личное"]

def add_category_tab(category_name, insert_before_plus=True):
    frame = ttk.Frame(notebook)
    tree = ttk.Treeview(frame, columns=("Task", "Priority", "Status"), show="headings")
    tree.heading("Task", text="Задача")
    tree.heading("Priority", text="Приоритет")
    tree.heading("Status", text="Статус")

    tree.column("Task", width=200, anchor="w")
    tree.column("Priority", width=100, anchor="w")
    tree.column("Status", width=100, anchor="w")

    tree.pack(fill="both", expand=True)
    category_trees[category_name] = tree

    # Проверяем наличие вкладки "+"
    tab_ids = notebook.tabs()
    plus_tab_present = any(notebook.tab(tab_id, "text") == "+" for tab_id in tab_ids)

    if insert_before_plus and plus_tab_present:
        index = notebook.index("end") - 1
        notebook.insert(index, frame, text=category_name)
    else:
        notebook.add(frame, text=category_name)

    # Привязываем событие выбора к функции обновления текста кнопки
    tree.bind('<<TreeviewSelect>>', update_mark_button_text)

def on_tab_changed(event):
    global previous_tab, deleting_category
    selected_tab = notebook.select()
    tab_text = notebook.tab(selected_tab, "text")

    if tab_text == "+":
        # Проверяем, не происходит ли сейчас удаление категории
        if deleting_category:
            # Сбрасываем флаг после обработки события
            deleting_category = False
            previous_tab = selected_tab
            return  # Не открываем диалоговое окно

        new_category_name = simpledialog.askstring("Новая категория", "Введите название новой категории:")
        if new_category_name:
            if new_category_name in category_trees:
                messagebox.showerror("Ошибка", "Категория с таким названием уже существует.")
                notebook.select(previous_tab)
            else:
                add_category_tab(new_category_name)
                categories.append(new_category_name)
                save_categories()
                # Переключаемся на новую вкладку
                notebook.select(notebook.tabs()[-2])
        else:
            # Если пользователь нажал "Отмена", возвращаемся на предыдущую вкладку
            notebook.select(previous_tab)
    else:
        previous_tab = selected_tab

def load_tasks():
    global tasks_data, task_id_counter, previous_tab

    # Инициализируем previous_tab
    previous_tab = None

    # Загружаем категории
    load_categories()

    # Создаем вкладки с задачами для каждой категории
    for category in categories:
        add_category_tab(category, insert_before_plus=False)

    # Добавляем вкладку "+"
    plus_tab = ttk.Frame(notebook)
    notebook.add(plus_tab, text="+")

    previous_tab = notebook.tabs()[0]  # Идентификатор первой вкладки

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    # Загрузка задач
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r", encoding='utf-8') as file:
            tasks_data = json.load(file)
            if tasks_data:
                max_id = max(task['id'] for task in tasks_data)
                task_id_counter = max_id + 1
            else:
                task_id_counter = 0
    else:
        tasks_data = []
    update_task_list()

# Сохранение задач в файл
def save_tasks():
    with open("tasks.json", "w", encoding='utf-8') as file:
        json.dump(tasks_data, file, ensure_ascii=False)

# Получение символа приоритета
def get_priority_symbol(priority):
    symbols = {
        "High": "🔴 High",
        "Medium": "🟠 Medium",
        "Low": "🟢 Low"
    }
    return symbols.get(priority, priority)

# Обновление отображения задач в интерфейсе
def update_task_list():
    for tree in category_trees.values():
        # Настраиваем цвет текста для выполненных задач
        tree.tag_configure('completed', foreground='grey')

        for item in tree.get_children():
            tree.delete(item)

    for task in tasks_data:
        task_id = task["id"]
        text = task["text"]
        completed = task["completed"]
        priority = task.get("priority", "Medium")
        category = task.get("category", "Дом")
        if category not in category_trees:
            continue  # Пропускаем задачи из удаленных категорий
        tree = category_trees[category]

        # Получаем символ приоритета
        priority_text = get_priority_symbol(priority)

        # Статус задачи
        status_text = "Выполнено" if completed else "Активно"

        # Отображаем только текст задачи без изменений
        text_display = text

        # Определяем тег на основе статуса задачи
        tags = ('completed',) if completed else ()

        # Вставляем задачу с соответствующим тегом
        tree.insert(
            "", "end", iid=str(task_id),
            values=(text_display, priority_text, status_text),
            tags=tags
        )

def add_task():
    global task_id_counter
    task_text = task_entry.get()
    priority = priority_var.get()
    category = notebook.tab(notebook.select(), "text")
    if task_text and category != "+":
        task = {
            "id": task_id_counter,
            "text": task_text,
            "completed": False,
            "priority": priority,
            "category": category
        }
        tasks_data.append(task)
        task_id_counter += 1  # Увеличиваем счетчик после добавления задачи
        update_task_list()
        task_entry.delete(0, tk.END)
        save_tasks()
        update_mark_button_text()  # Обновляем текст кнопки

def delete_task():
    category = notebook.tab(notebook.select(), "text")
    if category == "+":
        return
    tree = category_trees[category]
    selected_item = tree.selection()
    if selected_item:
        if messagebox.askyesno("Подтверждение удаления", "Вы уверены, что хотите удалить выбранную задачу?"):
            task_id = int(selected_item[0])
            # Удаляем задачу из tasks_data
            for task in tasks_data:
                if task["id"] == task_id:
                    tasks_data.remove(task)
                    break
            update_task_list()
            save_tasks()
            update_mark_button_text()  # Обновляем текст кнопки

def mark_task():
    category = notebook.tab(notebook.select(), "text")
    if category == "+":
        return
    tree = category_trees[category]
    selected_item = tree.selection()
    if selected_item:
        task_id = int(selected_item[0])
        # Обновляем статус задачи в tasks_data
        for task in tasks_data:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break
        update_task_list()
        save_tasks()
        update_mark_button_text()  # Обновляем текст кнопки

def open_edit_task_window(task):
    edit_window = tk.Toplevel(root)
    edit_window.title("Редактировать задачу")

    tk.Label(edit_window, text="Текст задачи:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    text_var = tk.StringVar(value=task["text"])
    text_entry = ttk.Entry(edit_window, textvariable=text_var, width=30)
    text_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(edit_window, text="Приоритет:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    priority_var = tk.StringVar(value=task.get("priority", "Medium"))
    priority_menu = ttk.Combobox(edit_window, textvariable=priority_var, values=["High", "Medium", "Low"], state="readonly", width=10)
    priority_menu.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(edit_window, text="Категория:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    category_var = tk.StringVar(value=task.get("category", "Дом"))
    category_menu = ttk.Combobox(edit_window, textvariable=category_var, values=categories, state="readonly", width=15)
    category_menu.grid(row=2, column=1, padx=5, pady=5)

    def save_changes():
        task["text"] = text_var.get()
        task["priority"] = priority_var.get()
        old_category = task["category"]
        new_category = category_var.get()
        task["category"] = new_category
        task["completed"] = task.get("completed", False)

        if old_category != new_category:
            update_task_list()
        else:
            update_task_in_tree(task)

        save_tasks()
        edit_window.destroy()

    save_button = ttk.Button(edit_window, text="Сохранить", command=save_changes)
    save_button.grid(row=3, column=0, columnspan=2, pady=10)

    edit_window.grab_set()

def edit_task():
    category = notebook.tab(notebook.select(), "text")
    if category == "+":
        return
    tree = category_trees[category]
    selected_item = tree.selection()
    if selected_item:
        task_id = int(selected_item[0])
        # Находим задачу в tasks_data
        for task in tasks_data:
            if task["id"] == task_id:
                open_edit_task_window(task)
                break

def update_task_in_tree(task):
    task_id = task["id"]
    text = task["text"]
    completed = task["completed"]
    priority = task.get("priority", "Medium")
    category = task.get("category", "Дом")
    tree = category_trees[category]

    # Получаем символ приоритета
    priority_text = get_priority_symbol(priority)

    # Статус задачи
    status_text = "Выполнено" if completed else "Активно"

    # Отображаем только текст задачи без изменений
    text_display = text

    # Определяем тег на основе статуса задачи
    tags = ('completed',) if completed else ()

    # Обновляем задачу в Treeview
    tree.item(str(task_id), values=(text_display, priority_text, status_text), tags=tags)

def sort_tasks_alphabetically():
    tasks_data.sort(key=lambda x: x["text"])
    update_task_list()
    save_tasks()

def sort_tasks_by_addition():
    tasks_data.sort(key=lambda x: x["id"])
    update_task_list()
    save_tasks()

def update_mark_button_text(event=None):
    category = notebook.tab(notebook.select(), "text")
    if category == "+":
        return
    tree = category_trees[category]
    selected_item = tree.selection()
    if selected_item:
        task_id = int(selected_item[0])
        # Находим задачу в tasks_data
        for task in tasks_data:
            if task["id"] == task_id:
                if task["completed"]:
                    mark_button.configure(text="Вернуть в активные")
                else:
                    mark_button.configure(text="Отметить как выполненное")
                break
    else:
        # Если ничего не выбрано, устанавливаем текст по умолчанию
        mark_button.configure(text="Отметить как выполненное")

def delete_category():
    global categories, deleting_category
    category = notebook.tab(notebook.select(), "text")
    if category == "+":
        messagebox.showerror("Ошибка", "Нельзя удалить эту вкладку.")
        return

    if messagebox.askyesno("Удалить категорию", f"Вы уверены, что хотите удалить категорию '{category}' и все связанные с ней задачи?"):
        deleting_category = True  # Устанавливаем флаг

        # Удаляем задачи, связанные с категорией
        global tasks_data
        tasks_data = [task for task in tasks_data if task["category"] != category]
        save_tasks()

        # Удаляем вкладку категории
        tab_id = notebook.select()
        notebook.forget(tab_id)

        # Удаляем категорию из списка и сохраняем
        categories.remove(category)
        save_categories()

        # Удаляем запись из category_trees
        del category_trees[category]

        # Обновляем интерфейс
        update_task_list()

        # Не сбрасываем флаг здесь

        # Переключаемся на другую вкладку, если категории остались
        if categories:
            notebook.select(notebook.tabs()[0])  # Переключаемся на первую вкладку
        else:
            # Если категорий не осталось, переключаемся на вкладку "+"
            notebook.select(notebook.tabs()[-1])

        messagebox.showinfo("Категория удалена", f"Категория '{category}' и все связанные задачи удалены.")

# Инициализация основного окна
root = tk.Tk()
root.title("Task List")

style = ttk.Style()
style.theme_use('clam')

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

task_frame = ttk.Frame(main_frame)
task_frame.pack(fill="x", pady=5)

task_label = ttk.Label(task_frame, text="Введите вашу задачу:")
task_label.pack(side="left", padx=5)

task_entry = ttk.Entry(task_frame, width=30)
task_entry.pack(side="left", padx=5)

priority_label = ttk.Label(task_frame, text="Приоритет:")
priority_label.pack(side="left", padx=5)

priority_var = tk.StringVar(value="Medium")
priority_menu = ttk.Combobox(task_frame, textvariable=priority_var, values=["High", "Medium", "Low"], state="readonly", width=10)
priority_menu.pack(side="left", padx=5)

add_task_button = ttk.Button(task_frame, text="Добавить задачу", command=add_task)
add_task_button.pack(side="left", padx=5)

button_frame = ttk.Frame(main_frame)
button_frame.pack(fill="x", pady=5)

edit_button = ttk.Button(button_frame, text="Редактировать", command=edit_task)
edit_button.pack(side="left", padx=5)

delete_button = ttk.Button(button_frame, text="Удалить", command=delete_task)
delete_button.pack(side="left", padx=5)

mark_button = ttk.Button(button_frame, text="Отметить как выполненное", command=mark_task)
mark_button.pack(side="left", padx=5)

delete_category_button = ttk.Button(button_frame, text="Удалить категорию", command=delete_category)
delete_category_button.pack(side="left", padx=5)

sort_alpha_button = ttk.Button(button_frame, text="Сортировать по алфавиту", command=sort_tasks_alphabetically)
sort_alpha_button.pack(side="left", padx=5)

sort_add_button = ttk.Button(button_frame, text="Сортировать по добавлению", command=sort_tasks_by_addition)
sort_add_button.pack(side="left", padx=5)

# Добавляем Notebook для категорий
notebook = ttk.Notebook(main_frame)
notebook.pack(fill="both", expand=True, pady=5)

# Загрузка задач при запуске программы
load_tasks()
update_mark_button_text()

root.mainloop()