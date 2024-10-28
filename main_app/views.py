# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from .models import Lesson, Attendance, ChatMessage, Student, UnknownQuestion, News
from .forms import LessonForm, CustomUserCreationForm, ExcelUploadForm, AttendanceForm, StudentForm
import pandas as pd
import os
from datetime import datetime, timedelta
from django.utils.dateformat import format
from itertools import groupby
from operator import attrgetter
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from pptx import Presentation
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import sys
from io import StringIO
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
import logging

logger = logging.getLogger(__name__)

def fix_session(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    try:
        Session.objects.get(session_key=request.session.session_key)
    except Session.DoesNotExist:
        request.session.save()
    return request

def wrap_view(view_func):
    def wrapped(request, *args, **kwargs):
        request = fix_session(request)
        return view_func(request, *args, **kwargs)
    return wrapped

@wrap_view
def home(request):
    news = News.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'home.html', {'news': news})

@wrap_view
def students(request):
    active_students = Student.objects.filter(active=True).select_related('project')
    students_data = []
    
    for student in active_students:
        student_data = {
            'name': student.name,
            'project': student.project.title if student.project else 'Проект не назначен',
            'description': student.project.description if student.project else 'Описание отсутствует'
        }
        students_data.append(student_data)
    
    return render(request, 'students.html', {'students': students_data})

@wrap_view
def lessons(request):
    lessons = Lesson.objects.all().order_by('-upload_date')
    return render(request, 'lessons.html', {'lessons': lessons})

