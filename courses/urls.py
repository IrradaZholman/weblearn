from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    # Статические маршруты должны быть выше динамических с slug
    path('my-submissions/', views.my_submissions, name='my_submissions'),
    path('standalone-assignments/', views.standalone_assignments, name='standalone_assignments'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    # Динамические маршруты с slug должны быть в конце
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/complete/', views.mark_lesson_complete, name='mark_lesson_complete'),
]
