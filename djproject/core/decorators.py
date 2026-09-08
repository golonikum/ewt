# coding=utf-8
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

def auth_required(function):
    '''
    Decorator for views that checks that the user is authenticated,
    if user is not authenticated then '403 HTTP Forbidden' is returned.
    '''
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated:
            #return HttpResponseForbidden()
            return render(request, 'auth.html', {'error_message': 'Необходимо сначала авторизоваться.'})
        else:
            return function(request, *args, **kwargs)
    return inner

# The error renderers receive only the exception, so they render without a
# request the way render_to_response used to.
def ajax_error(error):
    return HttpResponse(render_to_string('ajax_error.html', {'admin_mail': settings.ADMINS[0][1], 'error': error, 'debug': settings.DEBUG}))

def ajax_upload_error(error):
    return HttpResponse(render_to_string('ajax_upload_error.html', {'error': error}))

def exception_wrapper(err_f=ajax_error):
    '''
    Decorator that prevent from internal errors.
    '''
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                return err_f(e)
        return wrapped_f
    return wrap
