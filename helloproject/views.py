import datetime
import os
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages

from .models.beforefinalbatch13 import before_final_table
import pandas as pd
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from helloproject.middlewares.auth import is_allowed, is_allowed_student
from .models.courses import courses
from .models.enroll import enroll
from .models.teaches import teaches
from .models.teacher import teacher
from .models.student import student
def restall():
    courses.objects.all().delete()
    enroll.objects.all().delete()
    teaches.objects.all().delete()
    student.objects.all().delete()
    teacher.objects.all().delete()
def index(request):
    return render(request, 'index.html')


def signin_T(request):
    if request.method == 'GET':
        return render(request, 'teacherlogin.html')
    sir = teacher.objects.filter(email=request.POST.get('email'))
    if len(sir) == 0:
        messages.error(request, "The email address that you've entered doesn't match any account.")
        return HttpResponseRedirect('/teacherlogin.html')
    if check_password(request.POST.get('password'), sir.get().password) == True:
        request.session['email'] = sir.get().email
        return HttpResponseRedirect('/select_result_as_teacher.html')
    else:
        messages.error(request, "The password you entered is incorrect. Did you forget your password?")
        return HttpResponseRedirect('/teacherlogin.html')


def signin_S(request):
    if request.method == 'GET':
        return render(request, 'student_login.html')
    stud = student.objects.filter(sid=request.POST.get('sid'))
    if len(stud) == 0:
        messages.error(request, "The ID that you've entered doesn't match any account.")
        return HttpResponseRedirect('student_login.html')
    if check_password(request.POST.get('password'), stud.get().password) == True:
        request.session['sid'] = stud.get().sid
        return HttpResponseRedirect('select_result_as_student.html')
    else:
        messages.error(request, "The password you entered is incorrect. Did you forget your password?")
        return HttpResponseRedirect('student_login.html')


def signup(request):
    print(request.POST)
    if request.method == 'GET':
        return render(request, 'register_users.html')
    if request.POST.get('password1') != request.POST.get('password2'):
        messages.error(request, 'Password doesn\'t matches.')
        return HttpResponseRedirect('register_user.html')
    if request.POST.get('inlineRadioOptions') == 'Teacher':
        if teacher.objects.filter(email=request.POST.get('email')).exists():
            messages.error(request, "This email address is already being used.")
            return HttpResponseRedirect('register_user.html')
        newteacher = teacher(
            full_name=request.POST.get('name'),
            email=request.POST.get('email'),
            password=make_password(request.POST.get('password1'))
        )
        newteacher.save()
    elif request.POST.get('inlineRadioOptions') == 'Student':
        if student.objects.filter(sid=request.POST.get('id')).exists():
            messages.error(request, "This ID is already being used.")
            return HttpResponseRedirect('register_user.html')
        ss = request.POST.get('id')
        num = int(ss[1:3])
        s1 = 2000 + num
        s1 -= 1
        newstudent = student(
            full_name=request.POST.get('name'),
            sid=request.POST.get('id'),
            password=make_password(request.POST.get('password1')),
            s_session=str(str(s1) + '-' + str(s1 + 1))
        )
        newstudent.save()
    messages.success(request, 'Registration Successful')
    return HttpResponseRedirect('register_user.html')

@is_allowed
def select_result_as_teacher(request):
    if request.method == 'GET':
        eml = request.session.get('email')
        course = []
        session = []
        semester = []
        for i in teaches.objects.filter(T_email=eml).values():
            courseid = i['course_id']
            breakpoint = courseid.find(')') + 1
            course.append(courseid[0:breakpoint])
            session.append(courseid[breakpoint:breakpoint + 9])
            semester.append(courseid[breakpoint + 9:])
        course=list(set(course))
        session=list(set(session))
        semester=list(set(semester))
        all = {
            'course': course,
            'session': session,
            'semester': semester
        }
        return render(request, 'select_result_as_teacher.html', {'all': all})
    else:
        courseid = request.POST.get('SCourse') + request.POST.get('Ssession') + request.POST.get('sSemester')
        if teaches.objects.filter(course_id=courseid).exists() == 0:
            messages.warning(request, 'No Such Course Exits !!!')
            return HttpResponseRedirect('select_result_as_teacher.html')
        elif request.POST.get('SResult_type') == 'Before Final':
            request.session['courseid']=courseid
            return HttpResponseRedirect('teacher_beforeFinal.html')


@is_allowed_student
def select_result_as_student(request):
    if request.method == 'GET':
        return render(request, 'select_result_as_student.html')
    else:
        return HttpResponseRedirect('/teacher_beforeFinal.html')


@is_allowed
def before_final(request):
    if request.method == 'POST':
        print(list(request.POST.items()))
    table_data = before_final_table.objects.all().order_by('Student_id')
    contents = {}
    contents[0] = table_data[len(table_data) - 1]
    for i in range(0, len(table_data) - 1):
        contents[i + 1] = table_data[i]
    return render(request, 'teacher_beforeFinal.html', {'cons': contents})


