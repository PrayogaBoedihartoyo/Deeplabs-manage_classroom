from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ClassroomForm
from .models import Classroom
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, '../templates/signup.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('posts')
        else:
            return render(request, '../templates/signup.html', {'form': form})


@csrf_exempt
def signin(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, '../templates/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')

        messages.error(request, f'Invalid username or password')
        return render(request, '../templates/login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('login')


@login_required
def home(request):
    classrooms = Classroom.objects.all()
    return render(request, 'home.html', {'classrooms': classrooms})


def classroom_detail(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    return render(request, 'classroom_detail.html', {'classroom': classroom})


def add_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.save()
            form.save_m2m()

            students = form.cleaned_data.get('students')
            if students:
                classroom.students.set(students)

            return redirect('home')
    else:
        form = ClassroomForm()

    return render(request, 'add_classroom.html', {'form': form})
