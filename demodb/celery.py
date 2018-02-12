import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demodb.settings')

app = Celery('demodb')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'load_data_to_mysql': {
        'task': 'dmdb.tasks.load_data_to_mysql',
        'schedule': crontab(),
    },
}