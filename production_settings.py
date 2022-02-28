from inyoka import INYOKA_VERSION
from inyoka.default_settings import *
from os.path import join
import socket

def read_docker_secret(secret_name):
    with open('/run/secrets/{}'.format(secret_name)) as secret:
        return secret.read()

# Database Setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'inyoka',
        'USER': 'inyoka',
        'PASSWORD': read_docker_secret('inyoka-postgres-password'),
        'HOST': 'postgres',
        'PORT': '5432',
        'CONN_MAX_AGE': None,
    }
}

# Installed Apps with Theme
INSTALLED_APPS += (
    'inyoka_theme_ubuntuusers',
)

# Location of Media and Static Files
MEDIA_ROOT = '/srv/www/ubuntuusers/media' ## TODO
STATIC_ROOT = '/srv/www/ubuntuusers/static' ## TODO

# Debug disabled on Production!
DEBUG = TEMPLATE_DEBUG = DATABASE_DEBUG = False

# Cache Setup
CACHE_PREFIX = 'inyoka/'
CACHES['default']['LOCATION'] = 'redis://redis:6379/1'
CACHES['content']['LOCATION'] = 'redis://redis:6379/0'
CACHES['default']['OPTIONS']['PASSWORD'] = CACHES['content']['OPTIONS']['PASSWORD'] =  '{{ secret "inyoka-redis-password" }}'

# URL Setup
INYOKA_URI_SCHEME = 'https'
BASE_DOMAIN_NAME = 'ubuntuusers.de' ## TODO
SESSION_COOKIE_DOMAIN = '.%s' % BASE_DOMAIN_NAME
MEDIA_URL = 'https://media-cdn.ubuntu-de.org/' ## TODO
STATIC_URL = 'https://static-cdn.ubuntu-de.org/'
ALLOWED_HOSTS = [SESSION_COOKIE_DOMAIN]

# Mail Setup
SERVER_EMAIL = 'server-%s@ubuntuusers.de' % socket.gethostname().split('.')[0]
EMAIL_HOST = 'mail.ubuntu-de.org' ## TODO
DEFAULT_EMAIL_FROM = '@'.join(['no-reply', BASE_DOMAIN_NAME])
EMAIL_SUBJECT_PREFIX = '%s: ' % BASE_DOMAIN_NAME
INYOKA_SYSTEM_USER_EMAIL = '@'.join(['system', BASE_DOMAIN_NAME])
INYOKA_CONTACT_EMAIL = '@'.join(['webteam', BASE_DOMAIN_NAME])

# Antispam Setup
INYOKA_USE_AKISMET = True
INYOKA_AKISMET_KEY = read_docker_secret('inyoka-akismet-key')
INYOKA_AKISMET_URL = 'http://ubuntuusers.de/'
INYOKA_AKISMET_DEFAULT_IS_SPAM = False

# Forum Surge Protection
FORUM_SURGE_PROTECTION_TIMEOUT = 30

# Wiki Setup
WIKI_DISCUSSION_FORUM = 'wiki'
WIKI_MAIN_PAGE = 'Startseite'
WIKI_TEMPLATE_BASE = 'Wiki/Vorlagen'
WIKI_PRIVILEGED_PAGES = ['ubuntuusers', 'Trash', 'Wiki/ACL']
WIKI_RECENTCHANGES_MAX = 500

# Username of the System User
INYOKA_SYSTEM_USER = 'ubuntuusers'

SECRET_KEY = read_docker_secret('inyoka-secret-key')

# cookie lifetime (4 weeks)
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 4

# Sentry Configuration
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=read_docker_secret('inyoka-sentry-dsn'),
    integrations=[DjangoIntegration(),CeleryIntegration()],
    traces_sample_rate=1.0,
    release=INYOKA_VERSION,
    environment='staging',
)


# Celery Setup
CELERY_BROKER_URL = CELERY_RESULT_BACKEND = 'redis://{{ secret "inyoka-redis-password" }}@redis:6379/2'

# HTTPS Setup
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# i18n Setup
LC_ALL = 'de_DE.UTF-8'
LANGUAGE_CODE = 'de-de'

# User Setup
LOGIN_URL = 'https://%s/login' % BASE_DOMAIN_NAME
ANONYMOUS_USER_NAME = "anonymous"
INYOKA_ANONYMOUS_GROUP_NAME = "anonymous"
INYOKA_IKHAYA_GROUP_NAME = "Ikhayateam"
INYOKA_REGISTERED_GROUP_NAME = "Registriert"
INYOKA_TEAM_GROUP_NAME = "Team"

# IWL map
INYOKA_INTERWIKI_CSS_PATH = join(MEDIA_ROOT, 'linkmap/linkmap-{hash}.css')

FORUM_DISABLE_POSTING = False

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True ## TODO
