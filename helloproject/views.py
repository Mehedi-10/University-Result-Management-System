import datetime
import os
import uuid

totalinternalteachers = 17
yearno = ['1st', '2nd', '3rd', '4th']
semno = ['1st', '2nd']
inMark = ['0', '10', '20', '40']

from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q

import pandas as pd
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from helloproject.middlewares.auth import *

from .models.Courses import courses
from .models.Before_Final import before_final
from .models.Assigned_Courses import assigned_course
from .models.Teacher import teacher
from .models.Student import student
from .models.Published import published
from .models.Final import final
from .models.Officially_Published import officially_published
from .models.Chats import chats
from .models.Improve import improve
from .models.Exam_Committee import exam_committe


# def resetall():
#     courses.objects.all().delete()
#     enroll.objects.all().delete()
#     teaches.objects.all().delete()
#     student.objects.all().delete()
#     teacher.objects.all().delete()

def index(request):
    return render(request, 'index.html')


def signin_teacher(request):
    if request.method == 'GET':
        return render(request, 'teacherlogin.html')
    try:
        sir = teacher.objects.get(t_email=request.POST.get('email'))
    except teacher.DoesNotExist:
        messages.error(request, "The email address that you've entered doesn't match any account.")
        return HttpResponseRedirect('teacherlogin.html')
    if check_password(request.POST.get('password'), sir.password) == True:
        request.session['email'] = sir.t_email
        return HttpResponseRedirect('select_result_as_teacher.html')
    else:
        messages.error(request, "The password you entered is incorrect. Did you forget your password?")
        return HttpResponseRedirect('teacherlogin.html')


def signin_student(request):
    if request.method == 'GET':
        return render(request, 'student_login.html')
    try:
        stud = student.objects.get(s_id=request.POST.get('sid'))
    except student.DoesNotExist:
        messages.error(request, "The ID that you've entered doesn't match any account.")
        return HttpResponseRedirect('student_login.html')
    if check_password(request.POST.get('password'), stud.password) == True:
        request.session['email'] = stud.s_id
        return HttpResponseRedirect('select_result_as_student.html')
    else:
        messages.error(request, "The password you entered is incorrect. Did you forget your password?")
        return HttpResponseRedirect('student_login.html')


def teacher_signup(request):
    if request.method == 'GET':
        return render(request, 'register_teacher.html')
    if request.POST.get('password1') != request.POST.get('password2'):
        messages.error(request, 'Passwords do not match.')
        return HttpResponseRedirect('register_teacher.html')
    try:
        teacher.objects.get(t_email=request.POST.get('email'))
        messages.error(request, "This email address is already being used.")
        return HttpResponseRedirect('register_teacher.html')
    except teacher.DoesNotExist:
        newteacher = teacher(
            t_name=request.POST.get('name'),
            t_email=request.POST.get('email'),
            password=make_password(request.POST.get('password1')),
        )
        newteacher.save()
    messages.success(request, 'Registration Successful')
    return HttpResponseRedirect('register_teacher')


def student_signup(request):
    if request.method == 'GET':
        return render(request, 'register_student.html')
    if request.POST.get('password1') != request.POST.get('password2'):
        messages.error(request, 'Passwords do not match.')
        return HttpResponseRedirect('register_teacher')
    if len(request.POST.get('id')) != 8:
        messages.error(request, "Invalid ID.")
        return HttpResponseRedirect('register_teacher')
    try:
        student.objects.get(s_id=request.POST.get('id'))
        messages.error(request, "This ID is already being used.")
        return HttpResponseRedirect('register_teacher')
    except student.DoesNotExist:
        ss = request.POST.get('id')
        num = int(ss[1:3])
        s1 = 2000 + num
        s1 -= 1
        newstudent = student(
            s_name=request.POST.get('name'),
            s_id=request.POST.get('id'),
            password=make_password(request.POST.get('password1')),
            s_session=str(str(s1) + '-' + str(s1 + 1))
        )
        newstudent.save()
    messages.success(request, 'Registration Successful')
    return HttpResponseRedirect('register_teacher')


