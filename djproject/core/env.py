# coding=utf-8
import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """
    Get the environment variable or return exception.
    """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)

# Database settings
DB_NAME = get_env_variable('DB_NAME')
DB_USER = get_env_variable('DB_USER')
DB_PASSWORD = get_env_variable('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')

# Email and admin settings are optional: mail delivery is not required to serve
# the site, so missing values must not stop the process from starting.
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '25')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'root@localhost')

# Admin settings
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@localhost')

# Secret key
SECRET_KEY = get_env_variable('SECRET_KEY')

# Debug mode
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
