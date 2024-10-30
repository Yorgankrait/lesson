from django.db import migrations

def create_printer_article(apps, schema_editor):
    TeacherArticle = apps.get_model('main_app', 'TeacherArticle')
    TeacherResource = apps.get_model('main_app', 'TeacherResource')
    
    article = TeacherArticle.objects.create(
        title='Установка и настройка принтера Pantum (учительская)',
        content='''
# Установка и настройка принтера Pantum

В этой статье вы найдете пошаговую инструкцию по установке и настройке принтера Pantum в учительской.

## Необходимые файлы
- Драйвер принтера Pantum
- Скриншоты процесса установки

## Порядок установки:
1. Скачайте и запустите установочный файл драйвера
2. Следуйте инструкциям установщика
3. Подключите принтер к компьютеру
4. Завершите настройку, следуя скриншотам ниже

## Возможные проблемы и их решение
При возникновении проблем с установкой или работой принтера, обратитесь к системному администратору.
        ''',
        is_published=True
    )

class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0015_create_teacher_articles'),
    ]

    operations = [
        migrations.RunPython(create_printer_article),
    ] 