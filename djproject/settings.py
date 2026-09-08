import os
from core.env import DEBUG, SECRET_KEY, ADMIN_EMAIL, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, SERVER_EMAIL, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Django validates the Host header against this list whenever DEBUG is False
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', '*').split(',') if h.strip()]

# Django 4+ compares the browser Origin header to Host. Extra origins (with
# scheme) go here; nginx must also forward $http_host so the port is kept.
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if o.strip()
]

ADMINS = (
    ('admin', ADMIN_EMAIL),
)

DEFAULT_CHARSET = 'utf-8'

MANAGERS = ADMINS

# Existing tables use 32-bit integer primary keys; keep them to avoid a
# schema migration that only widens the id columns.
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# EMAIL: console backend in Docker so SMTP cannot block requests
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend',
)

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'
SITE_ID = 1
USE_I18N = True
# The models store naive local datetimes, so timezone support stays off.
USE_TZ = False
# SECRET_KEY is imported from env.py

ROOT_URL = '/'
# Templates and admin assets are served under /media/ (production nginx path).
# STATICFILES_DIRS must point at the same tree.
STATIC_URL = '/media/'
_DJPROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_DJPROJECT_DIR)
_MEDIA_DIR = os.environ.get('MEDIA_ROOT', os.path.join(_PROJECT_ROOT, 'htdocs', 'media'))
MEDIA_ROOT = _MEDIA_DIR
STATIC_ROOT = os.path.join(_PROJECT_ROOT, 'staticfiles')
STATICFILES_DIRS = (_MEDIA_DIR,)
ROOT_URLCONF = 'urls'
LOCALE_PATHS = (
    os.path.join(_DJPROJECT_DIR, 'locale'),
)

# core/fixtures is the app's default fixture directory and is found
# automatically; listing it in FIXTURE_DIRS is rejected as a duplicate.

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

_TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]
if os.environ.get('USE_TEMPLATE_CACHE') == '1':
    _TEMPLATE_LOADERS = [
        ('django.template.loaders.cached.Loader', _TEMPLATE_LOADERS),
    ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': _TEMPLATE_LOADERS,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'core',
)
