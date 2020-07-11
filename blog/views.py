from django.shortcuts import render

def blogHome(request):
    return render(request, 'bloghome.html')

def blog(request):
    return None