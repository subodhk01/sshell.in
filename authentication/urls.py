from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('email/<token>', views.email_verify, name="emailverify"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
]
