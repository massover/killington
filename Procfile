web: gunicorn killington.wsgi --log-file -
worker: celery -A killington worker -l info -Q celery
flood: celery -A killington worker -l info -Q flood
beat: celery -A killington beat -l info -S django