@csrf_exempt
@wrap_view
def chat_message(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Authentication required'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message').lower()
            
            # Сохраняем сообщ��ние пользователя
            ChatMessage.objects.create(user=request.user, message=message, is_bot=False)
            
            # Расширенные ответы бота
            responses = {
                # Приветствия и прощания
                'привет': 'Здравствуйте! Я помогу вам разобраться с сайтом. Спросите меня о любом разделе: главная, ученики, материалы, интерпретатор.',
                'пока': 'До свидания! Буду рад помочь снова!',
                'как дела': 'У меня всё хорошо, готов помогать! Что вас интересует?',
                
                # Описание разделов
                'главная': 'На главной странице вы найдете общую информацию о нашем обучающем проекте и меня - вашего помощника по сайту.',
                'ученики': 'В разделе "Ученики и их проекты" вы можете увидеть работы наших учеников, их достижения и проекты, которые они создали во время обучения.',
                'материаы': 'В разделе "Учебные материалы" собраны все презентации и уроки по программированию. Вы можете просматривать их онлайн или скачивать.',
                'интерпретатор': 'Python Интерпретатор позволяет писать и выполнять код прямо в браузере. Отличный инструмент для практики!',
                
                # Дополнительные функции
                'посещаемость': 'В разделе "Посещаемость" можно отслеживать присутствие учеников на занятиях. Доступно для преподавателей и родителей.',
                'регистрация': 'Чтобы зарегистрироваться на сайте, нажмите кнопку "Регистрация" внизу страницы и заполните форму.',
                'вход': 'Для входа на сайт используйте кнопку "Вход для учеников/родителей" в нижней части страницы.',
                'админ': 'Вход для администратора доступен по соответствующей кнопке в футере сайта.',
                
                # Помощь
                'помощь': 'Я могу ассказать о любом разделе сайта. Спросите меня о: главная, ученики, материалы, интерпретатор, посещаемость, регистрация, вход.',
                'что ты умеешь': 'Я могу рассказать о разных частях сайта, помочь с навигацией и ответить на базовые вопросы. Спросите меня о конкретном разделе!',
                
                # Дополнительые ключевые слова
                'проекты': 'Проекты учеников можно посмотреть в разделе "Ученики и их проекты". Там представлены их лучшие работы.',
                'уроки': 'Все уроки доступны в разделе "Учебные материалы". Они представлены в виде презентаций, которые можно просматривать онлайн.',
                'код': 'Вы можете писать и тестировать код в разделе "Python Интерпретатор". Он поддерживает все базовые функции Python.',
            }
            
            # Поиск ответа в стандартных ответах
            bot_response = None
            for key in responses:
                if key in message:
                    bot_response = responses[key]
                    break
            
            # Если стандартный ответ не найден
            if not bot_response:
                # Ищем похожие вопросы в базе (используем icontains для нечеткого поиска)
                similar_questions = UnknownQuestion.objects.filter(
                    question__icontains=message
                )
                
                # Если найден отвеченный вопрос, используем его ответ
                answered_question = similar_questions.filter(is_answered=True).first()
                if answered_question and answered_question.answer:
                    bot_response = answered_question.answer
                
                # Если похожий вопрос уже есть, но без ответа
                elif similar_questions.exists():
                    bot_response = ('Этот вопрос уже передан администратору и скоро будет отвечен. '
                                  'А пока я могу рассказать о разделах сайта - '
                                  'спросите меня о: главная, ученики, материалы, '
                                  'интерпретатор, или напишите "помощь".')
                
                # Если это совершенно новый вопрос
                else:
                    UnknownQuestion.objects.create(
                        user=request.user,
                        question=message
                    )
                    bot_response = ('Я пока не знаю ответа на этот вопрос, '
                                  'но я передам его администратору. '
                                  'А пока могу рассказать о разделах сайта - '
                                  'спросите меня о: главная, ученики, материалы, '
                                  'интерпретатор, или напишите "помощь".')
            
            # Сохраняем ответ бота
            ChatMessage.objects.create(user=request.user, message=bot_response, is_bot=True)
            
            return JsonResponse({'status': 'success', 'message': bot_response})
            
        except Exception as e:
            logger.error(f"Error in chat_message: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    elif request.method == 'GET':
        messages = ChatMessage.objects.filter(user=request.user).values('message', 'is_bot')
        return JsonResponse({'status': 'success', 'messages': list(messages)})
    
    elif request.method == 'DELETE':
        ChatMessage.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success', 'message': 'Chat history cleared'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
@wrap_view
def view_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    try:
        pptx_path = lesson.presentation.path
        prs = Presentation(pptx_path)
        
        slides = []
        for slide in prs.slides:
            img = Image.new('RGB', (960, 540), (0, 0, 0))  # Черный фон
            draw = ImageDraw.Draw(img)
            
            try:
                title_font = ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", 32)
                content_font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 24)
                code_font = ImageFont.truetype("/Library/Fonts/Courier New.ttf", 20)
            except IOError:
                title_font = ImageFont.load_default()
                content_font = ImageFont.load_default()
                code_font = ImageFont.load_default()
            
            y_position = 20
            for shape in slide.shapes:
                if hasattr(shape, 'text'):
                    text = shape.text.strip()
                    if text:
                        if shape.name == 'Title':
                            text_width = draw.textbbox((0, 0), text, font=title_font)[2]
                            x_position = (960 - text_width) / 2
                            draw.text((x_position, y_position), text, fill=(255, 255, 255), font=title_font)
                            y_position += 60
                        else:
                            paragraphs = text.split('\n\n')
                            for paragraph in paragraphs:
                                if paragraph.strip().startswith('# ') or '=' in paragraph or 'print(' in paragraph:
                                    lines = paragraph.split('\n')
                                    for line in lines:
                                        words = line.split()
                                        line = []
                                        for word in words:
                                            line.append(word)
                                            bbox = draw.textbbox((0, 0), ' '.join(line), font=code_font)
                                            w = bbox[2] - bbox[0]
                                            if w > 880:
                                                draw.text((40, y_position), ' '.join(line[:-1]), fill=(0, 255, 0), font=code_font)
                                                y_position += 25
                                                line = [word]
                                        if line:
                                            draw.text((40, y_position), ' '.join(line), fill=(0, 255, 0), font=code_font)
                                            y_position += 25
                                else:
                                    words = paragraph.split()
                                    line = []
                                    for word in words:
                                        line.append(word)
                                        bbox = draw.textbbox((0, 0), ' '.join(line), font=content_font)
                                        w = bbox[2] - bbox[0]
                                        if w > 880:
                                            draw.text((40, y_position), ' '.join(line[:-1]), fill=(255, 255, 255), font=content_font)
                                            y_position += 30
                                            line = [word]
                                    if line:
                                        draw.text((40, y_position), ' '.join(line), fill=(255, 255, 255), font=content_font)
                                        y_position += 30
                                y_position += 20
                
                if y_position > 520:
                    break
            
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            slides.append(f"data:image/png;base64,{img_str}")
        
        context = {
            'lesson': lesson,
            'slides': slides,
        }
        
        return render(request, 'view_lesson.html', context)
    
    except Exception as e:
        error_message = f'Ошибка при открытии презентации: {str(e)}'
        return render(request, 'error.html', {'error_message': error_message})

