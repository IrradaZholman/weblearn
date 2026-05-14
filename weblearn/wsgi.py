"""
WSGI config for WebLearn project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weblearn.settings')

application = get_wsgi_application()
