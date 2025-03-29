# Галерея изображений (Image Gallery)

## Описание проекта
Приложение на **PyQt5**, позволяющее:
- Загружать изображения в базу данных (**SQLite**) и просматривать их;
- Добавлять новые изображения, удалять и управлять ими через отдельное окно менеджера;
- Масштабировать и поворачивать изображения (с помощью ползунка и кнопок);
- Использовать горячие клавиши для удобного использования приложения;


## Основные возможности
1. **Просмотр изображений** из базы данных.
2. **Добавление** новых изображений (загружаются как BLOB).
3. **Удаление** выбранных изображений.
4. **Масштабирование** и **поворот** (ползунок и кнопки).
5. **Горячие клавиши**:  
   - Стрелка влево (←) — предыдущее изображение  
   - Стрелка вправо (→) — следующее изображение  
   - Кнопка "Delete" - удаление изображения
   - Кнопка "+" - приближение изображения
   - Кнопка "-" - отдаление изображения
6. **Управление списком** изображений в отдельном диалоговом окне.
7. **Сохранение** изображений в SQLite.




## Установка и запуск

1. **Установка зависимостей**:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Инициализация базы данных (опционально, если нужно создать таблицы с нуля)**:
   ```bash
   python database/init_db.py
   ```
   или
   ```bash 
   python init_db.py
   ```

    (в зависимости от того, где у вас лежит скрипт init_db.py).


2. **Запуск приложения**:
   ```bash
   python main.py
   ```
## Использование

**Главное окно**:

- Кнопки «Назад» и «Вперёд» для переключения изображений.

- Кнопка «Удалить» для удаления текущего изображения из БД.

- Кнопки «Приблизить» и «Отдалить» для масштабирования.

- Ползунок «Поворот (°)» для вращения изображения. Двойной клик по ползунку сбрасывает угол в 0.
![Пример использования](https://i.imgur.com/0AaHeiC.gif)

**Меню «Файл»**:

- «Открыть изображение» — добавить новые файлы в БД.

- «Управление списком» — открыть диалоговое окно, в котором можно просмотреть список изображений, добавить и удалить.

- «Выход» — закрыть приложение.
