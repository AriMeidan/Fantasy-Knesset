from base import *


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': 'fknesset.db',
    },
}
