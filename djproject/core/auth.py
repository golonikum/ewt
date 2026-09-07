# coding=utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from core.decorators import *

#*********************************************************
#******************** VIEWS
#*********************************************************
@ensure_csrf_cookie
def index(request):
    if not request.user.is_authenticated():
        if request.method == 'GET':
            return render(request, 'auth.html')
        elif request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'index.html', {'user': user})
            else:
                return render(request, 'auth.html', {'error_message': 'Пожалуйста, введите верные имя пользователя и пароль.'})            
    else:
        return render(request, 'index.html', {'user': request.user})

@auth_required
def exit(request):
    logout(request)    
    return render(request, 'auth.html')

