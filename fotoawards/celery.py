import os
from celery import Celery

os.environ.setdefault('DJANG)_SETTINGS_MODULE', 'fotoawards.settings')

app = Celery('send_email')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()