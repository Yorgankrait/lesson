from django.db import migrations

def add_more_articles(apps, schema_editor):
    TeacherArticle = apps.get_model('main_app', 'TeacherArticle')
    
    # Статья про Google Classroom
    classroom_article = TeacherArticle.objects.create(
        title='Использование Google Classroom в обучении',
        content='''
# Google Classroom для учителей

Google Classroom - это бесплатный веб-сервис для школ, который призван упростить создание, распространение и оценку заданий безбумажным способом.

## Основные преимущества:

1. Простая настройка
- Преподаватели могут организовывать курсы, приглашать учащихся и других преподавателей
- В структуре курса можно создавать темы, задания, публиковать объявления

2. Экономия времени
- Простой процесс регистрации
- Интеграция с Google Docs
- Автома��ическое создание копий документов для каждого учащегося

3. Удобная организация
- Материалы курса автоматически добавляются в структурированные папки на Google Drive
- Все задания отображаются на главной странице
- Преподаватели могут отслеживать работу над каждым заданием

4. Быстрая коммуникация
- Возможность публиковать объявления и задавать вопросы
- Комментирование заданий в реальном времени
- Отправка личных сообщений

## Как начать работу:

1. Войдите в свой аккаунт Google
2. Перейдите на classroom.google.com
3. Создайте свой первый курс
4. Пригласите учеников по электронной почте или коду курса

## Советы по использованию:

- Создавайте четкую структуру курса
- Используйте разные типы заданий
- Добавляйте сроки выполнения
- Регулярно проверя��те работы учеников
- Давайте конструктивную обратную связь
        ''',
        is_published=True
    )

    # Статья про Python в школе
    python_article = TeacherArticle.objects.create(
        title='Методика преподавания Python в школе',
        content='''
# Преподавание Python в школе

Python является одним из лучших языков программирования для начинающих благодаря своему простому и понятному синтаксису.

## Почему Python?

1. Простой синтаксис
- Код читается как обычный английский текст
- Минимум специальных символов
- Понятная структура кода

2. Широкие возможности
- Создание игр
- Работа с данными
- Веб-разработка
- Автоматизация задач

## Структура обучения:

### Начальный уровень:
1. Основы синтаксиса
2. Переменные и типы данных
3. Условные операторы
4. Циклы

### Средний уровень:
1. Функции
2. Списки и словари
3. Работа с файлами
4. Основы ООП

### Продвинутый уровень:
1. Библиотеки и модули
2. Создание проектов
3. Работа с API
4. Базы данных

## Практические советы:

1. Начинайте с простых задач
2. Используйте визуальные примеры
3. Поощряйте самостоятельные проекты
4. Организуйте командную работу
5. Проводите код-ревью

## Полезные ресурсы:

- Python.org - официальная документация
- Pythontutor - визуализация выполнения кода
- Codecademy - интерактивные уроки
- GitHub - хранение проектов
        ''',
        is_published=True
    )

def reverse_func(apps, schema_editor):
    TeacherArticle = apps.get_model('main_app', 'TeacherArticle')
    TeacherArticle.objects.filter(
        title__in=[
            'Использование Google Classroom в обучении',
            'Методика преподавания Python в школе'
        ]
    ).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0016_add_printer_article_data'),
    ]

    operations = [
        migrations.RunPython(add_more_articles, reverse_func),
    ] 