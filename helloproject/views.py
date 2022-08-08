import datetime

from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .models.signup_teacher import signup_teacher
from .models.beforefinalbatch13 import marks_1s
import pandas as pd
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from helloproject.middlewares.auth import is_allowed


def index(request):
    return render(request,'index.html')

def signin_T(request):
    if request.method == 'GET':
        return render(request, 'teacherlogin.html')
    sir = signup_teacher.objects.filter(email=request.POST.get('email'))
    if len(sir) == 0:
        messages.error(request, "The email address that you've entered doesn't match any account.")
        return HttpResponseRedirect('/teacherlogin.html')
    if check_password(request.POST.get('password'), sir.get().password) == True:
        request.session['email']= sir.get().email
        return HttpResponseRedirect('/teacherresult.html')
    else:
        messages.error(request, "The password you entered is incorrect. Did you forget your password?")
        return HttpResponseRedirect('/teacherlogin.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'register_users.html')
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
        Teacherob = signup_teacher(
            full_name=full_name,
            email=email,
            password=make_password(password))
        Teacherob.reg()
    if str[0] == 'P':
        messages.success(request, str)
    else:
        messages.error(request, str)
    return HttpResponseRedirect('/register_user.html')


@is_allowed
def selectresult(request):
    print(request.session.get('email'))
    if request.method == 'GET':
        return render(request, 'teacherresult.html')
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
