from base import *


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'fknesset',
        'USER': 'su',
        'PASSWORD': get_environ('DB_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}
