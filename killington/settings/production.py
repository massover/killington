import os
import dj_database_url
from .base import *

DEBUG = False

db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES = {'default': db_from_env}

SECRET_KEY = os.environ['SECRET_KEY']
CELERY_BROKER_URL = os.environ['RABBITMQ_BIGWIG_URL']
CAPTCHA_API_KEY = os.environ['CAPTCHA_API_KEY']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]
RAVEN_CONFIG = {
    'dsn': os.environ['SENTRY_DSN'],
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    #'release': os.environ['HEROKU_SLUG_COMMIT'],
    'release': '1',
}