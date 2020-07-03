from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from authentication.decorators import EmailVerified
from django.db import transaction
import urllib    


@login_required
@EmailVerified
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
@EmailVerified
def courses(request):
    return render(request, 'courses.html')

@login_required
@EmailVerified
def resources(request):
    return render(request, 'resources.html')

@login_required
@EmailVerified
def profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get('first_name') or user.first_name
        user.last_name = request.POST.get('last_name') or user.last_name
        user.website = request.POST.get('website') or user.website
        user.country = request.POST.get('country') or user.country
        user.about = request.POST.get('about') or user.about
        user.save()
        return redirect('profile')
    return render(request, 'profile.html')


@require_http_methods(['GET', 'POST'])
@login_required
@EmailVerified
@transaction.atomic
def setting(request):
    user = request.user
    if request.method == "POST":
        try:
            old_password = request.POST.get('password')
            new_password = request.POST['new_password']
            new_password2 = request.POST['new_password2']
        except KeyError:
            msg = "Missing Fields"
            return render(request, 'setting.html', {'msg':msg,'has_password':user.has_password })
        if new_password != new_password2:
            msg = "Passwords do not match"
            return render(request, 'setting.html', {'msg':msg, 'has_password':user.has_password })
        if len(new_password) >= 6:
            if old_password:
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    response = redirect('login')
                    response['Location'] += "?" + urllib.parse.urlencode({'password_reset':True})
                    return response
                else:
                    msg = "Invalid Old Password"
                    return render(request, 'setting.html', {'msg':msg,'has_password':user.has_password })
            elif not user.has_password:
                user.set_password(new_password)
                user.has_password = True
                user.save()
                response =  redirect('login')
                response['Location'] += "?" + urllib.parse.urlencode({'password_reset':True})
                return response
            else:
                msg = "Missing Old Password"
                return render(request, 'setting.html', {'msg':msg,'has_password':user.has_password })
        else:
            msg = "Password length should be at least 6 digits."
            return render(request, 'setting.html', {'msg':msg}, {'has_password':user.has_password })
    else:
        return render(request, 'setting.html', {'has_password':user.has_password})