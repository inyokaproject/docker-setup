from inyoka import INYOKA_VERSION
from production_settings import *

INTERNAL_IPS = ('0.0.0.0/0',)

DEBUG = DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ['.ubuntuusers.localhost']

# url settings
BASE_DOMAIN_NAME = 'ubuntuusers.localhost:8000'
INYOKA_URI_SCHEME = 'http'
SESSION_COOKIE_DOMAIN = '.ubuntuusers.localhost'
MEDIA_URL = '//media.%s/' % BASE_DOMAIN_NAME
STATIC_URL = '//static.%s/' % BASE_DOMAIN_NAME
LOGIN_URL='//%s/login/' % BASE_DOMAIN_NAME
ADMIN_MEDIA_PREFIX = STATIC_URL + '/_admin/'
INYOKA_SYSTEM_USER_EMAIL = '@'.join(['system', BASE_DOMAIN_NAME])
INYOKA_CONTACT_EMAIL = '@'.join(['webteam', BASE_DOMAIN_NAME])
INYOKA_HOST_STATICS = True

STATIC_ROOT = '/inyoka/theme/inyoka_theme_ubuntuusers/static' ## TODO

# Language code
LANGUAGE_CODE = 'de-DE'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
