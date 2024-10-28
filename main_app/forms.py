from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Lesson, Student, Attendance, Project, News

class AttendanceForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата'
    )
    no_class = forms.BooleanField(
        required=False,
        label="Отсутствие занятия"
    )
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Присутствующие ученики"
    )

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'presentation']
        labels = {
            'title': 'Название урока',
            'presentation': 'Презентация'
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        labels = {
            'title': 'Название проекта',
            'description': 'Описание'
        }

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published']
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'is_published': 'Опубликовать'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label=_("Имя пользователя"),
        help_text=_("Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_."),
        error_messages={
            'unique': _("Пользователь с таким именем уже существует."),
        },
    )
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput,
        help_text=_("Ваш пароль должен содержать как минимум 8 символов."),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput,
        help_text=_("Введите тот же пароль, что и выше, для подтверждения."),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'project', 'email', 'phone', 'notes', 'active']
        labels = {
            'name': 'ФИО',
            'project': 'Проект',
            'email': 'Email',
            'phone': 'Телефон',
            'notes': 'Заметки',
            'active': 'Активный'
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Excel файл')
