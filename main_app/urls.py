from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.students, name='students'),
    path('lessons/', views.lessons, name='lessons'),
    path('attendance/', views.attendance, name='attendance'),
    path('lessons/download/<int:lesson_id>/', views.download_lesson, name='download_lesson'),
    path('lessons/upload/', views.upload_lesson, name='upload_lesson'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('lessons/delete/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),
    path('chat_message/', views.chat_message, name='chat_message'),
    path('lessons/view/<int:lesson_id>/', views.view_lesson, name='view_lesson'),
    path('python-interpreter/', views.python_interpreter, name='python_interpreter'),
    path('run-python-code/', views.run_python_code, name='run_python_code'),
    path('attendance/add-student/', views.add_student, name='add_student'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    
    # Добавляем URL-шаблоны для сброса пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
