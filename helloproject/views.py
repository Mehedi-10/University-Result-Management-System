from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .models.product import prod
from .models.signup_teacher import signup_teacher
from django.contrib.auth.hashers import make_password, check_password

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
        return render(request,'teacherlogin.html')
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
        str = 'Password too short'
    else:
        Teacherob = signup_teacher(
            full_name=full_name,
            email=email,
            password=make_password(password))
        Teacherob.reg()
    messages.info(request, str)
    return HttpResponseRedirect('/register_user.html')

