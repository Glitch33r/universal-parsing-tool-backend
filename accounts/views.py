from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import auth


def login(request):
    args = dict()
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            args['profile'] = user
            return redirect('/', args)
        else:
            args['login_error'] = 'User not found!'
            return render(request, 'login/login.html', args)
    else:
        return render(request, 'login/login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')


def settings(request):
    pass