##  update marks with credits ##
@is_allowed
def select_result_as_teacher(request):
    if request.method == 'GET':
        eml = request.session.get('email')
        session = []
        for i in assigned_course.objects.filter(t_mail=eml).values():
            session.append(i['s_session'])
        session = list(set(session))
        all = {
            'session': session,
        }
        return render(request, 'select_result_as_teacher.html', {'all': all})
    else:
        if request.POST.get('SResult_type') == 'Before Semester Final':
            mark = 0
            cc = request.POST.get('SCourse')
            start = cc.find('(')
            cc = cc[start + 1:cc.find(')')]
            mark = 20
            dic = {
                'course': request.POST.get('SCourse')[0:start],
                'session': request.POST.get('Ssession'),
                'semester': request.POST.get('sSemester'),
                'course_code': cc,
                'marks': mark
            }
            request.session['all_info'] = dic
            return HttpResponseRedirect('teacher_beforeFinal.html')
        else:
            mark = 60
            cc = request.POST.get('SCourse')
            start = cc.find('(')
            cc = cc[start + 1:cc.find(')')]
            mark = 30
            dic = {
                'course': request.POST.get('SCourse')[0:start],
                'session': request.POST.get('Ssession'),
                'semester': request.POST.get('sSemester'),
                'course_code': cc,
                'marks': mark
            }
            request.session['all_info'] = dic
            return HttpResponseRedirect('teacher_Final.html')


@is_allowed
def teacher_select_with_ajax(request):
    course = []
    semester = []
    before = []
    if int(request.POST.get('step')) == 1:
        for i in assigned_course.objects.filter(t_mail=request.session.get('email')).filter(
                s_session=request.POST.get('subject_1')).values():
            coursevar = courses.objects.get(c_id=i['c_id_id'])
            cutpoint = coursevar.c_id.find('-') + 1
            semester.append(yearno[int(coursevar.c_id[cutpoint]) - 1] + ' year ' + semno[
                int(coursevar.c_id[cutpoint + 1]) - 1] + ' semester')
        semester = list(set(semester))
        return JsonResponse(semester, safe=False)
    if int(request.POST.get('step')) == 2:
        for i in assigned_course.objects.filter(t_mail=request.session.get('email')).filter(
                s_session=request.POST.get('subject_1')).values():
            coursevar = courses.objects.get(c_id=i['c_id_id'])
            cutpoint = coursevar.c_id.find('-') + 1
            if (yearno[int(coursevar.c_id[cutpoint]) - 1] + ' year ' + semno[
                int(coursevar.c_id[cutpoint + 1]) - 1] + ' semester') == request.POST.get('subject_2'):
                course.append(coursevar.c_name + ' (' + coursevar.c_id + ')')
        course = list(set(course))
        return JsonResponse(course, safe=False)
    if int(request.POST.get('step')) == 3:
        if assigned_course.objects.filter(t_mail=request.session.get('email')).filter(
                s_session=request.POST.get('subject_1')).filter(
            c_id__c_id=request.POST.get('subject_3')).last().guest == 'internal':
            request.session['status'] = True
            before.append('Before Semester Final')
            before.append('Semestar Final')
        else:
            request.session['status'] = False
            before.append('Semestar Final')
        return JsonResponse(before, safe=False)


@is_allowed
def sselect(request):
    course = []
    semester = []
    before = []
    if int(request.POST.get('step')) == 1:
        for i in assigned_course.objects.filter(t_mail=request.session.get('email')).filter(
                s_session=request.POST.get('subject_1')).values():
            coursevar = courses.objects.get(c_id=i['c_id_id'])
            cutpoint = coursevar.c_id.find('-') + 1
            semester.append(yearno[int(coursevar.c_id[cutpoint]) - 1] + ' year ' + semno[
                int(coursevar.c_id[cutpoint + 1]) - 1] + ' semester')
        semester = list(set(semester))
        return JsonResponse(semester, safe=False)
    if int(request.POST.get('step')) == 2:
        for i in assigned_course.objects.filter(t_mail=request.session.get('email')).filter(
                s_session=request.POST.get('subject_1')).values():
            coursevar = courses.objects.get(c_id=i['c_id_id'])
            cutpoint = coursevar.c_id.find('-') + 1
            if (yearno[int(coursevar.c_id[cutpoint]) - 1] + ' year ' + semno[
                int(coursevar.c_id[cutpoint + 1]) - 1] + ' semester') == request.POST.get('subject_2'):
                course.append(coursevar.c_name + ' (' + coursevar.c_id + ')')
        course = list(set(course))
        return JsonResponse(course, safe=False)
    if int(request.POST.get('step')) == 3:
        if assigned_course.objects.filter(t_mail=request.session.get('email')).filter(
                s_session=request.POST.get('subject_1')).filter(
            c_id__c_id=request.POST.get('subject_3')).last().guest == 'internal':
            before.append('Before Semester Final')
            before.append('Semestar Final')
        else:
            before.append('Semestar Final')
        return JsonResponse(before, safe=False)


