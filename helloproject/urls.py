from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index_page'),
    path('teacherlogin.html', signin_T),
    path('register_user.html', signup),
    path('select_result_as_teacher.html', select_result_as_teacher),
    path('teacher_beforeFinal.html', before_final),
    path('nothing', saving),
    path('excel.html', excelup),
    path('student_login.html', signin_S),
    path('select_result_as_student.html', select_result_as_student),
    path('enroll_course.html', course_enroll),
    path('add_new_course.html', add_course),
    path('func',func,name='func'),

]
