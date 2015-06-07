# Django settings for atool project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    "accounts.ocf.berkeley.edu",
    "dev-accounts.ocf.berkeley.edu"
]

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

# email
EMAIL_HOST = "smtp"
EMAIL_PORT = 25
EMAIL_USE_TLS = True

# approve
ADMIN_SSH_KEY = "/srv/atool/etc/atool-id_rsa"

# chpass
KRB_KEYTAB = "/srv/atool/etc/chpass.keytab"

# cmds
CMDS_HOST = "ssh.ocf.berkeley.edu"
CMDS_HOST_KEYS_FILENAME = "/srv/atool/etc/ssh_known_hosts"

TEST_OCF_ACCOUNTS = (
    "sanjay",  # an old, sorried account with kerberos princ
    "alec",  # an old, sorried account with no kerberos princ
    "guser",  # an account specifically made for testing
    "nonexist",  # this account does not exist
)

TESTER_CALNET_UIDS = (
    "871036",   # kedo
    "758566",   # waf
    "872544",   # daradib
    "646431",   # sanjayk
    "1034192",  # ckuehl
    "869331",   # tzhu
    "863499",   # morshed
)

# comma separated tuples of CalLink OIDs and student group names
TEST_GROUP_ACCOUNTS = (
    (91740, "The Testing Group"),  # needs to have a real OID, so boo
    (46187, "Open Computing Facility"),  # good old ocf
    (46692, "Awesome Group of Awesome")  # boo another real OID
)

ADMINS = (
    ('kedo', 'kedo@ocf.berkeley.edu'),
)

MANAGERS = ADMINS

DATABASES = {}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/atool_cache',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'not-really-secret__623f2)7y)fz7&bqmlm+kc+olr'

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
    "/srv/atool/src/atool/templates",
)

ALLOWED_INCLUDE_ROOTS = ()

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'atool.calnet',
    'atool.chpass',
    'atool.approve',
    'atool.ocf',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