@is_allowed
def process_before_final(request):
    try:
        course_code = request.session['all_info']['course_code']
        session_ = request.session['all_info']['session']
        status_ = request.session.get('status')
    except KeyError:
        return HttpResponseRedirect('select_result_as_teacher.html')
    else:
        if course_code == None or session_ == None or status_ == None or status_:
            return HttpResponseRedirect('select_result_as_teacher.html')
    sv = published.objects.filter(c_id=course_code).filter(s_session=session_).filter(
        t_email=request.session.get('email')).last()
    if request.method == 'POST':
        sv.published_before_final = True
        sv.save()
    table_data = before_final.objects.filter(c_id=course_code).filter(s_session=session_).order_by('s_id')
    if not table_data.exists():
        return HttpResponseRedirect('select_result_as_teacher.html')
    contents = {}
    contents[0] = table_data[len(table_data) - 1]
    for i in range(0, len(table_data) - 1):
        contents[i + 1] = table_data[i]
    all = {
        'constt': contents,
        'head': request.session['all_info'],
        'submitted': sv.published_before_final,
    }
    return render(request, 'teacher_beforeFinal.html', {'cons': all})


@is_allowed
def process_final_internal(request):
    try:
        course_code = request.session['all_info']['course_code']
        session_ = request.session['all_info']['session']
    except KeyError:
        return HttpResponseRedirect('select_result_as_teacher.html')
    sv = published.objects.filter(c_id=course_code).filter(s_session=session_).filter(
        t_email=request.session.get('email')).last()
    if request.method == 'POST':
        if request.method == 'POST':
            sv.published_final = True
            sv.save()
    table_data = final.objects.filter(c_id=course_code).filter(s_session=session_).order_by('s_id')
    if not table_data.exists():
        return HttpResponseRedirect('select_result_as_teacher.html')
    contents = {}
    contents[0] = table_data[len(table_data) - 1]
    for i in range(0, len(table_data) - 1):
        contents[i + 1] = table_data[i]
    print(contents)
    all = {
        'constt': contents,
        'head': request.session['all_info'],
        'submitted': sv.published_final,
        'status_': request.session['status']
    }
    return render(request, 'teacher_Final.html', {'cons': all})


@is_allowed
@csrf_protect
def saving(request):
    try:
        course_code = request.session['all_info']['course_code']
        session_ = request.session['all_info']['session']
    except KeyError:
        return HttpResponseRedirect('select_result_as_teacher.html')
    tabtmp1 = request.POST
    tabtmp1 = tabtmp1.dict()
    tmp = tabtmp1
    tabtmp1.popitem()
    tabtmp1 = list(tabtmp1.values())
    tabtmp2 = before_final.objects.filter(c_id=course_code).filter(s_session=session_).filter(s_id=tabtmp1[0])
    updt = before_final.objects.get(id=tabtmp2[0].id)
    updt.s_id = tabtmp1[0]
    updt.mid1 = tabtmp1[1]
    updt.mid2 = tabtmp1[2]
    updt.mid3 = tabtmp1[3]
    updt.class_test = tabtmp1[4]
    updt.presentation = tabtmp1[5]
    updt.attendance = tabtmp1[6]
    updt.assignment = tabtmp1[7]
    updt.exta_field = tabtmp1[8]
    updt.total = tabtmp1[9]
    for k, v in before_final.objects.filter(s_id='Exam Roll').filter(c_id=course_code).values()[0].items():
        if str(v).find('Total') != -1:
            updt.total_ump = updt.__getattribute__(k)
            break
    updt.save()
    return JsonResponse({'message': 'hendeled'})


