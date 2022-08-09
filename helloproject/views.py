from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .models.teacher import teacher
from .models.student import student
from .models.beforefinalbatch13 import marks_1s
import pandas as pd
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from helloproject.middlewares.auth import is_allowed, is_allowed_student


def index(request):
    return render(request,'index.html')

def signin_T(request):
    if request.method == 'GET':
        return render(request, 'teacherlogin.html')
    sir = teacher.objects.filter(email=request.POST.get('email'))
    if len(sir) == 0:
        messages.error(request, "The email address that you've entered doesn't match any account.")
        return HttpResponseRedirect('/teacherlogin.html')
    if check_password(request.POST.get('password'), sir.get().password) == True:
        request.session['email']= sir.get().email
        return HttpResponseRedirect('/select_result_as_teacher.html')
    else:
        messages.error(request, "The password you entered is incorrect. Did you forget your password?")
        return HttpResponseRedirect('/teacherlogin.html')

def signin_S(request):
    if request.method == 'GET':
        return render(request, 'student_login.html')
    stud =student.objects.filter(id=request.POST.get('sid'))
    if len(stud) == 0:
        messages.error(request, "The ID that you've entered doesn't match any account.")
        return HttpResponseRedirect('student_login.html')
    if check_password(request.POST.get('password'), stud.get().password) == True:
        request.session['email']= stud.get().email
        return HttpResponseRedirect('select_result_as_student.html')
    else:
        messages.error(request, "The password you entered is incorrect. Did you forget your password?")
        return HttpResponseRedirect('student_login.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'register_users.html')
    # print(request.POST.items)
    full_name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    repassword = request.POST.get('repassword')
    str = 'Registration Succsessfull!'
    if password != repassword:
        str = 'Password Not match!'
    elif len(password) == 0:
        str = 'Password too short!'
    else:
        Teacherob = teacher(
            full_name=full_name,
            email=email,
            password=make_password(password))
        Teacherob.reg()
    if str[0] == 'P':
        messages.success(request, str)
    else:
        messages.error(request, str)
    # marks_1s.objects.all().delete();
    return HttpResponseRedirect('/register_user.html')


@is_allowed
def select_result_as_teacher(request):
    if request.method == 'GET':
        return render(request, 'select_result_as_teacher.html')
    return HttpResponseRedirect('/teacher_beforeFinal.html')

@is_allowed_student
def select_result_as_student(request):
    if request.method == 'GET':
        return render(request, 'select_result_as_student.html')
    else:
        return HttpResponseRedirect('/teacher_beforeFinal.html')


@is_allowed
def fun(request):
    if request.method == 'POST':
        print(list(request.POST.items()))
    table_data = marks_1s.objects.all().order_by('Student_id')
    contents = {}
    contents[0] = table_data[len(table_data) - 1]
    for i in range(0, len(table_data) - 1):
        contents[i + 1] = table_data[i]
    for i, j in contents.items():
        print(i, j.Student_id)
    return render(request, 'teacher_beforeFinal.html', {'cons': contents})


@is_allowed
def saving(request):
    print(request.POST)
    return JsonResponse({'message': 'hendeled'})

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
            st = marks_1s(
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
