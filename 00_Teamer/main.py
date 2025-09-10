import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def init_db():
    with sqlite3.connect('business_orders.db') as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            order_details TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Новый' CHECK(status IN ('Новый','Завершён')),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """)


def add_order():
    name = customer_name_entry.get().strip()
    # берём текст и игнорируем плейсхолдер
    raw = order_details_text.get("1.0", "end-1c")
    details = raw.strip()
    if details == PLACEHOLDER:
        details = ""

    if not name or not details:
        messagebox.showerror("Ошибка", "Имя и детали заказа обязательны")
        return
    try:
        with sqlite3.connect('business_orders.db') as conn:
            conn.execute(
                "INSERT INTO orders (customer_name, order_details) VALUES (?, ?)",
                (name, details)
            )
    except Exception as e:
        messagebox.showerror("Ошибка БД", str(e))
        return
    # очистка полей и возврат плейсхолдера
    customer_name_entry.delete(0, tk.END)
    order_details_text.delete("1.0", "end")
    _apply_placeholder()  # функция, которую мы добавляли для плейсхолдера
    view_orders()
    app.update_idletasks()  # форс перерисовки до модального окна
    messagebox.showinfo("Готово", "Заказ добавлен")


def view_orders():
    tree.delete(*tree.get_children())  # одномоментно удалить все строки
    with sqlite3.connect('business_orders.db') as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, customer_name, order_details, status
            FROM orders
            ORDER BY created_at DESC
        """)
        for row in cur:  # итерируем курсор, без fetchall (меньше памяти на больших выборках)
            tag = "done" if row[3] == "Завершён" else "new"
            tree.insert("", tk.END, values=row, tags=(tag,))


def complete_order():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Предупреждение", "Выберите заказ для завершения")
        return
    item_id = selected[0]
    order_id = tree.item(item_id, 'values')[0]
    with sqlite3.connect('business_orders.db') as conn:
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status='Завершён' WHERE id=?", (order_id,))
    view_orders()
    app.update_idletasks()
    app.update_idletasks()  # форс перерисовки до модального окна
    messagebox.showinfo("Готово", f"Заказ #{order_id} завершён")


def toggle_status(event):
    sel = tree.selection()
    if not sel:
        return
    item = sel[0]
    order_id, _, _, status = tree.item(item, "values")
    order_id = int(order_id)  # ← опционально
    new_status = "Новый" if status == "Завершён" else "Завершён"
    with sqlite3.connect('business_orders.db') as conn:
        conn.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))
    view_orders()


def db_safe(fn):
    def wrap(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            messagebox.showerror("Ошибка БД", str(e))
    return wrap


PLACEHOLDER = "Опишите заказ: позиции, количество, комментарии…"

def _apply_placeholder():
    order_details_text.insert("1.0", PLACEHOLDER)
    order_details_text.config(fg="grey")

def _on_focus_in(event):
    if order_details_text.get("1.0", "end-1c") == PLACEHOLDER:
        order_details_text.delete("1.0", "end")
        order_details_text.config(fg="white")

def _on_focus_out(event):
    if not order_details_text.get("1.0", "end-1c").strip():
        _apply_placeholder()


add_order    = db_safe(add_order)
complete_order = db_safe(complete_order)
view_orders  = db_safe(view_orders)


app = tk.Tk()
app.title("Система управления заказами")

# стабильная тема (аqua на macOS любит переопределять цвета)
style = ttk.Style()
try:
    style.theme_use("clam")
except Exception:
    pass

# базовые цвета грида + что делать при выделении
style.configure(
    "Treeview",
    background="#1e1e1e",
    fieldbackground="#1e1e1e",
    foreground="#ffffff",
)
style.map(
    "Treeview",
    background=[("selected", "#3a3a3a")],
    foreground=[("selected", "#ffffff")],
)

tk.Label(app, text="Имя клиента").pack(anchor="center", pady=(8, 0))

customer_name_entry = tk.Entry(app, width=40, justify="center")
customer_name_entry.pack(anchor="center", pady=4)

tk.Label(app, text="Детали заказа").pack(anchor="center", pady=(8, 0))

order_details_text = tk.Text(
    app,
    height=4,
    width=60,
    wrap="word",
    relief="groove",
    borderwidth=2,
    bg="#1e1e1e",           # явный тёмный фон
    fg="#ffffff",           # белый текст
    insertbackground="#ffffff",   # белый курсор
)
# цвета выделения (иначе на тёмном фоне могут сливаться)
order_details_text.config(selectbackground="#3a3a3a", selectforeground="#ffffff")
order_details_text.pack(anchor="center", pady=4)

_apply_placeholder()
order_details_text.bind("<FocusIn>", _on_focus_in)
order_details_text.bind("<FocusOut>", _on_focus_out)

add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()

complete_button = tk.Button(app, text="Завершить заказ", command=complete_order)
complete_button.pack()

frame = ttk.Frame(app)
frame.pack(fill="both", expand=True)

columns = ("id","customer_name","order_details","status")
tree = ttk.Treeview(frame, columns=columns, show="headings")
vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)

tree.column("id", width=60, anchor="w")
tree.column("customer_name", width=180, anchor="w")
tree.column("order_details", width=360, anchor="w")
tree.column("status", width=120, anchor="w")

tree.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky="ns")
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

tree.tag_configure("done", foreground="#A0A0A0")
tree.tag_configure("new",  foreground="#FFFFFF")

tree.bind("<Double-1>", toggle_status)


init_db()
view_orders()
app.mainloop()