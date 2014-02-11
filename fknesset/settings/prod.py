from base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_environ('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY!
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# add SSLifyMiddleware as the first MIDDLEWARE_CLASSE
# classes = list(MIDDLEWARE_CLASSES)
# classes.insert(0, 'sslify.middleware.SSLifyMiddleware')
# MIDDLEWARE_CLASSES = tuple(classes)

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = dict(default=dj_database_url.config())

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
STATIC_ROOT = 'staticfiles'
