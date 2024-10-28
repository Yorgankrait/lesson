from django.db import models
from django.utils.dateformat import format
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_pptx(value):
    if not value.name.lower().endswith('.pptx'):
        raise ValidationError('Поддерживаются только файлы с расширением .pptx')

class Lesson(models.Model):
    title = models.CharField('Название', max_length=200)
    presentation = models.FileField('Презентация', upload_to='lessons/', validators=[validate_pptx])
    upload_date = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['-upload_date']

    def __str__(self):
        return self.title

    def formatted_date(self):
        return format(self.upload_date, 'd.m.Y')


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    message = models.TextField('Сообщение')
    is_bot = models.BooleanField('Сообщение бота', default=False)
    timestamp = models.DateTimeField('Время', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение чата'
        verbose_name_plural = 'Сообщения чата'
        ordering = ['timestamp']

class Student(models.Model):
    name = models.CharField('ФИО', max_length=100)
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Проект')
    email = models.EmailField('Email', blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    notes = models.TextField('Заметки', blank=True)
    active = models.BooleanField('Активный', default=True)
    
    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ['name']

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Ученик')
    date = models.DateField('Дата')
    present = models.BooleanField('Присутствовал', default=False)
    no_class = models.BooleanField('Занятия не было', default=False)

    class Meta:
        verbose_name = 'Посещаемость'
        verbose_name_plural = 'Посещаемость'
        unique_together = ['student', 'date']

class UnknownQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    question = models.TextField('Вопрос')
    answer = models.TextField('Ответ', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_answered = models.BooleanField('Отвечен', default=False)

    class Meta:
        verbose_name = 'Неотвеченный вопрос'
        verbose_name_plural = 'Неотвеченные вопросы'

    def __str__(self):
        return f"{self.question[:50]}..."

class Project(models.Model):
    title = models.CharField('Название проекта', max_length=200)
    description = models.TextField('Описание')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание')
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']  # Сортировка от новых к старым
    
    def __str__(self):
        return self.title
