from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as mail_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('', include('authentication.urls'))
]
