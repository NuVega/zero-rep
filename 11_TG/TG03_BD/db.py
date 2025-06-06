import sqlite3

def init_db():
    conn = sqlite3.connect("school_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            grade TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_student(name, age, grade):
    conn = sqlite3.connect("school_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", (name, age, grade))
    conn.commit()
    conn.close()

def get_all_students():
    conn = sqlite3.connect("school_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, age, grade FROM students")
    students = cursor.fetchall()
    conn.close()
    return students

