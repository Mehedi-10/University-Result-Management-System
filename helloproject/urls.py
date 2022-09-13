from django.urls import path
from .views import *

#
urlpatterns = [
    path('', index, name='index_page'),
    path('logout', logout),
    path('give_access', give_access),
    path('logoutadmin', adminlogout),
    path('loginadmin', admin_signin, name='getout'),
    path('send_edit_request', send_edit_request),
    path('who_are_you.html', who_are_u, name='who_are_you'),
    path('teacherlogin.html', signin_teacher),
    path('ec_teacherlogin', signin_ecteacher),
    path('register_teacher', teacher_signup),
    path('register_student', student_signup),
    path('select_result_as_teacher.html', select_result_as_teacher),
    path('ec_select_result_as_teacher', ec_select_result_as_teacher),
    path('teacher_beforeFinal.html', process_before_final),
    path('nothing', saving),
    path('ecnothing', ecsaving),
    path('ecfinal', ecsavingfinal),
    path('teacher_Final.html', process_final_internal),
    path('teacher_beforeFinal.html', process_before_final),
    path('ec_teacher_beforeFinal', ec_process_before_final),
    path('ec_teacher_Final', ec_process_final_internal),
    path('final', savingfinal),
    path('student_login', signin_student),
    path('show_before_final.html', show_before_final),
    path('show_final.html', showfinal),
    path('select_result_as_student.html', select_result_as_student),
    path('assign_course', assign_course),
    path('add_new_course', add_course),
    path('admin_home', admin_home),
    path('t_select', teacher_select_with_ajax),
    path('ec_t_select', ec_teacher_select_with_ajax),
    path('exam_committee', exam_com),
    path('teachers', showallteacher),
    path('forgotpassword', changepassword),
    path('sendcode', verify),
    path('change_pass', changepass_conf),
    path('students', show_all_student),
    path('improve', student_improve),
    path('readd', student_readd),
    path('improvefinally', saveimprove),
    path('readdfinally', savereadd),
    path('check_notifications', is_any_notifications)
]
