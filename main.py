import sys
from PyQt5.QtWidgets import QApplication
from assets.gallery_window import GalleryWindow
from database.database import init_db


def main():
    # Инициализируем базу данных перед запуском приложения
    init_db()
    # остальные приколюхи
    app = QApplication(sys.argv)
    window = GalleryWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
