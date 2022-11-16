from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    print(username)
    print(password)
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        return render(request, 'login.html', locals())


def index(request):
    username = request.user.username
    if username:
        print("username : " + username)
    return render(request, 'index.html', {
        'username': username,
    })


def logout(request):
    auth.logout(request)
    # return render('registration/login.html')
    return HttpResponseRedirect('/accounts/login/')
