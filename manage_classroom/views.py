from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


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
            return redirect('login')
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
                            classroom_id=classroom.id)
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


def edit_student(request, classroom_id, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = EditStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('classroom_detail', classroom_id=classroom_id)
    else:
        form = EditStudentForm(instance=student)

    return render(request, 'edit_student.html', {'form': form, 'classroom_id': classroom_id, 'student_id': student_id})


def assign_student(request, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    students = Student.objects.all()

    if request.method == 'POST':
        form = AssignStudentForm(request.POST)
        if form.is_valid():
            selected_students = form.cleaned_data['students']
            classroom.students.add(*selected_students)
            return redirect('classroom_detail', classroom_id=classroom.id)
    else:
        form = AssignStudentForm()

    return render(request, 'assign_student.html', {'classroom': classroom, 'students': students, 'form': form})


def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.save()
            return redirect('home')
    else:
        form = TeacherForm()

    return render(request, 'add_teacher.html', {'form': form})


def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})


def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        return HttpResponseRedirect('/teacher_list/')

    return render(request, 'delete_teacher.html', {'teacher': teacher})


def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/teacher_list/')
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'edit_teacher.html', {'form': form, 'teacher_id': teacher_id})


def generate_classroom_pdf(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    teacher = classroom.teacher
    students = classroom.students.all()

    template_path = '../templates/classroom_structure_template.html'
    context = {'classroom': classroom, 'teacher': teacher, 'students': students}
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{classroom.name}_structure.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


def handler404(request, exception):
    return render(request, '404.html', status=404)
