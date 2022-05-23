from inyoka import INYOKA_VERSION
from production_settings import *

INTERNAL_IPS = ('0.0.0.0/0',)

DEBUG = DEBUG_PROPAGATE_EXCEPTIONS = True

# url settings
#ADMIN_MEDIA_PREFIX = STATIC_URL + '/_admin/'
INYOKA_HOST_STATICS = True

STATIC_ROOT = '/inyoka/theme/inyoka_theme_ubuntuusers/static' ## TODO

INYOKA_USE_AKISMET = False

# Language code
LANGUAGE_CODE = 'de-DE'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtpd'
EMAIL_PORT = 1025

# disable sentry
sentry_sdk.init()
