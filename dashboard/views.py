from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from authentication.decorators import is_Verfied

@login_required
@is_Verfied
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile(request):
    return render(request, 'profile.html')
