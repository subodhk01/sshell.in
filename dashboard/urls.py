from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('courses/', views.courses, name="courses"),
    path('resources/', views.resources, name="resources"),
    path('profile/', views.profile, name="profile"),
    path('setting/', views.setting, name="setting")
]
