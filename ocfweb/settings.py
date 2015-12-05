import os
from configparser import ConfigParser
from getpass import getuser

from django.template.base import TemplateSyntaxError


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'not_a_secret'
DEBUG = True

ALLOWED_HOSTS = [
    'www.ocf.berkeley.edu',
    'dev.ocf.berkeley.edu',
    'dev-www.ocf.berkeley.edu',
    'ocfweb.ocf.berkeley.edu',
]

INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'mathfilters',
    'ocfweb',
    'ocfweb.about',
    'ocfweb.atool',
    'ocfweb.docs',
    'ocfweb.main',
    'ocfweb.middleware',
    'ocfweb.stats',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ocfweb.middleware.errors.OcflibErrorMiddleware',
)

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

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# on dev, we use a file-backed cache so that you don't get logged out every
# time you update code and the server restarts.
cache = {
    'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    'LOCATION': os.path.expanduser('~/atool-cache'),
}

CACHES = {  # sessions are stored here
    'default': cache,
    'TIMEOUT': 60 * 60 * 12,  # 12 hours
    'OPTIONS': {
        'MAX_ENTRIES': 1000,
    },
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = False
USE_L10N = False
USE_TZ = True

STATIC_URL = '/static/'
os.environ.setdefault('OCFWEB_STATIC_ROOT', '')
STATIC_ROOT = os.environ['OCFWEB_STATIC_ROOT']

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

CELERY_BROKER = 'redis://create'
CELERY_BACKEND = 'redis://create'


if getuser() == 'ocfweb':
    # not running in development, override options from config file
    conf = ConfigParser()
    conf.read('/etc/ocfweb/ocfweb.conf')

    SECRET_KEY = conf.get('django', 'secret')
    DEBUG = conf.getboolean('django', 'debug')

    STATIC_URL = conf.get('django', 'static_url')
    STATIC_ROOT = conf.get('django', 'static_root')

    CELERY_BROKER = conf.get('celery', 'broker')
    CELERY_BACKEND = conf.get('celery', 'backend')

    # on prod, we use an in-memory cache because we don't care about
    # performance, memory usage, or persistence
    cache = {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}
