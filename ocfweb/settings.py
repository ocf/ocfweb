import configparser
import os
import socket
import tempfile
import warnings

from django.core.cache import CacheKeyWarning
from django.template.base import TemplateSyntaxError


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTING = os.environ.get('OCFWEB_TESTING') == '1'

ALLOWED_HOSTS = [
    'www.ocf.berkeley.edu',
    'dev.ocf.berkeley.edu',
    'dev-www.ocf.berkeley.edu',
    'ocfweb.ocf.berkeley.edu',
]

INSTALLED_APPS = (
    'bootstrapform',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'mathfilters',

    'ocfweb',
    'ocfweb.about',
    'ocfweb.account',
    'ocfweb.announcements',
    'ocfweb.docs',
    'ocfweb.login',
    'ocfweb.main',
    'ocfweb.middleware',
    'ocfweb.stats',
    'ocfweb.test',
    'ocfweb.tv',
    'ocfweb.api',
    'ocfweb.reservations',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ocfweb.middleware.errors.OcflibErrorMiddleware',
)

# write flash messages into the session
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ROOT_URLCONF = 'ocfweb.urls'


class InvalidReferenceInTemplate(str):
    """Raise exceptions on invalid references in templates.

    By default Django just replaces references to undefined variables with
    empty strings. This is a horrible idea, so we instead hack it to raise an
    exception.
    """

    def __mod__(self, ref):
        raise TemplateSyntaxError('Invalid reference in template: {}'.format(ref))


TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.messages.context_processors.messages',
            'ocfweb.context_processors.ocf_template_processor',
        ],
        'string_if_invalid': InvalidReferenceInTemplate('%s'),
    },
}]

WSGI_APPLICATION = 'ocfweb.wsgi.application'

DATABASES = {}

# store sessions in the cache
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# XXX: DO NOT CHANGE
# Ensure cookies can't be read by JavaScript or users.
# Our proxy filters cookies starting with "OCFWEB_" when going to user sites,
# so it's important our cookies match this pattern.
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_NAME = 'OCFWEB_CSRF_TOKEN'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_PATH = '/'
SESSION_COOKIE_NAME = 'OCFWEB_SESSIONID'

CACHES = {  # sessions are stored here
    'TIMEOUT': 60 * 60 * 12,  # 12 hours
    'OPTIONS': {
        'MAX_ENTRIES': 1000,
    },
}

# Silence cache key warnings, since we are using redis and not memcached.
# https://docs.djangoproject.com/en/1.9/topics/cache/#cache-key-warnings
warnings.simplefilter('ignore', CacheKeyWarning)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = False
USE_L10N = False
USE_TZ = True

X_FRAME_OPTIONS = 'DENY'

# log exceptions to stderr
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

# Load the rest of the config from a file.
# We populate this file in dev with fake values or values for development
# databases, so this still works (as long as you're on supernova).
conf = configparser.ConfigParser()
conf.read('/etc/ocfweb/ocfweb.conf')

SECRET_KEY = conf.get('django', 'secret')
DEBUG = conf.getboolean('django', 'debug')

STATIC_URL = conf.get('django', 'static_url')
STATIC_ROOT = os.environ.get('OCFWEB_STATIC_ROOT') or conf.get('django', 'static_root')

CELERY_BROKER = conf.get('celery', 'broker')
CELERY_BACKEND = conf.get('celery', 'backend')

OCFMAIL_USER = conf.get('ocfmail', 'user')
OCFMAIL_PASSWORD = conf.get('ocfmail', 'password')
OCFMAIL_DB = conf.get('ocfmail', 'db')

if not DEBUG:
    # Prod-only settings.
    CACHES['default'] = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': conf.get('django', 'redis_uri'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }

    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_DOMAIN = 'www.ocf.berkeley.edu'
    CSRF_TRUSTED_ORIGINS = ['www.ocf.berkeley.edu']
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = 'www.ocf.berkeley.edu'
else:
    # Dev-only settings.
    CACHES['default'] = {
        # On dev, we use a file-backed cache so that you don't get logged out
        # every time you update code and the server restarts.
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    }
    if not TESTING:
        CACHES['default']['LOCATION'] = os.path.expanduser('~/.ocfweb-cache')
    else:
        # Use a temporary directory to prevent races where multiple tests
        # simultaneously try to write to the same cache directory.
        # Save this directory in a variable so it doesn't get deleted until
        # the app exits.
        cache_dir = tempfile.TemporaryDirectory()
        CACHES['default']['LOCATION'] = cache_dir.name

    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    ALLOWED_HOSTS += [
        socket.getfqdn(),
        socket.gethostname(),
        socket.gethostname() + '.ocf.io',
        'localhost',
        '127.0.0.1',
        '::1',
    ]