@is_allowed
@csrf_protect
def savingfinal(request):
    try:
        course_code = request.session['all_info']['course_code']
        session_ = request.session['all_info']['session']
        status_ = request.session.get('status')
    except KeyError:
        return HttpResponseRedirect('select_result_as_teacher.html')

    tabtmp1 = request.POST
    tabtmp1 = tabtmp1.dict()
    tabtmp1.popitem()
    tabtmp1 = list(tabtmp1.values())
    tabtmp2 = final.objects.filter(c_id=course_code).filter(s_session=session_).filter(s_id=tabtmp1[0])
    updt = final.objects.get(id=tabtmp2[0].id)
    if request.session.get('status'):
        updt.total1 = tabtmp1[1]
    else:
        updt.total2 = tabtmp1[1]
    updt.save()
    return JsonResponse({'message': 'hendeled'})


@is_allowed_student
def select_result_as_student(request):
    if request.method == 'GET':
        try:
            eml = request.session.get('email')
        except KeyError:
            return HttpResponseRedirect('student_login.html')
        course = []
        session = []
        semester = []
        for i in before_final.objects.filter(s_id=eml).values():
            coursevar = courses.objects.get(c_id=i['c_id_id'])
            course.append(coursevar.c_name + ' (' + coursevar.c_id + ')')
            session.append(i['s_session'])
            cutpoint = coursevar.c_id.find('-') + 1
            semester.append(yearno[int(coursevar.c_id[cutpoint]) - 1] + ' year ' + semno[
                int(coursevar.c_id[cutpoint + 1]) - 1] + ' semester')
        course = list(set(course))
        session = list(set(session))
        semester = list(set(semester))
        all = {
            'course': course,
            'session': session,
            'semester': semester
        }
        return render(request, 'select_result_as_student.html', {'all': all})
    else:
        if request.POST.get('SResult_type') == 'Final':
            session_ = request.POST.get('Ssession')
            semester_ = request.POST.get('sSemester')[0] + '-' + request.POST.get('sSemester')[9]
            if not officially_published.objects.filter(s_session=session_).filter(s_semester=semester_).exists():
                messages.warning(request, 'Invalid Selection')
                return HttpResponseRedirect('select_result_as_student.html')
            if not officially_published.objects.filter(s_session=session_).filter(
                    s_semester=semester_).last().is_published:
                messages.info(request, mark_safe('Keep Clam <br/> and hope that <br/> exam result will be good'))
                return HttpResponseRedirect('select_result_as_student.html')
            lookstr = '-' + semester_[0] + semester_[2]
            ob1 = final.objects.filter(s_id=request.session.get('email')).filter(c_id__c_id__contains=lookstr)
            li = {}
            for i in range(0, len(ob1)):
                dic = {}
                dic['course_code'] = ob1[i].c_id.c_id
                dic['course_name'] = ob1[i].c_id.c_name
                dic['crourse_credit'] = ob1[i].c_id.credit
                dic['latter_grade'] = ob1[i].lattergrade
                dic['before_final'] = before_final.objects.filter(s_id=request.session.get('email'), ).filter(
                    c_id=ob1[i].c_id.c_id).last().total_ump
                li[i] = dic
            per = {
                'id': request.session.get('email'),
                'name': student.objects.get(s_id=request.session.get('email')).s_name,
                'semester': request.POST.get('sSemester'),
                'course': request.POST.get('SCourse'),
                'session': request.POST.get('Ssession')
            }
            request.session['all'] = {'per': per, 'dic': li}
            return HttpResponseRedirect('show_final.html')
        else:
            coursev = request.POST.get('SCourse')
            courseid = coursev[coursev.find('(') + 1:coursev.find(')')]
            session_ = request.POST.get('Ssession')
            # + request.POST.get('sSemester') selected semester
            if not published.objects.filter(c_id=courseid).filter(s_session=session_).exists():
                messages.warning(request, 'Invalid Selection')
                return HttpResponseRedirect('select_result_as_student.html')
            if not published.objects.filter(c_id=courseid).filter(s_session=session_).last().published_before_final:
                messages.info(request, mark_safe('Keep Clam <br/> and hope that <br/> exam result will be good'))
                return HttpResponseRedirect('select_result_as_student.html')
            before_fin = before_final.objects.filter(c_id=courseid).filter(s_session=session_).order_by('s_id')
            ob1 = before_fin.last()
            ob2 = before_fin.filter(s_id=request.session.get('email')).last()
            dic = {}
            print(ob1.c_id)
            dic[ob1.mid1] = ob2.mid1
            dic[ob1.mid2] = ob2.mid2
            dic[ob1.mid3] = ob2.mid3
            dic[ob1.class_test] = ob2.class_test
            dic[ob1.presentation] = ob2.presentation
            dic[ob1.attendance] = ob2.attendance
            dic[ob1.assignment] = ob2.assignment
            dic[ob1.extra_field] = ob2.extra_field
            dic[ob1.total] = ob2.total
            try:
                dic.__delitem__('None')
            except KeyError:
                pass
            try:
                dic.__delitem__('')
            except KeyError:
                pass
            per = {
                'id': request.session.get('email'),
                'name': student.objects.get(s_id=request.session.get('email')).s_name,
                'semester': request.POST.get('sSemester'),
                'course': request.POST.get('SCourse'),
                'session': request.POST.get('Ssession')
            }
            request.session['all'] = {'per': per, 'dic': dic}
            return HttpResponseRedirect('show_before_final.html')


