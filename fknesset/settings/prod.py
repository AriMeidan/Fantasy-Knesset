from base import *



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


CSRF_COOKIE_SECURE = True


SESSION_COOKIE_SECURE = True


# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = dict(default=dj_database_url.config())

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
