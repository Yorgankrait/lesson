from django.db import models
from django.utils.dateformat import format
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

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

class AboutPage(models.Model):
    name = models.CharField('Имя', max_length=100)
    title = models.CharField('Должность', max_length=200)
    experience = models.TextField('Опыт работы')
    education = models.TextField('Образование')
    updated_at = models.DateTimeField('Последнее обновление', auto_now=True)

    class Meta:
        verbose_name = 'Страница "Обо мне"'
        verbose_name_plural = 'Страница "Обо мне"'

    def __str__(self):
        return f"Информация о {self.name}"

class TeacherArticle(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание', blank=True)
    preview_image = models.ImageField('Превью изображение', upload_to='article_previews/', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Последнее обновление', auto_now=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Статья для учителей'
        verbose_name_plural = 'Статьи для учителей'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_content(self):
        try:
            content = json.loads(self.content)
            if isinstance(content, (list, tuple)):
                return content
            return []
        except:
            return []

class TeacherResource(models.Model):
    article = models.ForeignKey(TeacherArticle, on_delete=models.CASCADE, related_name='resources', verbose_name='Статья')
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание', blank=True)
    file = models.FileField('Файл', upload_to='teacher_files/')
    file_type = models.CharField('Тип файла', max_length=50, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Последнее обновление', auto_now=True)

    class Meta:
        verbose_name = 'Файл для учителей'
        verbose_name_plural = 'Файлы для учителей'
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.file_type and self.file:
            ext = self.file.name.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'gif']:
                self.file_type = 'image'
            elif ext == 'exe':
                self.file_type = 'executable'
            else:
                self.file_type = 'other'
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    USER_TYPES = (
        ('student', 'Ученик'),
        ('parent', 'Родитель'),
        ('teacher', 'Учитель'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    is_teacher_activated = models.BooleanField(default=False)
    is_student_activated = models.BooleanField(default=False)  # Добавляем поле для активации учеников
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance)

class UserIdea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    idea = models.TextField('Идея')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_reviewed = models.BooleanField('Просмотрено', default=False)

    class Meta:
        verbose_name = 'Идея пользователя'
        verbose_name_plural = 'Идеи пользователей'
        ordering = ['-created_at']

    def __str__(self):
        return f"Идея от {self.user.username}"

class ArticleImage(models.Model):
    article = models.ForeignKey(TeacherArticle, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article_images/')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
