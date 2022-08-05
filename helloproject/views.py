from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .models.product import prod
from .models.signup_teacher import signup_teacher
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def index(request):
    produ = prod.get_all_products()
    return render(request, 'index.html', {'productss': produ})

def signin_T(request):
    if request.method=='GET':
        return render(request, 'teacherlogin.html')
    li=signup_teacher.objects.filter(email=request.POST.get('email')).values('password')
    if len(li)==0:
        messages.error(request,"The email address that you've entered doesn't match any account.")
        return HttpResponseRedirect('/teacherlogin.html')
    x=li[0]['password']
    if check_password(request.POST.get('password'),x)==True:
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
    if str[0]=='P':
        messages.success(request, str)
    else:
        messages.error(request,str)
    return HttpResponseRedirect('/register_user.html')
@login_required(login_url="index.html")
def selectresult(request):
    if request.method=='GET':
        return render(request,'teacherresult.html')
    return HttpResponseRedirect('/teacher_beforeFinal.html')
@login_required(login_url="index.html")
def fun(request):
    if request.method=='POST':
        print(list(request.POST.items()))
    row=[]
    for i in range(0,25):
        row.append(i)
    return render(request,'teacher_beforeFinal.html',{'rowu':row})
@login_required(login_url="index.html")
def saving(request):
    print(request.POST)
    return JsonResponse({'message':'hendeled'})