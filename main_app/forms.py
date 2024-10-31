from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from .models import Lesson, Student, Attendance, Project, News, UserProfile, TeacherArticle, TeacherResource, ArticleImage

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
    USER_TYPES = (
        ('student', 'Ученик'),
        ('parent', 'Родитель'),
        ('teacher', 'Учитель'),
    )
    
    user_type = forms.ChoiceField(choices=USER_TYPES, label='Тип пользователя')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_type = self.cleaned_data.get('user_type')
            
            # Создаем или получаем профиль пользователя
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.user_type = user_type
            
            # Если пользователь выбрал роль учителя, он не активирован по умолчанию
            if user_type == 'teacher':
                profile.is_teacher_activated = False
            
            profile.save()
            
            # Добавляем пользователя в соответствующую группу
            group_name = user_type.capitalize()
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
            
        return user

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

class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    email = forms.EmailField(label="Email")

class TeacherArticleForm(forms.ModelForm):
    class Meta:
        model = TeacherArticle
        fields = ['title', 'preview_image', 'is_published']
        labels = {
            'title': 'Заголовок',
            'preview_image': 'Превью изображение (необязательно)',
            'is_published': 'Опубликовать'
        }

class TeacherResourceForm(forms.ModelForm):
    class Meta:
        model = TeacherResource
        fields = ['title', 'description', 'file']
        labels = {
            'title': 'Название файла',
            'description': 'Описание',
            'file': 'Файл'
        }

class ArticleImageForm(forms.ModelForm):
    class Meta:
        model = ArticleImage
        fields = ['image']
