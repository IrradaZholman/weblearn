"""
URL configuration for WebLearn project.
"""
from django.contrib import admin

admin.site.site_header = 'WebLearn — Админ-панель'
admin.site.site_title = 'WebLearn'
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('courses/', include('courses.urls')),
    path('editor/', include('editor.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
