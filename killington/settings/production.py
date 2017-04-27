import os
import sys
import dj_database_url
from raven.transport import HTTPTransport

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
RAVEN_CONFIG['dsn'] = os.environ['SENTRY_DSN']
RAVEN_CONFIG['release'] = release or 'missing-release-from-env',

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

ACME_CHALLENGE_CONTENT = os.environ['ACME_CHALLENGE_CONTENT']

SECURE_SSL_REDIRECT = True

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SES_DOMAIN = os.environ['SES_DOMAIN']