import sqlite3
import os
import sys


def get_db_path():
    # Путь к папке db (считаем, что программа будет работать из текущей директории)
    db_dir = os.path.join(os.path.abspath("."), "db")

    # Проверяем, существует ли папка db
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)  # Если нет, создаем

    # Возвращаем путь к файлу базы данных внутри этой папки
    db_path = os.path.join(db_dir, "gallery.db")

    return db_path


DB_NAME = get_db_path()


# Функция для создания бд
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Создаем таблицу для хранения изображений
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            data BLOB
        )
    """)

    conn.commit()
    conn.close()


# Запуск инициализации
if __name__ == "__main__":
    init_db()
