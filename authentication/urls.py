from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/success/<token>/', views.signupsuccess, name="signupsuccess"),
    path('passwordreset', views.resetpassword, name="passwordreset"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
]
