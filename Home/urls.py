from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('login/', views.Login_view, name="Login"),
    path('signup/', views.Signup_view, name="Signup"),
    path('signout/', views.signout, name="Signout"),
]