@is_allowed_student
def show_before_final(request):
    try:
        dic = request.session['all']
        return render(request, 'show_before_final.html', {'all': dic})
    except KeyError:
        return HttpResponseRedirect('select_result_as_student.html')


@is_allowed_student
def showfinal(request):
    try:
        dic = request.session['all']
        return render(request, 'show_final.html', {'all': dic})
    except KeyError:
        return HttpResponseRedirect('select_result_as_student.html')


# def course_enroll(request):
#     if request.method == 'GET':
#         session = []
#         course = []
#         teachers = []
#         sem=[]
#         for i in yearno:
#             for j in semno:
#                 sem.append(i+' Year '+j+' Semester ')
#         for i in range(2017, datetime.datetime.now().year):
#             session.append(str(i) + '-' + str(i + 1))
#         for i in courses.objects.all().values():
#             course.append(i['course_name'] + ' (' + i['course_id'] + ')')
#         for i in teacher.objects.all().values():
#             teachers.append(i['full_name'])
#         all = {
#             'course': course,
#             'session': session,
#             'teacher': teachers,
#             'semester': sem
#         }
#         return render(request, 'assign_course.html', {'all': all})
#     courseid = request.POST.get('SCourse') + request.POST.get('Ssession') + request.POST.get('sSemester')
#     rolls = request.POST.get('query')
#     if len(rolls) != 14:
#         messages.error(request, 'Invalid Query format!!!')
#     elif rolls[0] != '=' or rolls[7] != '(' or rolls[10] != '-' or rolls[13] != ')':
#         messages.error(request, 'Invalid Query format!!!')
#     else:
#         start = int(rolls[1:7] + rolls[8:10])
#         end = int(rolls[1:7] + rolls[11:13])
#         cnt = False
#         eml = teacher.objects.filter(full_name=request.POST.get('STeacher'))[0].email
#         crs=request.POST.get('SCourse')
#         crid=crs[crs.find('(')+1:len(crs)-1]
#         crs=crs[0:crs.find('(')-1]
#         credit=courses.objects.filter(course_id=crid).filter(course_name=crs).last().credit
#         # update credit and marks
#         marks=40
#         marks1=60
#         if credit==2:
#             marks=20
#             marks1=30
#         Ecoursid=courseid+'**'+eml
#         if not before_final_table.objects.filter(CourseidandTeacherid=Ecoursid).exists():
#             newbeforefinal = before_final_table(
#                 CourseidandTeacherid=Ecoursid,
#                 Student_id='Exam Roll',
#                 A='Total'+'('+str(marks)+')',
#                 B=None,
#                 C=None,
#                 D=None,
#                 E=None,
#                 F=None,
#                 G=None,
#                 H=None,
#                 I=None
#             )
#             newbeforefinal.save()
#             newfinal=final_table(
#                 CourseidandTeacherid=Ecoursid,
#                 Student_id ='Exam Roll',
#                 Marks ='Marks''('+str(marks1)+')',
#                 Grade ='Letter Grade',
#                 GPA = 'GPA'
#             )
#             newfinal.save()
#         for i in student.objects.values():
#             if int(i['sid']) >= start and int(i['sid']) <= end:
#                 if before_final_table.objects.filter(CourseidandTeacherid=Ecoursid).filter(Student_id=i['sid']).exists():
#                     continue
#                 cnt = True
#                 newbeforefinal = before_final_table(
#                     CourseidandTeacherid=Ecoursid,
#                     Student_id=i['sid'],
#                     A='0.0',
#                     B='',
#                     C='',
#                     D='',
#                     E='',
#                     F='',
#                     G='',
#                     H='',
#                     I=''
#                 )
#                 newbeforefinal.save()
#                 newfinal = final_table(
#                     CourseidandTeacherid=Ecoursid,
#                     Student_id=i['sid'],
#                     Marks='',
#                     Grade='',
#                     GPA=''
#                 )
#                 newfinal.save()
#                 newenroll = enroll(
#                     course_id=courseid,
#                     sid=i['sid']
#                 )
#                 newenroll.save()
#         if cnt == True:
#             newteach = teaches(
#                 course_id=courseid,
#                 T_email=eml
#             )
#             newteach.save()
#         messages.success(request, 'Query successful !!!')
#     return HttpResponseRedirect('assign_course.html')

