from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
import os
# Create your views here.

def signed_in(func):
    def inner_func(*args, **kwargs):
        request = args[0]
        if request.user.is_authenticated:
            return func(*args, **kwargs)
        else:
            messages.warning(request, "You need to login first")
            return redirect("Home")
    return inner_func

def logged_out(func):
    def inner_func(*args, **kwargs):
        request = args[0]
        if request.user.is_authenticated:
            messages.warning(request, "You can't access this page while logged in")
            return redirect("Home")
        else:
            return func(*args, **kwargs)
    return inner_func

def admin_page(func):
    def inner_func(*args, **kwargs):
        request = args[0]
        if request.user.staff_status():
            return func(*args, **kwargs)
        else:
            messages.warning(request, "You need to be an admin to access this page")
            return redirect("Home")
    return inner_func
        




signout = LogoutView.as_view(template_name = 'home/signout.html')

def home(request):
    picture = os.path.join(settings.MEDIA_URL, "image/400097700330_82090.jpg")
    Contents = {'title':"AniBtoon", "picture":picture}
    return render(request, 'index.html', Contents)

@logged_out
def Login_view(request):
    if request.method=="POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('Home')
    else:
        form = AuthenticationForm()
    context = {'title': "Login", 'form':form}
    return render(request, 'home/login.html',context)

@logged_out
def Signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    context = {'title': 'signup', 'form': form}
    return render(request, 'home/signup.html', context)




