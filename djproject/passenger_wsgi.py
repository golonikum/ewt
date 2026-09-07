import os, sys
sys.path.insert(0,'/usr/lib/python2.7/site-packages/django-1.4')
sys.path.append('/home/g/golonru/etrainer/djproject')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
