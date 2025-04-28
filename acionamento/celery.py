import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acionamento.settings')

app = Celery('acionamento')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() 