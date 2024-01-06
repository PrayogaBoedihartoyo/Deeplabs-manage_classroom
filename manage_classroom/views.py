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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            if username == 'admin' and password == 'admin':
                user = form.get_user()
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Incorrect username or password. Please try again.')
        else:
            messages.error(request, 'Error logging in. Please check your credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def dashboard(request):
    return render(request, '../templates/dashboard.html')


def home(request):
    return render(request, '../templates/home.html')
