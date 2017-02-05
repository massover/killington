web: gunicorn killington.wsgi --log-file -
worker: celery -A killington worker -l info
beat: celery -A killington beat -l info -S django