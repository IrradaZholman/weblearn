from django.shortcuts import render
from django.db.models import Count
from courses.models import Course, Lesson, Submission
from django.contrib.auth.models import User


def home(request):
    # Статистика для главной страницы
    stats = {
        'courses_count': Course.objects.count(),
        'lessons_count': Lesson.objects.count(),
        'submissions_count': Submission.objects.count(),
        'users_count': User.objects.count(),
    }
    
    # Последние курсы
    recent_courses = Course.objects.prefetch_related('lessons').annotate(
        lessons_count=Count('lessons')
    )[:3]
    
    return render(request, 'main/home.html', {
        'stats': stats,
        'recent_courses': recent_courses,
    })


def about(request):
    return render(request, 'main/about.html')


def contacts(request):
    return render(request, 'main/contacts.html')


def methodical(request):
    return render(request, 'main/methodical.html')