def add_course(request):
    if request.method == 'GET':
        return render(request, 'add_new_course.html')
    newcourse = courses(
        course_name=request.POST.get('fcoursename'),
        course_id=request.POST.get('fcourseid'),
        syllabus_year=request.POST.get('fsyllabus_year'),
        credit=request.POST.get('fcoursecredit')
    )
    newcourse.save()
    return HttpResponseRedirect('add_new_course.html')


def assign_course(request):
    if request.method == 'POST':
        session_ = request.POST.get('s_ession')
        tmp_ = request.POST.get('c_ourse')
        tmp2_ = request.POST.get('t_eacher')
        type_ = request.POST.get('t_ype')
        courseid_ = tmp_[tmp_.find('(') + 1:tmp_.find(')')]
        tmail_ = tmp2_[tmp2_.find('<') + 1:tmp2_.find('>')]
        mark = 40
        if courses.objects.get(c_id=courseid_).credit == 2.0:
            mark = 20
        if not assigned_course.objects.filter(c_id__c_id=courseid_).filter(s_session=session_).filter(
                t_mail__t_email=tmail_).exists():
            nw = assigned_course(
                c_id_id=courseid_,
                t_mail_id=tmail_,
                s_session=session_,
                guest=type_
            )
            nw.save()
            if not published.objects.filter(c_id__c_id=courseid_).filter(s_session=session_).filter(
                    t_mail__t_email=tmail_).exists():
                nw = published(
                    c_id_id=courseid_,
                    t_mail_id=tmail_,
                    s_session=session_,
                )
            nw.save()

            messages.success(request, 'Assigned Successfully')
            if type_ == 'Internal':
                for i in student.objects.filter(s_session=session_):
                    nw = before_final(
                        c_id_id=courseid_,
                        s_session=session_,
                        s_id=i.s_id
                    )
                    nw.save()
                nw = before_final(
                    c_id_id=courseid_,
                    s_session=session_,
                    s_id='Exam Roll',
                    mid1='Total' + '(' + str(mark) + ')'
                )
                nw.save()
                mark = 60
                if courses.objects.get(c_id=courseid_).credit == 2.0:
                    mark = 30
                for i in student.objects.filter(s_session=session_):
                    nw = final(
                        c_id_id=courseid_,
                        s_session=session_,
                        s_id=i.s_id
                    )
                    nw.save()
                nw = final(
                    c_id_id=courseid_,
                    s_session=session_,
                    s_id='Exam Roll',
                    total1='Total' + '(' + str(mark) + ')'
                )
                nw.save()
        else:
            messages.info(request, 'Already Assigned.')
        return HttpResponseRedirect('assign_course')
    course = []
    teach = []
    session = []
    for i in courses.objects.all():
        course.append(i.c_name + ' (' + i.c_id + ')')
    for i in teacher.objects.all():
        teach.append(i.t_name + ' <' + i.t_email + '>')
    for i in student.objects.all():
        session.append(i.s_session)
    all = {
        'courses_': course,
        'teacher_': teach,
        'session_': session
    }
    return render(request, 'assign_course.html', {'all': all})


def func(request):
    vc = []
    for i in range(0, 9):
        vc.append(i)
    return JsonResponse({'fff': vc})


# @is_allowed
# def excelup(request):
#     if request.method == 'POST':
#         file = request.FILES["file"]
#         csv = pd.read_excel(file, dtype=str)
#         r_len = csv.count()[0]
#         li = []
#         ls = csv.columns.tolist()
#         li.append(ls)
#         for i in csv.values:
#             li.append(i.tolist())
#         for i in li:
#             print(len(i))
#             while len(i) < 10:
#                 i.append('')
#         for i in range(0, r_len):
#             st = before_final_table(
#                 Student_id=li[i][0],
#                 A=li[i][1],
#                 B=li[i][2],
#                 C=li[i][3],
#                 D=li[i][4],
#                 E=li[i][5],
#                 F=li[i][6],
#                 G=li[i][7],
#                 H=li[i][8],
#                 I=li[i][9]
#             )
#             st.save()
#     return render(request, 'excel.html')
# def send_mg(request):
#     pass

