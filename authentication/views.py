from django.shortcuts import render
from django.contrib.auth import get_user_model, logout as UserLogout
from django_email_verification import sendConfirm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

def login(request):
    pass

def signup(request):
    user = get_user_model().objects.create(password="qwerty@123",username="qwerty1234", email="subodh.verma.min19@iitbhu.ac.in")
    sendConfirm(user)
    return HttpResponse('sent')

def logout(request):
    UserLogout(request)