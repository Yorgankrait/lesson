from django.contrib import admin
from .models import Lesson, ChatMessage, Student, Attendance, UnknownQuestion, Project, News, AboutPage, TeacherResource, UserProfile, UserIdea

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

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'updated_at')
    search_fields = ('name', 'title', 'experience', 'education')

@admin.register(TeacherResource)
class TeacherResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'is_teacher_activated', 'is_student_activated', 'get_email')
    list_filter = ('user_type', 'is_teacher_activated', 'is_student_activated')
    search_fields = ('user__username', 'user__email')
    list_editable = ('is_teacher_activated', 'is_student_activated')
    actions = ['activate_teachers', 'deactivate_teachers', 'activate_students', 'deactivate_students']
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def activate_teachers(self, request, queryset):
        updated = queryset.filter(user_type='teacher').update(is_teacher_activated=True)
        self.message_user(request, f'Активировано {updated} учителей')
    activate_teachers.short_description = "Активировать выбранных учителей"

    def deactivate_teachers(self, request, queryset):
        updated = queryset.filter(user_type='teacher').update(is_teacher_activated=False)
        self.message_user(request, f'Деактивировано {updated} учителей')
    deactivate_teachers.short_description = "Деактивировать выбранных учителей"

    def activate_students(self, request, queryset):
        updated = queryset.filter(user_type='student').update(is_student_activated=True)
        self.message_user(request, f'Активировано {updated} учеников')
    activate_students.short_description = "Активировать выбранных учеников"

    def deactivate_students(self, request, queryset):
        updated = queryset.filter(user_type='student').update(is_student_activated=False)
        self.message_user(request, f'Деактивировано {updated} учеников')
    deactivate_students.short_description = "Деактивировать выбранных учеников"

@admin.register(UserIdea)
class UserIdeaAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea', 'created_at', 'is_reviewed')
    list_filter = ('is_reviewed', 'created_at')
    search_fields = ('user__username', 'idea')
    readonly_fields = ('created_at',)
