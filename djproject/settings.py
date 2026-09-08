import os
from core.env import DEBUG, SECRET_KEY, ADMIN_EMAIL, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, SERVER_EMAIL, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

TEMPLATE_DEBUG = DEBUG

# Django validates the Host header against this list whenever DEBUG is False
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', '*').split(',') if h.strip()]

ADMINS = (
    ('admin', ADMIN_EMAIL),
)

DEFAULT_CHARSET = 'utf-8'

MANAGERS = ADMINS

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
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
LANGUAGE_CODE = 'ru-RU'
SITE_ID = 1
USE_I18N = True
# SECRET_KEY is imported from env.py

ROOT_URL = '/'
STATIC_ROOT = ''
# Templates and admin assets are served under /media/ (production nginx path).
# runserver's StaticFilesHandler intercepts STATIC_URL, so STATICFILES_DIRS
# must point at the same tree. MEDIA_URL must stay distinct from STATIC_URL.
STATIC_URL = '/media/'
_DJPROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_DJPROJECT_DIR)
_MEDIA_DIR = os.environ.get('MEDIA_ROOT', os.path.join(_PROJECT_ROOT, 'htdocs', 'media'))
MEDIA_ROOT = _MEDIA_DIR
STATICFILES_DIRS = (_MEDIA_DIR,)
ROOT_URLCONF = 'urls'


FIXTURE_DIRS = (
   os.path.join(_DJPROJECT_DIR, 'core', 'fixtures'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
if os.environ.get('USE_TEMPLATE_CACHE') == '1':
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
    )
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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

#if DEBUG:
#    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
#    INSTALLED_APPS += ('debug_toolbar',)
#    DEBUG_TOOLBAR_CONFIG = {
#        'EXCLUDE_URLS': ('/admin',), 
#        'INTERCEPT_REDIRECTS': False,
#    }
#    INTERNAL_IPS = ('127.0.0.1',)
