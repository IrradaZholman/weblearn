from django.urls import path
from . import views
from courses import views as courses_views

app_name = 'accounts'

urlpatterns = [

    path('login/', views.CustomLoginView.as_view(), name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('register/', views.register, name='register'),

    path('profile/', courses_views.profile, name='profile'),
]
