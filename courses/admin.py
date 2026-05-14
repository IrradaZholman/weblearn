from django.contrib import admin
from .models import (
    Course, Lesson, Assignment, Submission, StandaloneAssignment,
    Quiz, Question, Answer, QuizAttempt, UserProgress, CourseReview
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'order', 'icon')}),
        ('Описание', {'fields': ('description', 'short_description')}),
        ('Медиа', {'fields': ('image', 'video_url')}),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'created_at']
    list_filter = ['course']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {'fields': ('course', 'title', 'slug', 'order')}),
        ('Содержание', {'fields': ('content',)}),
        ('Примеры кода', {'fields': ('example_code_html', 'example_code_css', 'example_code_js')}),
    )


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'order']
    list_filter = ['lesson__course']


@admin.register(StandaloneAssignment)
class StandaloneAssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'order']
    list_filter = ['difficulty']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'assignment', 'standalone_assignment', 'user', 'status', 'grade', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username', 'comment']
    readonly_fields = ['created_at']
    list_editable = ['status', 'grade']
    fieldsets = (
        (None, {'fields': ('assignment', 'standalone_assignment', 'user', 'status', 'grade')}),
        ('Работа ученика', {'fields': ('code', 'comment')}),
        ('Проверка', {'fields': ('reviewer_comment', 'reviewed_at')}),
    )


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2
    fields = ['text', 'is_correct', 'order']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'order']
    list_filter = ['quiz']
    inlines = [AnswerInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'course', 'passing_score', 'order']
    list_filter = ['lesson__course', 'course']
    fieldsets = (
        (None, {'fields': ('title', 'description', 'order')}),
        ('Привязка', {'fields': ('lesson', 'course'), 'description': 'Укажите либо урок, либо курс для общего теста'}),
        ('Настройки', {'fields': ('passing_score',)}),
    )


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'passed', 'completed_at']
    list_filter = ['passed', 'quiz']
    search_fields = ['user__username']
    readonly_fields = ['completed_at']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'course', 'completed', 'updated_at']
    list_filter = ['completed', 'lesson__course']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'rating', 'created_at']
    list_filter = ['rating', 'course']
    search_fields = ['user__username', 'text']
    readonly_fields = ['created_at']
