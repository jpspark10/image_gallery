import sqlite3
import os


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


def add_image_to_db(name: str):
    """
    Считывает файл (изображение) как двоичные данные и добавляет в таблицу images.
    Использует освобожденный ID, если такой имеется.
    Возвращает ID добавленной записи.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    with open(name, 'rb') as f:
        blob_data = f.read()

    name = os.path.basename(name)
    cursor.execute("INSERT INTO images (name, data) VALUES (?, ?)", (name, blob_data))
    image_id = cursor.lastrowid

    conn.commit()

    conn.close()
    return image_id


def get_all_images():
    """
    Возвращает список кортежей (id, name, data) для всех изображений в БД.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, data FROM images ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_image_from_db(image_id: int):
    """
    Удаляет запись из таблицы images и сохраняет ID в таблице deleted_ids.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
        conn.commit()
    except Exception as e:
        print(str(e))
    conn.close()


def insert_image(name, data):
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO images (name, data) VALUES (?, ?)", (name, data))
    conn.commit()
    conn.close()
