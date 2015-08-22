import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'not_a_secret-a(y))f7-_^ji^ezc5k7l%thr-m@(pk^rf)rz+)p#v82mmc_1dh'
DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ocfweb',
    'ocfweb.main',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ocfweb.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'ocfweb.wsgi.application'

DATABASES = {}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = True

os.environ.setdefault('OCFWEB_STATIC_URL', '/static/')
STATIC_URL = os.environ['OCFWEB_STATIC_URL']
os.environ.setdefault('OCFWEB_STATIC_ROOT', '')
STATIC_ROOT = os.environ['OCFWEB_STATIC_ROOT']

X_FRAME_OPTIONS = 'DENY'
