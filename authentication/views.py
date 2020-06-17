from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login as authLogin, authenticate ,logout as UserLogout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from authentication.models import RandomToken
from django_email_verification import sendConfirm

def index(request):
    return render(request, 'index.html')

def signupsuccess(request, token):
    TokenInstance = get_object_or_404(RandomToken, token=token)
    TokenInstance.clean()
    TokenInstance = get_object_or_404(RandomToken, token=token)
    return HttpResponse('Confirmation email sent to you email, checkin the email and login.')

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
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            password2 = request.POST['password2']
            email = request.POST['email']
        except:
            msg = "Some of the fields are missing."
            return render(request, 'accounts/register.html', { 'msg': msg })
        if len(password) > 6:
            if password != password2:
                msg = "Entered Passwords do not match"
                return render(request, 'accounts/register.html', { 'msg': msg, 'email':email })
            else:
                try:
                    user = get_user_model().objects.create_user(username, email, password)
                    sendConfirm(user)
                    TokenInstance = RandomToken(user=user, expiry_minutes=20)
                    TokenInstance.save()
                    return redirect("signupsuccess", token=TokenInstance.token)
                except Exception as e:
                    msg = "Unable to signup"
                    if "UNIQUE" in str(e):
                        if 'email' in str(e):
                            msg = "Account with email already exists"
                        elif 'username' in str(e):
                            msg = "Account with Username already exists"
                    return render(request, 'accounts/register.html', { 'msg': msg, 'email':email })
        else:
            msg = "Password length should be more than 6 digits"
            return render(request, 'accounts/register.html', { 'msg': msg, 'email':email })
    else:
        return render(request, 'accounts/register.html')

def logout(request):
    UserLogout(request)
    return redirect(index)