@login_required
@wrap_view
def download_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    response = HttpResponse(lesson.presentation, content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
    response['Content-Disposition'] = f'attachment; filename="{lesson.title}.pptx"'
    return response

@login_required
@wrap_view
def upload_lesson(request):
    if not request.user.is_staff:
        return redirect('lessons')
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            presentation = request.FILES['presentation']
            if not presentation.name.lower().endswith('.pptx'):
                form.add_error('presentation', 'Загруженный файл не является PowerPoint презентацией (.pptx).')
            else:
                form.save()
                return redirect('lessons')
    else:
        form = LessonForm()
    return render(request, 'upload_lesson.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
@wrap_view
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        lesson.delete()
        return redirect('lessons')
    return render(request, 'delete_lesson.html', {'lesson': lesson})

@wrap_view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@wrap_view
def python_interpreter(request):
    return render(request, 'python_interpreter.html')

@csrf_exempt
@wrap_view
def run_python_code(request):
    if request.method == 'POST':
        code = json.loads(request.body)['code']
        
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = sys.stdout = StringIO()
        redirected_error = sys.stderr = StringIO()

        try:
            exec(code)
            output = redirected_output.getvalue()
            error = redirected_error.getvalue()
            if error:
                output = f"Error:\n{error}\n\nOutput:\n{output}"
        except Exception as e:
            output = str(e)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        return JsonResponse({'output': output})

@user_passes_test(lambda u: u.is_staff)
@wrap_view
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ученик успешно добавлен.')
            return redirect('attendance')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

@wrap_view
def attendance(request):
    attendances = Attendance.objects.all().order_by('-date', 'student')
    
    grouped_attendances = []
    for date, group in groupby(attendances, key=lambda x: x.date.strftime('%B %Y')):
        grouped_attendances.append((date, list(group)))
    
    context = {
        'grouped_attendances': grouped_attendances,
    }
    if request.user.is_staff:
        context['students'] = Student.objects.all()
    return render(request, 'attendance.html', context)

@user_passes_test(lambda u: u.is_staff)
@wrap_view
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            no_class = form.cleaned_data['no_class']
            present_students = form.cleaned_data['students']
            
            if no_class:
                for student in Student.objects.all():
                    Attendance.objects.update_or_create(
                        student=student,
                        date=date,
                        defaults={'present': False, 'no_class': True}
                    )
            else:
                for student in Student.objects.all():
                    Attendance.objects.update_or_create(
                        student=student,
                        date=date,
                        defaults={'present': student in present_students, 'no_class': False}
                    )
            
            messages.success(request, 'Посещаемость успешно отмечена.')
            return redirect('attendance')
    else:
        form = AttendanceForm()
    return render(request, 'mark_attendance.html', {'form': form})

@require_http_methods(["GET", "POST"])
@wrap_view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/'})
            return redirect('home')
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

