from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QTransform, QKeySequence
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QShortcut

from assets.image_manager import ImageManagerDialog
from assets.resource_path import resource_path
from database.database import get_all_images, add_image_to_db, delete_image_from_db


class GalleryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(resource_path("ui/main_window.ui"), self)

        self.setWindowTitle("Галерея изображений")

        # Список кортежей (id, name, data)
        self.images = []
        self.current_index = -1

        # Для трансформаций
        self.original_pixmap = None  # Исходное изображение без трансформаций
        self.current_angle = 0  # Угол поворота
        self.current_scale = 1.0  # Масштаб

        # Подключаем действия из меню
        self.actionOpen.triggered.connect(self.open_images)
        self.actionExit.triggered.connect(self.close)
        self.actionManage.triggered.connect(self.open_manager_window)

        # Подключаем кнопки
        self.btnPrev.clicked.connect(self.show_prev_image)
        self.btnNext.clicked.connect(self.show_next_image)
        self.btnDelete.clicked.connect(self.delete_current_image)
        self.btnZoomIn.clicked.connect(self.zoom_in)
        self.btnZoomOut.clicked.connect(self.zoom_out)

        # Слайдер поворота
        self.sliderRotate.valueChanged.connect(self.rotate_image)
        # Добавляем обработку двойного клика по ползунку для сброса
        self.sliderRotate.installEventFilter(self)
        self.sliderRotate.setVisible(False)  # Скрываем до загрузки изображения

        # Хоткеи
        QShortcut(QKeySequence(Qt.Key_Delete), self, self.delete_current_image)
        QShortcut(QKeySequence(Qt.Key_Minus), self, self.zoom_out)
        QShortcut(QKeySequence(Qt.Key_Plus), self, self.zoom_in)
        QShortcut(QKeySequence(Qt.Key_Left), self, self.show_prev_image)
        QShortcut(QKeySequence(Qt.Key_Right), self, self.show_next_image)

        self.statusBar().showMessage("Готов к работе")

        # Загружаем существующие изображения из БД
        self.load_images_from_db()

    def load_images_from_db(self):
        """
        Считывает все изображения из БД и подготавливает их к отображению.
        """
        self.images = get_all_images()  # [(id, name, data), ...]
        if self.images:
            self.current_index = 0
            self.load_current_image()
        else:
            self.labelWelcome.setText("Нет изображений в базе данных.")
            self.sliderRotate.setVisible(False)

    def open_images(self):
        """
        Открывает диалог выбора изображений, добавляет их в БД.
        """
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Выберите изображения",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_paths:
            for file_path in file_paths:
                add_image_to_db(file_path)

            # Перезагружаем список из БД
            self.load_images_from_db()
            self.statusBar().showMessage(f"Добавлено изображений: {len(file_paths)}")
        else:
            self.statusBar().showMessage("Изображения не выбраны")

    def load_current_image(self):
        """
        Загружает текущее изображение (из BLOB) и сбрасывает трансформации.
        """
        if 0 <= self.current_index < len(self.images):
            image_id, image_name, blob_data = self.images[self.current_index]
            pixmap = QPixmap()
            success = pixmap.loadFromData(blob_data)
            if success:
                self.original_pixmap = pixmap
                self.current_angle = 0
                self.current_scale = 1.0
                self.sliderRotate.setValue(0)
                self.sliderRotate.setVisible(True)
                self.update_display_image()
                self.labelWelcome.setText(f"Просмотр: {image_name}")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение из БД.")
        else:
            self.labelImage.clear()
            self.labelWelcome.setText("Нет изображений для отображения.")
            self.sliderRotate.setVisible(False)

    def update_display_image(self):
        """
        Применяет текущие трансформации (поворот и масштаб) к оригинальному изображению и отображает его.
        """
        if self.original_pixmap is None:
            return

        transform = QTransform().rotate(self.current_angle).scale(self.current_scale, self.current_scale)
        transformed = self.original_pixmap.transformed(transform, Qt.SmoothTransformation)
        self.display_image(transformed)

    def display_image(self, pixmap: QPixmap):
        """
        Отображает QPixmap в labelImage.
        """
        self.labelImage.setPixmap(pixmap)

    def rotate_image(self):
        """
        Обновляет угол поворота из ползунка и применяет трансформацию.
        """
        if self.original_pixmap is None:
            return

        self.current_angle = self.sliderRotate.value()
        self.update_display_image()

    def zoom_in(self):
        """
        Увеличивает масштаб изображения.
        """
        if self.original_pixmap is None:
            return
        self.current_scale += 0.1
        self.update_display_image()

    def zoom_out(self):
        """
        Уменьшает масштаб изображения, но не меньше 0.1.
        """
        if self.original_pixmap is None:
            return
        self.current_scale = max(0.1, self.current_scale - 0.1)
        self.update_display_image()

    def show_next_image(self):
        """
        Переход к следующему изображению.
        """
        if not self.images:
            QMessageBox.information(self, "Информация", "Нет загруженных изображений.")
            return
        self.current_index = (self.current_index + 1) % len(self.images)
        self.load_current_image()

    def show_prev_image(self):
        """
        Переход к предыдущему изображению.
        """
        if not self.images:
            QMessageBox.information(self, "Информация", "Нет загруженных изображений.")
            return
        self.current_index = (self.current_index - 1) % len(self.images)
        self.load_current_image()

    def delete_current_image(self):
        """
        Удаляет текущее изображение из БД.
        """
        if not self.images:
            QMessageBox.information(self, "Информация", "Нет загруженных изображений.")
            return

        image_id, image_name, _ = self.images[self.current_index]
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Удалить файл из БД?\n{image_name} (ID: {image_id})",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            delete_image_from_db(image_id)
            # Обновим список изображений
            self.images = get_all_images()
            if self.images:
                self.current_index = max(0, self.current_index - 1)
                self.load_current_image()
            else:
                self.current_index = -1
                self.labelImage.clear()
                self.labelWelcome.setText("Все изображения удалены.")
                self.sliderRotate.setVisible(False)

    def open_manager_window(self):
        """
        Открывает окно для управления списком изображений.
        """
        dialog = ImageManagerDialog(self, self.images)
        dialog.exec_()
        # В случае изменений в диалоге — обновим список
        self.images = get_all_images()
        if self.images:
            self.current_index = min(self.current_index, len(self.images) - 1)
            if self.current_index < 0:
                self.current_index = 0
            self.load_current_image()
        else:
            self.current_index = -1
            self.labelImage.clear()
            self.labelWelcome.setText("Все изображения удалены.")
            self.sliderRotate.setVisible(False)

    def eventFilter(self, obj, event):
        """
        Обрабатывает двойной клик по ползунку для сброса угла поворота.
        """
        if obj == self.sliderRotate and event.type() == QEvent.MouseButtonDblClick:
            self.sliderRotate.setValue(0)
            return True
        return super().eventFilter(obj, event)
