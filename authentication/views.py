from django.shortcuts import render
from django.contrib.auth import get_user_model
from django_email_verification import sendConfirm

def signup(request):
    user = get_user_model().objects.create(username="qwerty123", password="qwerty@123", email="vermasubodhk@gmail.com")
    sendConfirm(user)