def admin_home(request):
    student_data = [['Session', 'No of Students']]
    cnt = {}
    for i in student.objects.order_by('s_session'):
        try:
            ob = officially_published.objects.filter(s_session=i.s_session).filter(s_semester='4-4').last()
        except officially_published.DoesNotExist:
            pass
        else:
            if ob != None and ob.is_published:
                continue
        if i.s_session not in cnt.keys():
            cnt.__setitem__(i.s_session, 0)
        cnt[i.s_session] += 1
    for i, j in cnt.items():
        student_data.append([i, j])

    teacher_data = [['Current Status', 'count']]
    not_on_leave = 0
    for i in teacher.objects.all():
        fnd = 0
        for j in assigned_course.objects.filter(t_mail=i.t_email):
            try:
                pb = published.objects.filter(c_id__c_id=j.c_id.c_id).filter(s_session=j.s_session).last()
                if not pb.published_final:
                    if j.guest == 'internal':
                        fnd = 1
                        break
            except AttributeError:
                pass
        if fnd:
            not_on_leave += 1
    teacher_data.append(['Not on study leave', not_on_leave])
    teacher_data.append(['On study leave', totalinternalteachers - not_on_leave])
    all = {
        'student_stat1': student_data,
        'teacher_stat1': teacher_data,
    }
    print(teacher_data)
    return render(request, 'homepage.html', {'all': all})


#
# @is_allowed_student
def exam_com(request):
    dic = {}
    ec = exam_committe.objects.filter(ec_status=True).last()
    ec_ = {
        'Memeber 1': 'None',
        'Memeber 2': 'None',
        'Memeber 3': 'None'
    }

    if ec != None:
        ec_ = {
            'Memeber 1': ec.t_mail1.t_name,
            'Memeber 2': ec.t_mail2.t_name,
            'Memeber 3': ec.t_mail3.t_name
        }
    teach = []
    for i in teacher.objects.all():
        teach.append(i.t_name + ' <' + i.t_email + '>')
    dic = {
        'ec_': ec_,
        'teachers_': teach,
    }

    return render(request, 'exam_committee.html', {'all': dic})


def showallteacher(request):
    dic = []
    for i in teacher.objects.all():
        a1 = []
        a2 = []
        a3 = []
        a1.append(i.t_name)
        for j in assigned_course.objects.filter(t_mail=i.t_email):
            try:
                pb = published.objects.filter(c_id__c_id=j.c_id.c_id).filter(s_session=j.s_session).last()
                if not pb.published_final:
                    if j.guest == 'internal':
                        a2.append(j.c_id.c_name)
                    else:
                        a3.append(j.c_id.c_name)
            except AttributeError:
                pass
        tmp = {
            'name': a1,
            'internal': a2,
            'external': a3
        }
        dic.append(tmp)
    return render(request, 'teacherslist.html', {'all': dic})


def who_are_u(request):
    return render(request, 'who_are_you.html')