@is_allowed
def saving(request):
    Ecoursid=request.session.get('courseid')+'**'+request.session.get('email')
    print(Ecoursid)
    tabtmp1=request.POST
    tabtmp2=before_final_table.objects.filter(CourseidandTeacherid=Ecoursid)
    for i in range(0,len(tabtmp2)):
        tabtmp2[i].Student_id=tabtmp1[str(i)+'A']
        tabtmp2[i].A=tabtmp1[str(i)+'B']
        tabtmp2[i].B=tabtmp1[str(i)+'C']
        tabtmp2[i].C=tabtmp1[str(i)+'D']
        tabtmp2[i].D=tabtmp1[str(i)+'E']
        tabtmp2[i].E=tabtmp1[str(i)+'F']
        tabtmp2[i].F=tabtmp1[str(i)+'G']
        tabtmp2[i].G=tabtmp1[str(i)+'H']
        tabtmp2[i].H=tabtmp1[str(i)+'I']
        tabtmp2[i].I=tabtmp1[str(i)+'J']
        tabtmp2[i].save()
    return JsonResponse({'message': 'hendeled'})

def course_enroll(request):
    if request.method == 'GET':
        session = []
        course = []
        teachers = []
        yearno = ['1st', '2nd', '3rd', '4th']
        semno=['1st','2nd']
        sem=[]
        for i in yearno:
            for j in semno:
                sem.append(i+' Year '+j+' Semester ')
        for i in range(2017, datetime.datetime.now().year):
            session.append(str(i) + '-' + str(i + 1))
        for i in courses.objects.all().values():
            course.append(i['course_name'] + ' (' + i['course_id'] + ')')
        for i in teacher.objects.all().values():
            teachers.append(i['full_name'])
        all = {
            'course': course,
            'session': session,
            'teacher': teachers,
            'semester': sem
        }
        return render(request, 'enroll_course.html', {'all': all})
    courseid = request.POST.get('SCourse') + request.POST.get('Ssession') + request.POST.get('sSemester')
    rolls = request.POST.get('query')
    if len(rolls) != 14:
        messages.error(request, 'Invalid Query format!!!')
    elif rolls[0] != '=' or rolls[7] != '(' or rolls[10] != '-' or rolls[13] != ')':
        messages.error(request, 'Invalid Query format!!!')
    else:
        start = int(rolls[1:7] + rolls[8:10])
        end = int(rolls[1:7] + rolls[11:13])
        cnt = False
        eml = teacher.objects.filter(full_name=request.POST.get('STeacher'))[0].email
        Ecoursid=courseid+'**'+eml
        if not before_final_table.objects.filter(CourseidandTeacherid=Ecoursid).exists():
            newbeforefinal = before_final_table(
                CourseidandTeacherid=Ecoursid,
                Student_id='Exam Roll',
                A=None,
                B=None,
                C=None,
                D=None,
                E=None,
                F=None,
                G=None,
                H=None,
                I=None
            )
            newbeforefinal.save()
        for i in student.objects.values():
            if int(i['sid']) >= start and int(i['sid']) <= end:
                cnt = True
                newbeforefinal = before_final_table(
                    CourseidandTeacherid=Ecoursid,
                    Student_id=i['sid'],
                    A='',
                    B='',
                    C='',
                    D='',
                    E='',
                    F='',
                    G='',
                    H='',
                    I=''
                )
                newbeforefinal.save()
                newenroll = enroll(
                    course_id=courseid,
                    sid=i['sid']
                )
                newenroll.save()
        if cnt == True:
            newteach = teaches(
                course_id=courseid,
                T_email=eml
            )
            newteach.save()
            messages.success(request, 'Query successful !!!')
    return HttpResponseRedirect('enroll_course.html')


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

def func(request):
    vc = []
    for i in range(0, 9):
        vc.append(i)
    return JsonResponse({'fff': vc})

@is_allowed
def excelup(request):
    if request.method == 'POST':
        file = request.FILES["file"]
        csv = pd.read_excel(file, dtype=str)
        r_len = csv.count()[0]
        li = []
        ls = csv.columns.tolist()
        li.append(ls)
        for i in csv.values:
            li.append(i.tolist())
        for i in li:
            print(len(i))
            while len(i) < 10:
                i.append('')
        for i in range(0, r_len):
            st = before_final_table(
                Student_id=li[i][0],
                A=li[i][1],
                B=li[i][2],
                C=li[i][3],
                D=li[i][4],
                E=li[i][5],
                F=li[i][6],
                G=li[i][7],
                H=li[i][8],
                I=li[i][9]
            )
            st.save()
    return render(request, 'excel.html')
