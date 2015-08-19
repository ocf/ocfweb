import os
import os.path
import socket
from configparser import ConfigParser


# this is validated against the "Host" header the user sends, so
# 'earthquake.o.b.e' or 'localhost' won't work here
#
# it's ok to not include dev-accounts, because there is no validation when
# DEBUG = True
ALLOWED_HOSTS = ['accounts.ocf.berkeley.edu']

DEBUG = TEMPLATE_DEBUG = socket.getfqdn().startswith('dev-')

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

# email
# TODO: send mail via ocflib
EMAIL_HOST = 'smtp'
EMAIL_PORT = 25
EMAIL_USE_TLS = True

# chpass
PASSWORD_ENCRYPTION_PUBKEY = '/etc/ocf-atool/create.pub'
KRB_KEYTAB = '/etc/ocf-atool/chpass.keytab'

# cmds
CMDS_HOST = 'ssh.ocf.berkeley.edu'
CMDS_HOST_KEYS_FILENAME = '/etc/ocf-atool/ssh_known_hosts'

TEST_OCF_ACCOUNTS = (
    'sanjay',  # an old, sorried account with kerberos princ
    'alec',  # an old, sorried account with no kerberos princ
    'guser',  # an account specifically made for testing
    'nonexist',  # this account does not exist
)

TESTER_CALNET_UIDS = (
    '872544',   # daradib
    '1034192',  # ckuehl
    '869331',   # tzhu
)

# comma separated tuples of CalLink OIDs and student group names
TEST_GROUP_ACCOUNTS = (
    (91740, 'The Testing Group'),  # needs to have a real OID, so boo
    (46187, 'Open Computing Facility'),  # good old ocf
    (46692, 'Awesome Group of Awesome')  # boo another real OID
)

DATABASES = {}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
if DEBUG:
    # on dev, we use a file-backed cache so that you don't get logged out every
    # time you update code and the server restarts.
    cache = {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.expanduser('~/atool-cache'),
    }
else:
    # on prod, we use an in-memory cache because we don't care about
    # performance, memory usage, or persistence
    cache = {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}

CACHES = {  # sessions are stored here
    'default': cache,
    'TIMEOUT': 60 * 60 * 12,  # 12 hours
    'OPTIONS': {
        'MAX_ENTRIES': 1000,
    },
}

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False

conf = ConfigParser()
conf.read('/etc/ocf-atool/ocf-atool.conf')

SECRET_KEY = conf.get('django', 'secret')
CELERY_BROKER = conf.get('celery', 'broker')
CELERY_BACKEND = conf.get('celery', 'backend')


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'atool.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates'),
)

ALLOWED_INCLUDE_ROOTS = ()

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'atool.calnet',
    'atool.chpass',
    'atool.approve',
    'atool.ocf',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

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
