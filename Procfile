web: gunicorn killington.wsgi --log-file -
worker: celery -A killington worker -l info
beat: celery -A killington beat -l info -S django
flower: celery flower -A killington --basic_auth=$FLOWER_BASIC_AUTH