from django.contrib import admin
from .models import Lesson, ChatMessage, Student, Attendance, UnknownQuestion, Project, News

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date')
    list_filter = ('upload_date',)
    search_fields = ('title',)
    ordering = ('-upload_date',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_bot', 'timestamp')
    list_filter = ('is_bot', 'timestamp', 'user')
    search_fields = ('message', 'user__username')
    ordering = ('-timestamp',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'email', 'phone', 'active')
    list_filter = ('active', 'project')
    search_fields = ('name', 'email', 'phone', 'notes')
    list_editable = ('active',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'email', 'phone', 'active')
        }),
        ('Проект', {
            'fields': ('project',)
        }),
        ('Дополнительно', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'present', 'no_class')
    list_filter = ('date', 'present', 'no_class')
    search_fields = ('student__name',)
    date_hierarchy = 'date'

@admin.register(UnknownQuestion)
class UnknownQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'created_at', 'is_answered')
    list_filter = ('is_answered', 'created_at')
    search_fields = ('question', 'answer', 'user__username')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'question', 'created_at')
        }),
        ('Ответ', {
            'fields': ('answer', 'is_answered')
        }),
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'is_published')
    list_filter = ('is_published', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'is_published')
        }),
    )
