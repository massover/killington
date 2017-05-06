from .base import *

DEBUG = False
SECRET_KEY = 'ia!%$GLg!gsDf8$^cq$SR+ZUkglYUmVNLYPeZb-lxjM_V4#7Rw'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'killington_test',
        'USER': 'killington',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CAPTCHA_API_KEY = 'Not used in testing'
ACME_CHALLENGE_CONTENT = 'acme-challenge-content'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

SES_DOMAIN = 'example.com'

G_RECAPTCHA_RESPONSE_TIMEOUT = -1
AFTER_CAPTCHA_UPLOAD_REQUEST_DELAY = 0