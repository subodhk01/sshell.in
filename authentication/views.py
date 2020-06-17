from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login as authLogin, authenticate ,logout as UserLogout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django_email_verification import sendConfirm

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.user.is_authenticated :
        return redirect(index)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            authLogin(request, user)
            return redirect(index)
        else:
            return render(request, 'accounts/login.html', { 'msg': "Invalid Credentials" })
    else:
        return render(request, 'accounts/login.html')

def signup(request):
    user = get_user_model().objects.create(password="qwerty@123",username="qwerty1234", email="subodh.verma.min19@iitbhu.ac.in")
    return HttpResponse('sent')

def logout(request):
    UserLogout(request)
    return redirect(index)