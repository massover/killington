from .base import *
import raven

DEBUG = True

SECRET_KEY = 'ia!%$GLg!gsDf8$^cq$SR+ZUkglYUmVNLYPeZb-lxjM_V4#7Rw'

INSTALLED_APPS += [
    'debug_toolbar',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'killington_local',
        'USER': 'killington',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': True,
}

MIDDLEWARE = MIDDLEWARE + [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel'
]

INTERNAL_IPS = ['127.0.0.1', ]

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'

with open('.2captcha', 'r') as fp:
    CAPTCHA_API_KEY = fp.read()

ACME_CHALLENGE_CONTENT = 'acme-challenge-content'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# INSTALLED_APPS += [
#     'raven.contrib.django.raven_compat',
# ]
#
# with open('.sentrydsn', 'r') as fp:
#     RAVEN_CONFIG = {
#         'dsn': fp.read(),
#         # If you are using git, you can also automatically configure the
#         # release based on the git info.
#         'release': raven.fetch_git_sha(BASE_DIR),
#     }
