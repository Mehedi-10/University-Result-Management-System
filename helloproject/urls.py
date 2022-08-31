from django.urls import path
from .views import *

#
urlpatterns = [
    path('', index, name='index_page'),
    path('who_are_you.html', who_are_u, name='who_are_you'),
    path('teacherlogin.html', signin_teacher),
    path('register_teacher', teacher_signup),
    path('register_student.html', student_signup),
    path('select_result_as_teacher.html', select_result_as_teacher),
    path('teacher_beforeFinal.html', process_before_final),
    path('nothing', saving),
    path('teacher_Final.html', process_final_internal),
    path('final', savingfinal),
    path('student_login.html', signin_student),
    path('show_before_final.html', show_before_final),
    path('show_final.html', showfinal),
    path('select_result_as_student.html', select_result_as_student),
    path('assign_course', assign_course),
    path('add_new_course', add_course),
    path('admin_home', admin_home),
    path('t_select', tselect),
    path('exam_committee', exam_com),
    path('teachers', showallteacher),
    path('forgotpassword', changepassword),
    path('sendcode', verify),
    path('change_pass', changepass_conf),
    path('students', show_all_student),
]
