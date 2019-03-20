from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'default/index.html')
