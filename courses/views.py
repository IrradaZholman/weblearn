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

    total_lessons = Lesson.objects.count()

    completed_lessons = lesson_progress.filter(
        completed=True
    ).count()

    completion_percentage = (
        completed_lessons / total_lessons * 100
    ) if total_lessons > 0 else 0

    submissions = Submission.objects.filter(
        user=request.user
    ).select_related(
        'assignment',
        'assignment__lesson__course',
        'standalone_assignment'
    ).order_by('-created_at')

    avg_grade = submissions.filter(
        grade__isnull=False
    ).aggregate(
        Avg('grade')
    )['grade__avg'] or 0

    errors = submissions.filter(status='revision')

    quiz_attempts = QuizAttempt.objects.filter(
        user=request.user
    ).select_related('quiz')


    # ==========================
    # ДОСТИЖЕНИЯ
    # ==========================

    five_count = submissions.filter(grade=5).count()

    days_registered = (
        timezone.now().date()
        - request.user.date_joined.date()
    ).days

    achievements_count = 0
    achievements = []

    if completed_lessons >= 1:
        achievements_count += 1
        achievements.append({
            "title": "Старт обучения",
            "desc": "Завершить первый урок",
            "icon": "bi-rocket-takeoff-fill"
        })

    if completed_lessons >= 5:
        achievements_count += 1
        achievements.append({
            "title": "Базовая подготовка",
            "desc": "Завершить 5 уроков",
            "icon": "bi-book-half"
        })

    if completed_lessons >= 10:
        achievements_count += 1
        achievements.append({
            "title": "Завершён модуль",
            "desc": "Завершить 10 уроков",
            "icon": "bi-mortarboard-fill"
        })

    if completed_lessons >= 20:
        achievements_count += 1
        achievements.append({
            "title": "Продвинутый уровень",
            "desc": "Завершить 20 уроков",
            "icon": "bi-fire"
        })

    if completed_lessons >= total_lessons and total_lessons > 0:
        achievements_count += 1
        achievements.append({
            "title": "Лидер платформы",
            "desc": "Завершить все уроки",
            "icon": "bi-trophy-fill"
        })

    if completed_lessons >= 3:
        achievements_count += 1
        achievements.append({
            "title": "Три урока",
            "desc": "Завершить 3 урока",
            "icon": "bi-1-circle-fill"
        })

    if completed_lessons >= 6:
        achievements_count += 1
        achievements.append({
            "title": "Шесть уроков",
            "desc": "Завершить 6 уроков",
            "icon": "bi-2-circle-fill"
        })

    if completed_lessons >= 9:
        achievements_count += 1
        achievements.append({
            "title": "Девять уроков",
            "desc": "Завершить 9 уроков",
            "icon": "bi-3-circle-fill"
        })

    if completed_lessons >= 12:
        achievements_count += 1
        achievements.append({
            "title": "Двенадцать уроков",
            "desc": "Завершить 12 уроков",
            "icon": "bi-4-circle-fill"
        })

    if submissions.count() >= 1:
        achievements_count += 1
        achievements.append({
            "title": "Первая работа",
            "desc": "Отправить первую работу",
            "icon": "bi-send-check-fill"
        })

    if submissions.count() >= 10:
        achievements_count += 1
        achievements.append({
            "title": "Активный участник",
            "desc": "Отправить 10 работ",
            "icon": "bi-lightning-charge-fill"
        })

    if submissions.count() >= 25:
        achievements_count += 1
        achievements.append({
            "title": "Практический опыт",
            "desc": "Отправить 25 работ",
            "icon": "bi-briefcase-fill"
        })

    if submissions.count() >= 50:
        achievements_count += 1
        achievements.append({
            "title": "Project Specialist",
            "desc": "Отправить 50 работ",
            "icon": "bi-kanban-fill"
        })

    if avg_grade >= 4.5:
        achievements_count += 1
        achievements.append({
            "title": "Высокая успеваемость",
            "desc": "Средний балл выше 4.5",
            "icon": "bi-graph-up-arrow"
        })

    if avg_grade >= 5:
        achievements_count += 1
        achievements.append({
            "title": "Академическое превосходство",
            "desc": "Средний балл 5.0",
            "icon": "bi-award-fill"
        })

    if five_count >= 10:
        achievements_count += 1
        achievements.append({
            "title": "Quality Expert",
            "desc": "10 работ на отлично",
            "icon": "bi-shield-check"
        })

    if five_count >= 20:
        achievements_count += 1
        achievements.append({
            "title": "Excellence Award",
            "desc": "20 работ на отлично",
            "icon": "bi-gem"
        })

    if request.user.date_joined:
        achievements_count += 1
        achievements.append({
            "title": "Первые шаги",
            "desc": "Регистрация на платформе",
            "icon": "bi-calendar-check"
        })

    if days_registered >= 3:
        achievements_count += 1
        achievements.append({
            "title": "Постоянный ученик",
            "desc": "3 дня на платформе",
            "icon": "bi-clock-history"
        })

    if days_registered >= 7:
        achievements_count += 1
        achievements.append({
            "title": "Неделя обучения",
            "desc": "7 дней на платформе",
            "icon": "bi-calendar-week"
        })

    if days_registered >= 30:
        achievements_count += 1
        achievements.append({
            "title": "Месяц обучения",
            "desc": "30 дней на платформе",
            "icon": "bi-calendar-month"
        })

    if days_registered >= 100:
        achievements_count += 1
        achievements.append({
            "title": "Верный платформе",
            "desc": "100 дней на платформе",
            "icon": "bi-hourglass-split"
        })

    if completed_lessons >= 15 and avg_grade >= 4.8:
        achievements_count += 1
        achievements.append({
            "title": "Звезда обучения",
            "desc": "15 уроков и средний балл 4.8+",
            "icon": "bi-stars"
        })

    if quiz_attempts.count() >= 1:
        achievements_count += 1
        achievements.append({
            "title": "Первый тест",
            "desc": "Пройти первый тест",
            "icon": "bi-patch-check-fill"
        })

    if quiz_attempts.count() >= 10:
        achievements_count += 1
        achievements.append({
            "title": "Опытный тестировщик",
            "desc": "Пройти 10 тестов",
            "icon": "bi-ui-checks-grid"
        })

    if (
        completed_lessons >= total_lessons
        and submissions.count() >= 50
        and avg_grade >= 5
    ):
        achievements_count += 1
        achievements.append({
            "title": "Легенда платформы",
            "desc": "Все уроки + 50 работ + средний балл 5.0",
            "icon": "bi-trophy-fill"
        })

    latest_achievements = list(reversed(achievements))[:3]

    print("completed_lessons =", completed_lessons)
    print("submissions =", submissions.count())
    print("avg_grade =", avg_grade)
    print("five_count =", five_count)
    print("days_registered =", days_registered)
    print("quiz_attempts =", quiz_attempts.count())
    print("achievements_count =", achievements_count)

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
        'achievements_count': achievements_count,
        'days_registered': days_registered,
        'five_count': five_count,
        'latest_achievements': latest_achievements,
    })
