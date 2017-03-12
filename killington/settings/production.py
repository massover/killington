import os
import sys
import dj_database_url
from .base import *

DEBUG = False

db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES = {'default': db_from_env}

SECRET_KEY = os.environ['SECRET_KEY']
CELERY_BROKER_URL = os.environ['RABBITMQ_BIGWIG_URL']
CAPTCHA_API_KEY = os.environ['CAPTCHA_API_KEY']

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

release = os.environ.get('SOURCE_VERSION') or os.environ.get('HEROKU_SLUG_COMMIT')

RAVEN_CONFIG = {
    'dsn': os.environ['SENTRY_DSN'],
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': release or '2',
}

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

ACME_CHALLENGE_CONTENT = os.environ['ACME_CHALLENGE_CONTENT']

SECURE_SSL_REDIRECT = True