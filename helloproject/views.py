import datetime
import os
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.utils.safestring import mark_safe

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

def resetall():
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
        request.session['email'] = stud.get().sid
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
        return HttpResponseRedirect('register_users.html')
    if request.POST.get('inlineRadioOptions') == 'Teacher':
        if teacher.objects.filter(email=request.POST.get('email')).exists():
            messages.error(request, "This email address is already being used.")
            return HttpResponseRedirect('register_users.html')
        newteacher = teacher(
            full_name=request.POST.get('name'),
            email=request.POST.get('email'),
            password=make_password(request.POST.get('password1'))
        )
        newteacher.save()
    elif request.POST.get('inlineRadioOptions') == 'Student':
        if student.objects.filter(sid=request.POST.get('id')).exists():
            messages.error(request, "This ID is already being used.")
            return HttpResponseRedirect('register_users.html')
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
    return HttpResponseRedirect('register_users.html')

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
        if teaches.objects.filter(course_id=courseid).exists() == 0 or request.POST.get('SResult_type')=='Exam Type':
            messages.warning(request, 'No Such Course Exits !!!')
            return HttpResponseRedirect('select_result_as_teacher.html')
        elif request.POST.get('SResult_type') == 'Before Final':
            mark=40
            cc=request.POST.get('SCourse')
            start=cc.find('(')
            cc=cc[start+1:cc.find(')')]
            if courses.objects.filter(course_id=cc).values_list()[0][4]==2:
                mark=20
            dic={
                'courseid':courseid,
                'course':request.POST.get('SCourse')[0:start],
                'session':request.POST.get('Ssession'),
                'semester':request.POST.get('sSemester'),
                'course_code':cc,
                'marks':mark
            }
            request.session['all_info']=dic
            return HttpResponseRedirect('teacher_beforeFinal.html')



@is_allowed_student
def select_result_as_student(request):
    if request.method == 'GET':
        eml = request.session.get('email')
        course = []
        session = []
        semester = []
        for i in enroll.objects.filter(sid=eml).values():
            courseid = i['course_id']
            breakpoint = courseid.find(')') + 1
            course.append(courseid[0:breakpoint])
            session.append(courseid[breakpoint:breakpoint + 9])
            semester.append(courseid[breakpoint + 9:])
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
        courseid = request.POST.get('SCourse') + request.POST.get('Ssession') + request.POST.get('sSemester')
        if not teaches.objects.filter(course_id=courseid).exists():
            messages.warning(request,'Invalid Selection')
            return HttpResponseRedirect('select_result_as_student.html')
        tch=teaches.objects.filter(course_id=courseid).values('T_email')
        t_email=tch.last()['T_email']
        Ecourse_id=courseid+'**'+t_email
        obs=before_final_table.objects.filter(CourseidandTeacherid=Ecourse_id).filter(Student_id=request.session.get('email'))
        obs1=before_final_table.objects.filter(CourseidandTeacherid=Ecourse_id).filter(Student_id='Exam Roll')
        if not before_final_table.objects.filter(CourseidandTeacherid=Ecourse_id).filter(Student_id="~~THE_END~~").exists():
            messages.info(request, mark_safe('Keep Clam <br/> and hope that <br/> exam result will be good'))
            return HttpResponseRedirect('select_result_as_student.html')

        dic={}

        for i in range(3,12):
            dic[obs1.values_list()[0][i]]=obs.values_list()[0][i]
        dic.__delitem__('None')
        per={
            'id':request.session.get('email'),
            'name':student.objects.filter(sid=request.session.get('email')).values_list()[0][1],
            'semester':request.POST.get('sSemester'),
            'course':request.POST.get('SCourse'),
            'session':request.POST.get('Ssession')
        }
        request.session['all']={'per':per,'dic':dic}
        return HttpResponseRedirect('show_before_final.html')


@is_allowed
def before_final(request):
    Ecoursid = request.session['all_info']['courseid'] + '**' + request.session.get('email')
    if request.method=='POST':
        if not before_final_table.objects.filter(CourseidandTeacherid=Ecoursid).filter(Student_id='~~THE_END~~').exists():
            sv=before_final_table(
                CourseidandTeacherid=Ecoursid,
                Student_id='~~THE_END~~'
            )
            sv.save()
    table_data = before_final_table.objects.filter(CourseidandTeacherid=Ecoursid).order_by('Student_id')
    if not table_data.exists():
        return HttpResponseRedirect('select_result_as_teacher.html')
    contents = {}
    lst=1
    if table_data[len(table_data) - 1].Student_id=='~~THE_END~~':
        lst=2
    contents[0] = table_data[len(table_data) - lst]
    for i in range(0, len(table_data) - lst):
        contents[i + 1] = table_data[i]
    if lst==2:
        contents[len(table_data)-1]=table_data[len(table_data)-1]
    all={
        'constt':contents,
        'head':request.session['all_info']
    }
    return render(request, 'teacher_beforeFinal.html', {'cons': all})
from django.views.decorators.csrf import csrf_protect
@is_allowed
@csrf_protect
def saving(request):
    Ecoursid=request.session['all_info']['courseid']+'**'+request.session.get('email')
    tabtmp1=request.POST
    tabtmp1=tabtmp1.dict()
    print(tabtmp1)
    tabtmp1.popitem()
    tabtmp1=list(tabtmp1.values())
    tabtmp2=before_final_table.objects.filter(CourseidandTeacherid=Ecoursid).filter(Student_id=tabtmp1[0])
    updt=before_final_table.objects.get(id=tabtmp2[0].id)
    updt.Student_id = tabtmp1[0]
    updt.A = tabtmp1[1]
    updt.B = tabtmp1[2]
    updt.C = tabtmp1[3]
    updt.D = tabtmp1[4]
    updt.E = tabtmp1[5]
    updt.F = tabtmp1[6]
    updt.G = tabtmp1[7]
    updt.H = tabtmp1[8]
    updt.I = tabtmp1[9]
    updt.save()
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
                A='Total',
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
                if before_final_table.objects.filter(CourseidandTeacherid=Ecoursid).filter(Student_id=i['sid']).exists():
                    continue
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

def admin_home(request):
    all={
        'teacher':teacher.objects.all().values()
    }
    # print(all)
    return render(request,'admin_home.html',{'all':all});
def who_are_u(request):
    return render(request,'who_are_you.html')
@is_allowed_student
def show_before_final(request):
    if  request.session.get('all'):
        dic=request.session['all']
        return render(request, 'show_before_final.html', {'all': dic})
    else:
        return HttpResponseRedirect('select_result_as_student.html')

