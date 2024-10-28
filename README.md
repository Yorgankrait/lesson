# Обучающая платформа Python

Веб-приложение для обучения программированию на Python, разработанное с использованием Django.

## Функциональность

### Для учеников и родителей
- 👥 Просмотр профилей учеников и их проектов
- 📚 Доступ к учебным материалам и презентациям
- 💻 Встроенный Python интерпретатор для практики
- 🤖 Чат-бот помощник
- 📅 Отслеживание посещаемости

### Для администратора
- ✏️ Управление учениками и их проектами
- 📝 Публикация новостей
- 📊 Управление посещаемостью
- 📚 Загрузка учебных материалов
- 💬 Ответы на вопросы через чат-бота

## Технологии

- Python 3.9+
- Django 4.2+
- SQLite
- HTML/CSS/JavaScript
- Bootstrap

## Установка и запуск

### Для Windows:

1. Клонируйте репозиторий:
git clone https://github.com/Yorgankrait/lesson.git
cd lesson

2. Создайте и активируйте виртуальное окружение:
python -m venv venv
.\venv\Scripts\activate

3. Установите зависимости:
pip install -r requirements_windows.txt

4. Примените миграции:
python manage.py migrate

5. Создайте суперпользователя:
python manage.py createsuperuser

6. Запустите сервер:
python manage.py runserver


### Для macOS/Linux:

1. Клонируйте репозиторий:
git clone https://github.com/Yorgankrait/lesson.git
cd lesson

2. Создайте и активируйте виртуальное окружение:
python3 -m venv venv
source venv/bin/activate

3. Установите зависимости:
pip install -r requirements.txt

4. Примените миграции:
python manage.py migrate

5. Создайте суперпользователя:
python manage.py createsuperuser


6. Запустите сервер:
python manage.py runserver


## Доступ к приложению

После запуска сервера:
1. Откройте браузер и перейдите по адресу: http://127.0.0.1:8000/
2. Для доступа к админ-панели: http://127.0.0.1:8000/admin/

## Структура проекта

- `main_app/` - основное приложение
  - `templates/` - HTML шаблоны
  - `static/` - статические файлы (CSS, JS, видео)
  - `models.py` - модели данных
  - `views.py` - представления
  - `urls.py` - маршрутизация
- `media/` - загруженные файлы
- `static/` - общие статические файлы
- `requirements.txt` - зависимости для macOS/Linux
- `requirements_windows.txt` - зависимости для Windows

## Лицензия

MIT License

## Автор

Сергей Жуков
