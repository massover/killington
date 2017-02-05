import dj_database_url
from .base import *

DEBUG = False

db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES = {'default': db_from_env}

SECRET_KEY = os.environ['SECRET_KEY']