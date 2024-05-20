from inyoka import INYOKA_VERSION
from production_settings import *

DEBUG = DEBUG_PROPAGATE_EXCEPTIONS = True

# idea via https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
for ip in ips:
    for i in range(0, 20):
        INTERNAL_IPS += [ip[: ip.rfind(".")] + "." + str(i)]

# url settings
#ADMIN_MEDIA_PREFIX = STATIC_URL + '/_admin/'
INYOKA_HOST_STATICS = True

INYOKA_USE_AKISMET = False

# Language code
LANGUAGE_CODE = 'de-DE'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# disable sentry
sentry_sdk.init()

# Django Debug Toolbar Integration
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar',)

