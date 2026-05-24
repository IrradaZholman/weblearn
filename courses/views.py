from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count, Avg
from django.utils import timezone
from .models import (
    Course, Lesson, Assignment, Submission, StandaloneAssignment,
    Quiz, Question, Answer, QuizAttempt, UserProgress, CourseReview
)


def course_list(request):
    courses = Course.objects.prefetch_related('lessons').annotate(
        lessons_count=Count('lessons')
    ).all()
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    reviews = CourseReview.objects.filter(course=course).select_related('user')[:5]
    avg_rating = CourseReview.objects.filter(course=course).aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Прогресс пользователя
    user_progress = None
    completed_lessons = set()
    if request.user.is_authenticated:
        user_progress = UserProgress.objects.filter(user=request.user, course=course).first()
        completed_lessons = set(
            UserProgress.objects.filter(
                user=request.user,
                lesson__course=course,
                completed=True
            ).values_list('lesson_id', flat=True)
        )
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'user_progress': user_progress,
        'completed_lessons': completed_lessons,
    })


def lesson_detail(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
    
    # Прогресс пользователя
    is_completed = False
    completed_lessons = set()
    if request.user.is_authenticated:
        progress = UserProgress.objects.filter(user=request.user, lesson=lesson).first()
        is_completed = progress.completed if progress else False
        completed_lessons = set(
            UserProgress.objects.filter(
                user=request.user,
                lesson__course=course,
                completed=True
            ).values_list('lesson_id', flat=True)
        )
    
    # Тест урока
    quiz = Quiz.objects.filter(lesson=lesson).first()
    
    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'is_completed': is_completed,
        'completed_lessons': completed_lessons,
        'quiz': quiz,
    })


@login_required
def my_submissions(request):
    submissions = Submission.objects.filter(
        user=request.user
    ).select_related('assignment__lesson__course', 'standalone_assignment').order_by('-created_at')
    return render(request, 'courses/my_submissions.html', {'submissions': submissions})


from django.core.paginator import Paginator

@login_required
def profile(request):
    """Личный профиль пользователя."""

    # Прогресс по курсам
    course_progress = UserProgress.objects.filter(
        user=request.user,
        course__isnull=False
    ).select_related('course')

    # Прогресс по урокам
    lesson_progress = UserProgress.objects.filter(
        user=request.user,
        lesson__isnull=False
    ).select_related('lesson', 'lesson__course')

    # Статистика
    total_lessons = Lesson.objects.count()

    completed_lessons = lesson_progress.filter(
        completed=True
    ).count()

    completion_percentage = (
        completed_lessons / total_lessons * 100
    ) if total_lessons > 0 else 0

    # ВСЕ РАБОТЫ ПОЛЬЗОВАТЕЛЯ
    submissions_list = Submission.objects.filter(
        user=request.user
    ).select_related(
        'assignment',
        'assignment__lesson__course',
        'standalone_assignment'
    ).order_by('-created_at')

    # PAGINATION
    paginator = Paginator(submissions_list, 5)

    page = request.GET.get('page')

    submissions = paginator.get_page(page)

    # Средняя оценка
    graded_submissions = submissions_list.filter(
        grade__isnull=False
    )

    avg_grade = graded_submissions.aggregate(
        Avg('grade')
    )['grade__avg'] or 0

    # Работы на доработке
    errors = submissions_list.filter(
        status='revision'
    )

    # Тесты
    quiz_attempts = QuizAttempt.objects.filter(
        user=request.user
    ).select_related('quiz')

    return render(request, 'accounts/profile.html', {
        'course_progress': course_progress,
        'lesson_progress': lesson_progress,

        'completed_lessons': completed_lessons,
        'total_lessons': total_lessons,
        'completion_percentage': round(completion_percentage, 1),

        'submissions': submissions,
        'avg_grade': round(avg_grade, 1),

        'errors': errors,
        'quiz_attempts': quiz_attempts,
    })


def quiz_result(request, attempt_id):
    """Результат прохождения теста."""
    attempt = get_object_or_404(QuizAttempt.objects.select_related('quiz', 'user'), pk=attempt_id)
    
    # Проверяем доступ
    if request.user != attempt.user and not request.user.is_staff:
        messages.error(request, 'У вас нет доступа к этому результату.')
        return redirect('courses:course_list')
    
    return render(request, 'courses/quiz_result.html', {'attempt': attempt})
