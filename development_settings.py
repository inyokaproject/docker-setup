from inyoka import INYOKA_VERSION
from inyoka.default_settings import *

# --------- begin: stuff for docker ---------

CACHES['default']['LOCATION'] = 'redis://redis:6379/1'
CACHES['content']['LOCATION'] = 'redis://redis:6379/0'
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
SECRET_KEY = 'docker'
INSTALLED_APPS = INSTALLED_APPS + (
    'inyoka_theme_ubuntuusers',
#    'raven.contrib.django.raven_compat',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'inyoka',
        'USER': 'inyoka',
        'PASSWORD': 'inyoka',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

INTERNAL_IPS = ('0.0.0.0/0',)

# -------- end: stuff for docker ------------

# debug settings
DEBUG = DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ['.ubuntuusers.local']

# url settings
BASE_DOMAIN_NAME = 'ubuntuusers.local:8080'
INYOKA_URI_SCHEME = 'http'
SESSION_COOKIE_DOMAIN = '.ubuntuusers.local'
MEDIA_URL = '//media.%s/' % BASE_DOMAIN_NAME
STATIC_URL = '//static.%s/' % BASE_DOMAIN_NAME
LOGIN_URL='//%s/login/' % BASE_DOMAIN_NAME
ADMIN_MEDIA_PREFIX = STATIC_URL + '/_admin/'
INYOKA_SYSTEM_USER_EMAIL = 'system@' + BASE_DOMAIN_NAME
INYOKA_CONTACT_EMAIL = '@'.join(['webteam', BASE_DOMAIN_NAME])
INYOKA_HOST_STATICS = True
# Language code
LANGUAGE_CODE = 'de-DE'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
