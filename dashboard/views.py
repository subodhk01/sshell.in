from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from authentication.decorators import is_Verfied

@login_required
@is_Verfied
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
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

@login_required
def setting(request):
    return render(request, 'setting.html')
