from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return render(request, '../templates/home.html')
        else:
            messages.error(request, 'Error creating account. Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, '../templates/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Error logging in. Please check your credentials.')
    else:
        form = AuthenticationForm()
    return render(request, '../templates/login.html', {'form': form})


def dashboard(request):
    return render(request, '../templates/dashboard.html')


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login', signin, name='login'),
    path('signup', signup, name='signup'),
]
