import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'killington.settings.local')

app = Celery('killington')
app.config_from_object('django.conf:settings', namespace='CELERY')

# To ensure the floods don't prevent normal subscription lottery entries from
# occuring, the celery jobs are separated into two separate queues.
#
# Normally routes can be autodiscovered using `app.autodiscover_tasks()`
# where by convention over configuration, celery knows to find tasks in
# django_app/tasks.py.
#
# If the task_routes can be replaced using `app.autodiscover_tasks()` instead
# of being explicit, then do it.
# app.conf.task_routes = {
#     'shows.tasks.process_enterable_lotteries': {'queue': 'celery'},
#     'shows.tasks.enter_user_in_lottery': {'queue': 'celery'},
#     'shows.tasks.run_shows_spider': {'queue': 'celery'},
#
#     'shows.tasks.process_enterable_floods': {'queue': 'flood'},
#     'shows.tasks.enter_user_in_lottery_for_flood': {'queue': 'flood'}
# }

app.autodiscover_tasks()


# shows.tasks.run_shows_spider needs to scrape the data off the site once a
# lottery is open to set lottery objects as enterable_objects. run_shows_spider
# finishes on the order of seconds, eg.
# Task shows.tasks.run_shows_spider[40faa8ce-796d-4ac0-98b8-53b8310f8282] succeeded in 2.1336671939934604s: None
#
# The schedule is set up to run the lottery scraping on the first minute of
# every hour, then process enterable loterries on the fifth minute.
app.conf.CELERYBEAT_SCHEDULE = {
    'run-shows-spider-every-hour': {
        'task': 'shows.tasks.run_shows_spider',
        'schedule': crontab(minute=1, hour='*'),
        'args': None,
        'options': {'queue': 'celery'},
    },
    'process-enterable-lotteries-every-hour': {
        'task': 'shows.tasks.process_enterable_lotteries',
        'schedule': crontab(minute=5, hour='*'),
        'args': None,
        'options': {'queue': 'celery'},
    },
    'process-enterable-floods-every-hour': {
        'task': 'shows.tasks.process_enterable_floods',
        'schedule': crontab(minute=5, hour='*'),
        'args': None,
        'options': {'queue': 'flood'},
    },
}
