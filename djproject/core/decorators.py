# coding=utf-8
from settings import ADMINS, DEBUG
from django.shortcuts import render, render_to_response

def auth_required(function):
    '''
    Decorator for views that checks that the user is authenticated,
    if user is not authenticated then '403 HTTP Forbidden' is returned.
    '''
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated():
            #return HttpResponseForbidden()
            return render(request, 'auth.html', {'error_message': 'Необходимо сначала авторизоваться.'})
        else:
            return function(request, *args, **kwargs) 
    return inner    

def ajax_error(error):
    return render_to_response('ajax_error.html', {'admin_mail': ADMINS[0][1], 'error': error, 'debug': DEBUG})

def ajax_upload_error(error):
    return render_to_response('ajax_upload_error.html', {'error': error})

def exception_wrapper(err_f=ajax_error):
    '''
    Decorator that prevent from internal errors.
    '''
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception, e:
                return err_f(e)
        return wrapped_f
    return wrap
