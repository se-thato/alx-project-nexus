from .celery import app as celery_app

# this will make sure Celery starts with Django
__all__ = ('celery_app',)