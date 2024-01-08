from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Teacher, Student, Classroom


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class ClassroomForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), empty_label="Select Teacher")
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), required=False)

    class Meta:
        model = Classroom
        fields = ['name', 'teacher', 'students']

    def save(self, commit=True):
        classroom = super().save(commit=False)
        if commit:
            classroom.save()
            self.save_m2m()
        return classroom


class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['teacher']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email']


class EditStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email']


class AssignStudentForm(forms.Form):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email']