@is_allowed_to_change_pass
def changepass_conf(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.session['user_type'] == 2:
            ob = student.objects.filter(s_email=request.session['to_verify']).last()
            ob.password = make_password(password)
            ob.save()
            messages.success(request, 'your password has been successfully changed.')
            del request.session['to_verify']
            return HttpResponseRedirect('student_login.html')
        else:
            ob = teacher.objects.get(t_email=request.session['to_verify'])
            ob.password = make_password(password)
            ob.save()
            del request.session['to_verify']
            messages.success(request, 'your password has been successfully changed.')
            return HttpResponseRedirect('teacherlogin.html')
    return render(request, 'change_pass.html')


@is_allowed_to_change_pass
def verify(request):
    if request.method == 'POST':
        li = ['false']
        if request.session['user_type'] == 2:
            ob = student.objects.filter(s_email=request.session['to_verify']).last()
            if check_password(request.POST.get('code'), ob.code):
                li[0] = 'true'
        else:
            ob = teacher.objects.get(t_email=request.session['to_verify'])
            if check_password(request.POST.get('code'), ob.code):
                li[0] = 'true'
        return JsonResponse(li, safe=False)


def changepassword(request):
    if request.method == 'POST':
        li = []
        code = ''
        name = ''
        try:
            ob = teacher.objects.get(t_email=request.POST.get('email'))
        except teacher.DoesNotExist:
            if not student.objects.filter(s_email=request.POST.get('email')).exists():
                li.append('false')
                return JsonResponse(li, safe=False)
            else:
                ob = student.objects.filter(s_email=request.POST.get('email')).last()
                code = uuid.uuid4().hex[:8]
                ob.code = make_password(code)
                name = ob.s_name
                ob.save()
                request.session['user_type'] = 2
                li.append('true')
        else:
            ob = teacher.objects.get(t_email=request.POST.get('email'))
            code = uuid.uuid4().hex[:8]
            ob.code = make_password(code)
            name = ob.t_name
            ob.save()
            request.session['user_type'] = 1
            li.append('true')

        request.session['to_verify'] = request.POST.get('email')

        tamp = render_to_string('passreset.html', {'username': name, 'code': code})
        email = EmailMessage(
            'testing email',
            tamp,
            settings.EMAIL_HOST_USER,
            ['mehedihasanarafat10@gmail.com'],
        )
        email.fail_scilenty = True
        email.send()
        return JsonResponse(li, safe=False)
    return render(request, 'forgot_password.html')


def show_all_student(request):
    if request.method == 'POST':
        try:
            ob = student.objects.get(s_id=request.POST.get('id'))
        except student.DoesNotExist:
            messages.error(request, 'id not exits')
            return HttpResponseRedirect('students')
        else:
            ob.s_status = request.POST.get('status') == 'true'
            ob.save()
            return JsonResponse({'message': request.POST.get('status')})
    dic = {}
    for i in student.objects.all():
        if i.s_session not in dic.keys():
            dic.__setitem__(i.s_session, [])
        tmp = {
            'id': i.s_id,
            'name': i.s_name,
            'email': i.s_email,
            'status': i.s_status
        }
        dic[i.s_session].append(tmp)
    return render(request, 'studentlist.html', {'all': dic})


def student_improve(request):
    dic = []
    if request.POST.get('step') == '1':
        for i in final.objects.filter(s_id=request.POST.get('id')):
            for j in officially_published.objects.filter(s_session=i.s_session).filter(is_published=True):
                dic.append(yearno[int(j.s_semester[0]) - 1] + ' year ' + semno[int(j.s_semester[2])] + ' semester')
        return JsonResponse(dic, safe=False)
    else:
        ob = student.objects.get(s_id=request.POST.get('id'))
        for i in student.objects.order_by().values('s_session').distinct():
            for j in i.values():
                if j >= ob.s_session:
                    dic.append(j)
        subjects_ = []
        for i in final.objects.filter(s_id=request.POST.get('id')).filter(pointgrade__lt=3.0):
            subjects_.append(i.c_id.c_name + ' (' + i.c_id.c_id + ')')
        alldata = []
        alldata.append(dic)
        alldata.append(subjects_)
        return JsonResponse(alldata, safe=False)


def student_readd(request):
    dic = []
    if request.POST.get('step') == '1':
        sem = []
        for i in final.objects.filter(s_id=request.POST.get('id')):
            for j in officially_published.objects.filter(s_session=i.s_session).filter(is_published=True):
                sem.append(yearno[int(j.s_semester[0]) - 1] + ' year ' + semno[int(j.s_semester[2])] + ' semester')
        dic.append(sem)
        try:
            ob = student.objects.get(s_id=request.POST.get('id'))
        except student.DoesNotExist:
            pass
        else:
            dic.append(ob.s_session)
        return JsonResponse(dic, safe=False)
    else:
        ob = student.objects.get(s_id=request.POST.get('id'))
        got_sem = request.POST.get('subject_2')
        for i in student.objects.order_by().values('s_session').distinct():
            for j in i.values():
                ob1 = officially_published.objects.filter(s_session=j).filter(s_semester=got_sem).last()
                if j >= ob.s_session and ob1 != None and not ob1.is_published:
                    dic.append(j)
        return JsonResponse(dic, safe=False)


def saveimprove(request):
    print(request.POST)
    pass


def savereadd(request):
    print(request.POST)
    pass