@login_required
@require_POST
def mark_lesson_complete(request, course_slug, lesson_slug):
    """Отметить урок как выполненный."""
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
    
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()
    
    messages.success(request, f'Урок "{lesson.title}" отмечен как выполненный!')
    return redirect('courses:lesson_detail', course_slug=course_slug, lesson_slug=lesson_slug)


def standalone_assignments(request):
    """Список дополнительных заданий."""
    assignments = StandaloneAssignment.objects.all()
    return render(request, 'courses/standalone_assignments.html', {'assignments': assignments})


def quiz_detail(request, quiz_id):
    """Страница теста."""
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions__answers'), pk=quiz_id)
    
    # Проверяем, проходил ли пользователь тест
    last_attempt = None
    if request.user.is_authenticated:
        last_attempt = QuizAttempt.objects.filter(
            user=request.user,
            quiz=quiz
        ).order_by('-completed_at').first()
    
    return render(request, 'courses/quiz_detail.html', {
        'quiz': quiz,
        'last_attempt': last_attempt,
    })


@login_required
@require_POST
def submit_quiz(request, quiz_id):
    """Отправить ответы на тест."""
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions__answers'), pk=quiz_id)
    
    # Получаем ответы пользователя
    user_answers = {}
    total_questions = quiz.questions.count()
    correct_answers = 0
    
    for question in quiz.questions.all():
        answer_id = request.POST.get(f'question_{question.id}')
        if answer_id:
            try:
                answer = Answer.objects.get(pk=answer_id, question=question)
                user_answers[question.id] = int(answer_id)
                if answer.is_correct:
                    correct_answers += 1
            except Answer.DoesNotExist:
                pass
    
    # Вычисляем процент
    score = int((correct_answers / total_questions * 100)) if total_questions > 0 else 0
    passed = score >= quiz.passing_score
    
    # Сохраняем попытку
    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        passed=passed,
        answers=user_answers
    )
    
    messages.success(
        request,
        f'Тест завершен! Вы набрали {score}% баллов. {"Поздравляем, тест пройден!" if passed else f"Нужно набрать минимум {quiz.passing_score}%."}'
    )
    
    return redirect('courses:quiz_result', attempt_id=attempt.id)


def quiz_result(request, attempt_id):
    """Результат прохождения теста."""
    attempt = get_object_or_404(QuizAttempt.objects.select_related('quiz', 'user'), pk=attempt_id)
    
    # Проверяем доступ
    if request.user != attempt.user and not request.user.is_staff:
        messages.error(request, 'У вас нет доступа к этому результату.')
        return redirect('courses:course_list')
    
    return render(request, 'courses/quiz_result.html', {'attempt': attempt})
