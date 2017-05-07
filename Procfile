web: gunicorn killington.wsgi --log-file -
worker: celery -A killington worker -l info -Q celery --concurrency=4
flood: celery -A killington worker -l info -Q flood --concurrency=8
beat: celery -A killington beat -l info -S django
