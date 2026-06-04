from django.contrib import admin
from .models import (
    Course, Lesson, Assignment, Submission, StandaloneAssignment,
    Quiz, Question, Answer, QuizAttempt, UserProgress,
    CourseReview, Achievement
)



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'order', 'icon')}),
        ('Описание', {'fields': ('description', 'short_description')}),
        ('Медиа', {'fields': ('image', 'video_url')}),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
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


from django.contrib import admin
from django.utils.html import format_html
import json

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'task_name',
        'user',
        'status',
        'grade'
    ]

    list_filter = ['status']
    search_fields = ['user__username', 'comment']
    list_editable = ['status', 'grade']

    readonly_fields = ['formatted_code']

    fieldsets = (
        (None, {
            'fields': (
                'assignment',
                'standalone_assignment',
                'user',
                'status',
                'grade'
            )
        }),
        ('Работа ученика', {
            'fields': (
                'formatted_code',
                'comment'
            )
        }),
        ('Проверка', {
            'fields': (
                'reviewer_comment',
                'reviewed_at'
            )
        }),
    )

    def formatted_code(self, obj):
        if not obj.code:
            return "-"

        try:
            data = json.loads(obj.code)

            html_code = data.get("html", "")
            css_code = data.get("css", "")
            js_code = data.get("js", "")

            result = ""

            if html_code:
                result += "HTML\n"
                result += "=" * 50 + "\n"
                result += html_code + "\n\n"

            if css_code:
                result += "CSS\n"
                result += "=" * 50 + "\n"
                result += css_code + "\n\n"

            if js_code:
                result += "JavaScript\n"
                result += "=" * 50 + "\n"
                result += js_code

            return format_html(
                '''
                <pre style="
                    white-space: pre-wrap;
                    font-family: Consolas, monospace;
                    background:#f8f9fa;
                    border:1px solid #ddd;
                    padding:15px;
                    max-height:700px;
                    overflow:auto;
                    margin:0;
                ">{}</pre>
                ''',
                result
            )

        except Exception:
            return format_html(
                '<pre style="white-space:pre-wrap;">{}</pre>',
                obj.code
            )

    formatted_code.short_description = "Код ученика"

    def task_name(self, obj):
        if obj.assignment:
            return obj.assignment.title
        if obj.standalone_assignment:
            return obj.standalone_assignment.title
        return '-'

    task_name.short_description = 'Задание'


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
    list_display = [
        'user',
        'quiz',
        'score',
        'passed'
    ]

    list_filter = ['passed', 'quiz']
    search_fields = ['user__username']




@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'course', 'completed']
    list_filter = ['completed', 'lesson__course']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']


