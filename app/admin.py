from django.contrib import admin

# Register your models here.

from .models import Teacher, Student, Classroom

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Classroom)
