from django.urls import path
from django.contrib import admin
from .views import *


urlpatterns = [
    path('admin', admin.site.urls),
    path('', signin, name='login'),
    path('signup', signup, name='signup'),
    path('logout', sign_out, name='logout'),
    path('home', home, name='home'),

    path('add_classroom/', add_classroom, name='add_classroom'),
    path('classroom/<int:classroom_id>/', classroom_detail, name='classroom_detail'),
    path('classroom/<int:classroom_id>/delete_classroom/', delete_classroom, name='delete_classroom'),

    path('teacher_list/', teacher_list, name='teacher_list'),
    path('add_teacher/', add_teacher, name='add_teacher'),
    path('classroom/<int:classroom_id>/update_teacher/', update_teacher, name='update_teacher'),
    path('edit_teacher/<int:teacher_id>/', edit_teacher, name='edit_teacher'),
    path('delete_teacher/<int:teacher_id>/', delete_teacher, name='delete_teacher'),

    path('classroom/<int:classroom_id>/add_student/', add_student, name='add_student'),
    path('classroom/<int:classroom_id>/assign_student/', assign_student, name='assign_student'),
    path('classroom/<int:classroom_id>/delete_student/<int:student_id>/', delete_student, name='delete_student'),
    path('classroom/<int:classroom_id>/edit_student/<int:student_id>/', edit_student, name='edit_student'),

    path('classroom/<int:classroom_id>/download-pdf/', generate_classroom_pdf, name='download_classroom_pdf'),
]
