import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lgsedu.settings')
app = Celery('lgsedu')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
