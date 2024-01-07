from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ClassroomForm, TeacherUpdateForm, StudentForm
from .models import *
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
    students = classroom.students.all()
    return render(request, 'classroom_detail.html', {'classroom': classroom, 'students': students})


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


@login_required
def update_teacher(request, classroom_id):
    classroom = Classroom.objects.get(pk=classroom_id)

    if request.method == 'POST':
        form = TeacherUpdateForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return redirect('classroom_detail',
                            classroom_id=classroom.id)  # Ganti 'classroom_detail' dengan nama URL detail classroom Anda
    else:
        form = TeacherUpdateForm(instance=classroom)

    return render(request, 'update_teacher.html', {'classroom': classroom, 'form': form})


@login_required
def add_student(request, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.classroom = classroom
            student.save()
            classroom.students.add(student)
            return redirect('classroom_detail', classroom_id=classroom.id)
    else:
        form = StudentForm()

    return render(request, 'add_student.html', {'form': form, 'classroom': classroom})


@login_required
def delete_student(request, classroom_id, student_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        classroom.students.remove(student)
        return redirect('classroom_detail', classroom_id=classroom.id)

    return render(request, 'delete_student.html', {'classroom': classroom, 'student': student})


@login_required
def delete_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)

    if request.method == 'POST':
        classroom.delete()
        return redirect('home')

    return render(request, 'delete_classroom.html', {'classroom': classroom})
