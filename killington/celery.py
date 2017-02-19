import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'killington.settings.local')

app = Celery('killington')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.CELERYBEAT_SCHEDULE = {
    'process-active-lotteries-every-hour': {
        'task': 'shows.tasks.process_active_lotteries',
        'schedule': crontab(minute=45, hour='*'),
        'args': None,
    },
    'run-shows-spider-every-hour': {
        'task': 'shows.tasks.run_shows_spider',
        'schedule': crontab(minute=15, hour='*'),
        'args': None,
    },
}

