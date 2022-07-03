from inyoka import INYOKA_VERSION
from inyoka.default_settings import *

from os.path import join
import socket
import urllib.parse

# Database Setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'inyoka',
        'USER': 'inyoka',
        'PASSWORD': '{{ secret "inyoka-postgres-password" }}',
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
MEDIA_ROOT = '/srv/www/media'
STATIC_ROOT = '/srv/www/static'

# Debug disabled on Production!
DEBUG = TEMPLATE_DEBUG = DATABASE_DEBUG = False

# Cache Setup
CACHE_PREFIX = 'inyoka/'
CACHES['default']['LOCATION'] = 'redis://redis:6379/1'
CACHES['content']['LOCATION'] = 'redis://redis:6379/0'
CACHES['default']['OPTIONS']['PASSWORD'] = CACHES['content']['OPTIONS']['PASSWORD'] = '{{ secret "inyoka-redis-password" }}'

# URL Setup
INYOKA_URI_SCHEME = 'https'
BASE_DOMAIN_NAME = '{{ config "inyoka-base-domain" }}'
SESSION_COOKIE_DOMAIN = f'.{BASE_DOMAIN_NAME}'
MEDIA_URL = f'{INYOKA_URI_SCHEME}://{{ config "inyoka-media-domain" }}/'
STATIC_URL = f'{INYOKA_URI_SCHEME}://{{ config "inyoka-static-domain" }}/'
ALLOWED_HOSTS = [SESSION_COOKIE_DOMAIN]

# Mail Setup
SERVER_EMAIL = 'server-%s@ubuntuusers.de' % socket.gethostname().split('.')[0]
EMAIL_HOST = 'mail.ubuntu-de.org' ## TODO
DEFAULT_EMAIL_FROM = '@'.join(['no-reply', BASE_DOMAIN_NAME])
EMAIL_SUBJECT_PREFIX = f'{BASE_DOMAIN_NAME}: '
INYOKA_SYSTEM_USER_EMAIL = '@'.join(['system', BASE_DOMAIN_NAME])
INYOKA_CONTACT_EMAIL = '@'.join(['webteam', BASE_DOMAIN_NAME])

# Antispam Setup
INYOKA_USE_AKISMET = True
INYOKA_AKISMET_KEY = '{{ secret "inyoka-akismet-key" }}'
INYOKA_AKISMET_URL = f'http://{BASE_DOMAIN_NAME}/'
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

SECRET_KEY = '{{ secret "inyoka-secret-key" }}'

# cookie lifetime (4 weeks)
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 4

# Sentry Configuration
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn='{{ secret "inyoka-sentry-dsn" }}',
    integrations=[DjangoIntegration(),CeleryIntegration()],
    traces_sample_rate=1.0,
    release=INYOKA_VERSION,
    environment='staging',
)


# Celery Setup
redis_password_quoted = urllib.parse.quote('{{ secret "inyoka-redis-password" }}', safe='')
CELERY_BROKER_URL = CELERY_RESULT_BACKEND = f'redis://:{redis_password_quoted}@redis:6379/2'

# HTTPS Setup
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# i18n Setup
LC_ALL = 'de_DE.UTF-8'
LANGUAGE_CODE = 'de-de'

# User Setup
LOGIN_URL = f'{INYOKA_URI_SCHEME}://{BASE_DOMAIN_NAME}/login'
ANONYMOUS_USER_NAME = "anonymous"
INYOKA_ANONYMOUS_GROUP_NAME = "anonymous"
INYOKA_IKHAYA_GROUP_NAME = "Ikhayateam"
INYOKA_REGISTERED_GROUP_NAME = "Registriert"
INYOKA_TEAM_GROUP_NAME = "Team"

# IWL map
INYOKA_INTERWIKI_CSS_PATH = join(MEDIA_ROOT, 'linkmap/linkmap-{hash}.css')

FORUM_DISABLE_POSTING = False

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True ## TODO
