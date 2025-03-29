from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.uic import loadUi

from assets.resource_path import resource_path
from database.database import get_all_images, add_image_to_db, delete_image_from_db


class ImageManagerDialog(QDialog):
    def __init__(self, parent, images):

        super().__init__(parent)
        # Загружаем интерфейс из UI-файла
        loadUi(resource_path("ui/image_manager.ui"), self)

        self.images = images  # [(id, name, data), ...]
        self.populate_list()

        # Привязываем кнопки, созданные в дизайнере
        self.btnAdd.clicked.connect(self.add_image)
        self.btnRemove.clicked.connect(self.delete_selected)
        self.btnClose.clicked.connect(self.close)

    def populate_list(self):
        self.listImages.clear()
        for img_id, img_name, _ in self.images:
            self.listImages.addItem(f"{img_name}")

    def add_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            try:
                add_image_to_db(file_path)
                self.images = get_all_images()
                self.populate_list()
            except Exception as e:
                print(str(e))

    def delete_selected(self):
        current_item = self.listImages.currentItem()
        if not current_item:
            return

        img_name = current_item.text()  # Получаем имя файла

        # Ищем ID по имени
        for img_id, name, _ in self.images:
            if name == img_name:
                delete_image_from_db(img_id)
                self.images = get_all_images()  # Запрашиваем актуальный список изображений
                self.populate_list()  # Перерисовываем список
                return
