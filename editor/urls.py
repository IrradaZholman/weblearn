from django.urls import path
from . import views

app_name = 'editor'

urlpatterns = [
    path('', views.editor_standalone, name='standalone'),
    path('builder/', views.builder, name='builder'),
    path('assignment/<int:assignment_id>/', views.editor, name='editor'),
    path('standalone/<int:standalone_assignment_id>/', views.editor_standalone, name='standalone_assignment'),
    path('submit/', views.submit_work, name='submit'),
    path('api/validate/', views.api_validate, name='api_validate'),
    path('api/chat/', views.api_chat, name='api_chat'),
]
