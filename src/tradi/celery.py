import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tradi.settings')

celery_app = Celery('app')
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks()
