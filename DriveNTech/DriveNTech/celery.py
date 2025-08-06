import os
from celery import Celery
"""
# this will tell Django to use the settings from the DriveNTech project
# when configuring Celery
"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DriveNTech.settings')

app = Celery('DriveNTech')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()