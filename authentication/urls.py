from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('emailnotverified/', views.emailnotverified, name="emailnotverified"),
    path('signup/success/<token>/', views.signupsuccess, name="signupsuccess"),
    path('passwordreset/', views.resetpassword, name="passwordreset"),
    path('passwordreset/forgotpassword/', views.forgotpasswordreset, name="forgotpasswordreset"),
    path('forgotpassword', views.forgotpassword, name="forgotpassword"),
    path('team/', views.team, name="team"),
    path('privacypolicy/', views.privacypolicy, name="privacypolicy"),
    path('contact/', views.contact, name="contact"),
    path('success/<token>/<msg>/', views.success, name="success"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
]
