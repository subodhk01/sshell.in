from django.urls import path
from . import views

urlpatterns = [
    path('blog/home', views.blogHome, name="bloghome"),
    path('blog.<slug>/', views.blog, name="blog")
]
